import random
import time
from collections.abc import Iterator
from typing import Any, Literal, Optional, TypeVar, Union, overload

import httpx

from ._base import BaseClient, OnBehalfOfContext, _raise_or_json
from .bundle import FHIRBundle
from .exceptions import MedplumError
from .helpers import decode_jwt_exp, to_fhir_json
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
        self, resource_type: str, resource_id: str, as_fhir: type[T]
    ) -> T: ...

    @overload
    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: None = None
    ) -> dict[str, Any]: ...  # type: ignore[overload-cannot-match]

    def read_resource(
        self, resource_type: str, resource_id: str, as_fhir: Optional[type[T]] = None
    ) -> Union[T, dict[str, Any]]:
        """Read a FHIR resource by type and ID.

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
        return_bundle: Literal[False] = False,
    ) -> dict[str, Any]: ...

    @overload
    def search_resources(
        self,
        resource_type: str,
        query: Optional[QueryTypes] = None,
        return_bundle: Literal[True] = ...,
    ) -> FHIRBundle: ...

    def search_resources(
        self,
        resource_type: str,
        query: Optional[QueryTypes] = None,
        return_bundle: bool = False,
    ) -> Union[FHIRBundle, dict[str, Any]]:
        """Search for FHIR resources.

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

    def export_ccda(self, patient_id: str) -> str:
        """Export a patient's complete history as a C-CDA XML document.

        Args:
            patient_id: The ID of the patient to export

        Returns:
            C-CDA XML document as a string

        Example:
            ccda_xml = client.export_ccda("patient-123")
            with open("patient-record.xml", "w") as f:
                f.write(ccda_xml)
        """
        response = self._http.get(
            f"{self.fhir_base_url}Patient/{patient_id}/$ccda-export",
            headers=self._get_headers(),
        )
        if response.status_code >= 400:
            from ._base import _raise_or_json

            _raise_or_json(response)
        return response.text

    def validate_valueset_code(
        self,
        valueset_url: Optional[str] = None,
        valueset_id: Optional[str] = None,
        code: Optional[str] = None,
        system: Optional[str] = None,
        coding: Optional[dict] = None,
        codeable_concept: Optional[dict] = None,
        display: Optional[str] = None,
        abstract: Optional[bool] = None,
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

        return self._request("POST", endpoint, json=params_resource)

    def validate_codesystem_code(
        self,
        codesystem_url: Optional[str] = None,
        codesystem_id: Optional[str] = None,
        code: Optional[str] = None,
        coding: Optional[dict] = None,
        version: Optional[str] = None,
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

        return self._request("POST", endpoint, json=params_resource)

    def execute_transaction(self, bundle: Union[dict, Any]) -> dict[str, Any]:
        """Execute a transaction bundle atomically.

        All operations in a transaction bundle succeed or fail together.
        Use placeholder IDs (urn:uuid:xxx) to reference resources within the bundle.

        Args:
            bundle: Bundle resource with type="transaction" or dict with entries

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
        from .helpers import to_fhir_json

        bundle_data = to_fhir_json(bundle) if hasattr(bundle, "model_dump") else bundle

        # Ensure it's a transaction bundle
        if bundle_data.get("type") != "transaction":
            bundle_data["type"] = "transaction"

        # POST to base URL (not /fhir/R4/Bundle, just /fhir/R4/)
        return self._request("POST", self.fhir_base_url.rstrip("/"), json=bundle_data)

    def upload_binary(
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
                binary = client.upload_binary(f.read(), "application/pdf")
            binary_id = binary["id"]
        """
        return self._request(
            "POST",
            f"{self.fhir_base_url}Binary",
            data=content,
            headers={"Content-Type": content_type},
        )

    def download_binary(self, binary_id: str) -> bytes:
        """Download binary content.

        Args:
            binary_id: ID of the Binary resource

        Returns:
            Binary content as bytes

        Example:
            content = client.download_binary("binary-123")
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
        response = self._http.get(
            f"{self.fhir_base_url}Binary/{binary_id}",
            headers={"Accept": "*/*", "Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code >= 400:
            from ._base import _raise_or_json

            _raise_or_json(response)
        return response.content

    def create_document_reference(
        self,
        patient_id: str,
        binary_id: str,
        content_type: str,
        title: str,
        description: Optional[str] = None,
        doc_type_code: Optional[dict] = None,
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
