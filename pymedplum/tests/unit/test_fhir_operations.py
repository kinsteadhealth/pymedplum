"""Unit tests for FHIR operations (C-CDA, validation, bundles, binary).

Tests the sync client implementation with mocked HTTP responses.
"""

import httpx
import pytest
from respx import MockRouter

from pymedplum.client import MedplumClient


@pytest.fixture
def client():
    """Create a MedplumClient with access token for testing."""
    return MedplumClient(
        base_url="https://api.medplum.com/",
        access_token="test-token",
    )


# C-CDA Export Tests


def test_export_ccda_success(client: MedplumClient, respx_mock: MockRouter):
    """Test successful C-CDA export."""
    ccda_xml = """<?xml version="1.0"?>
    <ClinicalDocument xmlns="urn:hl7-org:v3">
        <patient>Test Patient</patient>
    </ClinicalDocument>"""

    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/patient-123/$ccda-export"
    ).mock(return_value=httpx.Response(200, text=ccda_xml))

    result = client.export_ccda("patient-123")

    assert result == ccda_xml
    assert "ClinicalDocument" in result


def test_export_ccda_not_found(client: MedplumClient, respx_mock: MockRouter):
    """Test C-CDA export with non-existent patient."""
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/nonexistent/$ccda-export"
    ).mock(
        return_value=httpx.Response(
            404,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "not-found",
                        "details": {"text": "Patient not found"},
                    }
                ],
            },
        )
    )

    with pytest.raises(Exception):  # Should raise NotFoundError or similar
        client.export_ccda("nonexistent")


# ValueSet Validation Tests


