"""FHIR helper utilities for common operations.

These functions simplify working with FHIR data structures and
reduce boilerplate in application code.
"""

from typing import Any

from pydantic import BaseModel


def _to_dict(resource: dict[str, Any] | BaseModel) -> dict[str, Any]:
    if isinstance(resource, BaseModel):
        return resource.model_dump(by_alias=True, exclude_none=True)
    return resource


def parse_reference(reference: str) -> tuple[str, str]:
    """Parse a FHIR reference string into resource type and ID.

    Args:
        reference: FHIR reference like "Patient/123"

    Returns:
        Tuple of (resource_type, resource_id)

    Raises:
        ValueError: If reference format is invalid

    Example:
        >>> resource_type, resource_id = parse_reference("Patient/abc-123")
        >>> resource_type
        'Patient'
        >>> resource_id
        'abc-123'
    """
    if not reference or "/" not in reference:
        raise ValueError(f"Invalid FHIR reference: {reference}")

    parts = reference.split("/", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid FHIR reference format: {reference}")

    return parts[0], parts[1]


def build_reference(resource_type: str, resource_id: str) -> str:
    """Build a FHIR reference string from resource type and ID.

    Args:
        resource_type: FHIR resource type (e.g., "Patient")
        resource_id: Resource ID

    Returns:
        FHIR reference string

    Example:
        >>> build_reference("Patient", "123")
        'Patient/123'
    """
    return f"{resource_type}/{resource_id}"


def get_patient_display_name(patient: dict[str, Any] | BaseModel) -> str:
    """Extract a display-friendly name from a Patient resource.

    Handles the complexity of FHIR's HumanName structure and returns
    the best available name representation.

    Args:
        patient: Patient resource (dict or Pydantic model)

    Returns:
        Display name string, or "Unknown" if no name available

    Example:
        >>> patient = {"name": [{"given": ["John"], "family": "Doe"}]}
        >>> get_patient_display_name(patient)
        'John Doe'
    """
    patient = _to_dict(patient)
    name_list = patient.get("name", [])
    if not name_list:
        return "Unknown"

    # Use first name in list
    name_obj = name_list[0]

    # Prefer text representation if available
    text = name_obj.get("text")
    if isinstance(text, str) and text:
        return text

    # Build from parts
    parts: list[str] = []
    given = name_obj.get("given")
    if isinstance(given, list):
        parts.extend(str(g) for g in given)
    family = name_obj.get("family")
    if isinstance(family, str) and family:
        parts.append(family)

    return " ".join(parts) if parts else "Unknown"


def extract_identifier(resource: dict[str, Any] | BaseModel, system: str) -> str | None:
    """Extract an identifier value by system URI.

    Args:
        resource: FHIR resource with identifier field
        system: System URI to match (e.g., "http://hospital.org/mrn")

    Returns:
        Identifier value or None if not found

    Example:
        >>> patient = {"identifier": [
        ...     {"system": "http://hospital.org/mrn", "value": "123456"}
        ... ]}
        >>> extract_identifier(patient, "http://hospital.org/mrn")
        '123456'
    """
    resource = _to_dict(resource)
    for identifier in resource.get("identifier", []):
        if identifier.get("system") == system:
            value = identifier.get("value")
            return value if isinstance(value, str) else None

    return None


def get_code_display(codeable_concept: dict[str, Any] | BaseModel) -> str | None:
    """Extract display text from a CodeableConcept.

    Args:
        codeable_concept: FHIR CodeableConcept

    Returns:
        Display text or None

    Example:
        >>> concept = {"coding": [{"display": "Type 2 Diabetes"}]}
        >>> get_code_display(concept)
        'Type 2 Diabetes'
    """
    codeable_concept = _to_dict(codeable_concept)
    text = codeable_concept.get("text")
    if isinstance(text, str) and text:
        return text

    # Otherwise use first coding's display
    coding_list = codeable_concept.get("coding", [])
    if coding_list:
        display = coding_list[0].get("display")
        if isinstance(display, str) and display:
            return display

    return None


def to_fhir_json(resource: dict[str, Any] | BaseModel) -> dict[str, Any]:
    """Convert a resource to FHIR JSON format.

    Handles both dict resources and Pydantic models.

    Args:
        resource: FHIR resource (dict or Pydantic model)

    Returns:
        Dict representation suitable for JSON serialization

    Example:
        >>> from pymedplum.fhir.patient import Patient
        >>> patient = Patient(name=[{"given": ["John"], "family": "Doe"}])
        >>> data = to_fhir_json(patient)
        >>> data["resourceType"]
        'Patient'
    """
    return _to_dict(resource)


def get_resource_accounts(resource: dict[str, Any] | BaseModel) -> list[str]:
    """Return the account references assigned to a resource.

    Reads from Medplum's meta.accounts field, which stores account
    assignments used for compartment-based multi-tenant access control.

    Args:
        resource: FHIR resource dict

    Returns:
        List of reference strings (e.g., ["Organization/abc", "Practitioner/xyz"])

    Example:
        >>> resource = {
        ...     "resourceType": "Patient",
        ...     "meta": {
        ...         "accounts": [
        ...             {"reference": "Organization/org-1"},
        ...             {"reference": "Organization/org-2"},
        ...         ]
        ...     }
        ... }
        >>> get_resource_accounts(resource)
        ['Organization/org-1', 'Organization/org-2']
    """
    resource = _to_dict(resource)
    return [
        acc["reference"]
        for acc in resource.get("meta", {}).get("accounts", [])
        if isinstance(acc, dict) and "reference" in acc
    ]


def resource_has_account(resource: dict[str, Any], account_ref: str) -> bool:
    """Check if a resource is assigned to a given account.

    Checks Medplum's meta.accounts field for the given reference.

    Args:
        resource: FHIR resource dict
        account_ref: Account reference to check (e.g., "Organization/abc")

    Returns:
        True if the resource is assigned to the given account

    Example:
        >>> resource = {
        ...     "meta": {"accounts": [{"reference": "Organization/org-1"}]}
        ... }
        >>> resource_has_account(resource, "Organization/org-1")
        True
        >>> resource_has_account(resource, "Organization/org-2")
        False
    """
    return account_ref in get_resource_accounts(resource)
