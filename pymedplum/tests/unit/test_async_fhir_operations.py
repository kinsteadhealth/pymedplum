"""Unit tests for async FHIR operations (C-CDA, validation, bundles, binary).

Tests the async client implementation with mocked HTTP responses.
"""

import base64

import httpx
import pytest
from respx import MockRouter

from pymedplum.async_client import AsyncMedplumClient


@pytest.fixture
async def async_client():
    """Create an AsyncMedplumClient with access token for testing."""
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        access_token="test-token",
    ) as client:
        yield client


# C-CDA Export Tests


@pytest.mark.asyncio
async def test_async_export_ccda_success(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test successful async C-CDA export."""
    ccda_xml = """<?xml version="1.0"?>
    <ClinicalDocument xmlns="urn:hl7-org:v3">
        <patient>Test Patient</patient>
    </ClinicalDocument>"""

    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/patient-123/$ccda-export"
    ).mock(return_value=httpx.Response(200, text=ccda_xml))

    result = await async_client.export_ccda("patient-123")

    assert result == ccda_xml
    assert "ClinicalDocument" in result


@pytest.mark.asyncio
async def test_async_export_ccda_not_found(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async C-CDA export with non-existent patient."""
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

    with pytest.raises(Exception):
        await async_client.export_ccda("nonexistent")


# ValueSet Validation Tests


@pytest.mark.asyncio
async def test_async_validate_valueset_code_with_url_and_coding(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ValueSet validation with URL and coding."""
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

    result = await async_client.validate_valueset_code(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-severity",
        coding={"system": "http://snomed.info/sct", "code": "255604002"},
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueBoolean"] is True
    assert result["parameter"][1]["valueString"] == "Severe"


@pytest.mark.asyncio
async def test_async_validate_valueset_code_with_id_and_code_system(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ValueSet validation with instance ID and code+system."""
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

    result = await async_client.validate_valueset_code(
        valueset_id="my-valueset",
        code="12345",
        system="http://example.com/codesystem",
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueBoolean"] is False


# CodeSystem Validation Tests


@pytest.mark.asyncio
async def test_async_validate_codesystem_code_with_url_and_code(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async CodeSystem validation with URL and code."""
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

    result = await async_client.validate_codesystem_code(
        codesystem_url="http://snomed.info/sct", code="255604002"
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueBoolean"] is True


@pytest.mark.asyncio
async def test_async_validate_codesystem_code_with_version(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async CodeSystem validation with specific version."""
    respx_mock.post("https://api.medplum.com/fhir/R4/CodeSystem/$validate-code").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": True}],
            },
        )
    )

    result = await async_client.validate_codesystem_code(
        codesystem_url="http://snomed.info/sct",
        code="12345",
        version="2021-03",
    )

    assert result["parameter"][0]["valueBoolean"] is True


# Transaction Bundle Tests


@pytest.mark.asyncio
async def test_async_execute_transaction_bundle_success(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test successful async transaction bundle execution."""
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

    result = await async_client.execute_transaction(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "transaction-response"
    assert result["entry"][0]["response"]["status"] == "201 Created"


@pytest.mark.asyncio
async def test_async_execute_transaction_auto_sets_type(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test that async transaction type is automatically set."""
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

    bundle = {"resourceType": "Bundle", "entry": []}

    result = await async_client.execute_transaction(bundle)

    assert result["type"] == "transaction-response"


# Batch Bundle Tests


@pytest.mark.asyncio
async def test_async_execute_batch_bundle_success(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test successful async batch bundle execution."""
    # Mock the batch endpoint (without trailing slash)
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

    result = await async_client.execute_batch(bundle)

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "batch-response"
    assert len(result["entry"]) == 2


# Binary Operations Tests


@pytest.mark.asyncio
async def test_async_upload_binary(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async binary content upload."""
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
    result = await async_client.upload_binary(pdf_content, "application/pdf")

    assert result["resourceType"] == "Binary"
    assert result["id"] == "binary-123"
    assert result["contentType"] == "application/pdf"


@pytest.mark.asyncio
async def test_async_download_binary(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async binary content download."""
    pdf_content = b"%PDF-1.4 test content"

    # Mock the read_resource call that download_binary makes
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/binary-123").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Binary",
                "id": "binary-123",
                "contentType": "application/pdf",
                "data": base64.b64encode(pdf_content).decode("utf-8"),
            },
        )
    )

    result = await async_client.download_binary("binary-123")

    assert result == pdf_content
    assert isinstance(result, bytes)


@pytest.mark.asyncio
async def test_async_download_binary_not_found(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async download of non-existent binary."""
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
        await async_client.download_binary("nonexistent")


# DocumentReference Tests


@pytest.mark.asyncio
async def test_async_create_document_reference(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async creating a DocumentReference."""
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

    result = await async_client.create_document_reference(
        patient_id="patient-123",
        binary_id="binary-456",
        content_type="application/xml",
        title="Test Document",
    )

    assert result["resourceType"] == "DocumentReference"
    assert result["id"] == "doc-ref-123"
    assert result["subject"]["reference"] == "Patient/patient-123"
    assert result["content"][0]["attachment"]["url"] == "Binary/binary-456"


@pytest.mark.asyncio
async def test_async_create_document_reference_with_optional_fields(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async creating DocumentReference with optional fields."""
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

    result = await async_client.create_document_reference(
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
