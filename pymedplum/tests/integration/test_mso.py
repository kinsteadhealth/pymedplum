"""Multi-tenant MSO (Management Services Organization) Tests

Validates organization-based access control in a multi-tenant scenario.
"""

import secrets

import pytest

from pymedplum import (
    AsyncMedplumClient,
    get_resource_accounts,
    resource_has_account,
)


def _extract_practitioner_id(membership: dict) -> str:
    return membership["profile"]["reference"].split("/")[1]


def _bundle_ids(bundle: dict) -> set[str]:
    return {e["resource"]["id"] for e in bundle.get("entry", []) if "resource" in e}


def _create_mso_env(medplum_client, test_id, prefix, extra_resources=None):
    """Create 2 orgs, a compartment policy, and 2 practitioners with
    parameterized access. Returns (orgs, memberships, cleanup_list)."""
    cleanup = []
    project_id = medplum_client.project_id

    org_a = medplum_client.create_resource(
        {"resourceType": "Organization", "name": f"{prefix} A - {test_id}"}
    )
    org_b = medplum_client.create_resource(
        {"resourceType": "Organization", "name": f"{prefix} B - {test_id}"}
    )
    cleanup.extend(
        [
            ("Organization", org_a["id"]),
            ("Organization", org_b["id"]),
        ]
    )

    resource_entries = [
        {
            "resourceType": "Patient",
            "criteria": "Patient?_compartment=%organization",
        },
        {"resourceType": "Organization"},
        {"resourceType": "Practitioner"},
    ]
    if extra_resources:
        resource_entries.extend(extra_resources)

    policy = medplum_client.create_resource(
        {
            "resourceType": "AccessPolicy",
            "name": f"{prefix} Policy - {test_id}",
            "compartment": {"reference": "%organization"},
            "resource": resource_entries,
        }
    )
    cleanup.append(("AccessPolicy", policy["id"]))

    memberships = {}
    for label, org in [("PracA", org_a), ("PracB", org_b)]:
        email = f"{label.lower()}.{prefix.lower()}.{test_id}@test.example.com"
        membership = medplum_client.invite_user(
            project_id=project_id,
            resource_type="Practitioner",
            first_name=label,
            last_name=test_id,
            email=email,
            password=secrets.token_urlsafe(32),
            send_email=False,
            access_policy=f"AccessPolicy/{policy['id']}",
        )
        if membership:
            cleanup.append(("ProjectMembership", membership["id"]))
            membership["access"] = [
                {
                    "policy": {"reference": f"AccessPolicy/{policy['id']}"},
                    "parameter": [
                        {
                            "name": "organization",
                            "valueReference": {
                                "reference": f"Organization/{org['id']}"
                            },
                        }
                    ],
                }
            ]
            medplum_client.update_resource(membership)
            memberships[label] = membership

    return {
        "org_a": org_a,
        "org_b": org_b,
        "policy": policy,
        "memberships": memberships,
        "cleanup": cleanup,
    }


@pytest.fixture
def async_client(medplum_credentials):
    """Factory for authenticated async clients."""

    async def _create(**kwargs):
        client = AsyncMedplumClient(
            client_id=medplum_credentials["client_id"],
            client_secret=medplum_credentials["client_secret"],
            **kwargs,
        )
        return client

    return _create


