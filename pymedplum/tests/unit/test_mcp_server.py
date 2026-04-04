"""Unit tests for the MCP server module.

Tests helpers, validation, schema generation, read-only enforcement,
on-behalf-of validation, and Pydantic input models. All tests run
without a real Medplum server.
"""

import os
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest

import pymedplum.mcp.server as srv
from pymedplum.mcp.server import (
    BundleInput,
    PatchOp,
    _annotate_response,
    _collect_refs,
    _get_fhir_model,
    _is_read_only,
    _validate_on_behalf_of,
    _validate_resource,
    create_bot,
    create_resource,
    create_resource_if_none_exist,
    delete_resource,
    execute_batch,
    execute_bot,
    execute_operation,
    export_ccda,
    get_resource_schema,
    patch_resource,
    read_resource,
    save_and_deploy_bot,
    search_all_resources,
    search_one,
    search_resources,
    update_resource,
    validate_codesystem_code,
)


class TestGetFhirModel:
    def test_known_resource_type(self):
        model = _get_fhir_model("Patient")
        assert model is not None
        assert model.__name__ == "Patient"

    def test_known_data_type(self):
        model = _get_fhir_model("HumanName")
        assert model is not None

    def test_medplum_specific_type(self):
        model = _get_fhir_model("Bot")
        assert model is not None

    def test_unknown_type_returns_none(self):
        assert _get_fhir_model("NonExistentType") is None

    def test_empty_string_returns_none(self):
        assert _get_fhir_model("") is None


class TestCollectRefs:
    def test_finds_refs_in_dict(self):
        schema = {
            "properties": {
                "name": {"$ref": "#/$defs/HumanName"},
                "id": {"type": "string"},
            }
        }
        refs: set[str] = set()
        _collect_refs(schema, refs)
        assert refs == {"HumanName"}

    def test_finds_refs_in_nested_lists(self):
        schema = {
            "anyOf": [
                {"items": {"$ref": "#/$defs/Extension"}},
                {"type": "null"},
            ]
        }
        refs: set[str] = set()
        _collect_refs(schema, refs)
        assert refs == {"Extension"}

    def test_empty_schema(self):
        refs: set[str] = set()
        _collect_refs({}, refs)
        assert refs == set()


class TestAnnotateResponse:
    def test_adds_hints_for_known_type(self):
        result = {"resourceType": "Patient", "id": "123"}
        annotated = _annotate_response(result)
        assert annotated["_response_type"] == "Patient"
        assert "get_resource_schema('Patient')" in annotated["_schema_hint"]

    def test_no_hints_for_unknown_type(self):
        result = {"resourceType": "UnknownThing", "id": "123"}
        annotated = _annotate_response(result)
        assert "_response_type" not in annotated

    def test_no_hints_without_resource_type(self):
        result = {"data": "something"}
        annotated = _annotate_response(result)
        assert "_response_type" not in annotated

    def test_bundles_get_annotated(self):
        result = {"resourceType": "Bundle", "type": "searchset", "total": 0}
        annotated = _annotate_response(result)
        assert annotated["_response_type"] == "Bundle"


class TestValidateResource:
    def test_valid_patient_passes(self):
        _validate_resource({
            "resourceType": "Patient",
            "name": [{"given": ["Alice"], "family": "Smith"}],
        })

    def test_invalid_gender_raises(self):
        with pytest.raises(ValueError, match="FHIR Patient validation failed"):
            _validate_resource({
                "resourceType": "Patient",
                "gender": "invalid_value",
            })

    def test_error_includes_schema_hint(self):
        with pytest.raises(ValueError, match="get_resource_schema"):
            _validate_resource({
                "resourceType": "Patient",
                "birthDate": 12345,
            })

    def test_unknown_type_passes_silently(self):
        _validate_resource({"resourceType": "UnknownType", "foo": "bar"})

    def test_missing_resource_type_passes(self):
        _validate_resource({"foo": "bar"})

    def test_empty_dict_passes(self):
        _validate_resource({})


