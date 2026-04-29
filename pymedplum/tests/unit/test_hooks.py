from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
import pytest
import respx

from pymedplum.hooks import (
    PreparedRequest,
    RequestAttempt,
    RequestEvent,
    _compute_action,
    _compute_outcome,
    _parse_fhir_url,
    _parse_query_params,
    serialize_exception,
)

TOKEN_RESPONSE = {"access_token": "t", "expires_in": 3600}


@asynccontextmanager
async def async_hook_client(**kwargs):
    """Build an AsyncMedplumClient with an event-capturing hook and close it.

    Yields ``(client, events)``. The client is closed on exit.
    Default credentials ``client_id="c"``, ``client_secret="s"``, and
    ``base_url="https://api.medplum.com/"`` may be overridden via kwargs.
    """
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    client = AsyncMedplumClient(
        base_url=kwargs.pop("base_url", "https://api.medplum.com/"),
        client_id=kwargs.pop("client_id", "c"),
        client_secret=kwargs.pop("client_secret", "s"),
        on_request_complete=kwargs.pop("on_request_complete", events.append),
        **kwargs,
    )
    try:
        yield client, events
    finally:
        await client.aclose()


@contextmanager
def sync_hook_client(**kwargs):
    """Sync counterpart of ``async_hook_client``. Yields ``(client, events)``."""
    from pymedplum import MedplumClient

    events: list[RequestEvent] = []
    client = MedplumClient(
        base_url=kwargs.pop("base_url", "https://api.medplum.com/"),
        client_id=kwargs.pop("client_id", "c"),
        client_secret=kwargs.pop("client_secret", "s"),
        on_request_complete=kwargs.pop("on_request_complete", events.append),
        **kwargs,
    )
    try:
        yield client, events
    finally:
        client.close()


def test_prepared_request_is_frozen() -> None:
    p = PreparedRequest(method="GET", url="u", headers={}, json_body=None)
    with pytest.raises(AttributeError):
        p.method = "POST"  # type: ignore[misc]


def test_request_event_to_phi_audit_dict_is_json_serializable_for_simple_case() -> None:
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    json.dumps(ev.to_phi_audit_dict())


def test_request_event_serializes_exception_as_dict() -> None:
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[
            RequestAttempt(
                attempt_number=1,
                status_code=None,
                duration_seconds=0.1,
                on_behalf_of=None,
                exception=ValueError("bad"),
            ),
        ],
        final_status_code=None,
        final_exception=ValueError("bad"),
    )
    d = ev.to_phi_audit_dict()
    # Non-pymedplum exceptions pass ``str(exc)`` through verbatim. The hook
    # consumer owns their sink's PHI contract.
    assert d["attempts"][0]["exception"] == {
        "type": "ValueError",
        "message": "bad",
    }
    assert d["final_exception"] == {"type": "ValueError", "message": "bad"}


