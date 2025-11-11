"""Comprehensive API coverage tests for both sync and async clients.

Tests every public method on MedplumClient and AsyncMedplumClient to ensure:
- All methods work correctly against the live API
- Sync and async implementations have feature parity
- Edge cases and error handling work as expected
"""

import pytest

from pymedplum.fhir import Patient

# ============================================================================
# SYNC CLIENT TESTS
# ============================================================================


def test_sync_authenticate(medplum_client):
    """Test sync client authentication."""
    token = medplum_client.authenticate()
    assert token
    assert isinstance(token, str)
    assert len(token) > 0


def test_sync_create_resource(medplum_client):
    """Test sync client create_resource method."""
    patient = Patient(
        name=[{"family": "SyncTestCreate", "given": ["API", "Coverage"]}],
        gender="male",
    )

    result = medplum_client.create_resource(patient)
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["family"] == "SyncTestCreate"
    assert "id" in result


def test_sync_read_resource(medplum_client):
    """Test sync client read_resource method."""
    # Create a patient first
    patient = Patient(
        name=[{"family": "SyncTestRead", "given": ["Test"]}],
        gender="female",
    )
    created = medplum_client.create_resource(patient)

    # Read it back
    result = medplum_client.read_resource("Patient", created["id"])
    assert result["id"] == created["id"]
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["family"] == "SyncTestRead"


def test_sync_update_resource(medplum_client):
    """Test sync client update_resource method."""
    # Create a patient
    patient = Patient(
        name=[{"family": "SyncTestUpdate", "given": ["Original"]}],
        gender="male",
    )
    created = medplum_client.create_resource(patient)

    # Update it
    created["name"][0]["given"] = ["Updated"]
    updated = medplum_client.update_resource(created)

    assert updated["id"] == created["id"]
    assert updated["name"][0]["given"] == ["Updated"]


def test_sync_patch_resource(medplum_client):
    """Test sync client patch_resource method (JSON Patch)."""
    # Create a patient
    patient = Patient(
        name=[{"family": "SyncTestPatch", "given": ["Before"]}],
        gender="male",
    )
    created = medplum_client.create_resource(patient)

    # Patch it
    patches = [
        {"op": "replace", "path": "/name/0/given/0", "value": "After"},
    ]
    patched = medplum_client.patch_resource("Patient", created["id"], patches)

    assert patched["id"] == created["id"]
    assert patched["name"][0]["given"] == ["After"]


def test_sync_create_resource_with_as_fhir(medplum_client):
    """Test sync client create_resource with as_fhir parameter."""
    patient_data = {
        "resourceType": "Patient",
        "name": [{"family": "SyncTypedCreate", "given": ["Typed"]}],
        "gender": "female",
    }

    # Create with type-safe response
    result = medplum_client.create_resource(patient_data, as_fhir=Patient)

    # Verify we got a Pydantic model back
    assert isinstance(result, Patient)
    assert result.resource_type == "Patient"
    assert result.name[0].family == "SyncTypedCreate"
    assert result.id is not None


def test_sync_update_resource_with_as_fhir(medplum_client):
    """Test sync client update_resource with as_fhir parameter."""
    # Create a patient
    patient = Patient(
        name=[{"family": "SyncTypedUpdate", "given": ["Original"]}],
        gender="male",
    )
    created = medplum_client.create_resource(patient)

    # Update with type-safe response
    created["name"][0]["given"] = ["Modified"]
    updated = medplum_client.update_resource(created, as_fhir=Patient)

    # Verify we got a Pydantic model back
    assert isinstance(updated, Patient)
    assert updated.name[0].given == ["Modified"]
    assert updated.id == created["id"]


def test_sync_patch_resource_with_as_fhir(medplum_client):
    """Test sync client patch_resource with as_fhir parameter."""
    # Create a patient
    patient = Patient(
        name=[{"family": "SyncTypedPatch", "given": ["Before"]}],
        gender="female",
        active=True,
    )
    created = medplum_client.create_resource(patient)

    # Patch with type-safe response
    patches = [
        {"op": "replace", "path": "/active", "value": False},
    ]
    patched = medplum_client.patch_resource(
        "Patient", created["id"], patches, as_fhir=Patient
    )

    # Verify we got a Pydantic model back
    assert isinstance(patched, Patient)
    assert patched.active is False
    assert patched.id == created["id"]


