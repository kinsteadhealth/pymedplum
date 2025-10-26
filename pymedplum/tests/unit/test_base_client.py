"""Unit tests for BaseClient shared functionality.

Tests common methods used by both sync and async clients.
"""

import pytest

from pymedplum._base import BaseClient
from pymedplum.types import DEFAULT_ORG_EXTENSION_URL


def test_base_client_initialization():
    """Test BaseClient initialization with various parameters."""
    client = BaseClient(
        base_url="https://test.medplum.com/",
        client_id="test-client",
        client_secret="test-secret",
        project_id="test-project",
        org_mode="accounts",
        org_ref="Organization/test",
        default_on_behalf_of="membership-123",
    )

    assert client.base_url == "https://test.medplum.com/"
    assert client.fhir_base_url == "https://test.medplum.com/fhir/R4/"
    assert client.client_id == "test-client"
    assert client.client_secret == "test-secret"
    assert client.project_id == "test-project"
    assert client.org_mode == "accounts"
    assert client.org_ref == "Organization/test"
    # default_on_behalf_of is stored as-is, not normalized
    assert client.default_on_behalf_of == "membership-123"
    assert len(client._obo_stack) == 0


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
    """Test OBO stack takes precedence over default."""
    client = BaseClient(
        access_token="test-token", default_on_behalf_of="default-membership"
    )

    # Push to OBO stack
    client._obo_stack.append("ProjectMembership/active-membership")

    headers = client._get_headers()

    # Active OBO should override default
    assert headers["X-Medplum-On-Behalf-Of"] == "ProjectMembership/active-membership"


def test_obo_current_empty_stack():
    """Test _obo_current returns None when stack is empty."""
    client = BaseClient()

    assert client._obo_current() is None


def test_obo_current_with_values():
    """Test _obo_current returns top of stack."""
    client = BaseClient()

    client._obo_stack.append("ProjectMembership/first")
    assert client._obo_current() == "ProjectMembership/first"

    client._obo_stack.append("ProjectMembership/second")
    assert client._obo_current() == "ProjectMembership/second"


def test_inject_org_tag_accounts_mode():
    """Test org tag injection in accounts mode."""
    client = BaseClient(org_mode="accounts", org_ref="Organization/ORG_A")

    resource = {"resourceType": "Patient", "name": [{"family": "Test"}]}

    result = client._inject_org_tag(resource)

    assert "meta" in result
    assert "accounts" in result["meta"]
    assert {"reference": "Organization/ORG_A"} in result["meta"]["accounts"]


def test_inject_org_tag_extension_mode():
    """Test org tag injection in extension mode."""
    client = BaseClient(org_mode="extension", org_ref="Organization/ORG_B")

    resource = {"resourceType": "Patient"}

    result = client._inject_org_tag(resource)

    assert "meta" in result
    assert "extension" in result["meta"]

    ext = result["meta"]["extension"][0]
    assert ext["url"] == DEFAULT_ORG_EXTENSION_URL
    assert ext["valueReference"]["reference"] == "Organization/ORG_B"


def test_inject_org_tag_custom_extension_url():
    """Test org tag injection with custom extension URL."""
    custom_url = "https://custom.org/org-tag"
    client = BaseClient(
        org_mode="extension", org_ref="Organization/ORG_C", org_extension_url=custom_url
    )

    resource = {"resourceType": "Patient"}

    result = client._inject_org_tag(resource)

    ext = result["meta"]["extension"][0]
    assert ext["url"] == custom_url


def test_inject_org_tag_idempotent():
    """Test org tag injection is idempotent (doesn't duplicate)."""
    client = BaseClient(org_mode="accounts", org_ref="Organization/ORG_A")

    resource = {"resourceType": "Patient"}

    # Inject twice
    result1 = client._inject_org_tag(resource)
    result2 = client._inject_org_tag(result1)

    # Should only have one account entry
    assert len(result2["meta"]["accounts"]) == 1


def test_inject_org_tag_bundle_recursive():
    """Test org tag injection handles Bundle entries recursively."""
    client = BaseClient(org_mode="accounts", org_ref="Organization/ORG_A")

    bundle = {
        "resourceType": "Bundle",
        "entry": [
            {"resource": {"resourceType": "Patient", "id": "1"}},
            {"resource": {"resourceType": "Patient", "id": "2"}},
        ],
    }

    result = client._inject_org_tag(bundle)

    # Each entry should be tagged
    for entry in result["entry"]:
        assert "meta" in entry["resource"]
        assert "accounts" in entry["resource"]["meta"]


def test_inject_org_tag_no_mode():
    """Test org tag injection does nothing without org_mode."""
    client = BaseClient()

    resource = {"resourceType": "Patient"}
    result = client._inject_org_tag(resource)

    # Should be unchanged
    assert "meta" not in result


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


def test_build_query_params_invalid_type():
    """Test query parameter building rejects invalid type."""
    client = BaseClient()

    with pytest.raises(ValueError, match="Invalid query type"):
        client._build_query_params(12345)


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


def test_token_expiration_from_jwt():
    """Test that token_expires_at is correctly decoded from JWT."""
    import json
    import time
    from base64 import urlsafe_b64encode

    client = BaseClient(access_token="test-token")

    # Create a mock JWT with an 'exp' claim
    exp_time = int(time.time()) + 3600
    payload = {"exp": exp_time}
    # Properly encode the payload
    payload_bytes = json.dumps(payload).encode("utf-8")
    encoded_payload = urlsafe_b64encode(payload_bytes).rstrip(b"=").decode("utf-8")
    mock_jwt = f"header.{encoded_payload}.signature"
    client.access_token = mock_jwt

    # Manually trigger the decoding logic
    from pymedplum.helpers import decode_jwt_exp

    client.token_expires_at = decode_jwt_exp(client.access_token)

    assert client.token_expires_at is not None
    assert abs(client.token_expires_at.timestamp() - exp_time) < 1
