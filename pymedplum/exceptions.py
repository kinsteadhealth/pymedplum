"""Medplum-specific exceptions for better error handling.

These exceptions map to HTTP status codes and common error scenarios,
enabling targeted exception handling and clearer debugging.
"""

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import httpx


class MedplumError(Exception):
    """Base exception for all Medplum errors.

    All Medplum-specific exceptions inherit from this,
    allowing catching all Medplum errors with one except block.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

    def sanitize_for_logging(self) -> dict[str, object]:
        """Default PHI-free structured representation for logs.

        Body fields (``response_data``, server ``details.text``, etc.) are
        never included. Subclasses that attach non-PHI context (method,
        path_template) override this to add those fields back.
        """
        return {
            "type": type(self).__name__,
            "status_code": self.status_code,
        }


def _issue_field(issue: object, name: str) -> str | None:
    if isinstance(issue, dict):
        value = issue.get(name)
        return value if isinstance(value, str) else None
    value = getattr(issue, name, None)
    return value if isinstance(value, str) else None


class OperationOutcomeError(MedplumError):
    """FHIR OperationOutcome error.

    The string representation carries only ``severity/code`` pairs —
    never the server's ``diagnostics`` or ``details.text``, which can
    echo caller-supplied values (PHI risk) and routinely end up in
    error-tracking sinks via ``str(exc)``. This matches the
    ``BadRequestError`` convention.

    The human-readable server text is preserved on ``self.detail`` for
    interactive triage, and the full OperationOutcome on
    ``self.outcome``. Use ``sanitize_for_logging()`` for structured
    logging to PHI-restricted sinks.
    """

    def __init__(
        self,
        *,
        outcome: dict[str, Any] | object,
        status_code: int | None = None,
    ) -> None:
        self.outcome = outcome
        issues = (
            outcome.get("issue", [])
            if isinstance(outcome, dict)
            else getattr(outcome, "issue", []) or []
        )
        parts = []
        detail_parts = []
        for issue in issues:
            severity = _issue_field(issue, "severity")
            code = _issue_field(issue, "code")
            parts.append(f"{severity}/{code}")
            diagnostics = _issue_field(issue, "diagnostics")
            details_text: str | None = None
            details = (
                issue.get("details")
                if isinstance(issue, dict)
                else getattr(issue, "details", None)
            )
            if isinstance(details, dict):
                text = details.get("text")
                if isinstance(text, str):
                    details_text = text
            elif details is not None:
                text = getattr(details, "text", None)
                if isinstance(text, str):
                    details_text = text
            detail_segments = [s for s in (diagnostics, details_text) if s]
            if detail_segments:
                detail_parts.append(" | ".join(detail_segments))
        self.detail: str | None = "; ".join(detail_parts) or None
        super().__init__(
            "OperationOutcome: " + ("; ".join(parts) if parts else "no issues"),
            status_code=status_code,
        )

    def sanitize_for_logging(self) -> dict[str, object]:
        """Return a dict safe to emit to logs (no diagnostics/details.text)."""
        issues = (
            self.outcome.get("issue", [])
            if isinstance(self.outcome, dict)
            else getattr(self.outcome, "issue", []) or []
        )
        return {
            "type": type(self).__name__,
            "issues": [
                {
                    "severity": _issue_field(i, "severity"),
                    "code": _issue_field(i, "code"),
                }
                for i in issues
            ],
        }


class AuthenticationError(MedplumError):
    """Authentication failed or token expired.

    Raised when:
    - Client credentials are invalid
    - Access token has expired
    - Server returns 401 Unauthorized

    Recovery:
    - Check client_id and client_secret
    - Re-authenticate
    - Refresh token
    """

    pass


class AuthorizationError(MedplumError):
    """User lacks permission for requested resource.

    Raised when:
    - User doesn't have access to resource
    - Server returns 403 Forbidden
    - on_behalf_of membership has insufficient permissions

    Recovery:
    - Verify user permissions in Medplum
    - Check ProjectMembership access rules
    - Use different on_behalf_of membership
    """

    pass


class NotFoundError(MedplumError):
    """Requested FHIR resource not found.

    Raised when:
    - Resource ID doesn't exist
    - Resource was deleted
    - Server returns 404 Not Found

    Recovery:
    - Verify resource ID is correct
    - Check if resource was deleted
    - Search instead of direct read
    """

    pass


class GoneError(NotFoundError):
    """Resource was deleted (HTTP 410 Gone).

    Medplum soft-deletes resources and returns 410 for subsequent reads.
    Subclasses :class:`NotFoundError` so existing ``except NotFoundError``
    handlers treat deleted and missing resources uniformly; catch
    ``GoneError`` first to distinguish "was deleted" from "never existed".
    """

    pass


class ConflictError(MedplumError):
    """Request conflicts with current server state (HTTP 409).

    Raised when:
    - Concurrent writes hit a database serialization conflict
    - A scheduling operation (e.g. ``$book``) loses a slot race
    - Server returns 409 Conflict

    Recovery:
    - Re-read the resource and retry the operation against fresh state
    """

    pass


class BadRequestError(MedplumError):
    """Error for 400 Bad Request responses.

    The default message is "Bad Request" and ``str(exc)`` never echoes
    server-provided ``details.text`` or ``diagnostics`` (PHI risk).
    The full server OperationOutcome remains on ``exc.response_data``.
    """


class ValidationError(MedplumError):
    """Resource data failed validation.

    The SDK itself never raises this: server-side FHIR validation
    failures (HTTP 400) raise :class:`BadRequestError`. This class
    exists for callers that want to raise or map validation semantics
    of their own while staying inside the ``MedplumError`` hierarchy.
    """

    pass


class RateLimitError(MedplumError):
    """Rate limit exceeded.

    Raised when:
    - Too many requests in time window
    - Server returns 429 Too Many Requests

    Recovery:
    - Implement exponential backoff
    - Reduce request frequency
    - Check rate limit headers
    """

    pass


class ServerError(MedplumError):
    """Medplum server error (HTTP 5xx).

    The string representation intentionally omits the response body and
    the raw path (resource IDs embedded in ``/Patient/<id>`` are PHI).
    ``path_template`` is the PHI-free substitution used in logs; callers
    that need the exact path must read ``self.path``.
    """

    def __init__(
        self,
        *,
        status_code: int,
        method: str,
        path: str,
        path_template: str,
        response: "httpx.Response | None" = None,
    ) -> None:
        super().__init__(
            f"Server error (HTTP {status_code}) from {method} {path_template}",
            status_code=status_code,
        )
        self.method = method
        self.path = path
        self.path_template = path_template
        self.response = response
        self.has_resource_id = path != path_template

    def sanitize_for_logging(self) -> dict[str, object]:
        """Return a dict safe to emit to logs (no response body, no path)."""
        return {
            "type": type(self).__name__,
            "status": self.status_code,
            "method": self.method,
            "path_template": self.path_template,
            "has_resource_id": self.has_resource_id,
        }


class PreconditionFailedError(MedplumError):
    """Precondition failed (HTTP 412).

    Raised when:
    - If-Match header doesn't match current resource version (optimistic locking)
    - If-None-Match precondition fails
    - If-Modified-Since precondition fails
    - If-Unmodified-Since precondition fails
    - Server returns 412 Precondition Failed

    Common scenarios:
    - Version conflict during optimistic locking (concurrent updates)
    - Conditional request preconditions not met
    - Resource modified since last retrieval in race conditions

    Recovery:
    - Re-fetch the resource to get current state
    - Re-evaluate if operation should still proceed
    - Retry operation with updated preconditions if appropriate
    """

    pass


class NetworkError(MedplumError):
    """Network communication error.

    Raised when:
    - Connection timeout
    - DNS resolution failure
    - Network unreachable

    Recovery:
    - Check internet connection
    - Verify Medplum base URL
    - Check firewall/proxy settings
    """

    pass


class InsecureTransportError(MedplumError):
    """Constructor received a non-https URL without explicit opt-in."""


class UnsafeRedirectError(MedplumError):
    """Attempted to follow or construct a URL outside the configured origin."""


class TokenRefreshCooldownError(MedplumError):
    """Raised when token refresh is requested during the cooldown window
    after a prior refresh failure.

    Callers should respect exc.retry_after. DO NOT catch this and retry
    in a tight loop — the cooldown exists specifically to avoid piling
    on during an OAuth endpoint outage.
    """

    def __init__(self, failed_at: datetime, cooldown: timedelta) -> None:
        self._failed_at = failed_at
        self._cooldown = cooldown
        elapsed = datetime.now(timezone.utc) - failed_at
        self._retry_after = max(0.0, (cooldown - elapsed).total_seconds())
        super().__init__(
            f"Token refresh in cooldown for "
            f"{self._retry_after:.1f}s after prior failure."
        )

    @property
    def retry_after(self) -> float:
        """Seconds remaining before the cooldown expires."""
        return self._retry_after
