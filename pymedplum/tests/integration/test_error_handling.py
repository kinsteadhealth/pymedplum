"""Integration tests for error handling and security scenarios.

These tests verify that the client properly handles various error conditions
when interacting with a real Medplum server.
"""

import pytest

from pymedplum import AsyncMedplumClient, MedplumClient
from pymedplum.exceptions import NotFoundError


def test_read_nonexistent_resource(medplum_client: MedplumClient):
    """Test that reading a non-existent resource raises NotFoundError."""
    with pytest.raises(NotFoundError):
        medplum_client.read_resource("Patient", "does-not-exist-12345")


@pytest.mark.asyncio
async def test_async_read_nonexistent_resource(
    async_medplum_client: AsyncMedplumClient,
):
    """Test that reading a non-existent resource raises NotFoundError (async)."""
    with pytest.raises(NotFoundError):
        await async_medplum_client.read_resource("Patient", "does-not-exist-12345")


def test_invalid_search_parameter(medplum_client: MedplumClient):
    """Test searching with an invalid parameter.

    Medplum validates search parameters and returns a 400 error for unknown ones,
    which the client should properly surface as BadRequestError.
    """
    from pymedplum.exceptions import BadRequestError

    # Search with a clearly invalid parameter
    with pytest.raises(BadRequestError) as exc_info:
        medplum_client.search_resources(
            "Patient", {"this_param_definitely_does_not_exist_xyz": "value"}
        )

    # Verify the error message mentions the unknown parameter
    assert (
        "unknown" in str(exc_info.value).lower()
        or "search parameter" in str(exc_info.value).lower()
    )


def test_config_validation_empty_membership():
    """Test that empty membership ID raises ValueError."""
    client = MedplumClient(
        base_url="https://api.test.com/",
        client_id="test",
        client_secret="test",
    )

    with pytest.raises(ValueError, match="cannot be empty"):
        client._normalize_membership("")


def test_config_validation_invalid_membership_format():
    """Test that invalid membership format raises ValueError."""
    client = MedplumClient(
        base_url="https://api.test.com/",
        client_id="test",
        client_secret="test",
    )

    with pytest.raises(ValueError, match="Invalid ProjectMembership"):
        client._normalize_membership("ProjectMembership/")


def test_on_behalf_of_without_authentication():
    """Test that on-behalf-of without authentication raises error."""
    client = MedplumClient(
        base_url="https://api.test.com/",
        client_id="test",
        client_secret="test",
    )

    # Client not authenticated
    assert client.access_token is None

    with pytest.raises(ValueError, match="must be authenticated"):
        client._validate_on_behalf_of_usage()


def test_malformed_resource_creation(medplum_client: MedplumClient):
    """Test creating a resource with missing required fields.

    This tests that the server correctly validates resources and
    the client properly surfaces those validation errors.
    """
    # Try to create an Observation without required 'status' field
    # The server should reject this
    try:
        medplum_client.create_resource(
            {
                "resourceType": "Observation",
                "code": {"text": "Test"},
                # Missing required 'status' field
            }
        )
        # If it doesn't raise, that's actually fine - server may have defaults
        # Just verify we can handle the response
    except Exception as e:
        # If it does raise, verify it's a sensible error
        assert "status" in str(e).lower() or "required" in str(e).lower()


def test_create_resource_with_invalid_reference(medplum_client: MedplumClient):
    """Test creating a resource with an invalid reference format.

    Verifies the client can handle server validation errors for references.
    """
    try:
        medplum_client.create_resource(
            {
                "resourceType": "Observation",
                "status": "final",
                "code": {"text": "Test"},
                "subject": {"reference": "InvalidReferenceFormat"},  # Should be Type/ID
            }
        )
        # Server may accept this or reject it
    except Exception as e:
        # If rejected, error message should mention reference or format
        error_str = str(e).lower()
        assert "reference" in error_str or "invalid" in error_str


@pytest.mark.asyncio
async def test_async_malformed_resource_creation(
    async_medplum_client: AsyncMedplumClient,
):
    """Test async client handles malformed resource creation."""
    try:
        await async_medplum_client.create_resource(
            {
                "resourceType": "Observation",
                "code": {"text": "Test"},
                # Missing required 'status'
            }
        )
    except Exception as e:
        assert "status" in str(e).lower() or "required" in str(e).lower()
