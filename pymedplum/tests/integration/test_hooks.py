"""Integration tests for `on_request_complete` events against live Medplum.

Focused on what unit tests with respx can't verify:

- `wire_on_behalf_of` populated from the actual outgoing OBO header
- bundle/transaction action against the real FHIR root endpoint
- action mapping stable across a representative sequence of calls on a
  single client
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from pymedplum import MedplumClient
from pymedplum.fhir import Patient

if TYPE_CHECKING:
    from pymedplum.hooks import RequestEvent


@pytest.fixture
def hooked_client(medplum_credentials):
    events: list[RequestEvent] = []
    client = MedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
        project_id=os.getenv("MEDPLUM_PROJECT_ID"),
        on_request_complete=events.append,
    )
    yield client, events
    client.close()


def test_hook_captures_wire_on_behalf_of_from_real_header(
    hooked_client, medplum_membership
):
    client, events = hooked_client
    with client.on_behalf_of(medplum_membership):
        client.create_resource(
            Patient(name=[{"family": "OBOHookTest", "given": ["Wire"]}])
        )

    creates = [
        e for e in events if e.resource_type == "Patient" and e.action == "create"
    ]
    assert len(creates) == 1
    obo_attempts = [a for a in creates[0].attempts if a.on_behalf_of]
    assert obo_attempts, "no attempt recorded an OBO header"
    assert obo_attempts[-1].on_behalf_of == f"ProjectMembership/{medplum_membership}"


def test_hook_classifies_bundle_post_at_fhir_root(hooked_client):
    client, events = hooked_client
    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "BundleHookTest", "given": ["Txn"]}],
                },
                "request": {"method": "POST", "url": "Patient"},
            }
        ],
    }
    client.execute_batch(bundle)

    bundle_events = [e for e in events if e.action == "batch_or_transaction"]
    assert len(bundle_events) == 1
    assert bundle_events[0].resource_type is None
    assert bundle_events[0].operation is None
    assert bundle_events[0].outcome == "success"


def test_action_mapping_stable_across_a_session(hooked_client):
    client, events = hooked_client
    created = client.create_resource(
        Patient(name=[{"family": "SessionHookTest", "given": ["Mix"]}])
    )
    client.read_resource("Patient", created["id"])
    client.search_resources("Patient", {"_count": "1"})
    client.execute_operation("Patient", "everything", resource_id=created["id"])
    client.execute_graphql("query { PatientList(_count: 1) { id } }")

    fhir_events = [e for e in events if e.action is not None]
    actions = [e.action for e in fhir_events]
    assert "create" in actions
    assert "read" in actions
    assert "search" in actions
    assert "operation" in actions
    op_events = [e for e in fhir_events if e.action == "operation"]
    operations = {e.operation for e in op_events}
    assert "$everything" in operations
    assert "$graphql" in operations
    assert all(e.outcome == "success" for e in fhir_events)
