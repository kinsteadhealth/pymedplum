"""Tests for the FHIR model rebuild functionality.

The rebuild system handles circular dependencies in FHIR models by:
1. Importing all modules to load all class definitions
2. Rebuilding all models after imports complete to resolve forward references
3. Allowing models to reference each other (e.g., Patient -> Meta, Observation -> Reference)

Note: These tests verify that rebuild has already happened successfully by
attempting to create model instances with forward-referenced types.
"""

import pytest
from pydantic import ValidationError

from pymedplum.fhir import Observation, Patient

# Import all models at module level after rebuild


def test_patient_with_nested_forward_references():
    """Test that Patient can be created with all nested forward-referenced types.

    This verifies the rebuild system successfully resolved forward references like:
    - Meta, Identifier, HumanName, Extension
    """

    patient = Patient(
        **{
            "resourceType": "Patient",
            "id": "rebuild-test-1",
            "meta": {"versionId": "1"},  # Meta forward reference
            "identifier": [{"value": "12345"}],  # Identifier forward reference
            "name": [{"family": "Test"}],  # HumanName forward reference
        }
    )

    assert patient.id == "rebuild-test-1"
    assert patient.meta.version_id == "1"
    assert patient.identifier[0].value == "12345"
    assert patient.name[0].family == "Test"


def test_observation_with_references():
    """Test Observation with Reference and Quantity forward references."""

    obs = Observation(
        **{
            "resourceType": "Observation",
            "id": "rebuild-test-2",
            "status": "final",
            "code": {"text": "Test"},
            "subject": {"reference": "Patient/123"},  # Reference forward ref
            "valueQuantity": {"value": 72, "unit": "bpm"},  # Quantity forward ref
        }
    )

    assert obs.status == "final"
    assert obs.subject.reference == "Patient/123"
    assert obs.value_quantity.value == 72


def test_deeply_nested_structures():
    """Test deeply nested forward references are resolved."""

    patient = Patient(
        **{
            "resourceType": "Patient",
            "id": "rebuild-test-3",
            "contact": [  # PatientContact forward ref
                {
                    "name": {"family": "Emergency"},  # HumanName forward ref
                    "telecom": [  # ContactPoint forward ref
                        {"system": "phone", "value": "911"}
                    ],
                }
            ],
        }
    )

    assert patient.contact[0].name.family == "Emergency"
    assert patient.contact[0].telecom[0].value == "911"


def test_model_has_proper_fields_after_rebuild():
    """Verify models have all fields properly defined after rebuild."""

    # Model should have Pydantic fields attribute
    assert hasattr(Patient, "model_fields")

    # Check for common fields
    assert "id" in Patient.model_fields
    assert "meta" in Patient.model_fields
    assert "identifier" in Patient.model_fields
    assert "name" in Patient.model_fields


def test_pydantic_validation_works():
    """Verify Pydantic validation works correctly after rebuild."""

    # Valid data should work
    patient = Patient(resourceType="Patient", id="test", active=True)
    assert patient.active is True

    # Invalid type should raise ValidationError
    with pytest.raises(ValidationError):
        Patient(resourceType="Patient", id="test", active="not-a-boolean")


def test_extension_types_work():
    """Test that Extension forward references work."""

    patient = Patient(
        **{
            "resourceType": "Patient",
            "id": "ext-test",
            "extension": [
                {
                    "url": "http://example.org/extension",
                    "valueString": "test value",
                }
            ],
        }
    )

    assert len(patient.extension) == 1
    assert patient.extension[0].url == "http://example.org/extension"
    assert patient.extension[0].value_string == "test value"


def test_codeable_concept_and_coding():
    """Test CodeableConcept and Coding forward references."""

    obs = Observation(
        **{
            "resourceType": "Observation",
            "id": "coding-test",
            "status": "final",
            "code": {  # CodeableConcept forward ref
                "coding": [  # Coding forward ref
                    {
                        "system": "http://loinc.org",
                        "code": "8867-4",
                        "display": "Heart rate",
                    }
                ]
            },
        }
    )

    assert len(obs.code.coding) == 1
    assert obs.code.coding[0].code == "8867-4"
    assert obs.code.coding[0].display == "Heart rate"


def test_multiple_resource_types_coexist():
    """Test that multiple resource types can be used together."""

    # Create both types - this tests that the namespace has all types
    patient = Patient(resourceType="Patient", id="p1")
    observation = Observation(
        resourceType="Observation", id="o1", status="final", code={"text": "Test"}
    )

    assert patient.id == "p1"
    assert observation.id == "o1"


def test_list_resource_does_not_shadow_builtin_list():
    """Importing `List` (FHIR resource) must not collide with the builtin
    `list` used inside the lazy loader's ``__getattr__`` — the
    `pymedplum.fhir.list` submodule must not shadow it.
    """
    from pymedplum.fhir import List

    lst = List(status="current", mode="working")
    assert lst.status == "current"
    assert lst.mode == "working"


def test_parameters_is_fully_defined():
    """Regression: `Parameters` imported but was not instantiable because the
    rebuild namespace did not include `Resource` (a runtime alias for
    MedplumFHIRBase).
    """
    from pymedplum.fhir import Parameters, Patient

    patient = Patient(name=[{"family": "RegressionTest"}])
    params = Parameters(parameter=[{"name": "patient", "resource": patient}])
    assert params.parameter[0].resource.name[0].family == "RegressionTest"


def test_complex_observation_with_many_types():
    """Test complex Observation using many different forward-referenced types."""

    obs = Observation(
        **{
            "resourceType": "Observation",
            "id": "complex",
            "meta": {"versionId": "1"},  # Meta
            "identifier": [{"value": "obs-123"}],  # Identifier
            "status": "final",
            "category": [  # CodeableConcept
                {"coding": [{"code": "vital-signs"}]}  # Coding
            ],
            "code": {"coding": [{"code": "test"}]},
            "subject": {"reference": "Patient/123"},  # Reference
            "valueQuantity": {"value": 72},  # Quantity
            "note": [{"text": "Test note"}],  # Annotation
        }
    )

    # All nested types should work
    assert obs.meta.version_id == "1"
    assert obs.identifier[0].value == "obs-123"
    assert obs.category[0].coding[0].code == "vital-signs"
    assert obs.subject.reference == "Patient/123"
    assert obs.value_quantity.value == 72
    assert obs.note[0].text == "Test note"
