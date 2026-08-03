"""Replay-safety policy tests: 503 as ambiguous-commit and possibly_committed."""

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import (
    AsyncMedplumClient,
    MedplumClient,
    NetworkError,
    ServerError,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

_BASE_URL = "https://api.medplum.com/"
_PATIENT_TYPE = f"{_BASE_URL}fhir/R4/Patient"


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncMedplumClient]:
    client = AsyncMedplumClient(base_url=_BASE_URL, access_token="tkn")
    try:
        yield client
    finally:
        await client.aclose()


def test_conditional_create_retried_on_503(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """POST with If-None-Exist stays replay-safe under the 503 flip."""
    route = respx_mock.post(_PATIENT_TYPE).mock(
        side_effect=[
            httpx.Response(503, text="Service Unavailable"),
            httpx.Response(201, json={"resourceType": "Patient", "id": "p1"}),
        ]
    )

    result = sync_client.create_resource_if_none_exist(
        {"resourceType": "Patient"}, "identifier=http://example.org|1"
    )

    assert result["id"] == "p1"
    assert route.call_count == 2


async def test_async_post_create_not_replayed_on_503(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    """Async parity for the 503 flip: a bare POST is terminal."""
    route = respx_mock.post(_PATIENT_TYPE).mock(
        return_value=httpx.Response(503, text="Service Unavailable")
    )

    with pytest.raises(ServerError) as exc_info:
        await async_client.create_resource({"resourceType": "Patient"})

    assert exc_info.value.status_code == 503
    assert route.call_count == 1


def test_connect_error_sets_possibly_committed_false(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """Connect-phase failures provably never reached the origin."""
    respx_mock.post(_PATIENT_TYPE).mock(
        side_effect=httpx.ConnectError("connection refused")
    )

    with pytest.raises(NetworkError) as exc_info:
        sync_client.create_resource({"resourceType": "Patient"})

    assert exc_info.value.possibly_committed is False
    assert exc_info.value.sanitize_for_logging()["possibly_committed"] is False


def test_read_timeout_on_bare_post_sets_possibly_committed_true(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """A post-send failure may have committed — the caller must re-read
    before retrying anything non-idempotent."""
    route = respx_mock.post(_PATIENT_TYPE).mock(
        side_effect=httpx.ReadTimeout("read timed out")
    )

    with pytest.raises(NetworkError) as exc_info:
        sync_client.create_resource({"resourceType": "Patient"})

    # Bare POST + ambiguous transport failure: no retry, one attempt.
    assert route.call_count == 1
    assert exc_info.value.possibly_committed is True


def test_read_timeout_on_get_exhaustion_sets_possibly_committed_true(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(f"{_PATIENT_TYPE}/p1").mock(
        side_effect=httpx.ReadTimeout("read timed out")
    )

    with pytest.raises(NetworkError) as exc_info:
        sync_client.read_resource("Patient", "p1")

    assert exc_info.value.possibly_committed is True


async def test_async_possibly_committed_flags(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.post(_PATIENT_TYPE).mock(
        side_effect=httpx.ConnectError("connection refused")
    )
    with pytest.raises(NetworkError) as connect_exc:
        await async_client.create_resource({"resourceType": "Patient"})
    assert connect_exc.value.possibly_committed is False

    respx_mock.post(_PATIENT_TYPE).mock(side_effect=httpx.ReadTimeout("read timed out"))
    with pytest.raises(NetworkError) as timeout_exc:
        await async_client.create_resource({"resourceType": "Patient"})
    assert timeout_exc.value.possibly_committed is True
