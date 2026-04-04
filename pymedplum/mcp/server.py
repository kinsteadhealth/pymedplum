"""MCP server for Medplum FHIR operations.

Provides CRUD, search, terminology, and FHIR operation tools
via the Model Context Protocol using FastMCP.

Configuration via environment variables:
    MEDPLUM_BASE_URL: Medplum server base URL (default: https://api.medplum.com/)
    MEDPLUM_CLIENT_ID: OAuth2 client ID
    MEDPLUM_CLIENT_SECRET: OAuth2 client secret
    MEDPLUM_FHIR_URL_PATH: FHIR URL path (default: fhir/R4/)
    MEDPLUM_ON_BEHALF_OF: Default ProjectMembership ID for on-behalf-of requests
    MEDPLUM_READ_ONLY: Set to "true" to disable write operations
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
from collections import Counter
from contextlib import asynccontextmanager
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError

from pymedplum import AsyncMedplumClient
from pymedplum.fhir import REGISTRY as FHIR_REGISTRY
from pymedplum.types import (  # noqa: TC001 — runtime use by FastMCP schema generation
    SummaryMode,
    TotalMode,
)

_MCP_IMPORT_ERROR: ImportError | None = None

try:
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]
except ImportError as exc:
    _MCP_IMPORT_ERROR = exc

    class FastMCP:  # type: ignore[no-redef]
        """Fallback FastMCP shim so the module remains importable without extras."""

        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            pass

        def tool(self, *_args: Any, **_kwargs: Any):
            """Return a no-op decorator when MCP extras are unavailable."""

            def decorator(func):
                return func

            return decorator

        def resource(self, *_args: Any, **_kwargs: Any):
            """Return a no-op decorator when MCP extras are unavailable."""

            def decorator(func):
                return func

            return decorator

        def run(self) -> None:
            """Raise a helpful error when the server is launched without MCP extras."""
            msg = (
                "Error: The 'mcp' package is required but not installed.\n"
                "Install it with: pip install 'pymedplum[mcp]'"
            )
            raise RuntimeError(msg) from _MCP_IMPORT_ERROR


class PatchOp(BaseModel):
    """A single JSON Patch operation (RFC 6902)."""

    op: Literal["add", "remove", "replace", "copy", "move", "test"] = Field(
        description='The operation type: "add", "remove", "replace", "copy", "move", or "test"'
    )
    path: str = Field(
        description='JSON pointer to the target field, e.g. "/active" or "/name/0/family"'
    )
    value: Any | None = Field(
        default=None,
        description="The value to apply (required for add, replace, test)",
    )


class BundleInput(BaseModel):
    """Input for a FHIR batch or transaction bundle."""

    resourceType: Literal["Bundle"] = Field(
        default="Bundle", description="Must be 'Bundle'"
    )
    type: Literal["batch", "transaction"] = Field(
        description="Bundle type: 'batch' (independent entries) or 'transaction' (atomic)"
    )
    entry: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of bundle entries, each with a 'request' containing 'method' and 'url'",
    )


def _collect_refs(obj: Any, refs: set[str]) -> None:
    """Recursively collect $ref type names from a JSON schema."""
    if isinstance(obj, dict):
        if "$ref" in obj:
            refs.add(obj["$ref"].split("/")[-1])
        for v in obj.values():
            _collect_refs(v, refs)
    elif isinstance(obj, list):
        for v in obj:
            _collect_refs(v, refs)


def _get_fhir_model(resource_type: str) -> type[BaseModel] | None:
    """Look up a Pydantic FHIR model class by name from the registry.

    Returns None if the type is not found (rather than raising),
    so callers can decide whether to hard-fail or fall through.
    """
    if resource_type not in FHIR_REGISTRY:
        return None
    # Triggers lazy loading of the model
    from pymedplum import fhir

    return getattr(fhir, resource_type, None)


def _annotate_response(result: dict[str, Any]) -> dict[str, Any]:
    """Add schema hints to a FHIR response so the LLM knows its structure.

    If the response has a resourceType with a known Pydantic model,
    adds _response_type and _schema_hint fields.
    """
    resource_type = result.get("resourceType")
    if not resource_type:
        return result

    if resource_type in FHIR_REGISTRY:
        result["_response_type"] = resource_type
        result["_schema_hint"] = (
            f"Use get_resource_schema('{resource_type}') "
            f"to see field definitions and descriptions."
        )

    return result


def _validate_resource(resource: dict[str, Any]) -> None:
    """Validate a resource dict against its Pydantic FHIR model.

    If a model exists for the resource's resourceType, validates the data
    and raises ValueError with Pydantic's detailed error messages on failure.
    If no model is found, silently passes (the server will validate).
    """
    resource_type = resource.get("resourceType")
    if not resource_type:
        return

    model_class = _get_fhir_model(resource_type)
    if model_class is None:
        return

    try:
        model_class.model_validate(resource)
    except ValidationError as e:
        msg = (
            f"FHIR {resource_type} validation failed:\n{e}\n\n"
            f"Use get_resource_schema('{resource_type}') to see the expected fields."
        )
        raise ValueError(msg) from None


_UUID_PATTERN = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


def _validate_on_behalf_of(on_behalf_of: str) -> str:
    """Validate and normalize a ProjectMembership reference.

    Accepts:
    - A bare UUID: "abc-123-..."
    - A full reference: "ProjectMembership/abc-123-..."

    Returns the canonical "ProjectMembership/<id>" form.
    Raises ValueError with a clear message if the format is wrong.
    """
    value = on_behalf_of.strip()
    if not value:
        msg = "on_behalf_of cannot be empty."
        raise ValueError(msg)

    if value.startswith("ProjectMembership/"):
        membership_id = value[len("ProjectMembership/") :]
    else:
        membership_id = value

    if not re.match(_UUID_PATTERN, membership_id, re.IGNORECASE):
        msg = (
            f"Invalid ProjectMembership reference: '{on_behalf_of}'. "
            f"Expected a UUID or 'ProjectMembership/<uuid>' format. "
            f"Example: 'ProjectMembership/550e8400-e29b-41d4-a716-446655440000'"
        )
        raise ValueError(msg)

    return f"ProjectMembership/{membership_id}"


_READ_ONLY_OPERATIONS = frozenset(
    {
        "everything",
        "validate-code",
        "lookup",
        "expand",
        "translate",
        "match",
        "meta",
        "graphql",
        "document",
        "summary",
    }
)


def _is_read_only() -> bool:
    """Check if server is in read-only mode (re-evaluated per call)."""
    return os.getenv("MEDPLUM_READ_ONLY", "false").lower() in ("true", "1", "yes")


def _check_write_allowed() -> None:
    """Raise PermissionError if the server is in read-only mode."""
    if _is_read_only():
        msg = (
            "This server is running in read-only mode (MEDPLUM_READ_ONLY=true). "
            "Write operations are disabled."
        )
        raise PermissionError(msg)


@asynccontextmanager
async def _lifespan(_server: FastMCP):
    """Lifespan handler: clean up the shared client on shutdown."""
    yield
    global _client  # noqa: PLW0603
    if _client is not None:
        await _client.close()
        _client = None


mcp = FastMCP(
    "Medplum FHIR Server",
    lifespan=_lifespan,
    instructions=(
        "MCP server for interacting with a Medplum FHIR server. "
        "Provides tools for CRUD operations on any FHIR resource type, "
        "advanced search with FHIR search parameters, terminology operations "
        "(ValueSet, CodeSystem, ConceptMap), and generic FHIR operation execution. "
        "All tools accept standard FHIR resource types like Patient, Observation, "
        "Condition, MedicationRequest, etc. "
        "Prefer read and search tools first. Use create, update, patch, and "
        "delete only when explicitly requested by the user."
    ),
)

_client: AsyncMedplumClient | None = None
_client_lock: asyncio.Lock | None = None


async def _get_client() -> AsyncMedplumClient:
    """Get or create the authenticated AsyncMedplumClient.

    Uses a lock to prevent concurrent initialization races.
    The underlying client handles token refresh automatically.
    """
    global _client, _client_lock  # noqa: PLW0603

    if _client is not None:
        return _client

    if _client_lock is None:
        _client_lock = asyncio.Lock()

    async with _client_lock:
        # Double-check after acquiring lock
        if _client is not None:
            return _client

        base_url = os.getenv("MEDPLUM_BASE_URL", "https://api.medplum.com/")
        client_id = os.getenv("MEDPLUM_CLIENT_ID")
        client_secret = os.getenv("MEDPLUM_CLIENT_SECRET")
        fhir_url_path = os.getenv("MEDPLUM_FHIR_URL_PATH", "fhir/R4/")

        if not client_id or not client_secret:
            msg = (
                "MEDPLUM_CLIENT_ID and MEDPLUM_CLIENT_SECRET environment variables "
                "are required. Set them in your MCP server configuration."
            )
            raise ValueError(msg)

        default_obo = os.getenv("MEDPLUM_ON_BEHALF_OF")
        if default_obo:
            default_obo = _validate_on_behalf_of(default_obo)

        client = AsyncMedplumClient(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            fhir_url_path=fhir_url_path,
            default_on_behalf_of=default_obo,
        )
        await client.authenticate()
        _client = client
        return _client


@asynccontextmanager
async def _with_obo(on_behalf_of: str | None = None):
    """Yield an AsyncMedplumClient, optionally scoped to a ProjectMembership.

    If on_behalf_of is provided, validates it and wraps the call in an
    on_behalf_of context (overriding the default). Otherwise yields the
    base client (which may have its own default from MEDPLUM_ON_BEHALF_OF).
    """
    client = await _get_client()
    if on_behalf_of:
        ref = _validate_on_behalf_of(on_behalf_of)
        async with client.on_behalf_of(ref) as obo_client:
            yield obo_client
    else:
        yield client


@mcp.tool(
    annotations={
        "title": "Get FHIR Resource Schema",
        "readOnlyHint": True,
    }
)
async def get_resource_schema(
    resource_type: str,
    include_nested: bool = False,
) -> dict[str, Any]:
    """Get the Pydantic JSON schema for a FHIR resource or data type.

    Returns the full field definitions with descriptions, types, enums,
    and constraints for any FHIR R4 resource type or data type (including
    Medplum-specific types like Bot, Project, ProjectMembership).

    Use this before creating or updating resources to understand
    exactly what fields are available and their expected formats.

    By default, nested type definitions ($defs) are stripped to keep the
    response compact. The schema will still show $ref pointers indicating
    which child types are used — call this tool again with those type
    names to see their schemas.

    Args:
        resource_type: FHIR type name, e.g., "Patient", "Observation",
            "HumanName", "CodeableConcept", "Bot", "ProjectMembership"
        include_nested: If true, include full $defs for all referenced
            types in a single response (can be large)

    Returns:
        JSON Schema with field names, types, descriptions, and constraints
    """
    model_class = _get_fhir_model(resource_type)
    if model_class is None:
        available = sorted(FHIR_REGISTRY.keys())
        msg = (
            f"Unknown FHIR type '{resource_type}'. "
            f"Available types include: {', '.join(available[:30])}... "
            f"({len(available)} total)"
        )
        raise ValueError(msg)

    schema = model_class.model_json_schema()

    if not include_nested:
        # Strip $defs but collect referenced type names for discoverability
        compact = {k: v for k, v in schema.items() if k != "$defs"}
        refs: set[str] = set()
        _collect_refs(compact, refs)

        if refs:
            compact["_referenced_types"] = sorted(refs)
            compact["_hint"] = (
                "Nested type schemas were omitted for brevity. "
                "Call get_resource_schema with any type from "
                "_referenced_types to see its full schema."
            )

        return compact

    return schema


@mcp.tool(
    annotations={
        "title": "Read FHIR Resource",
        "readOnlyHint": True,
    }
)
async def read_resource(
    resource_type: str,
    resource_id: str,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Read a single FHIR resource by type and ID.

    Args:
        resource_type: FHIR resource type (e.g., "Patient", "Observation",
            "Condition", "MedicationRequest")
        resource_id: The resource's logical ID
        on_behalf_of: Optional ProjectMembership ID or reference
            (e.g., "ProjectMembership/<uuid>" or just "<uuid>").
            Executes the request as that project member.

    Returns:
        The FHIR resource as a JSON object
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.read_resource(resource_type, resource_id)
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Search FHIR Resources",
        "readOnlyHint": True,
    }
)
async def search_resources(
    resource_type: str,
    params: dict[str, Any] | None = None,
    count: int | None = None,
    offset: int | None = None,
    sort: str | None = None,
    include: str | list[str] | None = None,
    revinclude: str | list[str] | None = None,
    summary: SummaryMode | None = None,
    total: TotalMode | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Search for FHIR resources with standard FHIR search parameters.

    Use get_resource_capabilities first to discover valid search parameters
    for a resource type if you're unsure what parameters are available.

    Args:
        resource_type: FHIR resource type to search (e.g., "Patient",
            "Observation", "Condition")
        params: FHIR search parameters as key-value pairs.
            Examples: {"family": "Smith"}, {"patient": "Patient/123", "code": "29463-7"},
            {"status": "active", "date": "ge2024-01-01"}
        count: Maximum number of results to return per page (default: server default)
        offset: Starting offset for pagination (0-based)
        sort: Sort order, e.g., "-date" (descending) or "name" (ascending).
            Use comma-separated for multiple: "-date,status"
        include: Related resources to include via _include
            (e.g., "Observation:subject" to include the Patient)
        revinclude: Reverse includes via _revinclude
            (e.g., "Provenance:target" to include Provenance resources)
        summary: Result summary mode
        total: How to calculate Bundle.total
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        FHIR Bundle containing matching resources
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.search_with_options(
            resource_type,
            query=params,
            count=count,
            offset=offset,
            sort=sort,
            include=include,
            revinclude=revinclude,
            summary=summary,
            total=total,
        )

    if isinstance(result, dict) and result.get("total") == 0:
        result["_hint"] = (
            f"No results found. Use get_resource_capabilities('{resource_type}') "
            f"to see valid search parameters for {resource_type}."
        )

    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Search Single FHIR Resource",
        "readOnlyHint": True,
    }
)
async def search_one(
    resource_type: str,
    params: dict[str, Any] | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any] | None:
    """Search for a single FHIR resource, returning it directly (not in a Bundle).

    Convenience tool for when you expect exactly one result. Returns the
    resource directly instead of wrapping it in a Bundle, or null if not found.

    Args:
        resource_type: FHIR resource type to search (e.g., "Patient")
        params: FHIR search parameters as key-value pairs.
            Examples: {"identifier": "12345"}, {"family": "Smith", "given": "Alice"}
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        The matching FHIR resource, or null if no match found
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.search_one(resource_type, params)
    if result is None:
        return None
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Search All FHIR Resources",
        "readOnlyHint": True,
    }
)
async def search_all_resources(
    resource_type: str,
    params: dict[str, Any] | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Search across all pages and return a flattened Bundle of resources."""
    async with _with_obo(on_behalf_of) as client:
        resources = [
            resource
            async for resource in client.search_resource_pages(resource_type, params)
        ]

    result: dict[str, Any] = {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [{"resource": resource} for resource in resources],
        "total": len(resources),
        "_pages_mode": "all",
        "_resources_returned": len(resources),
    }
    if not resources:
        result["_hint"] = (
            f"No results found. Use get_resource_capabilities('{resource_type}') "
            f"to see valid search parameters for {resource_type}."
        )

    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Create FHIR Resource",
        "readOnlyHint": False,
        "destructiveHint": False,
    }
)
async def create_resource(
    resource: dict[str, Any],
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Create a new FHIR resource on the Medplum server.

    The resource must include a "resourceType" field.

    Args:
        resource: Complete FHIR resource as a JSON object. Must include
            "resourceType". Example:
            {"resourceType": "Patient", "name": [{"given": ["Alice"], "family": "Smith"}]}
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        The created resource with server-assigned id and meta
    """
    _check_write_allowed()
    if "resourceType" not in resource:
        msg = "Resource must include 'resourceType' field."
        raise ValueError(msg)
    _validate_resource(resource)

    async with _with_obo(on_behalf_of) as client:
        result = await client.create_resource(resource)
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Create FHIR Resource If None Exist",
        "readOnlyHint": False,
        "destructiveHint": False,
    }
)
async def create_resource_if_none_exist(
    resource: dict[str, Any],
    if_none_exist: str,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Create a FHIR resource only if no matching resource already exists.

    This uses FHIR conditional create via the If-None-Exist header. It is
    safer for agents than a search-then-create sequence because the server
    performs the existence check atomically.
    """
    _check_write_allowed()
    if "resourceType" not in resource:
        msg = "Resource must include 'resourceType' field."
        raise ValueError(msg)
    _validate_resource(resource)

    async with _with_obo(on_behalf_of) as client:
        result = await client.create_resource_if_none_exist(resource, if_none_exist)
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Update FHIR Resource",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def update_resource(
    resource: dict[str, Any],
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Update (replace) an existing FHIR resource on the Medplum server.

    The resource must include both "resourceType" and "id" fields.
    This performs a full replacement (HTTP PUT), not a partial update.
    Use patch_resource for partial updates.

    Args:
        resource: Complete FHIR resource with "resourceType" and "id".
            All fields should be included, not just changed ones.
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        The updated resource
    """
    _check_write_allowed()
    if "resourceType" not in resource:
        msg = "Resource must include 'resourceType' field."
        raise ValueError(msg)
    if "id" not in resource:
        msg = "Resource must include 'id' field for updates. Use create_resource for new resources."
        raise ValueError(msg)
    _validate_resource(resource)

    async with _with_obo(on_behalf_of) as client:
        result = await client.update_resource(resource)

    old_version = resource.get("meta", {}).get("versionId")
    new_version = result.get("meta", {}).get("versionId")
    if old_version and new_version and old_version != new_version:
        result["_update_info"] = {
            "previous_version": old_version,
            "new_version": new_version,
        }

    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Patch FHIR Resource",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def patch_resource(
    resource_type: str,
    resource_id: str,
    operations: list[PatchOp],
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Apply JSON Patch operations to a FHIR resource on the Medplum server.

    This performs a partial update using JSON Patch (RFC 6902).
    Useful when you only need to change specific fields without
    sending the entire resource.

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        resource_id: Resource ID to patch
        operations: List of JSON Patch operations
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        The patched resource
    """
    _check_write_allowed()
    if not operations:
        msg = "At least one patch operation is required."
        raise ValueError(msg)

    raw_ops = [op.model_dump(exclude_none=True) for op in operations]
    async with _with_obo(on_behalf_of) as client:
        result = await client.patch_resource(resource_type, resource_id, raw_ops)
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Delete FHIR Resource",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def delete_resource(
    resource_type: str,
    resource_id: str,
    on_behalf_of: str | None = None,
) -> dict[str, str]:
    """Delete a FHIR resource from the Medplum server.

    On Medplum, this performs a soft delete — the resource is marked as
    deleted but may be restorable. The resource will no longer appear
    in search results. Behavior may vary on other FHIR servers.

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        resource_id: Resource ID to delete
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Confirmation with the deleted resource type and ID
    """
    _check_write_allowed()
    async with _with_obo(on_behalf_of) as client:
        await client.delete_resource(resource_type, resource_id)
    return {
        "status": "deleted",
        "resourceType": resource_type,
        "id": resource_id,
    }


@mcp.tool(
    annotations={
        "title": "Get FHIR Capabilities",
        "readOnlyHint": True,
    }
)
async def get_resource_capabilities(
    resource_type: str | None = None,
) -> dict[str, Any]:
    """Get the FHIR server's CapabilityStatement or details for a resource type.

    Use this to discover what search parameters, operations, and interactions
    are available for a given resource type. Call without arguments to get
    the full server CapabilityStatement.

    Args:
        resource_type: Optional FHIR resource type to filter capabilities for.
            If provided, returns only the capabilities for that resource type.
            If omitted, returns the full CapabilityStatement.

    Returns:
        CapabilityStatement or filtered resource capabilities
    """
    client = await _get_client()
    fhir_url_path = os.getenv("MEDPLUM_FHIR_URL_PATH", "fhir/R4/")
    result = await client.get(f"{fhir_url_path}metadata")

    if resource_type and isinstance(result, dict):
        rest_blocks = result.get("rest", [])
        # Search all rest blocks, preferring mode=server
        for rest in sorted(
            rest_blocks,
            key=lambda r: r.get("mode") != "server",
        ):
            for r in rest.get("resource", []):
                if r.get("type") == resource_type:
                    return r
        msg = f"Resource type '{resource_type}' not found in CapabilityStatement"
        raise ValueError(msg)

    return result


@mcp.tool(
    annotations={
        "title": "Get Patient Everything",
        "readOnlyHint": True,
    }
)
async def get_patient_everything(
    patient_id: str,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Get all data for a patient using the FHIR $everything operation.

    Returns a Bundle containing the Patient resource and all related
    resources: Conditions, Observations, MedicationRequests, Encounters,
    AllergyIntolerances, Procedures, and more.

    This is the most common way to get a complete clinical picture
    for a single patient.

    Args:
        patient_id: The Patient resource ID
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Bundle containing the patient and all related resources,
        with a _resource_summary showing counts by type
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.execute_operation(
            "Patient", "everything", resource_id=patient_id, method="GET"
        )

    if isinstance(result, dict):
        entries = result.get("entry", [])
        type_counts = Counter(
            e.get("resource", {}).get("resourceType", "Unknown") for e in entries
        )
        result["_resource_summary"] = dict(type_counts.most_common())
        result["_total_resources"] = len(entries)

    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Validate Code in ValueSet",
        "readOnlyHint": True,
    }
)
async def validate_code(
    code: str,
    system: str,
    valueset_url: str | None = None,
    valueset_id: str | None = None,
    display: str | None = None,
) -> dict[str, Any]:
    """Check if a code belongs to a ValueSet.

    Validates whether a given code from a code system is a member
    of a specific ValueSet. Useful for checking if clinical codes
    are valid for a particular context.

    Args:
        code: The code to validate (e.g., "255604002")
        system: Code system URL (e.g., "http://snomed.info/sct",
            "http://loinc.org")
        valueset_url: Canonical URL of the ValueSet to check against
        valueset_id: ID of a specific ValueSet resource (alternative to URL)
        display: Optional display text to validate alongside the code

    Returns:
        Parameters resource indicating if the code is valid, with
        result (boolean) and optional display text
    """
    client = await _get_client()
    return await client.validate_valueset_code(
        valueset_url=valueset_url,
        valueset_id=valueset_id,
        code=code,
        system=system,
        display=display,
    )


@mcp.tool(
    annotations={
        "title": "Validate Code in CodeSystem",
        "readOnlyHint": True,
    }
)
async def validate_codesystem_code(
    code: str | None = None,
    codesystem_url: str | None = None,
    codesystem_id: str | None = None,
    coding: dict[str, Any] | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    """Check if a code exists in a CodeSystem."""
    client = await _get_client()
    return await client.validate_codesystem_code(
        codesystem_url=codesystem_url,
        codesystem_id=codesystem_id,
        code=code,
        coding=coding,
        version=version,
    )


@mcp.tool(
    annotations={
        "title": "Expand ValueSet",
        "readOnlyHint": True,
    }
)
async def expand_valueset(
    valueset_url: str | None = None,
    valueset_id: str | None = None,
    filter: str | None = None,
    count: int | None = None,
    offset: int | None = None,
    active_only: bool | None = None,
) -> dict[str, Any]:
    """Expand a ValueSet to list all its codes.

    Returns the full set of concepts in a ValueSet. Useful for
    populating dropdowns, discovering valid codes, or browsing
    terminology.

    Args:
        valueset_url: Canonical URL of the ValueSet
            (e.g., "http://hl7.org/fhir/ValueSet/administrative-gender")
        valueset_id: ID of a specific ValueSet resource
        filter: Text filter for substring matching on display names
            (e.g., "diab" to find diabetes-related codes)
        count: Maximum number of concepts to return
        offset: Starting offset for pagination
        active_only: If true, only include active codes

    Returns:
        ValueSet resource with expansion containing matching codes
    """
    client = await _get_client()
    return await client.expand_valueset(
        valueset_url=valueset_url,
        valueset_id=valueset_id,
        filter=filter,
        count=count,
        offset=offset,
        active_only=active_only,
    )


@mcp.tool(
    annotations={
        "title": "Lookup Code in CodeSystem",
        "readOnlyHint": True,
    }
)
async def lookup_concept(
    code: str,
    system: str | None = None,
    codesystem_id: str | None = None,
    display_language: str | None = None,
    property: list[str] | None = None,
) -> dict[str, Any]:
    """Look up details about a code in a CodeSystem.

    Returns detailed information including display name, definition,
    and properties for a code. Useful for understanding what a
    clinical code means.

    Args:
        code: The code to look up (e.g., "73211009")
        system: Code system URL (e.g., "http://snomed.info/sct",
            "http://loinc.org"). Required unless using codesystem_id.
        codesystem_id: ID of a specific CodeSystem resource
        display_language: Preferred language for display text (e.g., "en")
        property: List of properties to include in the response

    Returns:
        Parameters resource with code details (display, definition, properties)
    """
    client = await _get_client()
    return await client.lookup_concept(
        code=code,
        system=system,
        codesystem_id=codesystem_id,
        display_language=display_language,
        property=property,
    )


@mcp.tool(
    annotations={
        "title": "Translate Code Between Systems",
        "readOnlyHint": True,
    }
)
async def translate_concept(
    code: str,
    system: str,
    target_system: str | None = None,
    conceptmap_url: str | None = None,
    conceptmap_id: str | None = None,
    reverse: bool | None = None,
) -> dict[str, Any]:
    """Translate a code from one code system to another.

    Uses ConceptMap resources to map codes between different code systems
    (e.g., SNOMED CT to ICD-10). Useful for cross-system interoperability.

    Args:
        code: Source code to translate (e.g., "73211009")
        system: Source code system URL (e.g., "http://snomed.info/sct")
        target_system: Target code system URL
            (e.g., "http://hl7.org/fhir/sid/icd-10")
        conceptmap_url: Canonical URL of a specific ConceptMap to use
        conceptmap_id: ID of a specific ConceptMap resource
        reverse: If true, reverse the mapping direction

    Returns:
        Parameters resource with translation matches
    """
    client = await _get_client()
    return await client.translate_concept(
        code=code,
        system=system,
        target_system=target_system,
        conceptmap_url=conceptmap_url,
        conceptmap_id=conceptmap_id,
        reverse=reverse,
    )


@mcp.tool(
    annotations={
        "title": "Execute FHIR Operation",
    }
)
async def execute_operation(
    resource_type: str,
    operation: str,
    resource_id: str | None = None,
    params: dict[str, Any] | None = None,
    method: Literal["GET", "POST"] = "POST",
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a FHIR operation (standard or custom) on the Medplum server.

    Supports type-level operations (e.g., Patient/$match) and
    instance-level operations (e.g., Patient/123/$everything).

    In read-only mode, only known read-only operations are allowed
    (e.g., $everything, $validate-code, $lookup, $expand, $translate).

    Common operations:
    - Patient/$everything: Get all data for a patient
    - ValueSet/$validate-code: Validate a code (prefer validate_code tool)
    - CodeSystem/$lookup: Look up a code (prefer lookup_concept tool)

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        operation: Operation name without $ prefix (e.g., "everything", "match")
        resource_id: Resource ID for instance-level operations
        params: Parameters to pass to the operation
        method: HTTP method
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Operation response (typically Parameters or Bundle)
    """
    op_name = operation.lstrip("$").lower()

    if _is_read_only() and op_name not in _READ_ONLY_OPERATIONS:
        msg = (
            f"Operation '${operation}' is not in the read-only allowlist. "
            f"Server is in read-only mode (MEDPLUM_READ_ONLY=true). "
            f"Allowed operations: {', '.join(sorted('$' + o for o in _READ_ONLY_OPERATIONS))}"
        )
        raise PermissionError(msg)

    async with _with_obo(on_behalf_of) as client:
        result = await client.execute_operation(
            resource_type=resource_type,
            operation=operation,
            resource_id=resource_id,
            params=params,
            method=method,
            wrap_params=True,
        )
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Execute GraphQL Query",
        "readOnlyHint": True,
    }
)
async def execute_graphql(
    query: str,
    variables: dict[str, Any] | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a FHIR GraphQL query against the Medplum server.

    Medplum's GraphQL endpoint is read-only (queries only, no mutations).
    GraphQL provides a flexible way to query FHIR data, especially
    when you need to traverse resource references or fetch specific
    fields across multiple resource types in a single request.

    Args:
        query: GraphQL query string. Example:
            '{ Patient(id: "123") { name { given family } birthDate } }'
        variables: Optional GraphQL variables
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        GraphQL response
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.execute_graphql(query, variables)
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Export Patient C-CDA",
        "readOnlyHint": True,
    }
)
async def export_ccda(
    patient_id: str,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Export a patient's history as a C-CDA XML document."""
    async with _with_obo(on_behalf_of) as client:
        ccda_xml = await client.export_ccda(patient_id)
    return {
        "resourceType": "Binary",
        "contentType": "application/xml",
        "format": "ccda",
        "patientId": patient_id,
        "data": ccda_xml,
    }


@mcp.tool(
    annotations={
        "title": "Execute Medplum Bot",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def execute_bot(
    bot_id: str,
    input_data: dict[str, Any],
    content_type: str = "application/json",
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a Medplum Bot with the provided input data."""
    _check_write_allowed()
    async with _with_obo(on_behalf_of) as client:
        result = await client.execute_bot(bot_id, input_data, content_type=content_type)
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Create Medplum Bot",
        "readOnlyHint": False,
        "destructiveHint": False,
    }
)
async def create_bot(
    name: str,
    description: str = "",
    source_code: str = "",
    runtime_version: Literal["awslambda", "vmcontext"] | None = None,
    additional_fields: dict[str, Any] | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Create a Medplum Bot resource with agent-friendly defaults."""
    _check_write_allowed()
    async with _with_obo(on_behalf_of) as client:
        result = await client.create_bot(
            name=name,
            description=description,
            source_code=source_code,
            runtime_version=runtime_version,
            **(additional_fields or {}),
        )
    return _annotate_response(result)


@mcp.tool(
    annotations={
        "title": "Save And Deploy Medplum Bot",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def save_and_deploy_bot(
    bot_id: str,
    source_code: str,
    compiled_code: str,
    filename: str = "index.js",
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Save bot source code and deploy compiled code in one step."""
    _check_write_allowed()
    async with _with_obo(on_behalf_of) as client:
        bot, deploy_result = await client.save_and_deploy_bot(
            bot_id=bot_id,
            source_code=source_code,
            compiled_code=compiled_code,
            filename=filename,
        )
    return {
        "bot": _annotate_response(bot),
        "deployment": deploy_result,
    }


@mcp.tool(
    annotations={
        "title": "Execute FHIR Batch or Transaction",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def execute_batch(
    bundle: BundleInput,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a FHIR batch or transaction bundle on the Medplum server.

    A batch bundle processes each entry independently (some may fail
    while others succeed). A transaction bundle is atomic (all succeed
    or all fail).

    In read-only mode, bundles containing only GET requests are allowed
    (including transactions). Bundles with any write methods (POST, PUT,
    PATCH, DELETE) are blocked.

    Args:
        bundle: FHIR Bundle with type "batch" or "transaction"
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Response Bundle with results for each entry
    """
    write_methods = {"POST", "PUT", "PATCH", "DELETE"}
    has_writes = any(
        e.get("request", {}).get("method", "").upper() in write_methods
        for e in bundle.entry
    )

    if has_writes:
        _check_write_allowed()

    raw = bundle.model_dump(by_alias=True)
    async with _with_obo(on_behalf_of) as client:
        if bundle.type == "transaction":
            result = await client.execute_transaction(raw)
        else:
            result = await client.execute_batch(raw)
    return _annotate_response(result)


@mcp.resource("medplum://server-info")
async def server_info() -> dict[str, Any]:
    """Server connection info and configuration."""
    info: dict[str, Any] = {
        "base_url": os.getenv("MEDPLUM_BASE_URL", "https://api.medplum.com/"),
        "read_only": _is_read_only(),
    }

    default_obo = os.getenv("MEDPLUM_ON_BEHALF_OF")
    if default_obo:
        info["default_on_behalf_of"] = default_obo

    info["description"] = (
        "Medplum FHIR server MCP interface. "
        "Use get_resource_capabilities to discover available "
        "resource types and search parameters."
    )

    return info


def main() -> None:
    """Run the MCP server."""
    if _MCP_IMPORT_ERROR is not None:
        print(
            "Error: The 'mcp' package is required but not installed.\n"
            "Install it with: pip install 'pymedplum[mcp]'",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.getenv("MEDPLUM_CLIENT_ID") or not os.getenv("MEDPLUM_CLIENT_SECRET"):
        print(
            "Error: MEDPLUM_CLIENT_ID and MEDPLUM_CLIENT_SECRET environment "
            "variables are required.",
            file=sys.stderr,
        )
        sys.exit(1)

    mcp.run()


if __name__ == "__main__":
    main()
