"""Async transport tests for merge_project_membership_access.

Mirrors the scenario matrix in
``test_sync_project_membership_merge.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import (
    AsyncMedplumClient,
    MergeResult,
    PreconditionFailedError,
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


def _managed_entry() -> dict[str, Any]:
    return make_project_membership_access(
        "AccessPolicy/managed-1", {"organization": "Organization/org-a"}
    )


def _other_entry() -> dict[str, Any]:
    return make_project_membership_access(
        "AccessPolicy/other", {"organization": "Organization/org-z"}
    )


def _membership(
    *,
    membership_id: str = "abc",
    version_id: str = "1",
    access: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "resourceType": "ProjectMembership",
        "id": membership_id,
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
    membership_id = membership["id"]
    get_route = respx_mock.get(
        f"{_BASE_URL}fhir/R4/ProjectMembership/{membership_id}"
    ).mock(return_value=httpx.Response(200, json=membership))
    put_route = respx_mock.put(
        f"{_BASE_URL}fhir/R4/ProjectMembership/{membership_id}"
    ).mock(
        return_value=httpx.Response(
            200, json={**membership, "meta": {"versionId": next_version}}
        )
    )
    return get_route, put_route


@pytest.mark.asyncio
async def test_merge_writes_when_managed_diffs(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    membership = _membership(access=[])
    _, put_route = _mock_endpoints(respx_mock, membership)

    result = await async_client.merge_project_membership_access(
        "abc",
        managed_access=[_managed_entry()],
        managed_policy_ids={"managed-1"},
    )

    assert isinstance(result, MergeResult)
    assert result.updated is True
    assert result.version_id == "2"
    assert result.managed_count == 1
    assert result.untouched_count == 0
    assert put_route.called
    assert put_route.calls[0].request.headers.get("If-Match") == 'W/"1"'


@pytest.mark.asyncio
async def test_merge_skips_write_when_byte_equal(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    entry = _managed_entry()
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[entry]))

    result = await async_client.merge_project_membership_access(
        "abc",
        managed_access=[entry],
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is False
    assert result.version_id == "1"
    assert not put_route.called


@pytest.mark.asyncio
async def test_merge_force_writes_even_when_equal(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    entry = _managed_entry()
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[entry]))

    result = await async_client.merge_project_membership_access(
        "abc",
        managed_access=[entry],
        managed_policy_ids={"managed-1"},
        force=True,
    )

    assert result.updated is True
    assert put_route.called


@pytest.mark.asyncio
async def test_merge_empty_removes_managed_preserves_untouched(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    untouched = _other_entry()
    managed = _managed_entry()
    _, put_route = _mock_endpoints(respx_mock, _membership(access=[untouched, managed]))

    result = await async_client.merge_project_membership_access(
        "abc",
        managed_access=[],
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.managed_count == 0
    assert result.untouched_count == 1

    sent = put_route.calls[0].request.read().decode()
    assert "managed-1" not in sent
    assert "AccessPolicy/other" in sent


@pytest.mark.asyncio
async def test_merge_raises_when_remote_lacks_version_id(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    body = {
        "resourceType": "ProjectMembership",
        "id": "abc",
        "project": {"reference": "Project/p1"},
        "user": {"reference": "User/u1"},
        "profile": {"reference": "Practitioner/pr1"},
        "access": [],
    }
    get_route = respx_mock.get(_PM_PATH).mock(
        return_value=httpx.Response(200, json=body)
    )
    put_route = respx_mock.put(_PM_PATH).mock(
        return_value=httpx.Response(200, json=body)
    )

    with pytest.raises(ValueError, match=r"meta\.versionId"):
        await async_client.merge_project_membership_access(
            "abc",
            managed_access=[_managed_entry()],
            managed_policy_ids={"managed-1"},
        )

    assert get_route.called
    assert not put_route.called


@pytest.mark.asyncio
async def test_merge_rejects_managed_outside_managed_set(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    get_route = respx_mock.get(_PM_PATH)

    with pytest.raises(ValueError, match="outside managed_policy_ids"):
        await async_client.merge_project_membership_access(
            "abc",
            managed_access=[_other_entry()],
            managed_policy_ids={"managed-1"},
        )

    assert not get_route.called


@pytest.mark.asyncio
async def test_merge_412_retry_succeeds(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    membership_v1 = _membership(version_id="1", access=[])
    membership_v2 = _membership(version_id="2", access=[])

    get_route = respx_mock.get(_PM_PATH).mock(
        side_effect=[
            httpx.Response(200, json=membership_v1),
            httpx.Response(200, json=membership_v2),
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
            httpx.Response(200, json={**membership_v2, "meta": {"versionId": "3"}}),
        ]
    )

    result = await async_client.merge_project_membership_access(
        "abc",
        managed_access=[_managed_entry()],
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.version_id == "3"
    assert get_route.call_count == 2
    assert put_route.call_count == 2


@pytest.mark.asyncio
async def test_merge_412_exhaustion_raises(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    membership = _membership(access=[])
    respx_mock.get(_PM_PATH).mock(return_value=httpx.Response(200, json=membership))
    respx_mock.put(_PM_PATH).mock(
        return_value=httpx.Response(
            412,
            json={
                "resourceType": "OperationOutcome",
                "issue": [{"severity": "error", "code": "conflict"}],
            },
        )
    )

    with pytest.raises(PreconditionFailedError):
        await async_client.merge_project_membership_access(
            "abc",
            managed_access=[_managed_entry()],
            managed_policy_ids={"managed-1"},
            max_retries=1,
        )


@pytest.mark.asyncio
async def test_merge_counts_reflect_post_merge_state(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    untouched = _other_entry()
    _mock_endpoints(respx_mock, _membership(access=[untouched]))

    result = await async_client.merge_project_membership_access(
        "abc",
        managed_access=[
            make_project_membership_access(
                "managed-1", {"organization": "Organization/o1"}
            ),
            make_project_membership_access(
                "managed-1", {"organization": "Organization/o2"}
            ),
        ],
        managed_policy_ids={"managed-1"},
    )

    assert result.managed_count == 2
    assert result.untouched_count == 1


@pytest.mark.asyncio
async def test_merge_normalizes_membership_id(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    get_route, _ = _mock_endpoints(respx_mock, _membership(access=[]))

    await async_client.merge_project_membership_access(
        "ProjectMembership/abc",
        managed_access=[_managed_entry()],
        managed_policy_ids={"managed-1"},
    )

    assert get_route.called
    assert get_route.calls[0].request.url.path.endswith(
        "/fhir/R4/ProjectMembership/abc"
    )


@pytest.mark.asyncio
async def test_merge_rejects_empty_managed_policy_ids(
    async_client: AsyncMedplumClient,
) -> None:
    with pytest.raises(ValueError, match="managed_policy_ids"):
        await async_client.merge_project_membership_access(
            "abc",
            managed_access=[],
            managed_policy_ids=set(),
        )
