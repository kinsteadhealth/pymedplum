"""Unit tests for account helpers and _apply_accounts."""

import pytest

from pymedplum import MedplumClient
from pymedplum._base import BaseClient
from pymedplum.helpers import (
    extract_account_references,
    get_resource_accounts,
    resource_has_account,
)


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


def test_apply_accounts_does_not_mutate_caller_dict():
    # to_fhir_json returns dict inputs by identity, so in-place writes
    # would leak meta.accounts into caller-owned templates and
    # accumulate across calls.
    resource = {"resourceType": "Patient"}
    result = BaseClient._apply_accounts(resource, "Organization/org-1")
    assert result is not resource
    assert resource == {"resourceType": "Patient"}
    assert result["meta"]["accounts"] == [{"reference": "Organization/org-1"}]


def test_apply_accounts_does_not_mutate_existing_meta():
    meta = {"accounts": [{"reference": "Organization/org-1"}]}
    resource = {"resourceType": "Patient", "meta": meta}
    result = BaseClient._apply_accounts(resource, "Organization/org-2")
    assert meta == {"accounts": [{"reference": "Organization/org-1"}]}
    assert result["meta"]["accounts"] == [
        {"reference": "Organization/org-1"},
        {"reference": "Organization/org-2"},
    ]


def test_stamp_bundle_accounts_does_not_mutate_caller_bundle():
    """execute_batch(accounts=...) must not write stamped resources back
    into the caller's bundle entries — re-stamping a reused bundle would
    otherwise accumulate account refs across calls."""
    from pymedplum._base import _stamp_bundle_accounts

    bundle = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {"resource": {"resourceType": "Patient"}, "request": {"method": "POST"}},
            {"fullUrl": "urn:x"},  # no resource — passes through untouched
        ],
    }

    out1 = _stamp_bundle_accounts(
        bundle, "Organization/org-1", BaseClient._apply_accounts
    )
    out2 = _stamp_bundle_accounts(
        bundle, "Organization/org-2", BaseClient._apply_accounts
    )

    # Caller's bundle is pristine — no meta leaked, no accumulation.
    assert bundle["entry"][0]["resource"] == {"resourceType": "Patient"}
    # Each call stamps its own ref onto a fresh copy.
    assert out1["entry"][0]["resource"]["meta"]["accounts"] == [
        {"reference": "Organization/org-1"}
    ]
    assert out2["entry"][0]["resource"]["meta"]["accounts"] == [
        {"reference": "Organization/org-2"}
    ]
    # Non-resource entries pass through.
    assert out1["entry"][1] == {"fullUrl": "urn:x"}


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


# Tests for legacy singular meta.account support (deprecated by Medplum in
# favor of meta.accounts, but still emitted on older resources). Mirrors
# @medplum/core extractAccountReferences: account-first, deduped.
def test_get_resource_accounts_singular_account_only():
    resource = {"meta": {"account": {"reference": "Organization/org-1"}}}
    assert get_resource_accounts(resource) == ["Organization/org-1"]


def test_get_resource_accounts_singular_and_plural_account_first():
    resource = {
        "meta": {
            "account": {"reference": "Organization/org-1"},
            "accounts": [{"reference": "Organization/org-2"}],
        }
    }
    assert get_resource_accounts(resource) == [
        "Organization/org-1",
        "Organization/org-2",
    ]


def test_get_resource_accounts_singular_deduped_against_plural():
    resource = {
        "meta": {
            "account": {"reference": "Organization/org-1"},
            "accounts": [
                {"reference": "Organization/org-1"},
                {"reference": "Organization/org-2"},
            ],
        }
    }
    assert get_resource_accounts(resource) == [
        "Organization/org-1",
        "Organization/org-2",
    ]


def test_resource_has_account_matches_singular_account():
    resource = {"meta": {"account": {"reference": "Organization/org-1"}}}
    assert resource_has_account(resource, "Organization/org-1")


# Tests for extract_account_references (the meta-level primitive)
def test_extract_account_references_plural():
    meta = {"accounts": [{"reference": "Organization/org-1"}]}
    assert extract_account_references(meta) == ["Organization/org-1"]


def test_extract_account_references_singular():
    meta = {"account": {"reference": "Organization/org-1"}}
    assert extract_account_references(meta) == ["Organization/org-1"]


def test_extract_account_references_account_first():
    meta = {
        "account": {"reference": "Organization/org-1"},
        "accounts": [{"reference": "Organization/org-2"}],
    }
    assert extract_account_references(meta) == [
        "Organization/org-1",
        "Organization/org-2",
    ]


def test_extract_account_references_none_meta():
    assert extract_account_references(None) == []


def test_extract_account_references_empty_meta():
    assert extract_account_references({}) == []


def test_extract_account_references_accepts_pydantic_meta():
    from pymedplum.fhir import Meta, Reference

    meta = Meta(accounts=[Reference(reference="Organization/org-1")])
    assert extract_account_references(meta) == ["Organization/org-1"]


def test_extract_account_references_skips_non_string_plural_ref():
    meta = {"accounts": [{"reference": 5}, {"reference": "Organization/org-1"}]}
    assert extract_account_references(meta) == ["Organization/org-1"]


def test_extract_account_references_skips_non_string_singular_ref():
    meta = {"account": {"reference": 123}}
    assert extract_account_references(meta) == []


def test_set_accounts_prefer_async_without_propagate_raises():
    client = MedplumClient()
    with pytest.raises(ValueError, match="prefer_async only takes effect"):
        client.set_accounts("Patient/123", "Organization/org-1", prefer_async=True)


def test_resolve_async_job_url_from_operation_outcome():
    client = MedplumClient()
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "information",
                "code": "informational",
                "diagnostics": "https://api.medplum.com/fhir/R4/job/abc-123/status",
            }
        ],
    }
    assert client._resolve_async_job_url(outcome) == (
        "https://api.medplum.com/fhir/R4/job/abc-123/status"
    )


def test_resolve_async_job_url_from_full_url():
    client = MedplumClient()
    url = "https://api.medplum.com/fhir/R4/job/abc-123/status"
    assert client._resolve_async_job_url(url) == url


def test_resolve_async_job_url_from_job_id():
    client = MedplumClient()
    assert client._resolve_async_job_url("abc-123") == (
        "https://api.medplum.com/fhir/R4/job/abc-123/status"
    )


def test_resolve_async_job_url_from_pydantic_model():
    from pymedplum.fhir import OperationOutcome, OperationOutcomeIssue

    client = MedplumClient()
    outcome = OperationOutcome(
        issue=[
            OperationOutcomeIssue(
                severity="information",
                code="informational",
                diagnostics="https://api.medplum.com/fhir/R4/job/abc-123/status",
            )
        ],
    )
    assert client._resolve_async_job_url(outcome) == (
        "https://api.medplum.com/fhir/R4/job/abc-123/status"
    )


def test_resolve_async_job_url_invalid_dict_raises():
    client = MedplumClient()
    with pytest.raises(ValueError, match="Expected OperationOutcome"):
        client._resolve_async_job_url({"resourceType": "Patient"})
