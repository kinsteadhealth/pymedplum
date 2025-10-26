import random
import time
from collections.abc import Iterator
from typing import Any, Optional, Union, TypeVar, Type, overload

import httpx

from ._base import BaseClient, OnBehalfOfContext, _raise_or_json
from .bundle import FHIRBundle
from .exceptions import MedplumError
from .helpers import to_fhir_json, decode_jwt_exp
from .types import OrgMode, PatchOperation, QueryTypes

T = TypeVar("T")


class MedplumClient(BaseClient):
    """Synchronous Medplum client with retry logic and production features"""

    def __init__(self, http_client: Optional[httpx.Client] = None, **kwargs):
        super().__init__(**kwargs)

        if http_client:
            self._http = http_client
        else:
            self._http = httpx.Client(timeout=30.0)
        self._owns_http_client = http_client is None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        """Close HTTP client if we own it"""
        if self._owns_http_client:
            self._http.close()

    def authenticate(self) -> str:
        """Authenticate using client credentials flow.

        Returns:
            Access token string

        Raises:
            ValueError: If credentials are missing
            OperationOutcomeError: On authentication failure
        """
        if not (self.client_id and self.client_secret):
            raise ValueError("client_id and client_secret required for authentication")

        response = self._http.post(
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

    def _request(self, method: str, url: str, **kwargs) -> Optional[dict[str, Any]]:
        """Make HTTP request with retry logic and OperationOutcome handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional httpx request options

        Returns:
            Parsed JSON response or None

        Raises:
            OperationOutcomeError: On error responses
        """
        if self._should_refresh_token():
            self.authenticate()

        headers = self._get_headers()
        headers.update(kwargs.pop("headers", {}) or {})

        if self.before_request:
            self.before_request(method, url, headers, kwargs)

        for attempt in range(6):
            response = self._http.request(method, url, headers=headers, **kwargs)

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

                time.sleep(delay)
                continue

            return _raise_or_json(response)

        raise MedplumError("Request failed after retries")

    def on_behalf_of(self, membership: Union[str, Any]) -> OnBehalfOfContext:
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

    def create_resource(
        self,
        resource: Union[dict[str, Any], Any],
        org_mode: Optional[OrgMode] = None,
        org_ref: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a FHIR resource.

        Args:
            resource: FHIR resource dict or Pydantic model
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request

        Returns:
            Created resource with server-assigned id
        """
        data = to_fhir_json(resource)

        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")

        return self._request("POST", f"{self.fhir_base_url}{resource_type}", json=data)

    @overload
    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: None = None
    ) -> dict[str, Any]:
        """Return raw dict (backward compatible)"""
        ...

    @overload
    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: Type[T]
    ) -> T:
        """Return typed FHIR resource"""
        ...

    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: Optional[Type[T]] = None
    ) -> Union[T, dict[str, Any]]:
        """
        Read a FHIR resource by type and ID.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            as_fhir: Optional FHIR resource class for typed response

        Returns:
            Typed resource if as_fhir provided, else dict

        Examples:
            # Dict (backward compatible)
            patient_dict = client.read_resource("Patient", "123")

            # Typed (new)
            from pymedplum.fhir import Patient
            patient = client.read_resource("Patient", "123", as_fhir=Patient)
            print(patient.name[0].given)  # Full type safety!
        """
        response = self._request(
            "GET", f"{self.fhir_base_url}{resource_type}/{resource_id}"
        )

        if as_fhir:
            return as_fhir(**response)

        return response

    def update_resource(
        self,
        resource: Union[dict[str, Any], Any],
        org_mode: Optional[OrgMode] = None,
        org_ref: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update a FHIR resource (requires id).

        Args:
            resource: FHIR resource dict or Pydantic model
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request
        """
        data = to_fhir_json(resource)

        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        resource_id = data.get("id")

        if not resource_type or not resource_id:
            raise ValueError("Resource must have resourceType and id for update")

        return self._request(
            "PUT", f"{self.fhir_base_url}{resource_type}/{resource_id}", json=data
        )

    def patch_resource(
        self, resource_type: str, resource_id: str, operations: list[PatchOperation]
    ) -> dict[str, Any]:
        """Apply JSON Patch operations to a resource"""
        return self._request(
            "PATCH",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=operations,
            headers={"Content-Type": "application/json-patch+json"},
        )

    def delete_resource(self, resource_type: str, resource_id: str) -> None:
        """Delete a FHIR resource"""
        self._request("DELETE", f"{self.fhir_base_url}{resource_type}/{resource_id}")

    @overload
    def search_resources(
        self,
        resource_type: str,
        query: Optional[QueryTypes] = None,
        return_bundle: bool = False,
    ) -> dict[str, Any]: ...

    @overload
    def search_resources(
        self,
        resource_type: str,
        query: Optional[QueryTypes] = None,
        return_bundle: bool = True,
    ) -> FHIRBundle: ...

    def search_resources(
        self,
        resource_type: str,
        query: Optional[QueryTypes] = None,
        return_bundle: bool = False,
    ) -> Union[FHIRBundle, dict[str, Any]]:
        """
        Search for FHIR resources.

        Args:
            resource_type: FHIR resource type
            query: Search parameters
            return_bundle: If True, wrap in FHIRBundle helper

        Returns:
            FHIRBundle wrapper, or raw dict

        Examples:
            # Raw dict (backward compatible)
            bundle_dict = client.search_resources("Patient", {"family": "Smith"})

            # FHIRBundle wrapper
            bundle = client.search_resources("Patient", {}, return_bundle=True)
            for patient in bundle:
                print(patient['name'])

            # With typing
            from pymedplum.fhir import Patient
            bundle = client.search_resources("Patient", {}, return_bundle=True)
            patients = bundle.get_resources_typed(Patient)
        """
        params = self._build_query_params(query)
        response = self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )

        if return_bundle:
            return FHIRBundle(response)

        return response

    def search_one(
        self, resource_type: str, query: Optional[QueryTypes] = None
    ) -> Optional[dict[str, Any]]:
        """Search for a single resource (limit 1).

        Args:
            resource_type: Type of resource to search
            query: Search parameters

        Returns:
            First matching resource or None
        """
        params = self._build_query_params(query)
        params.append(("_count", "1"))

        bundle = self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )
        entries = bundle.get("entry", [])

        if entries and "resource" in entries[0]:
            return entries[0]["resource"]
        return None

    def search_resource_pages(
        self, resource_type: str, query: Optional[QueryTypes] = None
    ) -> Iterator[dict[str, Any]]:
        """Search resources with automatic pagination.

        Yields:
            Individual resources from paginated results
        """
        bundle = self.search_resources(resource_type, query)

        while bundle:
            for entry in bundle.get("entry", []):
                if "resource" in entry:
                    yield entry["resource"]

            next_url = None
            for link in bundle.get("link", []):
                if link.get("relation") == "next":
                    next_url = link.get("url")
                    break

            if not next_url:
                break

            bundle = self._request("GET", next_url)

    def execute_graphql(
        self, query: str, variables: Optional[dict] = None
    ) -> dict[str, Any]:
        """Execute a GraphQL query"""
        return self._request(
            "POST",
            f"{self.fhir_base_url}$graphql",
            json={"query": query, "variables": variables or {}},
        )

    def execute_batch(
        self,
        bundle: Union[dict[str, Any], Any],
        org_mode: Optional[OrgMode] = None,
        org_ref: Optional[str] = None,
    ) -> dict[str, Any]:
        """Execute a FHIR batch/transaction bundle.

        Args:
            bundle: FHIR Bundle resource
            org_mode: Override client org_mode for all bundle entries
            org_ref: Override client org_ref for all bundle entries
        """
        data = to_fhir_json(bundle)

        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        return self._request("POST", self.fhir_base_url, json=data)

    def set_accounts(self, resource_ref: str, org_ref: str) -> dict[str, Any]:
        """Explicitly set accounts using $set-accounts operation.
        Preferred over auto-injection for AccessPolicy compatibility.

        Args:
            resource_ref: Reference like "Patient/123"
            org_ref: Organization reference like "Organization/ORG_A"

        Returns:
            Updated resource
        """
        if "/" not in resource_ref:
            raise ValueError(f"Invalid resource reference: {resource_ref}")

        resource_type, resource_id = resource_ref.split("/", 1)

        return self._request(
            "POST",
            f"{self.fhir_base_url}{resource_type}/{resource_id}/$set-accounts",
            json={"account": [{"reference": org_ref}]},
        )

    def execute_bot(
        self, bot_id: str, input_data: Any, content_type: str = "application/json"
    ) -> dict[str, Any]:
        """Execute a Medplum Bot by its ID.

        Args:
            bot_id: The ID of the Bot to execute.
            input_data: The input data to pass to the bot.
            content_type: The content type of the input data.

        Returns:
            The result of the bot execution.
        """
        return self._request(
            "POST",
            f"{self.fhir_base_url}Bot/{bot_id}/$execute",
            json=input_data,
            headers={"Content-Type": content_type},
        )

    def get(self, path: str, **kwargs) -> dict[str, Any]:
        """GET from any Medplum endpoint (not just FHIR).

        Args:
            path: Endpoint path (e.g., "admin/projects/123")
            **kwargs: Additional request parameters (e.g., params, headers)

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{path}"
        return self._request("GET", url, **kwargs)

    def post(self, path: str, data: Any) -> dict[str, Any]:
        """POST to any Medplum endpoint (not just FHIR).

        Args:
            path: Endpoint path (e.g., "admin/projects/123/invite")
            data: Request body

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{path}"
        return self._request("POST", url, json=data)

    def invite_user(
        self,
        project_id: str,
        resource_type: str,
        first_name: str,
        last_name: str,
        email: str,
        password: Optional[str] = None,
        send_email: bool = True,
        admin: bool = False,
        scope: str = "project",
        access_policy: Optional[str] = None,
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

    # TypeScript-compatible aliases
    createResource = create_resource
    readResource = read_resource
    updateResource = update_resource
    patchResource = patch_resource
    deleteResource = delete_resource
    searchResources = search_resources
    graphql = execute_graphql
    executeBatch = execute_batch
    inviteUser = invite_user
