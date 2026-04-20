"""TDD-first tests for _auth.py. Each test drives the minimum code required."""

from __future__ import annotations

import asyncio
import concurrent.futures
import time
from datetime import timedelta
from typing import Any

import httpx
import pytest
import respx

TOKEN_URL = "https://api.medplum.com/oauth2/token"
FHIR_URL = "https://api.medplum.com/fhir/R4/Patient/abc"


@pytest.mark.asyncio
async def test_fresh_client_authenticates_on_first_request() -> None:
    from pymedplum import AsyncMedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "tok-1", "expires_in": 3600},
        )
        read_route = mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:
            result = await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

        assert token_route.called
        assert read_route.called
        auth_header = read_route.calls[0].request.headers.get("Authorization")
        assert auth_header == "Bearer tok-1"
        assert result["id"] == "abc"


@pytest.mark.asyncio
async def test_concurrent_refresh_only_fires_once_async() -> None:
    from pymedplum import AsyncMedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "tok-1", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:
            await asyncio.gather(
                *[client.read_resource("Patient", "abc") for _ in range(20)]
            )
        finally:
            await client.aclose()

        assert token_route.call_count == 1


@pytest.mark.asyncio
async def test_concurrent_first_request_on_fresh_client_async() -> None:
    from pymedplum import AsyncMedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "tok-1", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:
            results = await asyncio.gather(
                *[client.read_resource("Patient", "abc") for _ in range(10)]
            )
        finally:
            await client.aclose()

        assert token_route.call_count == 1
        assert all(r["id"] == "abc" for r in results)


def test_concurrent_refresh_only_fires_once_threaded() -> None:
    from pymedplum import MedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "tok-1", "expires_in": 3600},
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )

        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
                futures = [
                    pool.submit(client.read_resource, "Patient", "abc")
                    for _ in range(10)
                ]
                for f in futures:
                    f.result()
        finally:
            client.close()

        assert token_route.call_count == 1


@pytest.mark.asyncio
async def test_cooldown_raises_token_refresh_cooldown_error_async() -> None:
    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import MedplumError, TokenRefreshCooldownError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(500, text="oauth boom")
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=10.0,
        )
        try:
            with pytest.raises(MedplumError):
                await client.read_resource("Patient", "abc")
            with pytest.raises(TokenRefreshCooldownError) as ei:
                await client.read_resource("Patient", "abc")
            assert ei.value.retry_after > 0
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_cooldown_raises_on_force_refresh_async() -> None:
    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import MedplumError, TokenRefreshCooldownError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(500, text="boom")
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=10.0,
        )
        try:
            with pytest.raises(MedplumError):
                await client._tokens.force_refresh(client._http)
            with pytest.raises(TokenRefreshCooldownError):
                await client._tokens.force_refresh(client._http)
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_cooldown_retry_after_property_accurate() -> None:
    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import MedplumError, TokenRefreshCooldownError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(500, text="boom")
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=5.0,
        )
        try:
            with pytest.raises(MedplumError):
                await client.read_resource("Patient", "abc")
            await asyncio.sleep(0.1)
            with pytest.raises(TokenRefreshCooldownError) as ei:
                await client.read_resource("Patient", "abc")
            # Should be close to 5.0 - 0.1 = ~4.9s remaining
            assert 4.0 < ei.value.retry_after < 5.0
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_cooldown_cleared_after_success_async() -> None:
    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import MedplumError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token = mock.post("/oauth2/token")
        token.side_effect = [
            httpx.Response(500, text="boom"),
            httpx.Response(200, json={"access_token": "tok-1", "expires_in": 3600}),
        ]
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=0.02,
        )
        try:
            with pytest.raises(MedplumError):
                await client.read_resource("Patient", "abc")
            await asyncio.sleep(0.2)
            result = await client.read_resource("Patient", "abc")
            assert result["id"] == "abc"
            assert client._tokens.failed_refresh_at is None
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_acquire_token_failure_does_not_mutate_state() -> None:
    import json as _json

    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import MedplumError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(200, text="not json at all")
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=10.0,
        )
        try:
            # Malformed token response surfaces as either a wrapped
            # MedplumError or the raw JSONDecodeError depending on
            # where auth caught it.
            with pytest.raises((MedplumError, _json.JSONDecodeError)):
                await client.read_resource("Patient", "abc")
            assert client._tokens.access_token is None
            assert client._tokens.token_expires_at is None
            assert client._tokens.failed_refresh_at is not None
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_acquire_token_failure_sets_cooldown_under_lock() -> None:
    from pymedplum import AsyncMedplumClient
    from pymedplum.exceptions import TokenRefreshCooldownError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(500, text="boom")
        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=10.0,
        )
        try:
            results = await asyncio.gather(
                *[client.read_resource("Patient", "abc") for _ in range(5)],
                return_exceptions=True,
            )
            # At least one saw the primary failure; subsequent racers see
            # the cooldown that was set atomically under the lock.
            assert any(isinstance(r, Exception) for r in results)
            assert client._tokens.failed_refresh_at is not None

            # Any subsequent attempt must hit the cooldown guard.
            with pytest.raises(TokenRefreshCooldownError):
                await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_async_refresh_cancellation_does_not_set_cooldown() -> None:
    from pymedplum._auth import AsyncTokenManager, TokenSource

    class HangingAsyncClient:
        def build_request(self, *args: Any, **kwargs: Any) -> httpx.Request:
            return httpx.Request("POST", "https://api.medplum.com/oauth2/token")

        async def send(self, *args: Any, **kwargs: Any) -> httpx.Response:
            await asyncio.Event().wait()
            raise AssertionError("unreachable")

    manager = AsyncTokenManager(
        client_id="cid",
        client_secret="cs",
        token_url="https://api.medplum.com/oauth2/token",
        source=TokenSource.MANAGED,
        failed_refresh_cooldown=timedelta(seconds=30),
    )

    task = asyncio.create_task(manager._acquire_token(HangingAsyncClient()))
    await asyncio.sleep(0.05)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert manager.failed_refresh_at is None


