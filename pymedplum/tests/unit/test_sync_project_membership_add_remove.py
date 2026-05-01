"""Sync transport tests for atomic add/remove methods.

These verify that ``add_project_membership_access_entry`` and
``remove_project_membership_access_entry`` re-read inside the 412
retry loop so concurrent writes by other callers are preserved.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from respx import MockRouter

from pymedplum import (
    MedplumClient,
    make_project_membership_access,
)


_BASE_URL = "https://api.medplum.com/"
_PM_PATH = f"{_BASE_URL}fhir/R4/ProjectMembership/abc"


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


# ---------------------------------------------------------------------------
# add_project_membership_access_entry
# ---------------------------------------------------------------------------


def test_add_appends_to_existing_managed(
    sync_client: MedplumClient, mock_membership_endpoints: Any
) -> None:
    existing = _entry("a")
    membership = _membership(access=[existing])
    _, put_route = mock_membership_endpoints(membership, next_version="2")

    result = sync_client.add_project_membership_access_entry(
        "abc",
        _entry("b"),
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.managed_count == 2
    sent = put_route.calls[0].request.read().decode()
    assert "Organization/org-a" in sent
    assert "Organization/org-b" in sent


def test_add_is_idempotent_when_entry_present(
    sync_client: MedplumClient, mock_membership_endpoints: Any
) -> None:
    entry = _entry("a")
    membership = _membership(access=[entry])
    _, put_route = mock_membership_endpoints(membership)

    result = sync_client.add_project_membership_access_entry(
        "abc",
        entry,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is False
    assert not put_route.called


def test_add_preserves_concurrent_writer_via_412_retry(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """Race scenario: between our read and our write, another writer
    appends a different managed entry. The 412 retry must re-read,
    re-apply our mutation against the new state, and not lose
    the concurrent entry."""
    entry_a = _entry("a")  # ours, the one we're adding
    entry_x = _entry("x")  # the concurrent writer's entry

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

    result = sync_client.add_project_membership_access_entry(
        "abc",
        entry_a,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.version_id == "3"
    final_payload = put_route.calls[1].request.read().decode()
    # Both the concurrent writer's entry and ours survived.
    assert "Organization/org-x" in final_payload
    assert "Organization/org-a" in final_payload


def test_add_preserves_untouched_entries(
    sync_client: MedplumClient, mock_membership_endpoints: Any
) -> None:
    untouched = make_project_membership_access(
        "AccessPolicy/other",
        {"organization": "Organization/org-z"},
    )
    membership = _membership(access=[untouched])
    _, put_route = mock_membership_endpoints(membership)

    sync_client.add_project_membership_access_entry(
        "abc",
        _entry("a"),
        managed_policy_ids={"managed-1"},
    )

    sent = put_route.calls[0].request.read().decode()
    assert "AccessPolicy/other" in sent
    assert "Organization/org-z" in sent
    assert "Organization/org-a" in sent


def test_add_rejects_unmanaged_entry(sync_client: MedplumClient) -> None:
    bad_entry = make_project_membership_access(
        "AccessPolicy/other",
        {"organization": "Organization/org-z"},
    )

    with pytest.raises(ValueError, match="outside managed_policy_ids"):
        sync_client.add_project_membership_access_entry(
            "abc",
            bad_entry,
            managed_policy_ids={"managed-1"},
        )


# ---------------------------------------------------------------------------
# remove_project_membership_access_entry
# ---------------------------------------------------------------------------


def test_remove_drops_matching_entry(
    sync_client: MedplumClient, mock_membership_endpoints: Any
) -> None:
    keep = _entry("a")
    drop = _entry("b")
    membership = _membership(access=[keep, drop])
    _, put_route = mock_membership_endpoints(membership)

    result = sync_client.remove_project_membership_access_entry(
        "abc",
        drop,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    assert result.managed_count == 1
    sent = put_route.calls[0].request.read().decode()
    assert "Organization/org-a" in sent
    assert "Organization/org-b" not in sent


def test_remove_is_idempotent_when_entry_absent(
    sync_client: MedplumClient, mock_membership_endpoints: Any
) -> None:
    keep = _entry("a")
    membership = _membership(access=[keep])
    _, put_route = mock_membership_endpoints(membership)

    result = sync_client.remove_project_membership_access_entry(
        "abc",
        _entry("zzz"),
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is False
    assert not put_route.called


def test_remove_preserves_concurrent_add_via_412_retry(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """Race scenario: we want to remove entry-a; meanwhile another
    writer adds entry-x. The 412 retry must re-read, re-apply our
    removal, and leave entry-x intact."""
    entry_a = _entry("a")
    entry_x = _entry("x")

    initial = _membership(version_id="1", access=[entry_a])
    after_concurrent = _membership(
        version_id="2", access=[entry_a, entry_x]
    )

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

    result = sync_client.remove_project_membership_access_entry(
        "abc",
        entry_a,
        managed_policy_ids={"managed-1"},
    )

    assert result.updated is True
    final_payload = put_route.calls[1].request.read().decode()
    assert "Organization/org-x" in final_payload
    assert "Organization/org-a" not in final_payload


def test_remove_only_touches_managed_slice(
    sync_client: MedplumClient, mock_membership_endpoints: Any
) -> None:
    """Even if an unmanaged entry happens to look structurally like
    the managed entry we want to remove, the unmanaged one is left
    alone (different policy reference, so not byte-equal)."""
    managed = _entry("a")  # AccessPolicy/managed-1
    unmanaged = make_project_membership_access(
        "AccessPolicy/other",
        {"organization": "Organization/org-a"},
    )
    membership = _membership(access=[managed, unmanaged])
    _, put_route = mock_membership_endpoints(membership)

    sync_client.remove_project_membership_access_entry(
        "abc",
        managed,
        managed_policy_ids={"managed-1"},
    )

    sent = put_route.calls[0].request.read().decode()
    assert "AccessPolicy/managed-1" not in sent  # ours got removed
    assert "AccessPolicy/other" in sent  # unmanaged preserved
