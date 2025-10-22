import asyncio
import random
from collections.abc import AsyncIterator
from typing import Any, Optional, Union

import httpx

from ._base import AsyncOnBehalfOfContext, BaseClient, _raise_or_json
from .exceptions import MedplumError
from .helpers.fhir import to_fhir_json
from .helpers.jwt import decode_jwt_exp
from .types import OrgMode, QueryTypes


class AsyncMedplumClient(BaseClient):
    """Asynchronous Medplum client with retry logic and production features"""

    def __init__(self, http_client: Optional[httpx.AsyncClient] = None, **kwargs):
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

    async def _request(
        self, method: str, url: str, **kwargs
    ) -> Optional[dict[str, Any]]:
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

    def on_behalf_of(self, membership: Union[str, Any]) -> AsyncOnBehalfOfContext:
        """Create async context manager for on-behalf-of operations"""
        return AsyncOnBehalfOfContext(self, membership)

    async def create_resource(
        self,
        resource: Union[dict[str, Any], Any],
        org_mode: Optional[OrgMode] = None,
        org_ref: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a FHIR resource"""
        data = to_fhir_json(resource)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")

        return await self._request(
            "POST", f"{self.fhir_base_url}{resource_type}", json=data
        )

    async def read_resource(
        self, resource_type: str, resource_id: str
    ) -> dict[str, Any]:
        """Read a FHIR resource by type and ID"""
        return await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}/{resource_id}"
        )

    async def update_resource(
        self,
        resource: Union[dict[str, Any], Any],
        org_mode: Optional[OrgMode] = None,
        org_ref: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update a FHIR resource"""
        data = to_fhir_json(resource)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        resource_id = data.get("id")

        if not resource_type or not resource_id:
            raise ValueError("Resource must have resourceType and id for update")

        return await self._request(
            "PUT", f"{self.fhir_base_url}{resource_type}/{resource_id}", json=data
        )

    async def search_resources(
        self, resource_type: str, query: Optional[QueryTypes] = None
    ) -> dict[str, Any]:
        """Search for FHIR resources"""
        params = self._build_query_params(query)
        return await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )

    async def search_one(
        self, resource_type: str, query: Optional[QueryTypes] = None
    ) -> Optional[dict[str, Any]]:
        """Search for a single resource"""
        params = self._build_query_params(query)
        params.append(("_count", "1"))

        bundle = await self._request(
            "GET", f"{self.fhir_base_url}{resource_type}", params=params
        )
        entries = bundle.get("entry", [])

        if entries and "resource" in entries[0]:
            return entries[0]["resource"]
        return None

    async def search_resource_pages(
        self, resource_type: str, query: Optional[QueryTypes] = None
    ) -> AsyncIterator[dict[str, Any]]:
        """Search resources with automatic pagination"""
        bundle = await self.search_resources(resource_type, query)

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

            bundle = await self._request("GET", next_url)

    async def execute_graphql(
        self, query: str, variables: Optional[dict] = None
    ) -> dict[str, Any]:
        """Execute a GraphQL query"""
        return await self._request(
            "POST",
            f"{self.fhir_base_url}$graphql",
            json={"query": query, "variables": variables or {}},
        )

    async def execute_batch(
        self,
        bundle: Union[dict[str, Any], Any],
        org_mode: Optional[OrgMode] = None,
        org_ref: Optional[str] = None,
    ) -> dict[str, Any]:
        """Execute a FHIR batch/transaction bundle"""
        data = to_fhir_json(bundle)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        return await self._request("POST", self.fhir_base_url, json=data)

    async def execute_bot(
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
        return await self._request(
            "POST",
            f"{self.fhir_base_url}Bot/{bot_id}/$execute",
            json=input_data,
            headers={"Content-Type": content_type},
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
            payload["accessPolicy"] = access_policy

        return await self.post(f"admin/projects/{project_id}/invite", payload)

    # TypeScript-compatible aliases
    createResource = create_resource
    readResource = read_resource
    updateResource = update_resource
    searchResources = search_resources
    graphql = execute_graphql
    executeBatch = execute_batch