def test_sync_search_resources(medplum_client):
    """Test sync client search_resources method."""
    import uuid

    # Create a patient with a truly unique identifier
    unique_id = str(uuid.uuid4())
    patient = Patient(
        name=[{"family": f"SyncSearchTest-{unique_id}", "given": ["Coverage"]}],
        gender="female",
    )
    created = medplum_client.create_resource(patient)

    # Search for the patient using the unique family name
    results = medplum_client.search_resources(
        "Patient",
        {"family": f"SyncSearchTest-{unique_id}"},
    )

    assert results["resourceType"] == "Bundle"
    assert results["type"] == "searchset"
    assert len(results["entry"]) > 0
    assert any(e["resource"]["id"] == created["id"] for e in results["entry"])


def test_sync_search_one(medplum_client):
    """Test sync client search_one method."""
    import uuid

    # Create a patient with a unique identifier
    unique_id = str(uuid.uuid4())
    patient = Patient(
        name=[{"family": f"SyncSearchOne-{unique_id}", "given": ["Unique"]}],
        gender="male",
    )
    created = medplum_client.create_resource(patient)

    # Search for it using the unique family name
    result = medplum_client.search_one(
        "Patient", {"family": f"SyncSearchOne-{unique_id}"}
    )

    assert result is not None
    assert result["resourceType"] == "Patient"
    assert result["id"] == created["id"]


def test_sync_search_resource_pages(medplum_client):
    """Test sync client search_resource_pages iterator."""
    # Create multiple patients
    for i in range(3):
        patient = Patient(
            name=[{"family": "SyncPagination", "given": [f"Test{i}"]}],
            gender="male",
        )
        medplum_client.create_resource(patient)

    # Iterate through resources (search_resource_pages yields individual resources, not Bundles)
    resources = []
    for resource in medplum_client.search_resource_pages(
        "Patient",
        {"family": "SyncPagination"},
    ):
        resources.append(resource)
        # Limit to prevent infinite loop in case of pagination issues
        if len(resources) >= 5:
            break

    assert len(resources) >= 3
    assert all(isinstance(r, dict) for r in resources)
    assert all(r["resourceType"] == "Patient" for r in resources)


def test_sync_execute_batch(medplum_client):
    """Test sync client execute_batch method."""
    # Create a batch request
    batch = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "POST",
                    "url": "Patient",
                },
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "SyncBatch", "given": ["Test1"]}],
                    "gender": "male",
                },
            },
            {
                "request": {
                    "method": "POST",
                    "url": "Patient",
                },
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "SyncBatch", "given": ["Test2"]}],
                    "gender": "female",
                },
            },
        ],
    }

    result = medplum_client.execute_batch(batch)
    assert result["resourceType"] == "Bundle"
    assert result["type"] == "batch-response"
    assert len(result["entry"]) == 2
    assert all(e["response"]["status"].startswith("201") for e in result["entry"])


def test_sync_post(medplum_client):
    """Test sync client generic post method."""
    # Post to create a patient using the correct FHIR API path
    patient_data = {
        "resourceType": "Patient",
        "name": [{"family": "SyncPost", "given": ["Test"]}],
        "gender": "male",
    }

    result = medplum_client.post("fhir/R4/Patient", patient_data)
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["family"] == "SyncPost"
    assert "id" in result


def test_sync_on_behalf_of_context_manager(medplum_client, medplum_membership):
    """Test sync client on_behalf_of context manager."""
    # Create a patient outside the context
    patient1 = Patient(
        name=[{"family": "OutsideContext", "given": ["Test"]}],
        gender="male",
    )
    created1 = medplum_client.create_resource(patient1)

    # Create a patient inside the context
    with medplum_client.on_behalf_of(medplum_membership):
        patient2 = Patient(
            name=[{"family": "InsideContext", "given": ["Test"]}],
            gender="female",
        )
        created2 = medplum_client.create_resource(patient2)

        # Verify the context is active (check the internal stack)
        assert len(medplum_client._obo_stack) == 1
        # The stack stores normalized references with "ProjectMembership/" prefix
        assert (
            medplum_client._obo_stack[-1] == f"ProjectMembership/{medplum_membership}"
        )

    # Verify the context is cleared after exiting
    assert len(medplum_client._obo_stack) == 0

    # Both patients should exist
    assert created1["id"]
    assert created2["id"]


# ============================================================================
# ASYNC CLIENT TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_async_authenticate(async_medplum_client):
    """Test async client authentication."""
    token = await async_medplum_client.authenticate()
    assert token
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_async_create_resource(async_medplum_client):
    """Test async client create_resource method."""
    patient = Patient(
        name=[{"family": "AsyncTestCreate", "given": ["API", "Coverage"]}],
        gender="male",
    )

    result = await async_medplum_client.create_resource(patient)
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["family"] == "AsyncTestCreate"
    assert "id" in result