def test_to_phi_audit_dict_omits_query_params_by_default() -> None:
    ev = RequestEvent(
        method="GET",
        path="/fhir/R4/Patient",
        path_template="/fhir/R4/Patient",
        query_params={"identifier": ["mrn|123"]},
        resource_type="Patient",
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    assert "query_params" not in ev.to_phi_audit_dict()


def _sample_event() -> RequestEvent:
    return RequestEvent(
        method="GET",
        path="/fhir/R4/Patient/abc-123",
        path_template="/fhir/R4/Patient/{id}",
        query_params={"identifier": ["mrn|123"]},
        resource_type="Patient",
        resource_id="abc-123",
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[
            RequestAttempt(
                attempt_number=1,
                status_code=200,
                duration_seconds=0.05,
                on_behalf_of="ProjectMembership/aaaa-bbbb",
                exception=None,
            )
        ],
        final_status_code=200,
        final_exception=None,
    )


def test_to_phi_audit_dict_includes_phi_fields() -> None:
    payload = _sample_event().to_phi_audit_dict()
    assert payload["path"] == "/fhir/R4/Patient/abc-123"
    assert payload["resource_id"] == "abc-123"
    assert payload["attempts"][0]["on_behalf_of"] == "ProjectMembership/aaaa-bbbb"
    # query_params still opt-in even on PHI dict
    assert "query_params" not in payload


def test_to_phi_audit_dict_with_query_params() -> None:
    payload = _sample_event().to_phi_audit_dict(include_query_params=True)
    assert payload["query_params"] == {"identifier": ["mrn|123"]}


def test_to_non_phi_dict_strips_phi_fields() -> None:
    payload = _sample_event().to_non_phi_dict()
    # Shape data is present
    assert payload["method"] == "GET"
    assert payload["path_template"] == "/fhir/R4/Patient/{id}"
    assert payload["resource_type"] == "Patient"
    assert payload["final_status_code"] == 200
    assert payload["attempt_count"] == 1
    # PHI-bearing fields are absent
    assert "path" not in payload
    assert "resource_id" not in payload
    assert "query_params" not in payload
    assert "on_behalf_of" not in payload["attempts"][0]


def test_serialize_exception_passes_through_non_pymedplum_messages() -> None:
    """Non-pymedplum exceptions pass str(exc) through; consumer scrubs if needed."""
    from pymedplum.hooks import _serialize_exception

    payload = _serialize_exception(ValueError("connection refused"))
    assert payload == {"type": "ValueError", "message": "connection refused"}

    payload = _serialize_exception(httpx.ConnectError("Connection refused"))
    assert payload == {"type": "ConnectError", "message": "Connection refused"}

    request = httpx.Request("GET", "https://api.medplum.com/fhir/R4/Patient/abc")
    response = httpx.Response(404, request=request)
    exc = httpx.HTTPStatusError("404 Not Found", request=request, response=response)
    payload = _serialize_exception(exc)
    assert payload == {"type": "HTTPStatusError", "message": "404 Not Found"}


def test_serialize_exception_trusts_sanitize_for_logging() -> None:
    """Any object declaring sanitize_for_logging gets to control its payload."""
    from pymedplum.hooks import _serialize_exception

    class CustomError(Exception):
        def sanitize_for_logging(self) -> dict[str, object]:
            return {"type": "CustomError", "safe": True}

    payload = _serialize_exception(CustomError("raw PHI-ish"))
    assert payload == {"type": "CustomError", "safe": True}


def test_to_phi_audit_dict_includes_query_params_when_opted_in() -> None:
    ev = RequestEvent(
        method="GET",
        path="/fhir/R4/Patient",
        path_template="/fhir/R4/Patient",
        query_params={"identifier": ["mrn|123"], "_count": ["5"]},
        resource_type="Patient",
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    d = ev.to_phi_audit_dict(include_query_params=True)
    assert d["query_params"] == {
        "identifier": ["mrn|123"],
        "_count": ["5"],
    }


def test_request_event_started_ended_utc_ordered() -> None:
    start = datetime.now(timezone.utc)
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=start,
        ended_at=start + timedelta(seconds=0.1),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    assert ev.started_at.tzinfo is timezone.utc
    assert ev.started_at <= ev.ended_at


@pytest.mark.parametrize(
    "path,expected",
    [
        (
            "/fhir/R4/Patient/abc-123",
            ("Patient", "abc-123", None, "/fhir/R4/Patient/{id}"),
        ),
        (
            "/fhir/R4/Patient/abc-123/_history/4",
            (
                "Patient",
                "abc-123",
                None,
                "/fhir/R4/Patient/{id}/_history/{id}",
            ),
        ),
        (
            "/fhir/R4/Patient/abc-123/$everything",
            (
                "Patient",
                "abc-123",
                "$everything",
                "/fhir/R4/Patient/{id}/$everything",
            ),
        ),
        (
            "/fhir/R4/Patient",
            ("Patient", None, None, "/fhir/R4/Patient"),
        ),
        (
            "/fhir/R4/",
            (None, None, None, "/fhir/R4/"),
        ),
        (
            "/oauth2/token",
            (None, None, None, "/oauth2/token"),
        ),
    ],
)
def test_parse_fhir_url(
    path: str,
    expected: tuple[str | None, str | None, str | None, str],
) -> None:
    assert _parse_fhir_url(path) == expected


def test_parse_query_params_none_when_empty() -> None:
    assert _parse_query_params("") is None
    assert _parse_query_params(None) is None


def test_parse_query_params_basic() -> None:
    assert _parse_query_params("identifier=mrn%7C123&_count=5") == {
        "identifier": ["mrn|123"],
        "_count": ["5"],
    }


def test_parse_query_params_repeated_keys_preserved_as_list() -> None:
    assert _parse_query_params("tag=a&tag=b") == {"tag": ["a", "b"]}


def test_parse_query_params_empty_value_preserved() -> None:
    assert _parse_query_params("flag=") == {"flag": [""]}


def test_parse_query_params_empty_dict_for_bare_question_mark() -> None:
    assert _parse_query_params("?") == {}


# =========================================================================
# before_request hook pipeline
# =========================================================================


@pytest.mark.asyncio
async def test_before_request_headers_pre_redacted() -> None:
    seen: list[dict[str, str]] = []

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        seen.append(dict(req.headers))
        return None

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        async with async_hook_client(before_request=hook) as (client, _):
            await client.read_resource("Patient", "abc", on_behalf_of="A")

    assert seen
    for headers in seen:
        keys_lower = {k.lower() for k in headers}
        assert "authorization" not in keys_lower
        assert "x-medplum-on-behalf-of" not in keys_lower


@pytest.mark.asyncio
async def test_before_request_returning_none_leaves_request_unchanged() -> None:
    from pymedplum import AsyncMedplumClient

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        return None

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        route = mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            await client.read_resource("Patient", "abc", on_behalf_of="A")
        finally:
            await client.aclose()

    assert route.called
    wire = route.calls[0].request
    assert wire.headers.get("Authorization") == "Bearer t"
    assert wire.headers.get("X-Medplum-On-Behalf-Of") == "ProjectMembership/A"


@pytest.mark.asyncio
async def test_before_request_can_mutate_json_body() -> None:
    from pymedplum import AsyncMedplumClient

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        body = dict(req.json_body or {})
        body["hooked"] = True
        return PreparedRequest(
            method=req.method,
            url=req.url,
            headers=req.headers,
            json_body=body,
        )

    captured_bodies: list[Any] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_bodies.append(json.loads(request.content or b"{}"))
        return httpx.Response(201, json={"resourceType": "Patient", "id": "new"})

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.post("/fhir/R4/Patient").mock(side_effect=handler)
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            await client.create_resource(
                {"resourceType": "Patient", "name": [{"family": "Smith"}]}
            )
        finally:
            await client.aclose()

    assert captured_bodies
    assert captured_bodies[0].get("hooked") is True


@pytest.mark.asyncio
async def test_before_request_can_mutate_non_auth_headers() -> None:
    from pymedplum import AsyncMedplumClient

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        headers = dict(req.headers)
        headers["X-Request-ID"] = "req-42"
        return PreparedRequest(
            method=req.method,
            url=req.url,
            headers=headers,
            json_body=req.json_body,
        )

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        route = mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    assert route.called
    assert route.calls[0].request.headers.get("X-Request-ID") == "req-42"


@pytest.mark.asyncio
async def test_before_request_cross_origin_url_raises() -> None:
    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import UnsafeRedirectError

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        return PreparedRequest(
            method=req.method,
            url="https://evil.com/x",
            headers=req.headers,
            json_body=req.json_body,
        )

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            with pytest.raises(UnsafeRedirectError):
                await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_before_request_same_origin_path_rewrite_allowed() -> None:
    from pymedplum import AsyncMedplumClient

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        return PreparedRequest(
            method=req.method,
            url="https://api.medplum.com/fhir/R4/Patient/rewritten",
            headers=req.headers,
            json_body=req.json_body,
        )

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        rewritten = mock.get("/fhir/R4/Patient/rewritten").respond(
            json={"resourceType": "Patient", "id": "rewritten"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            result = await client.read_resource("Patient", "original")
        finally:
            await client.aclose()

    assert rewritten.called
    assert result is not None
    assert result["id"] == "rewritten"


@pytest.mark.asyncio
async def test_before_request_injected_authorization_is_stripped() -> None:
    from pymedplum import AsyncMedplumClient

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        headers = dict(req.headers)
        headers["Authorization"] = "Bearer FAKE"
        return PreparedRequest(
            method=req.method,
            url=req.url,
            headers=headers,
            json_body=req.json_body,
        )

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "REAL", "expires_in": 3600},
        )
        route = mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    assert route.called
    assert route.calls[0].request.headers.get("Authorization") == "Bearer REAL"


@pytest.mark.asyncio
async def test_before_request_injected_obo_header_is_stripped() -> None:
    from pymedplum import AsyncMedplumClient

    def hook(req: PreparedRequest) -> PreparedRequest | None:
        headers = dict(req.headers)
        headers["X-Medplum-On-Behalf-Of"] = "ProjectMembership/EVIL"
        return PreparedRequest(
            method=req.method,
            url=req.url,
            headers=headers,
            json_body=req.json_body,
        )

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        route = mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=hook,
        )
        try:
            await client.read_resource("Patient", "abc", on_behalf_of="REAL")
        finally:
            await client.aclose()

    assert route.called
    assert (
        route.calls[0].request.headers.get("X-Medplum-On-Behalf-Of")
        == "ProjectMembership/REAL"
    )


# =========================================================================
# on_request_complete dispatch (Task 5.4)
# =========================================================================


@pytest.mark.asyncio
async def test_hook_fires_once_per_logical_call_on_success() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        async with async_hook_client() as (client, events):
            await client.read_resource("Patient", "abc")

    data = [e for e in events if e.resource_type == "Patient"]
    assert len(data) == 1
    assert data[0].resource_id == "abc"
    assert data[0].path_template == "/fhir/R4/Patient/{id}"


@pytest.mark.asyncio
async def test_hook_fires_once_per_logical_call_on_final_failure() -> None:
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").mock(
            side_effect=[
                httpx.Response(500, json={"resourceType": "OperationOutcome"}),
                httpx.Response(500, json={"resourceType": "OperationOutcome"}),
                httpx.Response(500, json={"resourceType": "OperationOutcome"}),
            ]
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            with pytest.raises(Exception):
                await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    data = [e for e in events if e.resource_type == "Patient"]
    assert len(data) == 1
    assert data[0].final_status_code == 500 or data[0].final_exception is not None


@pytest.mark.asyncio
async def test_hook_fires_once_even_with_retries() -> None:
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        get_route = mock.get("/fhir/R4/Patient/abc")
        get_route.side_effect = [
            httpx.Response(429, headers={"Retry-After": "0"}, json={}),
            httpx.Response(429, headers={"Retry-After": "0"}, json={}),
            httpx.Response(200, json={"resourceType": "Patient", "id": "abc"}),
        ]
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    data = [e for e in events if e.resource_type == "Patient"]
    assert len(data) == 1
    assert len(data[0].attempts) == 3


@pytest.mark.asyncio
async def test_attempt_number_is_1_indexed() -> None:
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    data = [e for e in events if e.resource_type == "Patient"]
    assert data and data[0].attempts[0].attempt_number == 1


@pytest.mark.asyncio
async def test_hook_exception_is_swallowed_and_warning_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    from pymedplum import AsyncMedplumClient

    def broken(ev: RequestEvent) -> None:
        raise RuntimeError("hook failure")

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=broken,
        )
        try:
            with caplog.at_level(logging.WARNING, logger="pymedplum.hooks"):
                result = await client.read_resource("Patient", "abc")
            assert result is not None
            assert result["id"] == "abc"
            assert any("hook" in r.message.lower() for r in caplog.records)
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_hook_receives_per_attempt_obo_not_snapshot() -> None:
    """Spec: attempts[i].on_behalf_of reflects the OBO value sent on the
    wire at attempt time, not a single snapshot taken at event-fire time.

    We simulate an ambient-OBO change mid-retry by poking the private
    ContextVar from inside the respx handler. The public API
    (``client.on_behalf_of(...)``) cannot model a mid-retry ambient
    change without crossing task boundaries, which would break respx's
    single-request-flow handler model. The hook layer itself still
    reads OBO from the public ``_request_headers`` flow that the
    client uses on every attempt, so this narrow use of private
    state only triggers the scenario — it does not bypass the
    invariant under test.
    """
    attempt_counter = {"n": 0}
    observed_on_wire: list[str | None] = []

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        async with async_hook_client() as (client, events):

            async def handler(request: httpx.Request) -> httpx.Response:
                attempt_counter["n"] += 1
                observed_on_wire.append(
                    request.headers.get("X-Medplum-On-Behalf-Of"),
                )
                if attempt_counter["n"] == 1:
                    # Intentionally pokes private state to simulate a
                    # mid-retry ambient change. See docstring above.
                    client._obo_var.set(None)
                    return httpx.Response(429, headers={"Retry-After": "0"}, json={})
                return httpx.Response(
                    200, json={"resourceType": "Patient", "id": "abc"}
                )

            mock.get("/fhir/R4/Patient/abc").mock(side_effect=handler)
            async with client.on_behalf_of("A"):
                await client.read_resource("Patient", "abc")

    # Wire reality: attempt 1 saw OBO=A, attempt 2 saw OBO cleared.
    assert observed_on_wire == ["ProjectMembership/A", None]

    # Hook attempts must match the wire, not a single post-hoc snapshot.
    data = [e for e in events if e.resource_type == "Patient"]
    assert data
    attempts = data[0].attempts
    assert len(attempts) == 2
    assert attempts[0].on_behalf_of == "ProjectMembership/A"
    assert attempts[1].on_behalf_of is None


