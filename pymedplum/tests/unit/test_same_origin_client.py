"""Same-origin guards on pagination ``next`` links and async-job URLs.

Covers the real credential-leak surface: the server could emit a
``link[rel=next].url`` or an ``OperationOutcome.issue[0].diagnostics``
pointing at a different host, and the SDK would happily re-send the
bearer token. Phase 6 rejects both with ``UnsafeRedirectError``.
"""

from __future__ import annotations

import httpx
import pytest
from respx import MockRouter

from pymedplum.async_client import AsyncMedplumClient
from pymedplum.client import MedplumClient
from pymedplum.exceptions import UnsafeRedirectError


def test_pagination_next_cross_origin_rejected_sync(
    respx_mock: MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "entry": [{"resource": {"resourceType": "Patient", "id": "a"}}],
                "link": [{"relation": "next", "url": "https://evil.com/next"}],
            },
        )
    )
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    try:
        with pytest.raises(UnsafeRedirectError):
            list(client.search_resource_pages("Patient"))
    finally:
        client.close()


@pytest.mark.asyncio
async def test_pagination_next_cross_origin_rejected_async(
    respx_mock: MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "entry": [{"resource": {"resourceType": "Patient", "id": "a"}}],
                "link": [{"relation": "next", "url": "https://evil.com/next"}],
            },
        )
    )
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/", access_token="tkn"
    ) as client:
        with pytest.raises(UnsafeRedirectError):
            async for _ in client.search_resource_pages("Patient"):
                pass


def test_async_job_url_same_origin_accepted() -> None:
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    try:
        url = client._resolve_async_job_url(
            "https://api.medplum.com/fhir/R4/job/abc/status"
        )
        assert url == "https://api.medplum.com/fhir/R4/job/abc/status"
    finally:
        client.close()
