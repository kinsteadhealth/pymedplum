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
