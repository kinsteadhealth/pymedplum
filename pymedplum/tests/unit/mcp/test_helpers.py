"""Tests for internal helper functions."""

import os
from unittest.mock import patch

import pytest

from pymedplum.mcp.server import (
    _annotate_response,
    _collect_refs,
    _get_fhir_model,
    _is_read_only,
    _validate_on_behalf_of,
    _validate_resource,
)


class TestGetFhirModel:
    def test_known_resource_type(self):
        model = _get_fhir_model("Patient")
        assert model is not None
        assert model.__name__ == "Patient"

    def test_known_data_type(self):
        model = _get_fhir_model("HumanName")
        assert model is not None

    def test_medplum_specific_type(self):
        model = _get_fhir_model("Bot")
        assert model is not None

    def test_unknown_type_returns_none(self):
        assert _get_fhir_model("NonExistentType") is None

    def test_empty_string_returns_none(self):
        assert _get_fhir_model("") is None


class TestCollectRefs:
    def test_finds_refs_in_dict(self):
        schema = {
            "properties": {
                "name": {"$ref": "#/$defs/HumanName"},
                "id": {"type": "string"},
            }
        }
        refs: set[str] = set()
        _collect_refs(schema, refs)
        assert refs == {"HumanName"}

    def test_finds_refs_in_nested_lists(self):
        schema = {
            "anyOf": [
                {"items": {"$ref": "#/$defs/Extension"}},
                {"type": "null"},
            ]
        }
        refs: set[str] = set()
        _collect_refs(schema, refs)
        assert refs == {"Extension"}

    def test_no_refs(self):
        refs: set[str] = set()
        _collect_refs({"type": "string"}, refs)
        assert refs == set()

    def test_multiple_refs(self):
        schema = {
            "properties": {
                "a": {"$ref": "#/$defs/TypeA"},
                "b": {"$ref": "#/$defs/TypeB"},
            }
        }
        refs: set[str] = set()
        _collect_refs(schema, refs)
        assert refs == {"TypeA", "TypeB"}


class TestAnnotateResponse:
    def test_adds_hints_for_known_type(self):
        result = {"resourceType": "Patient", "id": "123"}
        annotated = _annotate_response(result)
        assert annotated["_response_type"] == "Patient"
        assert "get_resource_schema" in annotated["_schema_hint"]

    def test_skips_unknown_type(self):
        result = {"resourceType": "UnknownType123"}
        annotated = _annotate_response(result)
        assert "_response_type" not in annotated

    def test_skips_missing_resource_type(self):
        result = {"id": "123"}
        annotated = _annotate_response(result)
        assert "_response_type" not in annotated

    def test_returns_same_dict(self):
        result = {"resourceType": "Patient"}
        assert _annotate_response(result) is result


class TestValidateResource:
    def test_valid_patient_passes(self):
        _validate_resource({"resourceType": "Patient", "gender": "male"})

    def test_invalid_gender_raises(self):
        with pytest.raises(ValueError, match="FHIR Patient validation failed"):
            _validate_resource({"resourceType": "Patient", "gender": "invalid_value"})

    def test_error_includes_schema_hint(self):
        with pytest.raises(ValueError, match="get_resource_schema"):
            _validate_resource({"resourceType": "Patient", "birthDate": 12345})

    def test_unknown_type_passes_silently(self):
        _validate_resource({"resourceType": "UnknownType", "foo": "bar"})

    def test_missing_resource_type_passes(self):
        _validate_resource({"foo": "bar"})

    def test_empty_dict_passes(self):
        _validate_resource({})


class TestValidateOnBehalfOf:
    def test_bare_uuid(self):
        result = _validate_on_behalf_of("550e8400-e29b-41d4-a716-446655440000")
        assert result == "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"

    def test_full_reference(self):
        result = _validate_on_behalf_of(
            "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"
        )
        assert result == "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"

    def test_strips_whitespace(self):
        result = _validate_on_behalf_of("  550e8400-e29b-41d4-a716-446655440000  ")
        assert result == "ProjectMembership/550e8400-e29b-41d4-a716-446655440000"

    def test_case_insensitive_uuid(self):
        result = _validate_on_behalf_of("550E8400-E29B-41D4-A716-446655440000")
        assert result == "ProjectMembership/550E8400-E29B-41D4-A716-446655440000"

    def test_rejects_empty_string(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_on_behalf_of("")

    def test_rejects_non_uuid(self):
        with pytest.raises(ValueError, match="Invalid ProjectMembership"):
            _validate_on_behalf_of("not-a-uuid")

    def test_rejects_partial_uuid(self):
        with pytest.raises(ValueError, match="Invalid ProjectMembership"):
            _validate_on_behalf_of("550e8400-e29b-41d4")

    def test_rejects_garbage(self):
        with pytest.raises(ValueError, match="Invalid ProjectMembership"):
            _validate_on_behalf_of("garbage")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_on_behalf_of("   ")


class TestIsReadOnly:
    def test_true_values(self):
        for val in ("true", "True", "TRUE", "1", "yes"):
            with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": val}):
                assert _is_read_only() is True

    def test_false_values(self):
        for val in ("false", "0", "no", "anything"):
            with patch.dict(os.environ, {"MEDPLUM_READ_ONLY": val}):
                assert _is_read_only() is False

    def test_unset_is_false(self):
        with patch.dict(os.environ, {}, clear=True):
            assert _is_read_only() is False
