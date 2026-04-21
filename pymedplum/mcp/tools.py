"""MCP tool functions for Medplum FHIR operations.

All tools are registered on the shared ``mcp`` FastMCP instance from
``server.py`` via ``@mcp.tool()`` decorators.
"""

from __future__ import annotations

import os
from collections import Counter
from typing import TYPE_CHECKING, Any, Literal, cast

try:
    from mcp.types import ToolAnnotations
except ImportError:
    # Optional ``mcp`` extra not installed; server.py's FastMCP shim ignores
    # ``annotations=`` so a no-op stub keeps the module importable.
    class ToolAnnotations:  # type: ignore[no-redef]
        """No-op stub used when the ``mcp`` extra isn't installed."""

        def __init__(self, **_kwargs: Any) -> None:
            pass


from pymedplum._security import build_raw_request_url
from pymedplum.fhir import FHIR_TYPES
from pymedplum.mcp.server import (
    _READ_ONLY_OPERATIONS,
    BundleInput,
    PatchOp,
    _annotate_response,
    _check_bot_allowed,
    _check_write_allowed,
    _collect_refs,
    _get_client,
    _get_fhir_model,
    _is_read_only,
    _validate_resource,
    _with_obo,
    mcp,
)
from pymedplum.types import (  # noqa: TC001 — runtime use by FastMCP schema generation
    SummaryMode,
    TotalMode,
)

if TYPE_CHECKING:
    from pymedplum.types import PatchOperation


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get FHIR Resource Schema",
        readOnlyHint=True,
    )
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
        available = sorted(FHIR_TYPES)
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

        compact["_common_mistakes"] = (
            "FHIR types are NOT plain strings. Common errors: "
            'Reference: use {"reference": "Patient/123"}, NOT "Patient/123". '
            'CodeableConcept: use {"coding": [{"system": "...", "code": "..."}]}, NOT "12345". '
            'HumanName: use [{"given": ["Alice"], "family": "Smith"}], NOT "Alice Smith". '
            'Identifier: use [{"system": "...", "value": "..."}], NOT "12345". '
            'ContactPoint: use [{"system": "phone", "value": "555-1212"}], NOT "555-1212". '
            'Quantity: use {"value": 120, "unit": "mmHg", "system": "http://unitsofmeasure.org"}, NOT 120. '
            "Check _referenced_types and drill into any type "
            "you are not 100% certain about."
        )

        return compact

    return schema


