"""Tests for raw_request escape hatch.

Dangerous-path tests are function-based and assert no wire call is
made via respx — a direct signal that path sanitization short-circuits
before the HTTP layer.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest
import respx

from pymedplum import AsyncMedplumClient
from pymedplum.exceptions import UnsafeRedirectError
from pymedplum.mcp.tools import raw_request
from pymedplum.tests.unit.mcp.conftest import make_fake_obo

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@pytest.fixture
async def real_client() -> AsyncIterator[AsyncMedplumClient]:
    """Real AsyncMedplumClient pointed at the respx-mocked base URL."""
    client = AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        access_token="test-token",
    )
    try:
        yield client
    finally:
        await client.aclose()


@asynccontextmanager
async def _wire_obo(
    client: AsyncMedplumClient, on_behalf_of: str | None = None
) -> AsyncIterator[AsyncMedplumClient]:
    if on_behalf_of is not None:
        async with client.on_behalf_of(on_behalf_of) as obo_client:
            yield obo_client
    else:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bad",
    [
        "https://evil.com/x",
        "//evil.com/x",
        "..\\evil.com",
        "",
        "   ",
    ],
)
async def test_rejects_dangerous_paths_no_wire_call(
    bad: str, real_client: AsyncMedplumClient
) -> None:
    with respx.mock(
        base_url="https://api.medplum.com", assert_all_called=False
    ) as mock:
        # Fallback route — if any wire call escapes sanitization, this
        # route will record it and the assertion below fails.
        mock.route().respond(200, json={"should_not_fire": True})

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with (
            patch("pymedplum.mcp.tools._with_obo", fake),
            pytest.raises(UnsafeRedirectError),
        ):
            await raw_request("GET", bad)
        assert mock.calls.called is False


@pytest.mark.asyncio
async def test_get_happy_path_hits_wire(real_client: AsyncMedplumClient) -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        route = mock.get("/fhir/R4/Patient/1").respond(
            json={"resourceType": "Patient", "id": "1"},
        )

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with patch("pymedplum.mcp.tools._with_obo", fake):
            result = await raw_request("GET", "fhir/R4/Patient/1")

        assert route.called
        assert result["id"] == "1"


@pytest.mark.asyncio
async def test_post_with_body_and_params_on_wire(
    real_client: AsyncMedplumClient,
) -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        route = mock.post("/admin/projects/123/invite").respond(json={"ok": True})

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with patch("pymedplum.mcp.tools._with_obo", fake):
            result = await raw_request(
                "POST",
                "admin/projects/123/invite",
                body={"email": "a@b.com"},
                query_params=[["notify", "true"]],
            )

        assert route.called
        req = route.calls[0].request
        assert req.url.params["notify"] == "true"
        import json as _json

        assert _json.loads(req.content) == {"email": "a@b.com"}
        assert result["ok"] is True


@pytest.mark.asyncio
async def test_obo_is_plumbed_to_wire_header(
    real_client: AsyncMedplumClient,
) -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        route = mock.get("/fhir/R4/Patient/1").respond(
            json={"resourceType": "Patient", "id": "1"},
        )

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with patch("pymedplum.mcp.tools._with_obo", fake):
            await raw_request(
                "GET",
                "fhir/R4/Patient/1",
                on_behalf_of="11111111-1111-1111-1111-111111111111",
            )

        assert route.called
        got = route.calls[0].request.headers.get("X-Medplum-On-Behalf-Of")
        assert got == "ProjectMembership/11111111-1111-1111-1111-111111111111"


@pytest.mark.asyncio
async def test_write_blocked_in_read_only() -> None:
    with (
        patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
        pytest.raises(PermissionError, match="read-only mode"),
    ):
        await raw_request("POST", "fhir/R4/Patient", body={"resourceType": "Patient"})


@pytest.mark.asyncio
async def test_delete_blocked_in_read_only() -> None:
    with (
        patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
        pytest.raises(PermissionError),
    ):
        await raw_request("DELETE", "fhir/R4/Patient/1")


@pytest.mark.asyncio
async def test_get_allowed_in_read_only(real_client: AsyncMedplumClient) -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.get("/auth/me").respond(json={"data": "ok"})

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            patch("pymedplum.mcp.tools._with_obo", fake),
        ):
            result = await raw_request("GET", "auth/me")
        assert result["data"] == "ok"


@pytest.mark.asyncio
async def test_none_response_returns_empty_dict() -> None:
    mock = AsyncMock()
    mock.base_url = "https://api.medplum.com/"
    mock._request.return_value = None
    with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
        result = await raw_request("GET", "fhir/R4/Patient/x")
    assert result == {}


@pytest.mark.asyncio
async def test_falsy_response_preserved() -> None:
    mock = AsyncMock()
    mock.base_url = "https://api.medplum.com/"
    mock._request.return_value = []
    with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
        result = await raw_request("GET", "some/endpoint")
    assert result == []


@pytest.mark.asyncio
async def test_repeated_query_params(real_client: AsyncMedplumClient) -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        route = mock.get(url__regex=r"/fhir/R4/Observation.*").respond(
            json={"resourceType": "Bundle"},
        )

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with patch("pymedplum.mcp.tools._with_obo", fake):
            await raw_request(
                "GET",
                "fhir/R4/Observation",
                query_params=[
                    ["_include", "Observation:subject"],
                    ["_include", "Observation:performer"],
                    ["status", "active"],
                ],
            )

        assert route.called
        req = route.calls[0].request
        # Multi-valued _include preserved on the wire.
        assert req.url.params.get_list("_include") == [
            "Observation:subject",
            "Observation:performer",
        ]
        assert req.url.params["status"] == "active"


@pytest.mark.asyncio
async def test_accepts_relative_path(real_client: AsyncMedplumClient) -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        route = mock.get("/Patient").respond(json={"resourceType": "Patient"})

        @asynccontextmanager
        async def fake(on_behalf_of: str | None = None):
            async with _wire_obo(real_client, on_behalf_of) as c:
                yield c

        with patch("pymedplum.mcp.tools._with_obo", fake):
            result = await raw_request("GET", "Patient")

        assert route.called
        assert result["resourceType"] == "Patient"
