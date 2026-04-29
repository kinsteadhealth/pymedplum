from __future__ import annotations

import inspect
import logging
import secrets
import uuid
import warnings
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qsl, urlparse

import httpx
from pydantic import BaseModel

from ._auth import OnBehalfOfContext as _OboContextVar
from ._constants import (
    AUTH_HEADERS_LOWER,
    AUTHORIZATION_HEADER,
    MEDPLUM_EXTENDED_HEADER,
    MEDPLUM_EXTENDED_VALUE,
    OBO_HEADER,
)
from ._retry import RETRYABLE_STATUS_CODES, parse_retry_after_429
from ._security import assert_same_origin, validate_base_url
from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    MedplumError,
    NotFoundError,
    OperationOutcomeError,
    PreconditionFailedError,
    RateLimitError,
    ServerError,
)
from .hooks import (
    AsyncOnRequestCompleteHook,
    BeforeRequestHook,
    OnRequestCompleteHook,
    PreparedRequest,
    RequestAttempt,
    RequestEvent,
    _compute_action,
    _compute_outcome,
    _parse_fhir_url,
    _parse_query_params,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from .async_client import AsyncMedplumClient
    from .client import MedplumClient
    from .fhir.operationoutcome import OperationOutcome


_hooks_logger = logging.getLogger("pymedplum.hooks")
_auth_logger = logging.getLogger("pymedplum.auth")


def _resolve_if_match(
    resource: dict[str, Any] | BaseModel, if_match: bool | str
) -> str | None:
    """Compute the If-Match header value for ``update_resource``.

    - ``str``: treat as an explicit ETag; return verbatim.
    - ``False``: opt out, no header.
    - ``True``: read ``meta.versionId`` off the resource and wrap as
      ``W/"<versionId>"``; return ``None`` if no versionId is present.
    """
    if isinstance(if_match, str):
        return if_match
    if if_match is False:
        return None
    if if_match is True:
        meta = (
            resource.get("meta")
            if isinstance(resource, dict)
            else getattr(resource, "meta", None)
        )
        version_id: str | None = None
        if isinstance(meta, dict):
            version_id = meta.get("versionId")
        elif meta is not None:
            version_id = getattr(meta, "versionId", None)
        if version_id:
            return f'W/"{version_id}"'
        return None
    raise TypeError(f"if_match must be bool or str, got {type(if_match).__name__}")


_STATUS_EXCEPTIONS: dict[int, tuple[Callable[..., MedplumError], str]] = {
    400: (BadRequestError, "Bad Request"),
    401: (AuthenticationError, "Authentication failed or token expired"),
    403: (AuthorizationError, "Access denied - insufficient permissions"),
    404: (NotFoundError, "Resource not found"),
    412: (
        PreconditionFailedError,
        "Precondition failed - resource may have been modified by another process",
    ),
    429: (RateLimitError, "Rate limit exceeded"),
}


def _raise_or_json(
    response: httpx.Response, fhir_url_path: str | None = None
) -> dict[str, Any]:
    """Parse response or raise appropriate exception based on status code."""
    status = response.status_code
    if 200 <= status < 300:
        if status == 204 or not response.content:
            return {}
        data: Any = response.json()
        if isinstance(data, dict):
            return data
        # FHIR endpoints return objects; a list/scalar at the top level is
        # almost always a caller hitting a non-FHIR endpoint without
        # ``raw=True``. Surface it instead of silently returning ``{}``.
        raise MedplumError(
            f"Expected JSON object, got {type(data).__name__}; "
            "use raw=True for non-FHIR endpoints"
        )

    try:
        parsed = response.json()
    except ValueError:
        parsed = None
    outcome: dict[str, Any] | None = parsed if isinstance(parsed, dict) else None

    mapped = _STATUS_EXCEPTIONS.get(status)
    if mapped is not None:
        exc_cls, message = mapped
        raise exc_cls(message, status_code=status, response_data=outcome)

    if status >= 500:
        method, path = _method_and_path(response)
        _, _, _, path_template = _parse_fhir_url(path, fhir_url_path)
        raise ServerError(
            status_code=status,
            method=method,
            path=path,
            path_template=path_template,
            response=response,
        )

    raise OperationOutcomeError(outcome=outcome or {})


def _finalize_response(
    response: httpx.Response, *, raw: bool, fhir_url_path: str | None = None
) -> dict[str, Any] | httpx.Response:
    """Return parsed JSON or the raw response, raising on error status.

    When ``raw=True``, successful responses are returned as the underlying
    :class:`httpx.Response` so callers can reach for ``.content`` / ``.text``
    on binary or non-JSON endpoints. Error responses always flow through
    :func:`_raise_or_json` so exception types stay consistent.
    """
    if not raw:
        return _raise_or_json(response, fhir_url_path)
    if response.status_code >= 400:
        _raise_or_json(response, fhir_url_path)
    return response


def _method_and_path(response: httpx.Response) -> tuple[str, str]:
    """Extract HTTP method and URL path from a response's originating request.

    Falls back to empty strings if the request is not attached (e.g. hand-built
    responses in tests).
    """
    request = getattr(response, "request", None)
    if request is None:
        return "", ""
    return request.method, request.url.path


MAX_WIRE_ATTEMPTS: int = 6


def _append_include_param(
    params: list[tuple[str, Any]],
    key: str,
    value: str | list[str] | None,
) -> None:
    """Append ``(key, value)``; list values emit one tuple per item."""
    if not value:
        return
    if isinstance(value, list):
        params.extend((key, item) for item in value)
    else:
        params.append((key, value))


def _append_search_options(
    params: list[tuple[str, Any]],
    *,
    summary: str | None,
    elements: list[str] | None,
    total: str | None,
    at: str | None,
    count: int | None,
    offset: int | None,
    sort: str | list[str] | None,
    include: str | list[str] | None,
    include_iterate: str | list[str] | None,
    revinclude: str | list[str] | None,
    revinclude_iterate: str | list[str] | None,
) -> None:
    """Append FHIR search modifier params in-place.

    List-valued ``sort`` is comma-joined (``_sort=a,b``) while list-valued
    ``include`` / ``revinclude`` (and their ``:iterate`` variants) are
    emitted as repeated params. None and empty values are skipped.
    """
    scalars: tuple[tuple[str, Any], ...] = (
        ("_summary", summary),
        ("_elements", ",".join(elements) if elements else None),
        ("_total", total),
        ("_at", at),
        ("_count", str(count) if count is not None else None),
        ("_offset", str(offset) if offset is not None else None),
        ("_sort", ",".join(sort) if isinstance(sort, list) else sort),
    )
    for key, value in scalars:
        if value:
            params.append((key, value))

    _append_include_param(params, "_include", include)
    _append_include_param(params, "_include:iterate", include_iterate)
    _append_include_param(params, "_revinclude", revinclude)
    _append_include_param(params, "_revinclude:iterate", revinclude_iterate)


@dataclass
class _AttemptTracker:
    """Per-request bookkeeping for the retry loop and completion event."""

    method: str
    url: str
    started_at: datetime
    attempts: list[RequestAttempt] = field(default_factory=list)
    final_status_code: int | None = None
    final_exception: BaseException | None = None
    fhir_url_path: str | None = None

    def record(
        self,
        status_code: int | None,
        duration_seconds: float,
        on_behalf_of: str | None,
        exception: BaseException | None,
    ) -> None:
        self.attempts.append(
            RequestAttempt(
                attempt_number=len(self.attempts) + 1,
                status_code=status_code,
                duration_seconds=duration_seconds,
                on_behalf_of=on_behalf_of,
                exception=exception,
            )
        )

    def build_event(self, ended_at: datetime) -> RequestEvent:
        parsed = urlparse(self.url)
        resource_type, resource_id, operation, path_template = _parse_fhir_url(
            parsed.path, self.fhir_url_path
        )
        action = _compute_action(
            method=self.method,
            path=parsed.path,
            resource_type=resource_type,
            resource_id=resource_id,
            operation=operation,
            fhir_url_path=self.fhir_url_path,
        )
        outcome = _compute_outcome(
            final_status_code=self.final_status_code,
            final_exception=self.final_exception,
        )
        return RequestEvent(
            method=self.method,
            path=parsed.path,
            path_template=path_template,
            query_params=_parse_query_params(parsed.query),
            resource_type=resource_type,
            resource_id=resource_id,
            operation=operation,
            started_at=self.started_at,
            ended_at=ended_at,
            attempts=self.attempts,
            final_status_code=self.final_status_code,
            final_exception=self.final_exception,
            action=action,
            outcome=outcome,
        )


def _merge_params_into_url(url: str, params: Any) -> str:
    """Fold query params into the URL up front for a single wire URL.

    ``None`` or empty params leave the URL unchanged.
    """
    if not params:
        return url
    return str(httpx.URL(url, params=params))


def _retry_delay(
    response: httpx.Response, attempt: int, *, max_retry_delay_seconds: float = 60.0
) -> float | None:
    """Return delay seconds for a retryable response, or ``None`` if terminal.

    429 consults ``parse_retry_after_429``. 5xx uses exponential backoff
    with jitter, capped at 2.0s — the historical SDK policy.
    """
    status = response.status_code
    if status == 429:
        return float(
            parse_retry_after_429(response, max_delay_seconds=max_retry_delay_seconds)
        )
    if status in RETRYABLE_STATUS_CODES:
        backoff: float = min(0.25 * (2**attempt), 2.0)
        # secrets.SystemRandom for jitter — same shape as random.random(),
        # but doesn't trip Bandit B311 / pyflakes scanners that flag
        # ``random`` usage in security-relevant modules. Jitter here is
        # purely for de-correlating retries; not security-critical.
        return backoff + secrets.SystemRandom().random() * 0.2
    return None


def _retry_budget_exceeded(status_code: int, attempt: int) -> bool:
    """Return True when the caller has consumed its retry budget for this status.

    429 gets up to 5 retries; 5xx gets up to 2. ``attempt`` is the zero-based
    index of the just-completed attempt.
    """
    max_retries = 5 if status_code == 429 else 2
    return attempt >= max_retries


class BaseClient:
    """Shared logic for sync and async clients."""

    def __init__(
        self,
        base_url: str = "https://api.medplum.com/",
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        access_token: str | None = None,
        project_id: str | None = None,
        fhir_url_path: str = "fhir/R4/",
        before_request: BeforeRequestHook | None = None,
        on_request_complete: (
            OnRequestCompleteHook | AsyncOnRequestCompleteHook | None
        ) = None,
        allow_insecure_http: bool = False,
        default_on_behalf_of: str | None = None,
        max_retry_delay_seconds: float = 60.0,
    ) -> None:
        self.base_url = validate_base_url(
            base_url, allow_insecure_http=allow_insecure_http
        )
        self.fhir_url_path = fhir_url_path
        self.fhir_base_url = self.base_url + fhir_url_path
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.project_id = project_id
        self._before_request: BeforeRequestHook | None = before_request
        self._on_request_complete: (
            OnRequestCompleteHook | AsyncOnRequestCompleteHook | None
        ) = on_request_complete
        self.default_on_behalf_of = default_on_behalf_of
        # Per-attempt cap on server-driven retry delays (Retry-After,
        # _msBeforeNext). A hostile or misconfigured server can otherwise
        # pin a worker for an arbitrary duration.
        self.max_retry_delay_seconds = max(0.0, max_retry_delay_seconds)

        self.token_expires_at: datetime | None = None

        self._obo_var: ContextVar[str | None] = ContextVar(
            f"pymedplum.obo.{uuid.uuid4().hex[:8]}",
            default=None,
        )

        # token_expires_at stays None for caller-supplied access tokens.
        # The next 401 will reactively trigger a forced refresh — same code
        # path used for mid-session credential revocation.

    def __repr__(self) -> str:
        # The default repr would expose ``access_token`` and ``client_secret``
        # via the instance ``__dict__``. Keep the operationally useful fields
        # only — base URL and the public client_id (an OAuth public ID, not
        # a secret).
        return (
            f"{type(self).__name__}(base_url={self.base_url!r}, "
            f"client_id={self.client_id!r}, "
            f"authenticated={self.access_token is not None})"
        )

    def set_access_token(self, token: str, expires_at: datetime | None = None) -> None:
        """Set the access token explicitly.

        This allows using an externally-acquired access token instead of
        authenticating with client credentials. If ``expires_at`` is omitted,
        the SDK does not parse a hint from the token; the next 401 response
        will reactively trigger a forced refresh.

        Args:
            token: The access token string
            expires_at: Optional expiration datetime. When omitted, the SDK
                relies on the server returning a 401 to trigger refresh.

        Example:
            # Create client without credentials
            client = MedplumClient(base_url="https://api.medplum.com/")

            # Set externally-acquired token
            client.set_access_token(my_token)

            # Now client can make authenticated requests
            patient = client.read_resource("Patient", "123")
        """
        self.access_token = token
        self.token_expires_at = expires_at
        # Keep the token manager in sync — _finalize_headers_for_wire reads
        # from it first, so without this the old bearer would still ship.
        tokens = getattr(self, "_tokens", None)
        if tokens is not None:
            tokens.access_token = token
            tokens.token_expires_at = expires_at

    def _apply_before_request(self, original: PreparedRequest) -> PreparedRequest:
        """Run the ``before_request`` hook with pre-redacted auth headers.

        Invariants:
          - The hook never sees ``Authorization`` or
            ``X-Medplum-On-Behalf-Of``.
          - Any such headers in the hook's return value are stripped; the
            SDK re-applies them afterwards from the TokenManager.
          - If the hook returned a URL, it must be same-origin with
            ``self.base_url`` (``UnsafeRedirectError`` otherwise).
        """
        if self._before_request is None:
            return original
        _hooks_logger.debug("hook: dispatching before_request")
        redacted = PreparedRequest(
            method=original.method,
            url=original.url,
            headers={
                k: v
                for k, v in original.headers.items()
                if k.lower() not in AUTH_HEADERS_LOWER
            },
            json_body=original.json_body,
        )
        result = self._before_request(redacted)
        if result is None:
            return redacted
        assert_same_origin(self.base_url, result.url)
        cleaned = {
            k: v
            for k, v in result.headers.items()
            if k.lower() not in AUTH_HEADERS_LOWER
        }
        return PreparedRequest(
            method=result.method,
            url=result.url,
            headers=cleaned,
            json_body=result.json_body,
        )

    def _build_initial_prepared(
        self,
        method: str,
        url: str,
        *,
        caller_headers: dict[str, str] | None,
        json_body: Any,
    ) -> PreparedRequest:
        """Build the PreparedRequest before the ``before_request`` hook runs.

        Starts with the SDK's default non-auth headers, overlays caller
        overrides (``None`` values delete defaults), and attaches the
        JSON body untouched.
        """
        headers: dict[str, str] = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
            MEDPLUM_EXTENDED_HEADER: MEDPLUM_EXTENDED_VALUE,
        }
        for k, v in (caller_headers or {}).items():
            if v is None:
                headers.pop(k, None)
            else:
                headers[k] = v
        return PreparedRequest(
            method=method, url=url, headers=headers, json_body=json_body
        )

    def _finalize_headers_for_wire(
        self,
        base_non_auth_headers: dict[str, str],
        wire_obo: str | None,
    ) -> dict[str, str]:
        """Re-apply SDK-owned ``Authorization`` and OBO headers.

        The hook never sees auth headers and any it returned have already
        been stripped. The SDK is the sole source of the bearer token and
        normalized OBO reference on the wire.
        """
        headers = dict(base_non_auth_headers)
        token = getattr(self, "_tokens", None)
        access = (
            token.access_token if token is not None and token.access_token else None
        ) or self.access_token
        if access:
            headers[AUTHORIZATION_HEADER] = f"Bearer {access}"
        if wire_obo:
            headers[OBO_HEADER] = self._normalize_membership(wire_obo)
        return headers

    def _should_refresh_on_401(self, response: httpx.Response, attempt: int) -> bool:
        """Gate the one-shot reactive refresh on 401 to managed credentials."""
        from ._auth import TokenSource

        tokens = getattr(self, "_tokens", None)
        return (
            attempt == 0
            and response.status_code == 401
            and tokens is not None
            and tokens.source == TokenSource.MANAGED
            and tokens.has_credentials()
        )

    def _build_request_event(
        self,
        method: str,
        url: str,
        attempts: list[RequestAttempt],
        final_status: int | None,
        final_exception: BaseException | None,
        started_at: datetime,
        ended_at: datetime,
    ) -> RequestEvent:
        parsed = urlparse(url)
        resource_type, resource_id, operation, path_template = _parse_fhir_url(
            parsed.path, self.fhir_url_path
        )
        query_params = _parse_query_params(parsed.query)
        action = _compute_action(
            method=method,
            path=parsed.path,
            resource_type=resource_type,
            resource_id=resource_id,
            operation=operation,
            fhir_url_path=self.fhir_url_path,
        )
        outcome = _compute_outcome(
            final_status_code=final_status,
            final_exception=final_exception,
        )
        return RequestEvent(
            method=method,
            path=parsed.path,
            path_template=path_template,
            query_params=query_params,
            resource_type=resource_type,
            resource_id=resource_id,
            operation=operation,
            started_at=started_at,
            ended_at=ended_at,
            attempts=attempts,
            final_status_code=final_status,
            final_exception=final_exception,
            action=action,
            outcome=outcome,
        )

    def _dispatch_on_request_complete_sync(self, event: RequestEvent) -> None:
        """Invoke a sync ``on_request_complete`` hook with error swallowing.

        Raises ``TypeError`` if the hook is a coroutine function — the sync
        client rejects async hooks at construction, so this path should
        never see one.
        """
        hook = self._on_request_complete
        if hook is None:
            return
        if inspect.iscoroutinefunction(hook):
            raise TypeError(
                "Sync client cannot dispatch to an async hook. "
                "This indicates a bug in MedplumClient construction."
            )
        _hooks_logger.debug("hook: dispatching on_request_complete")
        try:
            hook(event)
        except Exception as exc:
            _hooks_logger.warning(
                "on_request_complete hook raised %s; swallowed",
                type(exc).__name__,
            )

    async def _dispatch_on_request_complete_async(self, event: RequestEvent) -> None:
        """Invoke an ``on_request_complete`` hook, awaiting if coroutine."""
        hook = self._on_request_complete
        if hook is None:
            return
        _hooks_logger.debug("hook: dispatching on_request_complete")
        try:
            result = hook(event)
            if inspect.isawaitable(result):
                await result
        except Exception as exc:
            _hooks_logger.warning(
                "on_request_complete hook raised %s; swallowed",
                type(exc).__name__,
            )

    def _dispatch_auth_event_sync(
        self,
        method: str,
        url: str,
        status_code: int | None,
        duration_seconds: float,
        exception: BaseException | None,
        started_at: datetime,
        ended_at: datetime,
    ) -> None:
        """Build a RequestEvent for an auth-endpoint call and dispatch.

        `on_behalf_of` is ALWAYS None for auth events (spec guarantee #10).
        Errors from the hook are swallowed and logged at WARNING.
        """
        if self._on_request_complete is None:
            return
        attempt = RequestAttempt(
            attempt_number=1,
            status_code=status_code,
            duration_seconds=duration_seconds,
            on_behalf_of=None,  # system-level event; no caller attribution
            exception=exception,
        )
        event = self._build_request_event(
            method=method,
            url=url,
            attempts=[attempt],
            final_status=status_code,
            final_exception=exception,
            started_at=started_at,
            ended_at=ended_at,
        )
        self._dispatch_on_request_complete_sync(event)

    async def _dispatch_auth_event_async(
        self,
        method: str,
        url: str,
        status_code: int | None,
        duration_seconds: float,
        exception: BaseException | None,
        started_at: datetime,
        ended_at: datetime,
    ) -> None:
        """Async counterpart of :meth:`_dispatch_auth_event_sync`."""
        if self._on_request_complete is None:
            return
        attempt = RequestAttempt(
            attempt_number=1,
            status_code=status_code,
            duration_seconds=duration_seconds,
            on_behalf_of=None,
            exception=exception,
        )
        event = self._build_request_event(
            method=method,
            url=url,
            attempts=[attempt],
            final_status=status_code,
            final_exception=exception,
            started_at=started_at,
            ended_at=ended_at,
        )
        await self._dispatch_on_request_complete_async(event)

    def _obo_current(self) -> str | None:
        """Get current on-behalf-of membership from the per-client ContextVar."""
        return self._obo_var.get()

    def _resolve_on_behalf_of(self, explicit: str | None) -> str | None:
        """Determine the effective OBO for a single request.

        - explicit kwarg wins if provided (including ``""`` which clears OBO
          for this call, overriding any ambient value).
        - else, this client's ambient ContextVar.
        - else, ``default_on_behalf_of``.
        - else, ``None``.
        """
        if explicit is not None:
            result = explicit or None
            _auth_logger.debug(
                "obo: resolved to %s",
                "explicit-kwarg" if result else "none (explicit clear)",
            )
            return result
        ambient = self._obo_var.get()
        if ambient is not None:
            _auth_logger.debug("obo: resolved to contextvar")
            return ambient
        if self.default_on_behalf_of:
            _auth_logger.debug("obo: resolved to default")
            return self.default_on_behalf_of
        _auth_logger.debug("obo: resolved to none")
        return None

    def _get_headers(self) -> dict[str, str]:
        """Build request headers with auth, OBO, and Medplum extension."""
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
            MEDPLUM_EXTENDED_HEADER: MEDPLUM_EXTENDED_VALUE,  # Required for OBO/audit
        }

        if self.access_token:
            headers[AUTHORIZATION_HEADER] = f"Bearer {self.access_token}"

        obo = self._resolve_on_behalf_of(None)
        if obo:
            headers[OBO_HEADER] = self._normalize_membership(obo)

        return headers

    def _normalize_membership(self, membership: str | Any) -> str:
        """Normalize membership input to canonical ProjectMembership reference.

        Args:
            membership: Either a ProjectMembership resource or a string/id

        Returns:
            Canonical reference string "ProjectMembership/<id>"
        """
        if isinstance(membership, str):
            membership_id = membership.strip()
            if not membership_id:
                msg = "ProjectMembership identifier cannot be empty"
                raise ValueError(msg)
            if not membership_id.startswith("ProjectMembership/"):
                membership_id = f"ProjectMembership/{membership_id}"
            if "/" not in membership_id or not membership_id.split("/")[1]:
                msg = (
                    f"Invalid ProjectMembership identifier: {membership}. "
                    "Expected 'ProjectMembership/<id>' or '<id>'."
                )
                raise ValueError(msg)
            return membership_id

        if not getattr(membership, "id", None):
            msg = (
                "ProjectMembership resource must have an id. "
                "Ensure it has been read from the server."
            )
            raise ValueError(msg)
        return f"ProjectMembership/{membership.id}"

    def _validate_on_behalf_of_usage(self) -> None:
        """Ensure client credentials are suitable for on-behalf-of."""
        if not self.access_token:
            msg = (
                "Client must be authenticated with ClientApplication credentials "
                "before using on-behalf-of. Make a request first so the client "
                "acquires a token."
            )
            raise ValueError(msg)
        if self.client_id and not self.client_secret:
            warnings.warn(
                "On-behalf-of should only be used with ClientApplication "
                "credentials (client_id + client_secret). "
                "Avoid using it in user-facing flows.",
                UserWarning,
                stacklevel=3,
            )

    def _should_refresh_token(self) -> bool:
        """Check if token needs refresh (< 60s remaining)."""
        if not self.token_expires_at:
            return False
        return datetime.now(timezone.utc) >= self.token_expires_at - timedelta(
            seconds=60
        )

    @staticmethod
    def _apply_accounts(
        resource: dict[str, Any],
        accounts: str | list[str],
    ) -> dict[str, Any]:
        """Set meta.accounts on a resource before sending to the server.

        Args:
            resource: FHIR resource dict
            accounts: Single reference or list of references to assign
                (e.g., "Organization/abc" or ["Organization/abc"])

        Returns:
            Modified resource dict with meta.accounts set
        """
        if isinstance(accounts, str):
            accounts = [accounts]

        meta = resource.setdefault("meta", {})
        existing = meta.setdefault("accounts", [])
        existing_refs = {
            acc.get("reference") for acc in existing if isinstance(acc, dict)
        }

        for ref in accounts:
            if not ref or "/" not in ref:
                raise ValueError(
                    f"Invalid account reference: {ref!r}. "
                    "Expected format like 'Organization/abc'."
                )
            if ref not in existing_refs:
                existing.append({"reference": ref})
                existing_refs.add(ref)

        return resource

    def _resolve_async_job_url(
        self, job: str | dict[str, Any] | OperationOutcome
    ) -> str:
        """Resolve an async job input to a polling URL.

        ``job`` may be a FHIR job ID, an absolute URL the server handed us
        back (in ``issue[0].diagnostics`` of an OperationOutcome), or an
        OperationOutcome dict / Pydantic model. Absolute URLs are accepted
        verbatim — if Medplum is compromised enough to misdirect the poll
        target, the SDK is not the layer that's going to stop the attack.

        Args:
            job: Job ID, full URL, OperationOutcome dict, or
                OperationOutcome Pydantic model

        Returns:
            Full URL for polling the job status
        """
        if isinstance(job, BaseModel):
            job = job.model_dump(by_alias=True, exclude_none=True)

        if isinstance(job, dict):
            issues = job.get("issue", [])
            if issues and isinstance(issues[0], dict):
                url = issues[0].get("diagnostics")
                if isinstance(url, str) and url:
                    return url
            raise ValueError(
                "Expected OperationOutcome with job URL in issue[0].diagnostics"
            )

        if job.startswith(("http://", "https://")):
            return job

        return f"{self.fhir_base_url}job/{job}/status"

    def _build_query_params(self, query: Any) -> list[tuple[str, Any]]:
        """Build query parameters from various input formats.

        Returns list of tuples to preserve multi-valued params.

        Args:
            query: None, str, dict, or list of tuples

        Returns:
            List of (key, value) tuples
        """
        if query is None:
            return []

        if isinstance(query, str):
            return [(k, v) for k, v in parse_qsl(query, keep_blank_values=True)]

        if isinstance(query, dict):
            params: list[tuple[str, str]] = []
            for k, v in query.items():
                # Handle list values by creating multiple params with same key
                if isinstance(v, list):
                    params.extend((k, str(item)) for item in v)
                else:
                    params.append((k, str(v)))
            return params

        if isinstance(query, list):
            return [(k, str(v)) for k, v in query]

        msg = f"Invalid query type: {type(query)}"
        raise ValueError(msg)