def test_validate_valueset_code_with_url_and_coding(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test ValueSet validation with URL and coding."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ValueSet/$validate-code").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "result", "valueBoolean": True},
                    {"name": "display", "valueString": "Severe"},
                ],
            },
        )
    )

    result = client.validate_valueset_code(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-severity",
        coding={"system": "http://snomed.info/sct", "code": "255604002"},
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueBoolean"] is True
    assert result["parameter"][1]["valueString"] == "Severe"


def test_validate_valueset_code_with_id_and_code_system(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test ValueSet validation with instance ID and code+system."""
    respx_mock.post(
        "https://api.medplum.com/fhir/R4/ValueSet/my-valueset/$validate-code"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": False}],
            },
        )
    )

    result = client.validate_valueset_code(
        valueset_id="my-valueset",
        code="12345",
        system="http://example.com/codesystem",
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueBoolean"] is False


def test_validate_valueset_code_with_codeable_concept(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test ValueSet validation with CodeableConcept."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ValueSet/$validate-code").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": True}],
            },
        )
    )

    result = client.validate_valueset_code(
        valueset_url="http://hl7.org/fhir/ValueSet/test",
        codeable_concept={
            "coding": [{"system": "http://snomed.info/sct", "code": "12345"}]
        },
    )

    assert result["parameter"][0]["valueBoolean"] is True


# CodeSystem Validation Tests


def test_validate_codesystem_code_with_url_and_code(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test CodeSystem validation with URL and code."""
    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$validate-code").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "result", "valueBoolean": True},
                    {"name": "display", "valueString": "Active"},
                ],
            },
        )
    )

    result = client.validate_codesystem_code(
        codesystem_url="http://snomed.info/sct", code="255604002"
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueBoolean"] is True


def test_validate_codesystem_code_with_version(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test CodeSystem validation with specific version."""
    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$validate-code").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": True}],
            },
        )
    )

    result = client.validate_codesystem_code(
        codesystem_url="http://snomed.info/sct",
        code="12345",
        version="2021-03",
    )

    assert result["parameter"][0]["valueBoolean"] is True


# Transaction Bundle Tests


def test_execute_transaction_bundle_success(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test successful transaction bundle execution."""
    respx_mock.post("https://api.medplum.com/fhir/R4").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "transaction-response",
                "entry": [
                    {
                        "response": {
                            "status": "201 Created",
                            "location": "Patient/123/_history/1",
                        },
                        "resource": {
                            "resourceType": "Patient",
                            "id": "123",
                        },
                    }
                ],
            },
        )
    )

    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "fullUrl": "urn:uuid:patient-temp",
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "Smith", "given": ["John"]}],
                },
                "request": {"method": "POST", "url": "Patient"},
            }
        ],
    }

    result = client.execute_transaction(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "transaction-response"
    assert result["entry"][0]["response"]["status"] == "201 Created"


def test_execute_transaction_auto_sets_type(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that transaction type is automatically set."""
    respx_mock.post("https://api.medplum.com/fhir/R4").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "transaction-response",
                "entry": [],
            },
        )
    )

    # Bundle without type should get type="transaction" automatically
    bundle = {"resourceType": "Bundle", "entry": []}

    result = client.execute_transaction(bundle)

    assert result["type"] == "transaction-response"


# Batch Bundle Tests


def test_execute_batch_bundle_success(client: MedplumClient, respx_mock: MockRouter):
    """Test successful batch bundle execution."""
    respx_mock.post("https://api.medplum.com/fhir/R4/").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "batch-response",
                "entry": [
                    {
                        "response": {"status": "200 OK"},
                        "resource": {"resourceType": "Patient", "id": "123"},
                    },
                    {
                        "response": {"status": "404 Not Found"},
                        "resource": {
                            "resourceType": "OperationOutcome",
                            "issue": [{"severity": "error", "code": "not-found"}],
                        },
                    },
                ],
            },
        )
    )

    bundle = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {"request": {"method": "GET", "url": "Patient/123"}},
            {"request": {"method": "GET", "url": "Patient/nonexistent"}},
        ],
    }

    result = client.execute_batch(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "batch-response"
    assert len(result["entry"]) == 2
    assert result["entry"][0]["response"]["status"] == "200 OK"
    assert result["entry"][1]["response"]["status"] == "404 Not Found"


# Binary Operations Tests


def test_upload_binary(client: MedplumClient, respx_mock: MockRouter):
    """Test binary content upload."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Binary").mock(
        return_value=httpx.Response(
            201,
            json={
                "resourceType": "Binary",
                "id": "binary-123",
                "contentType": "application/pdf",
            },
        )
    )

    pdf_content = b"%PDF-1.4 test content"
    result = client.upload_binary(pdf_content, "application/pdf")

    assert result["resourceType"] == "Binary"
    assert result["id"] == "binary-123"
    assert result["contentType"] == "application/pdf"


def test_download_binary(client: MedplumClient, respx_mock: MockRouter):
    """Test binary content download."""

    pdf_content = b"%PDF-1.4 test content"

    # Mock the read_resource call that download_binary makes
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/binary-123").mock(
        return_value=httpx.Response(
            200,
            content=pdf_content,
            headers={"Content-Type": "application/pdf"},
        )
    )

    result = client.download_binary("binary-123")

    assert result == pdf_content
    assert isinstance(result, bytes)


