"""PHI-in-logs invariants for pymedplum.*.

Enabling ``logging.getLogger("pymedplum").setLevel(DEBUG)`` must produce a
useful trace of auth + request lifecycle events while never interpolating:
  - bearer tokens / client secrets
  - ``X-Medplum-On-Behalf-Of`` identifiers (ProjectMembership IDs)
  - FHIR resource IDs, MRNs, or other search criteria
  - raw query strings

Logs are safe to emit for: status codes, durations, ``path_template``
(IDs replaced with ``{id}``), exception class names, cooldown remaining
seconds, and internal counters.
"""

from __future__ import annotations

import contextlib
import json
import logging
import time

import httpx
import pytest
import respx

BEARER = "super-secret-bearer-tok"
OBO_ID = "secret-membership-id"
OBO = f"ProjectMembership/{OBO_ID}"
RESOURCE_ID = "patient-uuid-abc123"
QS_VALUE = "search-secret-mrn-789"

MRN_IN_DIAGNOSTICS = "MRN-7724-SECRET"
NAME_IN_DETAILS_TEXT = "BOB-SENSITIVE"
CLIENT_SECRET_SENTINEL = "THIS-SHALL-NOT-APPEAR-IN-LOGS"


@pytest.fixture
def capture_all_pymedplum_logs(caplog):
    caplog.set_level(logging.DEBUG, logger="pymedplum")
    return caplog


@pytest.mark.asyncio
async def test_no_bearer_or_obo_or_resource_id_or_query_in_logs(
    capture_all_pymedplum_logs,
):
    from pymedplum import AsyncMedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": BEARER, "expires_in": 3600},
        )
        mock.get(f"/fhir/R4/Patient/{RESOURCE_ID}").respond(
            json={"resourceType": "Patient", "id": RESOURCE_ID},
        )
        mock.get("/fhir/R4/Patient").respond(
            json={"resourceType": "Bundle", "entry": []},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            async with client.on_behalf_of(OBO):
                await client.read_resource("Patient", RESOURCE_ID)
                await client.search_resources("Patient", {"identifier": QS_VALUE})
        finally:
            await client.aclose()

    records = capture_all_pymedplum_logs.records
    joined = "\n".join(r.getMessage() for r in records)
    assert BEARER not in joined
    assert OBO not in joined
    assert OBO_ID not in joined
    assert RESOURCE_ID not in joined
    assert QS_VALUE not in joined


def test_cooldown_entered_is_warning_level(caplog):
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(500)
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            failed_refresh_cooldown=5.0,
        )
        try:
            with (
                caplog.at_level(logging.WARNING, logger="pymedplum.auth"),
                contextlib.suppress(Exception),
            ):
                client.read_resource("Patient", "abc")
            warnings_ = [
                r
                for r in caplog.records
                if r.levelno == logging.WARNING and r.name == "pymedplum.auth"
            ]
            assert any("cooldown" in r.getMessage().lower() for r in warnings_)
        finally:
            client.close()


def test_recovery_after_failure_logs_info(caplog):
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token = mock.post("/oauth2/token")
        token.side_effect = [
            httpx.Response(500),
            httpx.Response(200, json={"access_token": "t", "expires_in": 3600}),
        ]
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            failed_refresh_cooldown=0.02,
        )
        try:
            with caplog.at_level(logging.INFO, logger="pymedplum.auth"):
                with contextlib.suppress(Exception):
                    client.read_resource("Patient", "abc")
                time.sleep(0.2)
                client.read_resource("Patient", "abc")
            infos = [
                r
                for r in caplog.records
                if r.levelno == logging.INFO and r.name == "pymedplum.auth"
            ]
            assert any("recovered" in r.getMessage().lower() for r in infos)
        finally:
            client.close()


def test_path_template_appears_in_request_debug_log(capture_all_pymedplum_logs):
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            client.read_resource("Patient", "abc")
        finally:
            client.close()

    messages = [
        r.getMessage()
        for r in capture_all_pymedplum_logs.records
        if r.name == "pymedplum.request"
    ]
    assert any("{id}" in m for m in messages)
    # The raw resource id must never appear in request logs.
    joined = "\n".join(messages)
    assert "Patient/abc" not in joined


def test_routine_refresh_success_logs_debug_not_info(capture_all_pymedplum_logs):
    """Fresh client + single successful refresh -> no INFO "recovered" log."""
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            client.read_resource("Patient", "abc")
        finally:
            client.close()
    infos = [
        r
        for r in capture_all_pymedplum_logs.records
        if r.levelno == logging.INFO and r.name == "pymedplum.auth"
    ]
    assert not any("recovered" in r.getMessage().lower() for r in infos)


