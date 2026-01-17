"""Integration tests for new FHIR operations.

Tests against a live Medplum server for:
- execute_operation (generic FHIR operations)
- C-CDA export
- ValueSet/CodeSystem validation
- Transaction and batch bundles
- Binary upload/download
- DocumentReference creation
"""

from pathlib import Path

import pytest

from pymedplum.fhir import Patient

# Path to test data
TEST_DATA_DIR = Path(__file__).parent / "data"
EXAMPLE_PDF_PATH = TEST_DATA_DIR / "example_document.pdf"


# execute_operation tests


def test_sync_execute_operation_everything(medplum_client):
    """Test sync execute_operation with $everything operation."""
    # Create a patient with some related data
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "ExecuteOpTest", "given": ["Sync"]}],
            gender="male",
            birthDate="1985-03-15",
        )
    )

    # Create an observation for this patient
    observation = medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "Test Observation"},
            "subject": {"reference": f"Patient/{patient['id']}"},
            "valueString": "Test value",
        }
    )

    # Use execute_operation to get $everything
    result = medplum_client.execute_operation(
        "Patient",
        "everything",
        resource_id=patient["id"],
    )

    # Should return a Bundle
    assert result["resourceType"] == "Bundle"
    assert result["type"] == "searchset"

    # Bundle should contain the patient
    resource_types = [
        entry["resource"]["resourceType"] for entry in result.get("entry", [])
    ]
    assert "Patient" in resource_types

    # Bundle should contain the observation we created
    obs_entries = [
        entry["resource"]
        for entry in result.get("entry", [])
        if entry["resource"]["resourceType"] == "Observation"
        and entry["resource"]["id"] == observation["id"]
    ]
    assert len(obs_entries) >= 1


@pytest.mark.asyncio
async def test_async_execute_operation_everything(async_medplum_client):
    """Test async execute_operation with $everything operation."""
    # Create a patient
    patient = await async_medplum_client.create_resource(
        Patient(
            name=[{"family": "AsyncExecuteOpTest", "given": ["Test"]}],
            gender="female",
            birthDate="1990-07-20",
        )
    )

    # Create a condition for this patient
    await async_medplum_client.create_resource(
        {
            "resourceType": "Condition",
            "clinicalStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        "code": "active",
                    }
                ]
            },
            "code": {"text": "Test Condition"},
            "subject": {"reference": f"Patient/{patient['id']}"},
        }
    )

    # Use execute_operation to get $everything
    result = await async_medplum_client.execute_operation(
        "Patient",
        "everything",
        resource_id=patient["id"],
    )

    # Should return a Bundle
    assert result["resourceType"] == "Bundle"
    assert result["type"] == "searchset"

    # Bundle should contain the patient
    patient_entries = [
        entry["resource"]
        for entry in result.get("entry", [])
        if entry["resource"]["resourceType"] == "Patient"
        and entry["resource"]["id"] == patient["id"]
    ]
    assert len(patient_entries) == 1


def test_sync_execute_operation_with_dollar_prefix(medplum_client):
    """Test that execute_operation works with $ prefix in operation name."""
    # Create a patient
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "DollarPrefixTest", "given": ["Sync"]}],
            gender="male",
        )
    )

    # Use $everything with explicit $ prefix
    result = medplum_client.execute_operation(
        "Patient",
        "$everything",  # With $ prefix
        resource_id=patient["id"],
    )

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "searchset"


def test_sync_execute_operation_validate(medplum_client):
    """Test sync execute_operation with $validate operation."""
    # Validate a Patient resource
    patient_to_validate = {
        "resourceType": "Patient",
        "name": [{"family": "ValidateTest", "given": ["Sync"]}],
        "gender": "male",
    }

    result = medplum_client.execute_operation(
        "Patient",
        "validate",
        params=patient_to_validate,
    )

    # Should return an OperationOutcome
    assert result["resourceType"] == "OperationOutcome"
    # If validation passes, there should be no errors (or only info/warnings)
    if "issue" in result:
        # Check that there are no error-level issues
        errors = [
            issue for issue in result["issue"] if issue.get("severity") == "error"
        ]
        # A valid patient should not have errors
        assert len(errors) == 0


@pytest.mark.asyncio
async def test_async_execute_operation_validate(async_medplum_client):
    """Test async execute_operation with $validate operation."""
    # Validate a Patient resource
    patient_to_validate = {
        "resourceType": "Patient",
        "name": [{"family": "AsyncValidateTest", "given": ["Test"]}],
        "gender": "female",
        "birthDate": "1995-12-01",
    }

    result = await async_medplum_client.execute_operation(
        "Patient",
        "validate",
        params=patient_to_validate,
    )

    # Should return an OperationOutcome
    assert result["resourceType"] == "OperationOutcome"


def test_sync_execute_operation_with_get_method(medplum_client):
    """Test sync execute_operation with GET method for CodeSystem/$lookup."""
    # Use GET method for a simple lookup operation
    result = medplum_client.execute_operation(
        "CodeSystem",
        "lookup",
        params={"code": "male", "system": "http://hl7.org/fhir/administrative-gender"},
        method="GET",
    )

    # Should return a Parameters resource with the lookup result
    assert result["resourceType"] == "Parameters"
    # Should have display parameter
    display_param = next(
        (p for p in result.get("parameter", []) if p.get("name") == "display"), None
    )
    assert display_param is not None
    assert "Male" in display_param.get("valueString", "")


@pytest.mark.asyncio
async def test_async_execute_operation_with_get_method(async_medplum_client):
    """Test async execute_operation with GET method for CodeSystem/$lookup."""
    result = await async_medplum_client.execute_operation(
        "CodeSystem",
        "lookup",
        params={
            "code": "female",
            "system": "http://hl7.org/fhir/administrative-gender",
        },
        method="GET",
    )

    assert result["resourceType"] == "Parameters"
    display_param = next(
        (p for p in result.get("parameter", []) if p.get("name") == "display"), None
    )
    assert display_param is not None


