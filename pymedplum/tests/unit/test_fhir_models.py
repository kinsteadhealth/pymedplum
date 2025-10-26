"""Unit tests for generated FHIR models.

Tests the Pydantic models generated from Medplum TypeScript definitions.
"""

import pytest
from pydantic import ValidationError

from pymedplum.fhir.address import Address
from pymedplum.fhir.bundle import Bundle, BundleEntry
from pymedplum.fhir.codeableconcept import CodeableConcept
from pymedplum.fhir.coding import Coding
from pymedplum.fhir.contactpoint import ContactPoint
from pymedplum.fhir.humanname import HumanName
from pymedplum.fhir.identifier import Identifier
from pymedplum.fhir.organization import Organization
from pymedplum.fhir.patient import Patient
from pymedplum.fhir.practitioner import Practitioner
from pymedplum.fhir.reference import Reference


# ============================================================================
# Basic Model Tests
# ============================================================================


def test_patient_minimal():
    """Test creating a minimal Patient resource."""
    patient = Patient()

    assert patient.resource_type == "Patient"
    assert patient.name is None
    assert patient.gender is None


def test_patient_with_name():
    """Test creating a Patient with a name."""
    name = HumanName(given=["John", "Q"], family="Doe")
    patient = Patient(name=[name])

    assert len(patient.name) == 1
    assert patient.name[0].given == ["John", "Q"]
    assert patient.name[0].family == "Doe"


def test_patient_with_gender():
    """Test creating a Patient with gender."""
    patient = Patient(gender="male")

    assert patient.gender == "male"


def test_patient_full_example():
    """Test creating a complete Patient resource."""
    patient = Patient(
        name=[HumanName(given=["Alice"], family="Smith")],
        gender="female",
        identifier=[Identifier(system="http://example.org/mrn", value="12345")],
        address=[
            Address(
                line=["123 Main St"],
                city="Springfield",
                state="IL",
                postal_code="62701",
                country="US",
            )
        ],
        telecom=[ContactPoint(system="phone", value="555-1234", use="home")],
    )

    assert patient.resource_type == "Patient"
    assert patient.name[0].given == ["Alice"]
    assert patient.gender == "female"
    assert patient.identifier[0].value == "12345"
    assert patient.address[0].city == "Springfield"
    assert patient.telecom[0].value == "555-1234"


# ============================================================================
# Practitioner Tests
# ============================================================================


def test_practitioner_minimal():
    """Test creating a minimal Practitioner resource."""
    practitioner = Practitioner()

    assert practitioner.resource_type == "Practitioner"


def test_practitioner_with_name():
    """Test creating a Practitioner with a name."""
    practitioner = Practitioner(name=[HumanName(given=["Jane"], family="Doctor")])

    assert practitioner.name[0].given == ["Jane"]
    assert practitioner.name[0].family == "Doctor"


# ============================================================================
# Organization Tests
# ============================================================================


def test_organization_minimal():
    """Test creating a minimal Organization resource."""
    org = Organization()

    assert org.resource_type == "Organization"


def test_organization_with_name():
    """Test creating an Organization with a name."""
    org = Organization(name="Test Hospital")

    assert org.name == "Test Hospital"


def test_organization_with_identifier():
    """Test creating an Organization with identifier."""
    org = Organization(
        name="Test Clinic",
        identifier=[Identifier(system="http://example.org/npi", value="1234567890")],
    )

    assert org.name == "Test Clinic"
    assert org.identifier[0].value == "1234567890"


# ============================================================================
# Complex Type Tests
# ============================================================================


def test_human_name_simple():
    """Test creating a simple HumanName."""
    name = HumanName(given=["John"], family="Doe")

    assert name.given == ["John"]
    assert name.family == "Doe"
    assert name.use is None


def test_human_name_with_prefix_suffix():
    """Test creating a HumanName with prefix and suffix."""
    name = HumanName(
        prefix=["Dr."], given=["Jane"], family="Smith", suffix=["MD", "PhD"]
    )

    assert name.prefix == ["Dr."]
    assert name.suffix == ["MD", "PhD"]


def test_identifier_simple():
    """Test creating a simple Identifier."""
    identifier = Identifier(system="http://example.org/id", value="123456")

    assert identifier.system == "http://example.org/id"
    assert identifier.value == "123456"


def test_identifier_with_type():
    """Test creating an Identifier with type."""
    identifier = Identifier(
        system="http://example.org/mrn",
        value="MRN-123",
        type=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="MR",
                    display="Medical Record Number",
                )
            ]
        ),
    )

    assert identifier.type.coding[0].code == "MR"


def test_codeable_concept_simple():
    """Test creating a simple CodeableConcept."""
    concept = CodeableConcept(
        coding=[
            Coding(
                system="http://snomed.info/sct", code="38341003", display="Hypertension"
            )
        ],
        text="High Blood Pressure",
    )

    assert concept.coding[0].code == "38341003"
    assert concept.text == "High Blood Pressure"


def test_address_simple():
    """Test creating a simple Address."""
    address = Address(
        line=["456 Elm St", "Apt 2B"], city="Boston", state="MA", postal_code="02101"
    )

    assert address.line == ["456 Elm St", "Apt 2B"]
    assert address.city == "Boston"


