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

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

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
    """A single JSON Patch operation (RFC 6902).

    Note: `value` is serialized with `exclude_unset=True` so an explicit
    `value=None` is preserved (valid JSON Patch) and distinguished from
    "value omitted".
    """

    model_config = ConfigDict(populate_by_name=True)

    op: Literal["add", "remove", "replace", "copy", "move", "test"] = Field(
        description='The operation type: "add", "remove", "replace", "copy", "move", or "test"'
    )
    path: str = Field(
        description='JSON pointer to the target field, e.g. "/active" or "/name/0/family"'
    )
    value: Any = Field(
        default=None,
        description=(
            "The value to apply (required for add, replace, test). "
            "May be explicitly null."
        ),
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description=(
            'JSON pointer to the source location (required for "copy" and "move"). '
            'Serialized as "from" per RFC 6902.'
        ),
    )

    @model_validator(mode="after")
    def _check_op_requirements(self) -> PatchOp:
        if self.op in ("copy", "move") and not self.from_:
            msg = f"JSON Patch '{self.op}' operation requires a 'from' field."
            raise ValueError(msg)
        if (
            self.op in ("add", "replace", "test")
            and "value" not in self.model_fields_set
        ):
            msg = f"JSON Patch '{self.op}' operation requires a 'value' field."
            raise ValueError(msg)
        return self


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


_MODEL_CACHE: dict[str, type[BaseModel] | None] = {}


