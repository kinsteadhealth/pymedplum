"""End-to-end pattern test for audit logging via on_request_complete.

Mirrors how a web framework (FastAPI, Django-ninja, Starlette) wires:

    1. A ContextVar is set by framework middleware before the handler runs.
    2. The handler makes a pymedplum call.
    3. pymedplum's on_request_complete hook reads the ContextVar in the
       caller's task stack and writes the actor + RequestEvent to an
       audit log.
    4. Multiple concurrent requests each see their own actor.

No real HTTP server is used; respx mocks the wire. The framework
scaffolding is a handful of async functions to keep the test focused
on the pymedplum integration shape rather than on framework ergonomics.
"""

from __future__ import annotations

import asyncio
from contextvars import ContextVar
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import respx

from pymedplum import AsyncMedplumClient, NotFoundError

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from pymedplum.hooks import RequestEvent


@dataclass(frozen=True)
class User:
    id: str
    medplum_membership_id: str


current_user: ContextVar[User | None] = ContextVar("current_user", default=None)


def _audit_record(event: RequestEvent, user: User | None) -> dict[str, Any]:
    return {
        "actor_user_id": user.id if user else None,
        "actor_membership_id": user.medplum_membership_id if user else None,
        "method": event.method,
        "path_template": event.path_template,
        "resource_type": event.resource_type,
        "resource_id": event.resource_id,
        "final_status_code": event.final_status_code,
        "wire_on_behalf_of": (
            event.attempts[0].on_behalf_of if event.attempts else None
        ),
    }


async def _with_user(user: User, handler: Callable[[], Awaitable[Any]]) -> Any:
    token = current_user.set(user)
    try:
        return await handler()
    finally:
        current_user.reset(token)


async def _get_patient(client: AsyncMedplumClient, patient_id: str) -> dict[str, Any]:
    user = current_user.get()
    assert user is not None, "handler must run inside user middleware"
    return await client.read_resource(
        "Patient",
        patient_id,
        on_behalf_of=user.medplum_membership_id,
    )


def _mock_medplum() -> respx.MockRouter:
    mock = respx.mock(base_url="https://api.medplum.com", assert_all_called=False)
    mock.post("/oauth2/token").respond(
        json={"access_token": "t", "expires_in": 3600},
    )
    mock.get(url__regex=r"/fhir/R4/Patient/[^/]+").respond(
        json={"resourceType": "Patient", "id": "abc"},
    )
    return mock


@pytest.mark.asyncio
async def test_audit_log_captures_actor_and_request_metadata():
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with _mock_medplum():
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            alice = User(
                id="alice-42", medplum_membership_id="ProjectMembership/pm-alice"
            )
            await _with_user(alice, lambda: _get_patient(client, "abc"))
        finally:
            await client.aclose()

    data = [r for r in records if r["resource_type"] == "Patient"]
    assert len(data) == 1
    record = data[0]
    assert record == {
        "actor_user_id": "alice-42",
        "actor_membership_id": "ProjectMembership/pm-alice",
        "method": "GET",
        "path_template": "/fhir/R4/Patient/{id}",
        "resource_type": "Patient",
        "resource_id": "abc",
        "final_status_code": 200,
        "wire_on_behalf_of": "ProjectMembership/pm-alice",
    }


@pytest.mark.asyncio
async def test_concurrent_requests_each_attribute_to_their_own_actor():
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with _mock_medplum():
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            alice = User(
                id="alice-42", medplum_membership_id="ProjectMembership/pm-alice"
            )
            bob = User(id="bob-99", medplum_membership_id="ProjectMembership/pm-bob")

            await asyncio.gather(
                _with_user(alice, lambda: _get_patient(client, "patient-a")),
                _with_user(bob, lambda: _get_patient(client, "patient-b")),
            )
        finally:
            await client.aclose()

    data = [r for r in records if r["resource_type"] == "Patient"]
    assert len(data) == 2

    by_user = {r["actor_user_id"]: r for r in data}
    assert by_user["alice-42"]["resource_id"] == "patient-a"
    assert by_user["alice-42"]["wire_on_behalf_of"] == "ProjectMembership/pm-alice"
    assert by_user["bob-99"]["resource_id"] == "patient-b"
    assert by_user["bob-99"]["wire_on_behalf_of"] == "ProjectMembership/pm-bob"


@pytest.mark.asyncio
async def test_auth_event_has_no_actor_attribution_even_with_user_context():
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with _mock_medplum():
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            alice = User(
                id="alice-42", medplum_membership_id="ProjectMembership/pm-alice"
            )
            await _with_user(alice, lambda: _get_patient(client, "abc"))
        finally:
            await client.aclose()

    auth_events = [r for r in records if r["path_template"] == "/oauth2/token"]
    assert len(auth_events) == 1
    auth = auth_events[0]

    assert auth["wire_on_behalf_of"] is None
    assert auth["resource_type"] is None
    assert auth["resource_id"] is None