@pytest.fixture
def mso_setup(
    medplum_client,
    test_id,
    create_test_org,
    create_test_patient,
    create_test_access_policy,
    create_test_membership,
):
    """Set up MSO environment with 2 orgs, 3 practitioners, and test patients"""
    project_id = medplum_client.project_id
    if not project_id:
        pytest.skip("MEDPLUM_PROJECT_ID must be set for MSO tests")

    cleanup = []

    try:
        org_a = create_test_org("A", test_id)
        org_b = create_test_org("B", test_id)
        cleanup.extend(
            [
                ("Organization", org_a["id"]),
                ("Organization", org_b["id"]),
            ]
        )

        policies = {
            "admin": create_test_access_policy("Admin Policy", test_id),
            "doctor_a": create_test_access_policy("Doctor A Policy", test_id),
            "doctor_b": create_test_access_policy("Doctor B Policy", test_id),
        }
        cleanup.extend([("AccessPolicy", p["id"]) for p in policies.values()])

        memberships = {}
        practitioners = {}
        members = [
            ("admin", "Admin", "Test", policies["admin"]),
            ("doctor_a", "Doctor", "A", policies["doctor_a"]),
            ("doctor_b", "Doctor", "B", policies["doctor_b"]),
        ]
        for key, first, last, policy in members:
            m = create_test_membership(project_id, first, last, policy["id"], test_id)
            if m:
                memberships[key] = m
                practitioners[key] = {
                    "id": _extract_practitioner_id(m),
                    "resourceType": "Practitioner",
                }
                cleanup.append(("ProjectMembership", m["id"]))

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


def test_organizations_created(mso_setup):
    assert "Test Org A" in mso_setup["orgs"]["a"]["name"]
    assert "Test Org B" in mso_setup["orgs"]["b"]["name"]


def test_practitioners_created(mso_setup):
    assert len(mso_setup["practitioners"]) == 3
    assert all(
        p["resourceType"] == "Practitioner" for p in mso_setup["practitioners"].values()
    )


def test_access_policies_created(mso_setup):
    for policy in mso_setup["policies"].values():
        assert policy["resourceType"] == "AccessPolicy"
        resource_types = {r["resourceType"] for r in policy["resource"]}
        assert {"Patient", "Organization", "Practitioner"} <= resource_types


def test_patients_tagged_correctly(mso_setup):
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    org_b_ref = f"Organization/{mso_setup['orgs']['b']['id']}"

    assert resource_has_account(mso_setup["patients"]["a1"], org_a_ref)
    assert resource_has_account(mso_setup["patients"]["a2"], org_a_ref)
    assert resource_has_account(mso_setup["patients"]["b1"], org_b_ref)
    assert not resource_has_account(mso_setup["patients"]["b1"], org_a_ref)


def test_search_patients_by_organization(medplum_client, mso_setup):
    bundle = medplum_client.search_resources(
        "Patient", {"family:contains": mso_setup["test_id"]}
    )
    found_ids = _bundle_ids(bundle)
    assert all(p["id"] in found_ids for p in mso_setup["patients"].values())

    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    org_b_ref = f"Organization/{mso_setup['orgs']['b']['id']}"

    patient_a1 = medplum_client.read_resource(
        "Patient", mso_setup["patients"]["a1"]["id"]
    )
    patient_b1 = medplum_client.read_resource(
        "Patient", mso_setup["patients"]["b1"]["id"]
    )

    a1_accounts = get_resource_accounts(patient_a1)
    b1_accounts = get_resource_accounts(patient_b1)

    assert org_a_ref in a1_accounts
    assert org_b_ref not in a1_accounts
    assert org_b_ref in b1_accounts
    assert org_a_ref not in b1_accounts


def test_on_behalf_of_context(create_scoped_client, mso_setup):
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]
    patient_id = mso_setup["patients"]["a1"]["id"]

    scoped_client = create_scoped_client(membership_id)
    try:
        patient = scoped_client.read_resource("Patient", patient_id)
        assert patient["id"] == patient_id
    finally:
        scoped_client.close()


def test_on_behalf_of_search(create_scoped_client, mso_setup):
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]

    scoped_client = create_scoped_client(membership_id)
    try:
        bundle = scoped_client.search_resources(
            "Patient", {"family:contains": mso_setup["test_id"]}
        )
        found_ids = _bundle_ids(bundle)
        assert mso_setup["patients"]["a1"]["id"] in found_ids
        assert mso_setup["patients"]["a2"]["id"] in found_ids
    finally:
        scoped_client.close()