class OnBehalfOfContext:
    """Sync context manager that sets OBO on the client's ContextVar.

    Thin wrapper over the canonical :class:`pymedplum._auth.OnBehalfOfContext`
    that normalizes the membership reference before installing it into
    the client's per-instance ContextVar. Does NOT authenticate on
    enter — auth happens at first request, as everywhere else.
    """

    def __init__(self, client: MedplumClient, membership: str | Any) -> None:
        self.client = client
        self.member_ref = client._normalize_membership(membership)
        self._inner = _OboContextVar(client._obo_var, self.member_ref)

    def __enter__(self) -> MedplumClient:
        self._inner.__enter__()
        return self.client

    def __exit__(self, *exc: object) -> None:
        self._inner.__exit__(*exc)


class AsyncOnBehalfOfContext:
    """Async counterpart to :class:`OnBehalfOfContext`."""

    def __init__(self, client: AsyncMedplumClient, membership: str | Any) -> None:
        self.client = client
        self.member_ref = client._normalize_membership(membership)
        self._inner = _OboContextVar(client._obo_var, self.member_ref)

    async def __aenter__(self) -> AsyncMedplumClient:
        self._inner.__enter__()
        return self.client

    async def __aexit__(self, *exc: object) -> None:
        self._inner.__exit__(*exc)
