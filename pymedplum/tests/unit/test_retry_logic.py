"""Unit tests for retry logic with exponential backoff and 429 handling"""

import json

import httpx
import pytest
import respx

from pymedplum import MedplumClient
from pymedplum.exceptions import RateLimitError, ServerError


@pytest.fixture
def mock_client():
    """Create a mock client with authentication"""
    client = MedplumClient(
        base_url="https://api.test.medplum.com/",
        client_id="test-client",
        client_secret="test-secret",
    )
    client.access_token = "test-token"
    return client


def test_sync_get_method(mock_client):
    """Test sync get method for non-FHIR endpoints."""
    with respx.mock:
        respx.get("https://api.test.medplum.com/admin/projects/123").mock(
            return_value=httpx.Response(
                200,
                json={"project": {"id": "123", "name": "Test Project"}},
            )
        )

        result = mock_client.get("admin/projects/123")

        assert result["project"]["id"] == "123"
        assert result["project"]["name"] == "Test Project"


def test_retry_429_with_medplum_diagnostics(mock_client):
    """Test that 429 errors parse Medplum diagnostics for wait time"""
    mock_response_data = {
        "resourceType": "OperationOutcome",
        "id": "too-many-requests",
        "issue": [
            {
                "severity": "error",
                "code": "throttled",
                "details": {"text": "Too Many Requests"},
                "diagnostics": json.dumps(
                    {
                        "_remainingPoints": 0,
                        "_msBeforeNext": 50,  # 50ms wait time
                        "_consumedPoints": 10000,
                        "_isFirstInDuration": False,
                        "limit": 50000,
                    }
                ),
            }
        ],
    }

    with respx.mock:
        # First 2 attempts return 429, third succeeds
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(429, json=mock_response_data),
                httpx.Response(429, json=mock_response_data),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 3


def test_retry_429_with_retry_after_header(mock_client):
    """Test that 429 errors use Retry-After header as fallback"""
    with respx.mock:
        # First attempt returns 429 with Retry-After, second succeeds
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(
                    429,
                    headers={"Retry-After": "1"},
                    json={"resourceType": "OperationOutcome"},
                ),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 2


def test_retry_429_max_attempts(mock_client):
    """Test that 429 errors retry up to 5 times before failing"""
    mock_response_data = {
        "resourceType": "OperationOutcome",
        "id": "too-many-requests",
        "issue": [{"severity": "error", "code": "throttled"}],
    }

    with respx.mock:
        # All 6 attempts (initial + 5 retries) return 429
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(return_value=httpx.Response(429, json=mock_response_data))

        with pytest.raises(RateLimitError) as exc_info:
            mock_client.read_resource("Patient", "123")

        assert exc_info.value.status_code == 429
        # Initial attempt + 5 retries = 6 total calls
        assert route.call_count == 6


def test_retry_502_max_attempts(mock_client):
    """Test that 502 errors retry up to 2 times before failing"""
    with respx.mock:
        # All 3 attempts (initial + 2 retries) return 502
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(return_value=httpx.Response(502, text="Bad Gateway"))

        with pytest.raises(ServerError) as exc_info:
            mock_client.read_resource("Patient", "123")

        assert exc_info.value.status_code == 502
        # Initial attempt + 2 retries = 3 total calls
        assert route.call_count == 3


def test_retry_503_eventual_success(mock_client):
    """Test that 503 errors retry and eventually succeed"""
    with respx.mock:
        # First attempt 503, second succeeds
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(503, text="Service Unavailable"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 2


def test_retry_504_eventual_success(mock_client):
    """Test that 504 errors retry and eventually succeed"""
    with respx.mock:
        # First attempt 504, second succeeds
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(504, text="Gateway Timeout"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 2


def test_no_retry_on_400(mock_client):
    """Test that 400 errors do not trigger retries"""
    from pymedplum.exceptions import BadRequestError

    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(return_value=httpx.Response(400, text="Bad Request"))

        with pytest.raises(BadRequestError):
            mock_client.read_resource("Patient", "123")

        # Should only be called once (no retries)
        assert route.call_count == 1


def test_no_retry_on_404(mock_client):
    """Test that 404 errors do not trigger retries"""
    from pymedplum.exceptions import NotFoundError

    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(return_value=httpx.Response(404, text="Not Found"))

        with pytest.raises(NotFoundError):
            mock_client.read_resource("Patient", "123")

        # Should only be called once (no retries)
        assert route.call_count == 1


def test_retry_with_default_on_behalf_of(mock_client):
    """Test that retries work correctly with default_on_behalf_of"""
    # Create client with default_on_behalf_of
    scoped_client = MedplumClient(
        base_url="https://api.test.medplum.com/",
        client_id="test-client",
        client_secret="test-secret",
        default_on_behalf_of="ProjectMembership/456",
    )
    scoped_client.access_token = "test-token"

    with respx.mock:
        # First attempt 429, second succeeds
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(429, json={"resourceType": "OperationOutcome"}),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = scoped_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 2

        # Verify the header was sent in both attempts
        for call in route.calls:
            assert (
                call.request.headers.get("X-Medplum-On-Behalf-Of")
                == "ProjectMembership/456"
            )


def test_execute_bot(mock_client):
    """Test execute_bot method with sync client"""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Bot/bot-123/$execute")
        route.mock(
            return_value=httpx.Response(
                200, json={"result": "success", "data": {"processed": True}}
            )
        )

        result = mock_client.execute_bot(
            bot_id="bot-123",
            input_data={"resourceType": "Patient", "id": "patient-123"},
        )

        assert result["result"] == "success"
        assert result["data"]["processed"] is True
        assert route.call_count == 1
