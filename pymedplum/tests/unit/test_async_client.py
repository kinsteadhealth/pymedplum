"""Unit tests for AsyncMedplumClient with mocked HTTP responses.

Tests async-specific behavior, error handling, and edge cases.
"""

import httpx
import pytest
from respx import MockRouter

# Import pymedplum.fhir first to trigger model rebuilding
import pymedplum.fhir  # noqa: F401
from pymedplum.async_client import AsyncMedplumClient
from pymedplum.exceptions import NotFoundError
from pymedplum.fhir import Patient


@pytest.mark.asyncio
async def test_async_client_context_manager(respx_mock: MockRouter):
    """Test AsyncMedplumClient as async context manager."""
    respx_mock.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "test-token",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )
    )
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient/abc").mock(
        return_value=httpx.Response(200, json={"resourceType": "Patient", "id": "abc"})
    )

    async with AsyncMedplumClient(
        client_id="test-client", client_secret="test-secret"
    ) as client:
        await client.read_resource("Patient", "abc")
        assert client.access_token == "test-token"


@pytest.mark.asyncio
async def test_async_read_resource_not_found(respx_mock: MockRouter):
    """Test async read_resource with 404 response."""
    # Mock authentication
    respx_mock.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            200,
            json={"access_token": "test-token", "expires_in": 3600},
        )
    )

    # Mock 404 response
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient/nonexistent").mock(
        return_value=httpx.Response(
            404,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "not-found",
                        "details": {"text": "Not found"},
                    }
                ],
            },
        )
    )

    async with AsyncMedplumClient(
        client_id="test", client_secret="test", access_token="test-token"
    ) as client:
        with pytest.raises(NotFoundError):
            await client.read_resource("Patient", "nonexistent")


@pytest.mark.asyncio
async def test_async_search_one_no_results(respx_mock: MockRouter):
    """Test async search_one returns None when no results."""
    # Mock search with empty bundle
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.search_one("Patient", {"name": "nonexistent"})

        assert result is None


@pytest.mark.asyncio
async def test_async_update_resource_with_pydantic(respx_mock: MockRouter):
    """Test async update_resource with Pydantic model."""
    # Mock update response
    respx_mock.put("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Patient",
                "id": "123",
                "name": [{"family": "Updated", "given": ["Test"]}],
            },
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        patient = Patient(id="123", name=[{"family": "Updated", "given": ["Test"]}])

        result = await client.update_resource(patient)

        assert result["id"] == "123"
        assert result["name"][0]["family"] == "Updated"


