"""Async transport tests for atomic add/remove methods.

Mirrors the scenario matrix in
``test_sync_project_membership_add_remove.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import (
    AsyncMedplumClient,
    make_project_membership_access,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

_BASE_URL = "https://api.medplum.com/"
_PM_PATH = f"{_BASE_URL}fhir/R4/ProjectMembership/abc"


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncMedplumClient]:
    client = AsyncMedplumClient(base_url=_BASE_URL, access_token="tkn")
    try:
        yield client
    finally:
        await client.aclose()


def _entry(org_suffix: str) -> dict[str, Any]:
    return make_project_membership_access(
        "AccessPolicy/managed-1",
        {"organization": f"Organization/org-{org_suffix}"},
    )


def _membership(
    *, version_id: str = "1", access: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    return {
        "resourceType": "ProjectMembership",
        "id": "abc",
        "meta": {"versionId": version_id},
        "project": {"reference": "Project/p1"},
        "user": {"reference": "User/u1"},
        "profile": {"reference": "Practitioner/pr1"},
        "access": access or [],
    }


def _mock_endpoints(
    respx_mock: MockRouter,
    membership: dict[str, Any],
    *,
    next_version: str = "2",
) -> tuple[Any, Any]:
    get_route = respx_mock.get(_PM_PATH).mock(
        return_value=httpx.Response(200, json=membership)
    )
    put_route = respx_mock.put(_PM_PATH).mock(
        return_value=httpx.Response(
            200, json={**membership, "meta": {"versionId": next_version}}
        )
    )
    return get_route, put_route


# ---------------------------------------------------------------------------
# add_project_membership_access_entry
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_add_appends_to_existing_managed(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    existing = _entry("a")
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[existing]))

    result = await async_client.add_project_membership_access_entry(
        "abc",
        _entry("b"),
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.managed_count == 2
    sent = put_route.calls[0].request.read().decode()
    assert "Organization/org-a" in sent
    assert "Organization/org-b" in sent


@pytest.mark.asyncio
async def test_add_is_idempotent_when_entry_present(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    entry = _entry("a")
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[entry]))

    result = await async_client.add_project_membership_access_entry(
        "abc",
        entry,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is False
    assert not put_route.called


@pytest.mark.asyncio
async def test_add_preserves_concurrent_writer_via_412_retry(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    entry_a = _entry("a")
    entry_x = _entry("x")

    initial = _membership(version_id="1", access=[])
    after_concurrent_write = _membership(version_id="2", access=[entry_x])

    respx_mock.get(_PM_PATH).mock(
        side_effect=[
            httpx.Response(200, json=initial),
            httpx.Response(200, json=after_concurrent_write),
        ]
    )
    put_route = respx_mock.put(_PM_PATH).mock(
        side_effect=[
            httpx.Response(
                412,
                json={
                    "resourceType": "OperationOutcome",
                    "issue": [{"severity": "error", "code": "conflict"}],
                },
            ),
            httpx.Response(
                200,
                json={**after_concurrent_write, "meta": {"versionId": "3"}},
            ),
        ]
    )

    result = await async_client.add_project_membership_access_entry(
        "abc",
        entry_a,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.version_id == "3"
    final_payload = put_route.calls[1].request.read().decode()
    assert "Organization/org-x" in final_payload
    assert "Organization/org-a" in final_payload


@pytest.mark.asyncio
async def test_add_preserves_untouched_entries(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    untouched = make_project_membership_access(
        "AccessPolicy/other",
        {"organization": "Organization/org-z"},
    )
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[untouched]))

    await async_client.add_project_membership_access_entry(
        "abc",
        _entry("a"),
        managed_policy_ids={"managed-1"},
    )

    sent = put_route.calls[0].request.read().decode()
    assert "AccessPolicy/other" in sent
    assert "Organization/org-z" in sent
    assert "Organization/org-a" in sent


@pytest.mark.asyncio
async def test_add_rejects_unmanaged_entry(
    async_client: AsyncMedplumClient,
) -> None:
    bad_entry = make_project_membership_access(
        "AccessPolicy/other",
        {"organization": "Organization/org-z"},
    )

    with pytest.raises(ValueError, match="outside managed_policy_ids"):
        await async_client.add_project_membership_access_entry(
            "abc",
            bad_entry,
            managed_policy_ids={"managed-1"},
        )


# ---------------------------------------------------------------------------
# remove_project_membership_access_entry
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_remove_drops_matching_entry(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    keep = _entry("a")
    drop = _entry("b")
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[keep, drop]))

    result = await async_client.remove_project_membership_access_entry(
        "abc",
        drop,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.managed_count == 1
    sent = put_route.calls[0].request.read().decode()
    assert "Organization/org-a" in sent
    assert "Organization/org-b" not in sent


@pytest.mark.asyncio
async def test_remove_is_idempotent_when_entry_absent(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    keep = _entry("a")
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[keep]))

    result = await async_client.remove_project_membership_access_entry(
        "abc",
        _entry("zzz"),
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is False
    assert not put_route.called


@pytest.mark.asyncio
async def test_remove_preserves_concurrent_add_via_412_retry(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    entry_a = _entry("a")
    entry_x = _entry("x")

    initial = _membership(version_id="1", access=[entry_a])
    after_concurrent = _membership(version_id="2", access=[entry_a, entry_x])

    respx_mock.get(_PM_PATH).mock(
        side_effect=[
            httpx.Response(200, json=initial),
            httpx.Response(200, json=after_concurrent),
        ]
    )
    put_route = respx_mock.put(_PM_PATH).mock(
        side_effect=[
            httpx.Response(
                412,
                json={
                    "resourceType": "OperationOutcome",
                    "issue": [{"severity": "error", "code": "conflict"}],
                },
            ),
            httpx.Response(
                200,
                json={**after_concurrent, "meta": {"versionId": "3"}},
            ),
        ]
    )

    result = await async_client.remove_project_membership_access_entry(
        "abc",
        entry_a,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    final_payload = put_route.calls[1].request.read().decode()
    assert "Organization/org-x" in final_payload
    assert "Organization/org-a" not in final_payload


@pytest.mark.asyncio
async def test_remove_only_touches_managed_slice(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    managed = _entry("a")
    unmanaged = make_project_membership_access(
        "AccessPolicy/other",
        {"organization": "Organization/org-a"},
    )
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[managed, unmanaged]))

    await async_client.remove_project_membership_access_entry(
        "abc",
        managed,
        managed_policy_ids={"managed-1"},
    )

    sent = put_route.calls[0].request.read().decode()
    assert "AccessPolicy/managed-1" not in sent
    assert "AccessPolicy/other" in sent
