"""Unit tests for BaseClient shared functionality.

Tests common methods used by both sync and async clients.
"""

import pytest

from pymedplum._base import BaseClient


def test_base_client_initialization():
    """Test BaseClient initialization with various parameters."""
    client = BaseClient(
        base_url="https://test.medplum.com/",
        client_id="test-client",
        client_secret="test-secret",
        project_id="test-project",
        default_on_behalf_of="membership-123",
    )

    assert client.base_url == "https://test.medplum.com/"
    assert client.fhir_base_url == "https://test.medplum.com/fhir/R4/"
    assert client.client_id == "test-client"
    assert client.client_secret == "test-secret"
    assert client.project_id == "test-project"
    # default_on_behalf_of is stored as-is, not normalized
    assert client.default_on_behalf_of == "membership-123"
    assert client._obo_var.get() is None


def test_base_client_custom_fhir_path():
    """Test BaseClient with custom FHIR URL path."""
    client = BaseClient(base_url="https://test.medplum.com/", fhir_url_path="fhir/R4B/")

    assert client.fhir_base_url == "https://test.medplum.com/fhir/R4B/"


def test_normalize_membership_with_string_id():
    """Test membership normalization with plain ID string."""
    client = BaseClient()

    # Plain ID should get prefix
    result = client._normalize_membership("abc-123")
    assert result == "ProjectMembership/abc-123"


def test_build_query_params_with_dict():
    """Test _build_query_params with dictionary input."""
    client = BaseClient()

    # Simple dict
    params = client._build_query_params({"family": "Smith", "given": "John"})
    assert params == [("family", "Smith"), ("given", "John")]


def test_build_query_params_with_list_values():
    """Test _build_query_params handles list values for multi-valued parameters.

    This is essential for FHIR date ranges and other multi-valued searches.
    For example, birthdate with both ge and le prefixes for a date range.
    """
    client = BaseClient()

    # Dict with list value - should create multiple params with same key
    params = client._build_query_params(
        {"family": "Smith", "birthdate": ["ge1990-01-01", "le2000-12-31"]}
    )

    # Should have 3 tuples: one for family, two for birthdate
    assert len(params) == 3
    assert ("family", "Smith") in params
    assert ("birthdate", "ge1990-01-01") in params
    assert ("birthdate", "le2000-12-31") in params


def test_build_query_params_with_string():
    """Test _build_query_params with query string input."""
    client = BaseClient()

    params = client._build_query_params("family=Smith&given=John")
    assert params == [("family", "Smith"), ("given", "John")]


def test_build_query_params_with_list_of_tuples():
    """Test _build_query_params with list of tuples input."""
    client = BaseClient()

    params = client._build_query_params([("family", "Smith"), ("given", "John")])
    assert params == [("family", "Smith"), ("given", "John")]


def test_build_query_params_with_none():
    """Test _build_query_params with None input."""
    client = BaseClient()

    params = client._build_query_params(None)
    assert params == []


def test_build_query_params_invalid_type():
    """Test _build_query_params raises error for invalid input type."""
    client = BaseClient()

    with pytest.raises(ValueError, match="Invalid query type"):
        client._build_query_params(12345)


def test_normalize_membership_with_full_reference():
    """Test membership normalization with full reference."""
    client = BaseClient()

    # Full reference should stay as-is
    result = client._normalize_membership("ProjectMembership/abc-123")
    assert result == "ProjectMembership/abc-123"


def test_normalize_membership_with_resource_object():
    """Test membership normalization with resource object."""
    client = BaseClient()

    # Mock resource object with id attribute
    class MockMembership:
        id = "resource-456"

    result = client._normalize_membership(MockMembership())
    assert result == "ProjectMembership/resource-456"


def test_normalize_membership_empty_string_error():
    """Test membership normalization rejects empty string."""
    client = BaseClient()

    with pytest.raises(ValueError, match="cannot be empty"):
        client._normalize_membership("")


def test_normalize_membership_missing_id_error():
    """Test membership normalization rejects resource without id."""
    client = BaseClient()

    class MockMembershipNoId:
        pass

    with pytest.raises(ValueError, match="must have an id"):
        client._normalize_membership(MockMembershipNoId())


def test_get_headers_with_token():
    """Test header generation with access token."""
    client = BaseClient(access_token="test-token-123")

    headers = client._get_headers()

    assert headers["Accept"] == "application/fhir+json"
    assert headers["Content-Type"] == "application/fhir+json"
    assert headers["X-Medplum"] == "extended"
    assert headers["Authorization"] == "Bearer test-token-123"


def test_get_headers_without_token():
    """Test header generation without access token."""
    client = BaseClient()

    headers = client._get_headers()

    assert "Authorization" not in headers
    assert headers["X-Medplum"] == "extended"