@pytest.mark.asyncio
async def test_async_refresh_timeout_surfaces_medplum_error() -> None:
    from pymedplum._auth import AsyncTokenManager, TokenSource
    from pymedplum.exceptions import MedplumError

    class HangingAsyncClient:
        def build_request(self, *args: Any, **kwargs: Any) -> httpx.Request:
            return httpx.Request("POST", "https://api.medplum.com/oauth2/token")

        async def send(self, *args: Any, **kwargs: Any) -> httpx.Response:
            await asyncio.Event().wait()
            raise AssertionError("unreachable")

    manager = AsyncTokenManager(
        client_id="cid",
        client_secret="cs",
        token_url="https://api.medplum.com/oauth2/token",
        source=TokenSource.MANAGED,
        _refresh_timeout_seconds=0.1,
    )

    with pytest.raises(MedplumError, match="did not complete within"):
        await manager.ensure_authenticated(HangingAsyncClient())


@pytest.mark.asyncio
async def test_refresh_task_not_cleared_while_in_flight_async() -> None:
    from pymedplum._auth import AsyncTokenManager, TokenSource

    gate = asyncio.Event()
    call_counter = {"n": 0}

    async def gated_handler(request: httpx.Request) -> httpx.Response:
        call_counter["n"] += 1
        await gate.wait()
        return httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").mock(side_effect=gated_handler)
        async with httpx.AsyncClient() as http:
            manager = AsyncTokenManager(
                client_id="cid",
                client_secret="cs",
                token_url="https://api.medplum.com/oauth2/token",
                source=TokenSource.MANAGED,
                _refresh_timeout_seconds=5.0,
            )

            waiter_a = asyncio.create_task(manager.ensure_authenticated(http))
            await asyncio.sleep(0.05)
            waiter_a.cancel()
            with pytest.raises(asyncio.CancelledError):
                await waiter_a

            waiter_b = asyncio.create_task(manager.ensure_authenticated(http))
            await asyncio.sleep(0.05)
            gate.set()
            await waiter_b

            assert manager.access_token == "tok"
            # One POST fired despite two waiters.
            assert call_counter["n"] == 1