def test_on_behalf_of_nested_contexts(create_scoped_client, mso_setup):
    admin_id = mso_setup["memberships"]["admin"]["id"]
    doctor_a_id = mso_setup["memberships"]["doctor_a"]["id"]
    patient_id = mso_setup["patients"]["a1"]["id"]

    admin_client = create_scoped_client(admin_id)
    try:
        patient1 = admin_client.read_resource("Patient", patient_id)
        assert patient1["id"] == patient_id

        with admin_client.on_behalf_of(f"ProjectMembership/{doctor_a_id}"):
            patient2 = admin_client.read_resource("Patient", patient_id)
            assert patient2["id"] == patient_id

        patient3 = admin_client.read_resource("Patient", patient_id)
        assert patient3["id"] == patient_id
    finally:
        admin_client.close()


def test_on_behalf_of_update_resource(medplum_client, create_scoped_client, mso_setup):
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]
    patient = mso_setup["patients"]["a1"].copy()

    scoped_client = create_scoped_client(membership_id)
    try:
        patient["gender"] = "male"
        updated = scoped_client.update_resource(patient)
        assert updated["gender"] == "male"

        obo = updated.get("meta", {}).get("onBehalfOf", {})
        if obo:
            assert "Practitioner" in obo.get("reference", "")
    finally:
        scoped_client.close()

    patient["gender"] = "female"
    medplum_client.update_resource(patient)


def test_on_behalf_of_different_members(create_scoped_client, mso_setup):
    for doctor_key, patient_key, expected_name in [
        ("doctor_a", "a1", "Alice"),
        ("doctor_b", "b1", "Bob"),
    ]:
        client = create_scoped_client(mso_setup["memberships"][doctor_key]["id"])
        try:
            patient = client.read_resource(
                "Patient", mso_setup["patients"][patient_key]["id"]
            )
            assert patient["name"][0]["given"][0] == expected_name
        finally:
            client.close()


def test_on_behalf_of_create_resource(medplum_client, create_scoped_client, mso_setup):
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    test_id = mso_setup["test_id"]

    scoped_client = create_scoped_client(membership_id)
    try:
        new_patient = scoped_client.create_resource(
            {
                "resourceType": "Patient",
                "name": [{"given": ["TestCreate"], "family": f"OBO-{test_id}"}],
                "gender": "female",
            },
            accounts=org_a_ref,
        )

        assert new_patient["id"]
        assert new_patient["name"][0]["given"][0] == "TestCreate"
        assert resource_has_account(new_patient, org_a_ref)

        medplum_client.delete_resource("Patient", new_patient["id"])
    finally:
        scoped_client.close()


def test_set_accounts_idempotent(medplum_client, mso_setup):
    patient_id = mso_setup["patients"]["a1"]["id"]
    org_ref = f"Organization/{mso_setup['orgs']['a']['id']}"

    patient = medplum_client.read_resource("Patient", patient_id)
    initial_count = len(patient["meta"]["accounts"])

    for _ in range(3):
        medplum_client.set_accounts(f"Patient/{patient_id}", org_ref)

    patient = medplum_client.read_resource("Patient", patient_id)
    assert len(patient["meta"]["accounts"]) == initial_count
    org_count = sum(
        1 for acc in patient["meta"]["accounts"] if acc.get("reference") == org_ref
    )
    assert org_count == 1


def test_set_accounts_operation(medplum_client, mso_setup):
    """Test the $set-accounts operation via set_accounts method."""
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    org_b_ref = f"Organization/{mso_setup['orgs']['b']['id']}"

    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["SetAccounts"], "family": "TestPatient"}],
            "gender": "other",
        }
    )

    try:
        result = medplum_client.set_accounts(f"Patient/{patient['id']}", org_a_ref)
        assert result["resourceType"] in ("Parameters", "Patient")

        updated = medplum_client.read_resource("Patient", patient["id"])
        assert resource_has_account(updated, org_a_ref)

        result2 = medplum_client.set_accounts(f"Patient/{patient['id']}", org_b_ref)
        assert result2["resourceType"] in ("Parameters", "Patient")

        updated2 = medplum_client.read_resource("Patient", patient["id"])
        assert resource_has_account(updated2, org_b_ref)
    finally:
        medplum_client.delete_resource("Patient", patient["id"])


