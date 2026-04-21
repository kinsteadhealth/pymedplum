"""Integration tests for auth flows on a fresh client.

These tests deliberately build their own ``AsyncMedplumClient`` rather
than reuse the pre-authenticated ``async_medplum_client`` fixture from
``conftest.py``. The whole point is to exercise the first-request path
on a brand-new client — that is the regression coverage for the bug
that pre-authenticating fixtures originally hid.
"""

import asyncio
import os

import pytest


def _require_creds() -> None:
    """Skip the test unless client-credentials are in the environment."""
    required = ("MEDPLUM_CLIENT_ID", "MEDPLUM_CLIENT_SECRET")
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        pytest.skip(f"Missing env vars: {missing}")


@pytest.mark.asyncio
async def test_first_request_client_credentials_against_live_medplum():
    """A freshly-constructed client authenticates on its first request."""
    _require_creds()
    from pymedplum import AsyncMedplumClient

    client = AsyncMedplumClient(
        base_url=os.environ.get("MEDPLUM_BASE_URL", "https://api.medplum.com/"),
        client_id=os.environ["MEDPLUM_CLIENT_ID"],
        client_secret=os.environ["MEDPLUM_CLIENT_SECRET"],
    )
    try:
        result = await client.search_resources("Patient", {"_count": "1"})
        assert result["resourceType"] == "Bundle"
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_concurrent_requests_against_live_medplum():
    """Concurrent first-requests share one auth flow without deadlocking."""
    _require_creds()
    from pymedplum import AsyncMedplumClient

    client = AsyncMedplumClient(
        base_url=os.environ.get("MEDPLUM_BASE_URL", "https://api.medplum.com/"),
        client_id=os.environ["MEDPLUM_CLIENT_ID"],
        client_secret=os.environ["MEDPLUM_CLIENT_SECRET"],
    )
    try:
        results = await asyncio.gather(
            *[client.search_resources("Patient", {"_count": "1"}) for _ in range(10)]
        )
        assert all(r["resourceType"] == "Bundle" for r in results)
    finally:
        await client.aclose()