@pytest.mark.asyncio
async def test_hook_path_does_not_include_query_string() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get(url__regex=r"/fhir/R4/Patient\?.*").respond(
            json={"resourceType": "Bundle", "entry": []},
        )
        async with async_hook_client() as (client, events):
            await client.search_resources("Patient", {"identifier": "mrn|123"})

    searches = [
        e for e in events if e.resource_type == "Patient" and e.resource_id is None
    ]
    assert searches
    assert "?" not in searches[0].path


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method_call,expected_template",
    [
        ("read", "/fhir/R4/Patient/{id}"),
    ],
)
async def test_hook_path_template_substitutes_ids(
    method_call: str, expected_template: str
) -> None:
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc-123").respond(
            json={"resourceType": "Patient", "id": "abc-123"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            await client.read_resource("Patient", "abc-123")
        finally:
            await client.aclose()

    data = [e for e in events if e.resource_type == "Patient"]
    assert data
    assert data[0].path_template == expected_template


@pytest.mark.asyncio
async def test_hook_path_contains_full_ids_for_audit_fidelity() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/abc-123").respond(
            json={"resourceType": "Patient", "id": "abc-123"},
        )
        async with async_hook_client() as (client, events):
            await client.read_resource("Patient", "abc-123")

    data = [e for e in events if e.resource_type == "Patient"]
    assert data
    assert data[0].path == "/fhir/R4/Patient/abc-123"
    assert data[0].resource_id == "abc-123"


