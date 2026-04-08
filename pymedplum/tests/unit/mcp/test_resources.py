"""Tests for MCP resource handlers."""

import os
from unittest.mock import patch

import pytest

from pymedplum.mcp.resources import common_errors, server_info, tool_guide


class TestServerInfo:
    @pytest.mark.asyncio
    async def test_default_values(self):
        info = await server_info()
        assert info["base_url"] == "https://api.medplum.com/"
        assert info["read_only"] is False
        assert "description" in info

    @pytest.mark.asyncio
    async def test_read_only_reflected(self):
        with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": "true"}):
            info = await server_info()
        assert info["read_only"] is True

    @pytest.mark.asyncio
    async def test_custom_base_url(self):
        with patch.dict(os.environ, {"MEDPLUM_BASE_URL": "https://custom.com/"}):
            info = await server_info()
        assert info["base_url"] == "https://custom.com/"

    @pytest.mark.asyncio
    async def test_obo_included_when_set(self):
        with patch.dict(
            os.environ,
            {"MEDPLUM_ON_BEHALF_OF": "ProjectMembership/abc-123"},
        ):
            info = await server_info()
        assert info["default_on_behalf_of"] == "ProjectMembership/abc-123"

    @pytest.mark.asyncio
    async def test_obo_absent_when_unset(self):
        info = await server_info()
        assert "default_on_behalf_of" not in info


class TestToolGuide:
    @pytest.mark.asyncio
    async def test_returns_string(self):
        guide = await tool_guide()
        assert isinstance(guide, str)
        assert "read_resource" in guide
        assert "search_resources" in guide
        assert "create_resource_if_none_exist" in guide
        assert "raw_request" in guide


class TestCommonErrors:
    @pytest.mark.asyncio
    async def test_returns_dict(self):
        errors = await common_errors()
        assert isinstance(errors, dict)
        assert "400 Bad Request" in errors
        assert "404 Not Found" in errors
        assert "429 Too Many Requests" in errors

    @pytest.mark.asyncio
    async def test_all_values_are_strings(self):
        errors = await common_errors()
        for k, v in errors.items():
            assert isinstance(k, str)
            assert isinstance(v, str)
