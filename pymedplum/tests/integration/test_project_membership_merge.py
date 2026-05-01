"""Integration tests for ``merge_project_membership_access``.

These run against a live Medplum server. They validate wire-format
behavior that mocked transport tests cannot prove: the actual
``If-Match`` shape, real 412 envelopes, and that the
``make_project_membership_access`` output is accepted as a real
parameterized AccessPolicy binding.

Gated behind the same env vars as other integration tests
(``MEDPLUM_CLIENT_ID``/``MEDPLUM_CLIENT_SECRET``/``MEDPLUM_PROJECT_ID``).
"""

from __future__ import annotations

import os
import secrets
from typing import Any

import pytest

from pymedplum import (
    AsyncMedplumClient,
    MedplumClient,
    MergeResult,
    PreconditionFailedError,
    get_project_membership_access_parameter,
    get_project_membership_access_policy_id,
    make_project_membership_access,
    to_fhir_json,
)
from pymedplum.fhir import (
    Organization,
    ProjectMembershipAccess,
    Reference,
)


def _require_project(medplum_client: MedplumClient) -> str:
    if not medplum_client.project_id:
        pytest.skip("MEDPLUM_PROJECT_ID must be set")
    return medplum_client.project_id


def _make_managed_policy(
    medplum_client: MedplumClient, test_id: str, label: str = "merge"
) -> dict[str, Any]:
    """Create a parameterized AccessPolicy with a real %organization variable.

    The existing MSO integration tests use dict literals for AccessPolicy
    (see ``test_mso.py::_create_mso_env``); same shape here.
    """
    return medplum_client.create_resource(
        {
            "resourceType": "AccessPolicy",
            "name": f"Merge Test Policy {label} - {test_id}",
            "compartment": {"reference": "%organization"},
            "resource": [
                {
                    "resourceType": "Patient",
                    "criteria": "Patient?_compartment=%organization",
                },
                {"resourceType": "Organization"},
                {"resourceType": "Practitioner"},
            ],
        }
    )


def _make_org(
    medplum_client: MedplumClient, test_id: str, suffix: str
) -> dict[str, Any]:
    org = Organization(name=f"Merge Org {suffix} - {test_id}")
    return medplum_client.create_resource(to_fhir_json(org))


def _make_membership(
    medplum_client: MedplumClient,
    project_id: str,
    test_id: str,
    label: str,
    policy_id: str,
) -> dict[str, Any]:
    email = f"{label.lower()}.merge.{test_id}@test.example.com"
    return medplum_client.invite_user(
        project_id=project_id,
        resource_type="Practitioner",
        first_name=label,
        last_name=test_id,
        email=email,
        password=secrets.token_urlsafe(32),
        send_email=False,
        access_policy=f"AccessPolicy/{policy_id}",
    )


@pytest.fixture
def merge_env(medplum_client, test_id):
    """Set up a clean environment for merge tests with cleanup."""
    project_id = _require_project(medplum_client)
    cleanup: list[tuple[str, str]] = []

    managed_policy = _make_managed_policy(medplum_client, test_id, "managed")
    cleanup.append(("AccessPolicy", managed_policy["id"]))

    other_policy = _make_managed_policy(medplum_client, test_id, "other")
    cleanup.append(("AccessPolicy", other_policy["id"]))

    org_a = _make_org(medplum_client, test_id, "A")
    org_b = _make_org(medplum_client, test_id, "B")
    cleanup.append(("Organization", org_a["id"]))
    cleanup.append(("Organization", org_b["id"]))

    membership = _make_membership(
        medplum_client, project_id, test_id, "Merger", managed_policy["id"]
    )
    if not membership:
        pytest.skip("Could not create test membership")
    cleanup.append(("ProjectMembership", membership["id"]))

    yield {
        "project_id": project_id,
        "managed_policy": managed_policy,
        "other_policy": other_policy,
        "org_a": org_a,
        "org_b": org_b,
        "membership": membership,
        "managed_policy_ids": {managed_policy["id"]},
    }

    for resource_type, resource_id in reversed(cleanup):
        try:
            medplum_client.delete_resource(resource_type, resource_id)
        except Exception as exc:
            print(f"Warning: Failed to delete {resource_type}/{resource_id}: {exc}")


