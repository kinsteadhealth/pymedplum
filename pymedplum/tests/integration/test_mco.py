"""Multi-tenant Organization (MCO) Test

This test validates organization-based access control in a multi-tenant scenario.
Uses fhir.resources for type-safe resource creation.

All helpers are now in conftest.py for reuse across test files.
"""

import pytest

from pymedplum import to_fhir_json, to_portable
from pymedplum.fhir.patient import Patient


@pytest.fixture
def mco_setup(
    medplum_client,
    test_id,
    create_test_org,
    create_test_practitioner,
    create_test_patient,
    create_test_access_policy,
    create_test_membership,
):
    """Set up MCO environment with 2 orgs, 3 practitioners, and test patients"""
    cleanup = []

    try:
        # Create organizations
        org_a = create_test_org("A", test_id)
        org_b = create_test_org("B", test_id)
        cleanup.extend([("Organization", org_a["id"]), ("Organization", org_b["id"])])

        # Create practitioners
        practitioners = {
            "admin": create_test_practitioner("Admin Test", test_id),
            "doctor_a": create_test_practitioner("Doctor A", test_id),
            "doctor_b": create_test_practitioner("Doctor B", test_id),
        }
        cleanup.extend([("Practitioner", p["id"]) for p in practitioners.values()])

        # Create access policies
        policies = {
            "admin": create_test_access_policy("Admin Policy", test_id),
            "doctor_a": create_test_access_policy("Doctor A Policy", test_id),
            "doctor_b": create_test_access_policy("Doctor B Policy", test_id),
        }
        cleanup.extend([("AccessPolicy", p["id"]) for p in policies.values()])

        # Get project ID from environment or use default
        project_id = (
            medplum_client.project_id if hasattr(medplum_client, "project_id") else None
        )

        # Create project memberships using invite API
        memberships = {}
        if project_id:
            memberships = {
                "admin": create_test_membership(
                    project_id,
                    practitioners["admin"],
                    policies["admin"]["id"],
                    test_id,
                ),
                "doctor_a": create_test_membership(
                    project_id,
                    practitioners["doctor_a"],
                    policies["doctor_a"]["id"],
                    test_id,
                ),
                "doctor_b": create_test_membership(
                    project_id,
                    practitioners["doctor_b"],
                    policies["doctor_b"]["id"],
                    test_id,
                ),
            }
            cleanup.extend(
                [("ProjectMembership", m["id"]) for m in memberships.values() if m]
            )
        else:
            print("Note: PROJECT_ID not available, skipping ProjectMembership creation")
            memberships = {"admin": None, "doctor_a": None, "doctor_b": None}

        # Create test patients
        patients = {
            "a1": create_test_patient("Alice", "OrgA-Patient1", org_a["id"], test_id),
            "a2": create_test_patient("Andrew", "OrgA-Patient2", org_a["id"], test_id),
            "b1": create_test_patient("Bob", "OrgB-Patient1", org_b["id"], test_id),
        }
        cleanup.extend([("Patient", p["id"]) for p in patients.values()])

        yield {
            "orgs": {"a": org_a, "b": org_b},
            "practitioners": practitioners,
            "policies": policies,
            "memberships": memberships,
            "patients": patients,
            "test_id": test_id,
        }

    finally:
        for resource_type, resource_id in reversed(cleanup):
            try:
                medplum_client.delete_resource(resource_type, resource_id)
            except Exception as e:
                print(f"Warning: Failed to delete {resource_type}/{resource_id}: {e}")


def test_organizations_created(mco_setup):
    """Test that both organizations were created"""
    assert "Test Org A" in mco_setup["orgs"]["a"]["name"]
    assert "Test Org B" in mco_setup["orgs"]["b"]["name"]


def test_practitioners_created(mco_setup):
    """Test that all practitioners were created"""
    assert len(mco_setup["practitioners"]) == 3
    assert all(
        p["resourceType"] == "Practitioner" for p in mco_setup["practitioners"].values()
    )


def test_access_policies_created(mco_setup):
    """Test that access policies were created with correct resource types"""
    admin_policy = mco_setup["policies"]["admin"]
    doctor_a_policy = mco_setup["policies"]["doctor_a"]
    doctor_b_policy = mco_setup["policies"]["doctor_b"]

    # Verify all policies have the expected resource types
    for policy in [admin_policy, doctor_a_policy, doctor_b_policy]:
        assert policy["resourceType"] == "AccessPolicy"
        resource_types = {r["resourceType"] for r in policy["resource"]}
        assert "Patient" in resource_types
        assert "Organization" in resource_types
        assert "Practitioner" in resource_types