@pytest.mark.asyncio
async def test_obo_isolation_across_async_tasks() -> None:
    from pymedplum import AsyncMedplumClient

    seen: list[str | None] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "tok", "expires_in": 3600}
        )

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request.headers.get("X-Medplum-On-Behalf-Of"))
            return httpx.Response(200, json={"resourceType": "Patient", "id": "x"})

        mock.get("/fhir/R4/Patient/x").mock(side_effect=handler)

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:

            async def task_a() -> None:
                async with client.on_behalf_of("A"):
                    await client.read_resource("Patient", "x")

            async def task_b() -> None:
                async with client.on_behalf_of("B"):
                    await client.read_resource("Patient", "x")

            await asyncio.gather(task_a(), task_b())
        finally:
            await client.aclose()

        assert set(seen) == {"ProjectMembership/A", "ProjectMembership/B"}


@pytest.mark.asyncio
async def test_obo_kwarg_overrides_context() -> None:
    from pymedplum import AsyncMedplumClient

    seen: list[str | None] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600}
        )

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request.headers.get("X-Medplum-On-Behalf-Of"))
            return httpx.Response(200, json={"resourceType": "Patient", "id": "x"})

        mock.get("/fhir/R4/Patient/x").mock(side_effect=handler)

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:
            async with client.on_behalf_of("A"):
                await client.read_resource("Patient", "x", on_behalf_of="B")
        finally:
            await client.aclose()
        assert seen == ["ProjectMembership/B"]


@pytest.mark.asyncio
async def test_obo_explicit_empty_string_clears_context() -> None:
    from pymedplum import AsyncMedplumClient

    seen: list[str | None] = []
    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "t", "expires_in": 3600}
        )

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request.headers.get("X-Medplum-On-Behalf-Of"))
            return httpx.Response(200, json={"resourceType": "Patient", "id": "x"})

        mock.get("/fhir/R4/Patient/x").mock(side_effect=handler)

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:
            async with client.on_behalf_of("A"):
                await client.read_resource("Patient", "x", on_behalf_of="")
        finally:
            await client.aclose()
        assert seen == [None]


def test_obo_isolation_across_client_instances() -> None:
    from pymedplum import MedplumClient

    c1 = MedplumClient(
        base_url="https://api.medplum.com/", client_id="c1", client_secret="s"
    )
    c2 = MedplumClient(
        base_url="https://api.medplum.com/", client_id="c2", client_secret="s"
    )
    try:
        with c1.on_behalf_of("A"):
            # Manually setting a stack value on c1 must not be visible from c2.
            assert c1._obo_var.get() == "ProjectMembership/A"
            assert c2._obo_var.get() is None
    finally:
        c1.close()
        c2.close()


@pytest.mark.asyncio
async def test_nested_obo_scopes_unwind_correctly() -> None:
    from pymedplum import AsyncMedplumClient

    client = AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        access_token="t",
    )
    try:
        assert client._obo_var.get() is None
        async with client.on_behalf_of("A"):
            assert client._obo_var.get() == "ProjectMembership/A"
            async with client.on_behalf_of("B"):
                assert client._obo_var.get() == "ProjectMembership/B"
            assert client._obo_var.get() == "ProjectMembership/A"
        assert client._obo_var.get() is None
    finally:
        await client.aclose()


def test_obo_context_exit_without_enter_is_noop() -> None:
    from contextvars import ContextVar

    from pymedplum._auth import OnBehalfOfContext as Ctx

    var: ContextVar[str | None] = ContextVar("noop", default=None)
    ctx = Ctx(var, "x")
    # Exit before enter — should not raise, should not mutate.
    ctx.__exit__(None, None, None)
    assert var.get() is None


@pytest.mark.asyncio
async def test_obo_context_cross_task_boundary_logs_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    import logging
    from contextvars import ContextVar

    from pymedplum._auth import OnBehalfOfContext as Ctx

    var: ContextVar[str | None] = ContextVar("cross", default=None)
    ctx: Ctx | None = None

    async def enter_in_task() -> None:
        nonlocal ctx
        ctx = Ctx(var, "A")
        ctx.__enter__()

    await asyncio.create_task(enter_in_task())

    assert ctx is not None
    with caplog.at_level(logging.WARNING, logger="pymedplum.auth"):
        ctx.__exit__(None, None, None)

    assert any("OnBehalfOfContext" in record.message for record in caplog.records)