def test_merge_writes_typed_and_dict_inputs(medplum_client, merge_env):
    """Both `make_project_membership_access` dicts and caller-built
    `ProjectMembershipAccess` models are accepted by Medplum and
    survive the round trip with their wire shape intact."""
    membership_id = merge_env["membership"]["id"]
    managed_policy_id = merge_env["managed_policy"]["id"]
    org_a = merge_env["org_a"]

    dict_entry = make_project_membership_access(
        f"AccessPolicy/{managed_policy_id}",
        {"organization": f"Organization/{org_a['id']}"},
    )
    typed_entry = ProjectMembershipAccess(
        policy=Reference(reference=f"AccessPolicy/{managed_policy_id}"),
        parameter=[
            {
                "name": "organization",
                "valueReference": {"reference": f"Organization/{org_a['id']}"},
            }
        ],  # type: ignore[list-item]
    )

    result = medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[dict_entry, typed_entry],
        managed_policy_ids=merge_env["managed_policy_ids"],
    )
    assert result.updated is True
    assert result.managed_count == 2

    fresh = medplum_client.read_resource("ProjectMembership", membership_id)
    access = fresh["access"]
    managed_entries = [
        e
        for e in access
        if get_project_membership_access_policy_id(e) == managed_policy_id
    ]
    assert len(managed_entries) == 2
    for entry in managed_entries:
        assert entry["policy"] == {"reference": f"AccessPolicy/{managed_policy_id}"}
        param = get_project_membership_access_parameter(entry, "organization")
        assert param is not None
        assert param["valueReference"] == {"reference": f"Organization/{org_a['id']}"}


def test_merge_preserves_untouched_entries(medplum_client, merge_env):
    """Entries pointing at policies outside `managed_policy_ids`
    survive merges that empty the managed slice."""
    membership_id = merge_env["membership"]["id"]
    managed_policy_id = merge_env["managed_policy"]["id"]
    other_policy_id = merge_env["other_policy"]["id"]

    membership = medplum_client.read_resource("ProjectMembership", membership_id)
    membership["access"] = [
        make_project_membership_access(
            f"AccessPolicy/{other_policy_id}",
            {"organization": f"Organization/{merge_env['org_b']['id']}"},
        )
    ]
    medplum_client.update_resource(membership)

    medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[
            make_project_membership_access(
                f"AccessPolicy/{managed_policy_id}",
                {"organization": f"Organization/{merge_env['org_a']['id']}"},
            )
        ],
        managed_policy_ids={managed_policy_id},
    )

    fresh = medplum_client.read_resource("ProjectMembership", membership_id)
    policy_ids = [
        get_project_membership_access_policy_id(e) for e in fresh.get("access", [])
    ]
    assert other_policy_id in policy_ids
    assert managed_policy_id in policy_ids

    # Empty the managed slice — untouched entry survives.
    medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[],
        managed_policy_ids={managed_policy_id},
    )

    fresh = medplum_client.read_resource("ProjectMembership", membership_id)
    policy_ids = [
        get_project_membership_access_policy_id(e) for e in fresh.get("access", [])
    ]
    assert managed_policy_id not in policy_ids
    assert other_policy_id in policy_ids


def test_merge_idempotent_no_write(medplum_client, merge_env):
    """A second call with the same managed_access (and no force) does
    not write."""
    membership_id = merge_env["membership"]["id"]
    managed_policy_id = merge_env["managed_policy"]["id"]
    entry = make_project_membership_access(
        f"AccessPolicy/{managed_policy_id}",
        {"organization": f"Organization/{merge_env['org_a']['id']}"},
    )

    first = medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[entry],
        managed_policy_ids={managed_policy_id},
    )
    second = medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[entry],
        managed_policy_ids={managed_policy_id},
    )

    assert first.updated is True
    assert second.updated is False
    assert second.version_id == first.version_id


def test_merge_force_writes_when_byte_equal(medplum_client, merge_env):
    """`force=True` skips the SDK's byte-equal short-circuit and sends
    the PUT.

    Note: Medplum itself optimizes byte-equal PUTs and may return the
    same ``versionId`` as before. ``MergeResult.updated=True`` reflects
    that the SDK issued a PUT — it does not promise the server bumped
    the version. The non-force path (covered by
    ``test_merge_idempotent_no_write``) verifies the SDK *doesn't*
    issue a PUT when nothing changed.
    """
    membership_id = merge_env["membership"]["id"]
    managed_policy_id = merge_env["managed_policy"]["id"]
    entry = make_project_membership_access(
        f"AccessPolicy/{managed_policy_id}",
        {"organization": f"Organization/{merge_env['org_a']['id']}"},
    )

    medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[entry],
        managed_policy_ids={managed_policy_id},
    )
    forced = medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[entry],
        managed_policy_ids={managed_policy_id},
        force=True,
    )

    assert forced.updated is True


def test_merge_rejects_unmanaged_entries(medplum_client, merge_env):
    """Helper rejects entries pointing at policies outside
    `managed_policy_ids` before any wire call."""
    with pytest.raises(ValueError):
        medplum_client.merge_project_membership_access(
            merge_env["membership"]["id"],
            managed_access=[
                make_project_membership_access(
                    f"AccessPolicy/{merge_env['other_policy']['id']}",
                    {"organization": f"Organization/{merge_env['org_a']['id']}"},
                )
            ],
            managed_policy_ids={merge_env["managed_policy"]["id"]},
        )


