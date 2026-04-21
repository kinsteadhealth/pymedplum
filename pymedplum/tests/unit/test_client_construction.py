"""Tests for MedplumClient / AsyncMedplumClient constructor contracts.

Phase 6 makes the constructor signature explicit and keyword-only,
removes ``**kwargs``, and enforces transport invariants at construction:

- unknown kwargs raise TypeError
- caller-supplied ``http_client`` must have ``follow_redirects=False``
- internally-constructed clients disable redirects
- ``base_url`` is validated and normalized up front
"""

from __future__ import annotations

import httpx
import pytest

from pymedplum import AsyncMedplumClient, MedplumClient
from pymedplum.exceptions import InsecureTransportError


def test_unknown_kwarg_raises_type_error_sync() -> None:
    with pytest.raises(TypeError):
        MedplumClient(not_a_real_param="oops")  # type: ignore[call-arg]


def test_unknown_kwarg_raises_type_error_async() -> None:
    with pytest.raises(TypeError):
        AsyncMedplumClient(not_a_real_param="oops")  # type: ignore[call-arg]


def test_caller_supplied_http_client_requires_follow_redirects_false_sync() -> None:
    http = httpx.Client(follow_redirects=True)
    try:
        with pytest.raises(ValueError, match="follow_redirects"):
            MedplumClient(http_client=http)
    finally:
        http.close()


@pytest.mark.asyncio
async def test_caller_supplied_http_client_requires_follow_redirects_false_async() -> (
    None
):
    http = httpx.AsyncClient(follow_redirects=True)
    try:
        with pytest.raises(ValueError, match="follow_redirects"):
            AsyncMedplumClient(http_client=http)
    finally:
        await http.aclose()


def test_caller_supplied_http_client_accepted_when_follow_redirects_false_sync() -> (
    None
):
    http = httpx.Client(follow_redirects=False)
    client = MedplumClient(http_client=http)
    try:
        assert client._http is http
        assert client._http.follow_redirects is False
    finally:
        client.close()


@pytest.mark.asyncio
async def test_caller_supplied_http_client_accepted_when_follow_redirects_false_async() -> (
    None
):
    http = httpx.AsyncClient(follow_redirects=False)
    client = AsyncMedplumClient(http_client=http)
    try:
        assert client._http is http
        assert client._http.follow_redirects is False
    finally:
        await client.aclose()


def test_internal_http_client_disables_redirects_sync() -> None:
    client = MedplumClient()
    try:
        assert client._http.follow_redirects is False
    finally:
        client.close()


@pytest.mark.asyncio
async def test_internal_http_client_disables_redirects_async() -> None:
    client = AsyncMedplumClient()
    try:
        assert client._http.follow_redirects is False
    finally:
        await client.aclose()


def test_base_url_validated_at_construction_sync() -> None:
    with pytest.raises(InsecureTransportError):
        MedplumClient(base_url="http://api.medplum.com/")


def test_base_url_validated_at_construction_async() -> None:
    with pytest.raises(InsecureTransportError):
        AsyncMedplumClient(base_url="http://api.medplum.com/")


def test_base_url_normalized_at_construction_sync() -> None:
    client = MedplumClient(base_url="https://API.medplum.com")
    try:
        assert client.base_url == "https://api.medplum.com/"
    finally:
        client.close()


@pytest.mark.asyncio
async def test_base_url_normalized_at_construction_async() -> None:
    client = AsyncMedplumClient(base_url="https://API.medplum.com")
    try:
        assert client.base_url == "https://api.medplum.com/"
    finally:
        await client.aclose()


def test_allow_insecure_http_permits_non_loopback_http_sync() -> None:
    client = MedplumClient(base_url="http://api.medplum.com/", allow_insecure_http=True)
    try:
        assert client.base_url == "http://api.medplum.com/"
    finally:
        client.close()