def _get_fhir_model(resource_type: str) -> type[BaseModel] | None:
    """Look up a Pydantic FHIR model class by name from the registry.

    Returns None if the type is not found (rather than raising),
    so callers can decide whether to hard-fail or fall through.
    Results are cached to avoid repeated imports/attribute lookups.
    """
    if resource_type in _MODEL_CACHE:
        return _MODEL_CACHE[resource_type]
    if resource_type not in FHIR_REGISTRY:
        _MODEL_CACHE[resource_type] = None
        return None
    # Triggers lazy loading of the model
    from pymedplum import fhir

    model = getattr(fhir, resource_type, None)
    _MODEL_CACHE[resource_type] = model
    return model


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
        "MCP server for a Medplum FHIR server. "
        #
        # Discovery workflow
        "Workflow: use get_resource_schema to learn a resource type's fields "
        "(also useful for nested types like Reference, CodeableConcept, "
        "Identifier, HumanName). Use get_resource_capabilities to discover "
        "likely supported search parameters — note that the CapabilityStatement "
        "describes what the server advertises, but actual support may vary; "
        "if a search fails, inspect the error and adjust. "
        #
        # Searching
        "For searching: prefer targeted queries over broad retrieval. "
        "search_one only when uniqueness is guaranteed by a stable identifier "
        "— do not assume uniqueness from names or demographics alone. "
        "search_resources for paginated results. "
        "search_all_resources only when the result set is known to be small "
        "or tightly constrained — clinical data types like Observation, "
        "AuditEvent, and Encounter grow very large. "
        "Prefer normal FHIR search/read over execute_graphql unless GraphQL "
        "is clearly better for shaping a multi-hop read. "
        #
        # Identity safety
        "For Patient, Practitioner, RelatedPerson, and Organization, prefer "
        "identifier-based lookup over name-based matching. "
        #
        # Writes
        "Read before write: before patch_resource, update_resource, or "
        "delete_resource, read the resource first unless the exact resource "
        "ID and intended change are already unambiguous. "
        "For writes: prefer create_resource_if_none_exist (with stable "
        "business identifiers in if_none_exist) over create_resource to "
        "avoid duplicates. Use patch_resource for partial field changes, "
        "update_resource only when replacing the full resource. "
        #
        # Terminology
        "Terminology tools (validate_code, expand_valueset, lookup_concept, "
        "translate_concept) wrap standard FHIR terminology operations. "
        "execute_operation is the escape hatch for any FHIR $operation not "
        "covered by a dedicated tool. "
        #
        # Safety
        "Inspect first, modify only when asked. Use write tools only when "
        "explicitly requested by the user. Bot execution and deployment are "
        "high-impact operations — only run them when the user explicitly asks."
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
    if on_behalf_of is not None:
        # Explicit (even empty) — validate so misconfiguration fails loudly.
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
    """Get the JSON schema for a FHIR resource or data type — field names,
    types, enums, descriptions, and constraints.

    Use this before create_resource or update_resource to understand what
    fields a resource type expects. Works for FHIR R4 resource types (e.g.,
    Patient, Observation), data types (e.g., HumanName, CodeableConcept),
    and Medplum-specific types (e.g., Bot, ProjectMembership).

    For search parameters (what to pass to search_resources), use
    get_resource_capabilities instead.

    By default, nested type definitions ($defs) are stripped for
    compactness. The schema still shows $ref pointers — call this tool
    again with those type names to drill into child types.

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
    """Search for FHIR resources. Returns one page of results in a Bundle.

    If you don't know valid search parameters for a resource type, call
    get_resource_capabilities(resource_type) first.

    Use search_one instead when you expect exactly one result.
    Use search_all_resources when you need every match across all pages
    (warning: can return very large result sets).

    Args:
        resource_type: FHIR resource type to search (e.g., "Patient",
            "Observation", "Condition")
        params: FHIR search parameters as key-value pairs. Values are
            strings. Use FHIR prefixes for comparisons (e.g., "ge", "le").
            Use modifiers in the key (e.g., "family:exact").
            List values become repeated params (OR semantics).
            E.g. {"family": "Smith"},
            {"patient": "Patient/123", "code": "29463-7"},
            {"status": "active", "date": "ge2024-01-01"},
            {"status": ["active", "completed"]} for OR search,
            {"family:exact": "Smith"} for modifier
        count: Maximum results per page (default: server default, usually 20)
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

    Uses _count=1 internally and returns the first match, or null if none
    found. If multiple resources could match, only the first is returned
    with no warning — use search_resources if you need to verify uniqueness.

    Only use this when the query is expected to be unique by a stable
    identifier or other strong uniqueness constraint. Do not assume
    uniqueness from names or demographics alone — in healthcare, near-
    matches are common and grabbing the first result silently can be
    dangerous.

    Args:
        resource_type: FHIR resource type to search (e.g., "Patient")
        params: FHIR search parameters as key-value pairs.
            Examples: {"identifier": "http://example.org|12345"},
            {"family": "Smith", "given": "Alice"} (use with caution —
            may match multiple)
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
    """Search across ALL pages and return every match in a single Bundle.

    Automatically follows pagination links until exhausted. Avoid unless
    the result set is known to be small or tightly constrained. Clinical
    data types like Observation, AuditEvent, Communication, Encounter,
    DiagnosticReport, and Provenance grow very large — an unconstrained
    search can return thousands of resources and blow through context.

    Prefer search_resources with count/offset for paginated browsing.

    Args:
        resource_type: FHIR resource type to search
        params: FHIR search parameters as key-value pairs. Should be
            tightly constrained (e.g., scoped to a single patient +
            date range + category)
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Bundle with all matching resources flattened into entries
    """
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

    If the resource should be unique (e.g., by identifier), prefer
    create_resource_if_none_exist to avoid duplicates.

    Use get_resource_schema(resource_type) to see valid fields before
    constructing the resource.

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

    Uses FHIR conditional create (If-None-Exist header). The server checks
    atomically — safer than a search-then-create sequence. If a match is
    found, returns the existing resource without creating a duplicate.

    Prefer this over create_resource when the resource should be unique
    (e.g., a Patient with a specific identifier).

    Args:
        resource: FHIR resource dict with "resourceType". Same format as
            create_resource.
        if_none_exist: Search query string (same syntax as search params,
            without a leading "?"). The server searches for existing matches
            using this query before creating. Use stable business identifiers
            whenever possible — loose demographic matching (name, DOB) can
            match too broadly or too narrowly.
            Good: "identifier=http://example.org|12345"
            Risky: "name=Smith&birthdate=2000-01-01"
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        The created or existing resource
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
    """Replace an existing FHIR resource on the Medplum server (HTTP PUT).

    This is a full replacement — omitted fields may be cleared. Do not
    construct the resource from memory. Always read the current resource
    first with read_resource, modify the needed fields, then pass the
    complete object here. For changing specific fields without sending
    the full resource, use patch_resource instead.

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

    Partial update using JSON Patch (RFC 6902). Preferred over
    update_resource when you only need to change specific fields.

    For complex nested arrays (name, telecom, identifier, address),
    read the resource first to determine correct array indices — blindly
    patching by index can target the wrong element.

    JSON Pointer examples:
        "/active" — root boolean field
        "/name/0/family" — first name entry, family field
        "/telecom/1/value" — second telecom entry, value
        "/identifier/-" — append to identifier array

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

    raw_ops = [op.model_dump(exclude_unset=True, by_alias=True) for op in operations]
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
    """Discover likely supported search parameters and operations for a resource type.

    Almost always pass resource_type — the full CapabilityStatement is very
    large and rarely useful. The filtered response shows searchParam names,
    supported interactions, and available operations for that type.

    Note: the CapabilityStatement describes what the server advertises, but
    actual support for modifiers, chained search, composite params, and
    custom operations may vary. If a search using an advertised param fails,
    inspect the error and adjust.

    Use this before search_resources if you're unsure what search parameters
    exist. For field definitions (what to pass to create/update), use
    get_resource_schema instead.

    Args:
        resource_type: FHIR resource type to get capabilities for (e.g.,
            "Patient", "Observation"). Strongly recommended. If omitted,
            returns the full CapabilityStatement (very large).

    Returns:
        Resource capability details (searchParam, interaction, operation),
        or full CapabilityStatement if resource_type is omitted
    """
    # Intentionally uses the raw client: /metadata is unauthenticated server
    # metadata and has no meaningful on_behalf_of semantics.
    client = await _get_client()
    fhir_url_path = os.getenv("MEDPLUM_FHIR_URL_PATH", "fhir/R4/")
    normalized_path = f"{fhir_url_path.strip('/')}/" if fhir_url_path.strip("/") else ""
    result = await client.get(f"{normalized_path}metadata")

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

    Useful for exploring a patient's chart or building a clinical summary.
    Can be expensive and return a large result set for patients with long
    histories. For targeted retrieval (e.g., recent labs, active
    medications), prefer search_resources scoped to the patient instead.

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
    on_behalf_of: str | None = None,
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
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Parameters resource indicating if the code is valid, with
        result (boolean) and optional display text
    """
    async with _with_obo(on_behalf_of) as client:
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
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Check if a code exists in a CodeSystem (not a ValueSet).

    Unlike validate_code which checks ValueSet membership, this checks
    whether a code is defined in a CodeSystem itself.

    Provide either (code + codesystem_url) or (coding) to identify
    what to validate.

    Args:
        code: The code to validate (e.g., "12345")
        codesystem_url: CodeSystem canonical URL (e.g., "http://loinc.org")
        codesystem_id: ID of a specific CodeSystem resource (alternative
            to codesystem_url)
        coding: A FHIR Coding object as a dict, e.g.,
            {"system": "http://loinc.org", "code": "12345"}. Alternative
            to passing code + codesystem_url separately.
        version: Specific CodeSystem version to validate against
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Parameters resource with result (boolean) and display
    """
    async with _with_obo(on_behalf_of) as client:
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
    on_behalf_of: str | None = None,
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
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        ValueSet resource with expansion containing matching codes
    """
    async with _with_obo(on_behalf_of) as client:
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
    on_behalf_of: str | None = None,
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
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Parameters resource with code details (display, definition, properties)
    """
    async with _with_obo(on_behalf_of) as client:
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
    on_behalf_of: str | None = None,
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
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        Parameters resource with translation matches
    """
    async with _with_obo(on_behalf_of) as client:
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
        "readOnlyHint": False,
        "destructiveHint": True,
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
    """Execute a FHIR $operation not covered by a dedicated tool.

    Escape hatch for any standard or custom FHIR operation. Prefer the
    dedicated tools when they exist:
    - Patient $everything → get_patient_everything
    - ValueSet $validate-code → validate_code
    - CodeSystem $validate-code → validate_codesystem_code
    - CodeSystem $lookup → lookup_concept
    - ValueSet $expand → expand_valueset
    - ConceptMap $translate → translate_concept

    Supports type-level (e.g., Patient/$match) and instance-level
    (e.g., Patient/123/$everything) operations.

    In read-only mode, only known read-only operations are allowed.

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        operation: Operation name without $ prefix (e.g., "everything", "match")
        resource_id: Resource ID for instance-level operations
        params: Key-value dict. For POST, automatically wrapped into a FHIR
            Parameters resource (works for simple scalar params like
            {"weight": 70, "unit": "kg"}). For operations needing nested
            Parameters, resources, or repeated parts, pass the full FHIR
            Parameters structure directly. For GET, converted to query
            parameters
        method: HTTP method — use GET for simple lookups, POST (default)
            for complex params
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

    Prefer normal FHIR search/read unless GraphQL is clearly better —
    e.g., traversing resource references or fetching specific fields
    across multiple resource types in a single request. Medplum's
    GraphQL endpoint is read-only (queries only, no mutations).

    Args:
        query: GraphQL query string. Example:
            '{ Patient(id: "123") { name { given family } birthDate } }'
        variables: Optional GraphQL variables
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        GraphQL response
    """
    if _is_read_only() and re.search(r"\bmutation\b", query, re.IGNORECASE):
        msg = (
            "GraphQL mutations are blocked in read-only mode (MEDPLUM_READ_ONLY=true)."
        )
        raise PermissionError(msg)

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
    """Export a patient's clinical history as a C-CDA (Consolidated CDA) XML document.

    C-CDA is a standard clinical document format used for health information
    exchange. Returns the raw XML string in a wrapper dict.
    """
    async with _with_obo(on_behalf_of) as client:
        ccda_xml = await client.export_ccda(patient_id)
    return {
        "format": "ccda",
        "contentType": "application/xml",
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
    """Execute a deployed Medplum Bot, passing input_data as its trigger payload.

    HIGH-IMPACT: Bots are arbitrary server-side code that can read, write,
    and delete FHIR resources, send communications, and trigger other
    workflows. Only execute a bot when the user explicitly asks, and only
    when you know what the bot does.

    The bot must already be deployed via save_and_deploy_bot. The bot's
    code receives input_data and can read/write FHIR resources on the server.
    """
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
    """Create a Medplum Bot (server-side JavaScript/TypeScript function).

    Bots are Medplum-specific resources that execute code on the server.
    You must set runtime_version for the bot to be executable:
    - "awslambda": runs on AWS Lambda (most common, required for production)
    - "vmcontext": runs in a VM sandbox (useful for development/testing)

    After creating a bot, use save_and_deploy_bot to upload and deploy code.
    """
    _check_write_allowed()
    extras = dict(additional_fields or {})
    # Prevent silent overrides of explicit arguments via additional_fields.
    reserved = {"name", "description", "source_code", "runtime_version"}
    collisions = reserved & extras.keys()
    if collisions:
        msg = (
            f"additional_fields cannot override explicit arguments: "
            f"{sorted(collisions)}. Pass these via their named parameters."
        )
        raise ValueError(msg)
    async with _with_obo(on_behalf_of) as client:
        result = await client.create_bot(
            name=name,
            description=description,
            source_code=source_code,
            runtime_version=runtime_version,
            **extras,
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
    """Save bot source code and deploy compiled code in one step.

    HIGH-IMPACT: Deployment replaces the live bot code immediately. Only
    deploy when the user explicitly asks to create or update bot code.

    Both `source_code` and `compiled_code` must be provided by the caller.
    This tool does not compile source — the caller (e.g. a build step in the
    host environment) is expected to run the TypeScript/JavaScript compiler
    and pass the resulting JS as `compiled_code`. The `source_code` is
    stored on the Bot for reference; `compiled_code` is what actually runs
    in the Medplum bot runtime.
    """
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

    Entry structure example::

        {"type": "transaction", "entry": [
            {"request": {"method": "POST", "url": "Patient"},
             "resource": {"resourceType": "Patient", "name": [...]}},
            {"request": {"method": "GET", "url": "Patient/123"}},
            {"request": {"method": "PUT", "url": "Patient/456"},
             "resource": {"resourceType": "Patient", "id": "456", ...}}
        ]}

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


@mcp.tool(
    annotations={
        "title": "Raw Medplum HTTP Request",
        "readOnlyHint": False,
        "destructiveHint": True,
    }
)
async def raw_request(
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    path: str,
    body: dict[str, Any] | list[Any] | None = None,
    query_params: list[list[str]] | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Send an authenticated HTTP request to any Medplum endpoint.

    Low-level escape hatch when no dedicated tool covers the endpoint.
    Prefer the dedicated tools (read_resource, search_resources,
    create_resource, execute_operation, etc.) for standard FHIR
    operations — they provide validation, response annotation, and
    better error messages.

    Use this for non-FHIR Medplum endpoints (admin, project management,
    bulk data, $reindex), FHIR interactions not covered by dedicated
    tools (_history, conditional update with custom headers), or
    endpoints discovered from Medplum documentation.

    The path is appended to the server's base URL. Do not include the
    base URL itself.

    Args:
        method: HTTP method
        path: Endpoint path relative to the base URL. Do not include
            a leading slash — the base URL already ends with one.
            FHIR examples: "fhir/R4/Patient/123/_history",
            "fhir/R4/Patient?_summary=count"
            Non-FHIR examples: "admin/projects/123",
            "auth/me", "fhir/R4/$reindex"
        body: Optional JSON request body (for POST, PUT, PATCH)
        query_params: Optional query parameters as a list of [key, value]
            pairs. A list of pairs (not a dict) because FHIR and Medplum
            endpoints often need repeated keys, e.g.,
            [["_include", "Observation:subject"],
            ["_include", "Observation:performer"],
            ["status", "active"]]
        on_behalf_of: Optional ProjectMembership ID to execute as

    Returns:
        The parsed JSON response from the server
    """
    if method in ("POST", "PUT", "PATCH", "DELETE"):
        _check_write_allowed()

    async with _with_obo(on_behalf_of) as client:
        url = f"{client.base_url}{path}"
        kwargs: dict[str, Any] = {}
        if body is not None:
            kwargs["json"] = body
        if query_params:
            kwargs["params"] = [(k, v) for k, v in query_params]
        result = await client._request(method, url, **kwargs)

    return result or {}


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


@mcp.resource("medplum://tool-guide")
async def tool_guide() -> str:
    """Quick reference for choosing the right tool."""
    return (
        "DISCOVER:\n"
        "  Field definitions     → get_resource_schema\n"
        "  Search parameters     → get_resource_capabilities\n"
        "\n"
        "READ:\n"
        "  Known ID              → read_resource\n"
        "  Find by identifier    → search_one (only if unique)\n"
        "  Find multiple         → search_resources (paginated)\n"
        "  Get everything        → search_all_resources (small sets only)\n"
        "  Patient full record   → get_patient_everything\n"
        "  GraphQL multi-hop     → execute_graphql\n"
        "\n"
        "WRITE (only when user asks):\n"
        "  Create (idempotent)   → create_resource_if_none_exist (preferred)\n"
        "  Create (simple)       → create_resource\n"
        "  Change some fields    → patch_resource (read first)\n"
        "  Replace entire        → update_resource (read first)\n"
        "  Remove                → delete_resource (read first)\n"
        "  Batch/transaction     → execute_batch\n"
        "\n"
        "TERMINOLOGY:\n"
        "  Check ValueSet membership  → validate_code\n"
        "  Check CodeSystem existence → validate_codesystem_code\n"
        "  List codes in ValueSet     → expand_valueset\n"
        "  Code meaning/display       → lookup_concept\n"
        "  Map between systems        → translate_concept\n"
        "\n"
        "ESCAPE HATCHES:\n"
        "  Any FHIR $operation   → execute_operation\n"
        "  Any Medplum endpoint  → raw_request (last resort)\n"
        "\n"
        "BOTS (high-impact, explicit user request only):\n"
        "  Create bot            → create_bot\n"
        "  Deploy code           → save_and_deploy_bot\n"
        "  Run bot               → execute_bot\n"
    )


@mcp.resource("medplum://common-errors")
async def common_errors() -> dict[str, str]:
    """Common FHIR/Medplum error codes and what to do about them."""
    return {
        "400 Bad Request": (
            "Validation failed. Check field names and types with "
            "get_resource_schema. Check search params with "
            "get_resource_capabilities."
        ),
        "401 Unauthorized": (
            "Authentication failed. Check MEDPLUM_CLIENT_ID and MEDPLUM_CLIENT_SECRET."
        ),
        "403 Forbidden": (
            "Access denied. Check on_behalf_of ProjectMembership permissions."
        ),
        "404 Not Found": (
            "Resource doesn't exist, was deleted, or you lack access. "
            "Try search_resources instead of read_resource."
        ),
        "409 Conflict": (
            "Version mismatch — resource was modified since you read it. "
            "Read the resource again and retry."
        ),
        "410 Gone": "Resource was soft-deleted on Medplum.",
        "429 Too Many Requests": (
            "Rate limited. The client retries automatically with backoff."
        ),
    }


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
