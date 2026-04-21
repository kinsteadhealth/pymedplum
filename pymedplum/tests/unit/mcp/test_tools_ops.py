"""Tests for operations, GraphQL, batch, patient, and terminology tools."""

import os
from unittest.mock import AsyncMock, patch

import pytest

from pymedplum.mcp.server import BundleInput
from pymedplum.mcp.tools import (
    execute_batch,
    execute_bot,
    execute_graphql,
    execute_operation,
    expand_valueset,
    get_patient_everything,
    lookup_concept,
    translate_concept,
    validate_code,
    validate_codesystem_code,
)
from pymedplum.tests.unit.mcp.conftest import make_fake_obo


class TestExecuteOperation:
    @pytest.mark.asyncio
    async def test_blocks_unknown_ops_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            pytest.raises(PermissionError, match="read-only allowlist"),
        ):
            await execute_operation("Patient", "some-write-op")

    @pytest.mark.asyncio
    async def test_allows_known_read_ops(self):
        mock = AsyncMock()
        mock.execute_operation.return_value = {"resourceType": "Bundle"}
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)),
        ):
            result = await execute_operation(
                "Patient", "everything", resource_id="123", method="GET"
            )
            assert result["resourceType"] == "Bundle"


class TestExecuteGraphQL:
    """GraphQL is treated as a write-capable tool because query text is
    unstructured. In read-only mode (the default), the entire tool is
    blocked rather than relying on a regex/parser to decide intent.
    """

    @pytest.mark.asyncio
    async def test_query_blocked_entirely_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            pytest.raises(PermissionError, match="read-only mode"),
        ):
            await execute_graphql('{ Patient(id: "1") { id } }')

    @pytest.mark.asyncio
    async def test_mutation_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            pytest.raises(PermissionError, match="read-only mode"),
        ):
            await execute_graphql("mutation { PatientCreate(resource: {}) { id } }")

    @pytest.mark.asyncio
    async def test_executes_when_writes_enabled(self):
        mock = AsyncMock()
        mock.execute_graphql.return_value = {"data": {"Patient": {"id": "1"}}}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await execute_graphql('{ Patient(id: "1") { id } }')
            assert result["data"]["Patient"]["id"] == "1"


class TestExecuteBatch:
    @pytest.mark.asyncio
    async def test_blocks_writes_in_read_only(self):
        with patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}):
            bundle = BundleInput(
                type="batch",
                entry=[{"request": {"method": "POST", "url": "Patient"}}],
            )
            with pytest.raises(PermissionError, match="read-only mode"):
                await execute_batch(bundle)

    @pytest.mark.asyncio
    async def test_allows_gets_in_read_only(self):
        mock = AsyncMock()
        mock.execute_batch.return_value = {
            "resourceType": "Bundle",
            "type": "batch-response",
        }
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)),
        ):
            bundle = BundleInput(
                type="batch",
                entry=[{"request": {"method": "GET", "url": "Patient/123"}}],
            )
            result = await execute_batch(bundle)
            assert result["type"] == "batch-response"

    @pytest.mark.asyncio
    async def test_transaction_uses_execute_transaction(self):
        mock = AsyncMock()
        mock.execute_transaction.return_value = {
            "resourceType": "Bundle",
            "type": "transaction-response",
        }
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)),
        ):
            bundle = BundleInput(
                type="transaction",
                entry=[{"request": {"method": "GET", "url": "Patient/123"}}],
            )
            result = await execute_batch(bundle)
            mock.execute_transaction.assert_awaited_once()
            assert result["type"] == "transaction-response"