class TestValidateOnBehalfOf:
    def test_bare_uuid(self):
        result = _validate_on_behalf_of("550e8400-e29b-41d4-a716-446655440000")
        assert result == "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"

    def test_full_reference(self):
        result = _validate_on_behalf_of(
            "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"
        )
        assert result == "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"

    def test_strips_whitespace(self):
        result = _validate_on_behalf_of(
            "  550e8400-e29b-41d4-a716-446655440000  "
        )
        assert result == "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"

    def test_case_insensitive_uuid(self):
        result = _validate_on_behalf_of("550E8400-E29B-41D4-A716-446655440000")
        assert result == "ProjectMembership/550E8400-E29B-41D4-A716-446655440000"

    def test_rejects_empty_string(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_on_behalf_of("")

    def test_rejects_non_uuid(self):
        with pytest.raises(ValueError, match="Invalid ProjectMembership reference"):
            _validate_on_behalf_of("not-a-uuid")

    def test_rejects_partial_uuid(self):
        with pytest.raises(ValueError, match="Invalid ProjectMembership reference"):
            _validate_on_behalf_of("550e8400-e29b-41d4")

    def test_error_includes_example(self):
        with pytest.raises(ValueError, match="Example:"):
            _validate_on_behalf_of("garbage")


class TestIsReadOnly:
    def test_default_is_false(self):
        with patch.dict(os.environ, {}, clear=True):
            assert _is_read_only() is False

    def test_true_values(self):
        for val in ("true", "True", "TRUE", "1", "yes", "YES"):
            with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": val}):
                assert _is_read_only() is True

    def test_false_values(self):
        for val in ("false", "0", "no", "anything"):
            with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": val}):
                assert _is_read_only() is False


class TestPatchOpModel:
    def test_valid_replace(self):
        op = PatchOp(op="replace", path="/active", value=True)
        assert op.op == "replace"
        assert op.path == "/active"
        assert op.value is True

    def test_valid_remove_no_value(self):
        op = PatchOp(op="remove", path="/extension/0")
        assert op.value is None

    def test_invalid_op_rejected(self):
        with pytest.raises(Exception):
            PatchOp(op="invalid", path="/foo")

    def test_missing_path_rejected(self):
        with pytest.raises(Exception):
            PatchOp(op="add")

    def test_dump_excludes_none(self):
        op = PatchOp(op="remove", path="/foo")
        dumped = op.model_dump(exclude_none=True)
        assert "value" not in dumped
        assert dumped == {"op": "remove", "path": "/foo"}


class TestBundleInputModel:
    def test_valid_batch(self):
        bundle = BundleInput(
            type="batch",
            entry=[{"request": {"method": "GET", "url": "Patient/123"}}],
        )
        assert bundle.type == "batch"
        assert bundle.resourceType == "Bundle"

    def test_valid_transaction(self):
        bundle = BundleInput(type="transaction", entry=[])
        assert bundle.type == "transaction"

    def test_invalid_type_rejected(self):
        with pytest.raises(Exception):
            BundleInput(type="invalid")

    def test_default_entry_empty(self):
        bundle = BundleInput(type="batch")
        assert bundle.entry == []

    def test_dump_uses_alias(self):
        bundle = BundleInput(type="batch")
        raw = bundle.model_dump(by_alias=True)
        assert raw["resourceType"] == "Bundle"
        assert raw["type"] == "batch"


class TestGetResourceSchema:
    @pytest.mark.asyncio
    async def test_patient_schema_has_properties(self):
        result = await get_resource_schema("Patient")
        assert "properties" in result
        props = result["properties"]
        assert "name" in props
        assert "birthDate" in props
        assert "gender" in props

    @pytest.mark.asyncio
    async def test_compact_mode_strips_defs(self):
        result = await get_resource_schema("Patient", include_nested=False)
        assert "$defs" not in result

    @pytest.mark.asyncio
    async def test_compact_mode_lists_referenced_types(self):
        result = await get_resource_schema("Patient", include_nested=False)
        assert "_referenced_types" in result
        assert "HumanName" in result["_referenced_types"]

    @pytest.mark.asyncio
    async def test_nested_mode_includes_defs(self):
        result = await get_resource_schema("Patient", include_nested=True)
        assert "$defs" in result
        assert "HumanName" in result["$defs"]

    @pytest.mark.asyncio
    async def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="Unknown FHIR type"):
            await get_resource_schema("NonExistentType")

    @pytest.mark.asyncio
    async def test_data_type_works(self):
        result = await get_resource_schema("Observation")
        assert "properties" in result
        assert "code" in result["properties"]

    @pytest.mark.asyncio
    async def test_medplum_type_works(self):
        result = await get_resource_schema("Bot")
        assert "properties" in result


