"""Unit tests for the FHIR extension helpers (dicts and models)."""

from __future__ import annotations

from typing import Any

import pytest

from pymedplum import (
    SERVICE_TYPE_REFERENCE_URL,
    get_extension,
    get_extension_value,
    get_extensions,
    get_nested_value,
    read_service_type_references,
    remove_extension,
    service_type_reference_extension,
    set_extension,
    upsert_extension,
)
from pymedplum.fhir import Patient, Schedule

_URL = "https://example.org/flag"
_OTHER_URL = "https://example.org/other"


def _dict_element() -> dict[str, Any]:
    return {
        "resourceType": "Patient",
        "extension": [
            {"url": _URL, "valueBoolean": True},
            {"url": _OTHER_URL, "valueString": "keep"},
        ],
    }


def test_get_extension_and_value_on_dict() -> None:
    element = _dict_element()
    assert get_extension(element, _URL) == {"url": _URL, "valueBoolean": True}
    assert get_extension(element, "https://example.org/missing") is None
    assert get_extension_value(element, _URL) is True
    assert get_extension_value(element, _OTHER_URL) == "keep"


def test_get_extensions_returns_all_matches() -> None:
    element = {
        "extension": [
            {"url": _URL, "valueInteger": 1},
            {"url": _URL, "valueInteger": 2},
        ]
    }
    assert [e["valueInteger"] for e in get_extensions(element, _URL)] == [1, 2]
    assert get_extensions(element, _OTHER_URL) == []


def test_set_extension_replaces_then_appends() -> None:
    element = _dict_element()
    set_extension(element, _URL, valueBoolean=False)
    assert get_extension_value(element, _URL) is False
    assert len(element["extension"]) == 2

    set_extension(element, "https://example.org/new", valueString="x")
    assert get_extension_value(element, "https://example.org/new") == "x"
    assert len(element["extension"]) == 3


def test_set_extension_accepts_snake_case_and_rejects_arity() -> None:
    element: dict[str, Any] = {}
    set_extension(element, _URL, value_string="snake")
    assert element["extension"] == [{"url": _URL, "valueString": "snake"}]

    with pytest.raises(ValueError, match="exactly one"):
        set_extension(element, _URL, valueString="a", valueBoolean=True)
    with pytest.raises(ValueError, match="exactly one"):
        set_extension(element, _URL)


def test_set_extension_rejects_invalid_value_keywords() -> None:
    """A typo'd or non-value[x] keyword must fail here, not surface
    later as a server rejection of a malformed extension."""
    element: dict[str, Any] = {}

    with pytest.raises(ValueError, match="not a FHIR Extension value"):
        set_extension(element, _URL, valueBooleann=True)
    with pytest.raises(ValueError, match="not a FHIR Extension value"):
        set_extension(element, _URL, foo="x")
    with pytest.raises(ValueError, match="must not be None"):
        set_extension(element, _URL, valueString=None)

    assert "extension" not in element


def test_set_extension_collapses_duplicate_urls() -> None:
    element = {
        "extension": [
            {"url": _URL, "valueInteger": 1},
            {"url": _OTHER_URL, "valueString": "keep"},
            {"url": _URL, "valueInteger": 2},
        ]
    }
    set_extension(element, _URL, valueInteger=3)
    assert element["extension"] == [
        {"url": _URL, "valueInteger": 3},
        {"url": _OTHER_URL, "valueString": "keep"},
    ]


def test_upsert_extension_keyed_merge() -> None:
    element = _dict_element()
    complex_ext = {
        "url": _URL,
        "extension": [{"url": "child", "valueCode": "c1"}],
    }
    upsert_extension(element, complex_ext, key_url=_URL)
    assert get_extension(element, _URL) == complex_ext

    appended = {"url": "https://example.org/new", "valueString": "n"}
    upsert_extension(element, appended, key_url="https://example.org/new")
    assert element["extension"][-1] == appended


def test_remove_extension() -> None:
    element = _dict_element()
    assert remove_extension(element, _URL) is True
    assert get_extension(element, _URL) is None
    assert remove_extension(element, _URL) is False

    assert remove_extension(element, _OTHER_URL) is True
    # An emptied list drops the key — FHIR JSON forbids empty arrays.
    assert "extension" not in element


def test_get_nested_value() -> None:
    ext = {
        "url": "https://example.org/complex",
        "extension": [
            {"url": "start", "valueDateTime": "2026-01-01T09:00:00Z"},
            {"url": "end", "valueDateTime": "2026-01-01T17:00:00Z"},
        ],
    }
    assert get_nested_value(ext, "start") == "2026-01-01T09:00:00Z"
    assert get_nested_value(ext, "missing") is None


def test_helpers_operate_on_models() -> None:
    patient = Patient(
        extension=[{"url": _URL, "valueBoolean": True}],
    )
    ext = get_extension(patient, _URL)
    assert ext is not None
    assert get_extension_value(patient, _URL) is True

    set_extension(patient, _URL, valueBoolean=False)
    assert get_extension_value(patient, _URL) is False

    set_extension(patient, _OTHER_URL, valueString="x")
    assert get_extension_value(patient, _OTHER_URL) == "x"

    assert remove_extension(patient, _URL) is True
    assert remove_extension(patient, _URL) is False
    assert remove_extension(patient, _OTHER_URL) is True
    assert patient.extension is None


def test_service_type_reference_extension_matches_medplum_shape() -> None:
    """Shape verified against Medplum's toCodeableReferenceLike
    (packages/server/src/util/servicetype.ts)."""
    concept = service_type_reference_extension("HealthcareService/hs-1")
    assert concept == {
        "extension": [
            {
                "url": "https://medplum.com/fhir/service-type-reference",
                "valueReference": {"reference": "HealthcareService/hs-1"},
            }
        ]
    }
    assert concept["extension"][0]["url"] == SERVICE_TYPE_REFERENCE_URL

    coding = {"system": "http://example.org/svc", "code": "intake"}
    with_codings = service_type_reference_extension(
        "HealthcareService/hs-1", codings=[coding]
    )
    assert with_codings["coding"] == [coding]

    with pytest.raises(ValueError, match="Invalid service reference"):
        service_type_reference_extension("not-a-reference")
    # The convention embeds a HealthcareService specifically — a mere
    # "/" is not enough (a Patient reference here would be meaningless).
    with pytest.raises(ValueError, match="HealthcareService"):
        service_type_reference_extension("Patient/123")
    with pytest.raises(ValueError, match="HealthcareService"):
        service_type_reference_extension("HealthcareService/")


def test_read_service_type_references_dict_and_model() -> None:
    slot = {
        "resourceType": "Slot",
        "serviceType": [
            service_type_reference_extension("HealthcareService/hs-1"),
            {"coding": [{"code": "untagged"}]},
            service_type_reference_extension("HealthcareService/hs-2"),
        ],
    }
    assert read_service_type_references(slot) == [
        "HealthcareService/hs-1",
        "HealthcareService/hs-2",
    ]

    schedule = Schedule(
        actor=[{"reference": "Practitioner/pr-1"}],
        service_type=[service_type_reference_extension("HealthcareService/hs-3")],
    )
    assert read_service_type_references(schedule) == ["HealthcareService/hs-3"]

    assert read_service_type_references({"resourceType": "Slot"}) == []