@pytest.mark.asyncio
async def test_hook_query_params_none_for_read() -> None:
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    data = [e for e in events if e.resource_type == "Patient"]
    assert data
    assert data[0].query_params is None


@pytest.mark.asyncio
async def test_hook_query_params_parsed_for_search() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get(url__regex=r"/fhir/R4/Patient\?.*").respond(
            json={"resourceType": "Bundle", "entry": []},
        )
        async with async_hook_client() as (client, events):
            await client.search_resources(
                "Patient", {"identifier": "mrn|123", "_count": "5"}
            )

    searches = [
        e for e in events if e.resource_type == "Patient" and e.resource_id is None
    ]
    assert searches
    qp = searches[0].query_params
    assert qp is not None
    assert qp.get("identifier") == ["mrn|123"]
    assert qp.get("_count") == ["5"]


@pytest.mark.asyncio
async def test_hook_runs_in_caller_task_can_read_contextvar() -> None:
    from pymedplum import AsyncMedplumClient

    actor_var: ContextVar[str | None] = ContextVar("actor", default=None)
    seen: list[str | None] = []

    def hook(ev: RequestEvent) -> None:
        seen.append(actor_var.get())

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            actor_var.set("alice")
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    assert "alice" in seen


@pytest.mark.asyncio
async def test_async_hook_runs_in_caller_task_preserves_context() -> None:
    from pymedplum import AsyncMedplumClient

    actor_var: ContextVar[str | None] = ContextVar("actor2", default=None)
    seen: list[str | None] = []

    async def hook(ev: RequestEvent) -> None:
        seen.append(actor_var.get())

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=hook,
        )
        try:
            actor_var.set("bob")
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    assert "bob" in seen


