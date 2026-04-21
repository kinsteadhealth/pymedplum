"""Shared fixtures for MCP server tests."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest


@pytest.fixture(autouse=True)
def enable_writes_and_obo_override(monkeypatch):
    """Enable write tools and per-call OBO overrides for MCP tests by default.

    The MCP server now defaults to read-only and rejects per-call ``on_behalf_of``;
    tests that want to exercise the gating opt back in by ``monkeypatch.delenv``
    or by setting their own values via ``patch.dict(os.environ, ...)``.
    """
    monkeypatch.setenv("MEDPLUM_ENABLE_WRITES", "true")
    monkeypatch.setenv("MEDPLUM_ALLOW_OBO_OVERRIDE", "true")


@pytest.fixture
def mock_client():
    """A mock AsyncMedplumClient with common return values."""
    client = AsyncMock()
    client.base_url = "https://api.medplum.com/"
    return client


@asynccontextmanager
async def fake_obo(obo=None):
    """Yields a mock client — use with patch on _with_obo."""
    client = AsyncMock()
    client.base_url = "https://api.medplum.com/"
    yield client


def make_fake_obo(mock_client):
    """Create a fake_obo that yields a specific mock client."""

    @asynccontextmanager
    async def _fake(obo=None):
        yield mock_client

    return _fake