@pytest.mark.asyncio
async def test_async_read_resource(async_medplum_client):
    """Test async client read_resource method."""
    # Create a patient first
    patient = Patient(
        name=[{"family": "AsyncTestRead", "given": ["Test"]}],
        gender="female",
    )
    created = await async_medplum_client.create_resource(patient)

    # Read it back
    result = await async_medplum_client.read_resource("Patient", created["id"])
    assert result["id"] == created["id"]
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["family"] == "AsyncTestRead"


@pytest.mark.asyncio
async def test_async_update_resource(async_medplum_client):
    """Test async client update_resource method."""
    # Create a patient
    patient = Patient(
        name=[{"family": "AsyncTestUpdate", "given": ["Original"]}],
        gender="male",
    )
    created = await async_medplum_client.create_resource(patient)

    # Update it
    created["name"][0]["given"] = ["Updated"]
    updated = await async_medplum_client.update_resource(created)

    assert updated["id"] == created["id"]
    assert updated["name"][0]["given"] == ["Updated"]


@pytest.mark.asyncio
async def test_async_patch_resource(async_medplum_client):
    """Test async client patch_resource method (JSON Patch)."""
    # Create a patient
    patient = Patient(
        name=[{"family": "AsyncTestPatch", "given": ["Before"]}],
        gender="male",
    )
    created = await async_medplum_client.create_resource(patient)

    # Patch it
    patches = [
        {"op": "replace", "path": "/name/0/given/0", "value": "After"},
    ]
    patched = await async_medplum_client.patch_resource(
        "Patient", created["id"], patches
    )

    assert patched["id"] == created["id"]
    assert patched["name"][0]["given"] == ["After"]


@pytest.mark.asyncio
async def test_async_create_resource_with_as_fhir(async_medplum_client):
    """Test async client create_resource with as_fhir parameter."""
    patient_data = {
        "resourceType": "Patient",
        "name": [{"family": "AsyncTypedCreate", "given": ["Typed"]}],
        "gender": "female",
    }

    # Create with type-safe response
    result = await async_medplum_client.create_resource(patient_data, as_fhir=Patient)

    # Verify we got a Pydantic model back
    assert isinstance(result, Patient)
    assert result.resource_type == "Patient"
    assert result.name[0].family == "AsyncTypedCreate"
    assert result.id is not None


@pytest.mark.asyncio
async def test_async_update_resource_with_as_fhir(async_medplum_client):
    """Test async client update_resource with as_fhir parameter."""
    # Create a patient
    patient = Patient(
        name=[{"family": "AsyncTypedUpdate", "given": ["Original"]}],
        gender="male",
    )
    created = await async_medplum_client.create_resource(patient)

    # Update with type-safe response
    created["name"][0]["given"] = ["Modified"]
    updated = await async_medplum_client.update_resource(created, as_fhir=Patient)

    # Verify we got a Pydantic model back
    assert isinstance(updated, Patient)
    assert updated.name[0].given == ["Modified"]
    assert updated.id == created["id"]


@pytest.mark.asyncio
async def test_async_patch_resource_with_as_fhir(async_medplum_client):
    """Test async client patch_resource with as_fhir parameter."""
    # Create a patient
    patient = Patient(
        name=[{"family": "AsyncTypedPatch", "given": ["Before"]}],
        gender="female",
        active=True,
    )
    created = await async_medplum_client.create_resource(patient)

    # Patch with type-safe response
    patches = [
        {"op": "replace", "path": "/active", "value": False},
    ]
    patched = await async_medplum_client.patch_resource(
        "Patient", created["id"], patches, as_fhir=Patient
    )

    # Verify we got a Pydantic model back
    assert isinstance(patched, Patient)
    assert patched.active is False
    assert patched.id == created["id"]


@pytest.mark.asyncio
async def test_async_search_resources(async_medplum_client):
    """Test async client search_resources method."""
    import asyncio
    import uuid

    # Create a patient with unique name
    unique_id = str(uuid.uuid4())
    patient = Patient(
        name=[{"family": f"AsyncSearchTest-{unique_id}", "given": ["Coverage"]}],
        gender="female",
    )
    created = await async_medplum_client.create_resource(patient)

    # Small delay to allow indexing
    await asyncio.sleep(0.5)

    # Search for it using the unique family name
    results = await async_medplum_client.search_resources(
        "Patient",
        {"family": f"AsyncSearchTest-{unique_id}"},
    )

    assert results["resourceType"] == "Bundle"
    assert results["type"] == "searchset"
    assert len(results["entry"]) > 0
    assert any(e["resource"]["id"] == created["id"] for e in results["entry"])