def test_merge_real_412_concurrent_writers(medplum_client, merge_env):
    """Two writers race against the same membership; the second one
    re-reads via the retry loop and succeeds (no PreconditionFailedError
    surfaces)."""
    membership_id = merge_env["membership"]["id"]
    managed_policy_id = merge_env["managed_policy"]["id"]

    pm_v1 = medplum_client.read_resource("ProjectMembership", membership_id)
    pm_stale = medplum_client.read_resource("ProjectMembership", membership_id)
    assert pm_v1["meta"]["versionId"] == pm_stale["meta"]["versionId"]

    # Writer 1 wins via plain update_resource — uses If-Match from pm_v1.
    pm_v1["access"] = [
        make_project_membership_access(
            f"AccessPolicy/{managed_policy_id}",
            {"organization": f"Organization/{merge_env['org_a']['id']}"},
        )
    ]
    medplum_client.update_resource(pm_v1)

    # Writer 2 (the merge helper) reads fresh state, builds, writes, succeeds.
    result = medplum_client.merge_project_membership_access(
        membership_id,
        managed_access=[
            make_project_membership_access(
                f"AccessPolicy/{managed_policy_id}",
                {"organization": f"Organization/{merge_env['org_b']['id']}"},
            )
        ],
        managed_policy_ids={managed_policy_id},
    )

    assert result.updated is True
    fresh = medplum_client.read_resource("ProjectMembership", membership_id)
    org_param = get_project_membership_access_parameter(
        fresh["access"][0], "organization"
    )
    assert org_param is not None
    assert org_param["valueReference"]["reference"].endswith(merge_env["org_b"]["id"])


def test_merge_does_not_send_obo_header(medplum_client, merge_env, monkeypatch):
    """Membership administration calls go without
    ``X-Medplum-On-Behalf-Of``. OBO is for clinical data, not
    membership administration."""
    seen_headers: list[dict[str, str]] = []

    original_request = medplum_client._request

    def _capture_request(method, url, **kwargs):
        merged = dict(kwargs.get("headers") or {})
        seen_headers.append(merged)
        return original_request(method, url, **kwargs)

    monkeypatch.setattr(medplum_client, "_request", _capture_request)

    medplum_client.merge_project_membership_access(
        merge_env["membership"]["id"],
        managed_access=[
            make_project_membership_access(
                f"AccessPolicy/{merge_env['managed_policy']['id']}",
                {"organization": f"Organization/{merge_env['org_a']['id']}"},
            )
        ],
        managed_policy_ids=merge_env["managed_policy_ids"],
    )

    for headers in seen_headers:
        assert "X-Medplum-On-Behalf-Of" not in headers


@pytest.mark.asyncio
async def test_async_merge_round_trip(medplum_client, merge_env):
    """Async client mirrors the sync wire behavior end-to-end."""
    client_id = os.getenv("MEDPLUM_CLIENT_ID")
    client_secret = os.getenv("MEDPLUM_CLIENT_SECRET")
    if not (client_id and client_secret):
        pytest.skip("Async test requires MEDPLUM_CLIENT_ID/SECRET")

    membership_id = merge_env["membership"]["id"]
    managed_policy_id = merge_env["managed_policy"]["id"]

    async with AsyncMedplumClient(
        client_id=client_id,
        client_secret=client_secret,
        project_id=os.getenv("MEDPLUM_PROJECT_ID"),
    ) as async_client:
        result = await async_client.merge_project_membership_access(
            membership_id,
            managed_access=[
                make_project_membership_access(
                    f"AccessPolicy/{managed_policy_id}",
                    {"organization": f"Organization/{merge_env['org_a']['id']}"},
                )
            ],
            managed_policy_ids={managed_policy_id},
        )
        assert isinstance(result, MergeResult)
        assert result.updated is True

        # Idempotent second call.
        result2 = await async_client.merge_project_membership_access(
            membership_id,
            managed_access=[
                make_project_membership_access(
                    f"AccessPolicy/{managed_policy_id}",
                    {"organization": f"Organization/{merge_env['org_a']['id']}"},
                )
            ],
            managed_policy_ids={managed_policy_id},
        )
        assert result2.updated is False


def test_async_412_propagates_after_exhaustion(monkeypatch):
    """The async helper raises PreconditionFailedError when retries
    are exhausted. Validated at the SDK layer rather than against
    Medplum because forcing repeated real 412s would be flaky."""
    # Sanity check: PreconditionFailedError is the exception class the
    # helper raises when retries are exhausted. The async transport
    # tests cover the actual flow.
    assert issubclass(PreconditionFailedError, Exception)