def test_contact_point_phone():
    """Test creating a phone ContactPoint."""
    contact = ContactPoint(system="phone", value="555-9876", use="work")

    assert contact.system == "phone"
    assert contact.value == "555-9876"
    assert contact.use == "work"


def test_contact_point_email():
    """Test creating an email ContactPoint."""
    contact = ContactPoint(system="email", value="john.doe@example.com")

    assert contact.system == "email"
    assert contact.value == "john.doe@example.com"


# ============================================================================
# Reference Tests
# ============================================================================


def test_reference_simple():
    """Test creating a simple Reference."""
    ref = Reference(reference="Patient/123")

    assert ref.reference == "Patient/123"


def test_reference_with_display():
    """Test creating a Reference with display."""
    ref = Reference(reference="Practitioner/456", display="Dr. Jane Smith")

    assert ref.reference == "Practitioner/456"
    assert ref.display == "Dr. Jane Smith"


# ============================================================================
# Bundle Tests
# ============================================================================


def test_bundle_minimal():
    """Test creating a minimal Bundle."""
    bundle = Bundle(type="searchset")

    assert bundle.resource_type == "Bundle"
    assert bundle.type == "searchset"


def test_bundle_with_entries():
    """Test creating a Bundle with entries."""
    patient = Patient(name=[HumanName(given=["Test"], family="Patient")])

    bundle = Bundle(
        type="searchset",
        entry=[
            BundleEntry(resource=patient.model_dump(by_alias=True, exclude_none=True))
        ],
    )

    assert len(bundle.entry) == 1
    assert bundle.entry[0].resource["resourceType"] == "Patient"


# ============================================================================
# Validation Tests
# ============================================================================


def test_patient_rejects_invalid_gender():
    """Test that Patient rejects invalid gender values."""
    # Pydantic validates Literal types on creation
    with pytest.raises(ValidationError) as exc_info:
        Patient(gender="invalid-gender")

    assert "gender" in str(exc_info.value)
    assert "literal_error" in str(exc_info.value)


def test_model_excludes_none_in_dict():
    """Test that model_dump excludes None values."""
    patient = Patient(
        name=[HumanName(given=["Test"], family="User")], gender=None  # Explicitly None
    )

    data = patient.model_dump(exclude_none=True)

    assert "name" in data
    assert "gender" not in data


def test_model_serialization_to_json():
    """Test that models can be serialized to JSON-compatible dict."""
    patient = Patient(
        name=[HumanName(given=["John"], family="Doe")],
        gender="male",
        identifier=[Identifier(system="http://example.org/id", value="123")],
    )

    data = patient.model_dump(mode="json", by_alias=True, exclude_none=True)

    assert isinstance(data, dict)
    assert data["resourceType"] == "Patient"
    assert isinstance(data["name"], list)
    assert isinstance(data["name"][0], dict)


# ============================================================================
# Field Alias Tests
# ============================================================================


def test_resource_type_alias():
    """Test that resourceType field alias works."""
    # Creating with Python field name
    patient = Patient()
    assert patient.resource_type == "Patient"

    # Should also work with alias in dict
    data = patient.model_dump(by_alias=True)
    assert "resourceType" in data


def test_field_aliases_in_complex_types():
    """Test that field aliases work in complex types."""
    name = HumanName(given=["Test"], family="User")

    # Serialize with aliases
    data = name.model_dump(by_alias=True, exclude_none=True)

    assert isinstance(data, dict)
    assert "given" in data
    assert "family" in data


# ============================================================================
# Integration Tests
# ============================================================================


def test_creating_patient_from_dict():
    """Test creating a Patient from a dictionary."""
    data = {
        "resourceType": "Patient",
        "name": [{"given": ["Alice"], "family": "Wonder"}],
        "gender": "female",
    }

    patient = Patient(**data)

    assert patient.name[0].given == ["Alice"]
    assert patient.gender == "female"


def test_round_trip_serialization():
    """Test that a model can be serialized and deserialized."""
    original = Patient(name=[HumanName(given=["Bob"], family="Builder")], gender="male")

    # Serialize
    data = original.model_dump(by_alias=True, exclude_none=True)

    # Deserialize
    reconstructed = Patient(**data)

    assert reconstructed.name[0].given == original.name[0].given
    assert reconstructed.gender == original.gender


def test_nested_model_creation():
    """Test creating nested models."""
    patient = Patient(
        name=[
            HumanName(given=["First"], family="Name"),
            HumanName(given=["Second"], family="Name", use="nickname"),
        ],
        identifier=[
            Identifier(system="sys1", value="val1"),
            Identifier(system="sys2", value="val2"),
        ],
    )

    assert len(patient.name) == 2
    assert len(patient.identifier) == 2
    assert patient.name[1].use == "nickname"


# ============================================================================
# Edge Cases
# ============================================================================


def test_empty_lists():
    """Test that empty lists are handled correctly."""
    patient = Patient(name=[], identifier=[])

    data = patient.model_dump(exclude_none=True)

    # Empty lists should be included (they're not None)
    assert "name" in data
    assert data["name"] == []


def test_optional_fields_default_to_none():
    """Test that optional fields default to None."""
    patient = Patient()

    assert patient.name is None
    assert patient.gender is None
    assert patient.birth_date is None