def test_get_headers_with_default_on_behalf_of():
    """Test headers include default on-behalf-of (normalized)."""
    client = BaseClient(
        access_token="test-token", default_on_behalf_of="default-membership"
    )

    headers = client._get_headers()

    # Header value should be normalized with ProjectMembership/ prefix
    assert headers["X-Medplum-On-Behalf-Of"] == "ProjectMembership/default-membership"


def test_get_headers_obo_stack_overrides_default():
    """Test ambient OBO ContextVar takes precedence over default."""
    client = BaseClient(
        access_token="test-token", default_on_behalf_of="default-membership"
    )

    token = client._obo_var.set("ProjectMembership/active-membership")
    try:
        headers = client._get_headers()
    finally:
        client._obo_var.reset(token)

    # Active OBO should override default
    assert headers["X-Medplum-On-Behalf-Of"] == "ProjectMembership/active-membership"


def test_obo_current_empty_stack():
    """Test _obo_current returns None when ContextVar is unset."""
    client = BaseClient()

    assert client._obo_current() is None


def test_obo_current_with_values():
    """Test _obo_current returns the ambient ContextVar value."""
    client = BaseClient()

    t1 = client._obo_var.set("ProjectMembership/first")
    assert client._obo_current() == "ProjectMembership/first"

    t2 = client._obo_var.set("ProjectMembership/second")
    assert client._obo_current() == "ProjectMembership/second"

    client._obo_var.reset(t2)
    client._obo_var.reset(t1)


def test_build_query_params_from_dict():
    """Test query parameter building from dict."""
    client = BaseClient()

    params = client._build_query_params({"name": "John", "gender": "male"})

    assert ("name", "John") in params
    assert ("gender", "male") in params


def test_build_query_params_from_string():
    """Test query parameter building from query string."""
    client = BaseClient()

    params = client._build_query_params("name=John&gender=male")

    assert ("name", "John") in params
    assert ("gender", "male") in params


def test_build_query_params_from_list():
    """Test query parameter building from list of tuples."""
    client = BaseClient()

    params = client._build_query_params([("name", "John"), ("name", "Jane")])

    # Should preserve duplicate keys
    assert params.count(("name", "John")) == 1
    assert params.count(("name", "Jane")) == 1


def test_build_query_params_none():
    """Test query parameter building with None."""
    client = BaseClient()

    params = client._build_query_params(None)

    assert params == []


def test_should_refresh_token_no_expiration():
    """Test token refresh check with no expiration set."""
    client = BaseClient(access_token="test-token")

    assert client._should_refresh_token() is False


def test_should_refresh_token_not_expired():
    """Test token refresh check with unexpired token."""
    from datetime import datetime, timedelta, timezone

    client = BaseClient(access_token="test-token")
    client.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=300)

    assert client._should_refresh_token() is False


def test_should_refresh_token_expired():
    """Test token refresh check with expired token."""
    from datetime import datetime, timedelta, timezone

    client = BaseClient(access_token="test-token")
    # Set expiration to past (needs refresh)
    client.token_expires_at = datetime.now(timezone.utc) - timedelta(seconds=10)

    assert client._should_refresh_token() is True


def test_should_refresh_token_soon_to_expire():
    """Test token refresh check with soon-to-expire token (< 60s)."""
    from datetime import datetime, timedelta, timezone

    client = BaseClient(access_token="test-token")
    # Set expiration to 30 seconds from now (should trigger refresh)
    client.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=30)

    assert client._should_refresh_token() is True


def test_validate_on_behalf_of_usage_without_token():
    """Test OBO validation rejects usage without token."""
    client = BaseClient(client_id="test", client_secret="test")

    with pytest.raises(ValueError, match="must be authenticated"):
        client._validate_on_behalf_of_usage()


def test_validate_on_behalf_of_usage_with_token():
    """Test OBO validation passes with token."""
    client = BaseClient(
        client_id="test", client_secret="test", access_token="test-token"
    )

    # Should not raise
    client._validate_on_behalf_of_usage()


def test_validate_on_behalf_of_usage_warns_without_secret():
    """Test OBO validation warns when client_id exists without secret."""
    import warnings

    client = BaseClient(client_id="test", access_token="test-token")

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        client._validate_on_behalf_of_usage()

        assert len(w) == 1
        assert "should only be used with ClientApplication" in str(w[0].message)