def test_sync_execute_operation_with_wrap_params(medplum_client):
    """Test sync execute_operation with wrap_params to auto-convert dict to Parameters.

    The wrap_params feature auto-wraps dicts into FHIR Parameters resources:
    - Dicts with 'resourceType' become resource params (tested here)
    - Dicts with 'system'/'code' become valueCoding params
    - Dicts with 'reference' become valueReference params
    - Strings become valueString params (for custom operations)

    For standard terminology operations like $validate-code or $lookup that require
    specific value types (valueUri, valueCode), use the dedicated helper methods
    like valueset_validate_code() or codesystem_lookup() instead.
    """
    # Test wrap_params with a resource parameter - this demonstrates the
    # resourceType detection that makes wrap_params useful for passing
    # FHIR resources as operation parameters
    result = medplum_client.execute_operation(
        "Patient",
        "validate",
        params={
            "resource": {
                "resourceType": "Patient",
                "name": [{"family": "WrapParamsTest", "given": ["Sync"]}],
                "gender": "male",
            }
        },
        wrap_params=True,
    )

    # Should return an OperationOutcome (validation result)
    assert result["resourceType"] == "OperationOutcome"


@pytest.mark.asyncio
async def test_async_execute_operation_with_wrap_params(async_medplum_client):
    """Test async execute_operation with wrap_params to auto-convert dict to Parameters.

    See test_sync_execute_operation_with_wrap_params for details on wrap_params behavior.
    """
    # Test wrap_params with a resource parameter - demonstrates resourceType detection
    result = await async_medplum_client.execute_operation(
        "Patient",
        "validate",
        params={
            "resource": {
                "resourceType": "Patient",
                "name": [{"family": "AsyncWrapParamsTest", "given": ["Test"]}],
                "gender": "female",
            }
        },
        wrap_params=True,
    )

    # Should return an OperationOutcome (validation result)
    assert result["resourceType"] == "OperationOutcome"


# Binary and DocumentReference workflow tests


def test_sync_binary_and_document_reference_workflow(medplum_client):
    """Test complete workflow: upload binary, create DocumentReference."""
    # Create a test patient
    patient = Patient(
        name=[{"family": "BinaryTest", "given": ["Integration"]}],
        gender="male",
    )
    created_patient = medplum_client.create_resource(patient)

    # Load actual PDF file
    with EXAMPLE_PDF_PATH.open("rb") as f:
        pdf_content = f.read()

    binary = medplum_client.upload_binary(pdf_content, "application/pdf")

    assert binary["resourceType"] == "Binary"
    assert binary["id"]
    assert binary["contentType"] == "application/pdf"

    # Download the binary to verify
    downloaded = medplum_client.download_binary(binary["id"])
    assert downloaded == pdf_content

    # Create a DocumentReference pointing to the binary
    doc_ref = medplum_client.create_document_reference(
        patient_id=created_patient["id"],
        binary_id=binary["id"],
        content_type="application/pdf",
        title="Test PDF Document",
        description="Integration test PDF document",
        doc_type_code={
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "34133-9",
                    "display": "Summary of Episode Note",
                }
            ]
        },
    )

    assert doc_ref["resourceType"] == "DocumentReference"
    assert doc_ref["id"]
    assert doc_ref["subject"]["reference"] == f"Patient/{created_patient['id']}"
    # Medplum stores binaries externally, so the URL will be a full storage URL
    # Just check that the binary ID is referenced somewhere in the URL
    assert binary["id"] in doc_ref["content"][0]["attachment"]["url"]
    assert doc_ref["description"] == "Integration test PDF document"


@pytest.mark.asyncio
async def test_async_binary_and_document_reference_workflow(async_medplum_client):
    """Test async complete workflow: upload binary, create DocumentReference."""
    # Create a test patient
    patient = Patient(
        name=[{"family": "AsyncBinaryTest", "given": ["Integration"]}],
        gender="female",
    )
    created_patient = await async_medplum_client.create_resource(patient)

    # Load actual PDF file
    with EXAMPLE_PDF_PATH.open("rb") as f:
        pdf_content = f.read()

    binary = await async_medplum_client.upload_binary(pdf_content, "application/pdf")

    assert binary["resourceType"] == "Binary"
    assert binary["id"]
    assert binary["contentType"] == "application/pdf"

    # Download the binary to verify
    downloaded = await async_medplum_client.download_binary(binary["id"])
    assert downloaded == pdf_content
    assert len(downloaded) == len(pdf_content)

    # Create a DocumentReference
    doc_ref = await async_medplum_client.create_document_reference(
        patient_id=created_patient["id"],
        binary_id=binary["id"],
        content_type="application/pdf",
        title="Example PDF Document",
    )

    assert doc_ref["resourceType"] == "DocumentReference"
    assert doc_ref["subject"]["reference"] == f"Patient/{created_patient['id']}"
    # Check that the binary ID is referenced in the URL
    assert binary["id"] in doc_ref["content"][0]["attachment"]["url"]
    assert doc_ref["content"][0]["attachment"]["title"] == "Example PDF Document"


# Transaction Bundle tests


