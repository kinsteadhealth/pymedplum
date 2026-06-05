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


def resolve_id(
    reference: str | dict[str, Any] | BaseModel | None,
) -> str | None:
    """Return the bare resource id from a reference, leniently.

    Unlike :func:`parse_reference` (which requires a ``"Type/id"`` string
    and raises on anything else), this accepts the shapes a FHIR id
    actually arrives in and never raises — it returns ``None`` when no id
    can be found. Mirrors ``@medplum/core``'s ``resolveId``, with added
    support for bare-id and reference *strings*.

    Accepts:
        - a reference string (``"Patient/123"`` -> ``"123"``)
        - a bare id string (``"123"`` -> ``"123"``)
        - a Reference dict/model (``{"reference": "Patient/123"}`` -> ``"123"``)
        - a Resource dict/model (returns its ``id``)

    Example:
        >>> resolve_id("Patient/123")
        '123'
        >>> resolve_id({"reference": "Patient/abc"})
        'abc'
        >>> resolve_id(None) is None
        True
    """
    if reference is None:
        return None
    if isinstance(reference, BaseModel):
        reference = _to_dict(reference)
    if isinstance(reference, dict):
        ref_str = reference.get("reference")
        if isinstance(ref_str, str) and ref_str:
            return ref_str.rsplit("/", 1)[-1] or None
        resource_id = reference.get("id")
        return resource_id if isinstance(resource_id, str) and resource_id else None
    if isinstance(reference, str) and reference:
        return reference.rsplit("/", 1)[-1] or None
    return None


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


def _clean_str(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def coding_parts(
    codeable_concept: dict[str, Any] | BaseModel | None,
) -> tuple[str | None, str | None, str | None, str | None]:
    """Return ``(code, system, display, text)`` from a CodeableConcept.

    A low-level projection accessor: reads the **first** (primary) coding
    plus the concept's free ``text``. A CodeableConcept may carry codings
    from several systems (e.g. ICD-10 and SNOMED); when you need the code
    for a specific system, use :func:`get_code_by_system` instead.

    Example:
        >>> coding_parts({"coding": [{"code": "E11.9", "display": "DM2"}]})
        ('E11.9', None, 'DM2', None)
    """
    if codeable_concept is None:
        return None, None, None, None
    codeable_concept = _to_dict(codeable_concept)
    text = _clean_str(codeable_concept.get("text"))
    coding_list = codeable_concept.get("coding")
    if not isinstance(coding_list, list) or not coding_list:
        return None, None, None, text
    first = coding_list[0]
    if not isinstance(first, dict):
        return None, None, None, text
    return (
        _clean_str(first.get("code")),
        _clean_str(first.get("system")),
        _clean_str(first.get("display")),
        text,
    )


def get_code_by_system(
    codeable_concept: dict[str, Any] | BaseModel | None, system: str
) -> str | None:
    """Return the code of the first coding matching ``system``.

    The Medplum-canonical way to pull a code from a CodeableConcept that
    may carry multiple systems. Mirrors ``@medplum/core``'s
    ``getCodeBySystem``.

    Example:
        >>> concept = {"coding": [
        ...     {"system": "http://snomed.info/sct", "code": "44054006"},
        ...     {"system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "E11.9"},
        ... ]}
        >>> get_code_by_system(concept, "http://hl7.org/fhir/sid/icd-10-cm")
        'E11.9'
    """
    if codeable_concept is None:
        return None
    codeable_concept = _to_dict(codeable_concept)
    for coding in codeable_concept.get("coding") or []:
        if isinstance(coding, dict) and coding.get("system") == system:
            return _clean_str(coding.get("code"))
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


def extract_account_references(
    meta: dict[str, Any] | BaseModel | None,
) -> list[str]:
    """Normalize a resource's ``meta.account`` and ``meta.accounts`` into one
    list of reference strings.

    Medplum stores account assignments — used for compartment-based
    multi-tenant access control — in ``meta.accounts`` (plural). The legacy
    ``meta.account`` (singular) is ``@deprecated`` in Medplum but still
    present on older resources, so a correct reader must consider both.
    Mirrors ``@medplum/core``'s ``extractAccountReferences``: the singular
    account comes first and is deduped against the plural list.

    Returns reference strings (this SDK is reference-string oriented), not
    Reference objects.

    Example:
        >>> extract_account_references({
        ...     "account": {"reference": "Organization/org-1"},
        ...     "accounts": [{"reference": "Organization/org-2"}],
        ... })
        ['Organization/org-1', 'Organization/org-2']
    """
    if not meta:
        return []
    meta = _to_dict(meta)
    plural = [
        ref
        for acc in meta.get("accounts") or []
        if isinstance(acc, dict) and (ref := _clean_str(acc.get("reference")))
    ]
    account = meta.get("account")
    account_ref = (
        _clean_str(account.get("reference"))
        if isinstance(account, dict)
        else None
    )
    if account_ref and account_ref not in plural:
        return [account_ref, *plural]
    return plural


def get_resource_accounts(resource: dict[str, Any] | BaseModel) -> list[str]:
    """Return the account references assigned to a resource.

    Reads from Medplum's ``meta.accounts`` (and the deprecated singular
    ``meta.account``), which store the account assignments used for
    compartment-based multi-tenant access control. See
    :func:`extract_account_references` for the normalization semantics.

    Args:
        resource: FHIR resource dict or model

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
    return extract_account_references(resource.get("meta"))


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