def test_attempt_tracker_record_appends_monotonic():
    from datetime import datetime, timezone

    from pymedplum._base import _AttemptTracker

    tracker = _AttemptTracker(
        method="GET",
        url="https://api.example.com/fhir/R4/Patient/123",
        started_at=datetime.now(timezone.utc),
    )
    tracker.record(
        status_code=200, duration_seconds=0.1, on_behalf_of=None, exception=None
    )
    tracker.record(
        status_code=429,
        duration_seconds=0.2,
        on_behalf_of="ProjectMembership/abc",
        exception=None,
    )

    assert [a.attempt_number for a in tracker.attempts] == [1, 2]
    assert tracker.attempts[0].status_code == 200
    assert tracker.attempts[1].on_behalf_of == "ProjectMembership/abc"


@pytest.fixture
def built_event_with_fhir_url():
    from datetime import datetime, timezone

    from pymedplum._base import _AttemptTracker

    started = datetime.now(timezone.utc)
    tracker = _AttemptTracker(
        method="GET",
        url="https://api.example.com/fhir/R4/Patient/123?_count=5",
        started_at=started,
    )
    tracker.record(
        status_code=200, duration_seconds=0.05, on_behalf_of=None, exception=None
    )
    tracker.final_status_code = 200
    ended = datetime.now(timezone.utc)
    return tracker.build_event(ended), started, ended


def test_attempt_tracker_build_event_populates_fhir_identity(
    built_event_with_fhir_url,
):
    event, _, _ = built_event_with_fhir_url
    assert event.method == "GET"
    assert event.resource_type == "Patient"
    assert event.resource_id == "123"


def test_attempt_tracker_build_event_populates_path_template_and_query(
    built_event_with_fhir_url,
):
    event, _, _ = built_event_with_fhir_url
    assert event.path_template == "/fhir/R4/Patient/{id}"
    assert event.query_params == {"_count": ["5"]}


def test_attempt_tracker_build_event_populates_timing_and_status(
    built_event_with_fhir_url,
):
    event, started, ended = built_event_with_fhir_url
    assert event.started_at is started
    assert event.ended_at is ended
    assert event.final_status_code == 200
    assert len(event.attempts) == 1


def test_retry_delay_429_and_5xx_and_terminal():
    import httpx

    from pymedplum._base import _retry_delay

    req = httpx.Request("GET", "https://example.test/")
    r429 = httpx.Response(429, request=req)
    delay = _retry_delay(r429, attempt=0, method="GET", headers=None)
    assert delay is not None
    assert delay >= 0.0

    r503 = httpx.Response(503, request=req)
    assert _retry_delay(r503, attempt=0, method="GET", headers=None) is not None

    r200 = httpx.Response(200, request=req)
    assert _retry_delay(r200, attempt=0, method="GET", headers=None) is None


def test_retry_delay_gates_502_504_on_idempotency():
    """502/504 must not replay a bare POST — they can arrive after the
    origin committed the write, so a retry creates a duplicate resource."""
    import httpx

    from pymedplum._base import _retry_delay

    req = httpx.Request("POST", "https://example.test/")
    for status in (502, 504):
        resp = httpx.Response(status, request=req)
        assert _retry_delay(resp, attempt=0, method="POST", headers=None) is None
        assert _retry_delay(resp, attempt=0, method="PATCH", headers=None) is None
        # Idempotent methods still retry.
        assert _retry_delay(resp, attempt=0, method="PUT", headers=None) is not None
        assert _retry_delay(resp, attempt=0, method="DELETE", headers=None) is not None
        # Conditional create is replay-safe server-side.
        assert (
            _retry_delay(
                resp,
                attempt=0,
                method="POST",
                headers={"If-None-Exist": "identifier=MRN|1"},
            )
            is not None
        )


def test_retry_delay_503_and_429_retry_every_method():
    """503 (no healthy upstream) and 429 (rate limit) are rejected before
    processing, so a bare POST is replay-safe for both."""
    import httpx

    from pymedplum._base import _retry_delay

    req = httpx.Request("POST", "https://example.test/")
    for status in (503, 429):
        resp = httpx.Response(status, request=req)
        assert _retry_delay(resp, attempt=0, method="POST", headers=None) is not None
        assert _retry_delay(resp, attempt=0, method="PATCH", headers=None) is not None


def test_is_replay_safe_requires_nonempty_if_none_exist():
    """An empty/blank If-None-Exist is not a conditional create
    server-side, so a bare POST carrying it must stay non-replay-safe."""
    from pymedplum._base import _is_replay_safe

    assert _is_replay_safe("POST", {"If-None-Exist": ""}) is False
    assert _is_replay_safe("POST", {"If-None-Exist": "   "}) is False
    assert _is_replay_safe("POST", {"if-none-exist": "identifier=MRN|1"}) is True
    assert _is_replay_safe("POST", None) is False
    # PATCH is never replay-safe, even with an If-None-Exist header.
    assert _is_replay_safe("PATCH", {"If-None-Exist": "x"}) is False
    # Idempotent methods are always safe.
    assert _is_replay_safe("GET", None) is True
    assert _is_replay_safe("delete", None) is True


