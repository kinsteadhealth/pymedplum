"""ProjectMembership access entry helpers and merge primitives.

Multi-tenant Medplum apps grant a user access to a tenant by
appending a parameterized AccessPolicy entry to
``ProjectMembership.access``. See Medplum's
``packages/docs/docs/access/multi-tenant-access-policy.md`` for the
data model.

The corresponding *write* path is a read-modify-write loop with
optimistic concurrency: read the membership, compute a new
``access`` list, write it back with ``If-Match``, retry on 412.
``merge_project_membership_access`` on the sync and async clients
implements that loop; this module ships the transport-agnostic
pieces it composes (entry construction, policy normalization,
partition, merge, byte-equality check).

The partition step (``managed_policy_ids``) is a defensive guard
against a second writer — typically a manual admin edit via the
Medplum app UI. In a single-writer setup it is a no-op: the entire
``access`` list is "managed", nothing is preserved untouched.
Tenant choice, parameter names, and business rules remain the
caller's responsibility.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from .helpers import to_fhir_json

__all__ = [
    "MergeResult",
    "build_merged_access",
    "get_project_membership_access_parameter",
    "get_project_membership_access_policy_id",
    "make_project_membership_access",
    "merged_equals_remote",
    "normalize_access_entry",
    "normalize_access_policy_id",
    "normalize_access_policy_reference",
    "partition_access",
    "validate_managed_access",
]


_PROJECT_MEMBERSHIP_RESOURCE_TYPE = "ProjectMembership"


def _normalize_project_membership_id(membership_id: str) -> str:
    """Return the bare ProjectMembership ID for a string input.

    Accepts ``"abc"`` and ``"ProjectMembership/abc"``. Raises
    :class:`ValueError` for empty inputs and references to other
    resource types.
    """
    if not isinstance(membership_id, str):
        raise TypeError(
            "membership_id must be a string, got "
            f"{type(membership_id).__name__}"
        )
    bare = membership_id.strip()
    if not bare:
        raise ValueError("membership_id must not be empty")
    if "/" in bare:
        resource_type, _, resource_id = bare.partition("/")
        if resource_type != _PROJECT_MEMBERSHIP_RESOURCE_TYPE:
            raise ValueError(
                "membership_id must reference ProjectMembership, got "
                f"'{resource_type}'"
            )
        if not resource_id:
            raise ValueError("membership_id is missing an ID")
        return resource_id
    return bare


_ACCESS_POLICY_RESOURCE_TYPE = "AccessPolicy"


@dataclass(frozen=True)
class MergeResult:
    """Outcome of a :meth:`merge_project_membership_access` call.

    Attributes:
        updated: Whether a PUT was sent. ``False`` means the merged
            access list was byte-equal to the remote and ``force`` was
            ``False``, so the helper short-circuited.
        version_id: ``meta.versionId`` of the membership after the
            merge — the freshly written value when ``updated`` is
            ``True``, the pre-existing value when ``updated`` is
            ``False``.
        managed_count: Number of entries in the managed slice after
            the merge.
        untouched_count: Number of entries preserved untouched.
    """

    updated: bool
    version_id: str
    managed_count: int
    untouched_count: int


def _entry_to_dict(entry: BaseModel | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(entry, BaseModel):
        return to_fhir_json(entry)
    if isinstance(entry, Mapping):
        return dict(entry)
    raise TypeError(
        "Access entry must be a Pydantic model or mapping, got "
        f"{type(entry).__name__}"
    )


def normalize_access_policy_reference(
    policy: str | BaseModel | Mapping[str, Any],
) -> dict[str, Any]:
    """Return a ``{"reference": "AccessPolicy/<id>"}`` dict.

    Accepts:
        * bare AccessPolicy ID (``"abc"``)
        * full reference string (``"AccessPolicy/abc"``)
        * generated ``Reference`` model
        * raw reference dict (``{"reference": "AccessPolicy/abc"}``)

    Raises:
        ValueError: If the input cannot be resolved to a non-empty
            ``AccessPolicy/<id>`` reference.
    """
    if isinstance(policy, str):
        bare = policy.strip()
        if not bare:
            raise ValueError("AccessPolicy reference must not be empty")
        if "/" in bare:
            resource_type, _, resource_id = bare.partition("/")
            if resource_type != _ACCESS_POLICY_RESOURCE_TYPE:
                raise ValueError(
                    "AccessPolicy reference must use resource type "
                    f"'AccessPolicy', got '{resource_type}'"
                )
            if not resource_id:
                raise ValueError("AccessPolicy reference is missing an ID")
            return {"reference": f"{_ACCESS_POLICY_RESOURCE_TYPE}/{resource_id}"}
        return {"reference": f"{_ACCESS_POLICY_RESOURCE_TYPE}/{bare}"}

    if isinstance(policy, BaseModel):
        data = to_fhir_json(policy)
    elif isinstance(policy, Mapping):
        data = dict(policy)
    else:
        raise TypeError(
            "AccessPolicy reference must be str, mapping, or Pydantic "
            f"model; got {type(policy).__name__}"
        )

    reference = data.get("reference")
    if not isinstance(reference, str) or not reference.strip():
        raise ValueError(
            "AccessPolicy reference dict/model must include a non-empty "
            "'reference' field"
        )
    return normalize_access_policy_reference(reference)


def normalize_access_policy_id(
    policy: str | BaseModel | Mapping[str, Any],
) -> str:
    """Return the bare AccessPolicy ID for a policy input.

    Accepts the same shapes as :func:`normalize_access_policy_reference`.
    """
    ref = normalize_access_policy_reference(policy)["reference"]
    return ref.split("/", 1)[1]


def _coerce_parameter_value(
    name: str,
    value: str | BaseModel | Mapping[str, Any],
) -> dict[str, Any]:
    """Build the value-bearing portion of a ProjectMembershipAccess parameter.

    Returns a dict with one of ``valueReference`` / ``valueString``.
    """
    if isinstance(value, str):
        if not value:
            raise ValueError(
                f"Parameter '{name}' value must not be an empty string"
            )
        if "/" in value:
            return {"valueReference": {"reference": value}}
        return {"valueString": value}

    if isinstance(value, BaseModel):
        data = to_fhir_json(value)
    elif isinstance(value, Mapping):
        data = dict(value)
    else:
        raise TypeError(
            f"Parameter '{name}' value must be str, mapping, or Pydantic "
            f"model; got {type(value).__name__}"
        )

    reference = data.get("reference")
    if isinstance(reference, str) and reference.strip():
        return {"valueReference": data}

    raise ValueError(
        f"Parameter '{name}' value must be a string or a Reference-shaped "
        "object with a non-empty 'reference' field"
    )


def make_project_membership_access(
    policy: str | BaseModel | Mapping[str, Any],
    parameters: Mapping[str, str | BaseModel | Mapping[str, Any]],
) -> dict[str, Any]:
    """Build a ``ProjectMembership.access`` entry dict.

    The result has the shape Medplum stores for a parameterized
    AccessPolicy binding::

        {
            "policy": {"reference": "AccessPolicy/<id>"},
            "parameter": [
                {"name": "<name>", "valueReference": {"reference": "..."}},
                {"name": "<name>", "valueString": "..."},
            ]
        }

    Args:
        policy: AccessPolicy reference. Bare ID, ``"AccessPolicy/<id>"``,
            ``Reference`` model, or raw reference dict.
        parameters: Mapping from parameter name to value. Values are
            either reference-shaped (``"ResourceType/id"``, a
            ``Reference`` model, or a dict with a ``reference`` field)
            and emitted as ``valueReference``, or plain strings emitted
            as ``valueString``.

    Returns:
        A FHIR JSON dict suitable for inclusion in
        ``ProjectMembership.access``.

    Raises:
        ValueError: If the policy is malformed, parameter names are
            empty, or a parameter value is unsupported.
    """
    policy_dict = normalize_access_policy_reference(policy)

    if not isinstance(parameters, Mapping):
        raise TypeError(
            "parameters must be a Mapping, got "
            f"{type(parameters).__name__}"
        )

    parameter_list: list[dict[str, Any]] = []
    for raw_name, raw_value in parameters.items():
        if not isinstance(raw_name, str) or not raw_name.strip():
            raise ValueError("Parameter name must be a non-empty string")
        value_dict = _coerce_parameter_value(raw_name, raw_value)
        parameter_list.append({"name": raw_name, **value_dict})

    entry: dict[str, Any] = {"policy": policy_dict}
    if parameter_list:
        entry["parameter"] = parameter_list
    return entry


def get_project_membership_access_policy_id(
    entry: BaseModel | Mapping[str, Any],
) -> str | None:
    """Return the bare AccessPolicy ID from an access entry, if any.

    Returns ``None`` for malformed entries (missing ``policy``,
    missing ``policy.reference``, non-string reference, or a
    reference that doesn't resolve to ``AccessPolicy/<id>``).
    """
    try:
        data = _entry_to_dict(entry)
    except TypeError:
        return None
    policy = data.get("policy")
    if not isinstance(policy, Mapping):
        return None
    reference = policy.get("reference")
    if not isinstance(reference, str):
        return None
    try:
        return normalize_access_policy_id(reference)
    except (TypeError, ValueError):
        return None


def get_project_membership_access_parameter(
    entry: BaseModel | Mapping[str, Any],
    name: str,
) -> dict[str, Any] | None:
    """Return the named parameter dict from an access entry, or None.

    The returned dict is the FHIR-JSON parameter element (``{"name":
    ..., "valueReference": ...}`` or similar). Returns ``None`` when
    the entry does not carry the parameter.
    """
    try:
        data = _entry_to_dict(entry)
    except TypeError:
        return None
    parameters = data.get("parameter")
    if not isinstance(parameters, Iterable):
        return None
    for param in parameters:
        if isinstance(param, BaseModel):
            param = to_fhir_json(param)
        if not isinstance(param, Mapping):
            continue
        if param.get("name") == name:
            return dict(param)
    return None


def normalize_access_entry(
    entry: BaseModel | Mapping[str, Any],
) -> dict[str, Any]:
    """Convert a ProjectMembership.access entry to FHIR JSON.

    Accepts a ``ProjectMembershipAccess`` Pydantic model or an already
    dict-shaped entry; returns a FHIR JSON dict with camelCase keys
    and ``None`` fields removed (via :func:`to_fhir_json`).
    """
    if isinstance(entry, BaseModel):
        return to_fhir_json(entry)
    if isinstance(entry, Mapping):
        # Round-trip through json to reject non-JSON-serializable values
        # while preserving dict shape (cheap and avoids surprising mutations
        # of caller-owned objects).
        return json.loads(json.dumps(entry))
    raise TypeError(
        "Access entry must be a Pydantic model or mapping, got "
        f"{type(entry).__name__}"
    )


def partition_access(
    current: list[BaseModel | Mapping[str, Any]] | None,
    managed_policy_ids: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split current ``access`` into (managed, untouched).

    In a single-writer app this returns ``(current, [])`` — every
    entry is managed, nothing is preserved. The "untouched" branch
    is a guard for entries written by a second source (typically a
    manual admin edit) so a routine reconcile doesn't silently
    delete them.

    Args:
        current: The remote ``ProjectMembership.access`` list (any
            mix of dicts and ``ProjectMembershipAccess`` models).
            ``None`` is treated as an empty list.
        managed_policy_ids: AccessPolicy IDs the caller manages.
            Entries whose policy resolves to an ID in this set are
            "managed"; everything else is "untouched". Malformed
            entries (missing policy, non-AccessPolicy reference,
            non-string reference) are left untouched so the helper
            never silently drops data it can't classify.

    Returns:
        ``(managed, untouched)`` — each a list of FHIR-JSON dicts.
        Untouched preserves original order.
    """
    if not managed_policy_ids:
        raise ValueError("managed_policy_ids must not be empty")

    managed: list[dict[str, Any]] = []
    untouched: list[dict[str, Any]] = []
    for raw_entry in current or []:
        entry_dict = normalize_access_entry(raw_entry)
        policy_id = get_project_membership_access_policy_id(entry_dict)
        if policy_id is not None and policy_id in managed_policy_ids:
            managed.append(entry_dict)
        else:
            untouched.append(entry_dict)
    return managed, untouched


def build_merged_access(
    untouched: list[BaseModel | Mapping[str, Any]],
    managed_access: list[BaseModel | Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Build the merged ``ProjectMembership.access`` list.

    The result is ``untouched`` (in original order) followed by
    ``managed_access`` (in caller order). Both are normalized to
    FHIR JSON.
    """
    return [normalize_access_entry(e) for e in untouched] + [
        normalize_access_entry(e) for e in managed_access
    ]


def _stable_dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def merged_equals_remote(
    merged: list[BaseModel | Mapping[str, Any]],
    remote: list[BaseModel | Mapping[str, Any]] | None,
) -> bool:
    """Return ``True`` if the merged list is byte-equal to remote.

    Equality is checked via canonical JSON (sorted keys, no
    insignificant whitespace), so semantically identical lists that
    differ only in key ordering compare equal. ``None`` and ``[]`` are
    equal.
    """
    merged_norm = [normalize_access_entry(e) for e in merged]
    remote_norm = [normalize_access_entry(e) for e in (remote or [])]
    return _stable_dump(merged_norm) == _stable_dump(remote_norm)


def validate_managed_access(
    managed_access: list[BaseModel | Mapping[str, Any]],
    managed_policy_ids: set[str],
) -> None:
    """Reject managed entries that reference unmanaged policies.

    Keeps the ``managed_access=[]`` lockout primitive honest: every
    entry the helper writes must belong to the managed set, so that
    a later ``[]`` call can fully remove its own footprint. An
    entry pointing at an outside policy would partition as
    "untouched" on the next call and survive the cleanup.

    Raises:
        ValueError: If any entry's policy resolves to an ID outside
            ``managed_policy_ids`` or cannot be resolved at all.
    """
    if not managed_policy_ids:
        raise ValueError("managed_policy_ids must not be empty")
    for index, raw_entry in enumerate(managed_access):
        entry = normalize_access_entry(raw_entry)
        policy_id = get_project_membership_access_policy_id(entry)
        if policy_id is None:
            raise ValueError(
                f"managed_access[{index}] has no resolvable AccessPolicy "
                "reference"
            )
        if policy_id not in managed_policy_ids:
            raise ValueError(
                f"managed_access[{index}] references AccessPolicy "
                f"'{policy_id}', which is outside managed_policy_ids"
            )
