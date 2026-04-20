"""Tests for ``update_resource`` If-Match behavior.

Phase 7: ``update_resource`` auto-attaches ``If-Match: W/"<versionId>"``
from ``meta.versionId`` when the caller hasn't passed an explicit
``If-Match`` header. The ``if_match`` keyword controls this:

- default ``True``: auto-attach when versionId is present
- ``False``: opt out; no If-Match header
- explicit ``str``: use verbatim

Explicit ``headers={"If-Match": ...}`` always wins.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from respx import MockRouter

from pymedplum.async_client import AsyncMedplumClient
from pymedplum.client import MedplumClient

if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture
def sync_client() -> Iterator[MedplumClient]:
    c = MedplumClient(
        base_url="https://api.medplum.com/",
        access_token="tkn",
    )
    try:
        yield c
    finally:
        c.close()


def _mock_update(
    respx_mock: MockRouter, resource_id: str, version_id: str = "5"
) -> httpx.Response:
    route = respx_mock.put(
        f"https://api.medplum.com/fhir/R4/Patient/{resource_id}"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Patient",
                "id": resource_id,
                "meta": {"versionId": version_id},
            },
        )
    )
    return route


def test_update_resource_auto_attaches_if_match(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = _mock_update(respx_mock, "abc")
    resource = {
        "resourceType": "Patient",
        "id": "abc",
        "meta": {"versionId": "4"},
    }
    sync_client.update_resource(resource)
    assert route.called
    request = route.calls[0].request
    assert request.headers.get("If-Match") == 'W/"4"'


def test_update_resource_if_match_false_opts_out(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = _mock_update(respx_mock, "abc")
    resource = {
        "resourceType": "Patient",
        "id": "abc",
        "meta": {"versionId": "4"},
    }
    sync_client.update_resource(resource, if_match=False)
    assert route.called
    request = route.calls[0].request
    assert "if-match" not in {k.lower() for k in request.headers}


def test_update_resource_if_match_custom_string(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = _mock_update(respx_mock, "abc")
    resource = {
        "resourceType": "Patient",
        "id": "abc",
        "meta": {"versionId": "4"},
    }
    sync_client.update_resource(resource, if_match='W/"7"')
    assert route.called
    request = route.calls[0].request
    assert request.headers.get("If-Match") == 'W/"7"'


def test_update_resource_no_versionid_no_header(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = _mock_update(respx_mock, "abc")
    resource = {"resourceType": "Patient", "id": "abc"}
    sync_client.update_resource(resource)
    assert route.called
    request = route.calls[0].request
    assert "if-match" not in {k.lower() for k in request.headers}


def test_update_resource_explicit_headers_override_if_match(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = _mock_update(respx_mock, "abc")
    resource = {
        "resourceType": "Patient",
        "id": "abc",
        "meta": {"versionId": "4"},
    }
    sync_client.update_resource(
        resource,
        headers={"If-Match": 'W/"9"'},
        if_match='W/"7"',
    )
    assert route.called
    request = route.calls[0].request
    assert request.headers.get("If-Match") == 'W/"9"'


@pytest.mark.asyncio
async def test_async_update_resource_auto_attaches_if_match(
    respx_mock: MockRouter,
) -> None:
    route = _mock_update(respx_mock, "abc")
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/", access_token="tkn"
    ) as client:
        await client.update_resource(
            {
                "resourceType": "Patient",
                "id": "abc",
                "meta": {"versionId": "4"},
            }
        )
    assert route.called
    request = route.calls[0].request
    assert request.headers.get("If-Match") == 'W/"4"'


@pytest.mark.asyncio
async def test_async_update_resource_if_match_false_opts_out(
    respx_mock: MockRouter,
) -> None:
    route = _mock_update(respx_mock, "abc")
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/", access_token="tkn"
    ) as client:
        await client.update_resource(
            {
                "resourceType": "Patient",
                "id": "abc",
                "meta": {"versionId": "4"},
            },
            if_match=False,
        )
    assert route.called
    request = route.calls[0].request
    assert "if-match" not in {k.lower() for k in request.headers}