@pytest.mark.asyncio
async def test_async_on_behalf_of_context(async_client, mso_setup):
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]
    patient_id = mso_setup["patients"]["a1"]["id"]

    async with await async_client(
        default_on_behalf_of=f"ProjectMembership/{membership_id}",
    ) as client:
        patient = await client.read_resource("Patient", patient_id)
        assert patient["id"] == patient_id


@pytest.mark.asyncio
async def test_async_on_behalf_of_create_resource(
    medplum_client, async_client, mso_setup
):
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    test_id = mso_setup["test_id"]

    async with await async_client() as client:
        async with client.on_behalf_of(f"ProjectMembership/{membership_id}"):
            new_patient = await client.create_resource(
                {
                    "resourceType": "Patient",
                    "name": [
                        {
                            "given": ["AsyncCreate"],
                            "family": f"OBO-{test_id}",
                        }
                    ],
                    "gender": "female",
                },
                accounts=org_a_ref,
            )

        assert new_patient["id"]
        assert new_patient["name"][0]["given"][0] == "AsyncCreate"
        assert resource_has_account(new_patient, org_a_ref)

        medplum_client.delete_resource("Patient", new_patient["id"])


@pytest.mark.asyncio
async def test_async_on_behalf_of_nested_contexts(async_client, mso_setup):
    admin_id = mso_setup["memberships"]["admin"]["id"]
    doctor_a_id = mso_setup["memberships"]["doctor_a"]["id"]
    patient_id = mso_setup["patients"]["a1"]["id"]

    async with await async_client(
        default_on_behalf_of=f"ProjectMembership/{admin_id}",
    ) as client:
        patient1 = await client.read_resource("Patient", patient_id)
        assert patient1["id"] == patient_id

        async with client.on_behalf_of(f"ProjectMembership/{doctor_a_id}"):
            patient2 = await client.read_resource("Patient", patient_id)
            assert patient2["id"] == patient_id

        patient3 = await client.read_resource("Patient", patient_id)
        assert patient3["id"] == patient_id


def test_multi_org_access_allowed(create_scoped_client, mso_setup):
    """Admin can access patients across organizations."""
    admin_id = mso_setup["memberships"]["admin"]["id"]

    admin_client = create_scoped_client(admin_id)
    try:
        patient_a = admin_client.read_resource(
            "Patient", mso_setup["patients"]["a1"]["id"]
        )
        assert patient_a["name"][0]["given"][0] == "Alice"

        patient_b = admin_client.read_resource(
            "Patient", mso_setup["patients"]["b1"]["id"]
        )
        assert patient_b["name"][0]["given"][0] == "Bob"
    finally:
        admin_client.close()


def test_on_behalf_of_header_sent(create_scoped_client, mso_setup):
    """Verify X-Medplum-On-Behalf-Of header is sent on requests."""
    membership_id = mso_setup["memberships"]["doctor_a"]["id"]
    header_was_set = False

    def check_headers(method, url, headers, kwargs):
        nonlocal header_was_set
        if "X-Medplum-On-Behalf-Of" in headers:
            header_was_set = True
            expected = f"ProjectMembership/{membership_id}"
            assert headers["X-Medplum-On-Behalf-Of"] == expected

    scoped_client = create_scoped_client(membership_id)
    scoped_client.before_request = check_headers

    try:
        scoped_client.search_resources("Patient", {"_count": "1"})
        assert header_was_set, "X-Medplum-On-Behalf-Of header was not set"
    finally:
        scoped_client.close()


