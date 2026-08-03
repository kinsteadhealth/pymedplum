"""FHIR extension helpers.

Read, set, and remove ``extension`` entries on FHIR elements without
open-coding URL walking at every call site. Every helper accepts both
raw dicts and generated Pydantic models — they share the ``extension``
list shape. Mutating helpers write FHIR JSON (camelCase) entries; when
the element is a Pydantic model, assignment triggers validation, so
entries are coerced to ``Extension`` models automatically.

Also carries Medplum's slot/schedule service-tagging convention
(``service-type-reference``): in R5/R6 ``serviceType`` becomes a
``CodeableReference<HealthcareService>``, and Medplum represents that in
R4 by embedding a ``valueReference`` extension inside each
``serviceType`` CodeableConcept.
"""

from __future__ import annotations

from typing import Any

SERVICE_TYPE_REFERENCE_URL = "https://medplum.com/fhir/service-type-reference"
"""Medplum's extension URL for a HealthcareService reference embedded in a
``serviceType`` CodeableConcept (their R4 stand-in for R5's
``CodeableReference``)."""


def _field(element: Any, name: str, fhir_name: str | None = None) -> Any:
    """Read a field off a dict (FHIR JSON key) or model (snake_case attr)."""
    if isinstance(element, dict):
        return element.get(fhir_name or name)
    return getattr(element, name, None)


def _extension_url(ext: Any) -> str | None:
    url = _field(ext, "url")
    return url if isinstance(url, str) else None


def _camel(key: str) -> str:
    """Normalize a kwarg name to FHIR JSON camelCase (value_string -> valueString)."""
    head, *rest = key.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in rest)


def _ext_to_dict(ext: Any) -> dict[str, Any]:
    if isinstance(ext, dict):
        return ext
    dumped: dict[str, Any] = ext.model_dump(by_alias=True, exclude_none=True)
    return dumped


def _set_extension_list(element: Any, extensions: list[Any]) -> None:
    """Write the extension list back, dropping the key/attr when empty.

    FHIR JSON forbids empty arrays, so an emptied list removes the
    ``extension`` key entirely (``None`` on models).
    """
    if isinstance(element, dict):
        if extensions:
            element["extension"] = extensions
        else:
            element.pop("extension", None)
    else:
        element.extension = extensions or None


def get_extension(element: Any, url: str) -> Any | None:
    """Return the first extension entry with the given URL, or ``None``.

    The entry is returned as stored — a dict on dict elements, an
    ``Extension`` model on model elements.
    """
    for ext in _field(element, "extension") or []:
        if _extension_url(ext) == url:
            return ext
    return None


def get_extensions(element: Any, url: str) -> list[Any]:
    """Return every extension entry with the given URL (possibly empty)."""
    return [
        ext for ext in _field(element, "extension") or [] if _extension_url(ext) == url
    ]


def get_extension_value(element: Any, url: str) -> Any | None:
    """Return the ``value[x]`` of the first extension with the given URL.

    ``None`` both when the extension is absent and when it carries no
    ``value[x]`` (e.g. a complex extension with nested children — use
    :func:`get_nested_value` for those).
    """
    ext = get_extension(element, url)
    if ext is None:
        return None
    return _value_of(ext)


def _value_of(ext: Any) -> Any | None:
    """Return the single ``value[x]`` field of an extension entry."""
    data = _ext_to_dict(ext)
    for key, value in data.items():
        if key.startswith("value"):
            return value
    return None


def set_extension(element: Any, url: str, **value_x: Any) -> None:
    """Set the extension with the given URL, replacing or appending.

    Exactly one ``value[x]`` keyword is expected, in either FHIR JSON
    camelCase or snake_case form (``valueString="x"`` /
    ``value_string="x"``). The first existing entry with the URL is
    replaced in place; any further duplicates are dropped; with no
    existing entry, the new one is appended.

    Example:
        >>> set_extension(patient, "https://example.org/flag", valueBoolean=True)
    """
    if len(value_x) != 1:
        raise ValueError(
            f"set_extension expects exactly one value[x] keyword, "
            f"got {sorted(value_x)!r}"
        )
    key, value = next(iter(value_x.items()))
    upsert_extension(element, {"url": url, _camel(key): value}, key_url=url)