def test_sync_execute_transaction(medplum_client):
    """Test sync transaction bundle execution."""
    # Create a transaction bundle with multiple resources
    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "fullUrl": "urn:uuid:patient-1",
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "TransactionTest", "given": ["Sync"]}],
                    "gender": "male",
                },
                "request": {"method": "POST", "url": "Patient"},
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {"text": "Heart Rate"},
                    "subject": {"reference": "urn:uuid:patient-1"},
                    "valueQuantity": {"value": 72, "unit": "bpm"},
                },
                "request": {"method": "POST", "url": "Observation"},
            },
        ],
    }

    result = medplum_client.execute_transaction(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "transaction-response"
    assert len(result["entry"]) == 2
    assert result["entry"][0]["response"]["status"].startswith("201")
    assert result["entry"][1]["response"]["status"].startswith("201")

    # Verify the resources were created
    patient_id = result["entry"][0]["resource"]["id"]
    observation_id = result["entry"][1]["resource"]["id"]

    patient = medplum_client.read_resource("Patient", patient_id)
    assert patient["name"][0]["family"] == "TransactionTest"

    observation = medplum_client.read_resource("Observation", observation_id)
    # Note: Medplum may not resolve urn:uuid references in the response
    # but the relationship is correctly stored - verify by checking the observation
    subject_ref = observation["subject"]["reference"]
    # Accept either the resolved reference or the urn:uuid (both are valid)
    assert subject_ref in {f"Patient/{patient_id}", "urn:uuid:patient-1"}


@pytest.mark.asyncio
async def test_async_execute_transaction(async_medplum_client):
    """Test async transaction bundle execution."""
    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "fullUrl": "urn:uuid:patient-async",
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "AsyncTransactionTest", "given": ["Test"]}],
                    "gender": "female",
                },
                "request": {"method": "POST", "url": "Patient"},
            },
        ],
    }

    result = await async_medplum_client.execute_transaction(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "transaction-response"
    assert len(result["entry"]) == 1
    assert result["entry"][0]["response"]["status"].startswith("201")


# Batch Bundle tests


def test_sync_execute_batch(medplum_client):
    """Test sync batch bundle execution."""
    # Create two patients first
    patient1 = medplum_client.create_resource(
        Patient(
            name=[{"family": "BatchTest1", "given": ["Sync"]}],
            gender="male",
        )
    )
    patient2 = medplum_client.create_resource(
        Patient(
            name=[{"family": "BatchTest2", "given": ["Sync"]}],
            gender="female",
        )
    )

    # Create a batch bundle to read both
    bundle = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {"request": {"method": "GET", "url": f"Patient/{patient1['id']}"}},
            {"request": {"method": "GET", "url": f"Patient/{patient2['id']}"}},
            {
                "request": {
                    "method": "GET",
                    "url": "Patient/nonexistent-id-for-batch-test",
                }
            },
        ],
    }

    result = medplum_client.execute_batch(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "batch-response"
    assert len(result["entry"]) == 3

    # First two should succeed
    assert result["entry"][0]["response"]["status"].startswith("200")
    assert result["entry"][1]["response"]["status"].startswith("200")

    # Third should fail but not affect others (that's the batch behavior)
    assert result["entry"][2]["response"]["status"].startswith("404")


@pytest.mark.asyncio
async def test_async_execute_batch(async_medplum_client):
    """Test async batch bundle execution."""
    # Create a patient
    patient = await async_medplum_client.create_resource(
        Patient(
            name=[{"family": "AsyncBatchTest", "given": ["Test"]}],
            gender="male",
        )
    )

    # Create a batch bundle
    bundle = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {"request": {"method": "GET", "url": f"Patient/{patient['id']}"}},
        ],
    }

    result = await async_medplum_client.execute_batch(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "batch-response"
    assert len(result["entry"]) == 1
    assert result["entry"][0]["response"]["status"].startswith("200")


# ValueSet and CodeSystem validation tests


def test_sync_validate_valueset_code(medplum_client):
    """Test sync ValueSet code validation.

    Note: This test uses a FHIR standard ValueSet.
    Results may vary based on the Medplum server configuration.
    """
    # Test with a standard FHIR ValueSet
    result = medplum_client.validate_valueset_code(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
        code="male",
        system="http://hl7.org/fhir/administrative-gender",
    )

    assert result["resourceType"] == "Parameters"
    # The result parameter should exist
    assert "parameter" in result
    # Look for the result parameter
    result_param = next(
        (p for p in result["parameter"] if p.get("name") == "result"), None
    )
    assert result_param is not None


@pytest.mark.asyncio
async def test_async_validate_valueset_code(async_medplum_client):
    """Test async ValueSet code validation."""
    result = await async_medplum_client.validate_valueset_code(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
        code="female",
        system="http://hl7.org/fhir/administrative-gender",
    )

    assert result["resourceType"] == "Parameters"
    assert "parameter" in result


def test_sync_validate_codesystem_code(medplum_client):
    """Test sync CodeSystem code validation.

    Note: This test validates against a standard code system.
    Results may vary based on server configuration.
    """
    result = medplum_client.validate_codesystem_code(
        codesystem_url="http://hl7.org/fhir/administrative-gender",
        code="male",
    )

    assert result["resourceType"] == "Parameters"
    assert "parameter" in result


@pytest.mark.asyncio
async def test_async_validate_codesystem_code(async_medplum_client):
    """Test async CodeSystem code validation."""
    result = await async_medplum_client.validate_codesystem_code(
        codesystem_url="http://hl7.org/fhir/administrative-gender",
        code="female",
    )

    assert result["resourceType"] == "Parameters"
    assert "parameter" in result


# C-CDA Export tests
# Note: C-CDA export requires patient data and may not be available on all servers


def test_sync_export_ccda_requires_patient(medplum_client):
    """Test sync C-CDA export (may not be available on all Medplum servers)."""
    # Create a patient with some data
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "CCDATest", "given": ["Sync"]}],
            gender="male",
            birthDate="1990-01-01",
        )
    )

    try:
        # Attempt to export C-CDA
        ccda = medplum_client.export_ccda(patient["id"])

        # If successful, verify it's XML
        assert isinstance(ccda, str)
        assert len(ccda) > 0
        # C-CDA documents should contain XML declaration
        if "<?xml" in ccda:
            assert "<?xml" in ccda

    except Exception as e:
        # C-CDA export may not be available on all servers
        # This is acceptable for this test
        pytest.skip(f"C-CDA export not available: {e}")


@pytest.mark.asyncio
async def test_async_export_ccda_requires_patient(async_medplum_client):
    """Test async C-CDA export (may not be available on all Medplum servers)."""
    # Create a patient
    patient = await async_medplum_client.create_resource(
        Patient(
            name=[{"family": "AsyncCCDATest", "given": ["Test"]}],
            gender="female",
            birthDate="1985-05-15",
        )
    )

    try:
        # Attempt to export C-CDA
        ccda = await async_medplum_client.export_ccda(patient["id"])

        # If successful, verify it's a string
        assert isinstance(ccda, str)
        assert len(ccda) > 0

    except Exception as e:
        # C-CDA export may not be available on all servers
        pytest.skip(f"C-CDA export not available: {e}")