def test_build_timeout_splits_connect_from_read():
    """A flat timeout becomes a short connect + the caller's read/write/pool,
    so a stuck TCP connect can't pin a worker for the full read budget."""
    import httpx

    from pymedplum._base import _build_timeout

    t = _build_timeout(30.0)
    assert t.connect == 5.0
    assert t.read == 30.0
    assert t.write == 30.0
    assert t.pool == 30.0

    # A timeout shorter than the connect default keeps the smaller value.
    assert _build_timeout(2.0).connect == 2.0

    # An explicit httpx.Timeout is passed through untouched.
    custom = httpx.Timeout(10.0, connect=1.0)
    assert _build_timeout(custom) is custom


def test_is_transport_retryable_presend_vs_ambiguous():
    """Pre-send failures retry for any method; ambiguous ones only when
    replay-safe (idempotent method or POST with If-None-Exist)."""
    import httpx

    from pymedplum._base import _is_transport_retryable

    # Pre-send: request never reached the server → any method.
    for exc in (
        httpx.ConnectError("x"),
        httpx.ConnectTimeout("x"),
        httpx.PoolTimeout("x"),
    ):
        assert _is_transport_retryable(exc, "POST", None) is True
        assert _is_transport_retryable(exc, "GET", None) is True

    # Ambiguous: sent, maybe processed → replay-safe only.
    for exc in (
        httpx.ReadTimeout("x"),
        httpx.WriteTimeout("x"),
        httpx.RemoteProtocolError("Server disconnected"),
    ):
        assert _is_transport_retryable(exc, "POST", None) is False
        assert _is_transport_retryable(exc, "GET", None) is True
        assert (
            _is_transport_retryable(exc, "POST", {"If-None-Exist": "identifier=MRN|1"})
            is True
        )


def test_transport_budget_exceeded():
    from pymedplum._base import _transport_budget_exceeded

    assert _transport_budget_exceeded(0) is False
    assert _transport_budget_exceeded(1) is False
    assert _transport_budget_exceeded(2) is True


def test_retry_budget_exceeded_caps_correctly():
    from pymedplum._base import _retry_budget_exceeded

    # 429 has a budget of 5 retries — so attempt 4 still gets one more,
    # attempt 5 does not.
    assert _retry_budget_exceeded(429, 4) is False
    assert _retry_budget_exceeded(429, 5) is True

    # 5xx has a budget of 2 retries.
    assert _retry_budget_exceeded(503, 1) is False
    assert _retry_budget_exceeded(503, 2) is True


def test_normalize_membership_rejects_profile_references():
    """Profile references must fail loudly instead of being mangled into
    'ProjectMembership/Practitioner/abc' and failing server-side."""
    client = BaseClient()

    for bad in ("Practitioner/abc", "Patient/abc", "ProjectMembership/"):
        with pytest.raises(ValueError):
            client._normalize_membership(bad)

    assert (
        client._normalize_membership("ProjectMembership/abc") == "ProjectMembership/abc"
    )


def test_build_query_params_coerces_bools_to_fhir_tokens():
    """Medplum rejects 'True'/'False' with a 400; only lowercase is valid."""
    client = BaseClient()

    assert client._build_query_params({"active": True}) == [("active", "true")]
    assert client._build_query_params({"active": False}) == [("active", "false")]
    assert client._build_query_params([("active", True)]) == [("active", "true")]
    assert client._build_query_params({"status": [True, "draft"]}) == [
        ("status", "true"),
        ("status", "draft"),
    ]


def test_build_query_params_skips_none_values():
    """str(None) would send the literal token 'None' — a valid search
    value that silently matches nothing."""
    client = BaseClient()

    assert client._build_query_params({"identifier": None}) == []
    assert client._build_query_params({"identifier": None, "family": "Smith"}) == [
        ("family", "Smith")
    ]
    assert client._build_query_params([("identifier", None)]) == []
    assert client._build_query_params({"birthdate": ["ge1990", None]}) == [
        ("birthdate", "ge1990")
    ]


def test_merge_params_into_url_preserves_existing_query():
    """httpx.URL(url, params=...) would *replace* the query string,
    silently dropping params already embedded in the URL."""
    from pymedplum._base import _merge_params_into_url

    merged = _merge_params_into_url(
        "https://api.medplum.com/fhir/R4/Patient?name=smith",
        [("active", "true")],
    )
    assert "name=smith" in merged
    assert "active=true" in merged

    # No params: URL unchanged.
    url = "https://api.medplum.com/fhir/R4/Patient?name=smith"
    assert _merge_params_into_url(url, None) == url
