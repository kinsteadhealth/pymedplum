"""Sync + async transport tests for update_with_retry."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import (
    AsyncMedplumClient,
    MedplumClient,
    MissingVersionIdError,
    PreconditionFailedError,
    UpdateResult,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

_BASE_URL = "https://api.medplum.com/"
_PATIENT_PATH = f"{_BASE_URL}fhir/R4/Patient/p1"


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncMedplumClient]:
    client = AsyncMedplumClient(base_url=_BASE_URL, access_token="tkn")
    try:
        yield client
    finally:
        await client.aclose()


def _patient(version_id: str | None = "1", active: bool = False) -> dict[str, Any]:
    resource: dict[str, Any] = {
        "resourceType": "Patient",
        "id": "p1",
        "active": active,
    }
    if version_id is not None:
        resource["meta"] = {"versionId": version_id}
    return resource


def _conflict() -> httpx.Response:
    return httpx.Response(
        412,
        json={
            "resourceType": "OperationOutcome",
            "issue": [{"severity": "error", "code": "conflict"}],
        },
    )


def _activate(resource: dict[str, Any]) -> dict[str, Any]:
    resource["active"] = True
    return resource


def test_writes_with_if_match_from_read(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("7"))
    )
    put_route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("8", active=True))
    )

    result = sync_client.update_with_retry("Patient", "p1", _activate)

    assert isinstance(result, UpdateResult)
    assert result.wrote is True
    assert result.version_id == "8"
    assert result.resource["active"] is True
    assert put_route.calls[0].request.headers["If-Match"] == 'W/"7"'


def test_skips_put_when_mutator_returns_none(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("3"))
    )
    put_route = respx_mock.put(_PATIENT_PATH)

    result = sync_client.update_with_retry("Patient", "p1", lambda _r: None)

    assert result.wrote is False
    assert result.version_id == "3"
    assert not put_route.called


def test_skips_put_when_state_unchanged(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("3"))
    )
    put_route = respx_mock.put(_PATIENT_PATH)

    result = sync_client.update_with_retry("Patient", "p1", dict)

    assert result.wrote is False
    assert not put_route.called


def test_in_place_mutation_returning_none_still_writes(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """The naive Python idiom — mutate in place, return None — must
    write, not silently no-op."""
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("3"))
    )
    put_route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("4", active=True))
    )

    def mutate_in_place(resource: dict[str, Any]) -> None:
        resource["active"] = True

    result = sync_client.update_with_retry("Patient", "p1", mutate_in_place)

    assert result.wrote is True
    assert put_route.called


def test_force_writes_even_when_unchanged(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("3"))
    )
    put_route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("4"))
    )

    result = sync_client.update_with_retry("Patient", "p1", lambda _r: None, force=True)

    assert result.wrote is True
    assert result.version_id == "4"
    assert put_route.called


def test_412_rereads_and_reruns_mutator(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    seen_versions: list[str] = []

    def record_and_activate(resource: dict[str, Any]) -> dict[str, Any]:
        seen_versions.append(resource["meta"]["versionId"])
        resource["active"] = True
        return resource

    get_route = respx_mock.get(_PATIENT_PATH).mock(
        side_effect=[
            httpx.Response(200, json=_patient("1")),
            httpx.Response(200, json=_patient("2")),
        ]
    )
    put_route = respx_mock.put(_PATIENT_PATH).mock(
        side_effect=[
            _conflict(),
            httpx.Response(200, json=_patient("3", active=True)),
        ]
    )

    result = sync_client.update_with_retry("Patient", "p1", record_and_activate)

    assert result.wrote is True
    assert result.version_id == "3"
    assert seen_versions == ["1", "2"]
    assert get_route.call_count == 2
    assert put_route.call_count == 2
    assert put_route.calls[1].request.headers["If-Match"] == 'W/"2"'


def test_412_exhaustion_raises(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("1"))
    )
    put_route = respx_mock.put(_PATIENT_PATH).mock(return_value=_conflict())

    with pytest.raises(PreconditionFailedError):
        sync_client.update_with_retry("Patient", "p1", _activate, max_retries=1)

    assert put_route.call_count == 2


def test_missing_version_id_raises_instead_of_unguarded_write(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient(version_id=None))
    )
    put_route = respx_mock.put(_PATIENT_PATH)

    with pytest.raises(MissingVersionIdError, match=r"meta\.versionId"):
        sync_client.update_with_retry("Patient", "p1", _activate)

    assert not put_route.called


def test_mutator_changing_identity_raises(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("1"))
    )

    with pytest.raises(ValueError, match="resourceType or id"):
        sync_client.update_with_retry("Patient", "p1", lambda r: {**r, "id": "p2"})


def test_empty_put_body_rereads_for_version(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        side_effect=[
            httpx.Response(200, json=_patient("1")),
            httpx.Response(200, json=_patient("2", active=True)),
        ]
    )
    respx_mock.put(_PATIENT_PATH).mock(return_value=httpx.Response(200, json={}))

    result = sync_client.update_with_retry("Patient", "p1", _activate)

    assert result.wrote is True
    assert result.version_id == "2"
    assert result.resource["active"] is True


async def test_async_writes_with_if_match_and_retries_412(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        side_effect=[
            httpx.Response(200, json=_patient("1")),
            httpx.Response(200, json=_patient("2")),
        ]
    )
    put_route = respx_mock.put(_PATIENT_PATH).mock(
        side_effect=[
            _conflict(),
            httpx.Response(200, json=_patient("3", active=True)),
        ]
    )

    result = await async_client.update_with_retry("Patient", "p1", _activate)

    assert result.wrote is True
    assert result.version_id == "3"
    assert put_route.call_count == 2
    assert put_route.calls[0].request.headers["If-Match"] == 'W/"1"'
    assert put_route.calls[1].request.headers["If-Match"] == 'W/"2"'


async def test_async_noop_and_missing_version(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient(version_id=None))
    )
    put_route = respx_mock.put(_PATIENT_PATH)

    result = await async_client.update_with_retry("Patient", "p1", lambda _r: None)
    assert result.wrote is False
    assert result.version_id == ""

    with pytest.raises(MissingVersionIdError):
        await async_client.update_with_retry("Patient", "p1", _activate)

    assert not put_route.called
