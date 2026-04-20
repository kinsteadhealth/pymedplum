"""Private helper functions for building FHIR operation parameters.

This module is not part of the public API and is subject to change.
"""

import json
from typing import Any


def _encode_dict(name: str, value: dict[str, Any]) -> dict[str, Any]:
    """Build a Parameters entry for a dict value, picking the right FHIR shape."""
    if "resourceType" in value:
        return {"name": name, "resource": value}
    if "system" in value and "code" in value:
        return {"name": name, "valueCoding": value}
    if "reference" in value:
        return {"name": name, "valueReference": value}
    return {"name": name, "valueString": json.dumps(value)}


def _encode_scalar(name: str, value: Any) -> dict[str, Any]:
    """Build a single FHIR Parameters entry for a scalar or dict value.

    Returns ``{"name": name}`` plus exactly one of ``valueX`` / ``resource``
    based on the value's type.
    """
    if isinstance(value, bool):
        return {"name": name, "valueBoolean": value}
    if isinstance(value, int):
        return {"name": name, "valueInteger": value}
    if isinstance(value, float):
        return {"name": name, "valueDecimal": value}
    if isinstance(value, str):
        return {"name": name, "valueString": value}
    if isinstance(value, dict):
        return _encode_dict(name, value)
    return {"name": name, "valueString": str(value)}


def dict_to_parameters(params: dict[str, Any]) -> dict[str, Any]:
    """Convert a simple dict to a FHIR Parameters resource.

    Converts key-value pairs into Parameters format with automatic type inference:
    - str -> valueString
    - int -> valueInteger
    - float -> valueDecimal
    - bool -> valueBoolean
    - dict with 'system'/'code' -> valueCoding
    - dict with 'reference' -> valueReference
    - other dict -> resource (if has resourceType) or valueString (JSON)

    Args:
        params: Simple dict of parameter name -> value

    Returns:
        FHIR Parameters resource dict

    Example:
        >>> dict_to_parameters({"code": "12345", "system": "http://loinc.org"})
        {
            "resourceType": "Parameters",
            "parameter": [
                {"name": "code", "valueString": "12345"},
                {"name": "system", "valueString": "http://loinc.org"}
            ]
        }
    """
    parameter_list: list[dict[str, Any]] = []

    for name, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            parameter_list.extend(_encode_scalar(name, item) for item in value)
            continue
        parameter_list.append(_encode_scalar(name, value))

    return {"resourceType": "Parameters", "parameter": parameter_list}


def is_parameters_resource(obj: Any) -> bool:
    """Check if an object is already a FHIR Parameters resource."""
    if isinstance(obj, dict):
        return bool(obj.get("resourceType") == "Parameters")
    # Check for Pydantic model with resource_type
    return bool(getattr(obj, "resource_type", None) == "Parameters")


def _append_optional(
    params: list[dict[str, Any]],
    name: str,
    value: Any,
    value_key: str,
    *,
    include_false: bool = False,
) -> None:
    """Append ``{"name": name, value_key: value}`` if value is meaningful.

    Falsy strings/lists are skipped; booleans are only skipped when ``None``
    (pass ``include_false=True`` to include ``False`` values).
    """
    if value is None:
        return
    if include_false or value or value is False:
        params.append({"name": name, value_key: value})


def build_valueset_validate_params(
    valueset_url: str | None = None,
    valueset_id: str | None = None,  # noqa: ARG001 - Reserved for future use
    code: str | None = None,
    system: str | None = None,
    coding: dict[str, Any | None] | None = None,
    codeable_concept: dict[str, Any | None] | None = None,
    display: str | None = None,
    abstract: bool | None = None,
) -> dict[str, Any]:
    """Build Parameters resource for ValueSet/$validate-code operation.

    Note:
        valueset_id is accepted for API consistency but not included in Parameters.
        The caller uses it to determine the endpoint path.

    Args:
        valueset_url: Canonical URL of the ValueSet
        valueset_id: ID of a specific ValueSet resource (used by caller for endpoint)
        code: Code to validate
        system: Code system URL
        coding: Full Coding object to validate
        codeable_concept: CodeableConcept to validate
        display: Display text to validate
        abstract: Include abstract codes

    Returns:
        Parameters resource for the operation
    """
    params: list[dict[str, Any]] = []

    if valueset_url:
        params.append({"name": "url", "valueUri": valueset_url})

    if code:
        params.append({"name": "code", "valueCode": code})

    if system:
        params.append({"name": "system", "valueUri": system})

    if coding:
        params.append({"name": "coding", "valueCoding": coding})

    if codeable_concept:
        params.append(
            {"name": "codeableConcept", "valueCodeableConcept": codeable_concept}
        )

    if display:
        params.append({"name": "display", "valueString": display})

    if abstract is not None:
        params.append({"name": "abstract", "valueBoolean": abstract})

    return {"resourceType": "Parameters", "parameter": params}