def test_download_binary_not_found(client: MedplumClient, respx_mock: MockRouter):
    """Test download of non-existent binary."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/nonexistent").mock(
        return_value=httpx.Response(
            404,
            json={
                "resourceType": "OperationOutcome",
                "issue": [{"severity": "error", "code": "not-found"}],
            },
        )
    )

    with pytest.raises(Exception):
        client.download_binary("nonexistent")


# DocumentReference Tests


def test_create_document_reference(client: MedplumClient, respx_mock: MockRouter):
    """Test creating a DocumentReference."""
    respx_mock.post("https://api.medplum.com/fhir/R4/DocumentReference").mock(
        return_value=httpx.Response(
            201,
            json={
                "resourceType": "DocumentReference",
                "id": "doc-ref-123",
                "status": "current",
                "subject": {"reference": "Patient/patient-123"},
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/xml",
                            "url": "Binary/binary-456",
                            "title": "Test Document",
                        }
                    }
                ],
            },
        )
    )

    result = client.create_document_reference(
        patient_id="patient-123",
        binary_id="binary-456",
        content_type="application/xml",
        title="Test Document",
    )

    assert result["resourceType"] == "DocumentReference"
    assert result["id"] == "doc-ref-123"
    assert result["subject"]["reference"] == "Patient/patient-123"
    assert result["content"][0]["attachment"]["url"] == "Binary/binary-456"


def test_create_document_reference_with_optional_fields(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test creating DocumentReference with optional fields."""
    respx_mock.post("https://api.medplum.com/fhir/R4/DocumentReference").mock(
        return_value=httpx.Response(
            201,
            json={
                "resourceType": "DocumentReference",
                "id": "doc-ref-456",
                "status": "current",
                "subject": {"reference": "Patient/patient-123"},
                "description": "C-CDA document",
                "type": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "34133-9",
                            "display": "Summary of Episode Note",
                        }
                    ]
                },
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/xml",
                            "url": "Binary/binary-789",
                            "title": "C-CDA Document",
                        }
                    }
                ],
            },
        )
    )

    result = client.create_document_reference(
        patient_id="patient-123",
        binary_id="binary-789",
        content_type="application/xml",
        title="C-CDA Document",
        description="C-CDA document",
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

    assert result["description"] == "C-CDA document"
    assert result["type"]["coding"][0]["code"] == "34133-9"


# Execute Operation Tests


def test_execute_operation_type_level(client: MedplumClient, respx_mock: MockRouter):
    """Test type-level FHIR operation execution."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient/$match").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [
                    {
                        "resource": {"resourceType": "Patient", "id": "123"},
                        "search": {"score": 0.95},
                    }
                ],
            },
        )
    )

    result = client.execute_operation(
        "Patient",
        "match",
        params={
            "resourceType": "Parameters",
            "parameter": [
                {
                    "name": "resource",
                    "resource": {
                        "resourceType": "Patient",
                        "name": [{"family": "Doe"}],
                    },
                }
            ],
        },
    )

    assert result["resourceType"] == "Bundle"
    assert len(result["entry"]) == 1


def test_execute_operation_instance_level(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test instance-level FHIR operation execution."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient/123/$everything").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [
                    {"resource": {"resourceType": "Patient", "id": "123"}},
                    {"resource": {"resourceType": "Observation", "id": "obs-1"}},
                ],
            },
        )
    )

    result = client.execute_operation("Patient", "everything", resource_id="123")

    assert result["resourceType"] == "Bundle"
    assert len(result["entry"]) == 2


def test_execute_operation_custom_with_headers(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test custom FHIR operation with custom headers."""
    respx_mock.post(
        "https://api.medplum.com/fhir/R4/MedicationRequest/med-123/$calculate-dose"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "dose", "valueQuantity": {"value": 500}}],
            },
        )
    )

    result = client.execute_operation(
        "MedicationRequest",
        "calculate-dose",
        resource_id="med-123",
        params={"weight": 70, "unit": "kg"},
        headers={"X-Custom-Header": "test-value"},
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueQuantity"]["value"] == 500


def test_execute_operation_allows_dollar_prefix(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that operation names with $ prefix are accepted."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient/$match").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    # Should work with or without the $ prefix
    result = client.execute_operation("Patient", "$match", params={})

    assert result["resourceType"] == "Bundle"


def test_execute_bot_uses_execute_operation(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that execute_bot internally uses execute_operation."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Bot/bot-123/$execute").mock(
        return_value=httpx.Response(
            200,
            json={"message": "Bot executed successfully"},
        )
    )

    result = client.execute_bot(
        bot_id="bot-123",
        input_data={"resourceType": "Patient", "id": "patient-123"},
    )

    assert result["message"] == "Bot executed successfully"


# Conditional Create Tests


def test_create_resource_if_none_exist_creates_new(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test conditional create when no matching resource exists."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            201,
            json={
                "resourceType": "Patient",
                "id": "new-patient-123",
                "identifier": [{"system": "http://example.org/mrn", "value": "12345"}],
            },
        )
    )

    patient = client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/mrn", "value": "12345"}],
        },
        if_none_exist="identifier=http://example.org/mrn|12345",
    )

    assert patient["resourceType"] == "Patient"
    assert patient["id"] == "new-patient-123"

    # Verify the If-None-Exist header was sent
    request = respx_mock.calls[0].request
    assert (
        request.headers.get("If-None-Exist")
        == "identifier=http://example.org/mrn|12345"
    )


