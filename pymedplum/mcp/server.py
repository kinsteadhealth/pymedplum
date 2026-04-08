"""MCP server for Medplum FHIR operations.

Core module: FastMCP instance, client lifecycle, helpers, models, and main().
Tool functions live in tools.py, MCP resources in resources.py.

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
from contextlib import asynccontextmanager
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from pymedplum import AsyncMedplumClient
from pymedplum.fhir import REGISTRY as FHIR_REGISTRY

# ---------------------------------------------------------------------------
# FastMCP instance (with fallback shim when mcp extras aren't installed)
# ---------------------------------------------------------------------------

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
            """No-op decorator when MCP extras are unavailable."""

            def decorator(func):
                return func

            return decorator

        def resource(self, *_args: Any, **_kwargs: Any):
            """No-op decorator when MCP extras are unavailable."""

            def decorator(func):
                return func

            return decorator

        def run(self) -> None:
            """Raise a helpful error when launched without MCP extras."""
            msg = (
                "Error: The 'mcp' package is required but not installed.\n"
                "Install it with: pip install 'pymedplum[mcp]'"
            )
            raise RuntimeError(msg) from _MCP_IMPORT_ERROR


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
        "MCP server for a Medplum FHIR server. Medplum is a healthcare "
        "platform built on the FHIR R4 standard — it stores protected "
        "health information (PHI) including patient records, clinical "
        "observations, conditions, medications, and more as FHIR "
        "resources accessed via a REST API. Medplum extends FHIR R4 "
        "with custom resource types (Bot, Project, ProjectMembership), "
        "custom operations, proprietary extensions, and stricter "
        "validation rules. "
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
        "HARD RULE: This server manages protected health information (PHI). "
        "Medplum extends and diverges from FHIR R4. Your training data "
        "about FHIR is NOT reliable for this server. Malformed writes "
        "can corrupt patient records. You MUST call get_resource_schema "
        "before ANY write operation (create, update, patch). You MUST "
        "call get_resource_capabilities before searching an unfamiliar "
        "resource type. These are not optional optimization steps — "
        "skipping them risks writing bad data to patient records. "
        "The server's schema is the only source of truth. "
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

# ---------------------------------------------------------------------------
# Pydantic input models
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


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

    Results are cached to avoid repeated imports/attribute lookups.
    """
    if resource_type in _MODEL_CACHE:
        return _MODEL_CACHE[resource_type]
    if resource_type not in FHIR_REGISTRY:
        _MODEL_CACHE[resource_type] = None
        return None
    from pymedplum import fhir

    model = getattr(fhir, resource_type, None)
    _MODEL_CACHE[resource_type] = model
    return model


def _annotate_response(result: dict[str, Any]) -> dict[str, Any]:
    """Add schema hints to a FHIR response so the LLM knows its structure."""
    resource_type = result.get("resourceType")
    if not resource_type:
        return result

    if resource_type in FHIR_REGISTRY:
        result["_PHI_WARNING"] = (
            "This response contains PROTECTED HEALTH INFORMATION (PHI). "
            "Handle with care — do not send to external services or "
            "include in logs."
        )
        result["_response_type"] = resource_type
        result["_schema_hint"] = (
            f"WARNING: This is patient data. Do NOT modify without "
            f"first calling get_resource_schema('{resource_type}'). "
            f"Medplum diverges from FHIR R4. Your training data "
            f"WILL be wrong — malformed writes corrupt patient records."
        )

    return result


def _validate_resource(resource: dict[str, Any]) -> None:
    """Validate a resource dict against its Pydantic FHIR model."""
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
    """Validate and normalize a ProjectMembership reference."""
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


# ---------------------------------------------------------------------------
# Read-only enforcement
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Client lifecycle
# ---------------------------------------------------------------------------

_client: AsyncMedplumClient | None = None
_client_lock: asyncio.Lock | None = None


async def _get_client() -> AsyncMedplumClient:
    """Get or create the authenticated AsyncMedplumClient."""
    global _client, _client_lock  # noqa: PLW0603

    if _client is not None:
        return _client

    if _client_lock is None:
        _client_lock = asyncio.Lock()

    async with _client_lock:
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
    """Yield an AsyncMedplumClient, optionally scoped to a ProjectMembership."""
    # Validate before hitting _get_client so bad input fails fast
    # (even without server credentials configured).
    if on_behalf_of is not None:
        ref = _validate_on_behalf_of(on_behalf_of)
    client = await _get_client()
    if on_behalf_of is not None:
        async with client.on_behalf_of(ref) as obo_client:
            yield obo_client
    else:
        yield client


# ---------------------------------------------------------------------------
# Register tools and resources (import triggers @mcp.tool/@mcp.resource)
# ---------------------------------------------------------------------------

import pymedplum.mcp.resources as _resources  # noqa: E402, F401
import pymedplum.mcp.tools as _tools  # noqa: E402, F401

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


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
