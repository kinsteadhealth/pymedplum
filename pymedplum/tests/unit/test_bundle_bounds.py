"""Opt-in bounds on bundle materialization and paginator iteration."""

from __future__ import annotations

import httpx
import pytest
import respx

from pymedplum import AsyncMedplumClient, MedplumClient
from pymedplum.bundle import FHIRBundle


def _bundle(n: int) -> dict:
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [
            {"resource": {"resourceType": "Patient", "id": f"p{i}"}} for i in range(n)
        ],
    }


def test_get_resources_unbounded_by_default() -> None:
    bundle = FHIRBundle(_bundle(1000))
    assert len(bundle.get_resources()) == 1000


def test_get_resources_max_resources_blocks_oversized_payload() -> None:
    bundle = FHIRBundle(_bundle(500))
    with pytest.raises(ValueError, match="exceeding max_resources=100"):
        bundle.get_resources(max_resources=100)


def test_get_resources_max_resources_allows_at_or_below_cap() -> None:
    bundle = FHIRBundle(_bundle(50))
    assert len(bundle.get_resources(max_resources=100)) == 50
    assert len(bundle.get_resources(max_resources=50)) == 50


def test_sync_paginator_caps_resources(respx_mock: respx.MockRouter) -> None:
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient", params={"_count": "10"}
    ).mock(return_value=httpx.Response(200, json=_bundle(10)))
    client = MedplumClient(access_token="t")
    try:
        out = list(
            client.search_resource_pages("Patient", {"_count": "10"}, max_resources=3)
        )
        assert len(out) == 3
        assert [r["id"] for r in out] == ["p0", "p1", "p2"]
    finally:
        client.close()


@pytest.mark.asyncio
async def test_async_paginator_caps_resources(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient", params={"_count": "10"}
    ).mock(return_value=httpx.Response(200, json=_bundle(10)))
    client = AsyncMedplumClient(access_token="t")
    try:
        out = [
            r
            async for r in client.search_resource_pages(
                "Patient", {"_count": "10"}, max_resources=4
            )
        ]
        assert len(out) == 4
    finally:
        await client.aclose()


def test_max_retry_delay_seconds_kwarg_propagates_to_client() -> None:
    """The constructor kwarg lands on the instance attribute."""
    client = MedplumClient(access_token="t", max_retry_delay_seconds=5.0)
    assert client.max_retry_delay_seconds == 5.0
    client.close()


def test_max_retry_delay_seconds_kwarg_propagates_to_async_client() -> None:
    client = AsyncMedplumClient(access_token="t", max_retry_delay_seconds=5.0)
    assert client.max_retry_delay_seconds == 5.0


def test_max_retry_delay_seconds_default_is_60() -> None:
    client = MedplumClient(access_token="t")
    assert client.max_retry_delay_seconds == 60.0
    client.close()


def test_max_retry_delay_seconds_negative_clamped_to_zero() -> None:
    """Defensive: a negative value would otherwise yield negative sleeps."""
    client = MedplumClient(access_token="t", max_retry_delay_seconds=-5.0)
    assert client.max_retry_delay_seconds == 0.0
    client.close()
