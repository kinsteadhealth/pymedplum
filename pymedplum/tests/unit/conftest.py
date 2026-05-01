"""Shared fixtures for unit tests."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest
from respx import MockRouter

from pymedplum.client import MedplumClient


_BASE_URL = "https://api.medplum.com/"


@pytest.fixture
def sync_client() -> Iterator[MedplumClient]:
    """Sync MedplumClient with a static access token (no OAuth roundtrip)."""
    client = MedplumClient(base_url=_BASE_URL, access_token="tkn")
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def membership_factory() -> Any:
    """Build a ProjectMembership dict with predictable shape."""

    def _make(
        membership_id: str = "abc",
        version_id: str = "1",
        access: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return {
            "resourceType": "ProjectMembership",
            "id": membership_id,
            "meta": {"versionId": version_id},
            "project": {"reference": "Project/p1"},
            "user": {"reference": "User/u1"},
            "profile": {"reference": "Practitioner/pr1"},
            "access": access or [],
        }

    return _make


@pytest.fixture
def mock_membership_endpoints(respx_mock: MockRouter) -> Any:
    """Helper to register GET / PUT mocks for a membership."""

    def _mock(
        membership: dict[str, Any],
        *,
        next_version: str = "2",
        put_status: int = 200,
        put_body: dict[str, Any] | None = None,
    ) -> tuple[Any, Any]:
        membership_id = membership["id"]
        get_route = respx_mock.get(
            f"{_BASE_URL}fhir/R4/ProjectMembership/{membership_id}"
        ).mock(return_value=httpx.Response(200, json=membership))
        if put_body is None:
            put_body = {**membership, "meta": {"versionId": next_version}}
        put_route = respx_mock.put(
            f"{_BASE_URL}fhir/R4/ProjectMembership/{membership_id}"
        ).mock(return_value=httpx.Response(put_status, json=put_body))
        return get_route, put_route

    return _mock