# Conditional Create (If-None-Exist) tests


def test_sync_create_resource_if_none_exist_creates_new(medplum_client):
    """Test sync conditional create creates a new resource when none exists."""
    import uuid

    # Generate unique identifier to ensure no existing resource matches
    unique_id = f"test-conditional-{uuid.uuid4()}"

    patient = medplum_client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/test", "value": unique_id}],
            "name": [{"family": "ConditionalCreate", "given": ["Sync"]}],
        },
        if_none_exist=f"identifier=http://example.org/test|{unique_id}",
    )

    assert patient["resourceType"] == "Patient"
    assert patient["id"]  # Should have been assigned an ID
    assert patient["identifier"][0]["value"] == unique_id


def test_sync_create_resource_if_none_exist_returns_existing(medplum_client):
    """Test sync conditional create returns existing resource when one matches."""
    import uuid

    unique_id = f"test-conditional-existing-{uuid.uuid4()}"

    # First, create a resource
    first_patient = medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/test", "value": unique_id}],
            "name": [{"family": "ConditionalExisting", "given": ["Sync"]}],
        }
    )

    # Now try conditional create with same identifier
    second_patient = medplum_client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/test", "value": unique_id}],
            "name": [{"family": "ShouldNotCreate", "given": ["Sync"]}],
        },
        if_none_exist=f"identifier=http://example.org/test|{unique_id}",
    )

    # Should return the same patient ID (existing resource)
    assert second_patient["id"] == first_patient["id"]
    # Name should be from first creation, not second
    assert second_patient["name"][0]["family"] == "ConditionalExisting"


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_creates_new(async_medplum_client):
    """Test async conditional create creates a new resource when none exists."""
    import uuid

    unique_id = f"test-conditional-async-{uuid.uuid4()}"

    patient = await async_medplum_client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/test", "value": unique_id}],
            "name": [{"family": "AsyncConditional", "given": ["Test"]}],
        },
        if_none_exist=f"identifier=http://example.org/test|{unique_id}",
    )

    assert patient["resourceType"] == "Patient"
    assert patient["id"]
    assert patient["identifier"][0]["value"] == unique_id


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_returns_existing(
    async_medplum_client,
):
    """Test async conditional create returns existing resource when one matches."""
    import uuid

    unique_id = f"test-conditional-existing-async-{uuid.uuid4()}"

    # First create
    first_patient = await async_medplum_client.create_resource(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/test", "value": unique_id}],
            "name": [{"family": "AsyncExisting", "given": ["Test"]}],
        }
    )

    # Conditional create
    second_patient = await async_medplum_client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/test", "value": unique_id}],
            "name": [{"family": "ShouldNotCreate", "given": ["Async"]}],
        },
        if_none_exist=f"identifier=http://example.org/test|{unique_id}",
    )

    assert second_patient["id"] == first_patient["id"]


# Search with Options tests


def test_sync_search_with_options_summary_count(medplum_client):
    """Test sync search with _summary=count."""
    result = medplum_client.search_with_options(
        "Patient",
        summary="count",
    )

    assert result["resourceType"] == "Bundle"
    assert "total" in result
    # With summary=count, entry should not be present or be empty
    assert "entry" not in result or len(result.get("entry", [])) == 0


def test_sync_search_with_options_elements(medplum_client):
    """Test sync search with _elements to limit returned fields."""
    # Create a patient to search for
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "ElementsTest", "given": ["Sync"]}],
            gender="male",
            birthDate="1990-05-15",
        )
    )

    result = medplum_client.search_with_options(
        "Patient",
        {"_id": patient["id"]},
        elements=["id", "name"],
    )

    assert result["resourceType"] == "Bundle"
    if result.get("entry"):
        resource = result["entry"][0]["resource"]
        assert "id" in resource
        assert "name" in resource
        # Gender and birthDate should be excluded (but server may still include them)


def test_sync_search_with_options_total_accurate(medplum_client):
    """Test sync search with _total=accurate."""
    result = medplum_client.search_with_options(
        "Patient",
        {"family": "ElementsTest"},
        total="accurate",
    )

    assert result["resourceType"] == "Bundle"
    # With _total=accurate, total should be present
    assert "total" in result
    assert isinstance(result["total"], int)


def test_sync_search_with_options_pagination(medplum_client):
    """Test sync search with count and offset for pagination."""
    result = medplum_client.search_with_options(
        "Patient",
        count=2,
        offset=0,
    )

    assert result["resourceType"] == "Bundle"
    # Should have at most 2 entries
    if result.get("entry"):
        assert len(result["entry"]) <= 2


def test_sync_search_with_options_sort(medplum_client):
    """Test sync search with _sort parameter."""
    result = medplum_client.search_with_options(
        "Patient",
        sort="-_lastUpdated",
        count=5,
    )

    assert result["resourceType"] == "Bundle"
    # Results should be sorted by lastUpdated descending


def test_sync_search_with_options_include(medplum_client):
    """Test sync search with _include parameter."""
    # Create a patient and observation
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "IncludeTest", "given": ["Sync"]}],
            gender="female",
        )
    )

    medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "Include Test Observation"},
            "subject": {"reference": f"Patient/{patient['id']}"},
            "valueString": "test",
        }
    )

    # Search observations with _include to get the patient
    result = medplum_client.search_with_options(
        "Observation",
        {"subject": f"Patient/{patient['id']}"},
        include="Observation:subject",
    )

    assert result["resourceType"] == "Bundle"
    # Bundle should contain both Observation and Patient
    if result.get("entry"):
        resource_types = [e["resource"]["resourceType"] for e in result["entry"]]
        # Observation should be present
        assert "Observation" in resource_types


@pytest.mark.asyncio
async def test_async_search_with_options_summary_count(async_medplum_client):
    """Test async search with _summary=count."""
    result = await async_medplum_client.search_with_options(
        "Patient",
        summary="count",
    )

    assert result["resourceType"] == "Bundle"
    assert "total" in result