class TestReadOnlyEnforcement:
    """Test that write tools respect read-only mode."""

    @pytest.mark.asyncio
    async def test_create_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await create_resource({"resourceType": "Patient"})

    @pytest.mark.asyncio
    async def test_update_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await update_resource({"resourceType": "Patient", "id": "123"})

    @pytest.mark.asyncio
    async def test_conditional_create_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await create_resource_if_none_exist(
                {"resourceType": "Patient"},
                "identifier=http://example.org|123",
            )

    @pytest.mark.asyncio
    async def test_patch_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}):
            ops = [PatchOp(op="replace", path="/active", value=True)]
            with pytest.raises(PermissionError, match="read-only mode"):
                await patch_resource("Patient", "123", ops)

    @pytest.mark.asyncio
    async def test_delete_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await delete_resource("Patient", "123")

    @pytest.mark.asyncio
    async def test_execute_bot_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await execute_bot(
                "bot-123", {"resourceType": "Parameters", "parameter": []}
            )

    @pytest.mark.asyncio
    async def test_create_bot_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await create_bot("Test Bot")

    @pytest.mark.asyncio
    async def test_save_and_deploy_bot_blocked_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only mode"
        ):
            await save_and_deploy_bot("bot-123", "source", "compiled")

    @pytest.mark.asyncio
    async def test_execute_operation_blocks_unknown_ops(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), pytest.raises(
            PermissionError, match="read-only allowlist"
        ):
            await execute_operation("Patient", "some-write-op")

    @pytest.mark.asyncio
    async def test_execute_operation_allows_known_read_ops(self):
        """Known read-only ops should pass the read-only check, not PermissionError."""
        mock_client = AsyncMock()
        mock_client.execute_operation.return_value = {"resourceType": "Bundle"}

        @asynccontextmanager
        async def fake_obo(obo=None):
            yield mock_client

        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), patch.object(
            srv, "_with_obo", fake_obo
        ):
            result = await execute_operation(
                "Patient", "everything", resource_id="123", method="GET"
            )
            assert result["resourceType"] == "Bundle"

    @pytest.mark.asyncio
    async def test_batch_blocks_writes_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}):
            bundle = BundleInput(
                type="batch",
                entry=[{"request": {"method": "POST", "url": "Patient"}}],
            )
            with pytest.raises(PermissionError, match="read-only mode"):
                await execute_batch(bundle)

    @pytest.mark.asyncio
    async def test_batch_allows_gets_in_read_only(self):
        """GET-only batch should pass read-only check, not PermissionError."""
        mock_client = AsyncMock()
        mock_client.execute_batch.return_value = {"resourceType": "Bundle", "type": "batch-response"}

        @asynccontextmanager
        async def fake_obo(obo=None):
            yield mock_client

        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), patch.object(
            srv, "_with_obo", fake_obo
        ):
            bundle = BundleInput(
                type="batch",
                entry=[{"request": {"method": "GET", "url": "Patient/123"}}],
            )
            result = await execute_batch(bundle)
            assert result["type"] == "batch-response"

    @pytest.mark.asyncio
    async def test_transaction_allows_gets_in_read_only(self):
        """GET-only transaction should also pass read-only check."""
        mock_client = AsyncMock()
        mock_client.execute_transaction.return_value = {"resourceType": "Bundle", "type": "transaction-response"}

        @asynccontextmanager
        async def fake_obo(obo=None):
            yield mock_client

        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}), patch.object(
            srv, "_with_obo", fake_obo
        ):
            bundle = BundleInput(
                type="transaction",
                entry=[{"request": {"method": "GET", "url": "Patient/123"}}],
            )
            result = await execute_batch(bundle)
            assert result["type"] == "transaction-response"


class TestInputValidation:
    @pytest.mark.asyncio
    async def test_create_requires_resource_type(self):
        with pytest.raises(ValueError, match="resourceType"):
            await create_resource({"name": "test"})

    @pytest.mark.asyncio
    async def test_conditional_create_requires_resource_type(self):
        with pytest.raises(ValueError, match="resourceType"):
            await create_resource_if_none_exist({"name": "test"}, "identifier=123")

    @pytest.mark.asyncio
    async def test_update_requires_resource_type(self):
        with pytest.raises(ValueError, match="resourceType"):
            await update_resource({"id": "123"})

    @pytest.mark.asyncio
    async def test_update_requires_id(self):
        with pytest.raises(ValueError, match="'id' field"):
            await update_resource({"resourceType": "Patient"})

    @pytest.mark.asyncio
    async def test_patch_requires_operations(self):
        with pytest.raises(ValueError, match="At least one"):
            await patch_resource("Patient", "123", [])

    @pytest.mark.asyncio
    async def test_create_validates_resource_against_model(self):
        with pytest.raises(ValueError, match="FHIR Patient validation failed"):
            await create_resource({
                "resourceType": "Patient",
                "gender": "invalid",
            })

    @pytest.mark.asyncio
    async def test_update_validates_resource_against_model(self):
        with pytest.raises(ValueError, match="FHIR Patient validation failed"):
            await update_resource({
                "resourceType": "Patient",
                "id": "123",
                "gender": "invalid",
            })


