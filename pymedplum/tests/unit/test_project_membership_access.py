"""Pure-function tests for ProjectMembership access helpers.

No HTTP, no client. Covers entry construction, policy normalization,
parameter lookup, partition / merge / equality, and validation.
"""

from __future__ import annotations

import pytest

from pymedplum.access import (
    build_merged_access,
    get_project_membership_access_parameter,
    get_project_membership_access_policy_id,
    make_project_membership_access,
    merged_equals_remote,
    normalize_access_entry,
    normalize_access_policy_id,
    normalize_access_policy_reference,
    partition_access,
    validate_managed_access,
)
from pymedplum.fhir import (
    ProjectMembershipAccess,
    ProjectMembershipAccessParameter,
    Reference,
)


# ---------------------------------------------------------------------------
# make_project_membership_access
# ---------------------------------------------------------------------------


def test_make_access_returns_doc_shape() -> None:
    entry = make_project_membership_access(
        "AccessPolicy/abc",
        {"organization": "Organization/org-a"},
    )
    assert entry == {
        "policy": {"reference": "AccessPolicy/abc"},
        "parameter": [
            {
                "name": "organization",
                "valueReference": {"reference": "Organization/org-a"},
            }
        ],
    }


def test_make_access_accepts_bare_policy_id() -> None:
    entry = make_project_membership_access(
        "abc", {"organization": "Organization/org-a"}
    )
    assert entry["policy"] == {"reference": "AccessPolicy/abc"}


def test_make_access_accepts_reference_model() -> None:
    ref = Reference(reference="AccessPolicy/abc")
    entry = make_project_membership_access(
        ref, {"organization": "Organization/org-a"}
    )
    assert entry["policy"] == {"reference": "AccessPolicy/abc"}


def test_make_access_accepts_raw_reference_dict() -> None:
    entry = make_project_membership_access(
        {"reference": "AccessPolicy/abc"},
        {"organization": "Organization/org-a"},
    )
    assert entry["policy"] == {"reference": "AccessPolicy/abc"}


def test_make_access_emits_value_string_for_plain_string() -> None:
    entry = make_project_membership_access(
        "AccessPolicy/abc", {"role": "admin"}
    )
    assert entry["parameter"] == [{"name": "role", "valueString": "admin"}]


def test_make_access_emits_value_reference_for_reference_string() -> None:
    entry = make_project_membership_access(
        "AccessPolicy/abc",
        {"organization": "Organization/org-a"},
    )
    assert entry["parameter"][0]["valueReference"] == {
        "reference": "Organization/org-a"
    }


def test_make_access_emits_value_reference_for_dict() -> None:
    entry = make_project_membership_access(
        "AccessPolicy/abc",
        {"organization": {"reference": "Organization/org-a"}},
    )
    assert entry["parameter"][0]["valueReference"] == {
        "reference": "Organization/org-a"
    }


def test_make_access_emits_value_reference_for_reference_model() -> None:
    entry = make_project_membership_access(
        "AccessPolicy/abc",
        {"organization": Reference(reference="Organization/org-a")},
    )
    assert entry["parameter"][0]["valueReference"] == {
        "reference": "Organization/org-a"
    }


def test_make_access_rejects_empty_parameter_name() -> None:
    with pytest.raises(ValueError):
        make_project_membership_access(
            "AccessPolicy/abc", {"": "Organization/org-a"}
        )


def test_make_access_rejects_empty_policy_id() -> None:
    with pytest.raises(ValueError):
        make_project_membership_access("", {"organization": "Organization/org"})


def test_make_access_rejects_wrong_resource_type() -> None:
    with pytest.raises(ValueError):
        make_project_membership_access(
            "Patient/abc", {"organization": "Organization/org"}
        )


def test_make_access_rejects_unsupported_value_shape() -> None:
    with pytest.raises((TypeError, ValueError)):
        make_project_membership_access(
            "AccessPolicy/abc", {"organization": 123}  # type: ignore[dict-item]
        )


def test_make_access_rejects_dict_without_reference_field() -> None:
    with pytest.raises(ValueError):
        make_project_membership_access(
            "AccessPolicy/abc", {"organization": {"display": "no ref"}}
        )


