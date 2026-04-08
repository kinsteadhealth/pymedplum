"""MCP resource handlers: server info, tool guide, common errors."""

from __future__ import annotations

import os
from typing import Any

from pymedplum.mcp.server import _is_read_only, mcp


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
