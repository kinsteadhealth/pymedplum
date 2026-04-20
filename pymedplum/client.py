from __future__ import annotations

import inspect
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload
from urllib.parse import urlparse

import httpx

from ._auth import TokenManager, TokenSource
from ._base import (
    MAX_WIRE_ATTEMPTS,
    BaseClient,
    OnBehalfOfContext,
    _append_search_options,
    _AttemptTracker,
    _finalize_response,
    _merge_params_into_url,
    _resolve_if_match,
    _retry_budget_exceeded,
    _retry_delay,
)
from ._fhir_ops import (
    build_codesystem_lookup_params,
    build_codesystem_validate_params,
    build_conceptmap_translate_params,
    build_valueset_expand_params,
    build_valueset_validate_params,
    dict_to_parameters,
    is_parameters_resource,
)
from ._security import (
    assert_same_origin,
    build_raw_request_url,
    sanitize_if_none_exist,
    validate_as_fhir_class,
    validate_operation_name,
    validate_resource_id,
    validate_resource_type,
)
from .bundle import FHIRBundle
from .exceptions import (
    MedplumError,
    TokenRefreshCooldownError,
)
from .fhir.base import MedplumFHIRBase
from .helpers import to_fhir_json
from .hooks import (
    AsyncOnRequestCompleteHook,
    BeforeRequestHook,
    OnRequestCompleteHook,
    PreparedRequest,
    _parse_fhir_url,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .fhir.operationoutcome import OperationOutcome
    from .types import PatchOperation, QueryTypes, SummaryMode, TotalMode

_request_logger = logging.getLogger("pymedplum.request")

ResourceT = TypeVar("ResourceT", bound=MedplumFHIRBase)


class MedplumClient(BaseClient):
    """Synchronous Medplum client with retry logic and production features"""

    def __init__(
        self,
        base_url: str = "https://api.medplum.com/",
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        access_token: str | None = None,
        project_id: str | None = None,
        fhir_url_path: str = "fhir/R4/",
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
        before_request: BeforeRequestHook | None = None,
        on_request_complete: OnRequestCompleteHook
        | AsyncOnRequestCompleteHook
        | None = None,
        allow_insecure_http: bool = False,
        failed_refresh_cooldown: float = 1.0,
        default_on_behalf_of: str | None = None,
        max_retry_delay_seconds: float = 60.0,
    ) -> None:
        if on_request_complete is not None and inspect.iscoroutinefunction(
            on_request_complete
        ):
            raise TypeError(
                "MedplumClient (sync) does not accept an async "
                "on_request_complete hook. Use AsyncMedplumClient or "
                "provide a sync callable."
            )
        super().__init__(
            base_url,
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            project_id=project_id,
            fhir_url_path=fhir_url_path,
            before_request=before_request,
            on_request_complete=on_request_complete,
            allow_insecure_http=allow_insecure_http,
            default_on_behalf_of=default_on_behalf_of,
            max_retry_delay_seconds=max_retry_delay_seconds,
        )

        if http_client is not None:
            if http_client.follow_redirects is not False:
                raise ValueError(
                    "http_client must be constructed with "
                    "follow_redirects=False. The SDK handles pagination and "
                    "async-job polling with explicit same-origin validation; "
                    "auto-followed redirects can leak auth headers to a "
                    "different origin."
                )
            self._http = http_client
        else:
            self._http = httpx.Client(timeout=timeout, follow_redirects=False)
        self._owns_http_client = http_client is None

        if self.client_id and self.client_secret:
            source = TokenSource.MANAGED
        elif self.access_token:
            source = TokenSource.EXTERNAL
        else:
            source = TokenSource.MANAGED
        self._tokens: TokenManager = TokenManager(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token,
            token_expires_at=self.token_expires_at,
            token_url=f"{self.base_url}oauth2/token",
            source=source,
            failed_refresh_cooldown=timedelta(seconds=failed_refresh_cooldown),
        )
        self._tokens.set_auth_event_dispatcher(self._dispatch_auth_event_sync)

    def __enter__(self) -> MedplumClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Close HTTP client and shut down the token-refresh executor."""
        self._tokens.close()
        if self._owns_http_client:
            self._http.close()

    @overload
    def _request(
        self,
        method: str,
        url: str,
        *,
        on_behalf_of: str | None = ...,
        raw: Literal[False] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    @overload
    def _request(
        self,
        method: str,
        url: str,
        *,
        on_behalf_of: str | None = ...,
        raw: Literal[True],
        **kwargs: Any,
    ) -> httpx.Response: ...

    def _request(
        self,
        method: str,
        url: str,
        *,
        on_behalf_of: str | None = None,
        raw: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | httpx.Response:
        """Make HTTP request with retry logic and OperationOutcome handling.

        When ``raw=True``, the underlying :class:`httpx.Response` is returned
        for successful (2xx) responses instead of the parsed JSON body — for
        binary/non-JSON endpoints like ``download_binary`` and ``export_ccda``.
        Error responses still flow through :func:`_raise_or_json` and raise.
        The ``on_request_complete`` hook fires exactly once regardless.
        """
        self._ensure_authenticated()
        final_url = _merge_params_into_url(url, kwargs.pop("params", None))
        prepared = self._apply_before_request(
            self._build_initial_prepared(
                method,
                final_url,
                caller_headers=kwargs.pop("headers", None),
                json_body=kwargs.get("json"),
            )
        )
        if prepared.json_body is not None:
            kwargs["json"] = prepared.json_body
        base_non_auth_headers = dict(prepared.headers)
        tracker = _AttemptTracker(
            method=prepared.method,
            url=prepared.url,
            started_at=datetime.now(timezone.utc),
            fhir_url_path=self.fhir_url_path,
        )
        try:
            response = self._send_with_retries(
                prepared,
                base_non_auth_headers,
                tracker,
                on_behalf_of=on_behalf_of,
                kwargs=kwargs,
            )
            tracker.final_status_code = response.status_code
            return _finalize_response(
                response, raw=raw, fhir_url_path=self.fhir_url_path
            )
        except BaseException as exc:
            if tracker.final_exception is None:
                tracker.final_exception = exc
            raise
        finally:
            self._dispatch_on_request_complete_sync(
                tracker.build_event(datetime.now(timezone.utc))
            )

    def _send_one(
        self,
        prepared: PreparedRequest,
        headers: dict[str, str],
        wire_obo: str | None,
        tracker: _AttemptTracker,
        kwargs: dict[str, Any],
        path_template: str,
    ) -> httpx.Response:
        """Issue one wire call, record it on the tracker, raise on transport error."""
        attempt_number = len(tracker.attempts) + 1
        _request_logger.debug(
            "request: %s %s (attempt %d)",
            prepared.method,
            path_template,
            attempt_number,
        )
        perf = time.perf_counter()
        exc: BaseException | None = None
        response: httpx.Response | None = None
        try:
            response = self._http.request(
                prepared.method, prepared.url, headers=headers, **kwargs
            )
        except Exception as e:
            exc = e
        duration = time.perf_counter() - perf
        tracker.record(
            status_code=response.status_code if response is not None else None,
            duration_seconds=duration,
            on_behalf_of=wire_obo,
            exception=exc,
        )
        if exc is not None:
            _request_logger.debug(
                "request: %s %s failed in %.3fs (%s)",
                prepared.method,
                path_template,
                duration,
                type(exc).__name__,
            )
            tracker.final_exception = exc
            raise exc
        assert response is not None
        _request_logger.debug(
            "request: %s %s completed in %.3fs with status %d",
            prepared.method,
            path_template,
            duration,
            response.status_code,
        )
        return response

    def _send_with_retries(
        self,
        prepared: PreparedRequest,
        base_non_auth_headers: dict[str, str],
        tracker: _AttemptTracker,
        *,
        on_behalf_of: str | None,
        kwargs: dict[str, Any],
    ) -> httpx.Response:
        """Drive the transient-failure retry loop and the 401-refresh branch."""
        _, _, _, path_template = _parse_fhir_url(
            urlparse(prepared.url).path, self.fhir_url_path
        )
        for attempt in range(MAX_WIRE_ATTEMPTS):
            wire_obo = self._resolve_on_behalf_of(on_behalf_of)
            headers = self._finalize_headers_for_wire(base_non_auth_headers, wire_obo)
            response = self._send_one(
                prepared, headers, wire_obo, tracker, kwargs, path_template
            )
            if self._should_refresh_on_401(response, attempt):
                refreshed = self._refresh_and_retry_once(
                    prepared,
                    base_non_auth_headers,
                    tracker,
                    on_behalf_of=on_behalf_of,
                    kwargs=kwargs,
                    path_template=path_template,
                )
                if refreshed is None:
                    return response
                response = refreshed
            delay = _retry_delay(
                response,
                attempt,
                max_retry_delay_seconds=self.max_retry_delay_seconds,
            )
            if delay is not None and not _retry_budget_exceeded(
                response.status_code, attempt
            ):
                reason = "429" if response.status_code == 429 else "5xx"
                _request_logger.debug(
                    "request: retry scheduled in %.3fs (reason: %s)",
                    delay,
                    reason,
                )
                time.sleep(delay)
                continue
            return response
        _request_logger.debug("request: retry budget exhausted")
        raise MedplumError("Request failed after retries")

    def _refresh_and_retry_once(
        self,
        prepared: PreparedRequest,
        base_non_auth_headers: dict[str, str],
        tracker: _AttemptTracker,
        *,
        on_behalf_of: str | None,
        kwargs: dict[str, Any],
        path_template: str,
    ) -> httpx.Response | None:
        """Force-refresh the token and replay the request exactly once.

        Returns ``None`` if the refresh failed so the caller surfaces the
        original 401; otherwise returns the replayed response.
        """
        try:
            self._tokens.force_refresh(self._http)
        except (MedplumError, TokenRefreshCooldownError):
            return None
        self.access_token = self._tokens.access_token
        self.token_expires_at = self._tokens.token_expires_at
        wire_obo = self._resolve_on_behalf_of(on_behalf_of)
        headers = self._finalize_headers_for_wire(base_non_auth_headers, wire_obo)
        return self._send_one(
            prepared, headers, wire_obo, tracker, kwargs, path_template
        )

    def _ensure_authenticated(self) -> None:
        self._tokens.ensure_authenticated(self._http)
        if self._tokens.access_token is not None:
            self.access_token = self._tokens.access_token
        if self._tokens.token_expires_at is not None:
            self.token_expires_at = self._tokens.token_expires_at

    def on_behalf_of(self, membership: str | Any) -> OnBehalfOfContext:
        """Create context manager for on-behalf-of operations.

        Example:
            with client.on_behalf_of("ProjectMembership/123"):
                patient = client.read_resource("Patient", "456")

        Args:
            membership: ProjectMembership resource or ID string

        Returns:
            Context manager that sets X-Medplum-On-Behalf-Of header
        """
        return OnBehalfOfContext(self, membership)

    @overload
    def create_resource(
        self,
        resource: dict[str, Any] | Any,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: type[ResourceT],
        on_behalf_of: str | None = None,
    ) -> ResourceT:
        pass

    @overload
    def create_resource(
        self,
        resource: dict[str, Any] | Any,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: None = None,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        pass

    def create_resource(
        self,
        resource: dict[str, Any] | Any,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: type[ResourceT] | None = None,
        on_behalf_of: str | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Create a FHIR resource.

        Args:
            resource: FHIR resource dict or Pydantic model
            headers: Optional HTTP headers to include in the request
            accounts: Account references to set on meta.accounts at
                creation time (e.g., "Organization/abc" or a list)
            as_fhir: Optional FHIR resource class for typed response
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Create and get as dict
            patient_dict = client.create_resource({
                "resourceType": "Patient",
                "name": [{"given": ["Alice"], "family": "Smith"}]
            })

            # Type-safe creation with Pydantic models
            from pymedplum.fhir import Patient
            patient = client.create_resource(
                {"resourceType": "Patient", "name": [{"given": ["Alice"], "family": "Smith"}]},
                as_fhir=Patient
            )
            print(patient.name[0].given)  # Full IDE autocomplete!
        """
        data = to_fhir_json(resource)

        if accounts is not None:
            data = self._apply_accounts(data, accounts)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")
        validate_resource_type(resource_type)

        response = self._request(
            "POST",
            f"{self.fhir_base_url}{resource_type}",
            json=data,
            headers=headers,
            on_behalf_of=on_behalf_of,
        )

        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
            return as_fhir(**response)

        return response

    @overload
    def create_resource_if_none_exist(
        self,
        resource: dict[str, Any] | Any,
        if_none_exist: str,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: type[ResourceT],
        on_behalf_of: str | None = None,
    ) -> ResourceT:
        pass

    @overload
    def create_resource_if_none_exist(
        self,
        resource: dict[str, Any] | Any,
        if_none_exist: str,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: None = None,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        pass

    def create_resource_if_none_exist(
        self,
        resource: dict[str, Any] | Any,
        if_none_exist: str,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: type[ResourceT] | None = None,
        on_behalf_of: str | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Conditionally create a resource only if no matching resource exists.

        Uses the FHIR conditional create pattern with the If-None-Exist header.
        This enables idempotent resource creation - calling multiple times with
        the same search criteria returns the same resource without duplicates.

        Args:
            resource: FHIR resource dict or Pydantic model to create
            if_none_exist: Search query string for matching existing resources
                (e.g., "identifier=http://example.org|12345")
            headers: Optional HTTP headers to include in the request
            accounts: Account references to set on meta.accounts at
                creation time (e.g., "Organization/abc" or a list)
            as_fhir: Optional FHIR resource class for typed response
            on_behalf_of: Optional ProjectMembership ID to act on behalf
                of for this request (overrides any context-bound value)

        Returns:
            Created or existing resource (as dict or typed model if as_fhir provided)

        Note:
            - Returns HTTP 201 Created with new resource if no match found
            - Returns HTTP 200 OK with existing resource if exactly one match
            - Returns HTTP 412 Precondition Failed if multiple matches exist

        Examples:
            # Create patient only if identifier doesn't exist
            patient = client.create_resource_if_none_exist(
                {"resourceType": "Patient", "identifier": [
                    {"system": "http://example.org/mrn", "value": "12345"}
                ]},
                if_none_exist="identifier=http://example.org/mrn|12345"
            )

            # Type-safe conditional creation
            from pymedplum.fhir import Patient
            patient = client.create_resource_if_none_exist(
                {"resourceType": "Patient", "identifier": [...]},
                if_none_exist="identifier=http://example.org/mrn|12345",
                as_fhir=Patient
            )
        """
        data = to_fhir_json(resource)

        if accounts is not None:
            data = self._apply_accounts(data, accounts)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")
        validate_resource_type(resource_type)

        normalized_query = sanitize_if_none_exist(if_none_exist, self.base_url)

        request_headers = {"If-None-Exist": normalized_query}
        if headers:
            request_headers.update(headers)

        response = self._request(
            "POST",
            f"{self.fhir_base_url}{resource_type}",
            json=data,
            headers=request_headers,
            on_behalf_of=on_behalf_of,
        )

        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
            return as_fhir(**response)

        return response

    @overload
    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: type[ResourceT]
    ) -> ResourceT:
        pass

    @overload
    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: None = None
    ) -> dict[str, Any]:
        pass

    def read_resource(
        self,
        resource_type: str,
        resource_id: str,
        as_fhir: type[ResourceT] | None = None,
        *,
        headers: dict[str, str] | None = None,
        on_behalf_of: str | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Read a FHIR resource by type and ID."""
        validate_resource_type(resource_type)
        validate_resource_id(resource_id)
        response = self._request(
            "GET",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            headers=headers,
            on_behalf_of=on_behalf_of,
        )

        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
            return as_fhir(**response)

        return response

    @overload
    def vread_resource(
        self,
        resource_type: str,
        resource_id: str,
        version_id: str,
        as_fhir: type[ResourceT],
    ) -> ResourceT:
        pass

    @overload
    def vread_resource(
        self,
        resource_type: str,
        resource_id: str,
        version_id: str,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    def vread_resource(
        self,
        resource_type: str,
        resource_id: str,
        version_id: str,
        as_fhir: type[ResourceT] | None = None,
        *,
        headers: dict[str, str] | None = None,
        on_behalf_of: str | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Read a specific version of a FHIR resource (vread).

        The vread operation retrieves a specific historical version of a resource.
        This is useful for auditing, comparing versions, or restoring previous states.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            version_id: Version ID (found in meta.versionId)
            as_fhir: Optional FHIR resource class for typed response
            headers: Optional HTTP headers to include in the request
            on_behalf_of: Optional ProjectMembership ID to act on behalf
                of for this request (overrides any context-bound value)

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Get a specific version as dict
            patient_v1 = client.vread_resource("Patient", "123", "1")

            # Type-safe versioned read
            from pymedplum.fhir import Patient
            patient_v1 = client.vread_resource("Patient", "123", "1", as_fhir=Patient)

            # Compare versions
            current = client.read_resource("Patient", "123")
            version_id = current["meta"]["versionId"]
            previous = client.vread_resource("Patient", "123", str(int(version_id) - 1))
        """
        validate_resource_type(resource_type)
        validate_resource_id(resource_id)
        validate_resource_id(version_id, field="version_id")
        response = self._request(
            "GET",
            f"{self.fhir_base_url}{resource_type}/{resource_id}/_history/{version_id}",
            headers=headers,
            on_behalf_of=on_behalf_of,
        )

        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
            return as_fhir(**response)

        return response

    @overload
    def update_resource(
        self,
        resource: dict[str, Any] | Any,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: type[ResourceT],
        on_behalf_of: str | None = None,
        if_match: bool | str = True,
    ) -> ResourceT:
        pass

    @overload
    def update_resource(
        self,
        resource: dict[str, Any] | Any,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: None = None,
        on_behalf_of: str | None = None,
        if_match: bool | str = True,
    ) -> dict[str, Any]:
        pass

    def update_resource(
        self,
        resource: dict[str, Any] | Any,
        *,
        headers: dict[str, str] | None = None,
        accounts: str | list[str] | None = None,
        as_fhir: type[ResourceT] | None = None,
        on_behalf_of: str | None = None,
        if_match: bool | str = True,
    ) -> dict[str, Any] | ResourceT:
        """Update a FHIR resource (requires id).

        Args:
            resource: FHIR resource dict or Pydantic model
            headers: Optional HTTP headers. An explicit ``If-Match`` here
                always wins over the ``if_match`` keyword.
            accounts: Account references to set on meta.accounts
                (e.g., "Organization/abc" or a list)
            as_fhir: Optional Pydantic model class to parse response into
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.
            if_match: Optimistic-concurrency control. ``True`` (default)
                auto-attaches ``If-Match: W/"<versionId>"`` from
                ``resource.meta.versionId`` if present. ``False`` opts
                out. A string is sent verbatim as the ``If-Match`` value.

        Returns:
            Updated resource as dict or Pydantic model if as_fhir provided

        Example with optimistic locking:
            # Retrieve resource
            patient = client.read_resource("Patient", "123")

            # If-Match is auto-attached from meta.versionId by default.
            patient["active"] = True
            updated = client.update_resource(patient)

        Example with type-safe response:
            from pymedplum.fhir import Patient

            patient["active"] = False
            updated = client.update_resource(patient, as_fhir=Patient)
            # updated is now a Pydantic Patient model
        """
        data = to_fhir_json(resource)

        if accounts is not None:
            data = self._apply_accounts(data, accounts)

        resource_type = data.get("resourceType")
        resource_id = data.get("id")

        if not resource_type or not resource_id:
            raise ValueError("Resource must have resourceType and id for update")
        validate_resource_type(resource_type)
        validate_resource_id(resource_id)

        resolved_if_match = _resolve_if_match(resource, if_match)
        merged_headers: dict[str, str] = {}
        if resolved_if_match is not None:
            merged_headers["If-Match"] = resolved_if_match
        if headers:
            merged_headers.update(headers)

        response = self._request(
            "PUT",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=data,
            headers=merged_headers or None,
            on_behalf_of=on_behalf_of,
        )

        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
            return as_fhir(**response)

        return response

    @overload
    def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        *,
        headers: dict[str, str] | None = None,
        as_fhir: type[ResourceT],
        on_behalf_of: str | None = None,
    ) -> ResourceT:
        pass

    @overload
    def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        *,
        headers: dict[str, str] | None = None,
        as_fhir: None = None,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        pass

    def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        *,
        headers: dict[str, str] | None = None,
        as_fhir: type[ResourceT] | None = None,
        on_behalf_of: str | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Apply JSON Patch operations to a resource.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            operations: List of JSON Patch operations
            headers: Optional HTTP headers (e.g., If-Match for optimistic locking)
            as_fhir: Optional FHIR resource class for typed response
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Patch and get as dict
            operations = [{"op": "replace", "path": "/active", "value": False}]
            patched = client.patch_resource("Patient", "123", operations)

            # Type-safe patching with Pydantic models
            from pymedplum.fhir import Patient
            operations = [{"op": "replace", "path": "/active", "value": True}]
            patched = client.patch_resource("Patient", "123", operations, as_fhir=Patient)
            print(patched.active)  # Full IDE autocomplete!
        """
        validate_resource_type(resource_type)
        validate_resource_id(resource_id)
        patch_headers = {"Content-Type": "application/json-patch+json"}
        if headers:
            patch_headers.update(headers)

        response = self._request(
            "PATCH",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=operations,
            headers=patch_headers,
            on_behalf_of=on_behalf_of,
        )

        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
            return as_fhir(**response)

        return response

    def delete_resource(
        self,
        resource_type: str,
        resource_id: str,
        *,
        headers: dict[str, str] | None = None,
        on_behalf_of: str | None = None,
    ) -> None:
        """Delete a FHIR resource."""
        validate_resource_type(resource_type)
        validate_resource_id(resource_id)
        self._request(
            "DELETE",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            headers=headers,
            on_behalf_of=on_behalf_of,
        )

    @overload
    def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[False] = False,
        as_fhir: None = None,
        *,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        pass

    @overload
    def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: None = None,
        *,
        on_behalf_of: str | None = None,
    ) -> FHIRBundle[dict[str, Any]]:
        pass

    @overload
    def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: type[ResourceT] = ...,
        *,
        on_behalf_of: str | None = None,
    ) -> FHIRBundle[ResourceT]:
        pass

    def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: bool = False,
        as_fhir: type[ResourceT] | None = None,
        *,
        on_behalf_of: str | None = None,
    ) -> FHIRBundle[ResourceT] | FHIRBundle[dict[str, Any]] | dict[str, Any]:
        """Search for FHIR resources.

        Args:
            resource_type: FHIR resource type
            query: Search parameters
            return_bundle: If True, wrap in FHIRBundle helper
            as_fhir: Optional FHIR resource class for typed response (only applies when return_bundle=True)
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            FHIRBundle wrapper, or raw dict

        Examples:
            # Get raw Bundle dict
            bundle_dict = client.search_resources("Patient", {"family": "Smith"})

            # Use FHIRBundle wrapper for convenience methods
            bundle = client.search_resources("Patient", {}, return_bundle=True)
            for patient in bundle:
                print(patient['name'])

            # Type-safe access with Pydantic models
            from pymedplum.fhir import Patient
            bundle = client.search_resources("Patient", {}, return_bundle=True, as_fhir=Patient)
            patients = bundle.get_resources_typed(Patient)
        """
        validate_resource_type(resource_type)
        params = self._build_query_params(query)
        response = self._request(
            "GET",
            f"{self.fhir_base_url}{resource_type}",
            params=params,
            on_behalf_of=on_behalf_of,
        )

        if return_bundle:
            bundle: FHIRBundle[Any] = FHIRBundle(response)
            if as_fhir:
                validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
                bundle._resource_class = as_fhir
            return bundle

        return response

    def search_one(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        *,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any] | None:
        """Search for a single resource (limit 1).

        Args:
            resource_type: Type of resource to search
            query: Search parameters
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            First matching resource or None
        """
        validate_resource_type(resource_type)
        params = self._build_query_params(query)
        params.append(("_count", "1"))

        bundle = self._request(
            "GET",
            f"{self.fhir_base_url}{resource_type}",
            params=params,
            on_behalf_of=on_behalf_of,
        )
        entries = bundle.get("entry", [])

        if entries and "resource" in entries[0]:
            resource = entries[0]["resource"]
            return resource if isinstance(resource, dict) else None
        return None

    def search_resource_pages(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        as_fhir: type[ResourceT] | None = None,
        *,
        on_behalf_of: str | None = None,
        max_resources: int | None = None,
    ) -> Iterator[ResourceT | dict[str, Any]]:
        """Search resources with automatic pagination.

        Args:
            resource_type: FHIR resource type
            query: Search parameters
            as_fhir: Optional FHIR resource class for typed response
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.
            max_resources: Optional cap on total resources yielded across
                pages. Stops following ``next`` links once the cap is hit.
                Default ``None`` preserves the historical unbounded
                behavior for legitimate bulk-data flows.

        Yields:
            Individual resources from paginated results

        Examples:
            # Iterate over dict resources
            for patient in client.search_resource_pages("Patient", {"family": "Smith"}):
                print(patient['name'])

            # Type-safe iteration with Pydantic models
            from pymedplum.fhir import Patient
            for patient in client.search_resource_pages("Patient", {"family": "Smith"}, as_fhir=Patient):
                print(patient.name[0].given)  # Full type safety and IDE autocomplete!
        """
        if as_fhir:
            validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)

        bundle = self.search_resources(resource_type, query, on_behalf_of=on_behalf_of)
        assert isinstance(bundle, dict)

        yielded = 0
        while bundle:
            for entry in bundle.get("entry", []):
                if "resource" in entry:
                    if max_resources is not None and yielded >= max_resources:
                        return
                    resource = entry["resource"]
                    if as_fhir:
                        yield as_fhir(**resource)
                    else:
                        yield resource
                    yielded += 1

            next_url = None
            for link in bundle.get("link", []):
                if link.get("relation") == "next":
                    next_url = link.get("url")
                    break

            if not next_url:
                break
            if max_resources is not None and yielded >= max_resources:
                return

            assert_same_origin(self.base_url, next_url)
            bundle = self._request("GET", next_url, on_behalf_of=on_behalf_of)

    @overload
    def search_with_options(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        *,
        summary: SummaryMode | None = None,
        elements: list[str] | None = None,
        total: TotalMode | None = None,
        at: str | None = None,
        count: int | None = None,
        offset: int | None = None,
        sort: str | list[str] | None = None,
        include: str | list[str] | None = None,
        include_iterate: str | list[str] | None = None,
        revinclude: str | list[str] | None = None,
        revinclude_iterate: str | list[str] | None = None,
        return_bundle: Literal[False] = False,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    @overload
    def search_with_options(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        *,
        summary: SummaryMode | None = None,
        elements: list[str] | None = None,
        total: TotalMode | None = None,
        at: str | None = None,
        count: int | None = None,
        offset: int | None = None,
        sort: str | list[str] | None = None,
        include: str | list[str] | None = None,
        include_iterate: str | list[str] | None = None,
        revinclude: str | list[str] | None = None,
        revinclude_iterate: str | list[str] | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: None = None,
    ) -> FHIRBundle[dict[str, Any]]:
        pass

    @overload
    def search_with_options(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        *,
        summary: SummaryMode | None = None,
        elements: list[str] | None = None,
        total: TotalMode | None = None,
        at: str | None = None,
        count: int | None = None,
        offset: int | None = None,
        sort: str | list[str] | None = None,
        include: str | list[str] | None = None,
        include_iterate: str | list[str] | None = None,
        revinclude: str | list[str] | None = None,
        revinclude_iterate: str | list[str] | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: type[ResourceT] = ...,
    ) -> FHIRBundle[ResourceT]:
        pass

    def search_with_options(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        *,
        summary: SummaryMode | None = None,
        elements: list[str] | None = None,
        total: TotalMode | None = None,
        at: str | None = None,
        count: int | None = None,
        offset: int | None = None,
        sort: str | list[str] | None = None,
        include: str | list[str] | None = None,
        include_iterate: str | list[str] | None = None,
        revinclude: str | list[str] | None = None,
        revinclude_iterate: str | list[str] | None = None,
        return_bundle: bool = False,
        as_fhir: type[ResourceT] | None = None,
        on_behalf_of: str | None = None,
    ) -> FHIRBundle[ResourceT] | FHIRBundle[dict[str, Any]] | dict[str, Any]:
        """Search for FHIR resources with explicit search parameter helpers.

        This method provides named parameters for common FHIR search modifiers,
        making it easier to construct complex queries without manually building
        query strings.

        Args:
            resource_type: FHIR resource type to search
            query: Base search parameters (dict, list of tuples, or query string)
            summary: Return summary of results (_summary parameter)
                - "true": Return only mandatory elements
                - "text": Return text, id, meta, and top-level mandatory elements
                - "data": Remove text element from returned resources
                - "count": Return only count (Bundle.total), no resources
                - "false": Return full resources (default)
            elements: Specific elements to return (_elements parameter)
            total: How to calculate Bundle.total (_total parameter)
                - "none": Don't include total
                - "estimate": Provide estimated count
                - "accurate": Provide exact count (may be slow)
            at: Point-in-time search - search historical versions (_at parameter)
                Format: "2024-01-15" or "2024-01-15T10:30:00Z"
            count: Maximum number of results per page (_count parameter)
            offset: Starting offset for pagination (_offset parameter)
            sort: Sort order (_sort parameter), e.g., "-date" or ["status", "-date"]
            include: Resources to include (_include parameter)
            include_iterate: Recursive includes (_include:iterate parameter) - follows
                references on included resources to include additional related resources
            revinclude: Reverse includes (_revinclude parameter)
            revinclude_iterate: Recursive reverse includes (_revinclude:iterate parameter) -
                follows references on reverse-included resources
            return_bundle: If True, wrap result in FHIRBundle helper
            as_fhir: Optional FHIR resource class for typed responses
            on_behalf_of: Optional ProjectMembership ID to act on behalf
                of for this request (overrides any context-bound value)

        Returns:
            FHIRBundle wrapper or raw dict based on return_bundle parameter

        Examples:
            # Get count only (fast)
            result = client.search_with_options(
                "Observation",
                {"patient": "Patient/123"},
                summary="count"
            )
            print(f"Total observations: {result.get('total')}")

            # Get specific elements only
            result = client.search_with_options(
                "Patient",
                {"family": "Smith"},
                elements=["id", "name", "birthDate"],
                total="accurate"
            )

            # Point-in-time search (historical data)
            result = client.search_with_options(
                "Observation",
                {"patient": "Patient/123"},
                at="2024-01-15T00:00:00Z"
            )

            # Complex search with sorting and pagination
            bundle = client.search_with_options(
                "Observation",
                {"patient": "Patient/123", "code": "29463-7"},
                sort=["-date", "status"],
                count=50,
                offset=100,
                include=["Observation:subject"],
                return_bundle=True
            )
        """
        validate_resource_type(resource_type)
        params = self._build_query_params(query)
        _append_search_options(
            params,
            summary=summary,
            elements=elements,
            total=total,
            at=at,
            count=count,
            offset=offset,
            sort=sort,
            include=include,
            include_iterate=include_iterate,
            revinclude=revinclude,
            revinclude_iterate=revinclude_iterate,
        )

        response = self._request(
            "GET",
            f"{self.fhir_base_url}{resource_type}",
            params=params,
            on_behalf_of=on_behalf_of,
        )

        if return_bundle:
            bundle_obj: FHIRBundle[Any] = FHIRBundle(response)
            if as_fhir:
                validate_as_fhir_class(as_fhir, expected_resource_type=resource_type)
                bundle_obj._resource_class = as_fhir
            return bundle_obj

        return response

    def execute_graphql(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        *,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query."""
        return self._request(
            "POST",
            f"{self.fhir_base_url}$graphql",
            json={"query": query, "variables": variables or {}},
            on_behalf_of=on_behalf_of,
        )

    def execute_batch(
        self,
        bundle: dict[str, Any] | Any,
        *,
        accounts: str | list[str] | None = None,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        """Execute a FHIR batch/transaction bundle.

        Args:
            bundle: FHIR Bundle resource
            accounts: Account references to set on each bundle entry's
                meta.accounts (e.g., "Organization/abc" or a list)
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.
        """
        data = to_fhir_json(bundle)

        if accounts is not None:
            for entry in data.get("entry", []):
                if "resource" in entry and isinstance(entry["resource"], dict):
                    entry["resource"] = self._apply_accounts(
                        entry["resource"], accounts
                    )

        return self._request(
            "POST", self.fhir_base_url, json=data, on_behalf_of=on_behalf_of
        )

    def set_accounts(
        self,
        resource_ref: str,
        account_refs: str | list[str],
        *,
        propagate: bool = False,
        prefer_async: bool = False,
    ) -> dict[str, Any]:
        """Assign a resource to accounts via the $set-accounts operation.

        Medplum uses meta.accounts for compartment-based multi-tenant
        access control. This operation assigns one or more account
        references (typically Organizations or Practitioners) to a
        resource. When propagate is True, the assignments cascade to
        all resources in the target's FHIR compartment (e.g., a
        Patient's Observations, Encounters, etc.).

        Args:
            resource_ref: Reference like "Patient/123"
            account_refs: Account references to assign — single string
                or list (e.g., "Organization/abc" or
                ["Organization/abc", "Practitioner/xyz"])
            propagate: If True, cascade account assignments to related
                resources (Appointments, Observations, etc.)
            prefer_async: If True, send Prefer: respond-async header.
                Only takes effect when propagate is also True.
                Server returns an OperationOutcome with the async job
                URL in issue[0].diagnostics. Poll with client.get().

        Returns:
            Synchronous: FHIR Parameters with resourcesUpdated count.
            Async (202): OperationOutcome with job URL in
            issue[0].diagnostics.

        Examples:
            # Assign patient to an organization's account
            client.set_accounts("Patient/123", "Organization/org-a")

            # Multiple accounts with propagation
            client.set_accounts(
                "Patient/123",
                ["Organization/org-a", "Practitioner/prac-1"],
                propagate=True,
            )

            # Async for large compartments
            result = client.set_accounts(
                "Patient/123",
                "Organization/org-a",
                propagate=True,
                prefer_async=True,
            )
            # Wait for the async job to complete
            job = client.wait_for_async_job(result, timeout=60)
        """
        if "/" not in resource_ref:
            raise ValueError(f"Invalid resource reference: {resource_ref}")

        if prefer_async and not propagate:
            raise ValueError("prefer_async only takes effect with propagate=True")

        resource_type, resource_id = resource_ref.split("/", 1)

        if isinstance(account_refs, str):
            account_refs = [account_refs]

        parameter: list[dict[str, Any]] = [
            {
                "name": "accounts",
                "valueReference": {"reference": ref},
            }
            for ref in account_refs
        ]

        if propagate:
            parameter.append({"name": "propagate", "valueBoolean": True})

        params = {
            "resourceType": "Parameters",
            "parameter": parameter,
        }

        headers = None
        if prefer_async:
            headers = {"Prefer": "respond-async"}

        return self.execute_operation(
            resource_type,
            "set-accounts",
            resource_id=resource_id,
            params=params,
            headers=headers,
        )

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """GET from any Medplum endpoint (not just FHIR).

        Args:
            path: Endpoint path (e.g., "admin/projects/123")
            **kwargs: Additional request parameters (e.g., params, headers)

        Returns:
            Response JSON
        """
        url = build_raw_request_url(self.base_url, path)
        kwargs.pop("raw", None)
        result = self._request("GET", url, **kwargs)
        assert isinstance(result, dict)
        return result

    def post(self, path: str, data: Any) -> dict[str, Any]:
        """POST to any Medplum endpoint (not just FHIR).

        Args:
            path: Endpoint path (e.g., "admin/projects/123/invite")
            data: Request body

        Returns:
            Response JSON
        """
        url = build_raw_request_url(self.base_url, path)
        return self._request("POST", url, json=data)

    def invite_user(
        self,
        project_id: str,
        resource_type: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str | None = None,
        send_email: bool = True,
        admin: bool = False,
        scope: str = "project",
        access_policy: str | None = None,
    ) -> dict[str, Any]:
        """Invite a user to a project, creating User, profile, and ProjectMembership.

        This endpoint:
        1. Creates a User if one doesn't exist
        2. Creates a FHIR profile resource (Patient, Practitioner, RelatedPerson)
        3. Creates a ProjectMembership linking User, profile, and access policy
        4. Optionally sends an email invite

        Args:
            project_id: ID of the project to invite the user to
            resource_type: Profile type ("Patient", "Practitioner", or "RelatedPerson")
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            password: Optional password (for silent user creation without email)
            send_email: Whether to send invitation email (default: True)
            admin: Whether to grant admin privileges (default: False)
            scope: User scope - "project" or "server" (default: "project")
            access_policy: Optional AccessPolicy reference (e.g., "AccessPolicy/123")

        Returns:
            ProjectMembership resource

        Raises:
            OperationOutcomeError: On invitation failure

        Example:
            membership = client.invite_user(
                project_id="abc",
                resource_type="Practitioner",
                first_name="Alice",
                last_name="Smith",
                email="alice@example.com",
                password="securepass123",
                send_email=False,
                admin=True
            )
        """
        validate_resource_id(project_id, field="project_id")
        validate_resource_type(resource_type)
        payload: dict[str, Any] = {
            "resourceType": resource_type,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "sendEmail": send_email,
            "admin": admin,
            "scope": scope,
        }

        if password:
            payload["password"] = password

        if access_policy:
            if isinstance(access_policy, str):
                payload["accessPolicy"] = {"reference": access_policy}
            else:
                payload["accessPolicy"] = access_policy

        return self.post(f"admin/projects/{project_id}/invite", payload)

    def export_ccda(self, patient_id: str, *, on_behalf_of: str | None = None) -> str:
        """Export a patient's complete history as a C-CDA XML document.

        Args:
            patient_id: The ID of the patient to export
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            C-CDA XML document as a string

        Example:
            ccda_xml = client.export_ccda("patient-123")
            with open("patient-record.xml", "w") as f:
                f.write(ccda_xml)
        """
        validate_resource_id(patient_id, field="patient_id")
        response = self._request(
            "GET",
            f"{self.fhir_base_url}Patient/{patient_id}/$ccda-export",
            raw=True,
            on_behalf_of=on_behalf_of,
        )
        return response.text

    def validate_valueset_code(
        self,
        valueset_url: str | None = None,
        valueset_id: str | None = None,
        code: str | None = None,
        system: str | None = None,
        coding: dict[str, Any] | None = None,
        codeable_concept: dict[str, Any] | None = None,
        display: str | None = None,
        abstract: bool | None = None,
    ) -> dict[str, Any]:
        """Validate if a code is in a ValueSet.

        Must provide either valueset_url or valueset_id, plus one of:
        - code + system (+ optional display)
        - coding
        - codeable_concept

        Args:
            valueset_url: Canonical URL of the ValueSet
            valueset_id: ID of a specific ValueSet resource
            code: Code to validate
            system: Code system URL
            coding: Full Coding object to validate
            codeable_concept: CodeableConcept to validate
            display: Display text to validate
            abstract: Include abstract codes

        Returns:
            Parameters resource with 'result' (bool) and optional 'display' (str)

        Example:
            result = client.validate_valueset_code(
                valueset_url="http://hl7.org/fhir/ValueSet/condition-severity",
                coding={"system": "http://snomed.info/sct", "code": "255604002"}
            )
            is_valid = result["parameter"][0]["valueBoolean"]  # True
        """
        # Build parameters using helper
        params_resource = build_valueset_validate_params(
            valueset_url=valueset_url,
            valueset_id=valueset_id,
            code=code,
            system=system,
            coding=coding,
            codeable_concept=codeable_concept,
            display=display,
            abstract=abstract,
        )

        return self.execute_operation(
            "ValueSet",
            "validate-code",
            resource_id=valueset_id,
            params=params_resource,
        )

    def validate_codesystem_code(
        self,
        codesystem_url: str | None = None,
        codesystem_id: str | None = None,
        code: str | None = None,
        coding: dict[str, Any] | None = None,
        version: str | None = None,
    ) -> dict[str, Any]:
        """Validate if a code exists in a CodeSystem.

        Must provide either codesystem_url or codesystem_id, plus one of:
        - code
        - coding

        Args:
            codesystem_url: Canonical URL of the CodeSystem
            codesystem_id: ID of a specific CodeSystem resource
            code: Code to validate
            coding: Full Coding object to validate
            version: Specific version of the CodeSystem

        Returns:
            Parameters resource with 'result' (bool) and optional 'display' (str)

        Example:
            result = client.validate_codesystem_code(
                codesystem_url="http://snomed.info/sct",
                code="255604002"
            )
            is_valid = result["parameter"][0]["valueBoolean"]  # True
        """
        # Build parameters using helper
        params_resource = build_codesystem_validate_params(
            codesystem_url=codesystem_url,
            codesystem_id=codesystem_id,
            code=code,
            coding=coding,
            version=version,
        )

        return self.execute_operation(
            "CodeSystem",
            "validate-code",
            resource_id=codesystem_id,
            params=params_resource,
        )

    def expand_valueset(
        self,
        valueset_url: str | None = None,
        valueset_id: str | None = None,
        filter: str | None = None,
        offset: int | None = None,
        count: int | None = None,
        include_designations: bool | None = None,
        active_only: bool | None = None,
        exclude_nested: bool | None = None,
        exclude_not_for_ui: bool | None = None,
        exclude_post_coordinated: bool | None = None,
        display_language: str | None = None,
        property: list[str] | None = None,
    ) -> dict[str, Any]:
        """Expand a ValueSet into its list of codes.

        The $expand operation returns the full set of concepts that belong
        to the ValueSet. This is useful for populating UI dropdowns or
        validating codes against a value set.

        Must provide either valueset_url or valueset_id.

        Args:
            valueset_url: Canonical URL of the ValueSet to expand
            valueset_id: ID of a specific ValueSet resource
            filter: Text filter to apply (substring match on display)
            offset: Starting index for paging (0-based)
            count: Maximum number of concepts to return
            include_designations: Include code system designations
            active_only: Only include active codes
            exclude_nested: Exclude nested codes from expansion
            exclude_not_for_ui: Exclude codes marked as notSelectable
            exclude_post_coordinated: Exclude post-coordinated codes
            display_language: Language for display text (e.g., "en", "de")
            property: List of properties to include for each concept

        Returns:
            Expanded ValueSet resource with expansion.contains listing codes

        Example:
            # Expand a standard value set
            result = client.expand_valueset(
                valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender"
            )
            for concept in result.get("expansion", {}).get("contains", []):
                print(f"{concept['code']}: {concept['display']}")

            # Expand with filtering
            result = client.expand_valueset(
                valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
                filter="diabetes",
                count=10
            )
        """
        params_resource = build_valueset_expand_params(
            valueset_url=valueset_url,
            valueset_id=valueset_id,
            filter=filter,
            offset=offset,
            count=count,
            include_designations=include_designations,
            active_only=active_only,
            exclude_nested=exclude_nested,
            exclude_not_for_ui=exclude_not_for_ui,
            exclude_post_coordinated=exclude_post_coordinated,
            display_language=display_language,
            property=property,
        )

        return self.execute_operation(
            "ValueSet",
            "expand",
            resource_id=valueset_id,
            params=params_resource,
        )

    def lookup_concept(
        self,
        code: str,
        system: str | None = None,
        codesystem_id: str | None = None,
        version: str | None = None,
        coding: dict[str, Any] | None = None,
        date: str | None = None,
        display_language: str | None = None,
        property: list[str] | None = None,
    ) -> dict[str, Any]:
        """Look up details about a code in a CodeSystem.

        The $lookup operation returns detailed information about a code,
        including its display name, definition, and properties.

        Args:
            code: Code to look up
            system: Code system URL (required if not using instance-level operation)
            codesystem_id: ID of a specific CodeSystem resource
            version: Specific version of the code system
            coding: Full Coding object (alternative to code+system)
            date: Date for which the code should be valid
            display_language: Language for display text (e.g., "en", "de")
            property: List of properties to return for the code

        Returns:
            Parameters resource with code details (display, definition, properties)

        Example:
            # Look up a SNOMED CT code
            result = client.lookup_concept(
                code="73211009",
                system="http://snomed.info/sct"
            )
            # Extract display name
            for param in result.get("parameter", []):
                if param.get("name") == "display":
                    print(f"Display: {param.get('valueString')}")

            # Look up with specific properties
            result = client.lookup_concept(
                code="73211009",
                system="http://snomed.info/sct",
                property=["inactive", "parent"]
            )
        """
        params_resource = build_codesystem_lookup_params(
            code=code,
            system=system,
            codesystem_id=codesystem_id,
            version=version,
            coding=coding,
            date=date,
            display_language=display_language,
            property=property,
        )

        return self.execute_operation(
            "CodeSystem",
            "lookup",
            resource_id=codesystem_id,
            params=params_resource,
        )

    def translate_concept(
        self,
        code: str | None = None,
        system: str | None = None,
        conceptmap_url: str | None = None,
        conceptmap_id: str | None = None,
        version: str | None = None,
        source: str | None = None,
        target: str | None = None,
        coding: dict[str, Any] | None = None,
        codeable_concept: dict[str, Any] | None = None,
        target_system: str | None = None,
        reverse: bool | None = None,
    ) -> dict[str, Any]:
        """Translate a code from one code system to another.

        The $translate operation uses ConceptMap resources to map codes
        between different code systems (e.g., SNOMED CT to ICD-10).

        Args:
            code: Code to translate
            system: Code system URL of the source code
            conceptmap_url: Canonical URL of the ConceptMap to use
            conceptmap_id: ID of a specific ConceptMap resource
            version: Version of the ConceptMap
            source: Source value set URL (filter for applicable mappings)
            target: Target value set URL (filter for applicable mappings)
            coding: Full Coding object (alternative to code+system)
            codeable_concept: CodeableConcept to translate
            target_system: Target code system URL
            reverse: Reverse the direction of the mapping

        Returns:
            Parameters resource with translation results including matches

        Example:
            # Translate using a specific ConceptMap
            result = client.translate_concept(
                code="73211009",
                system="http://snomed.info/sct",
                target_system="http://hl7.org/fhir/sid/icd-10"
            )

            # Check if translation was successful
            for param in result.get("parameter", []):
                if param.get("name") == "result":
                    if param.get("valueBoolean"):
                        print("Translation found!")
                elif param.get("name") == "match":
                    # Extract matched concepts
                    for part in param.get("part", []):
                        if part.get("name") == "concept":
                            coding = part.get("valueCoding", {})
                            print(f"Match: {coding.get('code')} - {coding.get('display')}")
        """
        params_resource = build_conceptmap_translate_params(
            code=code,
            system=system,
            conceptmap_url=conceptmap_url,
            conceptmap_id=conceptmap_id,
            version=version,
            source=source,
            target=target,
            coding=coding,
            codeable_concept=codeable_concept,
            target_system=target_system,
            reverse=reverse,
        )

        return self.execute_operation(
            "ConceptMap",
            "translate",
            resource_id=conceptmap_id,
            params=params_resource,
        )

    def clone_resource(
        self,
        resource_type: str,
        resource_id: str,
    ) -> dict[str, Any]:
        """Clone a resource using the Medplum $clone operation.

        Creates a deep copy of a resource with a new ID. The cloned resource
        will have all the same data as the original, but with a new identity.

        Args:
            resource_type: FHIR resource type (e.g., "Patient", "Questionnaire")
            resource_id: ID of the resource to clone

        Returns:
            The cloned resource with a new ID

        Example:
            # Clone a Questionnaire for modification
            original = client.read_resource("Questionnaire", "template-123")
            cloned = client.clone_resource("Questionnaire", "template-123")
            print(f"Cloned questionnaire ID: {cloned['id']}")

            # Clone a Patient resource
            cloned_patient = client.clone_resource("Patient", "patient-456")
        """
        return self.execute_operation(
            resource_type,
            "clone",
            resource_id=resource_id,
        )

    def expunge_resource(
        self,
        resource_type: str,
        resource_id: str,
        everything: bool = False,
    ) -> None:
        """Permanently delete a resource using the Medplum $expunge operation.

        Unlike regular delete (which is a soft delete), $expunge permanently removes
        the resource and all its history from the database. This operation cannot
        be undone.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: ID of the resource to expunge
            everything: If True, also expunge all resources in the resource's
                compartment (only valid for Patient resources)

        Warning:
            This operation permanently deletes data and cannot be undone.
            Use with extreme caution.

        Example:
            # Permanently delete a single resource
            client.expunge_resource("Observation", "obs-123")

            # Permanently delete a patient and all related resources
            client.expunge_resource("Patient", "patient-456", everything=True)
        """
        validate_resource_type(resource_type)
        validate_resource_id(resource_id)
        url = f"{self.fhir_base_url}{resource_type}/{resource_id}/$expunge"
        if everything:
            url += "?everything=true"

        self._request("POST", url)

    def get_async_job_status(
        self,
        job: str | dict[str, Any] | OperationOutcome,
    ) -> dict[str, Any]:
        """Get the status of an async job.

        Accepts a job ID, a job status URL, or an OperationOutcome
        returned from an async operation (e.g., set_accounts with
        prefer_async=True).

        Args:
            job: Job ID, full status URL, or OperationOutcome dict
                with the job URL in issue[0].diagnostics

        Returns:
            AsyncJob resource with current status

        Example:
            result = client.set_accounts(
                "Patient/123", "Organization/org-a",
                propagate=True, prefer_async=True,
            )
            job = client.get_async_job_status(result)
        """
        url = self._resolve_async_job_url(job)
        return self._request("GET", url)

    def wait_for_async_job(
        self,
        job: str | dict[str, Any] | OperationOutcome,
        poll_interval: float = 1.0,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Wait for an async job to complete, polling at intervals.

        Accepts the same inputs as get_async_job_status.

        Args:
            job: Job ID, full status URL, or OperationOutcome dict
            poll_interval: Seconds between status checks (default: 1.0)
            timeout: Maximum seconds to wait (None = indefinite)

        Returns:
            AsyncJob resource with final status

        Raises:
            TimeoutError: If timeout is reached before job completes

        Example:
            result = client.set_accounts(
                "Patient/123", "Organization/org-a",
                propagate=True, prefer_async=True,
            )
            job = client.wait_for_async_job(result, timeout=60)
            if job["status"] == "completed":
                print(job["output"])
        """
        url = self._resolve_async_job_url(job)
        start_time = time.time()
        terminal_statuses = {"completed", "error", "stopped", "cancelled"}

        while True:
            status_response = self._request("GET", url)
            status = status_response.get("status", "")

            if status in terminal_statuses:
                return status_response

            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    raise TimeoutError(
                        f"Async job did not complete within {timeout} seconds"
                    )

            time.sleep(poll_interval)

    def execute_transaction(
        self,
        bundle: dict[str, Any] | Any,
        *,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        """Execute a transaction bundle atomically.

        All operations in a transaction bundle succeed or fail together.
        Use placeholder IDs (urn:uuid:xxx) to reference resources within the bundle.

        Args:
            bundle: Bundle resource with type="transaction" or dict with entries
            on_behalf_of: Optional ProjectMembership ID to act on behalf
                of for this request (overrides any context-bound value)

        Returns:
            Bundle with type="transaction-response" containing results

        Example:
            from pymedplum.fhir.bundle import Bundle

            bundle = {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": [
                    {
                        "fullUrl": "urn:uuid:patient-temp",
                        "resource": {
                            "resourceType": "Patient",
                            "name": [{"family": "Smith", "given": ["John"]}]
                        },
                        "request": {"method": "POST", "url": "Patient"}
                    },
                    {
                        "resource": {
                            "resourceType": "Observation",
                            "status": "final",
                            "subject": {"reference": "urn:uuid:patient-temp"},
                            "code": {"text": "Heart Rate"}
                        },
                        "request": {"method": "POST", "url": "Observation"}
                    }
                ]
            }
            result = client.execute_transaction(bundle)
        """
        bundle_data = to_fhir_json(bundle)

        # Ensure it's a transaction bundle
        if bundle_data.get("type") != "transaction":
            bundle_data["type"] = "transaction"

        # POST to base URL (not /fhir/R4/Bundle, just /fhir/R4/)
        return self._request(
            "POST",
            self.fhir_base_url.rstrip("/"),
            json=bundle_data,
            on_behalf_of=on_behalf_of,
        )

    def upload_binary(
        self,
        content: bytes,
        content_type: str,
        *,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        """Upload binary content (like documents, images, PDFs).

        Args:
            content: Binary content as bytes
            content_type: MIME type (e.g., "application/pdf", "application/xml")
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            Binary resource

        Example:
            with open("document.pdf", "rb") as f:
                binary = client.upload_binary(f.read(), "application/pdf")
            binary_id = binary["id"]
        """
        return self._request(
            "POST",
            f"{self.fhir_base_url}Binary",
            data=content,
            headers={"Content-Type": content_type},
            on_behalf_of=on_behalf_of,
        )

    def download_binary(
        self,
        binary_id: str,
        *,
        on_behalf_of: str | None = None,
        max_bytes: int | None = None,
    ) -> bytes:
        """Download binary content.

        Args:
            binary_id: ID of the Binary resource
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.
            max_bytes: Optional cap on the response size. The check
                consults ``Content-Length`` first (cheap reject before
                materialization) and validates the actual byte count
                after read. Without a cap a hostile or misbehaving server
                can OOM the SDK process by serving an unbounded blob;
                set this when the expected payload size is known.

        Returns:
            Binary content as bytes

        Raises:
            ValueError: If ``max_bytes`` is set and the response advertises
                or returns more bytes than allowed.

        Example:
            content = client.download_binary("binary-123", max_bytes=10 * 1024 * 1024)
            with open("downloaded.pdf", "wb") as f:
                f.write(content)

        Note:
            This implementation uses the FHIR-compliant Accept: */* header to retrieve
            raw binary content directly. Per FHIR spec (https://hl7.org/fhir/binary.html#rest),
            when Accept: */* or Accept matches the contentType, the server returns raw bytes.
            When Accept: application/fhir+json, it returns the FHIR resource with base64 data.
        """
        validate_resource_id(binary_id, field="binary_id")
        response = self._request(
            "GET",
            f"{self.fhir_base_url}Binary/{binary_id}",
            headers={"Accept": "*/*", "Content-Type": None},
            raw=True,
            on_behalf_of=on_behalf_of,
        )
        if max_bytes is not None:
            advertised_int: int | None = None
            advertised = response.headers.get("Content-Length")
            if advertised is not None:
                try:
                    advertised_int = int(advertised)
                except ValueError:
                    advertised_int = None
            if advertised_int is not None and advertised_int > max_bytes:
                raise ValueError(
                    f"Binary {binary_id!r} advertises {advertised_int} "
                    f"bytes, exceeding max_bytes={max_bytes}"
                )
            content = response.content
            if len(content) > max_bytes:
                raise ValueError(
                    f"Binary {binary_id!r} returned {len(content)} bytes, "
                    f"exceeding max_bytes={max_bytes}"
                )
            return content
        return response.content

    def create_document_reference(
        self,
        patient_id: str,
        binary_id: str,
        content_type: str,
        title: str,
        description: str | None = None,
        doc_type_code: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a DocumentReference pointing to binary content.

        Args:
            patient_id: Patient ID
            binary_id: Binary resource ID
            content_type: MIME type
            title: Document title
            description: Optional description
            doc_type_code: Optional document type CodeableConcept

        Returns:
            DocumentReference resource

        Example:
            # Upload a C-CDA document
            with open("ccda.xml", "rb") as f:
                binary = client.upload_binary(f.read(), "application/xml")

            doc_ref = client.create_document_reference(
                patient_id="patient-123",
                binary_id=binary["id"],
                content_type="application/xml",
                title="Continuity of Care Document",
                doc_type_code={
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "34133-9",
                        "display": "Summary of Episode Note"
                    }]
                }
            )
        """
        doc_ref = {
            "resourceType": "DocumentReference",
            "status": "current",
            "subject": {"reference": f"Patient/{patient_id}"},
            "content": [
                {
                    "attachment": {
                        "contentType": content_type,
                        "url": f"Binary/{binary_id}",
                        "title": title,
                    }
                }
            ],
        }

        if description:
            doc_ref["description"] = description

        if doc_type_code:
            doc_ref["type"] = doc_type_code

        return self.create_resource(doc_ref)

    def execute_bot(
        self,
        bot_id: str,
        input_data: Any,
        content_type: str = "application/json",
    ) -> dict[str, Any]:
        """Execute a Medplum Bot by its ID.

        Args:
            bot_id: The ID of the Bot to execute
            input_data: The input data to pass to the bot
            content_type: The content type of the input data (default: "application/json")

        Returns:
            The result of the bot execution

        Example:
            result = client.execute_bot(
                bot_id="bot-id-here",
                input_data={"resourceType": "Parameters", "parameter": []}
            )
        """
        return self.execute_operation(
            resource_type="Bot",
            operation="execute",
            resource_id=bot_id,
            params=input_data,
            headers={"Content-Type": content_type},
        )

    def execute_operation(
        self,
        resource_type: str,
        operation: str,
        resource_id: str | None = None,
        params: dict[str, Any] | Any | None = None,
        *,
        headers: dict[str, str] | None = None,
        method: Literal["GET", "POST"] = "POST",
        wrap_params: bool = False,
        on_behalf_of: str | None = None,
    ) -> dict[str, Any]:
        """Execute a FHIR operation (standard or custom).

        Supports both type-level operations (e.g., Patient/$match) and
        instance-level operations (e.g., Patient/123/$everything).

        Args:
            resource_type: FHIR resource type (e.g., "Patient", "MedicationRequest")
            operation: Operation name without $ prefix (e.g., "match", "calculate-dose")
            resource_id: Optional resource ID for instance-level operations
            params: Optional Parameters resource or dict to send as request body/query
            headers: Optional additional HTTP headers for the request
            method: HTTP method - "GET" for query params, "POST" for body (default)
            wrap_params: If True and params is a simple dict (not Parameters),
                auto-wrap it into a Parameters resource for POST requests
            on_behalf_of: Per-call OBO override. ``None`` uses the
                ambient client OBO; empty string clears it for this call.

        Returns:
            Operation response (typically Parameters or resource-specific)

        Note:
            Many FHIR operations accept both GET (with query params) and POST (with
            Parameters body). Use method="GET" for simple lookups like $lookup,
            $expand, and $translate. Use method="POST" (default) when passing
            complex data or when the server requires a Parameters resource.

        Examples:
            # Type-level operation with Parameters: Patient/$match
            result = client.execute_operation(
                "Patient",
                "match",
                params={
                    "resourceType": "Parameters",
                    "parameter": [
                        {"name": "resource", "resource": {"resourceType": "Patient", ...}}
                    ]
                }
            )

            # Instance-level operation: Patient/123/$everything
            bundle = client.execute_operation("Patient", "everything", resource_id="123")

            # GET operation with query params (simpler for lookups)
            result = client.execute_operation(
                "CodeSystem",
                "lookup",
                params={"code": "12345", "system": "http://loinc.org"},
                method="GET"
            )

            # Auto-wrap simple dict into Parameters resource
            result = client.execute_operation(
                "MedicationRequest",
                "calculate-dose",
                resource_id="med-req-456",
                params={"weight": 70, "unit": "kg"},
                wrap_params=True  # Converts to Parameters resource
            )
        """
        # Build the URL
        validate_resource_type(resource_type)
        operation_name = validate_operation_name(operation)
        if resource_id:
            validate_resource_id(resource_id)
            url = f"{self.fhir_base_url}{resource_type}/{resource_id}/${operation_name}"
        else:
            url = f"{self.fhir_base_url}{resource_type}/${operation_name}"

        if method == "GET":
            # Convert params to query string
            if params:
                query_params = self._build_query_params(params)
                return self._request(
                    "GET",
                    url,
                    params=query_params,
                    headers=headers,
                    on_behalf_of=on_behalf_of,
                )
            return self._request("GET", url, headers=headers, on_behalf_of=on_behalf_of)
        else:
            # POST with body
            body = None
            if params is not None:
                body = to_fhir_json(params)
                # Auto-wrap if requested and not already a Parameters resource
                if (
                    wrap_params
                    and isinstance(body, dict)
                    and not is_parameters_resource(body)
                ):
                    body = dict_to_parameters(body)

            return self._request(
                "POST",
                url,
                json=body,
                headers=headers,
                on_behalf_of=on_behalf_of,
            )

    def deploy_bot(
        self,
        bot_id: str,
        code: str,
        filename: str = "index.js",
    ) -> dict[str, Any]:
        """Deploy bot code to AWS Lambda using the $deploy operation.

        This operation deploys the bot's compiled JavaScript code as an AWS Lambda function
        within the Medplum infrastructure. The bot code will be executed when the bot is
        triggered.

        Args:
            bot_id: The ID of the Bot resource to deploy
            code: The compiled JavaScript code to deploy
            filename: The filename for the bot code (default: "index.js")

        Returns:
            The response from the $deploy operation

        Example:
            # Read your compiled bot code
            with open("dist/my-bot.js") as f:
                bot_code = f.read()

            # Deploy the bot
            result = client.deploy_bot("bot-id-here", bot_code)
        """
        return self.execute_operation(
            "Bot",
            "deploy",
            resource_id=bot_id,
            params={"code": code, "filename": filename},
        )

    def save_bot_code(
        self,
        bot_id: str,
        source_code: str,
    ) -> dict[str, Any]:
        """Save source code to a Bot resource's code property.

        This updates the Bot resource to store the source code (typically TypeScript)
        in the `code` property. This is useful for version control and auditing purposes.

        Args:
            bot_id: The ID of the Bot resource
            source_code: The source code to save (typically TypeScript)

        Returns:
            The updated Bot resource

        Example:
            # Read your bot source code
            with open("src/my-bot.ts") as f:
                source_code = f.read()

            # Save the source code to the Bot resource
            bot = client.save_bot_code("bot-id-here", source_code)
        """
        # Read the current bot resource
        bot = self.read_resource("Bot", bot_id)

        # Update the code property
        bot["code"] = source_code

        # Update the resource
        return self.update_resource(bot)

    def save_and_deploy_bot(
        self,
        bot_id: str,
        source_code: str,
        compiled_code: str,
        filename: str = "index.js",
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Save source code and deploy compiled code in one operation.

        This convenience function combines save_bot_code and deploy_bot to both
        save the source code to the Bot resource and deploy the compiled code
        as an AWS Lambda function.

        Args:
            bot_id: The ID of the Bot resource
            source_code: The source code to save (typically TypeScript)
            compiled_code: The compiled JavaScript code to deploy
            filename: The filename for the bot code (default: "index.js")

        Returns:
            A tuple of (updated Bot resource, deploy response)

        Example:
            # Read source and compiled code
            with open("src/my-bot.ts") as f:
                source = f.read()
            with open("dist/my-bot.js") as f:
                compiled = f.read()

            # Save and deploy
            bot, deploy_result = client.save_and_deploy_bot(
                "bot-id-here", source, compiled
            )
        """
        # Save the source code
        bot = self.save_bot_code(bot_id, source_code)

        # Deploy the compiled code
        deploy_result = self.deploy_bot(bot_id, compiled_code, filename)

        return bot, deploy_result

    def create_bot(
        self,
        name: str,
        description: str = "",
        source_code: str = "",
        runtime_version: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new Bot resource.

        Important: For bots to execute on AWS Lambda, you must specify runtime_version="awslambda".
        Without a runtime version, the bot cannot be executed.

        Args:
            name: The name of the bot
            description: Optional description of the bot
            source_code: Optional initial source code
            runtime_version: Runtime environment - either "awslambda" or "vmcontext" (required for execution)
            **kwargs: Additional Bot resource properties. Common properties include:
                - timeout: Maximum execution time in seconds
                - system: Boolean flag for system bot access

        Returns:
            The created Bot resource

        Example:
            # Create a bot with AWS Lambda runtime (required for execution)
            bot = client.create_bot(
                name="My Bot",
                description="Processes patient data",
                runtime_version="awslambda"  # Required for bot execution!
            )
        """
        bot_data: dict[str, Any] = {
            "resourceType": "Bot",
            "name": name,
            "description": description,
        }
        if source_code:
            bot_data["code"] = source_code
        if runtime_version:
            bot_data["runtimeVersion"] = runtime_version
        bot_data.update(kwargs)

        return self.create_resource(bot_data)

    def read_bot(self, bot_id: str) -> dict[str, Any]:
        """Read a Bot resource by ID.

        Args:
            bot_id: The ID of the Bot resource

        Returns:
            The Bot resource

        Example:
            bot = client.read_bot("bot-id-here")
            print(bot["name"])
        """
        return self.read_resource("Bot", bot_id)

    def update_bot(self, bot: dict[str, Any]) -> dict[str, Any]:
        """Update a Bot resource.

        Args:
            bot: The Bot resource with updates

        Returns:
            The updated Bot resource

        Example:
            bot = client.read_bot("bot-id-here")
            bot["description"] = "Updated description"
            updated = client.update_bot(bot)
        """
        return self.update_resource(bot)

    def delete_bot(self, bot_id: str) -> None:
        """Delete a Bot resource.

        Args:
            bot_id: The ID of the Bot resource to delete

        Example:
            client.delete_bot("bot-id-here")
        """
        self.delete_resource("Bot", bot_id)

    def list_bots(self, **search_params: Any) -> dict[str, Any]:
        """List Bot resources with optional search parameters.

        Args:
            **search_params: Optional FHIR search parameters

        Returns:
            A Bundle of Bot resources

        Example:
            # List all bots
            bots = client.list_bots()

            # Search by name
            bots = client.list_bots(name="my-bot")
        """
        return self.search_resources("Bot", search_params)