def test_set_accounts_single_ref(medplum_client):
    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["SingleRef"], "family": "Test"}],
        }
    )
    org = medplum_client.create_resource(
        {"resourceType": "Organization", "name": "SingleRef Org"}
    )

    try:
        result = medplum_client.set_accounts(
            f"Patient/{patient['id']}", f"Organization/{org['id']}"
        )
        assert result["resourceType"] in ("Parameters", "Patient")

        updated = medplum_client.read_resource("Patient", patient["id"])
        assert resource_has_account(updated, f"Organization/{org['id']}")
    finally:
        medplum_client.delete_resource("Patient", patient["id"])
        medplum_client.delete_resource("Organization", org["id"])


def test_set_accounts_multiple_refs(medplum_client):
    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["MultiRef"], "family": "Test"}],
        }
    )
    org_a = medplum_client.create_resource(
        {"resourceType": "Organization", "name": "MultiRef Org A"}
    )
    org_b = medplum_client.create_resource(
        {"resourceType": "Organization", "name": "MultiRef Org B"}
    )

    try:
        result = medplum_client.set_accounts(
            f"Patient/{patient['id']}",
            [
                f"Organization/{org_a['id']}",
                f"Organization/{org_b['id']}",
            ],
        )
        assert result["resourceType"] in ("Parameters", "Patient")

        updated = medplum_client.read_resource("Patient", patient["id"])
        accounts = get_resource_accounts(updated)
        assert f"Organization/{org_a['id']}" in accounts
        assert f"Organization/{org_b['id']}" in accounts
    finally:
        medplum_client.delete_resource("Patient", patient["id"])
        medplum_client.delete_resource("Organization", org_a["id"])
        medplum_client.delete_resource("Organization", org_b["id"])


def test_set_accounts_with_propagate(medplum_client):
    """Verify propagate=True cascades accounts to related resources."""
    org = medplum_client.create_resource(
        {"resourceType": "Organization", "name": "Propagate Org"}
    )
    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["Propagate"], "family": "Test"}],
        }
    )
    observation = medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "29463-7",
                        "display": "Body Weight",
                    }
                ]
            },
            "subject": {"reference": f"Patient/{patient['id']}"},
            "valueQuantity": {"value": 70, "unit": "kg"},
        }
    )
    org_ref = f"Organization/{org['id']}"

    try:
        medplum_client.set_accounts(f"Patient/{patient['id']}", org_ref, propagate=True)

        updated_patient = medplum_client.read_resource("Patient", patient["id"])
        assert resource_has_account(updated_patient, org_ref)

        updated_obs = medplum_client.read_resource("Observation", observation["id"])
        assert resource_has_account(updated_obs, org_ref), (
            f"Expected {org_ref} in observation accounts "
            f"{get_resource_accounts(updated_obs)}"
        )
    finally:
        medplum_client.delete_resource("Observation", observation["id"])
        medplum_client.delete_resource("Patient", patient["id"])
        medplum_client.delete_resource("Organization", org["id"])


def test_set_accounts_prefer_async_and_wait(medplum_client):
    """Test the full async flow: set_accounts → wait_for_async_job."""
    org = medplum_client.create_resource(
        {"resourceType": "Organization", "name": "AsyncFlow Org"}
    )
    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["AsyncFlow"], "family": "Test"}],
        }
    )
    org_ref = f"Organization/{org['id']}"

    try:
        result = medplum_client.set_accounts(
            f"Patient/{patient['id']}",
            org_ref,
            propagate=True,
            prefer_async=True,
        )

        assert result["resourceType"] == "OperationOutcome"
        assert result["issue"][0]["diagnostics"]

        job = medplum_client.wait_for_async_job(result, timeout=30)
        assert job["status"] == "completed"

        updated = medplum_client.read_resource("Patient", patient["id"])
        assert resource_has_account(updated, org_ref)
    finally:
        medplum_client.delete_resource("Patient", patient["id"])
        medplum_client.delete_resource("Organization", org["id"])