class TestCrudToolsWithMockedClient:
    """Test CRUD tools with a mocked AsyncMedplumClient."""

    @pytest.fixture
    def mock_client(self):
        return AsyncMock()

    @pytest.fixture(autouse=True)
    def patch_with_obo(self, mock_client):
        @asynccontextmanager
        async def fake_obo(obo=None):
            yield mock_client

        with patch.object(srv, "_with_obo", fake_obo):
            yield

    @pytest.mark.asyncio
    async def test_read_resource(self, mock_client):
        mock_client.read_resource.return_value = {
            "resourceType": "Patient", "id": "123", "name": [{"family": "Smith"}]
        }
        result = await read_resource("Patient", "123")
        mock_client.read_resource.assert_awaited_once_with("Patient", "123")
        assert result["id"] == "123"
        assert result["_response_type"] == "Patient"

    @pytest.mark.asyncio
    async def test_search_one_found(self, mock_client):
        mock_client.search_one.return_value = {
            "resourceType": "Patient", "id": "456"
        }
        result = await search_one("Patient", {"family": "Smith"})
        assert result["id"] == "456"
        assert result["_response_type"] == "Patient"

    @pytest.mark.asyncio
    async def test_search_one_not_found(self, mock_client):
        mock_client.search_one.return_value = None
        result = await search_one("Patient", {"family": "Nobody"})
        assert result is None

    @pytest.mark.asyncio
    async def test_search_resources_empty_hint(self, mock_client):
        mock_client.search_with_options.return_value = {
            "resourceType": "Bundle", "type": "searchset", "total": 0, "entry": []
        }
        result = await search_resources("Patient", {"family": "Nobody"})
        assert "_hint" in result
        assert "get_resource_capabilities" in result["_hint"]

    @pytest.mark.asyncio
    async def test_search_resources_with_results(self, mock_client):
        mock_client.search_with_options.return_value = {
            "resourceType": "Bundle", "type": "searchset", "total": 1,
            "entry": [{"resource": {"resourceType": "Patient", "id": "1"}}]
        }
        result = await search_resources("Patient")
        assert "_hint" not in result
        assert result["_response_type"] == "Bundle"

    @pytest.mark.asyncio
    async def test_create_resource(self, mock_client):
        mock_client.create_resource.return_value = {
            "resourceType": "Patient", "id": "new-id"
        }
        result = await create_resource({"resourceType": "Patient"})
        assert result["id"] == "new-id"

    @pytest.mark.asyncio
    async def test_create_resource_if_none_exist(self, mock_client):
        mock_client.create_resource_if_none_exist.return_value = {
            "resourceType": "Patient", "id": "existing-or-new-id"
        }
        result = await create_resource_if_none_exist(
            {"resourceType": "Patient"},
            "identifier=http://example.org|123",
        )
        mock_client.create_resource_if_none_exist.assert_awaited_once_with(
            {"resourceType": "Patient"},
            "identifier=http://example.org|123",
        )
        assert result["id"] == "existing-or-new-id"

    @pytest.mark.asyncio
    async def test_update_resource_with_version_diff(self, mock_client):
        mock_client.update_resource.return_value = {
            "resourceType": "Patient", "id": "123",
            "meta": {"versionId": "2"}
        }
        result = await update_resource({
            "resourceType": "Patient", "id": "123",
            "meta": {"versionId": "1"}
        })
        assert result["_update_info"]["previous_version"] == "1"
        assert result["_update_info"]["new_version"] == "2"

    @pytest.mark.asyncio
    async def test_update_resource_no_version_change(self, mock_client):
        mock_client.update_resource.return_value = {
            "resourceType": "Patient", "id": "123",
            "meta": {"versionId": "1"}
        }
        result = await update_resource({
            "resourceType": "Patient", "id": "123",
            "meta": {"versionId": "1"}
        })
        assert "_update_info" not in result

    @pytest.mark.asyncio
    async def test_delete_resource(self, mock_client):
        mock_client.delete_resource.return_value = None
        result = await delete_resource("Patient", "123")
        assert result["status"] == "deleted"
        assert result["resourceType"] == "Patient"
        assert result["id"] == "123"

    @pytest.mark.asyncio
    async def test_patch_resource(self, mock_client):
        mock_client.patch_resource.return_value = {
            "resourceType": "Patient", "id": "123", "active": False
        }
        ops = [PatchOp(op="replace", path="/active", value=False)]
        result = await patch_resource("Patient", "123", ops)
        mock_client.patch_resource.assert_awaited_once_with(
            "Patient", "123", [{"op": "replace", "path": "/active", "value": False}]
        )
        assert result["active"] is False

    @pytest.mark.asyncio
    async def test_search_all_resources(self, mock_client):
        async def fake_pages(resource_type, params):
            assert resource_type == "Patient"
            assert params == {"family": "Smith"}
            yield {"resourceType": "Patient", "id": "1"}
            yield {"resourceType": "Patient", "id": "2"}

        mock_client.search_resource_pages = fake_pages
        result = await search_all_resources("Patient", {"family": "Smith"})
        assert result["resourceType"] == "Bundle"
        assert result["total"] == 2
        assert result["_resources_returned"] == 2
        assert result["entry"][0]["resource"]["id"] == "1"

    @pytest.mark.asyncio
    async def test_search_all_resources_empty_hint(self, mock_client):
        async def fake_pages(resource_type, params):
            if False:
                yield resource_type, params

        mock_client.search_resource_pages = fake_pages
        result = await search_all_resources("Patient", {"family": "Nobody"})
        assert result["total"] == 0
        assert "_hint" in result

    @pytest.mark.asyncio
    async def test_execute_bot(self, mock_client):
        mock_client.execute_bot.return_value = {
            "resourceType": "Parameters",
            "parameter": [{"name": "status", "valueString": "ok"}],
        }
        result = await execute_bot(
            "bot-123",
            {"resourceType": "Parameters", "parameter": []},
        )
        mock_client.execute_bot.assert_awaited_once_with(
            "bot-123",
            {"resourceType": "Parameters", "parameter": []},
            content_type="application/json",
        )
        assert result["resourceType"] == "Parameters"

    @pytest.mark.asyncio
    async def test_create_bot(self, mock_client):
        mock_client.create_bot.return_value = {
            "resourceType": "Bot",
            "id": "bot-123",
            "runtimeVersion": "awslambda",
        }
        result = await create_bot(
            "Test Bot",
            description="Desc",
            runtime_version="awslambda",
            additional_fields={"system": True},
        )
        mock_client.create_bot.assert_awaited_once_with(
            name="Test Bot",
            description="Desc",
            source_code="",
            runtime_version="awslambda",
            system=True,
        )
        assert result["id"] == "bot-123"

    @pytest.mark.asyncio
    async def test_save_and_deploy_bot(self, mock_client):
        mock_client.save_and_deploy_bot.return_value = (
            {"resourceType": "Bot", "id": "bot-123"},
            {"status": "deployed"},
        )
        result = await save_and_deploy_bot(
            "bot-123",
            "source",
            "compiled",
            filename="bundle.js",
        )
        mock_client.save_and_deploy_bot.assert_awaited_once_with(
            bot_id="bot-123",
            source_code="source",
            compiled_code="compiled",
            filename="bundle.js",
        )
        assert result["bot"]["id"] == "bot-123"
        assert result["deployment"]["status"] == "deployed"


