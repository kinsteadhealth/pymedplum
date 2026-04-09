"""Unit tests for account helpers and _apply_accounts."""

import pytest

from pymedplum import MedplumClient
from pymedplum._base import BaseClient
from pymedplum.helpers import get_resource_accounts, resource_has_account


def test_apply_accounts_single_string():
    result = BaseClient._apply_accounts(
        {"resourceType": "Patient"}, "Organization/org-1"
    )
    assert result["meta"]["accounts"] == [{"reference": "Organization/org-1"}]


def test_apply_accounts_list():
    result = BaseClient._apply_accounts(
        {"resourceType": "Patient"},
        ["Organization/org-1", "Practitioner/prac-1"],
    )
    assert len(result["meta"]["accounts"]) == 2
    refs = {acc["reference"] for acc in result["meta"]["accounts"]}
    assert refs == {"Organization/org-1", "Practitioner/prac-1"}


def test_apply_accounts_dedup_simple():
    resource = {
        "resourceType": "Patient",
        "meta": {"accounts": [{"reference": "Organization/org-1"}]},
    }
    result = BaseClient._apply_accounts(resource, "Organization/org-1")
    assert len(result["meta"]["accounts"]) == 1


def test_apply_accounts_dedup_with_extra_fields():
    """Dedup should work even if existing accounts have extra fields like display."""
    resource = {
        "resourceType": "Patient",
        "meta": {
            "accounts": [{"reference": "Organization/org-1", "display": "Clinic A"}]
        },
    }
    result = BaseClient._apply_accounts(resource, "Organization/org-1")
    assert len(result["meta"]["accounts"]) == 1


def test_apply_accounts_empty_string_raises():
    with pytest.raises(ValueError, match="Invalid account reference"):
        BaseClient._apply_accounts({"resourceType": "Patient"}, "")


def test_apply_accounts_no_slash_raises():
    with pytest.raises(ValueError, match="Invalid account reference"):
        BaseClient._apply_accounts({"resourceType": "Patient"}, "Organization")


def test_apply_accounts_empty_list_adds_no_entries():
    resource = {"resourceType": "Patient"}
    result = BaseClient._apply_accounts(resource, [])
    assert result["meta"]["accounts"] == []


def test_apply_accounts_mutates_in_place():
    resource = {"resourceType": "Patient"}
    result = BaseClient._apply_accounts(resource, "Organization/org-1")
    assert result is resource


def test_get_resource_accounts_basic():
    resource = {
        "meta": {
            "accounts": [
                {"reference": "Organization/org-1"},
                {"reference": "Practitioner/prac-1"},
            ]
        }
    }
    assert get_resource_accounts(resource) == [
        "Organization/org-1",
        "Practitioner/prac-1",
    ]


def test_get_resource_accounts_no_meta():
    assert get_resource_accounts({"resourceType": "Patient"}) == []


def test_get_resource_accounts_empty_accounts():
    assert get_resource_accounts({"meta": {"accounts": []}}) == []


def test_get_resource_accounts_skips_malformed():
    resource = {
        "meta": {
            "accounts": [
                {"reference": "Organization/org-1"},
                {"bad": "entry"},
                "not-a-dict",
            ]
        }
    }
    assert get_resource_accounts(resource) == ["Organization/org-1"]


def test_resource_has_account_true():
    resource = {"meta": {"accounts": [{"reference": "Organization/org-1"}]}}
    assert resource_has_account(resource, "Organization/org-1")


def test_resource_has_account_false():
    resource = {"meta": {"accounts": [{"reference": "Organization/org-1"}]}}
    assert not resource_has_account(resource, "Organization/org-2")


def test_resource_has_account_no_meta():
    assert not resource_has_account({"resourceType": "Patient"}, "Org/1")


def test_set_accounts_prefer_async_without_propagate_raises():
    client = MedplumClient()
    with pytest.raises(ValueError, match="prefer_async only takes effect"):
        client.set_accounts("Patient/123", "Organization/org-1", prefer_async=True)