def test_get_async_job_status_single_check(medplum_client):
    """Test get_async_job_status for a single non-polling check."""
    org = medplum_client.create_resource(
        {"resourceType": "Organization", "name": "StatusCheck Org"}
    )
    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["StatusCheck"], "family": "Test"}],
        }
    )

    try:
        result = medplum_client.set_accounts(
            f"Patient/{patient['id']}",
            f"Organization/{org['id']}",
            propagate=True,
            prefer_async=True,
        )

        job = medplum_client.get_async_job_status(result)
        assert job["resourceType"] == "AsyncJob"
        assert job["status"] in (
            "accepted",
            "active",
            "completed",
        )
    finally:
        medplum_client.delete_resource("Patient", patient["id"])
        medplum_client.delete_resource("Organization", org["id"])


def test_set_accounts_with_practitioner_ref(medplum_client, mso_setup):
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    prac_ref = f"Practitioner/{mso_setup['practitioners']['doctor_a']['id']}"

    patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "name": [{"given": ["MixedRefs"], "family": "Test"}],
        }
    )

    try:
        medplum_client.set_accounts(f"Patient/{patient['id']}", [org_a_ref, prac_ref])

        updated = medplum_client.read_resource("Patient", patient["id"])
        accounts = get_resource_accounts(updated)
        assert org_a_ref in accounts
        assert prac_ref in accounts
    finally:
        medplum_client.delete_resource("Patient", patient["id"])


@pytest.mark.asyncio
async def test_set_accounts_async(async_client, mso_setup):
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"

    async with await async_client() as client:
        patient = await client.create_resource(
            {
                "resourceType": "Patient",
                "name": [{"given": ["AsyncSetAccounts"], "family": "Test"}],
            }
        )

        try:
            result = await client.set_accounts(f"Patient/{patient['id']}", org_a_ref)
            assert result["resourceType"] in ("Parameters", "Patient")

            updated = await client.read_resource("Patient", patient["id"])
            assert resource_has_account(updated, org_a_ref)
        finally:
            await client.delete_resource("Patient", patient["id"])


def test_resource_has_account_helper(medplum_client, mso_setup):
    org_a_ref = f"Organization/{mso_setup['orgs']['a']['id']}"
    org_b_ref = f"Organization/{mso_setup['orgs']['b']['id']}"

    patient_a1 = medplum_client.read_resource(
        "Patient", mso_setup["patients"]["a1"]["id"]
    )

    assert resource_has_account(patient_a1, org_a_ref)
    assert not resource_has_account(patient_a1, org_b_ref)


def test_get_resource_accounts_helper(medplum_client, mso_setup):
    patient_a1 = medplum_client.read_resource(
        "Patient", mso_setup["patients"]["a1"]["id"]
    )

    accounts = get_resource_accounts(patient_a1)
    assert isinstance(accounts, list)
    assert len(accounts) >= 1
    assert f"Organization/{mso_setup['orgs']['a']['id']}" in accounts


def test_get_resource_accounts_no_meta():
    assert get_resource_accounts({"resourceType": "Patient"}) == []


def test_resource_has_account_no_meta():
    assert not resource_has_account({"resourceType": "Patient"}, "Organization/abc")