def upsert_extension(element: Any, ext: Any, *, key_url: str) -> None:
    """Merge a complete extension entry into the element, keyed by URL.

    The first existing entry whose ``url`` equals ``key_url`` is
    replaced by ``ext`` in place (further duplicates are dropped);
    otherwise ``ext`` is appended. ``ext`` may be a dict or an
    ``Extension`` model.
    """
    existing = list(_field(element, "extension") or [])
    replaced = False
    result: list[Any] = []
    for entry in existing:
        if _extension_url(entry) == key_url:
            if not replaced:
                result.append(ext)
                replaced = True
            continue
        result.append(entry)
    if not replaced:
        result.append(ext)
    _set_extension_list(element, result)


def remove_extension(element: Any, url: str) -> bool:
    """Remove every extension entry with the given URL.

    Returns ``True`` when at least one entry was removed. An emptied
    list removes the ``extension`` key entirely (FHIR JSON forbids
    empty arrays).
    """
    existing = list(_field(element, "extension") or [])
    kept = [ext for ext in existing if _extension_url(ext) != url]
    if len(kept) == len(existing):
        return False
    _set_extension_list(element, kept)
    return True


def get_nested_value(ext: Any, child_url: str) -> Any | None:
    """Return the ``value[x]`` of a child extension inside a complex extension.

    Complex extensions carry no ``value[x]`` of their own — their data
    lives in nested ``extension`` entries keyed by URL.

    Example:
        >>> ext = {"url": "https://example.org/complex", "extension": [
        ...     {"url": "start", "valueDateTime": "2026-01-01T09:00:00Z"},
        ... ]}
        >>> get_nested_value(ext, "start")
        '2026-01-01T09:00:00Z'
    """
    child = get_extension(ext, child_url)
    if child is None:
        return None
    return _value_of(child)


def service_type_reference_extension(
    reference: str,
    codings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a ``serviceType`` CodeableConcept carrying Medplum's service reference.

    Medplum tags Slot/Schedule ``serviceType`` concepts with an embedded
    ``Reference<HealthcareService>`` extension (their R4 representation
    of R5's ``CodeableReference`` — see
    :data:`SERVICE_TYPE_REFERENCE_URL`). The result goes straight into a
    ``serviceType`` list.

    Args:
        reference: The service reference, e.g. ``"HealthcareService/123"``.
        codings: Optional ``Coding`` dicts to carry alongside the
            reference (the concept's human-facing codes).

    Example:
        >>> slot["serviceType"] = [
        ...     service_type_reference_extension("HealthcareService/123")
        ... ]
    """
    if not reference or "/" not in reference:
        raise ValueError(
            f"Invalid service reference: {reference!r}. "
            "Expected format like 'HealthcareService/123'."
        )
    concept: dict[str, Any] = {}
    if codings:
        concept["coding"] = list(codings)
    concept["extension"] = [
        {
            "url": SERVICE_TYPE_REFERENCE_URL,
            "valueReference": {"reference": reference},
        }
    ]
    return concept


def read_service_type_references(slot_or_schedule: Any) -> list[str]:
    """Extract HealthcareService reference strings from ``serviceType``.

    Walks each ``serviceType`` CodeableConcept on a Slot/Schedule (dict
    or model) and collects the reference embedded under
    :data:`SERVICE_TYPE_REFERENCE_URL`. Concepts without the extension
    are skipped.
    """
    concepts = _field(slot_or_schedule, "service_type", "serviceType") or []
    references: list[str] = []
    for concept in concepts:
        value = get_extension_value(concept, SERVICE_TYPE_REFERENCE_URL)
        if value is None:
            continue
        ref = _field(value, "reference")
        if isinstance(ref, str) and ref:
            references.append(ref)
    return references
