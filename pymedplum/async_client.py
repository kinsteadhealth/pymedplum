import asyncio
import random
from collections.abc import AsyncIterator
from typing import Any, Literal, TypeVar, overload

import httpx

from ._base import AsyncOnBehalfOfContext, BaseClient, _raise_or_json
from .bundle import FHIRBundle
from .exceptions import MedplumError
from .fhir.base import MedplumFHIRBase
from .helpers import decode_jwt_exp, to_fhir_json
from .types import OrgMode, PatchOperation, QueryTypes

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

    async def create_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a FHIR resource.

        Args:
            resource: FHIR resource dict or Pydantic model
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request
            headers: Optional HTTP headers to include in the request

        Returns:
            Created resource with server-assigned id
        """
        data = to_fhir_json(resource)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Resource must have resourceType")

        return await self._request(
            "POST", f"{self.fhir_base_url}{resource_type}", json=data, headers=headers
        )

    @overload
    async def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: type[ResourceT]
    ) -> ResourceT: ...

    @overload
    async def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: None = None
    ) -> dict[str, Any]: ...

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

    async def update_resource(
        self,
        resource: dict[str, Any] | Any,
        org_mode: OrgMode | None = None,
        org_ref: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update a FHIR resource (requires id).

        Args:
            resource: FHIR resource dict or Pydantic model
            org_mode: Override client org_mode for this request
            org_ref: Override client org_ref for this request
            headers: Optional HTTP headers (e.g., If-Match for optimistic locking)

        Returns:
            Updated resource

        Example with optimistic locking:
            # Retrieve resource
            patient = await client.read_resource("Patient", "123")

            # Update with version check to prevent concurrent modifications
            patient["active"] = True
            updated = await client.update_resource(
                patient,
                headers={"If-Match": f'W/"{patient["meta"]["versionId"]}"'}
            )
        """
        data = to_fhir_json(resource)
        data = self._inject_org_tag(data, org_mode=org_mode, org_ref=org_ref)

        resource_type = data.get("resourceType")
        resource_id = data.get("id")

        if not resource_type or not resource_id:
            raise ValueError("Resource must have resourceType and id for update")

        return await self._request(
            "PUT",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=data,
            headers=headers,
        )

    async def patch_resource(
        self,
        resource_type: str,
        resource_id: str,
        operations: list[PatchOperation],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Apply JSON Patch operations to a resource.

        Args:
            resource_type: FHIR resource type (e.g., "Patient")
            resource_id: Resource ID
            operations: List of JSON Patch operations
            headers: Optional HTTP headers (e.g., If-Match for optimistic locking)

        Returns:
            Patched resource
        """
        patch_headers = {"Content-Type": "application/json-patch+json"}
        if headers:
            patch_headers.update(headers)

        return await self._request(
            "PATCH",
            f"{self.fhir_base_url}{resource_type}/{resource_id}",
            json=operations,
            headers=patch_headers,
        )

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
    ) -> dict[str, Any]: ...

    @overload
    async def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: None = None,
    ) -> FHIRBundle[dict[str, Any]]: ...

    @overload
    async def search_resources(
        self,
        resource_type: str,
        query: QueryTypes | None = None,
        return_bundle: Literal[True] = ...,
        as_fhir: type[ResourceT] = ...,
    ) -> FHIRBundle[ResourceT]: ...

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
        from ._fhir_ops import build_valueset_validate_params

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

        # Build endpoint
        if valueset_id:
            endpoint = f"{self.fhir_base_url}ValueSet/{valueset_id}/$validate-code"
        else:
            endpoint = f"{self.fhir_base_url}ValueSet/$validate-code"

        return await self._request("POST", endpoint, json=params_resource)

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
        from ._fhir_ops import build_codesystem_validate_params

        # Build parameters using helper
        params_resource = build_codesystem_validate_params(
            codesystem_url=codesystem_url,
            codesystem_id=codesystem_id,
            code=code,
            coding=coding,
            version=version,
        )

        # Build endpoint
        if codesystem_id:
            endpoint = f"{self.fhir_base_url}CodeSystem/{codesystem_id}/$validate-code"
        else:
            endpoint = f"{self.fhir_base_url}CodeSystem/$validate-code"

        return await self._request("POST", endpoint, json=params_resource)

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
        response = await self._http.get(
            f"{self.fhir_base_url}Binary/{binary_id}",
            headers={"Accept": "*/*", "Authorization": f"Bearer {self.access_token}"},
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

    # TypeScript-compatible aliases
    createResource = create_resource
    readResource = read_resource
    updateResource = update_resource
    searchResources = search_resources
    graphql = execute_graphql
    executeBatch = execute_batch
