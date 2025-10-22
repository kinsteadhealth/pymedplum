from typing import Any, Callable, Literal, Optional, TypedDict, Union

QueryTypes = Union[str, dict[str, Any], list[tuple]]
OrgMode = Literal["accounts", "extension"]

DEFAULT_ORG_EXTENSION_URL = "https://medplum.com/fhir/StructureDefinition/organization"


class MedplumRequestOptions(TypedDict, total=False):
    """Request options for Medplum API calls."""

    headers: Optional[dict[str, str]]
    timeout: Optional[float]
    org_mode: Optional[OrgMode]
    org_ref: Optional[str]


class PatchOperation(TypedDict):
    """JSON Patch operation for FHIR resources."""

    op: str  # 'add', 'remove', 'replace', 'copy', 'move', 'test'
    path: str
    value: Optional[Any]


BeforeRequestCallback = Callable[[str, str, dict[str, str], dict[str, Any]], None]
