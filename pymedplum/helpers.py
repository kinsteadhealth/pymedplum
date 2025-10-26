"""FHIR helper utilities for common operations.

These functions simplify working with FHIR data structures and
reduce boilerplate in application code.
"""

import base64
import copy
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union


def parse_reference(reference: str) -> Tuple[str, str]:
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


def get_patient_display_name(patient: Dict[str, Any]) -> str:
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
    # Convert Pydantic model to dict if needed
    if hasattr(patient, "model_dump"):
        patient = patient.model_dump()

    name_list = patient.get("name", [])
    if not name_list:
        return "Unknown"

    # Use first name in list
    name_obj = name_list[0]

    # Prefer text representation if available
    if name_obj.get("text"):
        return name_obj["text"]

    # Build from parts
    parts = []
    if name_obj.get("given"):
        parts.extend(name_obj["given"])
    if name_obj.get("family"):
        parts.append(name_obj["family"])

    return " ".join(parts) if parts else "Unknown"


def extract_identifier(resource: Dict[str, Any], system: str) -> Optional[str]:
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
    # Convert Pydantic model to dict if needed
    if hasattr(resource, "model_dump"):
        resource = resource.model_dump()

    for identifier in resource.get("identifier", []):
        if identifier.get("system") == system:
            return identifier.get("value")

    return None


def get_code_display(codeable_concept: Dict[str, Any]) -> Optional[str]:
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
    if hasattr(codeable_concept, "model_dump"):
        codeable_concept = codeable_concept.model_dump()

    # Prefer text if available
    if codeable_concept.get("text"):
        return codeable_concept["text"]

    # Otherwise use first coding's display
    coding_list = codeable_concept.get("coding", [])
    if coding_list and coding_list[0].get("display"):
        return coding_list[0]["display"]

    return None


def to_fhir_json(resource: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
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
    if hasattr(resource, "model_dump"):
        return resource.model_dump(by_alias=True, exclude_none=True)
    return resource


def to_portable(
    resource: Dict[str, Any],
    org_ext_url: str = "https://example.org/fhir/StructureDefinition/orgLink",
) -> Dict[str, Any]:
    """Convert Medplum-specific FHIR to portable FHIR.

    Removes vendor-specific meta fields and converts Medplum's
    multi-organization accounts to standard FHIR extensions.

    Args:
        resource: FHIR resource with Medplum-specific fields
        org_ext_url: Extension URL for organization links

    Returns:
        Portable FHIR resource (deep copy, original unchanged)

    Example:
        >>> resource = {
        ...     "resourceType": "Patient",
        ...     "meta": {
        ...         "accounts": [{"reference": "Organization/org1"}],
        ...         "author": {"reference": "ClientApplication/app1"}
        ...     }
        ... }
        >>> portable = to_portable(resource)
        >>> "accounts" in portable["meta"]
        False
        >>> "author" in portable["meta"]
        False
    """
    # Deep copy to avoid mutating original
    result = copy.deepcopy(resource)

    # Handle Bundle entries recursively
    if result.get("resourceType") == "Bundle" and result.get("entry"):
        for entry in result["entry"]:
            if "resource" in entry:
                entry["resource"] = to_portable(entry["resource"], org_ext_url)

    # Process meta field
    meta = result.get("meta")
    if not meta:
        return result

    # Convert accounts to extensions
    accounts = meta.pop("accounts", None)
    if accounts:
        extensions = meta.get("extension", [])
        for account in accounts:
            if "reference" in account:
                extensions.append(
                    {
                        "url": org_ext_url,
                        "valueReference": {"reference": account["reference"]},
                    }
                )
        if extensions:
            meta["extension"] = extensions

    # Remove vendor-specific fields
    vendor_fields = ["author", "project", "account", "compartment", "onBehalfOf"]
    for field in vendor_fields:
        meta.pop(field, None)

    return result


def decode_jwt_exp(token: str) -> Optional[datetime]:
    """Decode JWT token and extract expiration time.

    Args:
        token: JWT token string

    Returns:
        Expiration datetime or None if not found

    Example:
        >>> token = "eyJ...header...eyJ...payload...signature"
        >>> exp = decode_jwt_exp(token)
        >>> isinstance(exp, datetime) if exp else True
        True
    """
    try:
        # JWT format: header.payload.signature
        parts = token.split(".")
        if len(parts) != 3:
            return None

        # Decode payload (add padding if needed)
        payload = parts[1]
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += "=" * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)

        exp_timestamp = data.get("exp")
        if exp_timestamp is None:
            return None

        return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    except Exception:
        return None


def to_fhir_json(model):
    """Convert a Pydantic FHIR model to JSON-compatible dict.

    This helper converts Pydantic FHIR models to dictionaries suitable for
    sending to the Medplum API. It uses field aliases (FHIR's camelCase naming)
    and excludes None values to keep payloads clean.

    Args:
        model: Pydantic FHIR model instance or dict

    Returns:
        Dict with FHIR field names (aliases) and None values excluded

    Example:
        >>> from pymedplum.fhir.patient import Patient
        >>> patient = Patient(name=[HumanName(given=["John"], family="Doe")])
        >>> json_data = to_fhir_json(patient)
        >>> # json_data uses camelCase FHIR field names
    """
    if isinstance(model, dict):
        return model
    return model.model_dump(by_alias=True, exclude_none=True)
