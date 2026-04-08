"""Tests for write tool functions (create, update, patch, delete)."""

import os
from unittest.mock import AsyncMock, patch

import pytest

from pymedplum.mcp.server import (
    PatchOp,
    create_resource,
    create_resource_if_none_exist,
    delete_resource,
    patch_resource,
    update_resource,
)
from pymedplum.tests.unit.mcp.conftest import make_fake_obo


class TestCreateResource:
    @pytest.mark.asyncio
    async def test_creates_and_annotates(self):
        mock = AsyncMock()
        mock.create_resource.return_value = {
            "resourceType": "Patient",
            "id": "new-1",
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await create_resource(
                {"resourceType": "Patient", "name": [{"family": "Test"}]}
            )
        assert result["id"] == "new-1"
        assert result["_response_type"] == "Patient"

    @pytest.mark.asyncio
    async def test_missing_resource_type(self):
        with pytest.raises(ValueError, match="resourceType"):
            await create_resource({"name": "test"})

    @pytest.mark.asyncio
    async def test_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            pytest.raises(PermissionError, match="read-only mode"),
        ):
            await create_resource({"resourceType": "Patient"})

    @pytest.mark.asyncio
    async def test_validates_resource(self):
        with pytest.raises(ValueError, match="FHIR Patient validation"):
            await create_resource({"resourceType": "Patient", "gender": "invalid"})


class TestCreateResourceIfNoneExist:
    @pytest.mark.asyncio
    async def test_creates(self):
        mock = AsyncMock()
        mock.create_resource_if_none_exist.return_value = {
            "resourceType": "Patient",
            "id": "existing-1",
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await create_resource_if_none_exist(
                {"resourceType": "Patient", "name": [{"family": "Test"}]},
                "identifier=http://example.org|12345",
            )
        assert result["id"] == "existing-1"

    @pytest.mark.asyncio
    async def test_missing_resource_type(self):
        with pytest.raises(ValueError, match="resourceType"):
            await create_resource_if_none_exist({"name": "x"}, "id=1")


class TestUpdateResource:
    @pytest.mark.asyncio
    async def test_updates(self):
        mock = AsyncMock()
        mock.update_resource.return_value = {
            "resourceType": "Patient",
            "id": "123",
            "meta": {"versionId": "2"},
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await update_resource(
                {
                    "resourceType": "Patient",
                    "id": "123",
                    "meta": {"versionId": "1"},
                }
            )
        assert result["_update_info"]["previous_version"] == "1"
        assert result["_update_info"]["new_version"] == "2"

    @pytest.mark.asyncio
    async def test_missing_resource_type(self):
        with pytest.raises(ValueError, match="resourceType"):
            await update_resource({"id": "123"})

    @pytest.mark.asyncio
    async def test_missing_id(self):
        with pytest.raises(ValueError, match="'id' field"):
            await update_resource({"resourceType": "Patient"})

    @pytest.mark.asyncio
    async def test_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            pytest.raises(PermissionError),
        ):
            await update_resource({"resourceType": "Patient", "id": "1"})


class TestPatchResource:
    @pytest.mark.asyncio
    async def test_patches(self):
        mock = AsyncMock()
        mock.patch_resource.return_value = {
            "resourceType": "Patient",
            "id": "123",
            "active": False,
        }
        ops = [PatchOp(op="replace", path="/active", value=False)]
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await patch_resource("Patient", "123", ops)
        mock.patch_resource.assert_awaited_once_with(
            "Patient", "123", [{"op": "replace", "path": "/active", "value": False}]
        )
        assert result["active"] is False

    @pytest.mark.asyncio
    async def test_empty_ops_rejected(self):
        with pytest.raises(ValueError, match="At least one"):
            await patch_resource("Patient", "123", [])

    @pytest.mark.asyncio
    async def test_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            pytest.raises(PermissionError),
        ):
            ops = [PatchOp(op="replace", path="/active", value=True)]
            await patch_resource("Patient", "123", ops)


class TestDeleteResource:
    @pytest.mark.asyncio
    async def test_deletes(self):
        mock = AsyncMock()
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await delete_resource("Patient", "123")
        mock.delete_resource.assert_awaited_once_with("Patient", "123")
        assert result == {
            "status": "deleted",
            "resourceType": "Patient",
            "id": "123",
        }

    @pytest.mark.asyncio
    async def test_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            pytest.raises(PermissionError),
        ):
            await delete_resource("Patient", "123")
