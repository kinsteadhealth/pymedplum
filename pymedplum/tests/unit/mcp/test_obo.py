"""Tests for on-behalf-of edge cases and get_resource_capabilities path handling."""

import os
from unittest.mock import AsyncMock, patch

import pytest

from pymedplum.mcp.tools import (
    get_resource_capabilities,
    read_resource,
)


class TestWithOboEmptyString:
    @pytest.mark.asyncio
    async def test_empty_string_rejected(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            await read_resource("Patient", "123", on_behalf_of="")

    @pytest.mark.asyncio
    async def test_whitespace_only_rejected(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            await read_resource("Patient", "123", on_behalf_of="   ")


class TestObOOverrideLockdown:
    """Per-call ``on_behalf_of`` overrides are off by default; the autouse
    conftest fixture turns them on for the rest of the MCP suite. These
    tests opt back out to verify the lockdown.
    """

    @pytest.mark.asyncio
    async def test_per_call_obo_rejected_by_default(self, monkeypatch):
        monkeypatch.setenv("MEDPLUM_ALLOW_OBO_OVERRIDE", "false")
        with pytest.raises(PermissionError, match="MEDPLUM_ALLOW_OBO_OVERRIDE"):
            await read_resource(
                "Patient",
                "123",
                on_behalf_of="ProjectMembership/11111111-1111-1111-1111-111111111111",
            )

    @pytest.mark.asyncio
    async def test_no_obo_passthrough_when_override_disabled(self, monkeypatch):
        """Without an override, calls without on_behalf_of still flow through.

        The lockdown only blocks caller-supplied overrides; the server's
        startup OBO (env var) is unaffected.
        """
        from pymedplum.tests.unit.mcp.conftest import make_fake_obo

        monkeypatch.setenv("MEDPLUM_ALLOW_OBO_OVERRIDE", "false")
        mock_client = AsyncMock()
        mock_client.read_resource.return_value = {"resourceType": "Patient", "id": "1"}
        with patch(
            "pymedplum.mcp.tools._with_obo", make_fake_obo(mock_client)
        ):
            result = await read_resource("Patient", "1")
        assert result["resourceType"] == "Patient"


class TestGetCapabilitiesPathNormalization:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "env_path,expected",
        [
            ("fhir/R4/", "fhir/R4/metadata"),
            ("fhir/R4", "fhir/R4/metadata"),
            ("/fhir/R4/", "fhir/R4/metadata"),
            ("/fhir/R4", "fhir/R4/metadata"),
        ],
    )
    async def test_path_normalized(self, env_path, expected):
        mock_client = AsyncMock()
        mock_client.get.return_value = {"resourceType": "CapabilityStatement"}
        with (
            patch.dict(os.environ, {"MEDPLUM_FHIR_URL_PATH": env_path}),
            patch(
                "pymedplum.mcp.tools._get_client",
                AsyncMock(return_value=mock_client),
            ),
        ):
            await get_resource_capabilities()
        mock_client.get.assert_awaited_once_with(expected)

    @pytest.mark.asyncio
    async def test_filters_by_resource_type(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = {
            "resourceType": "CapabilityStatement",
            "rest": [
                {
                    "mode": "server",
                    "resource": [
                        {
                            "type": "Patient",
                            "searchParam": [{"name": "family"}],
                        },
                        {"type": "Observation"},
                    ],
                }
            ],
        }
        with patch(
            "pymedplum.mcp.tools._get_client",
            AsyncMock(return_value=mock_client),
        ):
            result = await get_resource_capabilities("Patient")
        assert result["type"] == "Patient"
        assert result["searchParam"][0]["name"] == "family"

    @pytest.mark.asyncio
    async def test_unknown_resource_type_raises(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = {
            "resourceType": "CapabilityStatement",
            "rest": [{"mode": "server", "resource": [{"type": "Patient"}]}],
        }
        with (
            patch(
                "pymedplum.mcp.tools._get_client",
                AsyncMock(return_value=mock_client),
            ),
            pytest.raises(ValueError, match="not found in CapabilityStatement"),
        ):
            await get_resource_capabilities("NonExistentType")