def test_create_resource_if_none_exist_returns_existing(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test conditional create when a matching resource exists."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,  # 200 OK indicates existing resource returned
            json={
                "resourceType": "Patient",
                "id": "existing-patient-456",
                "identifier": [{"system": "http://example.org/mrn", "value": "12345"}],
            },
        )
    )

    patient = client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/mrn", "value": "12345"}],
        },
        if_none_exist="identifier=http://example.org/mrn|12345",
    )

    assert patient["resourceType"] == "Patient"
    assert patient["id"] == "existing-patient-456"


def test_create_resource_if_none_exist_with_custom_headers(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test conditional create with additional custom headers."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            201,
            json={"resourceType": "Patient", "id": "123"},
        )
    )

    client.create_resource_if_none_exist(
        {"resourceType": "Patient", "name": [{"family": "Smith"}]},
        if_none_exist="name:exact=Smith",
        headers={"X-Custom-Header": "test-value"},
    )

    request = respx_mock.calls[0].request
    assert request.headers.get("If-None-Exist") == "name:exact=Smith"
    assert request.headers.get("X-Custom-Header") == "test-value"


# Search With Options Tests


def test_search_with_options_summary_count(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search with _summary=count returns only total."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "total": 150,
            },
        )
    )

    result = client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        summary="count",
    )

    assert result["total"] == 150
    assert "entry" not in result

    # Verify the _summary parameter was sent
    request = respx_mock.calls[0].request
    assert "_summary=count" in str(request.url)


def test_search_with_options_elements(client: MedplumClient, respx_mock: MockRouter):
    """Test search with _elements returns only specified fields."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [
                    {
                        "resource": {
                            "resourceType": "Patient",
                            "id": "123",
                            "name": [{"family": "Smith"}],
                        }
                    }
                ],
            },
        )
    )

    result = client.search_with_options(
        "Patient",
        {"family": "Smith"},
        elements=["id", "name", "birthDate"],
    )

    assert result["resourceType"] == "Bundle"

    request = respx_mock.calls[0].request
    assert "_elements=id%2Cname%2CbirthDate" in str(request.url)


def test_search_with_options_total_accurate(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search with _total=accurate."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "total": 42,
                "entry": [],
            },
        )
    )

    result = client.search_with_options(
        "Patient",
        summary="count",
        total="accurate",
    )

    assert result["total"] == 42

    request = respx_mock.calls[0].request
    assert "_total=accurate" in str(request.url)


def test_search_with_options_at_point_in_time(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search with _at for point-in-time query."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [],
            },
        )
    )

    result = client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        at="2024-01-15T00:00:00Z",
    )

    assert result["resourceType"] == "Bundle"

    request = respx_mock.calls[0].request
    assert "_at=2024-01-15T00%3A00%3A00Z" in str(request.url)


def test_search_with_options_pagination(client: MedplumClient, respx_mock: MockRouter):
    """Test search with count and offset for pagination."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [{"resource": {"resourceType": "Observation", "id": "obs-1"}}],
            },
        )
    )

    result = client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        count=50,
        offset=100,
    )

    assert result["resourceType"] == "Bundle"

    request = respx_mock.calls[0].request
    url = str(request.url)
    assert "_count=50" in url
    assert "_offset=100" in url


