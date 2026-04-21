"""Auth: token lifecycle + per-client OBO context.

Split into:
  _TokenManagerBase — shared dataclass state + decision helpers
  AsyncTokenManager — asyncio.Task + asyncio.shield single-flight
  TokenManager      — ThreadPoolExecutor(max_workers=1) single-flight
  OnBehalfOfContext — per-client ContextVar, sync+async
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import enum
import logging
import threading
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

import httpx

from pymedplum._constants import AUTH_HEADERS_LOWER
from pymedplum.exceptions import MedplumError, TokenRefreshCooldownError

if TYPE_CHECKING:
    from contextvars import ContextVar, Token

logger = logging.getLogger("pymedplum.auth")
_hooks_logger = logging.getLogger("pymedplum.hooks")

# Signature matches BaseClient._dispatch_auth_event_[sync|async]:
#   (method, url, status_code, duration, exception, started_at, ended_at)
AuthEventDispatcher = Callable[
    [str, str, int | None, float, BaseException | None, datetime, datetime],
    Awaitable[None] | None,
]


class TokenSource(enum.Enum):
    EXTERNAL = "external"
    MANAGED = "managed"


@dataclass
class _TokenManagerBase:
    # client_secret and access_token are explicitly excluded from repr so
    # logging or debugger inspection of a TokenManager (e.g. caplog dumps,
    # pytest tracebacks, exception chains) cannot surface them. client_id
    # is included because it's a non-secret OAuth public identifier.
    client_id: str | None = None
    client_secret: str | None = field(default=None, repr=False)
    access_token: str | None = field(default=None, repr=False)
    token_expires_at: datetime | None = None
    token_url: str = ""
    source: TokenSource = TokenSource.MANAGED
    failed_refresh_at: datetime | None = None
    failed_refresh_cooldown: timedelta = field(
        default_factory=lambda: timedelta(seconds=1)
    )
    _auth_event_dispatcher: AuthEventDispatcher | None = field(default=None, repr=False)
    # Count of consecutive refresh failures since the last success. Used to
    # gate the "refresh recovered" INFO log so it never fires on the happy
    # path, only after one or more prior WARNINGs.
    _consecutive_failures: int = 0

    def set_auth_event_dispatcher(self, fn: AuthEventDispatcher | None) -> None:
        """Install the owning client's auth-event dispatcher.

        Called by the client at construction after wiring ``self._tokens``
        so the TokenManager can emit ``on_request_complete`` events for
        its own OAuth token fetches.
        """
        self._auth_event_dispatcher = fn

    def has_credentials(self) -> bool:
        return bool(self.client_id and self.client_secret)

    def is_authenticated(self) -> bool:
        return self.access_token is not None

    def should_refresh_proactively(
        self, *, leeway: timedelta = timedelta(seconds=30)
    ) -> bool:
        if self.source == TokenSource.EXTERNAL:
            return self.access_token is None and self.has_credentials()
        if not self.has_credentials():
            return False
        if self.access_token is None:
            return True
        if self.token_expires_at is None:
            return False
        return (self.token_expires_at - datetime.now(timezone.utc)) <= leeway

    def _is_in_cooldown_locked(self) -> bool:
        if self.failed_refresh_at is None:
            return False
        return (
            datetime.now(timezone.utc) - self.failed_refresh_at
            < self.failed_refresh_cooldown
        )


@dataclass
class AsyncTokenManager(_TokenManagerBase):
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    _refresh_task: asyncio.Task[None] | None = None
    _refresh_timeout_seconds: float = 30.0

    async def ensure_authenticated(self, http_client: httpx.AsyncClient) -> None:
        if not self.should_refresh_proactively():
            return

        logger.debug("token: proactive refresh triggered")
        task_to_await: asyncio.Task[None] | None = None
        async with self._lock:
            if not self.should_refresh_proactively():
                return
            if self._is_in_cooldown_locked():
                assert self.failed_refresh_at is not None
                remaining = (
                    self.failed_refresh_cooldown
                    - (datetime.now(timezone.utc) - self.failed_refresh_at)
                ).total_seconds()
                logger.debug(
                    "token: cooldown check hit (%.2fs remaining)",
                    max(0.0, remaining),
                )
                raise TokenRefreshCooldownError(
                    self.failed_refresh_at,
                    self.failed_refresh_cooldown,
                )
            if self._refresh_task is None or self._refresh_task.done():
                logger.debug("token: acquiring new token")
                self._refresh_task = asyncio.create_task(
                    self._acquire_token(http_client)
                )
            else:
                logger.debug("token: awaiting in-flight refresh task")
            task_to_await = self._refresh_task

        try:
            await asyncio.wait_for(
                asyncio.shield(task_to_await),
                timeout=self._refresh_timeout_seconds,
            )
        except asyncio.TimeoutError:
            raise MedplumError(
                f"Token refresh did not complete within "
                f"{self._refresh_timeout_seconds:.1f}s."
            ) from None
        finally:
            async with self._lock:
                if self._refresh_task is task_to_await and task_to_await.done():
                    self._refresh_task = None

    async def force_refresh(self, http_client: httpx.AsyncClient) -> None:
        if self.source == TokenSource.EXTERNAL:
            raise MedplumError(
                "Cannot refresh an externally-provided access token. "
                "A 401 response means the token is invalid or revoked. "
                "Obtain a new token and construct a new client."
            )
        if not self.has_credentials():
            raise MedplumError("Cannot refresh - no client credentials configured.")

        logger.debug("token: reactive refresh triggered after 401")
        task_to_await: asyncio.Task[None] | None = None
        async with self._lock:
            if self._is_in_cooldown_locked():
                assert self.failed_refresh_at is not None
                remaining = (
                    self.failed_refresh_cooldown
                    - (datetime.now(timezone.utc) - self.failed_refresh_at)
                ).total_seconds()
                logger.debug(
                    "token: cooldown check hit (%.2fs remaining)",
                    max(0.0, remaining),
                )
                raise TokenRefreshCooldownError(
                    self.failed_refresh_at,
                    self.failed_refresh_cooldown,
                )
            if self._refresh_task is None or self._refresh_task.done():
                logger.debug("token: acquiring new token")
                self._refresh_task = asyncio.create_task(
                    self._acquire_token(http_client)
                )
            else:
                logger.debug("token: awaiting in-flight refresh task")
            task_to_await = self._refresh_task

        try:
            await asyncio.wait_for(
                asyncio.shield(task_to_await),
                timeout=self._refresh_timeout_seconds,
            )
        except asyncio.TimeoutError:
            raise MedplumError(
                f"Forced token refresh did not complete within "
                f"{self._refresh_timeout_seconds:.1f}s."
            ) from None
        finally:
            async with self._lock:
                if self._refresh_task is task_to_await and task_to_await.done():
                    self._refresh_task = None

    async def _acquire_token(self, http_client: httpx.AsyncClient) -> None:
        started_at = datetime.now(timezone.utc)
        start_perf = time.perf_counter()
        status_code: int | None = None
        try:
            # Build the request with explicitly-empty headers and then
            # strip anything the http_client merged in from its own
            # defaults. Passing ``headers={}`` to ``.post()`` is NOT
            # enough — httpx merges client-level default headers into
            # per-request headers. We must scrub Authorization and
            # X-Medplum-On-Behalf-Of off the built request before sending.
            req = http_client.build_request(
                "POST",
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                timeout=self._refresh_timeout_seconds - 5.0,
            )
            for h in AUTH_HEADERS_LOWER:
                if h in req.headers:
                    del req.headers[h]
            resp = await http_client.send(req)
            status_code = resp.status_code
            resp.raise_for_status()
            payload = resp.json()
            new_token: str = payload["access_token"]
            new_expires_at = _parse_token_expiry(payload)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            async with self._lock:
                self.failed_refresh_at = datetime.now(timezone.utc)
                self._consecutive_failures += 1
            logger.warning(
                "token: refresh failed (%s), cooldown entered (%.2fs)",
                type(exc).__name__,
                self.failed_refresh_cooldown.total_seconds(),
            )
            await self._emit_auth_event_async(
                started_at=started_at,
                start_perf=start_perf,
                status_code=status_code,
                exception=exc,
            )
            if isinstance(exc, httpx.HTTPError):
                raise MedplumError(
                    f"Token refresh failed: {type(exc).__name__}"
                ) from exc
            raise

        async with self._lock:
            self.access_token = new_token
            self.token_expires_at = new_expires_at
            self.failed_refresh_at = None
            prior_failures = self._consecutive_failures
            self._consecutive_failures = 0

        _log_token_acquired(new_expires_at, payload)
        if prior_failures > 0:
            logger.info(
                "token: refresh recovered after %d prior failure(s); cooldown cleared",
                prior_failures,
            )

        await self._emit_auth_event_async(
            started_at=started_at,
            start_perf=start_perf,
            status_code=status_code,
            exception=None,
        )

    async def _emit_auth_event_async(
        self,
        *,
        started_at: datetime,
        start_perf: float,
        status_code: int | None,
        exception: BaseException | None,
    ) -> None:
        dispatcher = self._auth_event_dispatcher
        if dispatcher is None:
            return
        ended_at = datetime.now(timezone.utc)
        duration = time.perf_counter() - start_perf
        try:
            awaitable = dispatcher(
                "POST",
                self.token_url,
                status_code,
                duration,
                exception,
                started_at,
                ended_at,
            )
            assert awaitable is not None, (
                "AsyncTokenManager expects an awaitable dispatcher; "
                "the async client installs _dispatch_auth_event_async."
            )
            await awaitable
        except Exception as exc:
            _hooks_logger.warning(
                "auth-event dispatcher raised %s; swallowed",
                type(exc).__name__,
            )


@dataclass
class TokenManager(_TokenManagerBase):
    """Sync variant. One dedicated worker thread per client for refreshes,
    owned by a bounded ThreadPoolExecutor.
    """

    _lock: threading.Lock = field(default_factory=threading.Lock)
    _refresh_future: concurrent.futures.Future[None] | None = None
    _executor: concurrent.futures.ThreadPoolExecutor = field(
        default_factory=lambda: concurrent.futures.ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="pymedplum-token-refresh",
        )
    )
    _refresh_timeout_seconds: float = 30.0

    def close(self) -> None:
        self._executor.shutdown(wait=True, cancel_futures=True)

    def ensure_authenticated(self, http_client: httpx.Client) -> None:
        if not self.should_refresh_proactively():
            return

        logger.debug("token: proactive refresh triggered")
        future_to_wait: concurrent.futures.Future[None] | None = None
        with self._lock:
            if not self.should_refresh_proactively():
                return
            if self._is_in_cooldown_locked():
                assert self.failed_refresh_at is not None
                remaining = (
                    self.failed_refresh_cooldown
                    - (datetime.now(timezone.utc) - self.failed_refresh_at)
                ).total_seconds()
                logger.debug(
                    "token: cooldown check hit (%.2fs remaining)",
                    max(0.0, remaining),
                )
                raise TokenRefreshCooldownError(
                    self.failed_refresh_at,
                    self.failed_refresh_cooldown,
                )
            if self._refresh_future is None or self._refresh_future.done():
                logger.debug("token: acquiring new token")
                self._refresh_future = self._executor.submit(
                    self._acquire_token, http_client
                )
            else:
                logger.debug("token: awaiting in-flight refresh task")
            future_to_wait = self._refresh_future

        try:
            future_to_wait.result(timeout=self._refresh_timeout_seconds)
        finally:
            with self._lock:
                if self._refresh_future is future_to_wait and future_to_wait.done():
                    self._refresh_future = None

    def force_refresh(self, http_client: httpx.Client) -> None:
        if self.source == TokenSource.EXTERNAL:
            raise MedplumError(
                "Cannot refresh an externally-provided access token. "
                "A 401 response means the token is invalid or revoked. "
                "Obtain a new token and construct a new client."
            )
        if not self.has_credentials():
            raise MedplumError("Cannot refresh - no client credentials configured.")

        logger.debug("token: reactive refresh triggered after 401")
        future_to_wait: concurrent.futures.Future[None] | None = None
        with self._lock:
            if self._is_in_cooldown_locked():
                assert self.failed_refresh_at is not None
                remaining = (
                    self.failed_refresh_cooldown
                    - (datetime.now(timezone.utc) - self.failed_refresh_at)
                ).total_seconds()
                logger.debug(
                    "token: cooldown check hit (%.2fs remaining)",
                    max(0.0, remaining),
                )
                raise TokenRefreshCooldownError(
                    self.failed_refresh_at,
                    self.failed_refresh_cooldown,
                )
            if self._refresh_future is None or self._refresh_future.done():
                logger.debug("token: acquiring new token")
                self._refresh_future = self._executor.submit(
                    self._acquire_token, http_client
                )
            else:
                logger.debug("token: awaiting in-flight refresh task")
            future_to_wait = self._refresh_future

        try:
            future_to_wait.result(timeout=self._refresh_timeout_seconds)
        finally:
            with self._lock:
                if self._refresh_future is future_to_wait and future_to_wait.done():
                    self._refresh_future = None

    def _acquire_token(self, http_client: httpx.Client) -> None:
        started_at = datetime.now(timezone.utc)
        start_perf = time.perf_counter()
        status_code: int | None = None
        try:
            # See AsyncTokenManager._acquire_token for the rationale on
            # using build_request + scrub + send instead of passing
            # ``headers={}`` directly.
            req = http_client.build_request(
                "POST",
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                timeout=self._refresh_timeout_seconds - 5.0,
            )
            for h in AUTH_HEADERS_LOWER:
                if h in req.headers:
                    del req.headers[h]
            resp = http_client.send(req)
            status_code = resp.status_code
            resp.raise_for_status()
            payload = resp.json()
            new_token: str = payload["access_token"]
            new_expires_at = _parse_token_expiry(payload)
        except Exception as exc:
            with self._lock:
                self.failed_refresh_at = datetime.now(timezone.utc)
                self._consecutive_failures += 1
            logger.warning(
                "token: refresh failed (%s), cooldown entered (%.2fs)",
                type(exc).__name__,
                self.failed_refresh_cooldown.total_seconds(),
            )
            self._emit_auth_event_sync(
                started_at=started_at,
                start_perf=start_perf,
                status_code=status_code,
                exception=exc,
            )
            if isinstance(exc, httpx.HTTPError):
                raise MedplumError(
                    f"Token refresh failed: {type(exc).__name__}"
                ) from exc
            raise

        with self._lock:
            self.access_token = new_token
            self.token_expires_at = new_expires_at
            self.failed_refresh_at = None
            prior_failures = self._consecutive_failures
            self._consecutive_failures = 0

        _log_token_acquired(new_expires_at, payload)
        if prior_failures > 0:
            logger.info(
                "token: refresh recovered after %d prior failure(s); cooldown cleared",
                prior_failures,
            )

        self._emit_auth_event_sync(
            started_at=started_at,
            start_perf=start_perf,
            status_code=status_code,
            exception=None,
        )

    def _emit_auth_event_sync(
        self,
        *,
        started_at: datetime,
        start_perf: float,
        status_code: int | None,
        exception: BaseException | None,
    ) -> None:
        dispatcher = self._auth_event_dispatcher
        if dispatcher is None:
            return
        ended_at = datetime.now(timezone.utc)
        duration = time.perf_counter() - start_perf
        try:
            dispatcher(
                "POST",
                self.token_url,
                status_code,
                duration,
                exception,
                started_at,
                ended_at,
            )
        except Exception as exc:
            _hooks_logger.warning(
                "auth-event dispatcher raised %s; swallowed",
                type(exc).__name__,
            )


def _parse_token_expiry(payload: dict[str, Any]) -> datetime | None:
    """Parse token expiry from the OAuth response.

    Reads ``expires_in`` (seconds-from-now) which Medplum and every
    standards-compliant OAuth server always returns. If a server omits it,
    we fall back to "no known expiry"; the next 401 reactively triggers
    a forced refresh, which is the same path that handles mid-session
    credential revocation.
    """
    expires_in = payload.get("expires_in")
    if isinstance(expires_in, (int, float)) and expires_in > 0:
        return datetime.now(timezone.utc) + timedelta(seconds=float(expires_in))
    return None


def _log_token_acquired(
    expires_at: datetime | None,
    payload: dict[str, Any],
) -> None:
    """Emit DEBUG logs for a successful token acquisition.

    Logs only the expiry source and seconds-until-expiry. Never logs the
    token value itself.
    """
    expires_in = payload.get("expires_in")
    source = (
        "expires_in"
        if isinstance(expires_in, (int, float)) and expires_in > 0
        else "none"
    )
    logger.debug("token: expiry parsed from %s", source)
    if expires_at is not None:
        remaining = (expires_at - datetime.now(timezone.utc)).total_seconds()
        logger.debug(
            "token: acquired new token (expires in %.0fs)",
            max(0.0, remaining),
        )
    else:
        logger.debug("token: acquired new token (no expiry known)")


class OnBehalfOfContext:
    """Context manager wrapping a per-client OBO ``ContextVar``.

    Supports both sync (``with``) and async (``async with``).

    Two failure modes that the context manager cannot fully prevent — use
    the ``on_behalf_of=`` keyword argument on the client method instead
    when either applies:

    1. ``asyncio.create_task()`` inside the ``with`` block::

           async with client.on_behalf_of("ProjectMembership/abc"):
               # The spawned task snapshots the current Context, so it
               # *inherits* the OBO. If the spawned task outlives the
               # ``with`` block, it continues running with that OBO until
               # the snapshot is reset, which can happen later than
               # expected. Pass on_behalf_of= explicitly to the spawned
               # task's call instead.
               asyncio.create_task(client.read_resource("Patient", "x"))

    2. ``threading.Thread`` inside the ``with`` block::

           with client.on_behalf_of("ProjectMembership/abc"):
               # Threads do NOT inherit ContextVar state by default —
               # the new thread sees the ambient OBO (or None), not the
               # one set here. The keyword argument is the only reliable
               # way to scope OBO across thread boundaries.
               threading.Thread(
                   target=client.read_resource, args=("Patient", "x")
               ).start()

    The context manager is the right choice for a sequence of awaits
    inside a single task or thread; for anything that crosses a task or
    thread boundary, prefer ``on_behalf_of=`` on the call itself.
    """

    def __init__(self, var: ContextVar[str | None], membership_id: str) -> None:
        self._var = var
        self._membership_id = membership_id
        self._token: Token[str | None] | None = None

    def __enter__(self) -> str:
        self._token = self._var.set(self._membership_id)
        return self._membership_id

    def __exit__(self, *exc: object) -> None:
        if self._token is None:
            return
        try:
            self._var.reset(self._token)
        except ValueError:
            logger.warning(
                "pymedplum: OnBehalfOfContext.reset() called on a token "
                "from a different Context (cross-task boundary?). "
                "Clearing OBO to prevent unintended value persistence. "
                "Use the on_behalf_of= kwarg rather than the context "
                "manager when crossing async task boundaries."
            )
            self._var.set(None)
        finally:
            self._token = None

    async def __aenter__(self) -> str:
        return self.__enter__()

    async def __aexit__(self, *exc: object) -> None:
        self.__exit__()
