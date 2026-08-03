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
    from datetime import datetime, timedelta, timezone

    client = MedplumClient(
        base_url="https://api.test.medplum.com/",
        client_id="test-client",
        client_secret="test-secret",
        access_token="test-token",
    )
    # Guard the token manager from proactive refresh for the duration of
    # the test: no expiry is set on the JWT, so without this it would
    # treat the token as MANAGED with no parsed expiry and skip proactive
    # refresh anyway — but we bump expiry far into the future to keep
    # the retry tests free of any token-endpoint mocking.
    client._tokens.token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    yield client
    client.close()


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


def test_post_create_not_replayed_on_502(mock_client):
    """A bare POST must not be replayed on 5xx — a 502/504 can arrive
    after the origin committed the write, so a replay would create a
    duplicate clinical resource. Exactly one wire call."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(return_value=httpx.Response(502, text="Bad Gateway"))

        with pytest.raises(ServerError) as exc_info:
            mock_client.create_resource({"resourceType": "Patient"})

        assert exc_info.value.status_code == 502
        assert route.call_count == 1


def test_post_create_not_replayed_on_503(mock_client):
    """503 is ambiguous like 502/504 — a draining pod mid-deploy can emit
    it after committing the write, so a bare POST must not be replayed."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(return_value=httpx.Response(503, text="Service Unavailable"))

        with pytest.raises(ServerError) as exc_info:
            mock_client.create_resource({"resourceType": "Patient"})

        assert exc_info.value.status_code == 503
        assert route.call_count == 1


def test_get_retried_on_503(mock_client):
    """Idempotent methods keep the 503 retry — only non-replay-safe
    writes went terminal when 503 joined the ambiguous-commit set."""
    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/p1")
        route.mock(
            side_effect=[
                httpx.Response(503, text="Service Unavailable"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "p1"}),
            ]
        )

        result = mock_client.read_resource("Patient", "p1")
        assert result["id"] == "p1"
        assert route.call_count == 2


def test_post_create_not_replayed_on_504(mock_client):
    """504 (gateway timeout) is ambiguous like 502 — a bare POST must
    not be replayed."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(return_value=httpx.Response(504, text="Gateway Timeout"))

        with pytest.raises(ServerError) as exc_info:
            mock_client.create_resource({"resourceType": "Patient"})

        assert exc_info.value.status_code == 504
        assert route.call_count == 1


def test_post_conditional_create_retried_on_502(mock_client):
    """POST with If-None-Exist is replay-safe server-side (conditional
    create is transactional), so it keeps the 5xx retry."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(
            side_effect=[
                httpx.Response(502, text="Bad Gateway"),
                httpx.Response(201, json={"resourceType": "Patient", "id": "p1"}),
            ]
        )

        result = mock_client.create_resource_if_none_exist(
            {"resourceType": "Patient"}, "identifier=MRN|123"
        )
        assert result["id"] == "p1"
        assert route.call_count == 2


def test_put_update_retried_on_502(mock_client):
    """PUT is idempotent and keeps the 5xx retry."""
    with respx.mock:
        route = respx.put("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(502, text="Bad Gateway"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.update_resource({"resourceType": "Patient", "id": "123"})
        assert result["id"] == "123"
        assert route.call_count == 2


def test_post_still_retried_on_429(mock_client):
    """429 means the request was rejected before processing — replaying
    any method, including bare POST, cannot duplicate a write."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(
            side_effect=[
                httpx.Response(429, headers={"Retry-After": "0"}),
                httpx.Response(201, json={"resourceType": "Patient", "id": "p1"}),
            ]
        )

        result = mock_client.create_resource({"resourceType": "Patient"})
        assert result["id"] == "p1"
        assert route.call_count == 2


def test_get_retried_on_connect_error(mock_client):
    """A connect-level failure (pre-send) is retried for any method and
    succeeds once the connection recovers — the routine ECS/ALB
    connection-churn case."""
    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.ConnectError("connection reset"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 2


def test_post_create_retried_on_connect_error(mock_client):
    """ConnectError is pre-send (request never reached the server), so even
    a bare POST is safe to retry — no duplicate-write risk."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(
            side_effect=[
                httpx.ConnectError("connection refused"),
                httpx.Response(201, json={"resourceType": "Patient", "id": "p1"}),
            ]
        )

        result = mock_client.create_resource({"resourceType": "Patient"})
        assert result["id"] == "p1"
        assert route.call_count == 2


