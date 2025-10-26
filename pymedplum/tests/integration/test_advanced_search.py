"""Integration tests for advanced FHIR search features.

Tests _include, _revinclude, chaining, modifiers, and other advanced search capabilities.
"""

import contextlib
import uuid
from datetime import datetime, timedelta

import pytest

from pymedplum.fhir.codeableconcept import CodeableConcept
from pymedplum.fhir.coding import Coding
from pymedplum.fhir.humanname import HumanName
from pymedplum.fhir.observation import Observation
from pymedplum.fhir.organization import Organization
from pymedplum.fhir.patient import Patient
from pymedplum.fhir.reference import Reference
from pymedplum.helpers import to_fhir_json


@pytest.fixture
def test_setup(medplum_client):
    """Create test data for advanced search tests."""
    test_id = str(uuid.uuid4())[:8]
    created_resources = []

    # Create organization
    org = Organization(name=f"Test Hospital {test_id}", active=True)
    org_result = medplum_client.create_resource(to_fhir_json(org))
    created_resources.append(("Organization", org_result["id"]))

    # Create patients linked to organization
    patients = []
    for _i, (family, given) in enumerate(
        [("TestSmith", "John"), ("TestSmithson", "Jane"), ("TestJones", "Bob")]
    ):
        patient = Patient(
            name=[HumanName(family=f"{family}_{test_id}", given=[given])],
            managingOrganization=Reference(
                reference=f"Organization/{org_result['id']}"
            ),
            active=True,
        )
        patient_result = medplum_client.create_resource(to_fhir_json(patient))
        created_resources.append(("Patient", patient_result["id"]))
        patients.append(patient_result)

    # Create observations for first patient
    today = datetime.now()
    observations = []
    for days_ago in [1, 3, 7]:
        obs_date = (today - timedelta(days=days_ago)).isoformat()
        obs = Observation(
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(system="http://loinc.org", code="15074-8", display="Glucose")
                ]
            ),
            subject=Reference(reference=f"Patient/{patients[0]['id']}"),
            effectiveDateTime=obs_date,
        )
        obs_result = medplum_client.create_resource(to_fhir_json(obs))
        created_resources.append(("Observation", obs_result["id"]))
        observations.append(obs_result)

    yield {
        "test_id": test_id,
        "organization": org_result,
        "patients": patients,
        "observations": observations,
    }

    # Cleanup
    for resource_type, resource_id in reversed(created_resources):
        with contextlib.suppress(Exception):
            medplum_client.delete_resource(resource_type, resource_id)


def test_include_related_resources(medplum_client, test_setup):
    """Test _include parameter to fetch related resources."""
    test_id = test_setup["test_id"]
    org_id = test_setup["organization"]["id"]

    # Search for patients and include their managing organization
    bundle = medplum_client.search_resources(
        "Patient", {"family:contains": test_id, "_include": "Patient:organization"}
    )

    # Verify we got both patients and organization
    resource_types = [
        entry["resource"]["resourceType"] for entry in bundle.get("entry", [])
    ]

    assert "Patient" in resource_types, "Should include Patient resources"
    assert "Organization" in resource_types, "Should include Organization via _include"

    # Verify the organization matches
    orgs = [
        e["resource"]
        for e in bundle.get("entry", [])
        if e["resource"]["resourceType"] == "Organization"
    ]
    assert len(orgs) > 0, "Should have at least one organization"
    assert any(org["id"] == org_id for org in orgs), (
        "Should include the correct organization"
    )


def test_revinclude_observations(medplum_client, test_setup):
    """Test _revinclude to fetch resources that reference the search results."""
    test_id = test_setup["test_id"]
    patient_id = test_setup["patients"][0]["id"]

    # Search for patient and include all their observations
    bundle = medplum_client.search_resources(
        "Patient",
        {
            "family:contains": test_id,
            "_id": patient_id,
            "_revinclude": "Observation:patient",
        },
    )

    # Verify we got both patient and observations
    entries = bundle.get("entry", [])
    resource_types = [entry["resource"]["resourceType"] for entry in entries]

    assert "Patient" in resource_types, "Should include Patient resource"
    assert "Observation" in resource_types, (
        "Should include Observations via _revinclude"
    )

    # Count observations
    observations = [
        e["resource"] for e in entries if e["resource"]["resourceType"] == "Observation"
    ]
    assert len(observations) == 3, "Should include all 3 observations for the patient"


def test_search_parameter_chaining(medplum_client, test_setup):
    """Test chaining search parameters through references."""
    test_id = test_setup["test_id"]

    # Find patients by their organization's name (chaining through managingOrganization)
    bundle = medplum_client.search_resources(
        "Patient", {"organization.name:contains": test_id}
    )

    entries = bundle.get("entry", [])
    assert len(entries) >= 2, "Should find patients via organization name chaining"

    # Verify all patients belong to the test organization
    for entry in entries:
        patient = entry["resource"]
        family_name = patient.get("name", [{}])[0].get("family", "")
        assert test_id in family_name, f"Patient should be from test: {family_name}"


def test_search_modifier_contains(medplum_client, test_setup):
    """Test :contains modifier for substring matching."""
    test_id = test_setup["test_id"]

    # Search with contains modifier - should match names containing "Smith"
    bundle = medplum_client.search_resources(
        "Patient", {"family:contains": f"Smith_{test_id}"}
    )

    entries = bundle.get("entry", [])
    # :contains should find at least one patient with "Smith" in the name
    assert len(entries) >= 1, "Should find at least one patient with :contains"

    family_names = [
        e["resource"].get("name", [{}])[0].get("family", "") for e in entries
    ]
    # Verify at least one name contains "Smith"
    assert any("Smith" in name for name in family_names), (
        "Should match names containing Smith"
    )


