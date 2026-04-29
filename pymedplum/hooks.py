"""Public hook surface: PreparedRequest, RequestAttempt, RequestEvent,
and type aliases BeforeRequestHook / OnRequestCompleteHook.

These dataclasses are part of the SDK's public API. Changes are breaking.
"""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import parse_qs

if TYPE_CHECKING:
    from datetime import datetime


RequestAction = Literal[
    "read",
    "search",
    "create",
    "update",
    "patch",
    "delete",
    "operation",
    "batch_or_transaction",
]
"""FHIR action category derived from method + URL shape.

Values follow the FHIR REST API verbs (read, search, create, update,
patch, delete) plus two compound categories:

- ``operation``: an extended ``$operation`` invocation, regardless of
  whether it targets a specific resource instance.
- ``batch_or_transaction``: a POST to the FHIR root (e.g. ``/fhir/R4/``)
  carrying a Bundle. Discriminating batch vs. transaction requires the
  request body's ``Bundle.type``, which the SDK does not retain.

Non-FHIR calls (auth/system endpoints) yield ``None``.
"""


RequestOutcome = Literal["success", "error"]
"""High-level status of the logical request.

``success`` if the SDK observed a 2xx/3xx final status and no exception
was raised; ``error`` otherwise (including network failures, where
``final_status_code`` is ``None``).
"""


_METHOD_TO_ACTION: dict[str, RequestAction] = {
    "POST": "create",
    "PUT": "update",
    "PATCH": "patch",
    "DELETE": "delete",
}


@dataclass(frozen=True, slots=True)
class PreparedRequest:
    """Request shape presented to a `before_request` hook."""

    method: str
    url: str
    headers: dict[str, str]
    json_body: Any | None


@dataclass(frozen=True, slots=True)
class RequestAttempt:
    """Per-attempt metadata for a single wire call within a logical request."""

    attempt_number: int
    status_code: int | None
    duration_seconds: float
    on_behalf_of: str | None
    exception: BaseException | None


@dataclass(frozen=True, slots=True)
class RequestEvent:
    """Outcome of a logical SDK request, dispatched to completion hooks."""

    method: str
    path: str
    path_template: str
    query_params: dict[str, list[str]] | None
    resource_type: str | None
    resource_id: str | None
    operation: str | None
    started_at: datetime
    ended_at: datetime
    attempts: list[RequestAttempt]
    final_status_code: int | None
    final_exception: BaseException | None
    # ``action`` and ``outcome`` carry defaults so external/test code that
    # hand-constructs a RequestEvent doesn't break. The SDK always computes
    # and populates them at the dispatch site.
    action: RequestAction | None = None
    """FHIR action category. ``None`` for non-FHIR requests (e.g.
    ``/oauth2/token``) or when the request shape can't be classified.
    Populated automatically by the SDK; defaults to ``None`` for
    hand-constructed events."""

    outcome: RequestOutcome = "error"
    """``"success"`` if the request finished with a 2xx/3xx and no
    exception; ``"error"`` otherwise. Populated automatically by the
    SDK; defaults to ``"error"`` for hand-constructed events so a
    forgotten field can't hide a failure."""

    def to_phi_audit_dict(
        self, *, include_query_params: bool = False
    ) -> dict[str, Any]:
        """JSON-serializable dict containing PHI-bearing fields for audit logs.

        Includes the resolved ``path`` (with patient/resource IDs), parsed
        ``resource_id``, per-attempt ``on_behalf_of`` (a ProjectMembership
        identifier), and — when ``include_query_params=True`` — the parsed
        FHIR search query.

        This payload is appropriate for a HIPAA-compliant audit sink that is
        contractually authorized to receive PHI. It is NOT appropriate for
        general observability backends (metrics, APM, error trackers,
        third-party log aggregators) unless they have been provisioned for
        PHI. For those, use :meth:`to_non_phi_dict` instead.
        """
        data: dict[str, Any] = {
            "method": self.method,
            "path": self.path,
            "path_template": self.path_template,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "operation": self.operation,
            "action": self.action,
            "outcome": self.outcome,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
            "attempts": [
                {
                    "attempt_number": a.attempt_number,
                    "status_code": a.status_code,
                    "duration_seconds": a.duration_seconds,
                    "on_behalf_of": a.on_behalf_of,
                    "exception": serialize_exception(a.exception),
                }
                for a in self.attempts
            ],
            "final_status_code": self.final_status_code,
            "final_exception": serialize_exception(self.final_exception),
        }
        if include_query_params:
            data["query_params"] = self.query_params
        return data

    def to_non_phi_dict(self) -> dict[str, Any]:
        """JSON-serializable dict suitable for non-PHI observability sinks.

        Strips PHI-bearing fields: no resolved ``path``, no ``resource_id``,
        no per-attempt ``on_behalf_of``, no query params. Retains shape and
        timing data — ``method``, ``path_template`` (e.g. ``/Patient/{id}``),
        ``resource_type``, ``operation``, ``action``, ``outcome``, attempt
        counts, status codes, durations, and exception type names — which
        is enough to drive most SLO / latency / error-rate dashboards
        without exporting protected information.

        Use this for metrics pipelines, generic log aggregators, error
        trackers, or any destination not contractually approved for PHI.
        """
        return {
            "method": self.method,
            "path_template": self.path_template,
            "resource_type": self.resource_type,
            "operation": self.operation,
            "action": self.action,
            "outcome": self.outcome,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
            "attempt_count": len(self.attempts),
            "attempts": [
                {
                    "attempt_number": a.attempt_number,
                    "status_code": a.status_code,
                    "duration_seconds": a.duration_seconds,
                    "exception_type": (
                        type(a.exception).__name__ if a.exception else None
                    ),
                }
                for a in self.attempts
            ],
            "final_status_code": self.final_status_code,
            "final_exception_type": (
                type(self.final_exception).__name__ if self.final_exception else None
            ),
        }