@pytest.mark.asyncio
async def test_hook_fires_for_oauth_token_fetch() -> None:
    from pymedplum import AsyncMedplumClient

    events: list[RequestEvent] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    templates = [e.path_template for e in events]
    assert "/oauth2/token" in templates
    assert "/fhir/R4/Patient/{id}" in templates


@pytest.mark.asyncio
async def test_hook_auth_event_has_none_resource_fields() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        async with async_hook_client() as (client, events):
            await client.read_resource("Patient", "abc")

    auth = [e for e in events if e.path_template == "/oauth2/token"]
    assert auth
    ev = auth[0]
    assert ev.resource_type is None
    assert ev.resource_id is None
    assert ev.operation is None


@pytest.mark.asyncio
async def test_hook_auth_event_always_has_none_on_behalf_of() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        async with (
            async_hook_client() as (client, events),
            client.on_behalf_of("A"),
        ):
            await client.read_resource("Patient", "abc")

    auth = [e for e in events if e.path_template == "/oauth2/token"]
    assert auth
    for attempt in auth[0].attempts:
        assert attempt.on_behalf_of is None


@pytest.mark.asyncio
async def test_auth_request_sends_no_authorization_header() -> None:
    from pymedplum import AsyncMedplumClient

    captured: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(dict(request.headers))
        return httpx.Response(200, json={"access_token": "t", "expires_in": 3600})

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").mock(side_effect=handler)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    assert captured
    for h in captured:
        keys = {k.lower() for k in h}
        assert "authorization" not in keys


@pytest.mark.asyncio
async def test_auth_request_sends_no_obo_header() -> None:
    from pymedplum import AsyncMedplumClient

    captured: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(dict(request.headers))
        return httpx.Response(200, json={"access_token": "t", "expires_in": 3600})

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").mock(side_effect=handler)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            async with client.on_behalf_of("A"):
                await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

    assert captured
    for h in captured:
        keys = {k.lower() for k in h}
        assert "x-medplum-on-behalf-of" not in keys


@pytest.mark.asyncio
async def test_auth_request_overrides_custom_http_client_default_auth_header() -> None:
    from pymedplum import AsyncMedplumClient

    captured: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(dict(request.headers))
        return httpx.Response(200, json={"access_token": "t", "expires_in": 3600})

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").mock(side_effect=handler)
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        inner = httpx.AsyncClient(headers={"Authorization": "Bearer stale"})
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            http_client=inner,
        )
        try:
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()
            await inner.aclose()

    assert captured
    for h in captured:
        assert h.get("authorization", "").lower() != "bearer stale"


@pytest.mark.asyncio
async def test_async_client_accepts_both_sync_and_async_hook() -> None:
    from pymedplum import AsyncMedplumClient

    sync_events: list[RequestEvent] = []
    async_events: list[RequestEvent] = []

    async def async_hook(ev: RequestEvent) -> None:
        async_events.append(ev)

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        c1 = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=sync_events.append,
        )
        try:
            await c1.read_resource("Patient", "abc")
        finally:
            await c1.aclose()

        c2 = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=async_hook,
        )
        try:
            await c2.read_resource("Patient", "abc")
        finally:
            await c2.aclose()

    assert sync_events
    assert async_events