def test_search_with_options_sort(client: MedplumClient, respx_mock: MockRouter):
    """Test search with _sort parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        sort=["-date", "status"],
    )

    request = respx_mock.calls[0].request
    assert "_sort=-date%2Cstatus" in str(request.url)


def test_search_with_options_include(client: MedplumClient, respx_mock: MockRouter):
    """Test search with _include parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    client.search_with_options(
        "Observation",
        {"code": "29463-7"},
        include=["Observation:patient", "Observation:performer"],
    )

    request = respx_mock.calls[0].request
    url = str(request.url)
    assert "_include=Observation%3Apatient" in url
    assert "_include=Observation%3Aperformer" in url


def test_search_with_options_revinclude(client: MedplumClient, respx_mock: MockRouter):
    """Test search with _revinclude parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    client.search_with_options(
        "Patient",
        {"identifier": "MRN|12345"},
        revinclude="Observation:patient",
    )

    request = respx_mock.calls[0].request
    assert "_revinclude=Observation%3Apatient" in str(request.url)


def test_search_with_options_return_bundle(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search_with_options with return_bundle=True."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Bundle",
                "type": "searchset",
                "entry": [
                    {"resource": {"resourceType": "Patient", "id": "p1"}},
                    {"resource": {"resourceType": "Patient", "id": "p2"}},
                ],
            },
        )
    )

    bundle = client.search_with_options(
        "Patient",
        {"family": "Smith"},
        return_bundle=True,
    )

    # Should return FHIRBundle wrapper
    assert hasattr(bundle, "get_resources")
    resources = list(bundle.get_resources())
    assert len(resources) == 2


# ValueSet $expand Tests


def test_expand_valueset_with_url(client: MedplumClient, respx_mock: MockRouter):
    """Test ValueSet $expand with canonical URL."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ValueSet/$expand").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ValueSet",
                "expansion": {
                    "contains": [
                        {"code": "male", "display": "Male"},
                        {"code": "female", "display": "Female"},
                        {"code": "other", "display": "Other"},
                    ]
                },
            },
        )
    )

    result = client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender"
    )

    assert result["resourceType"] == "ValueSet"
    assert len(result["expansion"]["contains"]) == 3


def test_expand_valueset_with_id(client: MedplumClient, respx_mock: MockRouter):
    """Test ValueSet $expand with resource ID."""
    respx_mock.post(
        "https://api.medplum.com/fhir/R4/ValueSet/my-valueset/$expand"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ValueSet",
                "expansion": {"contains": [{"code": "test", "display": "Test"}]},
            },
        )
    )

    result = client.expand_valueset(valueset_id="my-valueset")

    assert result["resourceType"] == "ValueSet"
    assert result["expansion"]["contains"][0]["code"] == "test"


def test_expand_valueset_with_filter(client: MedplumClient, respx_mock: MockRouter):
    """Test ValueSet $expand with text filter."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ValueSet/$expand").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ValueSet",
                "expansion": {
                    "contains": [
                        {"code": "123456", "display": "Type 2 Diabetes Mellitus"}
                    ]
                },
            },
        )
    )

    result = client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
        filter="diabetes",
        count=10,
    )

    assert result["resourceType"] == "ValueSet"
    assert "diabetes" in result["expansion"]["contains"][0]["display"].lower()


def test_expand_valueset_with_pagination(client: MedplumClient, respx_mock: MockRouter):
    """Test ValueSet $expand with pagination parameters."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ValueSet/$expand").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ValueSet",
                "expansion": {
                    "offset": 10,
                    "total": 100,
                    "contains": [{"code": "test", "display": "Test"}],
                },
            },
        )
    )

    result = client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
        offset=10,
        count=20,
    )

    assert result["expansion"]["offset"] == 10


# CodeSystem $lookup Tests