def test_patients_tagged_correctly(mco_setup):
    """Test that patients have correct org tags"""
    org_a_id = mco_setup["orgs"]["a"]["id"]
    org_b_id = mco_setup["orgs"]["b"]["id"]

    # Helper to check org in accounts
    def has_org(patient, org_id):
        return any(
            acc.get("reference") == f"Organization/{org_id}"
            for acc in patient.get("meta", {}).get("accounts", [])
        )

    assert has_org(mco_setup["patients"]["a1"], org_a_id)
    assert has_org(mco_setup["patients"]["a2"], org_a_id)
    assert has_org(mco_setup["patients"]["b1"], org_b_id)
    assert not has_org(mco_setup["patients"]["b1"], org_a_id)


def test_search_patients_by_organization(medplum_client, mco_setup):
    """Test patient search and org tag verification"""
    # Search for our test patients using unique test ID
    bundle = medplum_client.search_resources(
        "Patient", {"family:contains": mco_setup["test_id"]}
    )
    found_ids = {
        e["resource"]["id"] for e in bundle.get("entry", []) if "resource" in e
    }

    # Verify all test patients are findable
    assert all(p["id"] in found_ids for p in mco_setup["patients"].values())

    # Verify org tags are distinct
    org_a_id = mco_setup["orgs"]["a"]["id"]
    org_b_id = mco_setup["orgs"]["b"]["id"]

    patient_a1 = medplum_client.read_resource(
        "Patient", mco_setup["patients"]["a1"]["id"]
    )
    patient_b1 = medplum_client.read_resource(
        "Patient", mco_setup["patients"]["b1"]["id"]
    )

    a1_accounts = [acc["reference"] for acc in patient_a1["meta"]["accounts"]]
    b1_accounts = [acc["reference"] for acc in patient_b1["meta"]["accounts"]]

    assert f"Organization/{org_a_id}" in a1_accounts
    assert f"Organization/{org_b_id}" not in a1_accounts
    assert f"Organization/{org_b_id}" in b1_accounts
    assert f"Organization/{org_a_id}" not in b1_accounts


def test_on_behalf_of_context(create_scoped_client, mco_setup):
    """Test default_on_behalf_of with scoped client"""
    if mco_setup["memberships"]["doctor_a"] is None:
        pytest.skip("ProjectMembership not supported")

    membership_id = mco_setup["memberships"]["doctor_a"]["id"]
    patient_id = mco_setup["patients"]["a1"]["id"]

    scoped_client = create_scoped_client(membership_id)
    try:
        patient = scoped_client.read_resource("Patient", patient_id)
        assert patient["id"] == patient_id
    finally:
        scoped_client.close()


def test_on_behalf_of_search(create_scoped_client, mco_setup):
    """Test searching for patients with scoped client"""
    if mco_setup["memberships"]["doctor_a"] is None:
        pytest.skip("ProjectMembership not supported")

    membership_id = mco_setup["memberships"]["doctor_a"]["id"]

    scoped_client = create_scoped_client(membership_id)
    try:
        bundle = scoped_client.search_resources(
            "Patient", {"family:contains": mco_setup["test_id"]}
        )
        found_patients = [
            e["resource"] for e in bundle.get("entry", []) if "resource" in e
        ]

        # Should find at least org A patients
        found_ids = {p["id"] for p in found_patients}
        assert mco_setup["patients"]["a1"]["id"] in found_ids
        assert mco_setup["patients"]["a2"]["id"] in found_ids
    finally:
        scoped_client.close()


def test_on_behalf_of_nested_contexts(create_scoped_client, mco_setup):
    """Test that context manager can override default_on_behalf_of"""
    if not all(mco_setup["memberships"].values()):
        pytest.skip("ProjectMembership not supported")

    admin_id = mco_setup["memberships"]["admin"]["id"]
    doctor_a_id = mco_setup["memberships"]["doctor_a"]["id"]
    patient_id = mco_setup["patients"]["a1"]["id"]

    # Create client with default as admin
    admin_client = create_scoped_client(admin_id)
    try:
        # Default context (admin)
        patient1 = admin_client.read_resource("Patient", patient_id)
        assert patient1["id"] == patient_id

        # Override with context manager (doctor_a)
        with admin_client.on_behalf_of(f"ProjectMembership/{doctor_a_id}"):
            patient2 = admin_client.read_resource("Patient", patient_id)
            assert patient2["id"] == patient_id

        # Back to default context (admin) after context manager exits
        patient3 = admin_client.read_resource("Patient", patient_id)
        assert patient3["id"] == patient_id
    finally:
        admin_client.close()


def test_on_behalf_of_update_resource(medplum_client, create_scoped_client, mco_setup):
    """Test updating resources with scoped client for audit trail"""
    if mco_setup["memberships"]["doctor_a"] is None:
        pytest.skip("ProjectMembership not supported")

    membership_id = mco_setup["memberships"]["doctor_a"]["id"]
    patient = mco_setup["patients"]["a1"].copy()

    scoped_client = create_scoped_client(membership_id)
    try:
        patient["gender"] = "male"  # Change gender for testing
        updated = scoped_client.update_resource(patient)

        # Verify update worked
        assert updated["gender"] == "male"

        # Medplum tracks who performed the action in meta.onBehalfOf
        # This references the profile (Practitioner) not the ProjectMembership
        if "meta" in updated and "onBehalfOf" in updated.get("meta", {}):
            on_behalf_of = updated["meta"]["onBehalfOf"]
            assert "Practitioner" in on_behalf_of.get("reference", "")
    finally:
        scoped_client.close()

    # Restore original gender
    patient["gender"] = "female"
    medplum_client.update_resource(patient)


