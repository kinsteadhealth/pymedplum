"""Defenses against accidental disclosure of OAuth credentials.

Covers:
- ``__repr__`` on the client and the token managers omits secrets.
- ``download_binary(max_bytes=...)`` rejects oversized payloads on
  Content-Length and on actual byte count.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from pymedplum import AsyncMedplumClient, MedplumClient
from pymedplum._auth import AsyncTokenManager, TokenManager


def test_client_repr_omits_secrets() -> None:
    client = MedplumClient(
        client_id="public-client-id",
        client_secret="THIS-IS-A-SECRET",
        access_token="THIS-IS-A-TOKEN",
    )
    try:
        rendered = repr(client)
        assert "THIS-IS-A-SECRET" not in rendered
        assert "THIS-IS-A-TOKEN" not in rendered
        # Operationally useful fields are still present
        assert "public-client-id" in rendered
        assert "https://api.medplum.com/" in rendered
        assert "authenticated=True" in rendered
    finally:
        client.close()


def test_async_client_repr_omits_secrets() -> None:
    client = AsyncMedplumClient(
        client_id="public-client-id",
        client_secret="THIS-IS-A-SECRET",
        access_token="THIS-IS-A-TOKEN",
    )
    rendered = repr(client)
    assert "THIS-IS-A-SECRET" not in rendered
    assert "THIS-IS-A-TOKEN" not in rendered
    assert "public-client-id" in rendered


def test_token_manager_repr_omits_secrets() -> None:
    tm = TokenManager(
        client_id="public-client-id",
        client_secret="THIS-IS-A-SECRET",
        access_token="THIS-IS-A-TOKEN",
        token_url="https://api.medplum.com/oauth2/token",
    )
    rendered = repr(tm)
    assert "THIS-IS-A-SECRET" not in rendered
    assert "THIS-IS-A-TOKEN" not in rendered
    assert "public-client-id" in rendered


def test_async_token_manager_repr_omits_secrets() -> None:
    tm = AsyncTokenManager(
        client_id="public-client-id",
        client_secret="THIS-IS-A-SECRET",
        access_token="THIS-IS-A-TOKEN",
        token_url="https://api.medplum.com/oauth2/token",
    )
    rendered = repr(tm)
    assert "THIS-IS-A-SECRET" not in rendered
    assert "THIS-IS-A-TOKEN" not in rendered


def test_download_binary_rejects_advertised_oversize(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/abc").mock(
        return_value=httpx.Response(
            200,
            content=b"x" * 100,
            headers={"Content-Length": "9999999"},
        )
    )
    client = MedplumClient(access_token="t")
    try:
        with pytest.raises(ValueError, match="exceeding max_bytes=1024"):
            client.download_binary("abc", max_bytes=1024)
    finally:
        client.close()


def test_download_binary_rejects_actual_oversize_when_no_content_length(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/abc").mock(
        return_value=httpx.Response(200, content=b"x" * 5000)
    )
    client = MedplumClient(access_token="t")
    try:
        with pytest.raises(ValueError, match="exceeding max_bytes=1024"):
            client.download_binary("abc", max_bytes=1024)
    finally:
        client.close()


def test_download_binary_returns_payload_within_cap(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/abc").mock(
        return_value=httpx.Response(200, content=b"hello")
    )
    client = MedplumClient(access_token="t")
    try:
        out = client.download_binary("abc", max_bytes=1024)
        assert out == b"hello"
    finally:
        client.close()


def test_download_binary_unbounded_when_no_cap(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/abc").mock(
        return_value=httpx.Response(200, content=b"x" * 50_000)
    )
    client = MedplumClient(access_token="t")
    try:
        out = client.download_binary("abc")
        assert len(out) == 50_000
    finally:
        client.close()


@pytest.mark.asyncio
async def test_async_download_binary_rejects_oversize(
    respx_mock: respx.MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Binary/abc").mock(
        return_value=httpx.Response(200, content=b"x" * 5000)
    )
    client = AsyncMedplumClient(access_token="t")
    try:
        with pytest.raises(ValueError, match="exceeding max_bytes=1024"):
            await client.download_binary("abc", max_bytes=1024)
    finally:
        await client.aclose()