def test_lookup_concept_with_code_and_system(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test CodeSystem $lookup with code and system."""
    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$lookup").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "name", "valueString": "SNOMED CT"},
                    {"name": "display", "valueString": "Diabetes mellitus"},
                    {"name": "abstract", "valueBoolean": False},
                ],
            },
        )
    )

    result = client.lookup_concept(code="73211009", system="http://snomed.info/sct")

    assert result["resourceType"] == "Parameters"
    display_param = next(p for p in result["parameter"] if p["name"] == "display")
    assert display_param["valueString"] == "Diabetes mellitus"


def test_lookup_concept_with_codesystem_id(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test CodeSystem $lookup with instance ID."""
    respx_mock.post(
        "https://api.medplum.com/fhir/R4/CodeSystem/my-codesystem/$lookup"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "display", "valueString": "Custom Code"}],
            },
        )
    )

    result = client.lookup_concept(code="ABC123", codesystem_id="my-codesystem")

    assert result["resourceType"] == "Parameters"


def test_lookup_concept_with_properties(client: MedplumClient, respx_mock: MockRouter):
    """Test CodeSystem $lookup requesting specific properties."""
    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$lookup").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "display", "valueString": "Test"},
                    {
                        "name": "property",
                        "part": [
                            {"name": "code", "valueCode": "inactive"},
                            {"name": "value", "valueBoolean": False},
                        ],
                    },
                ],
            },
        )
    )

    result = client.lookup_concept(
        code="12345",
        system="http://example.org",
        property=["inactive", "parent"],
    )

    assert result["resourceType"] == "Parameters"


# ConceptMap $translate Tests


def test_translate_concept_with_code_and_system(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test ConceptMap $translate with code and system."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ConceptMap/$translate").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "result", "valueBoolean": True},
                    {
                        "name": "match",
                        "part": [
                            {"name": "equivalence", "valueCode": "equivalent"},
                            {
                                "name": "concept",
                                "valueCoding": {
                                    "system": "http://hl7.org/fhir/sid/icd-10",
                                    "code": "E11",
                                    "display": "Type 2 diabetes mellitus",
                                },
                            },
                        ],
                    },
                ],
            },
        )
    )

    result = client.translate_concept(
        code="73211009",
        system="http://snomed.info/sct",
        target_system="http://hl7.org/fhir/sid/icd-10",
    )

    assert result["resourceType"] == "Parameters"
    result_param = next(p for p in result["parameter"] if p["name"] == "result")
    assert result_param["valueBoolean"] is True


def test_translate_concept_with_conceptmap_id(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test ConceptMap $translate with specific ConceptMap ID."""
    respx_mock.post(
        "https://api.medplum.com/fhir/R4/ConceptMap/my-map/$translate"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": True}],
            },
        )
    )

    result = client.translate_concept(
        code="12345",
        system="http://example.org/source",
        conceptmap_id="my-map",
    )

    assert result["resourceType"] == "Parameters"


def test_translate_concept_with_coding(client: MedplumClient, respx_mock: MockRouter):
    """Test ConceptMap $translate with full Coding object."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ConceptMap/$translate").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": True}],
            },
        )
    )

    result = client.translate_concept(
        coding={
            "system": "http://snomed.info/sct",
            "code": "73211009",
            "display": "Diabetes mellitus",
        },
        target_system="http://hl7.org/fhir/sid/icd-10",
    )

    assert result["resourceType"] == "Parameters"


def test_translate_concept_no_match(client: MedplumClient, respx_mock: MockRouter):
    """Test ConceptMap $translate when no mapping found."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ConceptMap/$translate").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [
                    {"name": "result", "valueBoolean": False},
                    {"name": "message", "valueString": "No mapping found"},
                ],
            },
        )
    )

    result = client.translate_concept(
        code="unknown-code",
        system="http://example.org",
        target_system="http://example.org/target",
    )

    result_param = next(p for p in result["parameter"] if p["name"] == "result")
    assert result_param["valueBoolean"] is False


# Execute Operation GET/wrap_params Tests


def test_execute_operation_with_get_method(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test execute_operation with GET method and query parameters."""
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/ValueSet/$expand",
        params={"url": "http://example.org/vs", "filter": "test"},
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "ValueSet",
                "expansion": {"contains": [{"code": "test", "display": "Test"}]},
            },
        )
    )

    result = client.execute_operation(
        "ValueSet",
        "$expand",
        params={"url": "http://example.org/vs", "filter": "test"},
        method="GET",
    )

    assert result["resourceType"] == "ValueSet"
    assert "expansion" in result


