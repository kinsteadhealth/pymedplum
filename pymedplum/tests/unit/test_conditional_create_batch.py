"""Sync + async transport tests for conditional_create_batch."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import AsyncMedplumClient, BatchCreateResult, MedplumClient

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

_BASE_URL = "https://api.medplum.com/"
_FHIR_ROOT = f"{_BASE_URL}fhir/R4/"


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncMedplumClient]:
    client = AsyncMedplumClient(base_url=_BASE_URL, access_token="tkn")
    try:
        yield client
    finally:
        await client.aclose()


def _patient(n: int) -> dict[str, Any]:
    return {
        "resourceType": "Patient",
        "identifier": [{"system": "http://example.org/mrn", "value": str(n)}],
    }


def _entry(n: int) -> tuple[dict[str, Any], str]:
    return _patient(n), f"identifier=http://example.org/mrn|{n}"


def _batch_response(statuses: list[str]) -> dict[str, Any]:
    return {
        "resourceType": "Bundle",
        "type": "batch-response",
        "entry": [
            {"response": {"status": status, "location": f"Patient/p{i}"}}
            for i, status in enumerate(statuses)
        ],
    }


def test_batch_builds_conditional_entries_and_classifies(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(_FHIR_ROOT).mock(
        return_value=httpx.Response(
            200, json=_batch_response(["201 Created", "200 OK", "400 Bad Request"])
        )
    )

    result = sync_client.conditional_create_batch([_entry(1), _entry(2), _entry(3)])

    assert isinstance(result, BatchCreateResult)
    assert [r.index for r in result.created] == [0]
    assert [r.index for r in result.existed] == [1]
    assert [r.index for r in result.failed] == [2]
    assert result.ok is False

    sent = json.loads(route.calls[0].request.read())
    assert sent["type"] == "batch"
    assert len(sent["entry"]) == 3
    first = sent["entry"][0]
    assert first["request"]["method"] == "POST"
    assert first["request"]["url"] == "Patient"
    assert first["request"]["ifNoneExist"] == "identifier=http://example.org/mrn|1"
    assert first["resource"]["resourceType"] == "Patient"


def test_batch_chunks_and_rebases_indices(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(_FHIR_ROOT).mock(
        side_effect=[
            httpx.Response(200, json=_batch_response(["201 Created", "200 OK"])),
            httpx.Response(200, json=_batch_response(["201 Created"])),
        ]
    )

    result = sync_client.conditional_create_batch(
        [_entry(1), _entry(2), _entry(3)], chunk_size=2
    )

    assert route.call_count == 2
    assert [r.index for r in result.created] == [0, 2]
    assert [r.index for r in result.existed] == [1]
    assert result.failed == []
    assert result.ok is True
    chunk_sizes = [
        len(json.loads(call.request.read())["entry"]) for call in route.calls
    ]
    assert chunk_sizes == [2, 1]


def test_batch_truncated_response_marks_tail_failed(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """A response with fewer entries than sent must not read as a smaller
    success — the missing tail classifies as failed."""
    respx_mock.post(_FHIR_ROOT).mock(
        return_value=httpx.Response(200, json=_batch_response(["201 Created"]))
    )

    result = sync_client.conditional_create_batch([_entry(1), _entry(2)])

    assert [r.index for r in result.created] == [0]
    assert [r.index for r in result.failed] == [1]
    assert result.failed[0].status_code is None


def test_batch_retries_503_because_replay_safe(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """The outer bundle POST carries no If-None-Exist header, but every
    inner entry is a conditional create — the SDK marks the request
    replay-safe, so the ambiguous 503 retries instead of raising."""
    route = respx_mock.post(_FHIR_ROOT).mock(
        side_effect=[
            httpx.Response(503, text="Service Unavailable"),
            httpx.Response(200, json=_batch_response(["201 Created"])),
        ]
    )

    result = sync_client.conditional_create_batch([_entry(1)])

    assert route.call_count == 2
    assert len(result.created) == 1


def test_batch_stamps_accounts_and_sanitizes_query(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(_FHIR_ROOT).mock(
        return_value=httpx.Response(200, json=_batch_response(["201 Created"]))
    )

    sync_client.conditional_create_batch(
        [(_patient(1), "?identifier=http://example.org/mrn|1")],
        accounts="Organization/org-a",
    )

    sent = json.loads(route.calls[0].request.read())
    entry = sent["entry"][0]
    assert entry["request"]["ifNoneExist"] == "identifier=http://example.org/mrn|1"
    assert entry["resource"]["meta"]["accounts"] == [
        {"reference": "Organization/org-a"}
    ]


def test_batch_rejects_bad_inputs(sync_client: MedplumClient) -> None:
    with pytest.raises(ValueError, match="chunk_size"):
        sync_client.conditional_create_batch([_entry(1)], chunk_size=0)
    with pytest.raises(ValueError, match="resourceType"):
        sync_client.conditional_create_batch([({}, "identifier=x|1")])
    with pytest.raises(ValueError, match="if_none_exist"):
        sync_client.conditional_create_batch([(_patient(1), "  ")])


async def test_async_batch_classifies_and_rebases(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(_FHIR_ROOT).mock(
        side_effect=[
            httpx.Response(200, json=_batch_response(["201 Created"])),
            httpx.Response(200, json=_batch_response(["200 OK"])),
        ]
    )

    result = await async_client.conditional_create_batch(
        [_entry(1), _entry(2)], chunk_size=1
    )

    assert route.call_count == 2
    assert [r.index for r in result.created] == [0]
    assert [r.index for r in result.existed] == [1]
    assert result.existed[0].resource_id == "p0"


async def test_async_batch_retries_503_because_replay_safe(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(_FHIR_ROOT).mock(
        side_effect=[
            httpx.Response(503, text="Service Unavailable"),
            httpx.Response(200, json=_batch_response(["201 Created"])),
        ]
    )

    result = await async_client.conditional_create_batch([_entry(1)])

    assert route.call_count == 2
    assert len(result.created) == 1
