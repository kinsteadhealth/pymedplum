"""Tests for read/search tool functions."""

from unittest.mock import AsyncMock, patch

import pytest

from pymedplum.mcp.tools import (
    get_resource_schema,
    read_resource,
    search_all_resources,
    search_one,
    search_resources,
)
from pymedplum.tests.unit.mcp.conftest import make_fake_obo


class TestGetResourceSchema:
    @pytest.mark.asyncio
    async def test_known_type_returns_schema(self):
        schema = await get_resource_schema("Patient")
        assert "properties" in schema
        assert "_referenced_types" in schema

    @pytest.mark.asyncio
    async def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="Unknown FHIR type"):
            await get_resource_schema("NotARealType")

    @pytest.mark.asyncio
    async def test_include_nested(self):
        schema = await get_resource_schema("Patient", include_nested=True)
        assert "$defs" in schema
        assert "_referenced_types" not in schema

    @pytest.mark.asyncio
    async def test_compact_strips_defs(self):
        schema = await get_resource_schema("Patient", include_nested=False)
        assert "$defs" not in schema


class TestReadResource:
    @pytest.mark.asyncio
    async def test_returns_annotated(self):
        mock = AsyncMock()
        mock.read_resource.return_value = {
            "resourceType": "Patient",
            "id": "123",
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await read_resource("Patient", "123")
        mock.read_resource.assert_awaited_once_with("Patient", "123")
        assert result["_response_type"] == "Patient"


class TestSearchResources:
    @pytest.mark.asyncio
    async def test_returns_bundle(self):
        mock = AsyncMock()
        mock.search_with_options.return_value = {
            "resourceType": "Bundle",
            "total": 1,
            "entry": [{"resource": {"resourceType": "Patient"}}],
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_resources("Patient", {"family": "Smith"})
        assert result["total"] == 1

    @pytest.mark.asyncio
    async def test_zero_results_adds_hint(self):
        mock = AsyncMock()
        mock.search_with_options.return_value = {
            "resourceType": "Bundle",
            "total": 0,
            "entry": [],
        }
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_resources("Observation")
        assert "_hint" in result
        assert "get_resource_capabilities" in result["_hint"]


class TestSearchOne:
    @pytest.mark.asyncio
    async def test_found(self):
        mock = AsyncMock()
        mock.search_one.return_value = {"resourceType": "Patient", "id": "1"}
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_one("Patient", {"identifier": "12345"})
        assert result["id"] == "1"
        assert result["_response_type"] == "Patient"

    @pytest.mark.asyncio
    async def test_not_found(self):
        mock = AsyncMock()
        mock.search_one.return_value = None
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_one("Patient", {"identifier": "nope"})
        assert result is None


class TestSearchAllResources:
    @pytest.mark.asyncio
    async def test_collects_all_pages(self):
        mock = AsyncMock()

        async def fake_pages(rt, params):
            for r in [
                {"resourceType": "Patient", "id": "1"},
                {"resourceType": "Patient", "id": "2"},
            ]:
                yield r

        mock.search_resource_pages = fake_pages
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_all_resources("Patient")
        assert result["total"] == 2
        assert result["_pages_mode"] == "all"

    @pytest.mark.asyncio
    async def test_truncates_at_max(self):
        mock = AsyncMock()

        async def fake_pages(rt, params):
            for i in range(100):
                yield {"resourceType": "Patient", "id": str(i)}

        mock.search_resource_pages = fake_pages
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_all_resources("Patient", max_resources=5)
        assert result["total"] == 5
        assert result["_truncated"] is True
        assert "truncated at 5" in result["_warning"]

    @pytest.mark.asyncio
    async def test_no_truncation_under_max(self):
        mock = AsyncMock()

        async def fake_pages(rt, params):
            for i in range(3):
                yield {"resourceType": "Patient", "id": str(i)}

        mock.search_resource_pages = fake_pages
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_all_resources("Patient", max_resources=10)
        assert result["total"] == 3
        assert "_truncated" not in result
        assert "_warning" not in result

    @pytest.mark.asyncio
    async def test_empty_adds_hint(self):
        mock = AsyncMock()

        async def fake_pages(rt, params):
            return
            yield  # make it an async generator

        mock.search_resource_pages = fake_pages
        with patch("pymedplum.mcp.tools._with_obo", make_fake_obo(mock)):
            result = await search_all_resources("Observation", {"code": "x"})
        assert result["total"] == 0
        assert "_hint" in result