def test_execute_operation_with_wrap_params(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test execute_operation with wrap_params to auto-convert dict to Parameters."""

    def check_request(request):
        body = request.read()
        import json

        data = json.loads(body)
        # Should be wrapped in Parameters structure
        assert data["resourceType"] == "Parameters"
        assert len(data["parameter"]) == 2
        params_dict = {p["name"]: p for p in data["parameter"]}
        assert params_dict["code"]["valueString"] == "male"
        assert params_dict["system"]["valueString"] == "http://example.org"
        return httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "display", "valueString": "Male"}],
            },
        )

    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$lookup").mock(
        side_effect=check_request
    )

    result = client.execute_operation(
        "CodeSystem",
        "$lookup",
        params={"code": "male", "system": "http://example.org"},
        wrap_params=True,
    )

    assert result["resourceType"] == "Parameters"


def test_execute_operation_no_double_wrap_existing_parameters(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that execute_operation doesn't double-wrap existing Parameters resource."""
    # This tests the case where params is already a Parameters resource
    # and wrap_params=False (default) - it should be passed through unchanged

    existing_parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "code", "valueCode": "12345"},
            {"name": "system", "valueUri": "http://loinc.org"},
        ],
    }

    def check_request(request):
        body = request.read()
        import json

        data = json.loads(body)
        # Should NOT be double-wrapped - resourceType should be Parameters directly
        assert data["resourceType"] == "Parameters"
        assert len(data["parameter"]) == 2
        # Verify the original parameter types are preserved (valueCode, valueUri)
        params_dict = {p["name"]: p for p in data["parameter"]}
        assert params_dict["code"]["valueCode"] == "12345"
        assert params_dict["system"]["valueUri"] == "http://loinc.org"
        return httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "display", "valueString": "Test"}],
            },
        )

    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$lookup").mock(
        side_effect=check_request
    )

    result = client.execute_operation(
        "CodeSystem",
        "$lookup",
        params=existing_parameters,
        wrap_params=False,  # Explicit default - should not wrap
    )

    assert result["resourceType"] == "Parameters"


def test_execute_operation_wrap_params_skips_existing_parameters(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that wrap_params=True doesn't wrap already-valid Parameters resource."""
    # Even with wrap_params=True, an existing Parameters resource should not be wrapped

    existing_parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "code", "valueCode": "12345"},
        ],
    }

    def check_request(request):
        body = request.read()
        import json

        data = json.loads(body)
        # Should NOT be double-wrapped
        assert data["resourceType"] == "Parameters"
        assert len(data["parameter"]) == 1
        assert data["parameter"][0]["name"] == "code"
        assert data["parameter"][0]["valueCode"] == "12345"
        return httpx.Response(
            200,
            json={"resourceType": "Parameters", "parameter": []},
        )

    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$lookup").mock(
        side_effect=check_request
    )

    result = client.execute_operation(
        "CodeSystem",
        "$lookup",
        params=existing_parameters,
        wrap_params=True,  # Should detect existing Parameters and skip wrapping
    )

    assert result["resourceType"] == "Parameters"


# Conditional Create Query Normalization Tests


def test_create_resource_if_none_exist_normalizes_query_with_question_mark(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that leading ? is stripped from if_none_exist query."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            201,
            json={"resourceType": "Patient", "id": "new-patient"},
        )
    )

    client.create_resource_if_none_exist(
        {"resourceType": "Patient"},
        if_none_exist="?identifier=test",  # Note the leading ?
    )

    # Verify the ? was stripped
    request = respx_mock.calls[0].request
    assert request.headers.get("If-None-Exist") == "identifier=test"


