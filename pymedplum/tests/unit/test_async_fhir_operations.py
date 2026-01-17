"""Unit tests for async FHIR operations (C-CDA, validation, bundles, binary).

Tests the async client implementation with mocked HTTP responses.
"""

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

    # Mock the GET request with Accept: */* to return raw binary content
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/binary-123").mock(
        return_value=httpx.Response(
            200,
            content=pdf_content,
            headers={"Content-Type": "application/pdf"},
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


# Execute Operation Tests


@pytest.mark.asyncio
async def test_async_execute_operation_type_level(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async type-level FHIR operation execution."""
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

    result = await async_client.execute_operation(
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


@pytest.mark.asyncio
async def test_async_execute_operation_instance_level(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async instance-level FHIR operation execution."""
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

    result = await async_client.execute_operation(
        "Patient", "everything", resource_id="123"
    )

    assert result["resourceType"] == "Bundle"
    assert len(result["entry"]) == 2


@pytest.mark.asyncio
async def test_async_execute_operation_custom_with_headers(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async custom FHIR operation with custom headers."""
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

    result = await async_client.execute_operation(
        "MedicationRequest",
        "calculate-dose",
        resource_id="med-123",
        params={"weight": 70, "unit": "kg"},
        headers={"X-Custom-Header": "test-value"},
    )

    assert result["resourceType"] == "Parameters"
    assert result["parameter"][0]["valueQuantity"]["value"] == 500


@pytest.mark.asyncio
async def test_async_execute_operation_allows_dollar_prefix(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test that async operation names with $ prefix are accepted."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient/$match").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    # Should work with or without the $ prefix
    result = await async_client.execute_operation("Patient", "$match", params={})

    assert result["resourceType"] == "Bundle"


@pytest.mark.asyncio
async def test_async_execute_bot_uses_execute_operation(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test that async execute_bot internally uses execute_operation."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Bot/bot-123/$execute").mock(
        return_value=httpx.Response(
            200,
            json={"message": "Bot executed successfully"},
        )
    )

    result = await async_client.execute_bot(
        bot_id="bot-123",
        input_data={"resourceType": "Patient", "id": "patient-123"},
    )

    assert result["message"] == "Bot executed successfully"


# Conditional Create Tests


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_creates_new(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async conditional create when no matching resource exists."""
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

    patient = await async_client.create_resource_if_none_exist(
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


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_returns_existing(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async conditional create when a matching resource exists."""
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

    patient = await async_client.create_resource_if_none_exist(
        {
            "resourceType": "Patient",
            "identifier": [{"system": "http://example.org/mrn", "value": "12345"}],
        },
        if_none_exist="identifier=http://example.org/mrn|12345",
    )

    assert patient["resourceType"] == "Patient"
    assert patient["id"] == "existing-patient-456"


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_with_custom_headers(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async conditional create with additional custom headers."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            201,
            json={"resourceType": "Patient", "id": "123"},
        )
    )

    await async_client.create_resource_if_none_exist(
        {"resourceType": "Patient", "name": [{"family": "Smith"}]},
        if_none_exist="name:exact=Smith",
        headers={"X-Custom-Header": "test-value"},
    )

    request = respx_mock.calls[0].request
    assert request.headers.get("If-None-Exist") == "name:exact=Smith"
    assert request.headers.get("X-Custom-Header") == "test-value"


# Search With Options Tests


@pytest.mark.asyncio
async def test_async_search_with_options_summary_count(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _summary=count returns only total."""
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

    result = await async_client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        summary="count",
    )

    assert result["total"] == 150
    assert "entry" not in result

    request = respx_mock.calls[0].request
    assert "_summary=count" in str(request.url)


@pytest.mark.asyncio
async def test_async_search_with_options_elements(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _elements returns only specified fields."""
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

    result = await async_client.search_with_options(
        "Patient",
        {"family": "Smith"},
        elements=["id", "name", "birthDate"],
    )

    assert result["resourceType"] == "Bundle"

    request = respx_mock.calls[0].request
    assert "_elements=id%2Cname%2CbirthDate" in str(request.url)


@pytest.mark.asyncio
async def test_async_search_with_options_total_accurate(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _total=accurate."""
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

    result = await async_client.search_with_options(
        "Patient",
        summary="count",
        total="accurate",
    )

    assert result["total"] == 42

    request = respx_mock.calls[0].request
    assert "_total=accurate" in str(request.url)


@pytest.mark.asyncio
async def test_async_search_with_options_at_point_in_time(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _at for point-in-time query."""
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

    result = await async_client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        at="2024-01-15T00:00:00Z",
    )

    assert result["resourceType"] == "Bundle"

    request = respx_mock.calls[0].request
    assert "_at=2024-01-15T00%3A00%3A00Z" in str(request.url)


@pytest.mark.asyncio
async def test_async_search_with_options_pagination(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with count and offset for pagination."""
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

    result = await async_client.search_with_options(
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


@pytest.mark.asyncio
async def test_async_search_with_options_sort(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _sort parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    await async_client.search_with_options(
        "Observation",
        {"patient": "Patient/123"},
        sort=["-date", "status"],
    )

    request = respx_mock.calls[0].request
    assert "_sort=-date%2Cstatus" in str(request.url)


@pytest.mark.asyncio
async def test_async_search_with_options_include(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _include parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Observation").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    await async_client.search_with_options(
        "Observation",
        {"code": "29463-7"},
        include=["Observation:patient", "Observation:performer"],
    )

    request = respx_mock.calls[0].request
    url = str(request.url)
    assert "_include=Observation%3Apatient" in url
    assert "_include=Observation%3Aperformer" in url


@pytest.mark.asyncio
async def test_async_search_with_options_revinclude(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search with _revinclude parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    await async_client.search_with_options(
        "Patient",
        {"identifier": "MRN|12345"},
        revinclude="Observation:patient",
    )

    request = respx_mock.calls[0].request
    assert "_revinclude=Observation%3Apatient" in str(request.url)


@pytest.mark.asyncio
async def test_async_search_with_options_return_bundle(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search_with_options with return_bundle=True."""
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

    bundle = await async_client.search_with_options(
        "Patient",
        {"family": "Smith"},
        return_bundle=True,
    )

    # Should return FHIRBundle wrapper
    assert hasattr(bundle, "get_resources")
    resources = list(bundle.get_resources())
    assert len(resources) == 2


# ValueSet $expand Tests


@pytest.mark.asyncio
async def test_async_expand_valueset_with_url(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ValueSet $expand with canonical URL."""
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

    result = await async_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender"
    )

    assert result["resourceType"] == "ValueSet"
    assert len(result["expansion"]["contains"]) == 3


@pytest.mark.asyncio
async def test_async_expand_valueset_with_id(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ValueSet $expand with resource ID."""
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

    result = await async_client.expand_valueset(valueset_id="my-valueset")

    assert result["resourceType"] == "ValueSet"
    assert result["expansion"]["contains"][0]["code"] == "test"


@pytest.mark.asyncio
async def test_async_expand_valueset_with_filter(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ValueSet $expand with text filter."""
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

    result = await async_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
        filter="diabetes",
        count=10,
    )

    assert result["resourceType"] == "ValueSet"
    assert "diabetes" in result["expansion"]["contains"][0]["display"].lower()


@pytest.mark.asyncio
async def test_async_expand_valueset_with_pagination(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ValueSet $expand with pagination parameters."""
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

    result = await async_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
        offset=10,
        count=20,
    )

    assert result["expansion"]["offset"] == 10


# CodeSystem $lookup Tests


@pytest.mark.asyncio
async def test_async_lookup_concept_with_code_and_system(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async CodeSystem $lookup with code and system."""
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

    result = await async_client.lookup_concept(
        code="73211009", system="http://snomed.info/sct"
    )

    assert result["resourceType"] == "Parameters"
    display_param = next(p for p in result["parameter"] if p["name"] == "display")
    assert display_param["valueString"] == "Diabetes mellitus"


@pytest.mark.asyncio
async def test_async_lookup_concept_with_codesystem_id(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async CodeSystem $lookup with instance ID."""
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

    result = await async_client.lookup_concept(
        code="ABC123", codesystem_id="my-codesystem"
    )

    assert result["resourceType"] == "Parameters"


@pytest.mark.asyncio
async def test_async_lookup_concept_with_properties(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async CodeSystem $lookup requesting specific properties."""
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

    result = await async_client.lookup_concept(
        code="12345",
        system="http://example.org",
        property=["inactive", "parent"],
    )

    assert result["resourceType"] == "Parameters"


# ConceptMap $translate Tests


@pytest.mark.asyncio
async def test_async_translate_concept_with_code_and_system(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ConceptMap $translate with code and system."""
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

    result = await async_client.translate_concept(
        code="73211009",
        system="http://snomed.info/sct",
        target_system="http://hl7.org/fhir/sid/icd-10",
    )

    assert result["resourceType"] == "Parameters"
    result_param = next(p for p in result["parameter"] if p["name"] == "result")
    assert result_param["valueBoolean"] is True


@pytest.mark.asyncio
async def test_async_translate_concept_with_conceptmap_id(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ConceptMap $translate with specific ConceptMap ID."""
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

    result = await async_client.translate_concept(
        code="12345",
        system="http://example.org/source",
        conceptmap_id="my-map",
    )

    assert result["resourceType"] == "Parameters"


@pytest.mark.asyncio
async def test_async_translate_concept_with_coding(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ConceptMap $translate with full Coding object."""
    respx_mock.post("https://api.medplum.com/fhir/R4/ConceptMap/$translate").mock(
        return_value=httpx.Response(
            200,
            json={
                "resourceType": "Parameters",
                "parameter": [{"name": "result", "valueBoolean": True}],
            },
        )
    )

    result = await async_client.translate_concept(
        coding={
            "system": "http://snomed.info/sct",
            "code": "73211009",
            "display": "Diabetes mellitus",
        },
        target_system="http://hl7.org/fhir/sid/icd-10",
    )

    assert result["resourceType"] == "Parameters"


@pytest.mark.asyncio
async def test_async_translate_concept_no_match(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async ConceptMap $translate when no mapping found."""
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

    result = await async_client.translate_concept(
        code="unknown-code",
        system="http://example.org",
        target_system="http://example.org/target",
    )

    result_param = next(p for p in result["parameter"] if p["name"] == "result")
    assert result_param["valueBoolean"] is False


# Execute Operation GET/wrap_params Tests


@pytest.mark.asyncio
async def test_async_execute_operation_with_get_method(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async execute_operation with GET method and query parameters."""
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

    result = await async_client.execute_operation(
        "ValueSet",
        "$expand",
        params={"url": "http://example.org/vs", "filter": "test"},
        method="GET",
    )

    assert result["resourceType"] == "ValueSet"
    assert result["expansion"]["contains"][0]["code"] == "test"


@pytest.mark.asyncio
async def test_async_execute_operation_with_wrap_params(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async execute_operation with wrap_params to auto-convert dict."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient/$match").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    result = await async_client.execute_operation(
        "Patient",
        "$match",
        params={"name": "Smith", "birthdate": "1990-01-01"},
        wrap_params=True,
    )

    assert result["resourceType"] == "Bundle"

    # Verify the request body was wrapped in Parameters format
    request = respx_mock.calls[0].request
    import json

    body = json.loads(request.content)
    assert body["resourceType"] == "Parameters"
    assert "parameter" in body
    param_names = [p["name"] for p in body["parameter"]]
    assert "name" in param_names
    assert "birthdate" in param_names


# Create Resource If None Exist - Query Normalization Tests


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_normalizes_query_with_question_mark(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async that leading ? is stripped from if_none_exist query."""
    respx_mock.post("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            201,
            json={"resourceType": "Patient", "id": "123"},
        )
    )

    await async_client.create_resource_if_none_exist(
        {"resourceType": "Patient", "name": [{"family": "Smith"}]},
        if_none_exist="?identifier=http://example.org|12345",
    )

    request = respx_mock.calls[0].request
    # Should strip the leading ?
    assert request.headers.get("If-None-Exist") == "identifier=http://example.org|12345"


@pytest.mark.asyncio
async def test_async_create_resource_if_none_exist_rejects_empty_query(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async that empty query string raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        await async_client.create_resource_if_none_exist(
            {"resourceType": "Patient", "name": [{"family": "Smith"}]},
            if_none_exist="",
        )

    with pytest.raises(ValueError, match="cannot be empty"):
        await async_client.create_resource_if_none_exist(
            {"resourceType": "Patient", "name": [{"family": "Smith"}]},
            if_none_exist="?",
        )


# Search With Options - Include/Revinclude Iterate Tests


@pytest.mark.asyncio
async def test_async_search_with_options_include_iterate(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search_with_options with include_iterate parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/MedicationRequest").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    await async_client.search_with_options(
        "MedicationRequest",
        {"patient": "Patient/123"},
        include="MedicationRequest:medication",
        include_iterate="Medication:manufacturer",
    )

    # Verify the query params using multi_items for stability across httpx versions
    request = respx_mock.calls[0].request
    params = list(request.url.params.multi_items())
    assert ("_include", "MedicationRequest:medication") in params
    assert ("_include:iterate", "Medication:manufacturer") in params


@pytest.mark.asyncio
async def test_async_search_with_options_revinclude_iterate(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search_with_options with revinclude_iterate parameter."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    await async_client.search_with_options(
        "Patient",
        {"identifier": "MRN|12345"},
        revinclude_iterate="Provenance:target",
    )

    # Verify the query params using multi_items for stability across httpx versions
    request = respx_mock.calls[0].request
    params = list(request.url.params.multi_items())
    assert ("_revinclude:iterate", "Provenance:target") in params


@pytest.mark.asyncio
async def test_async_search_with_options_multiple_include_iterate(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async search_with_options with multiple include_iterate values."""
    respx_mock.get("https://api.medplum.com/fhir/R4/MedicationRequest").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    await async_client.search_with_options(
        "MedicationRequest",
        {"patient": "Patient/123"},
        include_iterate=["Medication:manufacturer", "Organization:partof"],
    )

    # Verify multiple iterate params using multi_items for stability across httpx versions
    request = respx_mock.calls[0].request
    params = list(request.url.params.multi_items())
    assert ("_include:iterate", "Medication:manufacturer") in params
    assert ("_include:iterate", "Organization:partof") in params


# vread_resource tests


@pytest.mark.asyncio
async def test_async_vread_resource_success(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test successful async version-specific read of a resource."""
    patient_data = {
        "resourceType": "Patient",
        "id": "patient-123",
        "meta": {"versionId": "2"},
        "name": [{"family": "Smith", "given": ["John"]}],
    }

    respx_mock.get(
        "https://api.medplum.com/fhir/R4/Patient/patient-123/_history/2"
    ).mock(return_value=httpx.Response(200, json=patient_data))

    result = await async_client.vread_resource("Patient", "patient-123", "2")

    assert result["resourceType"] == "Patient"
    assert result["id"] == "patient-123"
    assert result["meta"]["versionId"] == "2"


@pytest.mark.asyncio
async def test_async_vread_resource_with_as_fhir(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async vread_resource with as_fhir for type-safe response."""
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

    result = await async_client.vread_resource(
        "Patient", "patient-456", "1", as_fhir=Patient
    )

    # Verify it's a typed Patient model, not a dict
    assert isinstance(result, Patient)
    assert result.id == "patient-456"
    assert result.name[0].family == "Doe"
    assert result.gender == "female"


@pytest.mark.asyncio
async def test_async_vread_resource_not_found(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
):
    """Test async vread_resource with non-existent version."""
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
        await async_client.vread_resource("Patient", "patient-123", "999")
