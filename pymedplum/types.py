from collections.abc import Callable
from typing import Any, Literal, TypedDict

QueryTypes = str | dict[str, Any] | list[tuple]
OrgMode = Literal["accounts", "extension"]

DEFAULT_ORG_EXTENSION_URL = "https://medplum.com/fhir/StructureDefinition/organization"


class MedplumRequestOptions(TypedDict, total=False):
    """Request options for Medplum API calls."""

    headers: dict[str, str | None]
    timeout: float | None
    org_mode: OrgMode | None
    org_ref: str | None


class PatchOperation(TypedDict):
    """JSON Patch operation for FHIR resources."""

    op: str  # 'add', 'remove', 'replace', 'copy', 'move', 'test'
    path: str
    value: Any | None


BeforeRequestCallback = Callable[[str, str, dict[str, str], dict[str, Any]], None]
