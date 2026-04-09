"""Unit tests for FHIR helper functions."""

from pydantic import BaseModel

from pymedplum.fhir import HumanName, Patient
from pymedplum.helpers import to_fhir_json


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
