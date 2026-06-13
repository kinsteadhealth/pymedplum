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


def _observation(obs_id: str) -> dict:
    return {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "code": {"text": "test"},
    }


def _bundle_with_includes() -> dict:
    """One page: two Observation matches plus an included Patient."""
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [
            {"resource": _observation("o1"), "search": {"mode": "match"}},
            {"resource": _observation("o2"), "search": {"mode": "match"}},
            {
                "resource": {"resourceType": "Patient", "id": "p1"},
                "search": {"mode": "include"},
            },
        ],
    }


def test_sync_paginator_skips_include_entries(respx_mock: respx.MockRouter) -> None:
    """_include/_revinclude entries must not be yielded as matches —
    with as_fhir they are a different resource type and crash parsing."""
    from pymedplum.fhir import Observation

    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(200, json=_bundle_with_includes())
    )
    client = MedplumClient(access_token="t")
    try:
        out = list(
            client.search_resource_pages(
                "Observation",
                {"_include": "Observation:subject"},
                as_fhir=Observation,
            )
        )
        assert [o.id for o in out] == ["o1", "o2"]
    finally:
        client.close()


@pytest.mark.asyncio
async def test_async_paginator_skips_include_entries(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(200, json=_bundle_with_includes())
    )
    client = AsyncMedplumClient(access_token="t")
    try:
        out = [
            r
            async for r in client.search_resource_pages(
                "Observation", {"_include": "Observation:subject"}
            )
        ]
        assert [r["id"] for r in out] == ["o1", "o2"]
    finally:
        await client.aclose()


def test_sync_paginator_include_entries_do_not_consume_cap(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(200, json=_bundle_with_includes())
    )
    client = MedplumClient(access_token="t")
    try:
        out = list(client.search_resource_pages("Observation", max_resources=2))
        assert [r["id"] for r in out] == ["o1", "o2"]
    finally:
        client.close()


def test_get_total_uses_bundle_total_when_present() -> None:
    bundle = FHIRBundle({"resourceType": "Bundle", "total": 42, "entry": []})
    assert bundle.get_total() == 42


def test_get_total_counts_matches_when_single_complete_page() -> None:
    bundle = FHIRBundle(_bundle_with_includes())
    # No next link: the page is the full result set; includes don't count.
    assert bundle.get_total() == 2


def test_get_total_returns_none_when_paginated_without_total() -> None:
    """Without Bundle.total a paginated bundle's entry count is just the
    page size — returning it as a 'total' would be a lie."""
    data = _bundle(20)
    data["link"] = [
        {"relation": "next", "url": "https://api.medplum.com/fhir/R4/Patient?p=2"}
    ]
    bundle = FHIRBundle(data)
    assert bundle.get_total() is None


def test_get_total_counts_modeless_entries_as_matches() -> None:
    """Entries without ``search.mode`` are primary matches (servers may
    omit the mode); a complete single page counts them."""
    bundle = FHIRBundle(_bundle(7))
    assert bundle.get_total() == 7
