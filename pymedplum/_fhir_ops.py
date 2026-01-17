"""Private helper functions for building FHIR operation parameters.

This module is not part of the public API and is subject to change.
"""

from typing import Any


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
        param: dict[str, Any] = {"name": name}

        if value is None:
            continue  # Skip None values
        elif isinstance(value, bool):
            param["valueBoolean"] = value
        elif isinstance(value, int):
            param["valueInteger"] = value
        elif isinstance(value, float):
            param["valueDecimal"] = value
        elif isinstance(value, str):
            param["valueString"] = value
        elif isinstance(value, dict):
            # Check for special dict types
            if "resourceType" in value:
                # It's a FHIR resource
                param["resource"] = value
            elif "system" in value and "code" in value:
                # It's a Coding
                param["valueCoding"] = value
            elif "reference" in value:
                # It's a Reference
                param["valueReference"] = value
            else:
                # Treat as generic extension or nested structure
                import json

                param["valueString"] = json.dumps(value)
        elif isinstance(value, list):
            # Multiple values with same name
            for item in value:
                if isinstance(item, str):
                    parameter_list.append({"name": name, "valueString": item})
                elif isinstance(item, dict) and "resourceType" in item:
                    parameter_list.append({"name": name, "resource": item})
                else:
                    import json

                    parameter_list.append(
                        {"name": name, "valueString": json.dumps(item)}
                    )
            continue  # Already added to list
        else:
            # Fallback: convert to string
            param["valueString"] = str(value)

        parameter_list.append(param)

    return {"resourceType": "Parameters", "parameter": parameter_list}


def is_parameters_resource(obj: Any) -> bool:
    """Check if an object is already a FHIR Parameters resource."""
    if isinstance(obj, dict):
        return obj.get("resourceType") == "Parameters"
    # Check for Pydantic model with resource_type
    return getattr(obj, "resource_type", None) == "Parameters"


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

    if valueset_url:
        params.append({"name": "url", "valueUri": valueset_url})

    if filter:
        params.append({"name": "filter", "valueString": filter})

    if offset is not None:
        params.append({"name": "offset", "valueInteger": offset})

    if count is not None:
        params.append({"name": "count", "valueInteger": count})

    if include_designations is not None:
        params.append(
            {"name": "includeDesignations", "valueBoolean": include_designations}
        )

    if active_only is not None:
        params.append({"name": "activeOnly", "valueBoolean": active_only})

    if exclude_nested is not None:
        params.append({"name": "excludeNested", "valueBoolean": exclude_nested})

    if exclude_not_for_ui is not None:
        params.append({"name": "excludeNotForUI", "valueBoolean": exclude_not_for_ui})

    if exclude_post_coordinated is not None:
        params.append(
            {"name": "excludePostCoordinated", "valueBoolean": exclude_post_coordinated}
        )

    if display_language:
        params.append({"name": "displayLanguage", "valueCode": display_language})

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

    if conceptmap_url:
        params.append({"name": "url", "valueUri": conceptmap_url})

    if version:
        params.append({"name": "conceptMapVersion", "valueString": version})

    if codeable_concept:
        params.append(
            {"name": "codeableConcept", "valueCodeableConcept": codeable_concept}
        )
    elif coding:
        params.append({"name": "coding", "valueCoding": coding})
    else:
        if code:
            params.append({"name": "code", "valueCode": code})
        if system:
            params.append({"name": "system", "valueUri": system})

    if source:
        params.append({"name": "source", "valueUri": source})

    if target:
        params.append({"name": "target", "valueUri": target})

    if target_system:
        params.append({"name": "targetSystem", "valueUri": target_system})

    if reverse is not None:
        params.append({"name": "reverse", "valueBoolean": reverse})

    return {"resourceType": "Parameters", "parameter": params}
