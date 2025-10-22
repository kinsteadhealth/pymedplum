"""Unit tests for MedplumClient error handling with mocked HTTP responses"""

from datetime import datetime, timedelta

import httpx
import pytest
import respx

from pymedplum.client import MedplumClient
from pymedplum.exceptions import (
    AuthorizationError,
    BadRequestError,
    MedplumError,
    NotFoundError,
)


@pytest.fixture
def mock_client():
    """Create a MedplumClient for testing"""
    return MedplumClient(
        base_url="https://api.medplum.com",
        client_id="test-client-id",
        client_secret="test-client-secret",
    )


@respx.mock
def test_authorization_error_on_403(mock_client):
    """Test that 403 responses raise AuthorizationError"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read request to return 403
    respx.get("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(
            status_code=403,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "forbidden",
                        "details": {"text": "Access denied"},
                    }
                ],
            },
        )
    )

    with pytest.raises(AuthorizationError) as exc_info:
        mock_client.read_resource("Patient", "123")

    assert "Access denied" in str(exc_info.value)


@respx.mock
def test_not_found_error_on_404(mock_client):
    """Test that 404 responses raise NotFoundError"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read request to return 404
    respx.get("https://api.medplum.com/fhir/R4/Patient/nonexistent").mock(
        return_value=httpx.Response(
            status_code=404,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "not-found",
                        "details": {"text": "Resource not found"},
                    }
                ],
            },
        )
    )

    with pytest.raises(NotFoundError) as exc_info:
        mock_client.read_resource("Patient", "nonexistent")

    assert "Resource not found" in str(exc_info.value)


@respx.mock
def test_bad_request_error_on_400(mock_client):
    """Test that 400 responses raise BadRequestError"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the create request to return 400
    respx.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            status_code=400,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "invalid",
                        "details": {"text": "Invalid resource"},
                    }
                ],
            },
        )
    )

    with pytest.raises(BadRequestError) as exc_info:
        mock_client.create_resource({"resourceType": "Patient"})

    assert "Invalid resource" in str(exc_info.value)


@respx.mock
def test_generic_error_on_500(mock_client):
    """Test that 500 responses raise generic MedplumError"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read request to return 500
    respx.get("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(
            status_code=500,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "exception",
                        "details": {"text": "Internal server error"},
                    }
                ],
            },
        )
    )

    with pytest.raises(MedplumError) as exc_info:
        mock_client.read_resource("Patient", "123")

    assert "Internal server error" in str(exc_info.value)


@respx.mock
def test_network_error_handling(mock_client):
    """Test that network errors are properly handled"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read request to raise a network error
    respx.get("https://api.medplum.com/fhir/R4/Patient/123").mock(
        side_effect=httpx.ConnectError("Connection failed")
    )

    with pytest.raises(httpx.ConnectError):
        mock_client.read_resource("Patient", "123")


@respx.mock
def test_malformed_response_handling(mock_client):
    """Test handling of malformed JSON responses"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read request to return malformed JSON
    respx.get("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(status_code=200, content=b"{invalid json")
    )

    with pytest.raises(Exception):  # Could be JSONDecodeError or similar
        mock_client.read_resource("Patient", "123")


@respx.mock
def test_on_behalf_of_header_is_sent(mock_client):
    """Test that X-Medplum-On-Behalf-Of header is properly sent"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read request and capture headers
    read_route = respx.get("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(
            status_code=200, json={"resourceType": "Patient", "id": "123"}
        )
    )

    # Authenticate first - manually set token to avoid HTTP call
    mock_client.access_token = "test-token"
    from datetime import timezone

    mock_client.token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    # Make request with on_behalf_of
    with mock_client.on_behalf_of("pm-123"):
        mock_client.read_resource("Patient", "123")

    # Verify the header was sent
    assert read_route.call_count == 1
    first_request = read_route.calls[0].request
    assert (
        first_request.headers.get("X-Medplum-On-Behalf-Of")
        == "ProjectMembership/pm-123"
    )


@respx.mock
def test_on_behalf_of_context_cleanup(mock_client):
    """Test that on_behalf_of context is properly cleaned up"""
    # Mock successful auth
    respx.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "test-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )
    )

    # Mock the read requests
    read_route = respx.get("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(
            status_code=200, json={"resourceType": "Patient", "id": "123"}
        )
    )

    # Authenticate first - manually set token to avoid HTTP call
    mock_client.access_token = "test-token"
    from datetime import timezone

    mock_client.token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    # Request inside context should have header
    with mock_client.on_behalf_of("pm-123"):
        mock_client.read_resource("Patient", "123")
        assert (
            read_route.calls[0].request.headers.get("X-Medplum-On-Behalf-Of")
            == "ProjectMembership/pm-123"
        )

    # Request outside context should NOT have header
    mock_client.read_resource("Patient", "123")
    assert read_route.calls[1].request.headers.get("X-Medplum-On-Behalf-Of") is None