@pytest.mark.asyncio
async def test_async_execute_graphql(respx_mock: MockRouter):
    """Test async execute_graphql method."""
    respx_mock.post("https://api.medplum.com/fhir/R4/$graphql").mock(
        return_value=httpx.Response(
            200,
            json={"data": {"Patient": {"id": "123", "name": [{"family": "Test"}]}}},
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.execute_graphql(
            query="query { Patient(id: $id) { id name { family } } }",
            variables={"id": "123"},
        )

        assert "data" in result
        assert result["data"]["Patient"]["id"] == "123"


@pytest.mark.asyncio
async def test_async_execute_bot(respx_mock: MockRouter):
    """Test async execute_bot method."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Bot/bot-123/$execute").mock(
        return_value=httpx.Response(
            200,
            json={"result": "success", "data": {"processed": True}},
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.execute_bot(
            bot_id="bot-123",
            input_data={"resourceType": "Patient", "id": "patient-123"},
        )

        assert result["result"] == "success"


@pytest.mark.asyncio
async def test_async_invite_user(respx_mock: MockRouter):
    """Test async invite_user method."""
    respx_mock.post("https://api.medplum.com/admin/projects/test-project/invite").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ProjectMembership",
                "id": "membership-123",
                "project": {"reference": "Project/test-project"},
                "user": {"reference": "User/user-123"},
                "profile": {"reference": "Practitioner/practitioner-123"},
            },
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.invite_user(
            project_id="test-project",
            resource_type="Practitioner",
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            password="securepass123",
            send_email=False,
            admin=True,
        )

        assert result["resourceType"] == "ProjectMembership"
        assert result["id"] == "membership-123"


@pytest.mark.asyncio
async def test_async_invite_user_with_access_policy(respx_mock: MockRouter):
    """Test async invite_user with access policy."""
    respx_mock.post("https://api.medplum.com/admin/projects/test-project/invite").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ProjectMembership",
                "id": "membership-456",
            },
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.invite_user(
            project_id="test-project",
            resource_type="Patient",
            first_name="Bob",
            last_name="Jones",
            email="bob@example.com",
            access_policy="AccessPolicy/policy-123",
        )

        assert result["resourceType"] == "ProjectMembership"
        assert result["id"] == "membership-456"


@pytest.mark.asyncio
async def test_async_post(respx_mock: MockRouter):
    """Test async post method."""
    respx_mock.post("https://api.medplum.com/admin/custom/endpoint").mock(
        return_value=httpx.Response(
            200,
            json={"success": True, "message": "Operation completed"},
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.post("admin/custom/endpoint", {"data": "test"})

        assert result["success"] is True
        assert result["message"] == "Operation completed"


@pytest.mark.asyncio
async def test_async_get(respx_mock: MockRouter):
    """Test async get method."""
    respx_mock.get("https://api.medplum.com/admin/projects/123").mock(
        return_value=httpx.Response(
            200,
            json={"project": {"id": "123", "name": "Test Project"}},
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        result = await client.get("admin/projects/123")

        assert result["project"]["id"] == "123"
        assert result["project"]["name"] == "Test Project"


@pytest.mark.asyncio
async def test_async_on_behalf_of_async_context(respx_mock: MockRouter):
    """Test async on_behalf_of async context manager."""
    # Mock create resource
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            201,
            json={"resourceType": "Patient", "id": "123", "name": [{"family": "Test"}]},
        )
    )

    async with AsyncMedplumClient(
        client_id="test", client_secret="test", access_token="test-token"
    ) as client:
        # Verify no OBO before context
        assert client._obo_var.get() is None

        async with client.on_behalf_of("membership-123"):
            # Verify OBO is active
            assert client._obo_var.get() == "ProjectMembership/membership-123"

            # Make a request in context
            result = await client.create_resource(
                {"resourceType": "Patient", "name": [{"family": "Test"}]}
            )
            assert result["id"] == "123"

        # Verify OBO is cleared
        assert client._obo_var.get() is None


@pytest.mark.asyncio
async def test_async_default_on_behalf_of_header(respx_mock: MockRouter):
    """Test async client with default_on_behalf_of sends header."""

    # Mock request that checks headers
    def check_obo_header(request: httpx.Request) -> httpx.Response:
        assert "X-Medplum-On-Behalf-Of" in request.headers
        assert (
            request.headers["X-Medplum-On-Behalf-Of"] == "ProjectMembership/default-123"
        )
        return httpx.Response(
            200, json={"resourceType": "Bundle", "type": "searchset", "entry": []}
        )

    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        side_effect=check_obo_header
    )

    async with AsyncMedplumClient(
        access_token="test-token", default_on_behalf_of="default-123"
    ) as client:
        await client.search_resources("Patient")


@pytest.mark.asyncio
async def test_async_token_refresh(respx_mock: MockRouter):
    """Test async client auto-refreshes expired token."""
    from datetime import datetime, timedelta, timezone

    # Mock authentication responses
    respx_mock.post("https://api.medplum.com/oauth2/token").mock(
        return_value=httpx.Response(
            200, json={"access_token": "refreshed-token", "expires_in": 3600}
        )
    )

    # Mock search request
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200, json={"resourceType": "Bundle", "type": "searchset", "entry": []}
        )
    )

    async with AsyncMedplumClient(
        client_id="test", client_secret="test", access_token="old-token"
    ) as client:
        # Set the token manager's source to MANAGED so the client auto
        # refreshes on near-expiry. Externally-supplied tokens are not
        # auto-refreshed by design; this test predates that contract.
        from pymedplum._auth import TokenSource

        client._tokens.source = TokenSource.MANAGED
        past = datetime.now(timezone.utc) - timedelta(seconds=120)
        client.token_expires_at = past
        client._tokens.token_expires_at = past

        # Should trigger token refresh
        await client.search_resources("Patient")

        # Token should be refreshed
        assert client.access_token == "refreshed-token"


@pytest.mark.asyncio
async def test_async_patch_resource(respx_mock: MockRouter):
    """Test async patch_resource method."""
    respx_mock.patch("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Patient",
                "id": "123",
                "active": True,
                "name": [{"family": "Patched", "given": ["Test"]}],
            },
        )
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        operations = [
            {"op": "replace", "path": "/active", "value": True},
            {"op": "replace", "path": "/name/0/family", "value": "Patched"},
        ]

        result = await client.patch_resource("Patient", "123", operations)

        assert result["id"] == "123"
        assert result["active"] is True
        assert result["name"][0]["family"] == "Patched"


@pytest.mark.asyncio
async def test_async_patch_resource_with_headers(respx_mock: MockRouter):
    """Test async patch_resource with custom headers."""

    def check_headers(request: httpx.Request) -> httpx.Response:
        assert request.headers["Content-Type"] == "application/json-patch+json"
        assert request.headers["If-Match"] == 'W/"1"'
        assert request.headers["X-Custom-Header"] == "custom-value"
        return httpx.Response(
            200,
            json={"resourceType": "Patient", "id": "123", "active": True},
        )

    respx_mock.patch("https://api.medplum.com/fhir/R4/Patient/123").mock(
        side_effect=check_headers
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        operations = [{"op": "replace", "path": "/active", "value": True}]

        await client.patch_resource(
            "Patient",
            "123",
            operations,
            headers={"If-Match": 'W/"1"', "X-Custom-Header": "custom-value"},
        )


@pytest.mark.asyncio
async def test_async_delete_resource(respx_mock: MockRouter):
    """Test async delete_resource method."""
    respx_mock.delete("https://api.medplum.com/fhir/R4/Patient/123").mock(
        return_value=httpx.Response(204)
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        # Should not raise any exception
        await client.delete_resource("Patient", "123")


@pytest.mark.asyncio
async def test_async_delete_resource_with_headers(respx_mock: MockRouter):
    """Test async delete_resource with custom headers."""

    def check_headers(request: httpx.Request) -> httpx.Response:
        assert request.headers["If-Match"] == 'W/"5"'
        assert request.headers["X-Custom-Header"] == "test-value"
        return httpx.Response(204)

    respx_mock.delete("https://api.medplum.com/fhir/R4/Patient/123").mock(
        side_effect=check_headers
    )

    async with AsyncMedplumClient(access_token="test-token") as client:
        await client.delete_resource(
            "Patient",
            "123",
            headers={"If-Match": 'W/"5"', "X-Custom-Header": "test-value"},
        )
