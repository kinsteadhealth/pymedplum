from typing import Any

from pydantic import BaseModel


def to_fhir_json(resource: Any) -> dict[str, Any]:
    """Convert FHIR resource to JSON using Pydantic v2.

    Args:
        resource: FHIR resource instance or dict

    Returns:
        JSON-serializable dict
    """
    if isinstance(resource, BaseModel):
        return resource.model_dump(by_alias=True, exclude_none=True, mode="json")
    return resource


def to_portable(
    resource: dict[str, Any],
    org_ext_url: str = "https://example.org/fhir/StructureDefinition/orgLink",
) -> dict[str, Any]:
    """Convert vendor-specific Medplum meta fields to portable FHIR extensions.
    Removes non-standard meta fields like accounts, author, project, account, compartment.
    Useful for strict FHIR validation with fhir.resources.

    Args:
        resource: FHIR resource dict
        org_ext_url: URL for the organization extension

    Returns:
        Modified resource dict with portable extensions
    """
    r = dict(resource)
    m = r.get("meta")

    if isinstance(m, dict):
        ext = list(m.get("extension", []))

        if "accounts" in m:
            for a in m["accounts"]:
                ref = a.get("reference")
                if ref:
                    ext.append(
                        {"url": org_ext_url, "valueReference": {"reference": ref}}
                    )

        vendor_fields = {
            "accounts",
            "author",
            "project",
            "account",
            "compartment",
            "onBehalfOf",
        }
        m = {k: v for k, v in m.items() if k not in vendor_fields}

        if ext:
            m["extension"] = ext
        r["meta"] = m

    if r.get("resourceType") == "Bundle":
        r["entry"] = [
            (
                {**e, "resource": to_portable(e["resource"], org_ext_url)}
                if isinstance(e.get("resource"), dict)
                else e
            )
            for e in r.get("entry", [])
        ]

    return r