def test_mso_compartment_isolation(medplum_client, create_scoped_client, test_id):
    """Full MSO flow: compartment-based AccessPolicy with %organization,
    parameterized membership access, cross-org isolation via OBO.
    """
    if not medplum_client.project_id:
        pytest.skip("MEDPLUM_PROJECT_ID must be set")

    env = _create_mso_env(
        medplum_client,
        test_id,
        "Iso",
        extra_resources=[
            {
                "resourceType": "Observation",
                "criteria": "Observation?_compartment=%organization",
            }
        ],
    )
    cleanup = list(env["cleanup"])

    try:
        patient_a = medplum_client.create_resource(
            {
                "resourceType": "Patient",
                "name": [{"given": ["IsoAlice"], "family": f"Iso-A-{test_id}"}],
            }
        )
        cleanup.append(("Patient", patient_a["id"]))
        medplum_client.set_accounts(
            f"Patient/{patient_a['id']}",
            f"Organization/{env['org_a']['id']}",
            propagate=True,
        )

        patient_b = medplum_client.create_resource(
            {
                "resourceType": "Patient",
                "name": [{"given": ["IsoBob"], "family": f"Iso-B-{test_id}"}],
            }
        )
        cleanup.append(("Patient", patient_b["id"]))
        medplum_client.set_accounts(
            f"Patient/{patient_b['id']}",
            f"Organization/{env['org_b']['id']}",
            propagate=True,
        )

        assert "PracA" in env["memberships"]
        doctor_a_client = create_scoped_client(env["memberships"]["PracA"]["id"])
        try:
            found_a = _bundle_ids(
                doctor_a_client.search_resources(
                    "Patient", {"family:contains": f"Iso-A-{test_id}"}
                )
            )
            assert patient_a["id"] in found_a

            found_b = _bundle_ids(
                doctor_a_client.search_resources(
                    "Patient", {"family:contains": f"Iso-B-{test_id}"}
                )
            )
            assert patient_b["id"] not in found_b
        finally:
            doctor_a_client.close()

    finally:
        for resource_type, resource_id in reversed(cleanup):
            try:
                medplum_client.delete_resource(resource_type, resource_id)
            except Exception as e:
                print(f"Warning: Failed to delete {resource_type}/{resource_id}: {e}")


def test_obo_auto_compartment_and_admin_multi_org(
    medplum_client, create_scoped_client, test_id
):
    """OBO creates a patient (server auto-assigns compartment), then admin
    enrolls the patient in a second org via set_accounts.

    Validates:
    1. OBO creation auto-assigns meta.accounts from AccessPolicy compartment
    2. Admin can add a second org with set_accounts
    3. OBO user for the second org can then see the patient
    """
    if not medplum_client.project_id:
        pytest.skip("MEDPLUM_PROJECT_ID must be set")

    env = _create_mso_env(medplum_client, test_id, "AutoComp")
    cleanup = list(env["cleanup"])

    try:
        assert "PracA" in env["memberships"]
        assert "PracB" in env["memberships"]

        # Step 1: OBO user A creates a patient — no explicit accounts
        doctor_a_client = create_scoped_client(env["memberships"]["PracA"]["id"])
        try:
            patient = doctor_a_client.create_resource(
                {
                    "resourceType": "Patient",
                    "name": [{"given": ["AutoComp"], "family": f"Test-{test_id}"}],
                }
            )
            cleanup.append(("Patient", patient["id"]))
        finally:
            doctor_a_client.close()

        # Verify server auto-assigned org A's account
        patient_read = medplum_client.read_resource("Patient", patient["id"])
        org_a_ref = f"Organization/{env['org_a']['id']}"
        org_b_ref = f"Organization/{env['org_b']['id']}"
        assert resource_has_account(patient_read, org_a_ref), (
            f"Expected auto-assigned {org_a_ref} in "
            f"{get_resource_accounts(patient_read)}"
        )

        # Step 2: Admin enrolls patient in org B
        medplum_client.set_accounts(f"Patient/{patient['id']}", [org_a_ref, org_b_ref])

        patient_read = medplum_client.read_resource("Patient", patient["id"])
        accounts = get_resource_accounts(patient_read)
        assert org_a_ref in accounts
        assert org_b_ref in accounts

        # Step 3: OBO user B can now see the patient
        doctor_b_client = create_scoped_client(env["memberships"]["PracB"]["id"])
        try:
            found = _bundle_ids(
                doctor_b_client.search_resources(
                    "Patient", {"family:contains": f"Test-{test_id}"}
                )
            )
            assert patient["id"] in found, (
                "Doctor B should see patient after admin enrolled in org B"
            )
        finally:
            doctor_b_client.close()

    finally:
        for resource_type, resource_id in reversed(cleanup):
            try:
                medplum_client.delete_resource(resource_type, resource_id)
            except Exception as e:
                print(f"Warning: Failed to delete {resource_type}/{resource_id}: {e}")