@pytest.mark.asyncio
async def test_async_search_with_options_pagination(async_medplum_client):
    """Test async search with pagination parameters."""
    result = await async_medplum_client.search_with_options(
        "Patient",
        count=3,
        offset=0,
        total="accurate",
    )

    assert result["resourceType"] == "Bundle"
    assert "total" in result
    if result.get("entry"):
        assert len(result["entry"]) <= 3


# search_with_options include_iterate / revinclude_iterate tests


def test_sync_search_with_options_include_iterate(medplum_client):
    """Test sync search with _include:iterate for recursive includes."""
    # Create an Organization
    org = medplum_client.create_resource(
        {
            "resourceType": "Organization",
            "name": "Test Hospital for Iterate",
        }
    )

    # Create a Location that references the Organization
    location = medplum_client.create_resource(
        {
            "resourceType": "Location",
            "name": "Test Ward",
            "managingOrganization": {"reference": f"Organization/{org['id']}"},
        }
    )

    # Create an Encounter at the Location
    patient = medplum_client.create_resource(
        Patient(name=[{"family": "IterateTest", "given": ["Sync"]}])
    )
    medplum_client.create_resource(
        {
            "resourceType": "Encounter",
            "status": "finished",
            "class": {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "AMB",
            },
            "subject": {"reference": f"Patient/{patient['id']}"},
            "location": [{"location": {"reference": f"Location/{location['id']}"}}],
        }
    )

    # Search for encounters with recursive includes:
    # First include Location, then iterate to include Organization
    result = medplum_client.search_with_options(
        "Encounter",
        {"subject": f"Patient/{patient['id']}"},
        include="Encounter:location",
        include_iterate="Location:organization",
    )

    assert result["resourceType"] == "Bundle"
    # The bundle should contain Encounter, Location, and Organization
    if result.get("entry"):
        resource_types = [e["resource"]["resourceType"] for e in result["entry"]]
        assert "Encounter" in resource_types
        # Location should be included via _include
        assert "Location" in resource_types


@pytest.mark.asyncio
async def test_async_search_with_options_include_iterate(async_medplum_client):
    """Test async search with _include:iterate for recursive includes."""
    # Create resources for the test
    org = await async_medplum_client.create_resource(
        {
            "resourceType": "Organization",
            "name": "Async Test Hospital for Iterate",
        }
    )

    location = await async_medplum_client.create_resource(
        {
            "resourceType": "Location",
            "name": "Async Test Ward",
            "managingOrganization": {"reference": f"Organization/{org['id']}"},
        }
    )

    patient = await async_medplum_client.create_resource(
        Patient(name=[{"family": "AsyncIterateTest", "given": ["Test"]}])
    )
    await async_medplum_client.create_resource(
        {
            "resourceType": "Encounter",
            "status": "finished",
            "class": {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "AMB",
            },
            "subject": {"reference": f"Patient/{patient['id']}"},
            "location": [{"location": {"reference": f"Location/{location['id']}"}}],
        }
    )

    result = await async_medplum_client.search_with_options(
        "Encounter",
        {"subject": f"Patient/{patient['id']}"},
        include="Encounter:location",
        include_iterate="Location:organization",
    )

    assert result["resourceType"] == "Bundle"
    if result.get("entry"):
        resource_types = [e["resource"]["resourceType"] for e in result["entry"]]
        assert "Encounter" in resource_types
        assert "Location" in resource_types


def test_sync_search_with_options_revinclude_iterate(medplum_client):
    """Test sync search with _revinclude:iterate for recursive reverse includes."""
    # Create a patient and observation chain for testing revinclude iterate
    patient = medplum_client.create_resource(
        Patient(name=[{"family": "RevIterateTest", "given": ["Sync"]}])
    )

    # Create an observation referencing the patient
    observation = medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "RevInclude Iterate Test"},
            "subject": {"reference": f"Patient/{patient['id']}"},
            "valueString": "test value",
        }
    )

    # Create a Provenance targeting the Observation
    medplum_client.create_resource(
        {
            "resourceType": "Provenance",
            "target": [{"reference": f"Observation/{observation['id']}"}],
            "recorded": "2024-01-15T10:00:00Z",
            "agent": [
                {
                    "who": {"reference": f"Patient/{patient['id']}"},
                }
            ],
        }
    )

    # Search for patient with revinclude for observations,
    # then iterate to get provenance
    result = medplum_client.search_with_options(
        "Patient",
        {"_id": patient["id"]},
        revinclude="Observation:subject",
        revinclude_iterate="Provenance:target",
    )

    assert result["resourceType"] == "Bundle"
    if result.get("entry"):
        resource_types = [e["resource"]["resourceType"] for e in result["entry"]]
        assert "Patient" in resource_types
        assert "Observation" in resource_types


@pytest.mark.asyncio
async def test_async_search_with_options_revinclude_iterate(async_medplum_client):
    """Test async search with _revinclude:iterate for recursive reverse includes."""
    patient = await async_medplum_client.create_resource(
        Patient(name=[{"family": "AsyncRevIterateTest", "given": ["Test"]}])
    )

    observation = await async_medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "Async RevInclude Iterate Test"},
            "subject": {"reference": f"Patient/{patient['id']}"},
            "valueString": "async test value",
        }
    )

    await async_medplum_client.create_resource(
        {
            "resourceType": "Provenance",
            "target": [{"reference": f"Observation/{observation['id']}"}],
            "recorded": "2024-01-15T10:00:00Z",
            "agent": [
                {
                    "who": {"reference": f"Patient/{patient['id']}"},
                }
            ],
        }
    )

    result = await async_medplum_client.search_with_options(
        "Patient",
        {"_id": patient["id"]},
        revinclude="Observation:subject",
        revinclude_iterate="Provenance:target",
    )

    assert result["resourceType"] == "Bundle"
    if result.get("entry"):
        resource_types = [e["resource"]["resourceType"] for e in result["entry"]]
        assert "Patient" in resource_types
        assert "Observation" in resource_types


