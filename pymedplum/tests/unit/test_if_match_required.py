"""Tests for if_match="required", patch if_match, and transaction accounts."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import (
    AsyncMedplumClient,
    MedplumClient,
    MedplumError,
    MissingVersionIdError,
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


def _patient(version_id: str | None = "5") -> dict[str, Any]:
    resource: dict[str, Any] = {"resourceType": "Patient", "id": "p1"}
    if version_id is not None:
        resource["meta"] = {"versionId": version_id}
    return resource


def test_update_required_attaches_if_match(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )

    sync_client.update_resource(_patient("5"), if_match="required")

    assert route.calls[0].request.headers["If-Match"] == 'W/"5"'


def test_update_required_raises_without_version_id(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.put(_PATIENT_PATH)

    with pytest.raises(MissingVersionIdError) as exc_info:
        sync_client.update_resource(_patient(None), if_match="required")

    assert not route.called
    assert isinstance(exc_info.value, MedplumError)


def test_update_true_still_degrades_silently_without_version_id(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """The default keeps its documented (lenient) behavior — "required"
    is the opt-in strict mode, not a change to True."""
    route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("1"))
    )

    sync_client.update_resource(_patient(None))

    assert "If-Match" not in route.calls[0].request.headers


def test_patch_if_match_kwarg_sends_header(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.patch(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )

    sync_client.patch_resource(
        "Patient",
        "p1",
        [{"op": "replace", "path": "/active", "value": True}],
        if_match='W/"5"',
    )

    request = route.calls[0].request
    assert request.headers["If-Match"] == 'W/"5"'
    assert request.headers["Content-Type"] == "application/json-patch+json"


def test_patch_explicit_header_wins_over_kwarg(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.patch(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )

    sync_client.patch_resource(
        "Patient",
        "p1",
        [{"op": "replace", "path": "/active", "value": True}],
        headers={"If-Match": 'W/"9"'},
        if_match='W/"5"',
    )

    assert route.calls[0].request.headers["If-Match"] == 'W/"9"'


def test_patch_lowercase_header_wins_without_duplication(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """Header names are case-insensitive on the wire — a lowercase
    caller header must win over the kwarg, not combine with it into
    a joined 'W/"9", W/"5"' value."""
    route = respx_mock.patch(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )

    sync_client.patch_resource(
        "Patient",
        "p1",
        [{"op": "replace", "path": "/active", "value": True}],
        headers={"if-match": 'W/"9"'},
        if_match='W/"5"',
    )

    assert route.calls[0].request.headers.get_list("if-match") == ['W/"9"']


def test_update_lowercase_header_wins_and_required_defers(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    """A caller-supplied If-Match (any case) owns the guard: no joined
    header, and if_match="required" must not raise for a version-less
    resource when the caller already provided the ETag."""
    route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )

    sync_client.update_resource(
        _patient(None),
        headers={"if-match": 'W/"9"'},
        if_match="required",
    )

    assert route.calls[0].request.headers.get_list("if-match") == ['W/"9"']


async def test_async_lowercase_header_wins_without_duplication(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    patch_route = respx_mock.patch(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )
    await async_client.patch_resource(
        "Patient",
        "p1",
        [{"op": "replace", "path": "/active", "value": True}],
        headers={"if-match": 'W/"9"'},
        if_match='W/"5"',
    )
    assert patch_route.calls[0].request.headers.get_list("if-match") == ['W/"9"']

    put_route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )
    await async_client.update_resource(
        _patient(None),
        headers={"if-match": 'W/"9"'},
        if_match="required",
    )
    assert put_route.calls[0].request.headers.get_list("if-match") == ['W/"9"']


def test_execute_transaction_stamps_accounts_without_mutating_caller(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(f"{_BASE_URL}fhir/R4").mock(
        return_value=httpx.Response(
            200, json={"resourceType": "Bundle", "type": "transaction-response"}
        )
    )
    bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {"resourceType": "Patient"},
                "request": {"method": "POST", "url": "Patient"},
            }
        ],
    }

    sync_client.execute_transaction(bundle, accounts="Organization/org-a")

    sent = json.loads(route.calls[0].request.read())
    assert sent["type"] == "transaction"
    assert sent["entry"][0]["resource"]["meta"]["accounts"] == [
        {"reference": "Organization/org-a"}
    ]
    # The caller's bundle stays untouched — no type or accounts leak-back.
    assert "type" not in bundle
    assert "meta" not in bundle["entry"][0]["resource"]


async def test_async_update_required_and_patch_if_match(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    put_route = respx_mock.put(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )
    await async_client.update_resource(_patient("5"), if_match="required")
    assert put_route.calls[0].request.headers["If-Match"] == 'W/"5"'

    with pytest.raises(MissingVersionIdError):
        await async_client.update_resource(_patient(None), if_match="required")

    patch_route = respx_mock.patch(_PATIENT_PATH).mock(
        return_value=httpx.Response(200, json=_patient("6"))
    )
    await async_client.patch_resource(
        "Patient",
        "p1",
        [{"op": "replace", "path": "/active", "value": True}],
        if_match='W/"5"',
    )
    assert patch_route.calls[0].request.headers["If-Match"] == 'W/"5"'


async def test_async_execute_transaction_stamps_accounts(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.post(f"{_BASE_URL}fhir/R4").mock(
        return_value=httpx.Response(
            200, json={"resourceType": "Bundle", "type": "transaction-response"}
        )
    )
    bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {"resourceType": "Patient"},
                "request": {"method": "POST", "url": "Patient"},
            }
        ],
    }

    await async_client.execute_transaction(bundle, accounts="Organization/org-a")

    sent = json.loads(route.calls[0].request.read())
    assert sent["entry"][0]["resource"]["meta"]["accounts"] == [
        {"reference": "Organization/org-a"}
    ]