def test_post_create_not_retried_on_read_timeout(mock_client):
    """A read timeout is ambiguous (the request was sent; the write may
    have committed), so a bare POST is NOT replayed — it surfaces as
    NetworkError after a single attempt."""
    from pymedplum.exceptions import NetworkError

    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(side_effect=httpx.ReadTimeout("read timed out"))

        with pytest.raises(NetworkError):
            mock_client.create_resource({"resourceType": "Patient"})

        assert route.call_count == 1


def test_get_retried_on_read_timeout(mock_client):
    """A read timeout on an idempotent GET is safe to retry."""
    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.ReadTimeout("read timed out"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        assert route.call_count == 2


def test_conditional_create_retried_on_remote_protocol_error(mock_client):
    """A stale-keepalive 'server disconnected' is ambiguous, but a
    conditional create (If-None-Exist) is replay-safe, so it retries."""
    with respx.mock:
        route = respx.post("https://api.test.medplum.com/fhir/R4/Patient")
        route.mock(
            side_effect=[
                httpx.RemoteProtocolError("Server disconnected"),
                httpx.Response(201, json={"resourceType": "Patient", "id": "p1"}),
            ]
        )

        result = mock_client.create_resource_if_none_exist(
            {"resourceType": "Patient"}, "identifier=MRN|123"
        )
        assert result["id"] == "p1"
        assert route.call_count == 2


def test_transport_error_exhausts_budget_then_networkerror(mock_client):
    """A persistent transport failure retries up to the budget (3 attempts)
    then raises NetworkError."""
    from pymedplum.exceptions import NetworkError

    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(side_effect=httpx.ConnectError("down"))

        with pytest.raises(NetworkError):
            mock_client.read_resource("Patient", "123")

        assert route.call_count == 3


def test_transport_retry_then_success_reports_clean_event(mock_client):
    """A retried-then-succeeded transport error must not leave a stale
    failure on the completion event (final_exception cleared on retry)."""
    events = []
    mock_client._on_request_complete = events.append
    with respx.mock:
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.ConnectError("blip"),
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        mock_client.read_resource("Patient", "123")

    assert len(events) == 1
    assert events[0].final_status_code == 200
    assert events[0].final_exception is None
    # The failed first attempt is still recorded for observability.
    assert len(events[0].attempts) == 2


def test_terminal_transport_error_reports_networkerror_to_hook(mock_client):
    """On a terminal transport failure the completion event carries the
    wrapped NetworkError (not the raw httpx exception) so hooks/telemetry
    observe the SDK type; the raw cause is preserved via __cause__."""
    from pymedplum.exceptions import NetworkError

    events = []
    mock_client._on_request_complete = events.append
    with respx.mock:
        respx.get("https://api.test.medplum.com/fhir/R4/Patient/123").mock(
            side_effect=httpx.ConnectError("down")
        )
        with pytest.raises(NetworkError):
            mock_client.read_resource("Patient", "123")

    assert len(events) == 1
    assert isinstance(events[0].final_exception, NetworkError)
    assert isinstance(events[0].final_exception.__cause__, httpx.ConnectError)


def test_post_refresh_replay_transport_error_is_handled(mock_client):
    """A transport error on the post-401-refresh replay must go through the
    same transport handling (wrapped/retried), not escape as raw httpx —
    the _refresh_and_retry_once replay now sits inside the retry try-block."""
    with respx.mock:
        respx.post("https://api.test.medplum.com/oauth2/token").mock(
            return_value=httpx.Response(
                200, json={"access_token": "fresh", "expires_in": 3600}
            )
        )
        route = respx.get("https://api.test.medplum.com/fhir/R4/Patient/123")
        route.mock(
            side_effect=[
                httpx.Response(401, text="expired"),  # initial → triggers refresh
                httpx.ConnectError("blip on replay"),  # replay after refresh
                httpx.Response(200, json={"resourceType": "Patient", "id": "123"}),
            ]
        )

        result = mock_client.read_resource("Patient", "123")
        assert result["id"] == "123"
        # initial 401 + replay ConnectError + retried success
        assert route.call_count == 3


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
    from datetime import datetime, timedelta, timezone

    scoped_client = MedplumClient(
        base_url="https://api.test.medplum.com/",
        client_id="test-client",
        client_secret="test-secret",
        access_token="test-token",
        default_on_behalf_of="ProjectMembership/456",
    )
    scoped_client._tokens.token_expires_at = datetime.now(timezone.utc) + timedelta(
        hours=1
    )

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