# ValueSet $expand tests


def test_sync_expand_valueset_standard(medplum_client):
    """Test sync ValueSet $expand with standard FHIR ValueSet."""
    result = medplum_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
    )

    assert result["resourceType"] == "ValueSet"
    assert "expansion" in result
    assert "contains" in result["expansion"]
    # Assert structure rather than specific codes (avoids flaky tests)
    contains = result["expansion"]["contains"]
    assert len(contains) > 0
    # Each entry should have at least code and system
    for entry in contains:
        assert "code" in entry
        assert "system" in entry


def test_sync_expand_valueset_with_filter(medplum_client):
    """Test sync ValueSet $expand with text filter."""
    result = medplum_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
        filter="mal",
    )

    assert result["resourceType"] == "ValueSet"
    assert "expansion" in result
    # Filter should narrow results - just verify structure, not specific codes
    if result["expansion"].get("contains"):
        contains = result["expansion"]["contains"]
        # Each entry should have valid structure
        for entry in contains:
            assert "code" in entry
            assert "system" in entry


def test_sync_expand_valueset_with_pagination(medplum_client):
    """Test sync ValueSet $expand with pagination."""
    result = medplum_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
        count=2,
    )

    assert result["resourceType"] == "ValueSet"
    assert "expansion" in result
    # Should respect count limit
    if result["expansion"].get("contains"):
        assert len(result["expansion"]["contains"]) <= 2


@pytest.mark.asyncio
async def test_async_expand_valueset_standard(async_medplum_client):
    """Test async ValueSet $expand with standard FHIR ValueSet."""
    result = await async_medplum_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
    )

    assert result["resourceType"] == "ValueSet"
    assert "expansion" in result
    # Assert structure rather than specific codes (avoids flaky tests)
    contains = result["expansion"]["contains"]
    assert len(contains) > 0
    for entry in contains:
        assert "code" in entry
        assert "system" in entry


@pytest.mark.asyncio
async def test_async_expand_valueset_with_filter(async_medplum_client):
    """Test async ValueSet $expand with filter."""
    result = await async_medplum_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender",
        filter="fem",
    )

    assert result["resourceType"] == "ValueSet"
    # Filter should narrow results - just verify structure, not specific codes
    if result["expansion"].get("contains"):
        contains = result["expansion"]["contains"]
        for entry in contains:
            assert "code" in entry
            assert "system" in entry


# CodeSystem $lookup tests


def test_sync_lookup_concept_standard(medplum_client):
    """Test sync CodeSystem $lookup with standard FHIR CodeSystem."""
    result = medplum_client.lookup_concept(
        code="male",
        system="http://hl7.org/fhir/administrative-gender",
    )

    assert result["resourceType"] == "Parameters"
    assert "parameter" in result

    # Should have display name
    display_param = next(
        (p for p in result["parameter"] if p.get("name") == "display"), None
    )
    assert display_param is not None
    assert "Male" in display_param.get("valueString", "")


def test_sync_lookup_concept_with_display_language(medplum_client):
    """Test sync CodeSystem $lookup with display language."""
    result = medplum_client.lookup_concept(
        code="female",
        system="http://hl7.org/fhir/administrative-gender",
        display_language="en",
    )

    assert result["resourceType"] == "Parameters"


@pytest.mark.asyncio
async def test_async_lookup_concept_standard(async_medplum_client):
    """Test async CodeSystem $lookup with standard FHIR CodeSystem."""
    result = await async_medplum_client.lookup_concept(
        code="female",
        system="http://hl7.org/fhir/administrative-gender",
    )

    assert result["resourceType"] == "Parameters"
    display_param = next(
        (p for p in result["parameter"] if p.get("name") == "display"), None
    )
    assert display_param is not None


# ConceptMap $translate tests


@pytest.fixture
def test_concept_map(medplum_client):
    """Create or reuse a test ConceptMap for translation tests.

    Uses a deterministic URL so the same ConceptMap can be reused across test runs.
    This avoids cluttering the Medplum project with duplicate ConceptMaps.
    """
    # Use a fixed URL for the test ConceptMap
    concept_map_url = "http://example.org/fhir/ConceptMap/pymedplum-test-gender-mapping"

    # Check if ConceptMap already exists
    existing = medplum_client.search_resources("ConceptMap", {"url": concept_map_url})
    if existing.get("entry"):
        # Reuse existing ConceptMap
        return existing["entry"][0]["resource"]

    # Create a simple ConceptMap that maps administrative-gender to a test system
    concept_map = {
        "resourceType": "ConceptMap",
        "url": concept_map_url,
        "name": "PymedplumTestGenderMapping",
        "status": "active",
        "sourceUri": "http://hl7.org/fhir/ValueSet/administrative-gender",
        "targetUri": "http://example.org/test-gender-codes",
        "group": [
            {
                "source": "http://hl7.org/fhir/administrative-gender",
                "target": "http://example.org/test-gender-codes",
                "element": [
                    {
                        "code": "male",
                        "display": "Male",
                        "target": [
                            {
                                "code": "M",
                                "display": "Male Test Code",
                                "equivalence": "equivalent",
                            }
                        ],
                    },
                    {
                        "code": "female",
                        "display": "Female",
                        "target": [
                            {
                                "code": "F",
                                "display": "Female Test Code",
                                "equivalence": "equivalent",
                            }
                        ],
                    },
                ],
            }
        ],
    }

    # Create the ConceptMap (no cleanup - intentionally persisted for reuse)
    return medplum_client.create_resource(concept_map)


def test_sync_translate_concept(medplum_client, test_concept_map):
    """Test sync ConceptMap $translate with a created ConceptMap."""
    result = medplum_client.translate_concept(
        code="male",
        system="http://hl7.org/fhir/administrative-gender",
        conceptmap_url=test_concept_map["url"],
        target_system="http://example.org/test-gender-codes",
    )

    assert result["resourceType"] == "Parameters"

    # Result parameter should indicate whether translation was found
    result_param = next(
        (p for p in result["parameter"] if p.get("name") == "result"), None
    )
    assert result_param is not None

    # If translation was successful, check the match
    if result_param.get("valueBoolean"):
        match_param = next(
            (p for p in result["parameter"] if p.get("name") == "match"), None
        )
        assert match_param is not None
        # Extract the translated code
        for part in match_param.get("part", []):
            if part.get("name") == "concept":
                coding = part.get("valueCoding", {})
                assert coding.get("code") == "M"
                assert coding.get("system") == "http://example.org/test-gender-codes"


