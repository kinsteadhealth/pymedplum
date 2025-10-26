"""Private helper functions for building FHIR operation parameters.

This module is not part of the public API and is subject to change.
"""

from typing import Any, Optional


def build_valueset_validate_params(
    valueset_url: Optional[str] = None,
    valueset_id: Optional[str] = None,  # noqa: ARG001 - Reserved for future use
    code: Optional[str] = None,
    system: Optional[str] = None,
    coding: Optional[dict[str, Any]] = None,
    codeable_concept: Optional[dict[str, Any]] = None,
    display: Optional[str] = None,
    abstract: Optional[bool] = None,
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
    codesystem_url: Optional[str] = None,
    codesystem_id: Optional[str] = None,  # noqa: ARG001 - Reserved for future use
    code: Optional[str] = None,
    coding: Optional[dict[str, Any]] = None,
    version: Optional[str] = None,
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