def test_sync_client_rejects_async_hook_at_construction() -> None:
    from pymedplum import MedplumClient

    async def async_hook(ev: RequestEvent) -> None:
        return None

    with pytest.raises(TypeError):
        MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=async_hook,
        )


# =========================================================================
# Regression guards for Phase 5.1 invariants
# =========================================================================


def test_event_to_phi_audit_dict_is_json_serializable_for_simple_case() -> None:
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    json.dumps(ev.to_phi_audit_dict())


def test_event_to_phi_audit_dict_serializes_exception_as_dict_not_object() -> None:
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=None,
        final_exception=ValueError("x"),
    )
    assert ev.to_phi_audit_dict()["final_exception"] == {
        "type": "ValueError",
        "message": "x",
    }


def test_event_started_at_is_utc_aware() -> None:
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    assert ev.started_at.tzinfo is timezone.utc


def test_event_started_at_preceded_ended_at() -> None:
    start = datetime.now(timezone.utc)
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=start,
        ended_at=start + timedelta(seconds=0.1),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    assert ev.started_at <= ev.ended_at


@pytest.mark.asyncio
async def test_hook_fires_for_export_ccda() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        route = mock.get("/fhir/R4/Patient/abc/$ccda-export").respond(
            200,
            headers={"Content-Type": "application/xml"},
            content=b"<ccda/>",
        )
        async with async_hook_client() as (client, events):
            result = await client.export_ccda("abc")

    assert route.called
    assert result == "<ccda/>"
    wire_events = [e for e in events if e.resource_type == "Patient"]
    assert len(wire_events) == 1
    ev = wire_events[0]
    assert ev.operation == "$ccda-export"
    assert ev.resource_id == "abc"
    assert ev.final_status_code == 200


@pytest.mark.asyncio
async def test_hook_fires_for_download_binary() -> None:
    captured_headers: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_headers.append(dict(request.headers))
        return httpx.Response(
            200,
            headers={"Content-Type": "application/pdf"},
            content=b"%PDF-bytes",
        )

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        route = mock.get("/fhir/R4/Binary/bin-123").mock(side_effect=handler)
        async with async_hook_client() as (client, events):
            content = await client.download_binary("bin-123")

    assert route.called
    assert content == b"%PDF-bytes"
    assert captured_headers[0].get("accept") == "*/*"
    assert "content-type" not in {k.lower() for k in captured_headers[0]}
    wire_events = [e for e in events if e.resource_type == "Binary"]
    assert len(wire_events) == 1
    assert wire_events[0].resource_id == "bin-123"
    assert wire_events[0].final_status_code == 200


@pytest.mark.asyncio
async def test_hook_fires_for_raw_request_escape_hatch() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/admin/projects/proj-1").respond(json={"id": "proj-1"})
        async with async_hook_client() as (client, events):
            result = await client.get("admin/projects/proj-1")

    assert result == {"id": "proj-1"}
    wire_events = [e for e in events if e.path == "/admin/projects/proj-1"]
    assert len(wire_events) == 1
    assert wire_events[0].final_status_code == 200


def test_hook_fires_for_sync_export_ccda() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/abc/$ccda-export").respond(
            200,
            headers={"Content-Type": "application/xml"},
            content=b"<ccda/>",
        )
        with sync_hook_client() as (client, events):
            result = client.export_ccda("abc")

    assert result == "<ccda/>"
    wire_events = [e for e in events if e.resource_type == "Patient"]
    assert len(wire_events) == 1
    assert wire_events[0].operation == "$ccda-export"


def test_hook_fires_for_sync_download_binary() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Binary/bin-123").respond(
            200,
            headers={"Content-Type": "application/pdf"},
            content=b"%PDF-bytes",
        )
        with sync_hook_client() as (client, events):
            content = client.download_binary("bin-123")

    assert content == b"%PDF-bytes"
    wire_events = [e for e in events if e.resource_type == "Binary"]
    assert len(wire_events) == 1
    assert wire_events[0].resource_id == "bin-123"