def build_codesystem_validate_params(
    codesystem_url: str | None = None,
    codesystem_id: str | None = None,  # noqa: ARG001 - Reserved for future use
    code: str | None = None,
    coding: dict[str, Any | None] | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    """Build Parameters resource for CodeSystem/$validate-code operation.

    Note:
        codesystem_id is accepted for API consistency but not included in Parameters.
        The caller uses it to determine the endpoint path.

    Args:
        codesystem_url: Canonical URL of the CodeSystem
        codesystem_id: ID of a specific CodeSystem resource (used by caller for endpoint)
        code: Code to validate
        coding: Full Coding object to validate
        version: Specific version of the CodeSystem

    Returns:
        Parameters resource for the operation
    """
    params: list[dict[str, Any]] = []

    if codesystem_url:
        params.append({"name": "url", "valueUri": codesystem_url})

    if version:
        params.append({"name": "version", "valueString": version})

    if code:
        params.append({"name": "code", "valueCode": code})

    if coding:
        params.append({"name": "coding", "valueCoding": coding})

    return {"resourceType": "Parameters", "parameter": params}


def build_valueset_expand_params(
    valueset_url: str | None = None,
    valueset_id: str | None = None,  # noqa: ARG001 - Reserved for future use
    filter: str | None = None,
    offset: int | None = None,
    count: int | None = None,
    include_designations: bool | None = None,
    active_only: bool | None = None,
    exclude_nested: bool | None = None,
    exclude_not_for_ui: bool | None = None,
    exclude_post_coordinated: bool | None = None,
    display_language: str | None = None,
    property: list[str] | None = None,
) -> dict[str, Any]:
    """Build Parameters resource for ValueSet/$expand operation.

    Note:
        valueset_id is accepted for API consistency but not included in Parameters.
        The caller uses it to determine the endpoint path.

    Args:
        valueset_url: Canonical URL of the ValueSet to expand
        valueset_id: ID of a specific ValueSet resource (used by caller for endpoint)
        filter: Text filter to apply to the expansion (substring match on display)
        offset: Starting index for paging (0-based)
        count: Maximum number of concepts to return in the expansion
        include_designations: Include code system designations in expansion
        active_only: Only include active codes
        exclude_nested: Exclude nested codes from expansion
        exclude_not_for_ui: Exclude codes marked as notSelectable
        exclude_post_coordinated: Exclude post-coordinated codes
        display_language: Language for display text (e.g., "en", "de")
        property: List of properties to include for each concept

    Returns:
        Parameters resource for the operation
    """
    params: list[dict[str, Any]] = []

    _append_optional(params, "url", valueset_url or None, "valueUri")
    _append_optional(params, "filter", filter or None, "valueString")
    _append_optional(params, "offset", offset, "valueInteger", include_false=True)
    _append_optional(params, "count", count, "valueInteger", include_false=True)
    _append_optional(
        params,
        "includeDesignations",
        include_designations,
        "valueBoolean",
        include_false=True,
    )
    _append_optional(
        params, "activeOnly", active_only, "valueBoolean", include_false=True
    )
    _append_optional(
        params, "excludeNested", exclude_nested, "valueBoolean", include_false=True
    )
    _append_optional(
        params,
        "excludeNotForUI",
        exclude_not_for_ui,
        "valueBoolean",
        include_false=True,
    )
    _append_optional(
        params,
        "excludePostCoordinated",
        exclude_post_coordinated,
        "valueBoolean",
        include_false=True,
    )
    _append_optional(params, "displayLanguage", display_language or None, "valueCode")

    if property:
        params.extend({"name": "property", "valueString": prop} for prop in property)

    return {"resourceType": "Parameters", "parameter": params}


def build_codesystem_lookup_params(
    code: str,
    system: str | None = None,
    codesystem_id: str | None = None,  # noqa: ARG001 - Reserved for future use
    version: str | None = None,
    coding: dict[str, Any | None] | None = None,
    date: str | None = None,
    display_language: str | None = None,
    property: list[str] | None = None,
) -> dict[str, Any]:
    """Build Parameters resource for CodeSystem/$lookup operation.

    Note:
        codesystem_id is accepted for API consistency but not included in Parameters.
        The caller uses it to determine the endpoint path.

    Args:
        code: Code to look up
        system: Code system URL (required if not using instance-level operation)
        codesystem_id: ID of a specific CodeSystem resource (used by caller for endpoint)
        version: Specific version of the code system
        coding: Full Coding object (alternative to code+system)
        date: Date for which the code should be valid
        display_language: Language for display text (e.g., "en", "de")
        property: List of properties to return for the code

    Returns:
        Parameters resource for the operation
    """
    params: list[dict[str, Any]] = []

    if coding:
        params.append({"name": "coding", "valueCoding": coding})
    else:
        params.append({"name": "code", "valueCode": code})
        if system:
            params.append({"name": "system", "valueUri": system})

    if version:
        params.append({"name": "version", "valueString": version})

    if date:
        params.append({"name": "date", "valueDateTime": date})

    if display_language:
        params.append({"name": "displayLanguage", "valueCode": display_language})

    if property:
        params.extend({"name": "property", "valueCode": prop} for prop in property)

    return {"resourceType": "Parameters", "parameter": params}


def _append_translate_source(
    params: list[dict[str, Any]],
    *,
    code: str | None,
    system: str | None,
    coding: dict[str, Any | None] | None,
    codeable_concept: dict[str, Any | None] | None,
) -> None:
    """Append exactly one source term (codeableConcept > coding > code+system)."""
    if codeable_concept:
        params.append(
            {"name": "codeableConcept", "valueCodeableConcept": codeable_concept}
        )
        return
    if coding:
        params.append({"name": "coding", "valueCoding": coding})
        return
    if code:
        params.append({"name": "code", "valueCode": code})
    if system:
        params.append({"name": "system", "valueUri": system})


def build_conceptmap_translate_params(
    code: str | None = None,
    system: str | None = None,
    conceptmap_url: str | None = None,
    conceptmap_id: str | None = None,  # noqa: ARG001 - Reserved for future use
    version: str | None = None,
    source: str | None = None,
    target: str | None = None,
    coding: dict[str, Any | None] | None = None,
    codeable_concept: dict[str, Any | None] | None = None,
    target_system: str | None = None,
    reverse: bool | None = None,
) -> dict[str, Any]:
    """Build Parameters resource for ConceptMap/$translate operation.

    Note:
        conceptmap_id is accepted for API consistency but not included in Parameters.
        The caller uses it to determine the endpoint path.

    Args:
        code: Code to translate
        system: Code system URL of the source code
        conceptmap_url: Canonical URL of the ConceptMap to use
        conceptmap_id: ID of a specific ConceptMap resource (used by caller for endpoint)
        version: Version of the ConceptMap
        source: Source value set URL (filter for applicable mappings)
        target: Target value set URL (filter for applicable mappings)
        coding: Full Coding object (alternative to code+system)
        codeable_concept: CodeableConcept to translate
        target_system: Target code system URL
        reverse: Reverse the direction of the mapping

    Returns:
        Parameters resource for the operation
    """
    params: list[dict[str, Any]] = []

    _append_optional(params, "url", conceptmap_url or None, "valueUri")
    _append_optional(params, "conceptMapVersion", version or None, "valueString")

    _append_translate_source(
        params,
        code=code,
        system=system,
        coding=coding,
        codeable_concept=codeable_concept,
    )

    _append_optional(params, "source", source or None, "valueUri")
    _append_optional(params, "target", target or None, "valueUri")
    _append_optional(params, "targetSystem", target_system or None, "valueUri")
    _append_optional(params, "reverse", reverse, "valueBoolean", include_false=True)

    return {"resourceType": "Parameters", "parameter": params}