def test_make_access_omits_parameter_when_empty() -> None:
    entry = make_project_membership_access("AccessPolicy/abc", {})
    assert "parameter" not in entry


# ---------------------------------------------------------------------------
# normalize_access_policy_reference / normalize_access_policy_id
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "policy",
    [
        "abc",
        "AccessPolicy/abc",
        Reference(reference="AccessPolicy/abc"),
        {"reference": "AccessPolicy/abc"},
    ],
)
def test_normalize_access_policy_id_agreement(policy) -> None:
    assert normalize_access_policy_id(policy) == "abc"
    assert normalize_access_policy_reference(policy) == {
        "reference": "AccessPolicy/abc"
    }


def test_normalize_rejects_other_resource_type() -> None:
    with pytest.raises(ValueError):
        normalize_access_policy_reference("Patient/abc")


def test_normalize_rejects_empty() -> None:
    with pytest.raises(ValueError):
        normalize_access_policy_reference("   ")


# ---------------------------------------------------------------------------
# get_project_membership_access_policy_id / parameter
# ---------------------------------------------------------------------------


def test_get_policy_id_from_dict_entry() -> None:
    entry = {"policy": {"reference": "AccessPolicy/abc"}}
    assert get_project_membership_access_policy_id(entry) == "abc"


def test_get_policy_id_from_pydantic_entry() -> None:
    entry = ProjectMembershipAccess(
        policy=Reference(reference="AccessPolicy/abc")
    )
    assert get_project_membership_access_policy_id(entry) == "abc"


@pytest.mark.parametrize(
    "entry",
    [
        {},
        {"policy": None},
        {"policy": {}},
        {"policy": {"reference": None}},
        {"policy": {"reference": "Patient/abc"}},
        {"policy": "AccessPolicy/abc"},  # reference must be a dict, not str
    ],
)
def test_get_policy_id_returns_none_for_malformed(entry) -> None:
    assert get_project_membership_access_policy_id(entry) is None


def test_get_parameter_returns_named() -> None:
    entry = make_project_membership_access(
        "abc", {"organization": "Organization/o1"}
    )
    param = get_project_membership_access_parameter(entry, "organization")
    assert param is not None
    assert param["valueReference"] == {"reference": "Organization/o1"}


def test_get_parameter_returns_none_when_absent() -> None:
    entry = make_project_membership_access("abc", {})
    assert get_project_membership_access_parameter(entry, "organization") is None


def test_get_parameter_handles_pydantic_entry() -> None:
    entry = ProjectMembershipAccess(
        policy=Reference(reference="AccessPolicy/abc"),
        parameter=[
            ProjectMembershipAccessParameter(
                name="organization",
                value_reference=Reference(reference="Organization/o1"),
            )
        ],
    )
    param = get_project_membership_access_parameter(entry, "organization")
    assert param is not None
    assert param["valueReference"] == {"reference": "Organization/o1"}


# ---------------------------------------------------------------------------
# partition_access
# ---------------------------------------------------------------------------


def test_partition_separates_managed_and_untouched() -> None:
    managed_ids = {"managed-1"}
    current = [
        {"policy": {"reference": "AccessPolicy/managed-1"}},
        {"policy": {"reference": "AccessPolicy/other"}},
    ]
    managed, untouched = partition_access(current, managed_ids)
    assert managed == [{"policy": {"reference": "AccessPolicy/managed-1"}}]
    assert untouched == [{"policy": {"reference": "AccessPolicy/other"}}]


def test_partition_handles_bare_id_in_managed_set() -> None:
    # managed_policy_ids holds bare IDs, not full references
    managed_ids = {"managed-1"}
    current = [{"policy": {"reference": "AccessPolicy/managed-1"}}]
    managed, untouched = partition_access(current, managed_ids)
    assert len(managed) == 1
    assert untouched == []


@pytest.mark.parametrize(
    "entry",
    [
        {},
        {"policy": None},
        {"policy": {"reference": None}},
        {"policy": {"reference": 123}},
        {"policy": {}},
    ],
)
def test_partition_treats_malformed_as_untouched(entry) -> None:
    managed, untouched = partition_access([entry], {"x"})
    assert managed == []
    assert len(untouched) == 1