def test_create_resource_if_none_exist_rejects_empty_query(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test that empty query string raises ValueError."""
    import pytest

    with pytest.raises(ValueError, match="non-empty"):
        client.create_resource_if_none_exist(
            {"resourceType": "Patient"},
            if_none_exist="",
        )


# Search with Options include_iterate/revinclude_iterate Tests


def test_search_with_options_include_iterate(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search_with_options with include_iterate parameter."""
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/MedicationRequest",
    ).mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    client.search_with_options(
        "MedicationRequest",
        include=["MedicationRequest:medication"],
        include_iterate=["Medication:manufacturer"],
    )

    # Verify the query params were sent correctly using multi_items for stability
    request = respx_mock.calls[0].request
    params = list(request.url.params.multi_items())
    assert ("_include", "MedicationRequest:medication") in params
    assert ("_include:iterate", "Medication:manufacturer") in params


def test_search_with_options_revinclude_iterate(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search_with_options with revinclude_iterate parameter."""
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient",
    ).mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    client.search_with_options(
        "Patient",
        revinclude=["Observation:patient"],
        revinclude_iterate=["Provenance:target"],
    )

    # Verify the query params were sent correctly using multi_items for stability
    request = respx_mock.calls[0].request
    params = list(request.url.params.multi_items())
    assert ("_revinclude", "Observation:patient") in params
    assert ("_revinclude:iterate", "Provenance:target") in params


def test_search_with_options_multiple_include_iterate(
    client: MedplumClient, respx_mock: MockRouter
):
    """Test search_with_options with multiple include_iterate values."""
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Encounter",
    ).mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    client.search_with_options(
        "Encounter",
        include_iterate=["Location:organization", "Organization:partOf"],
    )

    # Verify multiple iterate params were sent using multi_items for stability
    request = respx_mock.calls[0].request
    params = list(request.url.params.multi_items())
    assert ("_include:iterate", "Location:organization") in params
    assert ("_include:iterate", "Organization:partOf") in params


# vread_resource tests


def test_vread_resource_success(client: MedplumClient, respx_mock: MockRouter):
    """Test successful version-specific read of a resource."""
    patient_data = {
        "resourceType": "Patient",
        "id": "patient-123",
        "meta": {"versionId": "2"},
        "name": [{"family": "Smith", "given": ["John"]}],
    }

    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/patient-123/_history/2"
    ).mock(return_value=httpx.Response(200, json=patient_data))

    result = client.vread_resource("Patient", "patient-123", "2")

    assert result["resourceType"] == "Patient"
    assert result["id"] == "patient-123"
    assert result["meta"]["versionId"] == "2"


def test_vread_resource_with_as_fhir(client: MedplumClient, respx_mock: MockRouter):
    """Test vread_resource with as_fhir for type-safe response."""
    from pymedplum.fhir import Patient

    patient_data = {
        "resourceType": "Patient",
        "id": "patient-456",
        "meta": {"versionId": "1"},
        "name": [{"family": "Doe", "given": ["Jane"]}],
        "gender": "female",
    }

    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/patient-456/_history/1"
    ).mock(return_value=httpx.Response(200, json=patient_data))

    result = client.vread_resource("Patient", "patient-456", "1", as_fhir=Patient)

    # Verify it's a typed Patient model, not a dict
    assert isinstance(result, Patient)
    assert result.id == "patient-456"
    assert result.name[0].family == "Doe"
    assert result.gender == "female"


def test_vread_resource_not_found(client: MedplumClient, respx_mock: MockRouter):
    """Test vread_resource with non-existent version."""
    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/patient-123/_history/999"
    ).mock(
        return_value=httpx.Response(
            404,
            json={
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "not-found",
                        "details": {"text": "Version not found"},
                    }
                ],
            },
        )
    )

    with pytest.raises(Exception):  # Should raise NotFoundError
        client.vread_resource("Patient", "patient-123", "999")
