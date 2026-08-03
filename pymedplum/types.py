from dataclasses import dataclass
from typing import Any, Literal, TypedDict

QueryTypes = str | dict[str, Any] | list[tuple[str, Any]]


@dataclass(frozen=True)
class UpdateResult:
    """Outcome of an ``update_with_retry`` call.

    Attributes:
        wrote: Whether a PUT was sent. ``False`` means the mutator
            returned ``None`` or left the resource unchanged, so the
            write was skipped.
        version_id: ``meta.versionId`` after the call — the freshly
            written version when ``wrote`` is ``True``, the version
            read when ``wrote`` is ``False``. Empty string if the
            server never surfaced one.
        resource: The resource state after the call — the server's PUT
            response when ``wrote`` is ``True`` (re-read when the
            server returned an empty body), the read-back state when
            ``wrote`` is ``False``.
    """

    wrote: bool
    version_id: str
    resource: dict[str, Any]


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
