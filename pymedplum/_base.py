from __future__ import annotations

import warnings
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qsl

import httpx

from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    NotFoundError,
    OperationOutcomeError,
    PreconditionFailedError,
    RateLimitError,
    ServerError,
)
from .helpers import decode_jwt_exp

if TYPE_CHECKING:
    from .async_client import AsyncMedplumClient
    from .client import MedplumClient
    from .fhir.operationoutcome import OperationOutcome
    from .types import BeforeRequestCallback


def _raise_or_json(response: httpx.Response) -> dict[str, Any | None]:
    """Parse response or raise appropriate exception based on status code.

    Args:
        response: httpx Response object

    Returns:
        Parsed JSON if successful, None if no content (204)

    Raises:
        AuthenticationError: On 401 Unauthorized
        AuthorizationError: On 403 Forbidden
        NotFoundError: On 404 Not Found
        PreconditionFailedError: On 412 Precondition Failed
        BadRequestError: On 400 Bad Request
        OperationOutcomeError: On other error responses
    """
    if 200 <= response.status_code < 300:
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    try:
        outcome = response.json()
        error_text = response.text
        if (
            isinstance(outcome, dict)
            and outcome.get("resourceType") == "OperationOutcome"
        ):
            issues = outcome.get("issue", [])
            if issues and isinstance(issues, list):
                details = issues[0].get("details", {})
                if isinstance(details, dict):
                    error_text = details.get("text", response.text)
    except ValueError:
        outcome = None
        error_text = response.text

    if response.status_code == 400:
        raise BadRequestError(error_text, status_code=400, response_data=outcome)
    elif response.status_code == 401:
        raise AuthenticationError(
            "Authentication failed or token expired",
            status_code=401,
            response_data=outcome,
        )
    elif response.status_code == 403:
        raise AuthorizationError(
            "Access denied - insufficient permissions",
            status_code=403,
            response_data=outcome,
        )
    elif response.status_code == 404:
        raise NotFoundError(
            "Resource not found", status_code=404, response_data=outcome
        )
    elif response.status_code == 412:
        raise PreconditionFailedError(
            "Precondition failed - resource may have been modified by another process",
            status_code=412,
            response_data=outcome,
        )
    elif response.status_code == 429:
        raise RateLimitError(
            "Rate limit exceeded", status_code=429, response_data=outcome
        )
    elif response.status_code >= 500:
        raise ServerError(
            error_text,
            status_code=response.status_code,
            response_data=outcome,
        )
    else:
        raise OperationOutcomeError(response.status_code, outcome, error_text)


class BaseClient:
    """Shared logic for sync and async clients."""

    def __init__(
        self,
        base_url: str = "https://api.medplum.com/",
        client_id: str | None = None,
        client_secret: str | None = None,
        access_token: str | None = None,
        fhir_url_path: str = "fhir/R4/",
        project_id: str | None = None,
        before_request: BeforeRequestCallback | None = None,
        default_on_behalf_of: str | None = None,
    ):
        self.base_url = base_url.rstrip("/") + "/"
        self.fhir_base_url = self.base_url + fhir_url_path
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.project_id = project_id
        self.before_request = before_request
        self.default_on_behalf_of = default_on_behalf_of

        self.token_expires_at: datetime | None = None
        self._obo_stack: list[str] = []

        # If access_token was provided, try to extract expiry from JWT
        if self.access_token:
            self.token_expires_at = decode_jwt_exp(self.access_token)

    def set_access_token(self, token: str, expires_at: datetime | None = None) -> None:
        """Set the access token explicitly.

        This allows using an externally-acquired access token instead of
        authenticating with client credentials. If expires_at is not provided,
        the method will attempt to decode the expiration from the JWT.

        Args:
            token: The access token string
            expires_at: Optional expiration datetime. If not provided and the
                token is a valid JWT, expiration will be decoded from it.

        Example:
            # Create client without credentials
            client = MedplumClient(base_url="https://api.medplum.com/")

            # Set externally-acquired token
            client.set_access_token(my_token)

            # Now client can make authenticated requests
            patient = client.read_resource("Patient", "123")
        """
        self.access_token = token
        if expires_at is not None:
            self.token_expires_at = expires_at
        else:
            # Try to decode expiry from JWT
            self.token_expires_at = decode_jwt_exp(token)

    def _obo_current(self) -> str | None:
        """Get current on-behalf-of membership (top of stack)."""
        return self._obo_stack[-1] if self._obo_stack else None

    def _get_headers(self) -> dict[str, str]:
        """Build request headers with auth, OBO, and Medplum extension."""
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
            "X-Medplum": "extended",  # Required for OBO/audit
        }

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        obo = self._obo_current() or self.default_on_behalf_of
        if obo:
            headers["X-Medplum-On-Behalf-Of"] = self._normalize_membership(obo)

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
                "before using on-behalf-of. Call authenticate() first."
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

        Args:
            job: Job ID, full URL, OperationOutcome dict, or
                OperationOutcome Pydantic model

        Returns:
            Full URL for polling the job status
        """
        if hasattr(job, "model_dump"):
            job = job.model_dump(by_alias=True, exclude_none=True)

        if isinstance(job, dict):
            issues = job.get("issue", [])
            if issues and isinstance(issues[0], dict):
                url = issues[0].get("diagnostics")
                if url:
                    return url
            raise ValueError(
                "Expected OperationOutcome with job URL in issue[0].diagnostics"
            )

        if job.startswith(("http://", "https://")):
            return job

        return f"{self.base_url}fhir/R4/job/{job}/status"

    def _build_query_params(self, query: Any) -> list[tuple]:
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
    """Context manager for on-behalf-of operations with auto-authentication.

    Supports nested contexts safely and auto-authenticates if needed.
    """

    def __init__(self, client: MedplumClient, membership: str | Any):
        self.client = client
        self.member_ref = client._normalize_membership(membership)

    def __enter__(self):
        # Auto-authenticate if not already authenticated
        if (
            (not self.client.access_token or self.client._should_refresh_token())
            and self.client.client_id
            and self.client.client_secret
        ):
            self.client.authenticate()

        self.client._validate_on_behalf_of_usage()
        self.client._obo_stack.append(self.member_ref)
        return self.client

    def __exit__(self, *exc):
        self.client._obo_stack.pop()


class AsyncOnBehalfOfContext:
    """Async context manager for on-behalf-of operations with auto-authentication."""

    def __init__(self, client: AsyncMedplumClient, membership: str | Any):
        self.client = client
        self.member_ref = client._normalize_membership(membership)

    async def __aenter__(self):
        # Auto-authenticate if not already authenticated
        if (
            (not self.client.access_token or self.client._should_refresh_token())
            and self.client.client_id
            and self.client.client_secret
        ):
            await self.client.authenticate()

        self.client._validate_on_behalf_of_usage()
        self.client._obo_stack.append(self.member_ref)
        return self.client

    async def __aexit__(self, *exc):
        self.client._obo_stack.pop()