@mcp.tool(
    annotations=ToolAnnotations(
        title="Read FHIR Resource",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID or reference
            (e.g., "ProjectMembership/<uuid>" or just "<uuid>").
            Executes the request as that project member.

    Returns:
        The FHIR resource as a JSON object
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.read_resource(resource_type, resource_id)
    return _annotate_response(result)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Search FHIR Resources",
        readOnlyHint=True,
    )
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
    get_resource_capabilities(resource_type) first. Search parameter
    names are NOT resource field paths — use params from the
    CapabilityStatement (e.g., "family", "identifier"), not guessed
    field names from the schema.

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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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

    if not isinstance(result, dict):
        msg = "search_with_options returned unexpected type"
        raise TypeError(msg)

    if result.get("total") == 0:
        result["_hint"] = (
            f"No results found. Use get_resource_capabilities('{resource_type}') "
            f"to see valid search parameters for {resource_type}."
        )
    result["_schema_hint"] = (
        f"Search results show only populated fields. BEFORE creating "
        f"or modifying a {resource_type}, call "
        f"get_resource_schema('{resource_type}') to see all required "
        f"fields, types, and constraints."
    )

    return result


@mcp.tool(
    annotations=ToolAnnotations(
        title="Search Single FHIR Resource",
        readOnlyHint=True,
    )
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

    If you're unsure what search parameters are available, call
    get_resource_capabilities(resource_type) first.

    Args:
        resource_type: FHIR resource type to search (e.g., "Patient")
        params: FHIR search parameters as key-value pairs.
            Examples: {"identifier": "http://example.org|12345"},
            {"family": "Smith", "given": "Alice"} (use with caution —
            may match multiple)
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        The matching FHIR resource, or null if no match found
    """
    async with _with_obo(on_behalf_of) as client:
        result = await client.search_one(resource_type, params)
    if result is None:
        return None
    return _annotate_response(result)


_DEFAULT_MAX_RESOURCES = 50


@mcp.tool(
    annotations=ToolAnnotations(
        title="Search All FHIR Resources",
        readOnlyHint=True,
    )
)
async def search_all_resources(
    resource_type: str,
    params: dict[str, Any] | None = None,
    max_resources: int = _DEFAULT_MAX_RESOURCES,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Search across ALL pages and return every match in a single Bundle.

    Automatically follows pagination links until the limit is reached.
    Defaults to 50 resources max. Clinical data types like Observation,
    AuditEvent, and Encounter can have thousands of records — always
    constrain your search params tightly.

    Prefer search_resources with count/offset for paginated browsing.

    If you're unsure what search parameters are available, call
    get_resource_capabilities(resource_type) first.

    Args:
        resource_type: FHIR resource type to search
        params: FHIR search parameters as key-value pairs. Should be
            tightly constrained (e.g., scoped to a single patient +
            date range + category)
        max_resources: Maximum number of resources to return (default
            50). Set higher only if you are certain the result set is
            bounded.
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        Bundle with matching resources. If truncated, includes
        _truncated flag and _total_available count.
    """
    resources: list[dict[str, Any]] = []
    truncated = False
    async with _with_obo(on_behalf_of) as client:
        async for resource in client.search_resource_pages(resource_type, params):
            resources.append(resource)
            if len(resources) >= max_resources:
                truncated = True
                break

    result: dict[str, Any] = {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [{"resource": resource} for resource in resources],
        "total": len(resources),
        "_pages_mode": "all",
        "_resources_returned": len(resources),
    }
    if truncated:
        result["_truncated"] = True
        result["_warning"] = (
            f"Results truncated at {max_resources} resources. "
            f"Use search_resources with count/offset for paginated "
            f"access, or pass a higher max_resources if you are "
            f"certain you need more."
        )
    if not resources:
        result["_hint"] = (
            f"No results found. Use get_resource_capabilities('{resource_type}') "
            f"to see valid search parameters for {resource_type}."
        )
    result["_schema_hint"] = (
        f"WARNING: This is patient data. Search results show only "
        f"populated fields, NOT the full schema. Do NOT use these "
        f"results to infer field names or types for writes. You MUST "
        f"call get_resource_schema('{resource_type}') before any "
        f"create, update, or patch — malformed writes corrupt patient "
        f"records."
    )

    return result


@mcp.tool(
    annotations=ToolAnnotations(
        title="Create FHIR Resource",
        readOnlyHint=False,
        destructiveHint=False,
    )
)
async def create_resource(
    resource: dict[str, Any],
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Create a new FHIR resource on the Medplum server.

    If the resource should be unique (e.g., by identifier), prefer
    create_resource_if_none_exist to avoid duplicates.

    REQUIRED PREREQUISITE: call get_resource_schema(resource_type)
    before calling this tool. This server stores protected health
    information (PHI). Medplum extends and diverges from FHIR R4 —
    your training data is not reliable. Malformed resources risk
    corrupting patient records.

    Args:
        resource: Complete FHIR resource as a JSON object. Must include
            "resourceType". Example:
            {"resourceType": "Patient", "name": [{"given": ["Alice"], "family": "Smith"}]}
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Create FHIR Resource If None Exist",
        readOnlyHint=False,
        destructiveHint=False,
    )
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

    REQUIRED PREREQUISITES (both mandatory):
    1. call get_resource_schema(resource_type) to verify field names
       and types — Medplum diverges from FHIR R4.
    2. call get_resource_capabilities(resource_type) to verify valid
       search parameter names for the if_none_exist query — guessing
       param names (e.g., "name" vs "family") causes silent mismatches.

    This server stores protected health information (PHI). Malformed
    resources or bad search criteria risk duplicating or corrupting
    patient records.

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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Update FHIR Resource",
        readOnlyHint=False,
        destructiveHint=True,
    )
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

    REQUIRED PREREQUISITE: call get_resource_schema(resource_type)
    before calling this tool. This server stores protected health
    information (PHI). Medplum extends and diverges from FHIR R4 —
    your training data is not reliable. Malformed resources risk
    corrupting patient records.

    Args:
        resource: Complete FHIR resource with "resourceType" and "id".
            All fields should be included, not just changed ones.
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Patch FHIR Resource",
        readOnlyHint=False,
        destructiveHint=True,
    )
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

    REQUIRED PREREQUISITES (both mandatory):
    1. call get_resource_schema(resource_type) to verify field names
       and types — Medplum diverges from FHIR R4.
    2. call read_resource(resource_type, resource_id) to see the
       current state — you cannot construct a correct patch without
       knowing what fields and array entries already exist.

    This server stores protected health information (PHI). Patching
    without reading first risks targeting wrong array indices,
    replacing values that don't exist, or corrupting patient records.

    JSON Pointer examples:
        "/active" — root boolean field
        "/name/0/family" — first name entry, family field
        "/telecom/1/value" — second telecom entry, value
        "/identifier/-" — append to identifier array

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        resource_id: Resource ID to patch
        operations: List of JSON Patch operations
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        The patched resource
    """
    _check_write_allowed()
    if not operations:
        msg = "At least one patch operation is required."
        raise ValueError(msg)

    raw_ops = [
        cast("PatchOperation", op.model_dump(exclude_unset=True, by_alias=True))
        for op in operations
    ]
    async with _with_obo(on_behalf_of) as client:
        result = await client.patch_resource(resource_type, resource_id, raw_ops)
    return _annotate_response(result)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Delete FHIR Resource",
        readOnlyHint=False,
        destructiveHint=True,
    )
)
async def delete_resource(
    resource_type: str,
    resource_id: str,
    on_behalf_of: str | None = None,
) -> dict[str, str]:
    """Delete a FHIR resource from the Medplum server.

    DESTRUCTIVE: This server stores protected health information (PHI).
    Even though Medplum soft-deletes, the resource immediately
    disappears from search results and references to it may break,
    potentially disrupting clinical workflows. Only delete when the
    user explicitly asks. Always read_resource first to confirm you
    have the correct resource.

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        resource_id: Resource ID to delete
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Get FHIR Capabilities",
        readOnlyHint=True,
    )
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
                if isinstance(r, dict) and r.get("type") == resource_type:
                    r["_search_syntax"] = (
                        "FHIR search param names are NOT resource field "
                        "names (e.g., field is 'name' but search params "
                        "are 'family', 'given'). Use the searchParam list "
                        "above, not get_resource_schema field names. "
                        "Values are also NOT plain strings: "
                        'dates need prefixes {"date": "ge2024-01-01"}, '
                        "tokens need system|code "
                        '{"code": "http://loinc.org|12345"}, '
                        "references use Resource/ID "
                        '{"subject": "Patient/123"}. '
                        "Omitting prefixes or systems causes silent "
                        "zero-result searches."
                    )
                    return r
        msg = f"Resource type '{resource_type}' not found in CapabilityStatement"
        raise ValueError(msg)

    return result


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Patient Everything",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Validate Code in ValueSet",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Validate Code in CodeSystem",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Expand ValueSet",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Lookup Code in CodeSystem",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Translate Code Between Systems",
        readOnlyHint=True,
    )
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
        on_behalf_of: Optional ProjectMembership UUID to execute as

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
    annotations=ToolAnnotations(
        title="Execute FHIR Operation",
        readOnlyHint=False,
        destructiveHint=True,
    )
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
        params: For POST with simple scalar params, pass a plain dict like
            {"weight": 70, "unit": "kg"} — it will be auto-wrapped into a
            FHIR Parameters resource. For operations needing nested parts,
            embedded resources, or repeated parameters, pass the full FHIR
            Parameters structure directly (with "resourceType": "Parameters").
            Do NOT pass an already-wrapped Parameters resource as a plain
            dict — it will be double-wrapped. For GET, params are converted
            to query parameters
        method: HTTP method — use GET for simple lookups, POST (default)
            for complex params
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        Operation response (typically Parameters or Bundle)
    """
    op_name = operation.lstrip("$").lower()

    if _is_read_only() and op_name not in _READ_ONLY_OPERATIONS:
        msg = (
            f"Operation '${operation}' is not in the read-only allowlist. "
            f"Server is in read-only mode; set MEDPLUM_ENABLE_WRITES=true "
            f"to enable write-capable operations. "
            f"Allowed in read-only mode: "
            f"{', '.join(sorted('$' + o for o in _READ_ONLY_OPERATIONS))}"
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
    annotations=ToolAnnotations(
        title="Execute GraphQL Query",
        readOnlyHint=False,
        destructiveHint=True,
    )
)
async def execute_graphql(
    query: str,
    variables: dict[str, Any] | None = None,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a FHIR GraphQL query (or mutation) against the Medplum server.

    Treated as a write-capable tool: GraphQL queries are arbitrary text and
    cannot be reliably distinguished from mutations or subscription requests
    without a full parser. Rather than attempting per-query gating, this tool
    is blocked entirely in read-only mode (the default) and is unrestricted
    once the operator opts into writes via ``MEDPLUM_ENABLE_WRITES=true``.

    Prefer normal FHIR search/read unless GraphQL is clearly better —
    e.g., traversing resource references or fetching specific fields
    across multiple resource types in a single request.

    Args:
        query: GraphQL query string. Example:
            '{ Patient(id: "123") { name { given family } birthDate } }'
        variables: Optional GraphQL variables
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        GraphQL response
    """
    _check_write_allowed()
    async with _with_obo(on_behalf_of) as client:
        result = await client.execute_graphql(query, variables)
    return _annotate_response(result)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Execute Medplum Bot",
        readOnlyHint=False,
        destructiveHint=True,
    )
)
async def execute_bot(
    bot_id: str,
    input_data: dict[str, Any],
    content_type: str = "application/json",
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a deployed Medplum Bot, passing input_data as its trigger payload.

    HIGH-IMPACT: This server stores protected health information (PHI).
    Bots are arbitrary server-side code that can read, write, and delete
    patient records, send communications, and trigger clinical workflows.
    Only execute a bot when the user explicitly asks, and only when you
    know what the bot does.

    Operators can restrict which bots an LLM may invoke by setting
    ``MEDPLUM_ALLOWED_BOT_IDS=uuid1,uuid2`` — the curated set acts as a
    safety net even when writes are enabled.

    The bot must already be deployed via save_and_deploy_bot. The bot's
    code receives input_data and can read/write FHIR resources on the server.
    """
    _check_write_allowed()
    _check_bot_allowed(bot_id)
    async with _with_obo(on_behalf_of) as client:
        result = await client.execute_bot(bot_id, input_data, content_type=content_type)
    return _annotate_response(result)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Create Medplum Bot",
        readOnlyHint=False,
        destructiveHint=False,
    )
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

    REQUIRED PREREQUISITE if passing additional_fields: call
    get_resource_schema('Bot') first. Bot is a Medplum-specific
    resource not in FHIR R4 — your training data is not reliable.
    """
    _check_write_allowed()
    extras = dict(additional_fields or {})
    # Prevent silent overrides of explicit arguments via additional_fields.
    reserved = {
        "name",
        "description",
        "source_code",
        "runtime_version",
        # SDK key names (create_bot maps these from the params above)
        "code",
        "runtimeVersion",
    }
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
    annotations=ToolAnnotations(
        title="Save And Deploy Medplum Bot",
        readOnlyHint=False,
        destructiveHint=True,
    )
)
async def save_and_deploy_bot(
    bot_id: str,
    source_code: str,
    compiled_code: str,
    filename: str = "index.js",
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Save bot source code and deploy compiled code in one step.

    HIGH-IMPACT: This server stores protected health information (PHI).
    Deployment replaces the live bot code immediately — deployed bots
    can modify patient records. Only deploy when the user explicitly
    asks to create or update bot code.

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
    annotations=ToolAnnotations(
        title="Execute FHIR Batch or Transaction",
        readOnlyHint=False,
        destructiveHint=True,
    )
)
async def execute_batch(
    bundle: BundleInput,
    on_behalf_of: str | None = None,
) -> dict[str, Any]:
    """Execute a FHIR batch or transaction bundle on the Medplum server.

    This server stores protected health information (PHI). Bundles can
    create, update, and delete multiple patient records in a single
    call. Construct with care.

    REQUIRED PREREQUISITE: call get_resource_schema(resource_type) for
    every resource type included in the bundle entries. Medplum diverges
    from FHIR R4 — your training data is not reliable for field names
    or types. For entries that write resources, the same schema and
    validation rules apply as create_resource and update_resource.

    Batch vs transaction:
    - "batch": each entry processed independently (some may fail while
      others succeed)
    - "transaction": atomic (all succeed or all fail, with rollback)

    Entry structure — each entry needs a "request" with "method" and
    "url", plus a "resource" for writes::

        {"type": "transaction", "entry": [
            {"request": {"method": "POST", "url": "Patient"},
             "resource": {"resourceType": "Patient", "name": [...]}},
            {"request": {"method": "GET", "url": "Patient/123"}},
            {"request": {"method": "PUT", "url": "Patient/456"},
             "resource": {"resourceType": "Patient", "id": "456", ...}}
        ]}

    Common mistakes:
    - request.url MUST be relative (e.g., "Patient", "Patient/123"),
      NOT full absolute server URLs
    - PUT entries MUST include "id" in the resource body
    - POST entries MUST NOT include "id" (server assigns it)
    - Resources inside entries follow the same schema rules as
      create_resource / update_resource — do not guess field shapes

    In read-only mode, bundles containing only GET requests are allowed
    (including transactions). Bundles with any write methods (POST, PUT,
    PATCH, DELETE) are blocked.

    Args:
        bundle: FHIR Bundle with type "batch" or "transaction"
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        Response Bundle with one entry per input, each containing a
        response with status code and (for reads/creates) the resource
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
    annotations=ToolAnnotations(
        title="Raw Medplum HTTP Request",
        readOnlyHint=False,
        destructiveHint=True,
    )
)
async def raw_request(
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    path: str,
    body: dict[str, Any] | list[Any] | None = None,
    query_params: list[list[str]] | None = None,
    on_behalf_of: str | None = None,
) -> Any:
    """Send an authenticated HTTP request to any Medplum endpoint.

    DANGEROUS: This tool bypasses all schema validation, response
    annotation, and safety checks provided by the dedicated tools.
    Incorrect paths, methods, or body structures can silently corrupt
    or delete patient data with no client-side guardrails. This server
    stores protected health information (PHI).

    LAST RESORT ONLY. Do not use this to reimplement standard
    read/search/create/update/delete flows — use the dedicated tools.
    If a dedicated tool failed, fix the inputs to that tool instead of
    dropping to raw_request.

    Use this only for non-FHIR Medplum endpoints (admin, project
    management, bulk data, $reindex), FHIR interactions not covered
    by dedicated tools (_history, conditional update with custom
    headers), or endpoints discovered from Medplum documentation.

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
        on_behalf_of: Optional ProjectMembership UUID to execute as

    Returns:
        The parsed JSON response from the server
    """
    if method in ("POST", "PUT", "PATCH", "DELETE"):
        _check_write_allowed()

    async with _with_obo(on_behalf_of) as client:
        url = build_raw_request_url(client.base_url, path)
        kwargs: dict[str, Any] = {}
        if body is not None:
            kwargs["json"] = body
        if query_params:
            kwargs["params"] = [(k, v) for k, v in query_params]
        result = await client._request(method, url, **kwargs)

    return result if result is not None else {}