@pytest.fixture
def cooldown_client_and_records(caplog):
    """Drive a client into cooldown + a second attempt still inside cooldown.

    Yields (first_attempt_records, second_attempt_records). Each is a list
    of LogRecord scoped to ``pymedplum.auth`` for that attempt.
    """
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(500)
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            failed_refresh_cooldown=60.0,
        )
        try:
            with caplog.at_level(logging.DEBUG, logger="pymedplum.auth"):
                with contextlib.suppress(Exception):
                    client.read_resource("Patient", "abc")
                first = [r for r in caplog.records if r.name == "pymedplum.auth"]
                caplog.clear()
                with contextlib.suppress(Exception):
                    client.read_resource("Patient", "abc")
                second = [r for r in caplog.records if r.name == "pymedplum.auth"]
                yield first, second
        finally:
            client.close()


def test_initial_cooldown_entry_logs_warning(cooldown_client_and_records):
    first, _ = cooldown_client_and_records
    warnings_ = [r for r in first if r.levelno == logging.WARNING]
    assert len(warnings_) >= 1


def test_repeated_cooldown_hits_do_not_log_warning(cooldown_client_and_records):
    _, second = cooldown_client_and_records
    warnings_ = [r for r in second if r.levelno == logging.WARNING]
    assert warnings_ == []


def test_repeated_cooldown_hits_log_debug(cooldown_client_and_records):
    _, second = cooldown_client_and_records
    debugs = [r for r in second if r.levelno == logging.DEBUG]
    assert any("cooldown" in r.getMessage().lower() for r in debugs)


def test_request_debug_log_includes_status_and_duration(
    capture_all_pymedplum_logs,
):
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            client.read_resource("Patient", "abc")
        finally:
            client.close()

    messages = [
        r.getMessage()
        for r in capture_all_pymedplum_logs.records
        if r.name == "pymedplum.request"
    ]
    joined = "\n".join(messages)
    assert "status 200" in joined
    assert "completed" in joined
    assert any("(attempt 1)" in m for m in messages)


def test_retry_scheduled_log_names_reason(capture_all_pymedplum_logs):
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        route = mock.get("/fhir/R4/Patient/abc")
        route.side_effect = [
            httpx.Response(503),
            httpx.Response(200, json={"resourceType": "Patient", "id": "abc"}),
        ]
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            client.read_resource("Patient", "abc")
        finally:
            client.close()

    messages = [
        r.getMessage()
        for r in capture_all_pymedplum_logs.records
        if r.name == "pymedplum.request"
    ]
    joined = "\n".join(messages)
    assert "retry scheduled" in joined
    assert "5xx" in joined


def test_security_if_none_exist_warning_omits_query_and_path(caplog):
    from pymedplum._security import sanitize_if_none_exist

    with caplog.at_level(logging.WARNING, logger="pymedplum.security"):
        sanitize_if_none_exist(
            "https://api.medplum.com/fhir/R4/Patient?identifier=mrn|SECRET123",
            "https://api.medplum.com/",
        )

    warnings_ = [
        r
        for r in caplog.records
        if r.levelno == logging.WARNING and r.name == "pymedplum.security"
    ]
    assert warnings_
    joined = "\n".join(r.getMessage() for r in warnings_)
    assert "SECRET123" not in joined
    assert "/fhir/R4/Patient" not in joined
    assert "identifier=" not in joined


def test_before_request_hook_dispatch_is_debug(capture_all_pymedplum_logs):
    from pymedplum import MedplumClient

    def before(req):
        return None

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            before_request=before,
        )
        try:
            client.read_resource("Patient", "abc")
        finally:
            client.close()

    hooks_msgs = [
        r.getMessage()
        for r in capture_all_pymedplum_logs.records
        if r.name == "pymedplum.hooks"
    ]
    assert any("before_request" in m for m in hooks_msgs)


def test_token_acquired_log_does_not_include_token(capture_all_pymedplum_logs):
    from pymedplum import MedplumClient

    secret_token = "totally-secret-access-token"
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": secret_token, "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
        )
        try:
            client.read_resource("Patient", "abc")
        finally:
            client.close()

    auth_msgs = [
        r.getMessage()
        for r in capture_all_pymedplum_logs.records
        if r.name == "pymedplum.auth"
    ]
    joined = "\n".join(auth_msgs)
    assert secret_token not in joined
    assert any("acquired new token" in m for m in auth_msgs)


@pytest.fixture
async def trigger_400_with_phi(caplog):
    from pymedplum import AsyncMedplumClient, BadRequestError

    events = []

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600}
        )
        bad_body = {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "invalid",
                    "diagnostics": (
                        f"Patient {MRN_IN_DIAGNOSTICS} cohort check failed"
                    ),
                    "details": {"text": f"Subject name was {NAME_IN_DETAILS_TEXT}"},
                }
            ],
        }
        mock.post("/fhir/R4/Patient").respond(400, json=bad_body)

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            with (
                caplog.at_level(logging.DEBUG, logger="pymedplum"),
                pytest.raises(BadRequestError) as ei,
            ):
                await client.create_resource({"resourceType": "Patient"})
        finally:
            await client.aclose()
    yield ei.value, events, caplog