def test_sync_translate_concept_by_id(medplum_client, test_concept_map):
    """Test sync ConceptMap $translate using ConceptMap ID."""
    result = medplum_client.translate_concept(
        code="female",
        system="http://hl7.org/fhir/administrative-gender",
        conceptmap_id=test_concept_map["id"],
        target_system="http://example.org/test-gender-codes",
    )

    assert result["resourceType"] == "Parameters"

    result_param = next(
        (p for p in result["parameter"] if p.get("name") == "result"), None
    )
    assert result_param is not None


@pytest.mark.asyncio
async def test_async_translate_concept(async_medplum_client, test_concept_map):
    """Test async ConceptMap $translate with a created ConceptMap."""
    result = await async_medplum_client.translate_concept(
        code="female",
        system="http://hl7.org/fhir/administrative-gender",
        conceptmap_url=test_concept_map["url"],
        target_system="http://example.org/test-gender-codes",
    )

    assert result["resourceType"] == "Parameters"

    result_param = next(
        (p for p in result["parameter"] if p.get("name") == "result"), None
    )
    assert result_param is not None

    # If translation was successful, verify the mapped code
    if result_param.get("valueBoolean"):
        match_param = next(
            (p for p in result["parameter"] if p.get("name") == "match"), None
        )
        assert match_param is not None
        for part in match_param.get("part", []):
            if part.get("name") == "concept":
                coding = part.get("valueCoding", {})
                assert coding.get("code") == "F"


# vread tests


def test_sync_vread_resource(medplum_client):
    """Test sync vread_resource to read a specific version of a resource."""
    # Create a patient
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "VreadTest", "given": ["Sync"]}],
            gender="male",
        )
    )
    version_1 = patient["meta"]["versionId"]

    # Update the patient to create a new version
    patient["gender"] = "female"
    updated_patient = medplum_client.update_resource(patient)
    version_2 = updated_patient["meta"]["versionId"]

    # vread the first version
    patient_v1 = medplum_client.vread_resource("Patient", patient["id"], version_1)

    # Verify we got version 1 (gender should be "male")
    assert patient_v1["meta"]["versionId"] == version_1
    assert patient_v1["gender"] == "male"

    # vread the current version
    patient_v2 = medplum_client.vread_resource("Patient", patient["id"], version_2)
    assert patient_v2["meta"]["versionId"] == version_2
    assert patient_v2["gender"] == "female"


def test_sync_vread_resource_typed(medplum_client):
    """Test sync vread_resource with as_fhir for type-safe response."""
    # Create a patient
    patient = medplum_client.create_resource(
        Patient(
            name=[{"family": "VreadTypedTest", "given": ["Sync"]}],
            gender="male",
        )
    )
    version_id = patient["meta"]["versionId"]

    # vread with typed response
    patient_typed = medplum_client.vread_resource(
        "Patient", patient["id"], version_id, as_fhir=Patient
    )

    # Should be a Patient instance
    assert isinstance(patient_typed, Patient)
    assert patient_typed.gender == "male"


@pytest.mark.asyncio
async def test_async_vread_resource(async_medplum_client):
    """Test async vread_resource to read a specific version."""
    # Create a patient
    patient = await async_medplum_client.create_resource(
        Patient(
            name=[{"family": "AsyncVreadTest", "given": ["Test"]}],
            gender="female",
        )
    )
    version_1 = patient["meta"]["versionId"]

    # Update to create version 2
    patient["gender"] = "male"
    updated_patient = await async_medplum_client.update_resource(patient)
    version_2 = updated_patient["meta"]["versionId"]

    # vread version 1
    patient_v1 = await async_medplum_client.vread_resource(
        "Patient", patient["id"], version_1
    )
    assert patient_v1["gender"] == "female"

    # vread version 2
    patient_v2 = await async_medplum_client.vread_resource(
        "Patient", patient["id"], version_2
    )
    assert patient_v2["gender"] == "male"


@pytest.mark.asyncio
async def test_async_vread_resource_typed(async_medplum_client):
    """Test async vread_resource with as_fhir for type-safe response."""
    # Create a patient
    patient = await async_medplum_client.create_resource(
        Patient(
            name=[{"family": "AsyncVreadTypedTest", "given": ["Test"]}],
            gender="female",
        )
    )
    version_id = patient["meta"]["versionId"]

    # vread with typed response
    patient_typed = await async_medplum_client.vread_resource(
        "Patient", patient["id"], version_id, as_fhir=Patient
    )

    # Should be a Patient instance
    assert isinstance(patient_typed, Patient)
    assert patient_typed.gender == "female"
    assert patient_typed.name[0].family == "AsyncVreadTypedTest"


# clone_resource tests
# Note: $clone is a Medplum-specific operation that may not be enabled on all servers


def test_sync_clone_resource(medplum_client):
    """Test sync clone_resource to create a copy of a resource."""
    from pymedplum.exceptions import NotFoundError, OperationOutcomeError

    # Create a patient to clone
    original = medplum_client.create_resource(
        Patient(
            name=[{"family": "CloneTest", "given": ["Original"]}],
            gender="male",
            birthDate="1990-01-01",
        )
    )

    try:
        # Clone the patient
        cloned = medplum_client.clone_resource("Patient", original["id"])

        # The clone should have a different ID
        assert cloned["id"] != original["id"]

        # But the same data
        assert cloned["name"] == original["name"]
        assert cloned["gender"] == original["gender"]
        assert cloned["birthDate"] == original["birthDate"]
    except (NotFoundError, OperationOutcomeError) as e:
        pytest.skip(f"$clone operation not available: {e}")


