import asyncio
import random
from collections.abc import AsyncIterator
from typing import Any, Literal, TypeVar, overload
from urllib.parse import urlparse

import httpx

from ._base import AsyncOnBehalfOfContext, BaseClient, _raise_or_json
from ._fhir_ops import (
    build_codesystem_lookup_params,
    build_codesystem_validate_params,
    build_conceptmap_translate_params,
    build_valueset_expand_params,
    build_valueset_validate_params,
    dict_to_parameters,
    is_parameters_resource,
)
from .bundle import FHIRBundle
from .exceptions import MedplumError
from .fhir.base import MedplumFHIRBase
from .helpers import decode_jwt_exp, to_fhir_json
from .types import OrgMode, PatchOperation, QueryTypes, SummaryMode, TotalMode

ResourceT = TypeVar("ResourceT", bound=MedplumFHIRBase)


class AsyncMedplumClient(BaseClient):
    """Asynchronous Medplum client with retry logic and production features"""

    def __init__(self, http_client: httpx.AsyncClient | None = None, **kwargs):
        super().__init__(**kwargs)

        if http_client:
            self._http = http_client
        else:
            self._http = httpx.AsyncClient(timeout=30.0)
        self._owns_http_client = http_client is None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()

    async def close(self):
        """Close HTTP client if we own it"""
        if self._owns_http_client:
            await self._http.aclose()

    async def authenticate(self) -> str:
        """Authenticate using client credentials flow.

        Returns:
            Access token string
        """
        if not (self.client_id and self.client_secret):
            raise ValueError("client_id and client_secret required for authentication")

        response = await self._http.post(
            f"{self.base_url}oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=30.0,
        )

        data = _raise_or_json(response)
        self.access_token = data["access_token"]
        self.token_expires_at = decode_jwt_exp(self.access_token)

        return self.access_token

    async def _request(self, method: str, url: str, **kwargs) -> dict[str, Any] | None:
        """Make async HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional httpx request options

        Returns:
            Parsed JSON response or None
        """
        if self._should_refresh_token():
            await self.authenticate()

        headers = self._get_headers()
        headers.update(kwargs.pop("headers", {}) or {})

        if self.before_request:
            self.before_request(method, url, headers, kwargs)

        for attempt in range(6):
            response = await self._http.request(method, url, headers=headers, **kwargs)

            max_retries = 5 if response.status_code == 429 else 2
            if response.status_code in (429, 502, 503, 504) and attempt < max_retries:
                delay = 0.25

                if response.status_code == 429:
                    try:
                        data = response.json()
                        if data.get("resourceType") == "OperationOutcome":
                            for issue in data.get("issue", []):
                                diagnostics = issue.get("diagnostics", "")
                                if diagnostics:
                                    import json

                                    diag_data = json.loads(diagnostics)
                                    ms_before_next = diag_data.get("_msBeforeNext", 0)
                                    if ms_before_next:
                                        delay = (ms_before_next / 1000.0) + 0.1
                                        break
                    except (ValueError, KeyError, json.JSONDecodeError):
                        pass

                if delay == 0.25:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        delay = min(int(retry_after), 30)
                    else:
                        delay = min(0.25 * (2**attempt), 2.0) + random.random() * 0.2

                await asyncio.sleep(delay)
                continue

            return _raise_or_json(response)

        raise MedplumError("Request failed after retries")

    def on_behalf_of(self, membership: str | Any) -> AsyncOnBehalfOfContext:
        """Create async context manager for on-behalf-of operations"""
        return AsyncOnBehalfOfContext(self, membership)

    @overload
    async def create_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT],
    ) -> ResourceT:
        pass

    @overload
    async def create_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    async def create_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT] | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Create a FHIR resource.

        Args:
            resource: FHIR resource dict or Pydantic model
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request
            headers: Optional HTTP headers to include in the request
            as_fhir: Optional FHIR resource class for typed response

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Create and get as dict
            patient_dict = await client.create_resource({
                "resourceType": "Patient",
                "name": [{"given": ["Alice"], "family": "Smith"}]
            })

            # Type-safe creation with Pydantic models
            from pymedplum.fhir import Patient
            patient = await client.create_resource(
                {"resourceType": "Patient", "name": [{"given": ["Alice"], "family": "Smith"}]},
                as_fhir=Patient
            )
            print(patient.name[0].given)  # Full IDE autocomplete!
        """
        data = to_fhir_json(resource)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")

        response = await self._request(
            "POST", f"{self.fhir_base_url}{resource_type}", json=data, headers=headers
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    @overload
    async def create_resource_if_none_exist(
        self,
        resource: dict[str, Any] | Any,
        if_none_exist: str,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT],
    ) -> ResourceT:
        pass

    @overload
    async def create_resource_if_none_exist(
        self,
        resource: dict[str, Any] | Any,
        if_none_exist: str,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    async def create_resource_if_none_exist(
        self,
        resource: dict[str, Any] | Any,
        if_none_exist: str,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT] | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Conditionally create a resource only if no matching resource exists.

        Uses the FHIR conditional create pattern with the If-None-Exist header.
        This enables idempotent resource creation - calling multiple times with
        the same search criteria returns the same resource without duplicates.

        Args:
            resource: FHIR resource dict or Pydantic model to create
            if_none_exist: Search query string for matching existing resources
                (e.g., "identifier=http://example.org|12345")
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request
            headers: Optional HTTP headers to include in the request
            as_fhir: Optional FHIR resource class for typed response

        Returns:
            Created or existing resource (as dict or typed model if as_fhir provided)

        Note:
            - Returns HTTP 201 Created with new resource if no match found
            - Returns HTTP 200 OK with existing resource if exactly one match
            - Returns HTTP 412 Precondition Failed if multiple matches exist

        Examples:
            # Create patient only if identifier doesn't exist
            patient = await client.create_resource_if_none_exist(
                {"resourceType": "Patient", "identifier": [
                    {"system": "http://example.org/mrn", "value": "12345"}
                ]},
                if_none_exist="identifier=http://example.org/mrn|12345"
            )

            # Type-safe conditional creation
            from pymedplum.fhir import Patient
            patient = await client.create_resource_if_none_exist(
                {"resourceType": "Patient", "identifier": [...]},
                if_none_exist="identifier=http://example.org/mrn|12345",
                as_fhir=Patient
            )
        """
        data = to_fhir_json(resource)

        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")

        # Normalize query string: handle full URLs, ?-prefixed, or plain query strings
        if if_none_exist.startswith(("http://", "https://")):
            # Full URL - extract just the query portion
            parsed = urlparse(if_none_exist)
            normalized_query = parsed.query
        else:
            # Plain query string - just strip leading ? if present
            normalized_query = if_none_exist.lstrip("?")

        normalized_query = normalized_query.strip()
        if not normalized_query:
            raise ValueError("if_none_exist query string cannot be empty")

        request_headers = {"If-None-Exist": normalized_query}
        if headers:
            request_headers.update(headers)

        response = await self._request(
            "POST",
            f"{self.fhir_base_url}{resource_type}",
            json=data,
            headers=request_headers,
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    @overload
    async def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: type[ResourceT]
    ) -> ResourceT:
        pass

    @overload
    async def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: None = None
    ) -> dict[str, Any]:
        pass

    async def read_resource(
        self,
        resource_type: str,
        resource_id: str,
        as_fhir: type[ResourceT] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Read a FHIR resource by type and ID.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            as_fhir: Optional FHIR resource class for typed response
            headers: Optional HTTP headers to include in the request

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Get resource as dict
            patient_dict = await client.read_resource("Patient", "123")

            # Type-safe access with Pydantic models
            from pymedplum.fhir import Patient
            patient = await client.read_resource("Patient", "123", as_fhir=Patient)
            print(patient.name[0].given)  # Full IDE autocomplete and type checking!
        """
        response = await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}/{resource_id}", headers=headers
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    @overload
    async def vread_resource(
        self,
        resource_type: str,
        resource_id: str,
        version_id: str,
        as_fhir: type[ResourceT],
    ) -> ResourceT:
        pass

    @overload
    async def vread_resource(
        self,
        resource_type: str,
        resource_id: str,
        version_id: str,
        as_fhir: None = None,
    ) -> dict[str, Any]:  # type: ignore[overload-cannot-match]
        pass

    async def vread_resource(
        self,
        resource_type: str,
        resource_id: str,
        version_id: str,
        as_fhir: type[ResourceT] | None = None,
        headers: dict[str, str] | None = None,
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

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Get a specific version as dict
            patient_v1 = await client.vread_resource("Patient", "123", "1")

            # Type-safe versioned read
            from pymedplum.fhir import Patient
            patient_v1 = await client.vread_resource("Patient", "123", "1", as_fhir=Patient)

            # Compare versions
            current = await client.read_resource("Patient", "123")
            version_id = current["meta"]["versionId"]
            previous = await client.vread_resource("Patient", "123", str(int(version_id) - 1))
        """
        response = await self._request(
            "GET",
            f"{self.fhir_base_url}{resource_type}/{resource_id}/_history/{version_id}",
            headers=headers,
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    @overload
    async def update_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT],
    ) -> ResourceT:
        pass

    @overload
    async def update_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    async def update_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT] | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Update a FHIR resource (requires id).

        Args:
            resource: FHIR resource dict or Pydantic model
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request
            headers: Optional HTTP headers (e.g., If-Match for optimistic locking)
            as_fhir: Optional FHIR resource class for typed response

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Update and get as dict
            patient = await client.read_resource("Patient", "123")
            patient["active"] = True
            updated = await client.update_resource(patient)

            # Type-safe update with Pydantic models
            from pymedplum.fhir import Patient
            patient = await client.read_resource("Patient", "123", as_fhir=Patient)
            patient.active = True
            updated = await client.update_resource(patient, as_fhir=Patient)
            print(updated.name[0].given)  # Full IDE autocomplete!

            # With optimistic locking
            patient = await client.read_resource("Patient", "123")
            patient["active"] = True
            updated = await client.update_resource(
                patient,
                headers={"If-Match": f'W/"{patient["meta"]["versionId"]}"'},
                as_fhir=Patient
            )
        """
        data = to_fhir_json(resource)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        resource_id = data.get("id")

        if not resource_type or not resource_id:
            raise ValueError("Resource must have resourceType and id for update")

        response = await self._request(
            "PUT",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=data,
            headers=headers,
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    @overload
    async def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT],
    ) -> ResourceT:
        pass

    @overload
    async def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        headers: dict[str, str] | None = None,
        *,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    async def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        headers: dict[str, str] | None = None,
        *,
        as_fhir: type[ResourceT] | None = None,
    ) -> ResourceT | dict[str, Any]:
        """Apply JSON Patch operations to a resource.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            operations: List of JSON Patch operations
            headers: Optional HTTP headers (e.g., If-Match for optimistic locking)
            as_fhir: Optional FHIR resource class for typed response

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Patch and get as dict
            operations = [{"op": "replace", "path": "/active", "value": False}]
            patched = await client.patch_resource("Patient", "123", operations)

            # Type-safe patching with Pydantic models
            from pymedplum.fhir import Patient
            operations = [{"op": "replace", "path": "/active", "value": True}]
            patched = await client.patch_resource("Patient", "123", operations, as_fhir=Patient)
            print(patched.active)  # Full IDE autocomplete!
        """
        patch_headers = {"Content-Type": "application/json-patch+json"}
        if headers:
            patch_headers.update(headers)

        response = await self._request(
            "PATCH",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=operations,
            headers=patch_headers,
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    async def delete_resource(
        self,
        resource_type: str,
        resource_id: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Delete a FHIR resource.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            headers: Optional HTTP headers to include in the request
        """
        await self._request(
            "DELETE",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            headers=headers,
        )

    @overload
    async def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[False] = False,
        as_fhir: None = None,
    ) -> dict[str, Any]:
        pass

    @overload
    async def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: None = None,
    ) -> FHIRBundle[dict[str, Any]]:
        pass

    @overload
    async def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: type[ResourceT] = ...,
    ) -> FHIRBundle[ResourceT]:
        pass

    async def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: bool = False,
        as_fhir: type[ResourceT] | None = None,
    ) -> FHIRBundle[ResourceT] | FHIRBundle[dict[str, Any]] | dict[str, Any]:
        """Search for FHIR resources.

        Args:
            resource_type: FHIR resource type
            query: Search parameters
            return_bundle: If True, wrap in FHIRBundle helper
            as_fhir: Optional FHIR resource class for typed response (only applies when return_bundle=True)

        Returns:
            FHIRBundle wrapper, or raw dict

        Examples:
            # Get raw Bundle dict
            bundle_dict = await client.search_resources("Patient", {"family": "Smith"})

            # Use FHIRBundle wrapper for convenience methods
            bundle = await client.search_resources("Patient", {}, return_bundle=True)
            for patient in bundle:
                print(patient['name'])

            # Type-safe access with Pydantic models
            from pymedplum.fhir import Patient
            bundle = await client.search_resources("Patient", {}, return_bundle=True, as_fhir=Patient)
            patients = bundle.get_resources_typed(Patient)
        """
        params = self._build_query_params(query)
        response = await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )

        if return_bundle:
            bundle: FHIRBundle[Any] = FHIRBundle(response)
            if as_fhir:
                bundle._resource_class = as_fhir
            return bundle

        return response

    async def search_one(
        self, resource_type: str, query: QueryTypes | None = None
    ) -> dict[str, Any] | None:
        """Search for a single resource"""
        params = self._build_query_params(query)
        params.append(("_count", "1"))

        bundle: dict[str, Any] | None = await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )
        assert bundle is not None
        entries = bundle.get("entry", [])

        if entries and "resource" in entries[0]:
            return entries[0]["resource"]
        return None

    async def search_resource_pages(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        as_fhir: type[ResourceT] | None = None,
    ) -> AsyncIterator[ResourceT | dict[str, Any]]:
        """Search resources with automatic pagination.

        Args:
            resource_type: FHIR resource type
            query: Search parameters
            as_fhir: Optional FHIR resource class for typed response

        Yields:
            Individual resources from paginated results

        Examples:
            # Iterate over dict resources
            async for patient in client.search_resource_pages("Patient", {"family": "Smith"}):
                print(patient['name'])

            # Type-safe iteration with Pydantic models
            from pymedplum.fhir import Patient
            async for patient in client.search_resource_pages("Patient", {"family": "Smith"}, as_fhir=Patient):
                print(patient.name[0].given)  # Full type safety and IDE autocomplete!
        """
        bundle_response = await self.search_resources(resource_type, query)
        assert isinstance(bundle_response, dict)
        bundle: dict[str, Any] | None = bundle_response

        while bundle:
            for entry in bundle.get("entry", []):
                if "resource" in entry:
                    resource = entry["resource"]
                    if as_fhir:
                        yield as_fhir(**resource)
                    else:
                        yield resource

            next_url = None
            for link in bundle.get("link", []):
                if link.get("relation") == "next":
                    next_url = link.get("url")
                    break

            if not next_url:
                break

            bundle = await self._request("GET", next_url)

    @overload
    async def search_with_options(
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
    async def search_with_options(
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
    async def search_with_options(
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

    async def search_with_options(
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

        Returns:
            FHIRBundle wrapper or raw dict based on return_bundle parameter

        Examples:
            # Get count only (fast)
            result = await client.search_with_options(
                "Observation",
                {"patient": "Patient/123"},
                summary="count"
            )
            print(f"Total observations: {result.get('total')}")

            # Get specific elements only
            result = await client.search_with_options(
                "Patient",
                {"family": "Smith"},
                elements=["id", "name", "birthDate"],
                total="accurate"
            )

            # Point-in-time search (historical data)
            result = await client.search_with_options(
                "Observation",
                {"patient": "Patient/123"},
                at="2024-01-15T00:00:00Z"
            )

            # Complex search with sorting and pagination
            bundle = await client.search_with_options(
                "Observation",
                {"patient": "Patient/123", "code": "29463-7"},
                sort=["-date", "status"],
                count=50,
                offset=100,
                include=["Observation:subject"],
                return_bundle=True
            )
        """
        params = self._build_query_params(query)

        if summary:
            params.append(("_summary", summary))

        if elements:
            params.append(("_elements", ",".join(elements)))

        if total:
            params.append(("_total", total))

        if at:
            params.append(("_at", at))

        if count is not None:
            params.append(("_count", str(count)))

        if offset is not None:
            params.append(("_offset", str(offset)))

        if sort:
            if isinstance(sort, list):
                params.append(("_sort", ",".join(sort)))
            else:
                params.append(("_sort", sort))

        if include:
            if isinstance(include, list):
                for inc in include:
                    params.append(("_include", inc))
            else:
                params.append(("_include", include))

        if include_iterate:
            if isinstance(include_iterate, list):
                for inc in include_iterate:
                    params.append(("_include:iterate", inc))
            else:
                params.append(("_include:iterate", include_iterate))

        if revinclude:
            if isinstance(revinclude, list):
                for rev in revinclude:
                    params.append(("_revinclude", rev))
            else:
                params.append(("_revinclude", revinclude))

        if revinclude_iterate:
            if isinstance(revinclude_iterate, list):
                for rev in revinclude_iterate:
                    params.append(("_revinclude:iterate", rev))
            else:
                params.append(("_revinclude:iterate", revinclude_iterate))

        response = await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )

        if return_bundle:
            bundle_obj: FHIRBundle[Any] = FHIRBundle(response)
            if as_fhir:
                bundle_obj._resource_class = as_fhir
            return bundle_obj

        return response

    # Alias for TypeScript compatibility
    searchWithOptions = search_with_options

    async def execute_graphql(
        self, query: str, variables: dict | None = None
    ) -> dict[str, Any]:
        """Execute a GraphQL query"""
        return await self._request(
            "POST",
            f"{self.fhir_base_url}$graphql",
            json={"query": query, "variables": variables or {}},
        )

    async def execute_batch(
        self,
        bundle: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
    ) -> dict[str, Any]:
        """Execute a FHIR batch/transaction bundle"""
        data = to_fhir_json(bundle)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        return await self._request("POST", self.fhir_base_url, json=data)

    async def set_accounts(
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
                Recommended for large compartments to avoid timeouts.
                Server returns 202 with Content-Location for polling.

        Returns:
            FHIR Parameters with resourcesUpdated count, or the resource
            itself (response format depends on Medplum server version).

        Examples:
            # Assign patient to an organization's account
            await client.set_accounts("Patient/123", "Organization/org-a")

            # Multiple accounts with propagation
            await client.set_accounts(
                "Patient/123",
                ["Organization/org-a", "Practitioner/prac-1"],
                propagate=True,
            )
        """
        if "/" not in resource_ref:
            raise ValueError(f"Invalid resource reference: {resource_ref}")

        resource_type, resource_id = resource_ref.split("/", 1)

        # Normalize to list
        if isinstance(account_refs, str):
            account_refs = [account_refs]

        # Build FHIR Parameters resource
        parameter = [
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

        return await self.execute_operation(
            resource_type,
            "set-accounts",
            resource_id=resource_id,
            params=params,
            headers=headers,
        )

    async def get(self, path: str, **kwargs) -> dict[str, Any]:
        """GET from any Medplum endpoint (not just FHIR).

        Args:
            path: Endpoint path (e.g., "admin/projects/123")
            **kwargs: Additional request parameters (e.g., params, headers)

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{path}"
        return await self._request("GET", url, **kwargs)

    async def post(self, path: str, data: Any) -> dict[str, Any]:
        """POST to any Medplum endpoint (not just FHIR).

        Args:
            path: Endpoint path (e.g., "admin/projects/123/invite")
            data: Request body

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{path}"
        return await self._request("POST", url, json=data)

    async def invite_user(
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
            membership = await client.invite_user(
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

        return await self.post(f"admin/projects/{project_id}/invite", payload)

    async def export_ccda(self, patient_id: str) -> str:
        """Export a patient's complete history as a C-CDA XML document.

        Args:
            patient_id: The ID of the patient to export

        Returns:
            C-CDA XML document as a string

        Example:
            ccda_xml = await client.export_ccda("patient-123")
            with open("patient-record.xml", "w") as f:
                f.write(ccda_xml)
        """
        response = await self._http.get(
            f"{self.fhir_base_url}Patient/{patient_id}/$ccda-export",
            headers=self._get_headers(),
        )
        if response.status_code >= 400:
            from ._base import _raise_or_json

            _raise_or_json(response)
        return response.text

    async def validate_valueset_code(
        self,
        valueset_url: str | None = None,
        valueset_id: str | None = None,
        code: str | None = None,
        system: str | None = None,
        coding: dict | None = None,
        codeable_concept: dict | None = None,
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
            result = await client.validate_valueset_code(
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

        return await self.execute_operation(
            "ValueSet",
            "validate-code",
            resource_id=valueset_id,
            params=params_resource,
        )

    async def validate_codesystem_code(
        self,
        codesystem_url: str | None = None,
        codesystem_id: str | None = None,
        code: str | None = None,
        coding: dict | None = None,
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
            result = await client.validate_codesystem_code(
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

        return await self.execute_operation(
            "CodeSystem",
            "validate-code",
            resource_id=codesystem_id,
            params=params_resource,
        )

    async def expand_valueset(
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
            result = await client.expand_valueset(
                valueset_url="http://hl7.org/fhir/ValueSet/administrative-gender"
            )
            for concept in result.get("expansion", {}).get("contains", []):
                print(f"{concept['code']}: {concept['display']}")

            # Expand with filtering
            result = await client.expand_valueset(
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

        return await self.execute_operation(
            "ValueSet",
            "expand",
            resource_id=valueset_id,
            params=params_resource,
        )

    async def lookup_concept(
        self,
        code: str,
        system: str | None = None,
        codesystem_id: str | None = None,
        version: str | None = None,
        coding: dict | None = None,
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
            result = await client.lookup_concept(
                code="73211009",
                system="http://snomed.info/sct"
            )
            # Extract display name
            for param in result.get("parameter", []):
                if param.get("name") == "display":
                    print(f"Display: {param.get('valueString')}")

            # Look up with specific properties
            result = await client.lookup_concept(
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

        return await self.execute_operation(
            "CodeSystem",
            "lookup",
            resource_id=codesystem_id,
            params=params_resource,
        )

    async def translate_concept(
        self,
        code: str | None = None,
        system: str | None = None,
        conceptmap_url: str | None = None,
        conceptmap_id: str | None = None,
        version: str | None = None,
        source: str | None = None,
        target: str | None = None,
        coding: dict | None = None,
        codeable_concept: dict | None = None,
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
            result = await client.translate_concept(
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

        return await self.execute_operation(
            "ConceptMap",
            "translate",
            resource_id=conceptmap_id,
            params=params_resource,
        )

    async def clone_resource(
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
            original = await client.read_resource("Questionnaire", "template-123")
            cloned = await client.clone_resource("Questionnaire", "template-123")
            print(f"Cloned questionnaire ID: {cloned['id']}")

            # Clone a Patient resource
            cloned_patient = await client.clone_resource("Patient", "patient-456")
        """
        return await self.execute_operation(
            resource_type,
            "clone",
            resource_id=resource_id,
        )

    async def expunge_resource(
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
            await client.expunge_resource("Observation", "obs-123")

            # Permanently delete a patient and all related resources
            await client.expunge_resource("Patient", "patient-456", everything=True)
        """
        url = f"{self.fhir_base_url}{resource_type}/{resource_id}/$expunge"
        if everything:
            url += "?everything=true"

        await self._request("POST", url)

    async def get_async_job_status(
        self,
        job_id: str,
    ) -> dict[str, Any]:
        """Get the status of an async job (BulkDataExport).

        Medplum uses the BulkDataExport resource to track the status of
        long-running operations like bulk exports. This method retrieves
        the current status of such a job.

        Args:
            job_id: The ID of the BulkDataExport resource

        Returns:
            BulkDataExport resource with current status

        Example:
            # Start a bulk export (returns immediately with job ID)
            # Then poll for status
            job = await client.get_async_job_status("export-job-123")

            if job.get("status") == "completed":
                # Get output files
                for output in job.get("output", []):
                    print(f"File: {output['url']}")
            elif job.get("status") == "error":
                print(f"Export failed: {job.get('error')}")
        """
        return await self.read_resource("BulkDataExport", job_id)

    async def wait_for_async_job(
        self,
        job_id: str,
        poll_interval: float = 1.0,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Wait for an async job to complete, polling at regular intervals.

        Polls the job status until it reaches a terminal state (completed, error)
        or until the timeout is reached.

        Args:
            job_id: The ID of the BulkDataExport resource
            poll_interval: Seconds between status checks (default: 1.0)
            timeout: Maximum seconds to wait (default: None = wait indefinitely)

        Returns:
            BulkDataExport resource with final status

        Raises:
            TimeoutError: If timeout is reached before job completes

        Example:
            # Wait for a bulk export to complete
            job = await client.wait_for_async_job("export-job-123", timeout=300)

            if job.get("status") == "completed":
                for output in job.get("output", []):
                    # Download output files
                    content = await client.get(output["url"].replace(client.base_url, ""))
        """
        import time

        start_time = time.time()
        terminal_statuses = {"completed", "error", "stopped"}

        while True:
            job = await self.get_async_job_status(job_id)
            status = job.get("status", "")

            if status in terminal_statuses:
                return job

            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    raise TimeoutError(
                        f"Async job {job_id} did not complete within {timeout} seconds"
                    )

            await asyncio.sleep(poll_interval)

    async def execute_transaction(self, bundle: dict | Any) -> dict[str, Any]:
        """Execute a transaction bundle atomically.

        All operations in a transaction bundle succeed or fail together.
        Use placeholder IDs (urn:uuid:xxx) to reference resources within the bundle.

        Args:
            bundle: Bundle resource with type="transaction" or dict with entries

        Returns:
            Bundle with type="transaction-response" containing results

        Example:
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
                    }
                ]
            }
            result = await client.execute_transaction(bundle)
        """
        from .helpers import to_fhir_json

        bundle_data = to_fhir_json(bundle) if hasattr(bundle, "model_dump") else bundle

        if bundle_data.get("type") != "transaction":
            bundle_data["type"] = "transaction"

        return await self._request(
            "POST", self.fhir_base_url.rstrip("/"), json=bundle_data
        )

    async def upload_binary(
        self,
        content: bytes,
        content_type: str,
    ) -> dict[str, Any]:
        """Upload binary content (like documents, images, PDFs).

        Args:
            content: Binary content as bytes
            content_type: MIME type (e.g., "application/pdf", "application/xml")

        Returns:
            Binary resource

        Example:
            with open("document.pdf", "rb") as f:
                binary = await client.upload_binary(f.read(), "application/pdf")
        """
        return await self._request(
            "POST",
            f"{self.fhir_base_url}Binary",
            data=content,
            headers={"Content-Type": content_type},
        )

    async def download_binary(self, binary_id: str) -> bytes:
        """Download binary content.

        Args:
            binary_id: ID of the Binary resource

        Returns:
            Binary content as bytes

        Example:
            content = await client.download_binary("binary-123")
            with open("downloaded.pdf", "wb") as f:
                f.write(content)

        Note:
            This implementation uses the FHIR-compliant Accept: */* header to retrieve
            raw binary content directly. Per FHIR spec (https://hl7.org/fhir/binary.html#rest),
            when Accept: */* or Accept matches the contentType, the server returns raw bytes.
            When Accept: application/fhir+json, it returns the FHIR resource with base64 data.
        """
        # Request raw binary content using Accept: */*
        # This is FHIR-compliant and more efficient than fetching the resource
        # and decoding base64 (Medplum correctly implements this per FHIR spec)
        # Use _get_headers() to ensure token refresh and on-behalf-of handling
        headers = self._get_headers()
        headers["Accept"] = "*/*"
        headers.pop("Content-Type", None)  # Not needed for GET
        response = await self._http.get(
            f"{self.fhir_base_url}Binary/{binary_id}",
            headers=headers,
        )
        if response.status_code >= 400:
            from ._base import _raise_or_json

            _raise_or_json(response)
        return response.content

    async def create_document_reference(
        self,
        patient_id: str,
        binary_id: str,
        content_type: str,
        title: str,
        description: str | None = None,
        doc_type_code: dict | None = None,
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
            with open("ccda.xml", "rb") as f:
                binary = await client.upload_binary(f.read(), "application/xml")

            doc_ref = await client.create_document_reference(
                patient_id="patient-123",
                binary_id=binary["id"],
                content_type="application/xml",
                title="Continuity of Care Document"
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

        return await self.create_resource(doc_ref)

    async def execute_bot(
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
            result = await client.execute_bot(
                bot_id="bot-id-here",
                input_data={"resourceType": "Parameters", "parameter": []}
            )
        """
        return await self.execute_operation(
            resource_type="Bot",
            operation="execute",
            resource_id=bot_id,
            params=input_data,
            headers={"Content-Type": content_type},
        )

    async def execute_operation(
        self,
        resource_type: str,
        operation: str,
        resource_id: str | None = None,
        params: dict[str, Any] | Any | None = None,
        headers: dict[str, str] | None = None,
        method: Literal["GET", "POST"] = "POST",
        wrap_params: bool = False,
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

        Returns:
            Operation response (typically Parameters or resource-specific)

        Note:
            Many FHIR operations accept both GET (with query params) and POST (with
            Parameters body). Use method="GET" for simple lookups like $lookup,
            $expand, and $translate. Use method="POST" (default) when passing
            complex data or when the server requires a Parameters resource.

        Examples:
            # Type-level operation with Parameters: Patient/$match
            result = await client.execute_operation(
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
            bundle = await client.execute_operation("Patient", "everything", resource_id="123")

            # GET operation with query params (simpler for lookups)
            result = await client.execute_operation(
                "CodeSystem",
                "lookup",
                params={"code": "12345", "system": "http://loinc.org"},
                method="GET"
            )

            # Auto-wrap simple dict into Parameters resource
            result = await client.execute_operation(
                "MedicationRequest",
                "calculate-dose",
                resource_id="med-req-456",
                params={"weight": 70, "unit": "kg"},
                wrap_params=True  # Converts to Parameters resource
            )
        """
        # Build the URL
        operation_name = operation.lstrip("$")  # Allow both "match" and "$match"
        if resource_id:
            url = f"{self.fhir_base_url}{resource_type}/{resource_id}/${operation_name}"
        else:
            url = f"{self.fhir_base_url}{resource_type}/${operation_name}"

        if method == "GET":
            # Convert params to query string
            if params:
                query_params = self._build_query_params(params)
                return await self._request(
                    "GET", url, params=query_params, headers=headers
                )
            return await self._request("GET", url, headers=headers)
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

            return await self._request("POST", url, json=body, headers=headers)

    async def deploy_bot(
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
            result = await client.deploy_bot("bot-id-here", bot_code)
        """
        return await self.execute_operation(
            "Bot",
            "deploy",
            resource_id=bot_id,
            params={"code": code, "filename": filename},
        )

    async def save_bot_code(
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
            bot = await client.save_bot_code("bot-id-here", source_code)
        """
        # Read the current bot resource
        bot = await self.read_resource("Bot", bot_id)

        # Update the code property
        bot["code"] = source_code

        # Update the resource
        return await self.update_resource(bot)

    async def save_and_deploy_bot(
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
            bot, deploy_result = await client.save_and_deploy_bot(
                "bot-id-here", source, compiled
            )
        """
        # Save the source code
        bot = await self.save_bot_code(bot_id, source_code)

        # Deploy the compiled code
        deploy_result = await self.deploy_bot(bot_id, compiled_code, filename)

        return bot, deploy_result

    async def create_bot(
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
            bot = await client.create_bot(
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

        return await self.create_resource(bot_data)

    async def read_bot(self, bot_id: str) -> dict[str, Any]:
        """Read a Bot resource by ID.

        Args:
            bot_id: The ID of the Bot resource

        Returns:
            The Bot resource

        Example:
            bot = await client.read_bot("bot-id-here")
            print(bot["name"])
        """
        return await self.read_resource("Bot", bot_id)

    async def update_bot(self, bot: dict[str, Any]) -> dict[str, Any]:
        """Update a Bot resource.

        Args:
            bot: The Bot resource with updates

        Returns:
            The updated Bot resource

        Example:
            bot = await client.read_bot("bot-id-here")
            bot["description"] = "Updated description"
            updated = await client.update_bot(bot)
        """
        return await self.update_resource(bot)

    async def delete_bot(self, bot_id: str) -> None:
        """Delete a Bot resource.

        Args:
            bot_id: The ID of the Bot resource to delete

        Example:
            await client.delete_bot("bot-id-here")
        """
        await self.delete_resource("Bot", bot_id)

    async def list_bots(self, **search_params: Any) -> dict[str, Any]:
        """List Bot resources with optional search parameters.

        Args:
            **search_params: Optional FHIR search parameters

        Returns:
            A Bundle of Bot resources

        Example:
            # List all bots
            bots = await client.list_bots()

            # Search by name
            bots = await client.list_bots(name="my-bot")
        """
        return await self.search_resources("Bot", search_params)

    # TypeScript-compatible aliases
    createResource = create_resource
    createResourceIfNoneExist = create_resource_if_none_exist
    readResource = read_resource
    vreadResource = vread_resource
    updateResource = update_resource
    patchResource = patch_resource
    searchResources = search_resources
    graphql = execute_graphql
    executeBatch = execute_batch
    inviteUser = invite_user
    executeBot = execute_bot
    executeOperation = execute_operation
    deployBot = deploy_bot
    saveBotCode = save_bot_code
    saveAndDeployBot = save_and_deploy_bot
    createBot = create_bot
    readBot = read_bot
    updateBot = update_bot
    deleteBot = delete_bot
    listBots = list_bots
    expandValueSet = expand_valueset
    lookupConcept = lookup_concept
    translateConcept = translate_concept
    cloneResource = clone_resource
    expungeResource = expunge_resource
    getAsyncJobStatus = get_async_job_status
    waitForAsyncJob = wait_for_async_job