@pytest.mark.asyncio
async def test_phi_in_400_error_does_not_leak_into_exception_str(
    trigger_400_with_phi,
):
    exc, _, _ = trigger_400_with_phi
    s = str(exc)
    assert MRN_IN_DIAGNOSTICS not in s
    assert NAME_IN_DETAILS_TEXT not in s


@pytest.mark.asyncio
async def test_phi_in_400_error_does_not_leak_into_logs(trigger_400_with_phi):
    _, _, caplog = trigger_400_with_phi
    joined_logs = "\n".join(r.getMessage() for r in caplog.records)
    assert MRN_IN_DIAGNOSTICS not in joined_logs
    assert NAME_IN_DETAILS_TEXT not in joined_logs


@pytest.mark.asyncio
async def test_phi_in_400_error_does_not_leak_into_hook_event(
    trigger_400_with_phi,
):
    _, events, _ = trigger_400_with_phi
    data_events = [e for e in events if e.resource_type == "Patient"]
    assert data_events, "hook did not fire for the failed request"
    for e in data_events:
        serialized = json.dumps(e.to_phi_audit_dict())
        assert MRN_IN_DIAGNOSTICS not in serialized
        assert NAME_IN_DETAILS_TEXT not in serialized


@pytest.fixture
async def trigger_500_with_phi(caplog):
    from pymedplum import AsyncMedplumClient, ServerError

    events = []

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600}
        )
        mock.get("/fhir/R4/Patient/SECRET-PATIENT-ID").respond(
            500, text=f"stack trace mentioning MRN {MRN_IN_DIAGNOSTICS}"
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="c",
            client_secret="s",
            on_request_complete=events.append,
        )
        try:
            with (
                caplog.at_level(logging.DEBUG, logger="pymedplum"),
                pytest.raises(ServerError) as ei,
            ):
                await client.read_resource("Patient", "SECRET-PATIENT-ID")
        finally:
            await client.aclose()
    yield ei.value, events, caplog


@pytest.mark.asyncio
async def test_phi_in_500_error_does_not_leak_into_exception_str(
    trigger_500_with_phi,
):
    exc, _, _ = trigger_500_with_phi
    s = str(exc)
    assert "SECRET-PATIENT-ID" not in s
    assert MRN_IN_DIAGNOSTICS not in s


@pytest.mark.asyncio
async def test_phi_in_500_error_sanitize_for_logging_is_clean(
    trigger_500_with_phi,
):
    exc, _, _ = trigger_500_with_phi
    safe_str = json.dumps(exc.sanitize_for_logging())
    assert "SECRET-PATIENT-ID" not in safe_str
    assert MRN_IN_DIAGNOSTICS not in safe_str


@pytest.mark.asyncio
async def test_phi_in_500_error_does_not_leak_into_logs(trigger_500_with_phi):
    _, _, caplog = trigger_500_with_phi
    joined_logs = "\n".join(r.getMessage() for r in caplog.records)
    assert "SECRET-PATIENT-ID" not in joined_logs
    assert MRN_IN_DIAGNOSTICS not in joined_logs


@pytest.mark.asyncio
async def test_phi_in_500_error_hook_final_exception_is_clean(
    trigger_500_with_phi,
):
    from pymedplum.hooks import serialize_exception

    _, events, _ = trigger_500_with_phi
    data_events = [e for e in events if e.path_template == "/fhir/R4/Patient/{id}"]
    assert data_events, "hook did not fire for the 500"
    serialized_excs = [
        json.dumps(serialize_exception(e.final_exception))
        for e in data_events
        if e.final_exception is not None
    ]
    assert serialized_excs, "expected at least one attempt with final_exception"
    for serialized in serialized_excs:
        assert "SECRET-PATIENT-ID" not in serialized
        assert MRN_IN_DIAGNOSTICS not in serialized


def test_client_secret_never_in_logs(caplog):
    """Constructor-supplied client_secret never lands in any pymedplum log."""
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600}
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"}
        )

        with caplog.at_level(logging.DEBUG, logger="pymedplum"):
            client = MedplumClient(
                base_url="https://api.medplum.com/",
                client_id="c",
                client_secret=CLIENT_SECRET_SENTINEL,
            )
            try:
                client.read_resource("Patient", "abc")
            finally:
                client.close()

    joined = "\n".join(r.getMessage() for r in caplog.records)
    assert CLIENT_SECRET_SENTINEL not in joined