@pytest.mark.asyncio
async def test_async_search_one(async_medplum_client):
    """Test async client search_one method."""
    import uuid

    # Create a patient with a unique identifier
    unique_id = str(uuid.uuid4())
    patient = Patient(
        name=[{"family": f"AsyncSearchOne-{unique_id}", "given": ["Unique"]}],
        gender="male",
    )
    created = await async_medplum_client.create_resource(patient)

    # Search for it using the unique family name
    result = await async_medplum_client.search_one(
        "Patient", {"family": f"AsyncSearchOne-{unique_id}"}
    )

    assert result is not None
    assert result["resourceType"] == "Patient"
    assert result["id"] == created["id"]


@pytest.mark.asyncio
async def test_async_search_resource_pages(async_medplum_client):
    """Test async client search_resource_pages async iterator."""
    # Create multiple patients
    for i in range(3):
        patient = Patient(
            name=[{"family": "AsyncPagination", "given": [f"Test{i}"]}],
            gender="male",
        )
        await async_medplum_client.create_resource(patient)

    # Iterate through resources (search_resource_pages yields individual resources, not Bundles)
    resources = []
    async for resource in async_medplum_client.search_resource_pages(
        "Patient",
        {"family": "AsyncPagination"},
    ):
        resources.append(resource)
        # Limit to prevent issues
        if len(resources) >= 5:
            break

    assert len(resources) >= 3
    assert all(isinstance(r, dict) for r in resources)
    assert all(r["resourceType"] == "Patient" for r in resources)


@pytest.mark.asyncio
async def test_async_execute_batch(async_medplum_client):
    """Test async client execute_batch method."""
    # Create a batch request
    batch = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "POST",
                    "url": "Patient",
                },
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "AsyncBatch", "given": ["Test1"]}],
                    "gender": "male",
                },
            },
            {
                "request": {
                    "method": "POST",
                    "url": "Patient",
                },
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "AsyncBatch", "given": ["Test2"]}],
                    "gender": "female",
                },
            },
        ],
    }

    result = await async_medplum_client.execute_batch(batch)
    assert result["resourceType"] == "Bundle"
    assert result["type"] == "batch-response"
    assert len(result["entry"]) == 2
    assert all(e["response"]["status"].startswith("201") for e in result["entry"])


@pytest.mark.asyncio
async def test_async_post(async_medplum_client):
    """Test async client generic post method."""
    # Post to create a patient using the correct FHIR API path
    patient_data = {
        "resourceType": "Patient",
        "name": [{"family": "AsyncPost", "given": ["Test"]}],
        "gender": "male",
    }

    result = await async_medplum_client.post("fhir/R4/Patient", patient_data)
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["family"] == "AsyncPost"
    assert "id" in result


# ============================================================================
# SYNC/ASYNC FEATURE PARITY TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_sync_async_create_parity(medplum_client, async_medplum_client):
    """Verify sync and async create_resource produce equivalent results."""
    # Create via sync
    sync_patient = Patient(
        name=[{"family": "ParityTest", "given": ["Sync"]}],
        gender="male",
    )
    sync_result = medplum_client.create_resource(sync_patient)

    # Create via async
    async_patient = Patient(
        name=[{"family": "ParityTest", "given": ["Async"]}],
        gender="female",
    )
    async_result = await async_medplum_client.create_resource(async_patient)

    # Both should have same structure
    assert sync_result["resourceType"] == async_result["resourceType"]
    assert "id" in sync_result
    assert "id" in async_result
    assert "meta" in sync_result
    assert "meta" in async_result


@pytest.mark.asyncio
async def test_sync_async_search_parity(medplum_client, async_medplum_client):
    """Verify sync and async search_resources produce equivalent results."""
    # Create a test patient
    patient = Patient(
        name=[{"family": "SearchParity", "given": ["Test"]}],
        gender="male",
    )
    medplum_client.create_resource(patient)

    # Search via sync
    sync_results = medplum_client.search_resources(
        "Patient",
        {"family": "SearchParity"},
    )

    # Search via async
    async_results = await async_medplum_client.search_resources(
        "Patient",
        {"family": "SearchParity"},
    )

    # Both should return bundles with same structure
    assert sync_results["resourceType"] == async_results["resourceType"] == "Bundle"
    assert sync_results["type"] == async_results["type"] == "searchset"
    assert len(sync_results["entry"]) > 0
    assert len(async_results["entry"]) > 0
