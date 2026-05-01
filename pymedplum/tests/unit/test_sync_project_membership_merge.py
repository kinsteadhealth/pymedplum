"""Sync transport tests for merge_project_membership_access."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from respx import MockRouter

from pymedplum import (
    MedplumClient,
    MergeResult,
    PreconditionFailedError,
    make_project_membership_access,
)


_BASE_URL = "https://api.medplum.com/"
_PM_PATH = f"{_BASE_URL}fhir/R4/ProjectMembership/abc"


def _managed_entry() -> dict[str, Any]:
    return make_project_membership_access(
        "AccessPolicy/managed-1", {"organization": "Organization/org-a"}
    )


def _other_entry() -> dict[str, Any]:
    return make_project_membership_access(
        "AccessPolicy/other", {"organization": "Organization/org-z"}
    )


def test_merge_writes_when_managed_diffs(
    sync_client: MedplumClient,
    membership_factory: Any,
    mock_membership_endpoints: Any,
) -> None:
    membership = membership_factory(access=[])
    _, put_route = mock_membership_endpoints(membership, next_version="2")

    result = sync_client.merge_project_membership_access(
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
    request = put_route.calls[0].request
    assert request.headers.get("If-Match") == 'W/"1"'


def test_merge_skips_write_when_byte_equal(
    sync_client: MedplumClient,
    membership_factory: Any,
    mock_membership_endpoints: Any,
) -> None:
    entry = _managed_entry()
    membership = membership_factory(access=[entry])
    _, put_route = mock_membership_endpoints(membership)

    result = sync_client.merge_project_membership_access(
        "abc",
        managed_access=[entry],
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is False
    assert result.version_id == "1"
    assert result.managed_count == 1
    assert result.untouched_count == 0
    assert not put_route.called


def test_merge_force_writes_even_when_equal(
    sync_client: MedplumClient,
    membership_factory: Any,
    mock_membership_endpoints: Any,
) -> None:
    entry = _managed_entry()
    membership = membership_factory(access=[entry])
    _, put_route = mock_membership_endpoints(membership, next_version="2")

    result = sync_client.merge_project_membership_access(
        "abc",
        managed_access=[entry],
        managed_policy_ids={"managed-1"},
        force=True,
    )

    assert result.updated is True
    assert result.version_id == "2"
    assert put_route.called


def test_merge_empty_removes_managed_preserves_untouched(
    sync_client: MedplumClient,
    membership_factory: Any,
    mock_membership_endpoints: Any,
) -> None:
    untouched = _other_entry()
    managed = _managed_entry()
    membership = membership_factory(access=[untouched, managed])
    _, put_route = mock_membership_endpoints(membership, next_version="2")

    result = sync_client.merge_project_membership_access(
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


def test_merge_raises_when_remote_lacks_version_id(
    sync_client: MedplumClient,
    respx_mock: MockRouter,
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

    with pytest.raises(ValueError, match="meta.versionId"):
        sync_client.merge_project_membership_access(
            "abc",
            managed_access=[_managed_entry()],
            managed_policy_ids={"managed-1"},
        )

    assert get_route.called
    assert not put_route.called


def test_merge_rejects_managed_outside_managed_set(
    sync_client: MedplumClient,
    respx_mock: MockRouter,
) -> None:
    get_route = respx_mock.get(_PM_PATH)

    with pytest.raises(ValueError, match="outside managed_policy_ids"):
        sync_client.merge_project_membership_access(
            "abc",
            managed_access=[_other_entry()],
            managed_policy_ids={"managed-1"},
        )

    assert not get_route.called


def test_merge_412_retry_succeeds(
    sync_client: MedplumClient,
    respx_mock: MockRouter,
    membership_factory: Any,
) -> None:
    membership_v1 = membership_factory(version_id="1", access=[])
    membership_v2 = membership_factory(version_id="2", access=[])

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
            httpx.Response(
                200, json={**membership_v2, "meta": {"versionId": "3"}}
            ),
        ]
    )

    result = sync_client.merge_project_membership_access(
        "abc",
        managed_access=[_managed_entry()],
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.version_id == "3"
    assert get_route.call_count == 2
    assert put_route.call_count == 2


def test_merge_412_exhaustion_raises(
    sync_client: MedplumClient,
    respx_mock: MockRouter,
    membership_factory: Any,
) -> None:
    membership = membership_factory(access=[])
    respx_mock.get(_PM_PATH).mock(
        return_value=httpx.Response(200, json=membership)
    )
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
        sync_client.merge_project_membership_access(
            "abc",
            managed_access=[_managed_entry()],
            managed_policy_ids={"managed-1"},
            max_retries=1,
        )


def test_merge_counts_reflect_post_merge_state(
    sync_client: MedplumClient,
    membership_factory: Any,
    mock_membership_endpoints: Any,
) -> None:
    untouched = _other_entry()
    membership = membership_factory(access=[untouched])
    mock_membership_endpoints(membership)

    result = sync_client.merge_project_membership_access(
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


def test_merge_normalizes_membership_id(
    sync_client: MedplumClient,
    membership_factory: Any,
    mock_membership_endpoints: Any,
) -> None:
    membership = membership_factory(access=[])
    get_route, _ = mock_membership_endpoints(membership)

    sync_client.merge_project_membership_access(
        "ProjectMembership/abc",
        managed_access=[_managed_entry()],
        managed_policy_ids={"managed-1"},
    )

    assert get_route.called
    assert get_route.calls[0].request.url.path.endswith(
        "/fhir/R4/ProjectMembership/abc"
    )


def test_merge_rejects_empty_managed_policy_ids(
    sync_client: MedplumClient,
) -> None:
    with pytest.raises(ValueError, match="managed_policy_ids"):
        sync_client.merge_project_membership_access(
            "abc",
            managed_access=[],
            managed_policy_ids=set(),
        )