@pytest.mark.asyncio
async def test_error_response_still_fires_hook_with_actor_attribution():
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/missing-id").respond(
            404,
            json={"resourceType": "OperationOutcome", "issue": []},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            alice = User(
                id="alice-42", medplum_membership_id="ProjectMembership/pm-alice"
            )
            with pytest.raises(NotFoundError):
                await _with_user(alice, lambda: _get_patient(client, "missing-id"))
        finally:
            await client.aclose()

    data = [r for r in records if r["resource_type"] == "Patient"]
    assert len(data) == 1
    record = data[0]
    assert record["actor_user_id"] == "alice-42"
    assert record["actor_membership_id"] == "ProjectMembership/pm-alice"
    assert record["final_status_code"] == 404
    assert record["wire_on_behalf_of"] == "ProjectMembership/pm-alice"


@pytest.mark.asyncio
async def test_multiple_fhir_calls_in_one_handler_share_actor_and_audit_each():
    """Realistic handler pattern: read patient, search their conditions + observations."""
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        mock.get(url__regex=r"/fhir/R4/Condition.*").respond(
            json={"resourceType": "Bundle", "entry": []},
        )
        mock.get(url__regex=r"/fhir/R4/Observation.*").respond(
            json={"resourceType": "Bundle", "entry": []},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        alice = User(id="alice-42", medplum_membership_id="ProjectMembership/pm-alice")

        async def handler() -> None:
            user = current_user.get()
            assert user is not None
            await client.read_resource(
                "Patient", "abc", on_behalf_of=user.medplum_membership_id
            )
            await client.search_resources(
                "Condition",
                {"patient": "abc"},
                on_behalf_of=user.medplum_membership_id,
            )
            await client.search_resources(
                "Observation",
                {"patient": "abc"},
                on_behalf_of=user.medplum_membership_id,
            )

        try:
            await _with_user(alice, handler)
        finally:
            await client.aclose()

    data = [
        r
        for r in records
        if r["resource_type"] in {"Patient", "Condition", "Observation"}
    ]
    assert len(data) == 3
    assert {r["resource_type"] for r in data} == {"Patient", "Condition", "Observation"}
    for r in data:
        assert r["actor_user_id"] == "alice-42"
        assert r["wire_on_behalf_of"] == "ProjectMembership/pm-alice"


@pytest.mark.asyncio
async def test_context_manager_obo_block_audits_every_inner_call_with_ambient_identity():
    """`async with client.on_behalf_of(...)` avoids repeating the kwarg per call."""
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        mock.get(url__regex=r"/fhir/R4/Condition.*").respond(
            json={"resourceType": "Bundle", "entry": []},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        alice = User(id="alice-42", medplum_membership_id="ProjectMembership/pm-alice")

        async def handler() -> None:
            user = current_user.get()
            assert user is not None
            async with client.on_behalf_of(user.medplum_membership_id):
                await client.read_resource("Patient", "abc")
                await client.search_resources("Condition", {"patient": "abc"})

        try:
            await _with_user(alice, handler)
        finally:
            await client.aclose()

    data = [r for r in records if r["resource_type"] in {"Patient", "Condition"}]
    assert len(data) == 2
    for r in data:
        assert r["actor_user_id"] == "alice-42"
        assert r["wire_on_behalf_of"] == "ProjectMembership/pm-alice"


@pytest.mark.asyncio
async def test_search_query_params_visible_to_hook_under_opt_in_policy():
    """Demonstrates the per-resource-type query-param policy from docs/advanced/audit_logging.md."""
    records: list[dict[str, Any]] = []
    phi_resource_types = {"Patient"}

    def hook(event: RequestEvent) -> None:
        base = _audit_record(event, current_user.get())
        include_qp = event.resource_type in phi_resource_types
        base["query_params"] = event.query_params if include_qp else None
        base["from_to_dict"] = event.to_phi_audit_dict(include_query_params=include_qp)
        records.append(base)

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get(url__regex=r"/fhir/R4/Patient.*").respond(
            json={"resourceType": "Bundle", "entry": []},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        alice = User(id="alice-42", medplum_membership_id="ProjectMembership/pm-alice")

        async def handler() -> None:
            await client.search_resources(
                "Patient",
                {"identifier": "mrn|123", "_count": "5"},
                on_behalf_of=alice.medplum_membership_id,
            )

        try:
            await _with_user(alice, handler)
        finally:
            await client.aclose()

    searches = [
        r
        for r in records
        if r["resource_type"] == "Patient" and r["resource_id"] is None
    ]
    assert len(searches) == 1
    s = searches[0]

    assert s["query_params"] == {"identifier": ["mrn|123"], "_count": ["5"]}
    assert s["path_template"] == "/fhir/R4/Patient"
    assert "query_params" in s["from_to_dict"]
    assert s["from_to_dict"]["query_params"] == {
        "identifier": ["mrn|123"],
        "_count": ["5"],
    }


@pytest.mark.asyncio
async def test_write_operations_audited_with_method_and_actor():
    """Mutations (POST/PUT/PATCH) produce audit records with the right method."""
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.post("/fhir/R4/Observation").respond(
            201,
            json={"resourceType": "Observation", "id": "obs-new"},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        alice = User(id="alice-42", medplum_membership_id="ProjectMembership/pm-alice")

        async def handler() -> None:
            await client.create_resource(
                {
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {"text": "systolic-bp"},
                },
                on_behalf_of=alice.medplum_membership_id,
            )

        try:
            await _with_user(alice, handler)
        finally:
            await client.aclose()

    data = [r for r in records if r["resource_type"] == "Observation"]
    assert len(data) == 1
    r = data[0]
    assert r["method"] == "POST"
    assert r["final_status_code"] == 201
    assert r["actor_user_id"] == "alice-42"
    assert r["wire_on_behalf_of"] == "ProjectMembership/pm-alice"


@pytest.mark.asyncio
async def test_async_hook_writes_to_async_sink_with_actor_context():
    """Production audit sinks are typically async (DB write, queue publish)."""
    sink: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

    async def async_hook(event: RequestEvent) -> None:
        await sink.put(_audit_record(event, current_user.get()))

    with _mock_medplum():
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=async_hook,
        )
        alice = User(id="alice-42", medplum_membership_id="ProjectMembership/pm-alice")
        try:
            await _with_user(alice, lambda: _get_patient(client, "abc"))
        finally:
            await client.aclose()

    records: list[dict[str, Any]] = []
    while not sink.empty():
        records.append(sink.get_nowait())
    data = [r for r in records if r["resource_type"] == "Patient"]
    assert len(data) == 1
    assert data[0]["actor_user_id"] == "alice-42"
    assert data[0]["wire_on_behalf_of"] == "ProjectMembership/pm-alice"


@pytest.mark.asyncio
async def test_handler_without_user_context_records_null_actor():
    """A healthcheck / cron handler without user context still audits cleanly."""
    records: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        records.append(_audit_record(event, current_user.get()))

    with _mock_medplum():
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            await client.read_resource(
                "Patient", "abc", on_behalf_of="ProjectMembership/system-cron"
            )
        finally:
            await client.aclose()

    data = [r for r in records if r["resource_type"] == "Patient"]
    assert len(data) == 1
    r = data[0]
    assert r["actor_user_id"] is None
    assert r["actor_membership_id"] is None
    assert r["wire_on_behalf_of"] == "ProjectMembership/system-cron"


@pytest.mark.asyncio
async def test_retry_path_captured_as_one_event_with_per_attempt_detail():
    """429 → retry → 200 produces one audit event whose attempts list reflects both wire attempts."""
    detailed: list[dict[str, Any]] = []

    def hook(event: RequestEvent) -> None:
        rec = _audit_record(event, current_user.get())
        rec["attempt_count"] = len(event.attempts)
        rec["attempt_status_codes"] = [a.status_code for a in event.attempts]
        rec["attempt_obo_values"] = [a.on_behalf_of for a in event.attempts]
        detailed.append(rec)

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        route = mock.get("/fhir/R4/Patient/flaky")
        route.side_effect = [
            httpx.Response(429, headers={"Retry-After": "0"}, json={}),
            httpx.Response(200, json={"resourceType": "Patient", "id": "flaky"}),
        ]

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        alice = User(id="alice-42", medplum_membership_id="ProjectMembership/pm-alice")
        try:
            await _with_user(alice, lambda: _get_patient(client, "flaky"))
        finally:
            await client.aclose()

    data = [r for r in detailed if r["resource_type"] == "Patient"]
    assert len(data) == 1, "one logical event, not one per wire attempt"
    r = data[0]
    assert r["actor_user_id"] == "alice-42"
    assert r["final_status_code"] == 200
    assert r["attempt_count"] == 2
    assert r["attempt_status_codes"] == [429, 200]
    assert r["attempt_obo_values"] == [
        "ProjectMembership/pm-alice",
        "ProjectMembership/pm-alice",
    ]