def serialize_exception(
    exc: BaseException | None,
) -> dict[str, Any] | None:
    """Reduce an exception to a dict for hook delivery.

    If the exception declares ``sanitize_for_logging()``, trust it — this
    is how every ``pymedplum.*`` exception controls what it exposes. For
    everything else, pass through ``str(exc)`` verbatim. The hook consumer
    owns their sink's PHI contract; the SDK should not silently redact
    information a developer needs to triage failures.

    Public API since 0.2.0.
    """
    if exc is None:
        return None
    sanitizer = getattr(exc, "sanitize_for_logging", None)
    if callable(sanitizer):
        result = sanitizer()
        if isinstance(result, dict):
            return result
    return {"type": type(exc).__name__, "message": str(exc)}


# Backwards-compatible alias for the underscore-prefixed name used
# internally before 0.2.0. New code should import `serialize_exception`.
_serialize_exception = serialize_exception


def _compute_action(
    *,
    method: str,
    path: str,
    resource_type: str | None,
    resource_id: str | None,
    operation: str | None,
    fhir_url_path: str | None,
) -> RequestAction | None:
    """Internal: classify a request into a FHIR action category.

    Used at `RequestEvent` construction time. Not part of the public
    API; consumers should read :attr:`RequestEvent.action` instead.
    """
    if operation:
        return "operation"
    upper = method.upper()
    if resource_type:
        if upper == "GET":
            return "read" if resource_id else "search"
        return _METHOD_TO_ACTION.get(upper)
    if upper == "POST" and _is_fhir_rooted(path, fhir_url_path):
        return "batch_or_transaction"
    return None


def _compute_outcome(
    *,
    final_status_code: int | None,
    final_exception: BaseException | None,
) -> RequestOutcome:
    """Internal: classify the final disposition of a logical request."""
    if final_exception is not None:
        return "error"
    if final_status_code is not None and 200 <= final_status_code < 400:
        return "success"
    return "error"


def _is_fhir_rooted(path: str, fhir_url_path: str | None) -> bool:
    """Return True when ``path`` falls under the configured FHIR prefix."""
    if fhir_url_path is not None:
        configured = "/" + fhir_url_path.lstrip("/")
        if not configured.endswith("/"):
            configured = configured + "/"
        return path.startswith(configured)
    return _FHIR_PREFIX_RE.match(path) is not None


BeforeRequestHook = Callable[[PreparedRequest], "PreparedRequest | None"]
OnRequestCompleteHook = Callable[[RequestEvent], None]
AsyncOnRequestCompleteHook = Callable[[RequestEvent], Awaitable[None]]


_FHIR_PREFIX_RE = re.compile(r"^/fhir/R\d+[A-Za-z]*/")
_RESOURCE_TYPE_RE = re.compile(r"^[A-Z][A-Za-z]+$")


def _parse_fhir_url(
    path: str,
    fhir_url_path: str | None = None,
) -> tuple[str | None, str | None, str | None, str]:
    """Parse a FHIR URL path into (resource_type, resource_id, operation, path_template).

    FHIR R4 path shapes recognized:
        {prefix}{ResourceType}
        {prefix}{ResourceType}/{id}
        {prefix}{ResourceType}/{id}/_history
        {prefix}{ResourceType}/{id}/_history/{vid}
        {prefix}{ResourceType}/{id}/$operation
        {prefix}{ResourceType}/$operation

    path_template substitutes "{id}" for resource and version IDs so it is
    safe to use as a metric tag or non-PHI log field. Non-FHIR paths
    return (None, None, None, path) unchanged.

    ``fhir_url_path`` matches the client's configured prefix literally when
    given (e.g. ``"fhir/R4B/"``, ``"fhir/"``). Otherwise the standard
    ``/fhir/R<version>/`` shape is accepted.
    """
    if fhir_url_path is not None:
        configured = "/" + fhir_url_path.lstrip("/")
        if not configured.endswith("/"):
            configured = configured + "/"
        if not path.startswith(configured):
            return None, None, None, path
        prefix = configured
    else:
        prefix_match = _FHIR_PREFIX_RE.match(path)
        if prefix_match is None:
            return None, None, None, path
        prefix = prefix_match.group(0)
    segments = [s for s in path[len(prefix) :].split("/") if s]
    if not segments or not _RESOURCE_TYPE_RE.match(segments[0]):
        return None, None, None, path

    resource_type = segments[0]
    resource_id: str | None = None
    operation: str | None = None
    template_segments: list[str] = [resource_type]

    for index, segment in enumerate(segments[1:], start=1):
        if segment.startswith("$"):
            operation = segment
            template_segments.append(segment)
        elif segment == "_history":
            template_segments.append(segment)
        else:
            if index == 1:
                resource_id = segment
            template_segments.append("{id}")

    path_template = prefix + "/".join(template_segments)
    return resource_type, resource_id, operation, path_template


def _parse_query_params(
    query: str | None,
) -> dict[str, list[str]] | None:
    """Parse a URL query string into a PHI-bearing params dict.

    - None / "" -> None (no query on the URL)
    - "?" alone -> {} (empty but present)
    - Otherwise: urllib.parse.parse_qs with keep_blank_values=True.
    """
    if query is None or query == "":
        return None
    if query.startswith("?"):
        query = query[1:]
    if query == "":
        return {}
    return parse_qs(query, keep_blank_values=True)