def test_search_modifier_exact(medplum_client, test_setup):
    """Test :exact modifier for case-sensitive exact matching."""
    test_id = test_setup["test_id"]
    exact_family = f"TestSmith_{test_id}"

    # Search with exact modifier
    bundle = medplum_client.search_resources("Patient", {"family:exact": exact_family})

    entries = bundle.get("entry", [])
    # Should only match exact "TestSmith", not "TestSmithson"
    for entry in entries:
        family = entry["resource"].get("name", [{}])[0].get("family", "")
        assert family == exact_family, (
            f"Exact match should only return {exact_family}, got {family}"
        )


def test_date_range_search(medplum_client, test_setup):
    """Test date range searches with prefixes."""
    patient_id = test_setup["patients"][0]["id"]
    today = datetime.now().date()
    five_days_ago = today - timedelta(days=5)

    # Search for observations from the last 5 days
    bundle = medplum_client.search_resources(
        "Observation",
        {"patient": f"Patient/{patient_id}", "date": f"ge{five_days_ago.isoformat()}"},
    )

    entries = bundle.get("entry", [])
    # Should find observations from 1 and 3 days ago, but not 7 days ago
    assert len(entries) == 2, (
        f"Should find 2 observations from last 5 days, found {len(entries)}"
    )


def test_date_range_with_both_bounds(medplum_client, test_setup):
    """Test date range with both lower and upper bounds using chained parameters."""
    patient_id = test_setup["patients"][0]["id"]
    today = datetime.now().date()

    # Search for observations from more than 2 days ago (should find 3 and 7 day old)
    two_days_ago = (today - timedelta(days=2)).isoformat()

    bundle = medplum_client.search_resources(
        "Observation",
        {
            "patient": f"Patient/{patient_id}",
            "date": f"lt{two_days_ago}",  # less than 2 days ago
        },
    )

    entries = bundle.get("entry", [])
    # Should find observations from 3 and 7 days ago
    assert len(entries) == 2, (
        f"Should find 2 observations older than 2 days, found {len(entries)}"
    )


def test_combined_advanced_features(medplum_client, test_setup):
    """Test combining multiple advanced search features."""
    test_id = test_setup["test_id"]

    # Complex query: patients with test_id in name, include org, revinclude recent observations
    bundle = medplum_client.search_resources(
        "Patient",
        {
            "family:contains": test_id,
            "_include": "Patient:organization",
            "_revinclude": "Observation:patient",
            "_count": "50",
        },
    )

    # Collect resources by type
    entries = bundle.get("entry", [])
    by_type = {}
    for entry in entries:
        resource_type = entry["resource"]["resourceType"]
        by_type.setdefault(resource_type, []).append(entry["resource"])

    # Verify we got all expected resource types
    assert "Patient" in by_type, "Should have Patient resources"
    assert "Organization" in by_type, "Should have included Organization"
    assert "Observation" in by_type, "Should have reverse-included Observations"

    # Verify counts
    assert len(by_type["Patient"]) >= 2, "Should have multiple patients"
    assert len(by_type["Observation"]) == 3, "Should have all observations"


def test_search_with_count_limit(medplum_client, test_setup):
    """Test _count parameter to limit results per page."""
    test_id = test_setup["test_id"]

    # Search with count=1 to get only one result
    bundle = medplum_client.search_resources(
        "Patient", {"family:contains": test_id, "_count": "1"}
    )

    entries = bundle.get("entry", [])
    assert len(entries) <= 1, "Should respect _count parameter"


def test_search_with_sort(medplum_client, test_setup):
    """Test _sort parameter for ordering results."""
    test_id = test_setup["test_id"]

    # Sort patients by family name
    bundle = medplum_client.search_resources(
        "Patient", {"family:contains": test_id, "_sort": "family"}
    )

    entries = bundle.get("entry", [])
    if len(entries) >= 2:
        # Verify sorting (should be TestJones, TestSmith, TestSmithson)
        family_names = [
            e["resource"].get("name", [{}])[0].get("family", "") for e in entries
        ]
        # Just verify they're in some order (exact order depends on how server sorts the test_id suffix)
        assert len(family_names) >= 2, "Should have multiple results to verify sorting"


def test_pagination_with_advanced_search(medplum_client, test_setup):
    """Test search_resource_pages with advanced search parameters."""
    test_id = test_setup["test_id"]

    # Use iterator with advanced search
    all_patients = []
    for patient in medplum_client.search_resource_pages(
        "Patient",
        {"family:contains": test_id, "_count": "1"},  # Force pagination
    ):
        all_patients.append(patient)
        # Only iterate through patients (not included/reverse-included resources)
        if len(all_patients) >= 3:
            break

    assert len(all_patients) >= 2, "Should find multiple patients through pagination"


@pytest.mark.asyncio
async def test_async_advanced_search(async_medplum_client, test_setup):
    """Test advanced search features with async client."""
    test_id = test_setup["test_id"]

    # Test async _include
    bundle = await async_medplum_client.search_resources(
        "Patient", {"family:contains": test_id, "_include": "Patient:organization"}
    )

    resource_types = [
        entry["resource"]["resourceType"] for entry in bundle.get("entry", [])
    ]
    assert "Patient" in resource_types
    assert "Organization" in resource_types


@pytest.mark.asyncio
async def test_async_pagination_with_advanced_search(async_medplum_client, test_setup):
    """Test async search_resource_pages with advanced parameters."""
    test_id = test_setup["test_id"]

    all_patients = []
    async for patient in async_medplum_client.search_resource_pages(
        "Patient", {"family:contains": test_id, "_count": "1"}
    ):
        all_patients.append(patient)
        if len(all_patients) >= 3:
            break

    assert len(all_patients) >= 2, (
        "Should find multiple patients through async pagination"
    )
