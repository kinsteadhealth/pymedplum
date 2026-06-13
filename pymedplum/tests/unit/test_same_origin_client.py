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


def test_async_job_url_cross_origin_rejected() -> None:
    """The job poll attaches the bearer token; a cross-origin job URL
    would exfiltrate it. This was the one escape hatch without the
    same-origin guard every other URL path enforces."""
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    try:
        with pytest.raises(UnsafeRedirectError):
            client._resolve_async_job_url("https://evil.com/fhir/R4/job/abc/status")
    finally:
        client.close()


def test_async_job_url_cross_origin_diagnostics_rejected() -> None:
    """Same guard for URLs extracted from OperationOutcome diagnostics —
    a stored/poisoned outcome must not redirect the token off-origin."""
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "information", "diagnostics": "https://evil.com/job"}],
    }
    try:
        with pytest.raises(UnsafeRedirectError):
            client._resolve_async_job_url(outcome)
    finally:
        client.close()


@pytest.mark.parametrize(
    "evil",
    [
        "HTTPS://evil.com/fhir/R4/job/abc/status",  # mixed-case scheme
        "Https://evil.com/job",
        "hTTpS://evil.com/job",
        "//evil.com/job",  # protocol-relative
        "http://evil.com/job",
    ],
)
def test_async_job_url_cross_origin_scheme_variants_rejected(evil: str) -> None:
    """A case-sensitive scheme check would let HTTPS://evil.com/... skip
    the same-origin guard and exfiltrate the bearer token. Absolute-URL
    detection must be scheme-case-insensitive and catch protocol-relative
    forms — both as a caller string and via OperationOutcome diagnostics."""
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "information", "diagnostics": evil}],
    }
    try:
        with pytest.raises(UnsafeRedirectError):
            client._resolve_async_job_url(evil)
        with pytest.raises(UnsafeRedirectError):
            client._resolve_async_job_url(outcome)
    finally:
        client.close()


def test_async_job_url_bare_id_unaffected() -> None:
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    try:
        assert (
            client._resolve_async_job_url("abc")
            == "https://api.medplum.com/fhir/R4/job/abc/status"
        )
    finally:
        client.close()


def test_async_job_url_same_origin_diagnostics_accepted() -> None:
    client = MedplumClient(base_url="https://api.medplum.com/", access_token="tkn")
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "information",
                "diagnostics": "https://api.medplum.com/fhir/R4/job/j1/status",
            }
        ],
    }
    try:
        url = client._resolve_async_job_url(outcome)
        assert url == "https://api.medplum.com/fhir/R4/job/j1/status"
    finally:
        client.close()
