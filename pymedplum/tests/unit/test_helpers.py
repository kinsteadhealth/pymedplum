"""Unit tests for FHIR helper functions."""

from pydantic import BaseModel

from pymedplum.fhir import CodeableConcept, Coding, HumanName, Patient, Reference
from pymedplum.helpers import (
    coding_parts,
    get_code_by_system,
    resolve_id,
    to_fhir_json,
)


# Test fixtures for to_fhir_json
class MockPydanticV2Model(BaseModel):
    """Mock model for testing Pydantic v2."""

    name: str
    value: int
    optional_field: str | None = None

    class Config:
        populate_by_name = True


# Tests for to_fhir_json
def test_to_fhir_json_with_pydantic_model():
    """Test converting Pydantic model to JSON."""
    model = MockPydanticV2Model(name="test", value=42)
    result = to_fhir_json(model)

    assert isinstance(result, dict)
    assert result["name"] == "test"
    assert result["value"] == 42
    assert "optional_field" not in result  # Should exclude None values


def test_to_fhir_json_with_fhir_model():
    """Test converting FHIR Pydantic model to JSON."""
    patient = Patient(name=[HumanName(given=["John"], family="Doe")], gender="male")
    result = to_fhir_json(patient)

    assert isinstance(result, dict)
    assert result["resourceType"] == "Patient"
    assert result["name"][0]["given"] == ["John"]
    assert result["gender"] == "male"


def test_to_fhir_json_with_dict():
    """Test that dict input is returned as-is."""
    input_dict = {"resourceType": "Patient", "id": "123"}
    result = to_fhir_json(input_dict)

    assert result is input_dict
    assert result == {"resourceType": "Patient", "id": "123"}


def test_to_fhir_json_excludes_none():
    """Test that None values are excluded from output."""
    model = MockPydanticV2Model(name="test", value=42, optional_field=None)
    result = to_fhir_json(model)

    assert "optional_field" not in result


def test_to_fhir_json_uses_aliases():
    """Test that field aliases are used in output."""
    patient = Patient(name=[HumanName(given=["Test"], family="User")])
    result = to_fhir_json(patient)

    # Should use 'resourceType' (alias) not 'resource_type' (Python name)
    assert "resourceType" in result
    assert "resource_type" not in result


# Tests for coding_parts
ICD10 = "http://hl7.org/fhir/sid/icd-10-cm"


def test_coding_parts_full_concept():
    concept = {
        "coding": [{"code": "E11.9", "system": ICD10, "display": "Type 2 diabetes"}],
        "text": "DM2",
    }
    assert coding_parts(concept) == ("E11.9", ICD10, "Type 2 diabetes", "DM2")


def test_coding_parts_uses_first_coding_only():
    concept = {"coding": [{"code": "a"}, {"code": "b"}]}
    assert coding_parts(concept) == ("a", None, None, None)


def test_coding_parts_text_only_no_coding():
    assert coding_parts({"text": "free text"}) == (None, None, None, "free text")


def test_coding_parts_empty_concept():
    assert coding_parts({}) == (None, None, None, None)


def test_coding_parts_none():
    assert coding_parts(None) == (None, None, None, None)


def test_coding_parts_malformed_coding_not_a_list():
    # `coding` present but not a list — degrade, don't raise.
    assert coding_parts({"coding": "nope", "text": "t"}) == (
        None,
        None,
        None,
        "t",
    )


def test_coding_parts_malformed_first_not_a_dict():
    assert coding_parts({"coding": ["nope"]}) == (None, None, None, None)


def test_coding_parts_malformed_first_is_none():
    assert coding_parts({"coding": [None]}) == (None, None, None, None)


def test_coding_parts_pydantic_model():
    concept = CodeableConcept(
        coding=[Coding(code="E11.9", system=ICD10, display="Type 2 diabetes")],
        text="DM2",
    )
    assert coding_parts(concept) == ("E11.9", ICD10, "Type 2 diabetes", "DM2")


# Tests for get_code_by_system
def test_get_code_by_system_finds_matching_system():
    concept = {
        "coding": [
            {"system": "http://snomed.info/sct", "code": "44054006"},
            {"system": ICD10, "code": "E11.9"},
        ]
    }
    assert get_code_by_system(concept, ICD10) == "E11.9"


def test_get_code_by_system_not_found():
    concept = {"coding": [{"system": "http://snomed.info/sct", "code": "44054006"}]}
    assert get_code_by_system(concept, ICD10) is None


def test_get_code_by_system_none_concept():
    assert get_code_by_system(None, ICD10) is None


def test_get_code_by_system_pydantic_model():
    concept = CodeableConcept(coding=[Coding(system=ICD10, code="E11.9")])
    assert get_code_by_system(concept, ICD10) == "E11.9"


# Tests for resolve_id
def test_resolve_id_from_reference_string():
    assert resolve_id("Patient/123") == "123"


def test_resolve_id_from_bare_id():
    assert resolve_id("123") == "123"


def test_resolve_id_from_reference_dict():
    assert resolve_id({"reference": "Patient/abc-123"}) == "abc-123"


def test_resolve_id_from_reference_model():
    assert resolve_id(Reference(reference="Patient/xyz")) == "xyz"


def test_resolve_id_from_resource_model():
    assert resolve_id(Patient(id="pat-1")) == "pat-1"


def test_resolve_id_none():
    assert resolve_id(None) is None


def test_resolve_id_empty_string():
    assert resolve_id("") is None


def test_resolve_id_empty_dict():
    assert resolve_id({}) is None


def test_resolve_id_trailing_slash_only():
    assert resolve_id("Patient/") is None