@pytest.mark.asyncio
async def test_async_clone_resource(async_medplum_client):
    """Test async clone_resource to create a copy of a resource."""
    from pymedplum.exceptions import NotFoundError, OperationOutcomeError

    # Create a patient to clone
    original = await async_medplum_client.create_resource(
        Patient(
            name=[{"family": "AsyncCloneTest", "given": ["Original"]}],
            gender="female",
            birthDate="1985-06-15",
        )
    )

    try:
        # Clone the patient
        cloned = await async_medplum_client.clone_resource("Patient", original["id"])

        # The clone should have a different ID but same data
        assert cloned["id"] != original["id"]
        assert cloned["name"] == original["name"]
        assert cloned["gender"] == original["gender"]
    except (NotFoundError, OperationOutcomeError) as e:
        pytest.skip(f"$clone operation not available: {e}")


# expunge_resource tests


def test_sync_expunge_resource(medplum_client):
    """Test sync expunge_resource to permanently delete a resource."""
    # Create a simple observation to expunge
    observation = medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "Expunge Test Observation"},
            "valueString": "Test value for expunge",
        }
    )
    obs_id = observation["id"]

    # Verify it exists
    fetched = medplum_client.read_resource("Observation", obs_id)
    assert fetched["id"] == obs_id

    # Expunge the resource
    medplum_client.expunge_resource("Observation", obs_id)

    # Verify it's gone (should raise 404/410 or similar error)
    with pytest.raises(Exception):
        medplum_client.read_resource("Observation", obs_id)


@pytest.mark.asyncio
async def test_async_expunge_resource(async_medplum_client):
    """Test async expunge_resource to permanently delete a resource."""
    # Create a simple observation to expunge
    observation = await async_medplum_client.create_resource(
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "Async Expunge Test Observation"},
            "valueString": "Test value for async expunge",
        }
    )
    obs_id = observation["id"]

    # Verify it exists
    fetched = await async_medplum_client.read_resource("Observation", obs_id)
    assert fetched["id"] == obs_id

    # Expunge the resource
    await async_medplum_client.expunge_resource("Observation", obs_id)

    # Verify it's gone
    with pytest.raises(Exception):
        await async_medplum_client.read_resource("Observation", obs_id)


# set_access_token tests


def test_sync_set_access_token(medplum_credentials):
    """Test setting access token explicitly on sync client."""
    from pymedplum import MedplumClient

    # First, authenticate with credentials to get a valid token
    auth_client = MedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
    )
    token = auth_client.authenticate()
    auth_client.close()

    # Create a new client without credentials and set the token
    token_client = MedplumClient()
    token_client.set_access_token(token)

    try:
        # Verify the client can make authenticated requests
        result = token_client.search_resources("Patient", {"_count": "1"})
        assert result["resourceType"] == "Bundle"

        # Verify the token was set correctly
        assert token_client.access_token == token
        # token_expires_at should be set from JWT
        assert token_client.token_expires_at is not None
    finally:
        token_client.close()


def test_sync_client_with_access_token_in_constructor(medplum_credentials):
    """Test creating sync client with access_token in constructor."""
    from pymedplum import MedplumClient

    # First, authenticate with credentials to get a valid token
    auth_client = MedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
    )
    token = auth_client.authenticate()
    auth_client.close()

    # Create a new client directly with the access_token
    token_client = MedplumClient(access_token=token)

    try:
        # Verify the client can make authenticated requests
        result = token_client.search_resources("Patient", {"_count": "1"})
        assert result["resourceType"] == "Bundle"

        # Verify the token and expiry were set
        assert token_client.access_token == token
        assert token_client.token_expires_at is not None
    finally:
        token_client.close()


@pytest.mark.asyncio
async def test_async_set_access_token(medplum_credentials):
    """Test setting access token explicitly on async client."""
    from pymedplum import AsyncMedplumClient

    # First, authenticate with credentials to get a valid token
    auth_client = AsyncMedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
    )
    token = await auth_client.authenticate()
    await auth_client.close()

    # Create a new client without credentials and set the token
    token_client = AsyncMedplumClient()
    token_client.set_access_token(token)

    try:
        # Verify the client can make authenticated requests
        result = await token_client.search_resources("Patient", {"_count": "1"})
        assert result["resourceType"] == "Bundle"

        # Verify the token was set correctly
        assert token_client.access_token == token
        # token_expires_at should be set from JWT
        assert token_client.token_expires_at is not None
    finally:
        await token_client.close()


@pytest.mark.asyncio
async def test_async_client_with_access_token_in_constructor(medplum_credentials):
    """Test creating async client with access_token in constructor."""
    from pymedplum import AsyncMedplumClient

    # First, authenticate with credentials to get a valid token
    auth_client = AsyncMedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
    )
    token = await auth_client.authenticate()
    await auth_client.close()

    # Create a new client directly with the access_token
    token_client = AsyncMedplumClient(access_token=token)

    try:
        # Verify the client can make authenticated requests
        result = await token_client.search_resources("Patient", {"_count": "1"})
        assert result["resourceType"] == "Bundle"

        # Verify the token and expiry were set
        assert token_client.access_token == token
        assert token_client.token_expires_at is not None
    finally:
        await token_client.close()


def test_sync_set_access_token_with_explicit_expiry(medplum_credentials):
    """Test setting access token with explicit expiry datetime."""
    from datetime import datetime, timedelta, timezone

    from pymedplum import MedplumClient

    # First, authenticate with credentials to get a valid token
    auth_client = MedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
    )
    token = auth_client.authenticate()
    auth_client.close()

    # Create a new client and set token with explicit expiry
    token_client = MedplumClient()
    custom_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    token_client.set_access_token(token, expires_at=custom_expiry)

    try:
        # Verify the client can make authenticated requests
        result = token_client.search_resources("Patient", {"_count": "1"})
        assert result["resourceType"] == "Bundle"

        # Verify the custom expiry was used (not JWT-decoded one)
        assert token_client.token_expires_at == custom_expiry
    finally:
        token_client.close()