@pytest.mark.parametrize(
    (
        "method",
        "path",
        "resource_type",
        "resource_id",
        "operation",
        "expected_action",
    ),
    [
        ("GET", "/fhir/R4/Patient/p-1", "Patient", "p-1", None, "read"),
        ("GET", "/fhir/R4/Patient", "Patient", None, None, "search"),
        ("POST", "/fhir/R4/Patient", "Patient", None, None, "create"),
        ("PUT", "/fhir/R4/Patient/p-1", "Patient", "p-1", None, "update"),
        ("PATCH", "/fhir/R4/Patient/p-1", "Patient", "p-1", None, "patch"),
        ("DELETE", "/fhir/R4/Patient/p-1", "Patient", "p-1", None, "delete"),
        (
            "POST",
            "/fhir/R4/Patient/p-1/$everything",
            "Patient",
            "p-1",
            "$everything",
            "operation",
        ),
        (
            "POST",
            "/fhir/R4/Patient/$match",
            "Patient",
            None,
            "$match",
            "operation",
        ),
        (
            "POST",
            "/fhir/R4/Bot/bot-1/$execute",
            "Bot",
            "bot-1",
            "$execute",
            "operation",
        ),
        (
            "GET",
            "/fhir/R4/Patient/p-1/$ccda-export",
            "Patient",
            "p-1",
            "$ccda-export",
            "operation",
        ),
        ("POST", "/fhir/R4/Binary", "Binary", None, None, "create"),
        ("GET", "/fhir/R4/Binary/bin-1", "Binary", "bin-1", None, "read"),
        ("POST", "/fhir/R4/", None, None, None, "batch_or_transaction"),
        ("POST", "/oauth2/token", None, None, None, None),
        ("GET", "/healthcheck", None, None, None, None),
        ("HEAD", "/fhir/R4/Patient/p-1", "Patient", "p-1", None, None),
        ("OPTIONS", "/fhir/R4/Patient", "Patient", None, None, None),
    ],
)
def test_compute_action_covers_all_supported_request_shapes(
    method, path, resource_type, resource_id, operation, expected_action
) -> None:
    assert (
        _compute_action(
            method=method,
            path=path,
            resource_type=resource_type,
            resource_id=resource_id,
            operation=operation,
            fhir_url_path="fhir/R4/",
        )
        == expected_action
    )


def test_compute_action_classifies_bundle_post_under_configured_prefix() -> None:
    assert (
        _compute_action(
            method="POST",
            path="/fhir/R4B/",
            resource_type=None,
            resource_id=None,
            operation=None,
            fhir_url_path="fhir/R4B/",
        )
        == "batch_or_transaction"
    )


def test_compute_action_returns_none_when_path_is_outside_configured_prefix() -> None:
    assert (
        _compute_action(
            method="POST",
            path="/fhir/R4B/",
            resource_type=None,
            resource_id=None,
            operation=None,
            fhir_url_path="fhir/R4/",
        )
        is None
    )


def test_compute_action_falls_back_to_default_fhir_prefix_when_unset() -> None:
    assert (
        _compute_action(
            method="POST",
            path="/fhir/R5/",
            resource_type=None,
            resource_id=None,
            operation=None,
            fhir_url_path=None,
        )
        == "batch_or_transaction"
    )


@pytest.mark.parametrize(
    ("status", "exception", "expected_outcome"),
    [
        (200, None, "success"),
        (201, None, "success"),
        (204, None, "success"),
        (304, None, "success"),
        (400, None, "error"),
        (404, None, "error"),
        (500, None, "error"),
        (None, None, "error"),
        (200, RuntimeError("boom"), "error"),
        (None, RuntimeError("boom"), "error"),
    ],
)
def test_compute_outcome_classifies_success_vs_error(
    status, exception, expected_outcome
) -> None:
    assert (
        _compute_outcome(final_status_code=status, final_exception=exception)
        == expected_outcome
    )


def test_request_event_defaults_action_and_outcome_for_hand_constructed_events() -> (
    None
):
    ev = RequestEvent(
        method="GET",
        path="/p",
        path_template="/p",
        query_params=None,
        resource_type=None,
        resource_id=None,
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
    )
    assert ev.action is None
    assert ev.outcome == "error"


def test_to_phi_audit_dict_includes_action_and_outcome() -> None:
    ev = RequestEvent(
        method="GET",
        path="/fhir/R4/Patient/p-1",
        path_template="/fhir/R4/Patient/{id}",
        query_params=None,
        resource_type="Patient",
        resource_id="p-1",
        operation=None,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=200,
        final_exception=None,
        action="read",
        outcome="success",
    )
    payload = ev.to_phi_audit_dict()
    assert payload["action"] == "read"
    assert payload["outcome"] == "success"


def test_to_non_phi_dict_includes_action_and_outcome() -> None:
    ev = RequestEvent(
        method="POST",
        path="/fhir/R4/Patient/p-1/$everything",
        path_template="/fhir/R4/Patient/{id}/$everything",
        query_params=None,
        resource_type="Patient",
        resource_id="p-1",
        operation="$everything",
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        attempts=[],
        final_status_code=500,
        final_exception=None,
        action="operation",
        outcome="error",
    )
    payload = ev.to_non_phi_dict()
    assert payload["action"] == "operation"
    assert payload["outcome"] == "error"


