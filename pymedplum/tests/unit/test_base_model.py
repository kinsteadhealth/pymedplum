"""Unit tests for MedplumFHIRBase convenience properties."""

from pymedplum.fhir import Meta, Patient, Reference


def test_medplum_accounts_from_plural():
    patient = Patient(meta=Meta(accounts=[Reference(reference="Organization/org-1")]))
    assert patient.medplum_accounts == ["Organization/org-1"]


def test_medplum_accounts_from_singular():
    patient = Patient(meta=Meta(account=Reference(reference="Organization/org-1")))
    assert patient.medplum_accounts == ["Organization/org-1"]


def test_medplum_accounts_singular_and_plural_account_first():
    patient = Patient(
        meta=Meta(
            account=Reference(reference="Organization/org-1"),
            accounts=[Reference(reference="Organization/org-2")],
        )
    )
    assert patient.medplum_accounts == [
        "Organization/org-1",
        "Organization/org-2",
    ]


def test_medplum_accounts_no_meta():
    assert Patient().medplum_accounts == []


def test_medplum_account_returns_primary():
    patient = Patient(
        meta=Meta(
            accounts=[
                Reference(reference="Organization/org-1"),
                Reference(reference="Organization/org-2"),
            ]
        )
    )
    assert patient.medplum_account == "Organization/org-1"


def test_medplum_account_none_when_absent():
    assert Patient().medplum_account is None