@pytest.mark.asyncio
async def test_reactive_refresh_on_401_for_unparsed_expiry() -> None:
    """Managed token with no parseable expiry: first request hits 401,
    SDK forces refresh and retries once successfully.
    """
    from pymedplum import AsyncMedplumClient

    with respx.mock(base_url="https://api.medplum.com") as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "tok-fresh", "expires_in": 3600}
        )

        call_state = {"n": 0}

        def read_handler(request: httpx.Request) -> httpx.Response:
            call_state["n"] += 1
            auth = request.headers.get("Authorization", "")
            # First call returns 401 with the pre-seeded stale token.
            if call_state["n"] == 1:
                assert auth == "Bearer stale", f"unexpected auth: {auth}"
                return httpx.Response(401, text="token expired")
            # Second call sees the force-refreshed token.
            assert auth == "Bearer tok-fresh", f"unexpected auth: {auth}"
            return httpx.Response(200, json={"resourceType": "Patient", "id": "abc"})

        mock.get("/fhir/R4/Patient/abc").mock(side_effect=read_handler)

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            access_token="stale",  # dual-cred → MANAGED
        )
        try:
            result = await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

        assert result["id"] == "abc"
        # Exactly one reactive refresh (token endpoint hit once).
        assert token_route.call_count == 1
        # Exactly two data-call attempts: 401 then 200.
        assert call_state["n"] == 2


@pytest.mark.asyncio
async def test_dual_credentials_source_of_truth() -> None:
    """Construct with both access_token= and client_id/client_secret=.
    Source must be MANAGED; supplied token is used for the first request.
    """
    from pymedplum import AsyncMedplumClient
    from pymedplum._auth import TokenSource

    with respx.mock(
        base_url="https://api.medplum.com", assert_all_called=False
    ) as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "tok-refresh", "expires_in": 3600}
        )
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"}
        )

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            access_token="supplied-token",
        )
        try:
            assert client._tokens.source == TokenSource.MANAGED
            await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

        # Supplied token was used; no OAuth POST needed because no expiry
        # was parseable and the request succeeded on the first try.
        assert token_route.call_count == 0


@pytest.mark.asyncio
async def test_external_token_not_auto_refreshed() -> None:
    """Only access_token provided → EXTERNAL source. A 401 from the
    server surfaces as-is; SDK never attempts the OAuth endpoint.
    """
    from pymedplum import AsyncMedplumClient
    from pymedplum._auth import TokenSource
    from pymedplum.exceptions import AuthenticationError

    with respx.mock(
        base_url="https://api.medplum.com", assert_all_called=False
    ) as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "should-not-be-called", "expires_in": 3600}
        )
        mock.get("/fhir/R4/Patient/abc").respond(401, text="nope")

        client = AsyncMedplumClient(
            base_url="https://api.medplum.com/",
            access_token="external-tok",
        )
        try:
            assert client._tokens.source == TokenSource.EXTERNAL
            with pytest.raises(AuthenticationError):
                await client.read_resource("Patient", "abc")
        finally:
            await client.aclose()

        assert token_route.call_count == 0


def test_obo_isolation_across_threads() -> None:
    """Each thread sets explicit on_behalf_of= on its own call; the
    header observed at the wire matches the thread's supplied value.
    """
    import threading

    from pymedplum import MedplumClient

    seen: dict[str, str | None] = {}
    lock = threading.Lock()

    with respx.mock(base_url="https://api.medplum.com") as mock:
        mock.post("/oauth2/token").respond(
            json={"access_token": "tok", "expires_in": 3600}
        )

        def handler(request: httpx.Request) -> httpx.Response:
            # Use the thread name as the key for deterministic check.
            with lock:
                seen[threading.current_thread().name] = request.headers.get(
                    "X-Medplum-On-Behalf-Of"
                )
            return httpx.Response(200, json={"resourceType": "Patient", "id": "x"})

        mock.get("/fhir/R4/Patient/x").mock(side_effect=handler)

        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
        )
        try:

            def worker_a() -> None:
                client.read_resource("Patient", "x", on_behalf_of="A")

            def worker_b() -> None:
                client.read_resource("Patient", "x", on_behalf_of="B")

            t_a = threading.Thread(target=worker_a, name="worker-a")
            t_b = threading.Thread(target=worker_b, name="worker-b")
            t_a.start()
            t_b.start()
            t_a.join()
            t_b.join()
        finally:
            client.close()

        assert seen["worker-a"] == "ProjectMembership/A"
        assert seen["worker-b"] == "ProjectMembership/B"