class TestDirectClientTools:
    @pytest.mark.asyncio
    async def test_validate_codesystem_code(self):
        mock_client = AsyncMock()
        mock_client.validate_codesystem_code.return_value = {
            "resourceType": "Parameters",
            "parameter": [{"name": "result", "valueBoolean": True}],
        }
        with patch.object(srv, "_get_client", AsyncMock(return_value=mock_client)):
            result = await validate_codesystem_code(
                code="12345",
                codesystem_url="http://loinc.org",
            )
        mock_client.validate_codesystem_code.assert_awaited_once_with(
            codesystem_url="http://loinc.org",
            codesystem_id=None,
            code="12345",
            coding=None,
            version=None,
        )
        assert result["resourceType"] == "Parameters"

    @pytest.mark.asyncio
    async def test_export_ccda(self):
        mock_client = AsyncMock()

        @asynccontextmanager
        async def fake_obo(obo=None):
            yield mock_client

        mock_client.export_ccda.return_value = "<ClinicalDocument />"
        with patch.object(srv, "_with_obo", fake_obo):
            result = await export_ccda("patient-123")

        mock_client.export_ccda.assert_awaited_once_with("patient-123")
        assert result["contentType"] == "application/xml"
        assert result["patientId"] == "patient-123"
        assert result["data"] == "<ClinicalDocument />"
