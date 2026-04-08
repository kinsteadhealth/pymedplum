"""Tests for raw_request escape hatch."""

import os
from unittest.mock import AsyncMock, patch

import pytest

from pymedplum.mcp.server import raw_request
from pymedplum.tests.unit.mcp.conftest import make_fake_obo


class TestRawRequest:
    @pytest.mark.asyncio
    async def test_get(self):
        mock = AsyncMock()
        mock.base_url = "https://api.medplum.com/"
        mock._request.return_value = {"resourceType": "Patient", "id": "1"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await raw_request("GET", "fhir/R4/Patient/1")
        mock._request.assert_awaited_once_with(
            "GET", "https://api.medplum.com/fhir/R4/Patient/1"
        )
        assert result["id"] == "1"

    @pytest.mark.asyncio
    async def test_post_with_body_and_params(self):
        mock = AsyncMock()
        mock.base_url = "https://api.medplum.com/"
        mock._request.return_value = {"ok": True}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await raw_request(
                "POST",
                "admin/projects/123/invite",
                body={"email": "a@b.com"},
                query_params=[["notify", "true"]],
            )
        call_args = mock._request.await_args
        assert call_args[0] == (
            "POST",
            "https://api.medplum.com/admin/projects/123/invite",
        )
        assert call_args[1]["json"] == {"email": "a@b.com"}
        assert call_args[1]["params"] == [("notify", "true")]
        assert result["ok"] is True

    @pytest.mark.asyncio
    async def test_write_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            pytest.raises(PermissionError, match="read-only mode"),
        ):
            await raw_request(
                "POST", "fhir/R4/Patient", body={"resourceType": "Patient"}
            )

    @pytest.mark.asyncio
    async def test_delete_blocked_in_read_only(self):
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            pytest.raises(PermissionError),
        ):
            await raw_request("DELETE", "fhir/R4/Patient/1")

    @pytest.mark.asyncio
    async def test_get_allowed_in_read_only(self):
        mock = AsyncMock()
        mock.base_url = "https://api.medplum.com/"
        mock._request.return_value = {"data": "ok"}
        with (
            patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}),
            patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)),
        ):
            result = await raw_request("GET", "auth/me")
        assert result["data"] == "ok"

    @pytest.mark.asyncio
    async def test_none_response_returns_empty_dict(self):
        mock = AsyncMock()
        mock.base_url = "https://api.medplum.com/"
        mock._request.return_value = None
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await raw_request("GET", "fhir/R4/Patient/x")
        assert result == {}

    @pytest.mark.asyncio
    async def test_falsy_response_preserved(self):
        mock = AsyncMock()
        mock.base_url = "https://api.medplum.com/"
        mock._request.return_value = []
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await raw_request("GET", "some/endpoint")
        assert result == []

    @pytest.mark.asyncio
    async def test_repeated_query_params(self):
        mock = AsyncMock()
        mock.base_url = "https://api.medplum.com/"
        mock._request.return_value = {"resourceType": "Bundle"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            await raw_request(
                "GET",
                "fhir/R4/Observation",
                query_params=[
                    ["_include", "Observation:subject"],
                    ["_include", "Observation:performer"],
                    ["status", "active"],
                ],
            )
        call_args = mock._request.await_args
        assert call_args[1]["params"] == [
            ("_include", "Observation:subject"),
            ("_include", "Observation:performer"),
            ("status", "active"),
        ]