def test_partition_empty_input() -> None:
    managed, untouched = partition_access(None, {"x"})
    assert managed == []
    assert untouched == []


def test_partition_rejects_empty_managed_set() -> None:
    with pytest.raises(ValueError):
        partition_access([{"policy": {"reference": "AccessPolicy/abc"}}], set())


# ---------------------------------------------------------------------------
# validate_managed_access
# ---------------------------------------------------------------------------


def test_validate_managed_access_accepts_managed() -> None:
    validate_managed_access(
        [{"policy": {"reference": "AccessPolicy/m1"}}], {"m1"}
    )


def test_validate_managed_access_rejects_unmanaged() -> None:
    with pytest.raises(ValueError):
        validate_managed_access(
            [{"policy": {"reference": "AccessPolicy/other"}}], {"m1"}
        )


def test_validate_managed_access_rejects_malformed() -> None:
    with pytest.raises(ValueError):
        validate_managed_access([{"policy": {}}], {"m1"})


def test_validate_managed_access_rejects_empty_set() -> None:
    with pytest.raises(ValueError):
        validate_managed_access([], set())


def test_validate_managed_access_accepts_pydantic_entries() -> None:
    entry = ProjectMembershipAccess(
        policy=Reference(reference="AccessPolicy/m1")
    )
    validate_managed_access([entry], {"m1"})


# ---------------------------------------------------------------------------
# normalize_access_entry
# ---------------------------------------------------------------------------


def test_normalize_access_entry_pydantic_matches_dict() -> None:
    pyd = ProjectMembershipAccess(
        policy=Reference(reference="AccessPolicy/abc"),
        parameter=[
            ProjectMembershipAccessParameter(
                name="organization",
                value_reference=Reference(reference="Organization/o1"),
            )
        ],
    )
    dict_entry = make_project_membership_access(
        "AccessPolicy/abc", {"organization": "Organization/o1"}
    )
    assert normalize_access_entry(pyd) == normalize_access_entry(dict_entry)


# ---------------------------------------------------------------------------
# build_merged_access
# ---------------------------------------------------------------------------


def test_build_merged_access_preserves_order() -> None:
    untouched = [{"policy": {"reference": "AccessPolicy/u"}}]
    managed = [
        {"policy": {"reference": "AccessPolicy/m1"}},
        {"policy": {"reference": "AccessPolicy/m2"}},
    ]
    merged = build_merged_access(untouched, managed)
    assert [
        get_project_membership_access_policy_id(e) for e in merged
    ] == ["u", "m1", "m2"]


def test_build_merged_access_empty_managed_returns_untouched() -> None:
    untouched = [{"policy": {"reference": "AccessPolicy/u"}}]
    assert build_merged_access(untouched, []) == untouched


# ---------------------------------------------------------------------------
# merged_equals_remote
# ---------------------------------------------------------------------------


def test_merged_equals_remote_byte_equal() -> None:
    a = [{"policy": {"reference": "AccessPolicy/abc"}}]
    b = [{"policy": {"reference": "AccessPolicy/abc"}}]
    assert merged_equals_remote(a, b) is True


def test_merged_equals_remote_ignores_key_order() -> None:
    a = [
        {
            "policy": {"reference": "AccessPolicy/abc"},
            "parameter": [
                {
                    "name": "organization",
                    "valueReference": {"reference": "Organization/o1"},
                }
            ],
        }
    ]
    b = [
        {
            "parameter": [
                {
                    "valueReference": {"reference": "Organization/o1"},
                    "name": "organization",
                }
            ],
            "policy": {"reference": "AccessPolicy/abc"},
        }
    ]
    assert merged_equals_remote(a, b) is True


def test_merged_equals_remote_different_lists_unequal() -> None:
    a = [{"policy": {"reference": "AccessPolicy/abc"}}]
    b = [{"policy": {"reference": "AccessPolicy/xyz"}}]
    assert merged_equals_remote(a, b) is False


def test_merged_equals_remote_none_and_empty_equal() -> None:
    assert merged_equals_remote([], None) is True
