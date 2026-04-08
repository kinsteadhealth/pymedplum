"""Shared fixtures for MCP server tests."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest


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
