from collections.abc import Callable
from typing import Any, Literal, TypedDict

QueryTypes = str | dict[str, Any] | list[tuple]

# Search result summary modes per FHIR spec
SummaryMode = Literal["true", "text", "data", "count", "false"]

# Search total count modes per FHIR spec
TotalMode = Literal["none", "estimate", "accurate"]


class MedplumRequestOptions(TypedDict, total=False):
    """Request options for Medplum API calls."""

    headers: dict[str, str | None]
    timeout: float | None


class PatchOperation(TypedDict):
    """JSON Patch operation for FHIR resources."""

    op: str  # 'add', 'remove', 'replace', 'copy', 'move', 'test'
    path: str
    value: Any | None


BeforeRequestCallback = Callable[[str, str, dict[str, str], dict[str, Any]], None]