def test_cooldown_clears_after_successful_refresh() -> None:
    """Sync: a failure sets the cooldown; after cooldown elapses and a
    subsequent refresh succeeds, failed_refresh_at is cleared.
    """
    from pymedplum import MedplumClient
    from pymedplum.exceptions import MedplumError

    with respx.mock(base_url="https://api.medplum.com") as mock:
        route = mock.post("/oauth2/token")
        route.side_effect = [
            httpx.Response(500, text="boom"),
            httpx.Response(200, json={"access_token": "tok", "expires_in": 3600}),
        ]
        mock.get("/fhir/R4/Patient/abc").respond(
            json={"resourceType": "Patient", "id": "abc"},
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            client_id="cid",
            client_secret="cs",
            failed_refresh_cooldown=0.02,
        )
        try:
            with pytest.raises(MedplumError):
                client.read_resource("Patient", "abc")
            time.sleep(0.2)
            result = client.read_resource("Patient", "abc")
            assert result["id"] == "abc"
            assert client._tokens.failed_refresh_at is None
        finally:
            client.close()


def test_force_refresh_external_token_raises_medplum_error() -> None:
    """TokenSource.EXTERNAL force_refresh is a hard error, no OAuth
    attempt.
    """
    from pymedplum import MedplumClient
    from pymedplum.exceptions import MedplumError

    with respx.mock(
        base_url="https://api.medplum.com", assert_all_called=False
    ) as mock:
        token_route = mock.post("/oauth2/token").respond(
            json={"access_token": "x", "expires_in": 3600}
        )
        client = MedplumClient(
            base_url="https://api.medplum.com/",
            access_token="external",
        )
        try:
            with pytest.raises(MedplumError, match="externally-provided"):
                client._tokens.force_refresh(client._http)
        finally:
            client.close()
        assert token_route.call_count == 0


def test_force_refresh_no_credentials_raises_medplum_error() -> None:
    """Managed-but-credentialless force_refresh raises before fetch."""
    from pymedplum._auth import TokenManager, TokenSource
    from pymedplum.exceptions import MedplumError

    manager = TokenManager(
        token_url="https://api.medplum.com/oauth2/token",
        source=TokenSource.MANAGED,
    )
    try:
        with (
            httpx.Client() as http,
            pytest.raises(MedplumError, match="no client credentials"),
        ):
            manager.force_refresh(http)
    finally:
        manager.close()


@pytest.mark.asyncio
async def test_asyncio_to_thread_propagates_context() -> None:
    """asyncio.to_thread copies the current context by default, so OBO
    ambient propagates to the thread.
    """
    from contextvars import ContextVar

    var: ContextVar[str | None] = ContextVar("to_thread_test", default=None)

    def read_var() -> str | None:
        return var.get()

    token = var.set("in-async")
    try:
        result = await asyncio.to_thread(read_var)
    finally:
        var.reset(token)
    assert result == "in-async"


def test_thread_pool_executor_does_not_propagate_context_without_copy_context() -> None:
    """Documenting footgun: raw ThreadPoolExecutor.submit does NOT
    capture the parent thread's context. Callers must use
    ``contextvars.copy_context().run`` to propagate.

    This is why we recommend the ``on_behalf_of=`` kwarg over the
    context-manager form when crossing into a threadpool.
    """
    from contextvars import ContextVar, copy_context

    var: ContextVar[str | None] = ContextVar("tpe_test", default=None)

    def read_var() -> str | None:
        return var.get()

    token = var.set("in-main-thread")
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            # Raw submit: default=None is what the worker sees.
            fut_naive = pool.submit(read_var)
            assert fut_naive.result() is None

            # Explicit context copy: parent's value propagates.
            ctx = copy_context()
            fut_explicit = pool.submit(ctx.run, read_var)
            assert fut_explicit.result() == "in-main-thread"
    finally:
        var.reset(token)


def test_token_manager_close_shuts_down_executor() -> None:
    """MedplumClient.close() must shut down the per-client executor."""
    from pymedplum import MedplumClient

    client = MedplumClient(
        base_url="https://api.medplum.com/",
        client_id="c",
        client_secret="s",
    )
    executor = client._tokens._executor
    client.close()
    # ThreadPoolExecutor exposes `_shutdown` after shutdown(); acceptable
    # in tests.
    assert executor._shutdown