def test_serialize_exception_returns_none_for_none_input() -> None:
    assert serialize_exception(None) is None


def test_serialize_exception_returns_type_and_message_for_plain_exception() -> None:
    assert serialize_exception(ValueError("bad")) == {
        "type": "ValueError",
        "message": "bad",
    }


def test_serialize_exception_honors_sanitize_for_logging_when_present() -> None:
    class _SanitizingError(Exception):
        def sanitize_for_logging(self) -> dict[str, Any]:
            return {"type": "MedplumHTTPError", "status": 404}

    payload = serialize_exception(_SanitizingError("would-leak/PHI/path"))
    assert payload == {"type": "MedplumHTTPError", "status": 404}


def test_serialize_exception_falls_back_to_str_when_sanitizer_returns_non_dict() -> (
    None
):
    class _BadSanitizerError(Exception):
        def sanitize_for_logging(self) -> str:  # type: ignore[override]
            return "not-a-dict"

    payload = serialize_exception(_BadSanitizerError("msg"))
    assert payload == {"type": "_BadSanitizerError", "message": "msg"}


def test_underscored_alias_remains_for_backwards_compatibility() -> None:
    from pymedplum.hooks import _serialize_exception, serialize_exception

    assert _serialize_exception is serialize_exception


def test_sync_client_populates_action_for_read() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/p-1").respond(
            200, json={"resourceType": "Patient", "id": "p-1"}
        )
        with sync_hook_client() as (client, events):
            client.read_resource("Patient", "p-1")

    fhir_events = [e for e in events if e.resource_type == "Patient"]
    assert len(fhir_events) == 1
    assert fhir_events[0].action == "read"
    assert fhir_events[0].outcome == "success"


def test_sync_client_populates_action_for_search() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient").respond(
            200, json={"resourceType": "Bundle", "entry": []}
        )
        with sync_hook_client() as (client, events):
            client.search_resources("Patient", {"identifier": "mrn|123"})

    fhir_events = [e for e in events if e.resource_type == "Patient"]
    assert len(fhir_events) == 1
    assert fhir_events[0].action == "search"


def test_sync_client_populates_action_for_bot_execute() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.post("/fhir/R4/Bot/bot-1/$execute").respond(200, json={"ok": True})
        with sync_hook_client() as (client, events):
            client.execute_bot(bot_id="bot-1", input_data={"x": 1})

    fhir_events = [e for e in events if e.resource_type == "Bot"]
    assert len(fhir_events) == 1
    assert fhir_events[0].action == "operation"
    assert fhir_events[0].operation == "$execute"


def test_sync_client_populates_action_for_ccda_export() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/p-1/$ccda-export").respond(
            200, headers={"Content-Type": "application/xml"}, content=b"<XML/>"
        )
        with sync_hook_client() as (client, events):
            client.export_ccda("p-1")

    fhir_events = [e for e in events if e.resource_type == "Patient"]
    assert len(fhir_events) == 1
    assert fhir_events[0].action == "operation"
    assert fhir_events[0].operation == "$ccda-export"


def test_sync_client_populates_action_for_binary_upload() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.post("/fhir/R4/Binary").respond(
            200, json={"resourceType": "Binary", "id": "bin-1"}
        )
        with sync_hook_client() as (client, events):
            client.upload_binary(b"%PDF-bytes", "application/pdf")

    fhir_events = [e for e in events if e.resource_type == "Binary"]
    assert len(fhir_events) == 1
    assert fhir_events[0].action == "create"


def test_sync_client_populates_action_for_binary_download() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Binary/bin-1").respond(
            200, headers={"Content-Type": "application/pdf"}, content=b"x"
        )
        with sync_hook_client() as (client, events):
            client.download_binary("bin-1")

    fhir_events = [e for e in events if e.resource_type == "Binary"]
    assert len(fhir_events) == 1
    assert fhir_events[0].action == "read"


def test_sync_client_populates_outcome_error_for_5xx() -> None:
    from pymedplum.exceptions import ServerError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/p-1").respond(500, json={})
        with sync_hook_client() as (client, events), pytest.raises(ServerError):
            client.read_resource("Patient", "p-1")

    fhir_events = [e for e in events if e.resource_type == "Patient"]
    assert len(fhir_events) == 1
    assert fhir_events[0].outcome == "error"


def test_sync_client_classifies_token_endpoint_as_non_fhir() -> None:
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(json=TOKEN_RESPONSE)
        mock.get("/fhir/R4/Patient/p-1").respond(
            200, json={"resourceType": "Patient", "id": "p-1"}
        )
        with sync_hook_client() as (client, events):
            client.read_resource("Patient", "p-1")

    auth_events = [e for e in events if "/oauth2/" in e.path]
    assert len(auth_events) == 1
    assert auth_events[0].action is None
    assert auth_events[0].outcome == "success"
