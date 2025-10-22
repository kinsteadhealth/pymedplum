"""Unit tests for FHIR helper functions"""

from pydantic import BaseModel

from pymedplum.helpers.fhir import to_fhir_json, to_portable


# Test fixtures for to_fhir_json
class MockPydanticV2Model(BaseModel):
    """Mock model for testing Pydantic v2"""

    name: str
    value: int
    optional_field: str | None = None

    class Config:
        populate_by_name = True


class MockPydanticV1Model(BaseModel):
    """Mock model for testing Pydantic v1 fallback"""

    name: str
    value: int

    def model_dump(self):
        # Simulate v1 by raising an error on v2 method
        raise AttributeError("model_dump not available")


# Tests for to_fhir_json
def test_to_fhir_json_with_pydantic_model():
    """Test converting Pydantic model to JSON"""
    model = MockPydanticV2Model(name="test", value=42)
    result = to_fhir_json(model)

    assert isinstance(result, dict)
    assert result["name"] == "test"
    assert result["value"] == 42
    assert "optional_field" not in result  # Should exclude None values


def test_to_fhir_json_with_dict():
    """Test that dict input is returned as-is"""
    input_dict = {"resourceType": "Patient", "id": "123"}
    result = to_fhir_json(input_dict)

    assert result is input_dict
    assert result == {"resourceType": "Patient", "id": "123"}


def test_to_fhir_json_excludes_none():
    """Test that None values are excluded from output"""
    model = MockPydanticV2Model(name="test", value=42, optional_field=None)
    result = to_fhir_json(model)

    assert "optional_field" not in result


# Tests for to_portable
def test_to_portable_removes_vendor_fields():
    """Test that Medplum-specific meta fields are removed"""
    resource = {
        "resourceType": "Patient",
        "id": "123",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2024-01-01T00:00:00Z",
            "accounts": [{"reference": "Organization/org1"}],
            "author": {"reference": "ClientApplication/app1"},
            "project": "project-123",
            "account": {"reference": "Organization/org1"},
            "compartment": [{"reference": "Patient/123"}],
            "onBehalfOf": {"reference": "ProjectMembership/pm1"},
        },
    }

    result = to_portable(resource)

    # Standard FHIR meta fields should remain
    assert result["meta"]["versionId"] == "1"
    assert result["meta"]["lastUpdated"] == "2024-01-01T00:00:00Z"

    # Vendor fields should be removed
    assert "accounts" not in result["meta"]
    assert "author" not in result["meta"]
    assert "project" not in result["meta"]
    assert "account" not in result["meta"]
    assert "compartment" not in result["meta"]
    assert "onBehalfOf" not in result["meta"]


def test_to_portable_converts_accounts_to_extensions():
    """Test that accounts are converted to extensions"""
    resource = {
        "resourceType": "Patient",
        "id": "123",
        "meta": {
            "accounts": [
                {"reference": "Organization/org1"},
                {"reference": "Organization/org2"},
            ]
        },
    }

    result = to_portable(resource)

    # Should have extensions for each account
    assert "extension" in result["meta"]
    assert len(result["meta"]["extension"]) == 2

    ext1 = result["meta"]["extension"][0]
    assert ext1["url"] == "https://example.org/fhir/StructureDefinition/orgLink"
    assert ext1["valueReference"]["reference"] == "Organization/org1"

    ext2 = result["meta"]["extension"][1]
    assert ext2["url"] == "https://example.org/fhir/StructureDefinition/orgLink"
    assert ext2["valueReference"]["reference"] == "Organization/org2"


def test_to_portable_custom_extension_url():
    """Test that custom extension URL is used"""
    resource = {
        "resourceType": "Patient",
        "id": "123",
        "meta": {"accounts": [{"reference": "Organization/org1"}]},
    }

    custom_url = "https://custom.org/fhir/ext/org"
    result = to_portable(resource, org_ext_url=custom_url)

    assert result["meta"]["extension"][0]["url"] == custom_url


def test_to_portable_preserves_existing_extensions():
    """Test that existing extensions are preserved"""
    resource = {
        "resourceType": "Patient",
        "id": "123",
        "meta": {
            "extension": [{"url": "https://existing.org/ext", "valueString": "test"}],
            "accounts": [{"reference": "Organization/org1"}],
        },
    }

    result = to_portable(resource)

    # Should have both existing and new extensions
    assert len(result["meta"]["extension"]) == 2

    # Existing extension should be first
    assert result["meta"]["extension"][0]["url"] == "https://existing.org/ext"
    assert result["meta"]["extension"][0]["valueString"] == "test"

    # New extension should be second
    assert (
        result["meta"]["extension"][1]["url"]
        == "https://example.org/fhir/StructureDefinition/orgLink"
    )


def test_to_portable_handles_bundle_entries():
    """Test that Bundle entries are recursively processed"""
    bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "p1",
                    "meta": {
                        "accounts": [{"reference": "Organization/org1"}],
                        "author": {"reference": "ClientApplication/app1"},
                    },
                }
            },
            {
                "resource": {
                    "resourceType": "Practitioner",
                    "id": "pr1",
                    "meta": {
                        "project": "project-123",
                    },
                }
            },
        ],
    }

    result = to_portable(bundle)

    # Check first entry
    patient_meta = result["entry"][0]["resource"]["meta"]
    assert "accounts" not in patient_meta
    assert "author" not in patient_meta
    assert "extension" in patient_meta  # accounts converted to extension

    # Check second entry
    practitioner_meta = result["entry"][1]["resource"]["meta"]
    assert "project" not in practitioner_meta


def test_to_portable_handles_missing_meta():
    """Test that resources without meta are handled gracefully"""
    resource = {
        "resourceType": "Patient",
        "id": "123",
        "name": [{"given": ["John"], "family": "Doe"}],
    }

    result = to_portable(resource)

    assert result == resource  # Should be unchanged


def test_to_portable_handles_empty_meta():
    """Test that empty meta objects are handled"""
    resource = {"resourceType": "Patient", "id": "123", "meta": {}}

    result = to_portable(resource)

    assert result["meta"] == {}


def test_to_portable_skips_accounts_without_reference():
    """Test that accounts without reference are skipped"""
    resource = {
        "resourceType": "Patient",
        "id": "123",
        "meta": {
            "accounts": [
                {"reference": "Organization/org1"},
                {"display": "No Reference"},  # Missing reference
                {"reference": "Organization/org2"},
            ]
        },
    }

    result = to_portable(resource)

    # Should only have 2 extensions (skipping the one without reference)
    assert len(result["meta"]["extension"]) == 2
    assert (
        result["meta"]["extension"][0]["valueReference"]["reference"]
        == "Organization/org1"
    )
    assert (
        result["meta"]["extension"][1]["valueReference"]["reference"]
        == "Organization/org2"
    )


def test_to_portable_does_not_mutate_original():
    """Test that the original resource is not modified"""
    original = {
        "resourceType": "Patient",
        "id": "123",
        "meta": {
            "accounts": [{"reference": "Organization/org1"}],
            "author": {"reference": "ClientApplication/app1"},
        },
    }

    # Make a copy to compare later
    original_copy = dict(original)
    original_copy["meta"] = dict(original["meta"])

    result = to_portable(original)

    # Original should be unchanged
    assert original == original_copy
    assert "accounts" in original["meta"]
    assert "author" in original["meta"]

    # Result should have transformations
    assert "accounts" not in result["meta"]
    assert "author" not in result["meta"]