def test_on_behalf_of_different_members(create_scoped_client, mco_setup):
    """Test that different scoped clients have access to their respective org patients"""
    if not all(
        [mco_setup["memberships"]["doctor_a"], mco_setup["memberships"]["doctor_b"]]
    ):
        pytest.skip("ProjectMembership not supported")

    doctor_a_id = mco_setup["memberships"]["doctor_a"]["id"]
    doctor_b_id = mco_setup["memberships"]["doctor_b"]["id"]

    # Doctor A accessing Org A patient
    doctor_a_client = create_scoped_client(doctor_a_id)
    try:
        patient_a = doctor_a_client.read_resource(
            "Patient", mco_setup["patients"]["a1"]["id"]
        )
        assert patient_a["name"][0]["given"][0] == "Alice"
    finally:
        doctor_a_client.close()

    # Doctor B accessing Org B patient
    doctor_b_client = create_scoped_client(doctor_b_id)
    try:
        patient_b = doctor_b_client.read_resource(
            "Patient", mco_setup["patients"]["b1"]["id"]
        )
        assert patient_b["name"][0]["given"][0] == "Bob"
    finally:
        doctor_b_client.close()


def test_on_behalf_of_create_resource(medplum_client, create_scoped_client, mco_setup):
    """Test creating resources with scoped client sets proper audit fields"""
    if mco_setup["memberships"]["doctor_a"] is None:
        pytest.skip("ProjectMembership not supported")

    membership_id = mco_setup["memberships"]["doctor_a"]["id"]
    org_a_id = mco_setup["orgs"]["a"]["id"]
    test_id = mco_setup["test_id"]

    scoped_client = create_scoped_client(membership_id)
    try:
        new_patient = scoped_client.create_resource(
            {
                "resourceType": "Patient",
                "name": [{"given": ["TestCreate"], "family": f"OBO-{test_id}"}],
                "gender": "female",
            },
            org_mode="accounts",
            org_ref=f"Organization/{org_a_id}",
        )

        # Verify patient was created
        assert new_patient["id"]
        assert new_patient["name"][0]["given"][0] == "TestCreate"

        # Verify org tagging
        assert any(
            acc.get("reference") == f"Organization/{org_a_id}"
            for acc in new_patient.get("meta", {}).get("accounts", [])
        )

        # Cleanup
        medplum_client.delete_resource("Patient", new_patient["id"])
    finally:
        scoped_client.close()


def test_org_tag_idempotent(medplum_client, mco_setup):
    """Test that org tagging is idempotent"""
    patient = mco_setup["patients"]["a1"]
    org_ref = f"Organization/{mco_setup['orgs']['a']['id']}"

    initial_count = len(patient["meta"]["accounts"])

    # Update multiple times
    for _ in range(3):
        patient = medplum_client.update_resource(
            patient, org_mode="accounts", org_ref=org_ref
        )

    # Verify no duplicates
    assert len(patient["meta"]["accounts"]) == initial_count
    org_count = sum(
        1 for acc in patient["meta"]["accounts"] if acc.get("reference") == org_ref
    )
    assert org_count == 1


def test_fhir_resources_roundtrip(medplum_client, mco_setup):
    """Test that we can read a resource and parse it with fhir.resources"""
    patient_dict = medplum_client.read_resource(
        "Patient", mco_setup["patients"]["a1"]["id"]
    )

    # Medplum returns vendor-specific meta fields (accounts, author, project, etc.)
    # Convert to portable FHIR extensions for strict validation
    portable_patient = to_portable(patient_dict)

    # Parse with fhir.resources - this validates the structure
    patient_model = Patient(**portable_patient)

    # Verify key fields
    assert patient_model.id == mco_setup["patients"]["a1"]["id"]
    # Use the Python field name (resource_type) not the FHIR alias (resourceType)
    assert patient_model.resource_type == "Patient"
    assert len(patient_model.name) == 1
    assert patient_model.name[0].given[0] == "Alice"
    assert patient_model.gender == "female"

    # Verify org link is preserved as extension
    org_ext_url = "https://example.org/fhir/StructureDefinition/orgLink"
    org_extensions = [
        ext for ext in patient_model.meta.extension or [] if ext.url == org_ext_url
    ]
    assert len(org_extensions) > 0, "Organization link should be preserved as extension"

    # Convert back and verify it matches
    patient_json = to_fhir_json(patient_model)
    assert patient_json["id"] == patient_dict["id"]
    assert patient_json["resourceType"] == patient_dict["resourceType"]