class TestGetPatientEverything:
    @pytest.mark.asyncio
    async def test_returns_summary(self):
        mock = AsyncMock()
        mock.execute_operation.return_value = {
            "resourceType": "Bundle",
            "entry": [
                {"resource": {"resourceType": "Patient", "id": "1"}},
                {"resource": {"resourceType": "Observation", "id": "2"}},
                {"resource": {"resourceType": "Observation", "id": "3"}},
            ],
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await get_patient_everything("patient-1")
        assert result["_total_resources"] == 3
        assert result["_resource_summary"]["Observation"] == 2
        assert result["_resource_summary"]["Patient"] == 1


class TestTerminologyTools:
    @pytest.mark.asyncio
    async def test_validate_code(self):
        mock = AsyncMock()
        mock.validate_valueset_code.return_value = {
            "resourceType": "Parameters",
            "parameter": [{"name": "result", "valueBoolean": True}],
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await validate_code(
                code="12345",
                system="http://loinc.org",
            )
        assert result["resourceType"] == "Parameters"

    @pytest.mark.asyncio
    async def test_validate_codesystem_code(self):
        mock = AsyncMock()
        mock.validate_codesystem_code.return_value = {
            "resourceType": "Parameters",
            "parameter": [{"name": "result", "valueBoolean": True}],
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await validate_codesystem_code(
                code="12345",
                codesystem_url="http://loinc.org",
            )
        assert result["resourceType"] == "Parameters"

    @pytest.mark.asyncio
    async def test_expand_valueset(self):
        mock = AsyncMock()
        mock.expand_valueset.return_value = {"resourceType": "ValueSet"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await expand_valueset(valueset_url="http://example.org/vs")
        assert result["resourceType"] == "ValueSet"

    @pytest.mark.asyncio
    async def test_lookup_concept(self):
        mock = AsyncMock()
        mock.lookup_concept.return_value = {"resourceType": "Parameters"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await lookup_concept(code="12345", system="http://loinc.org")
        assert result["resourceType"] == "Parameters"

    @pytest.mark.asyncio
    async def test_translate_concept(self):
        mock = AsyncMock()
        mock.translate_concept.return_value = {"resourceType": "Parameters"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await translate_concept(
                code="12345", system="http://snomed.info/sct"
            )
        assert result["resourceType"] == "Parameters"


class TestBotTools:
    @pytest.mark.asyncio
    async def test_execute_bot(self):
        mock = AsyncMock()
        mock.execute_bot.return_value = {"result": "ok"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await execute_bot("bot-1", {"data": "test"})
        mock.execute_bot.assert_awaited_once_with(
            "bot-1", {"data": "test"}, content_type="application/json"
        )
        assert result["result"] == "ok"

    @pytest.mark.asyncio
    async def test_execute_bot_blocked_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_ENABLE_WRITES": "false"}),
            pytest.raises(PermissionError),
        ):
            await execute_bot("bot-1", {"data": "test"})

    @pytest.mark.asyncio
    async def test_execute_bot_blocked_when_not_in_allowlist(self):
        """Even with writes enabled, a bot not in MEDPLUM_ALLOWED_BOT_IDS is rejected."""
        with (
            patch.dict(
                os.environ,
                {"MEDPLUM_ALLOWED_BOT_IDS": "allowed-bot-1,allowed-bot-2"},
            ),
            pytest.raises(PermissionError, match="MEDPLUM_ALLOWED_BOT_IDS"),
        ):
            await execute_bot("forbidden-bot", {"data": "test"})

    @pytest.mark.asyncio
    async def test_execute_bot_allowed_when_in_allowlist(self):
        mock = AsyncMock()
        mock.execute_bot.return_value = {"result": "ok"}
        with (
            patch.dict(
                os.environ,
                {"MEDPLUM_ALLOWED_BOT_IDS": "allowed-bot-1,allowed-bot-2"},
            ),
            patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)),
        ):
            result = await execute_bot("allowed-bot-1", {"data": "test"})
        assert result["result"] == "ok"

    @pytest.mark.asyncio
    async def test_execute_bot_unrestricted_when_allowlist_unset(self):
        """No allowlist means any bot is callable (write-enabled mode)."""
        mock = AsyncMock()
        mock.execute_bot.return_value = {"result": "ok"}
        # The autouse conftest fixture enables writes; ensure the
        # allowlist env var is truly unset for this test.
        with (
            patch.dict(os.environ, {}, clear=False),
            patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)),
        ):
            os.environ.pop("MEDPLUM_ALLOWED_BOT_IDS", None)
            result = await execute_bot("any-bot-id", {"data": "test"})
        assert result["result"] == "ok"

    @pytest.mark.asyncio
    async def test_create_bot_collision(self):
        from pymedplum.mcp.tools import create_bot

        with pytest.raises(ValueError, match="additional_fields cannot override"):
            await create_bot("Test", additional_fields={"name": "Other"})

    @pytest.mark.asyncio
    async def test_create_bot_allows_extras(self):
        from pymedplum.mcp.tools import create_bot

        mock = AsyncMock()
        mock.create_bot.return_value = {"resourceType": "Bot", "id": "b1"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await create_bot(
                "Test Bot", additional_fields={"category": [{"text": "foo"}]}
            )
        assert result["id"] == "b1"

    @pytest.mark.asyncio
    async def test_save_and_deploy_bot(self):
        from pymedplum.mcp.tools import save_and_deploy_bot

        mock = AsyncMock()
        mock.save_and_deploy_bot.return_value = (
            {"resourceType": "Bot", "id": "b1"},
            {"status": "deployed"},
        )
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await save_and_deploy_bot("b1", "src", "compiled")
        assert result["bot"]["id"] == "b1"
        assert result["deployment"]["status"] == "deployed"
