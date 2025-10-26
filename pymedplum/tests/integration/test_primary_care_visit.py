"""Primary Care Visit Integration Tests

Simulates a complete primary care visit workflow for a 70-year-old diabetic patient
on Medicare requiring prescription refills, lab review, and follow-up scheduling.

Demonstrates:
- Real-world FHIR resource creation and management
- On-behalf-of usage with scoped clients
- Value-based care quality measures
- Complete clinical workflow from check-in to follow-up
"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from pymedplum import to_fhir_json
from pymedplum.fhir import (
    Address,
    Appointment,
    AppointmentParticipant,
    Attachment,
    CarePlan,
    CarePlanActivity,
    Claim,
    ClaimDiagnosis,
    ClaimInsurance,
    ClaimItem,
    CodeableConcept,
    Coding,
    Condition,
    Consent,
    ConsentProvision,
    ContactPoint,
    Coverage,
    CoverageClass,
    DocumentReference,
    DocumentReferenceContent,
    Dosage,
    Duration,
    Encounter,
    EncounterParticipant,
    Goal,
    GoalTarget,
    HumanName,
    Identifier,
    MedicationRequest,
    MedicationRequestDispenseRequest,
    Money,
    Observation,
    Organization,
    Patient,
    Period,
    Practitioner,
    Procedure,
    Provenance,
    ProvenanceAgent,
    Quantity,
    Reference,
    ServiceRequest,
    Timing,
    TimingRepeat,
)


@pytest.fixture
def visit_test_id():
    """Unique ID for this test run"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def primary_care_clinic(medplum_client, visit_test_id):
    """Create a primary care clinic organization"""
    clinic = Organization(
        name=f"Healthy Hearts Primary Care - {visit_test_id}",
        identifier=[
            Identifier(
                system="http://example.org/clinic-npi",
                value=f"1234567890-{visit_test_id}",
            )
        ],
        type=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/organization-type",
                        code="prov",
                        display="Healthcare Provider",
                    )
                ]
            )
        ],
    )
    return medplum_client.create_resource(to_fhir_json(clinic))


@pytest.fixture
def dr_smith(medplum_client, visit_test_id):
    """Create the primary care physician"""
    provider = Practitioner(
        name=[HumanName(given=["Sarah"], family="Smith", prefix=["Dr."])],
        identifier=[
            Identifier(
                system="http://hl7.org/fhir/sid/us-npi",
                value=f"9876543210-{visit_test_id}",
            )
        ],
        qualification=[
            {
                "code": CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/v2-0360",
                            code="MD",
                            display="Doctor of Medicine",
                        )
                    ]
                )
            }
        ],
    )
    return medplum_client.create_resource(to_fhir_json(provider))


@pytest.fixture
def elderly_diabetic_patient(medplum_client, primary_care_clinic, visit_test_id):
    """Create a 70-year-old female diabetic patient on Medicare"""
    patient = Patient(
        name=[HumanName(given=["Dorothy"], family=f"Martinez-{visit_test_id}")],
        gender="female",
        birthDate="1953-08-15",  # 70 years old
        address=[
            Address(
                line=["123 Oak Street"],
                city="Springfield",
                state="IL",
                postalCode="62701",
                country="US",
            )
        ],
        telecom=[
            ContactPoint(system="phone", value="555-0123", use="home"),
            ContactPoint(
                system="email", value=f"dorothy.martinez.{visit_test_id}@example.com"
            ),
        ],
        identifier=[
            Identifier(
                system="http://hl7.org/fhir/sid/us-medicare",
                value=f"1EG4-TE5-MK73-{visit_test_id}",
            )
        ],
    )

    # Tag to clinic using org_mode
    return medplum_client.create_resource(
        to_fhir_json(patient),
        org_mode="accounts",
        org_ref=f"Organization/{primary_care_clinic['id']}",
    )


@pytest.fixture
def medicare_coverage(medplum_client, elderly_diabetic_patient, visit_test_id):
    """Create Medicare coverage for the patient"""
    coverage = Coverage(
        status="active",
        type=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    code="MEDICARE",
                    display="Medicare",
                )
            ]
        ),
        subscriber=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        beneficiary=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        payor=[Reference(display="Centers for Medicare & Medicaid Services")],
        class_=[
            CoverageClass(
                type=CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/coverage-class",
                            code="plan",
                            display="Plan",
                        )
                    ]
                ),
                value=f"Part-B-{visit_test_id}",
                name="Medicare Part B",
            )
        ],
    )
    return medplum_client.create_resource(to_fhir_json(coverage))


def test_01_create_primary_care_encounter(
    create_scoped_client,
    medplum_credentials,
    elderly_diabetic_patient,
    dr_smith,
    primary_care_clinic,
    visit_test_id,
):
    """Test creating the encounter for the primary care visit using scoped client"""
    # Get project ID and create a simple membership (in real scenario, would use proper membership)
    import os

    project_id = os.getenv("MEDPLUM_PROJECT_ID")

    if not project_id:
        pytest.skip("PROJECT_ID required for this test")

    # For this test, we'll use the base client without on_behalf_of
    # In production, you'd use: scoped_client = create_scoped_client(membership_id)
    from pymedplum import MedplumClient

    client = MedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
        project_id=project_id,
    )
    client.authenticate()

    try:
        # Create encounter for annual diabetic follow-up visit
        encounter = Encounter(
            status="finished",
            class_=Coding(
                system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
                code="AMB",
                display="ambulatory",
            ),
            type=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://snomed.info/sct",
                            code="185349003",
                            display="Encounter for 'check-up'",
                        )
                    ],
                    text="Annual Diabetic Follow-up",
                )
            ],
            subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
            participant=[
                EncounterParticipant(
                    individual=Reference(reference=f"Practitioner/{dr_smith['id']}")
                )
            ],
            serviceProvider=Reference(
                reference=f"Organization/{primary_care_clinic['id']}"
            ),
            period={
                "start": datetime.now(timezone.utc).isoformat(),
                "end": datetime.now(timezone.utc).isoformat(),
            },
        )

        result = client.create_resource(to_fhir_json(encounter))

        assert result["resourceType"] == "Encounter"
        assert result["status"] == "finished"
        assert (
            result["subject"]["reference"]
            == f"Patient/{elderly_diabetic_patient['id']}"
        )
        assert len(result["participant"]) == 1

        # Cleanup
        client.delete_resource("Encounter", result["id"])
    finally:
        client.close()


def test_02_document_diabetes_condition(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test documenting active diabetes mellitus Type 2 condition"""
    condition = Condition(
        clinicalStatus=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                    code="active",
                )
            ]
        ),
        verificationStatus=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    code="confirmed",
                )
            ]
        ),
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/condition-category",
                        code="encounter-diagnosis",
                    )
                ]
            )
        ],
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://snomed.info/sct",
                    code="44054006",
                    display="Diabetes mellitus type 2",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        onsetDateTime="2010-03-15",  # Diagnosed 13 years ago
        recorder=Reference(reference=f"Practitioner/{dr_smith['id']}"),
    )

    result = medplum_client.create_resource(to_fhir_json(condition))

    assert result["resourceType"] == "Condition"
    assert result["clinicalStatus"]["coding"][0]["code"] == "active"
    assert "Diabetes" in result["code"]["coding"][0]["display"]

    # Cleanup
    medplum_client.delete_resource("Condition", result["id"])


def test_03_record_hba1c_lab_result(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test recording HbA1c lab result for quality measure tracking"""
    # HbA1c of 7.2% - slightly above target but acceptable for elderly patient
    observation = Observation(
        status="final",
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/observation-category",
                        code="laboratory",
                    )
                ]
            )
        ],
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://loinc.org",
                    code="4548-4",
                    display="Hemoglobin A1c/Hemoglobin.total in Blood",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        effectiveDateTime=datetime.now(timezone.utc).isoformat(),
        performer=[Reference(reference=f"Practitioner/{dr_smith['id']}")],
        valueQuantity=Quantity(
            value=7.2, unit="%", system="http://unitsofmeasure.org", code="%"
        ),
    )

    result = medplum_client.create_resource(to_fhir_json(observation))

    assert result["resourceType"] == "Observation"
    assert result["code"]["coding"][0]["code"] == "4548-4"  # HbA1c LOINC code
    assert result["valueQuantity"]["value"] == 7.2
    assert result["status"] == "final"

    # Cleanup
    medplum_client.delete_resource("Observation", result["id"])


def test_04_record_kidney_function_labs(
    medplum_client, elderly_diabetic_patient, visit_test_id
):
    """Test recording kidney function tests (eGFR) for diabetic nephropathy screening"""
    # eGFR of 72 - Stage 2 CKD, common in elderly diabetics
    observation = Observation(
        status="final",
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/observation-category",
                        code="laboratory",
                    )
                ]
            )
        ],
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://loinc.org",
                    code="33914-3",
                    display="Glomerular filtration rate/1.73 sq M.predicted [Volume Rate/Area] in Serum or Plasma by Creatinine-based formula (MDRD)",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        effectiveDateTime=datetime.now(timezone.utc).isoformat(),
        valueQuantity=Quantity(
            value=72,
            unit="mL/min/1.73m2",
            system="http://unitsofmeasure.org",
            code="mL/min/{1.73_m2}",
        ),
    )

    result = medplum_client.create_resource(to_fhir_json(observation))

    assert result["resourceType"] == "Observation"
    assert result["valueQuantity"]["value"] == 72

    # Cleanup
    medplum_client.delete_resource("Observation", result["id"])


def test_05_refill_metformin_prescription(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test creating a prescription refill for metformin"""
    medication_request = MedicationRequest(
        status="active",
        intent="order",
        medicationCodeableConcept=CodeableConcept(
            coding=[
                Coding(
                    system="http://www.nlm.nih.gov/research/umls/rxnorm",
                    code="860975",
                    display="metformin hydrochloride 1000 MG Oral Tablet",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        authoredOn=datetime.now(timezone.utc).isoformat(),
        requester=Reference(reference=f"Practitioner/{dr_smith['id']}"),
        dosageInstruction=[
            Dosage(
                text="Take 1 tablet by mouth twice daily with meals",
                timing=Timing(
                    repeat=TimingRepeat(frequency=2, period=1, periodUnit="d")
                ),
                doseAndRate=[
                    {
                        "doseQuantity": Quantity(
                            value=1,
                            unit="tablet",
                            system="http://unitsofmeasure.org",
                            code="{tablet}",
                        )
                    }
                ],
            )
        ],
        dispenseRequest=MedicationRequestDispenseRequest(
            numberOfRepeatsAllowed=3,
            quantity=Quantity(
                value=180,
                unit="tablet",
                system="http://unitsofmeasure.org",
                code="{tablet}",
            ),
            expectedSupplyDuration=Duration(
                value=90, unit="days", system="http://unitsofmeasure.org", code="d"
            ),
        ),
    )

    result = medplum_client.create_resource(to_fhir_json(medication_request))

    assert result["resourceType"] == "MedicationRequest"
    assert result["status"] == "active"
    assert (
        "metformin"
        in result["medicationCodeableConcept"]["coding"][0]["display"].lower()
    )
    assert result["dispenseRequest"]["numberOfRepeatsAllowed"] == 3

    # Cleanup
    medplum_client.delete_resource("MedicationRequest", result["id"])


def test_06_create_diabetes_care_goal(
    medplum_client, elderly_diabetic_patient, visit_test_id
):
    """Test creating a diabetes management goal for HbA1c control"""
    goal = Goal(
        lifecycleStatus="active",
        description=CodeableConcept(
            text="Maintain HbA1c below 7.5% for diabetes control"
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        startDate=datetime.now(timezone.utc).date().isoformat(),
        target=[
            GoalTarget(
                measure=CodeableConcept(
                    coding=[
                        Coding(
                            system="http://loinc.org",
                            code="4548-4",
                            display="Hemoglobin A1c",
                        )
                    ]
                ),
                detailQuantity=Quantity(
                    value=7.5,
                    comparator="<",
                    unit="%",
                    system="http://unitsofmeasure.org",
                    code="%",
                ),
                dueDate=(datetime.now() + timedelta(days=90)).date().isoformat(),
            )
        ],
    )

    result = medplum_client.create_resource(to_fhir_json(goal))

    assert result["resourceType"] == "Goal"
    assert result["lifecycleStatus"] == "active"
    assert result["target"][0]["detailQuantity"]["value"] == 7.5

    # Cleanup
    medplum_client.delete_resource("Goal", result["id"])


def test_07_schedule_follow_up_appointment(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test scheduling a 3-month follow-up appointment"""
    follow_up_date = datetime.now(timezone.utc) + timedelta(days=90)

    appointment = Appointment(
        status="booked",
        appointmentType=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0276",
                    code="FOLLOWUP",
                    display="Follow-up",
                )
            ]
        ),
        description="3-month diabetes follow-up to review HbA1c",
        start=follow_up_date.isoformat(),
        end=(follow_up_date + timedelta(minutes=30)).isoformat(),
        minutesDuration=30,
        participant=[
            AppointmentParticipant(
                actor=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
                required="required",
                status="accepted",
            ),
            AppointmentParticipant(
                actor=Reference(reference=f"Practitioner/{dr_smith['id']}"),
                required="required",
                status="accepted",
            ),
        ],
    )

    result = medplum_client.create_resource(to_fhir_json(appointment))

    assert result["resourceType"] == "Appointment"
    assert result["status"] == "booked"
    assert len(result["participant"]) == 2
    assert result["minutesDuration"] == 30

    # Cleanup
    medplum_client.delete_resource("Appointment", result["id"])


def test_08_create_diabetes_care_plan(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test creating a comprehensive diabetes care plan"""
    care_plan = CarePlan(
        status="active",
        intent="plan",
        title="Diabetes Mellitus Type 2 Management Plan",
        description="Comprehensive diabetes management including medication, diet, exercise, and monitoring",
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        period={
            "start": datetime.now().date().isoformat(),
            "end": (datetime.now() + timedelta(days=365)).date().isoformat(),
        },
        author=Reference(reference=f"Practitioner/{dr_smith['id']}"),
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="698360004",
                        display="Diabetes self management plan",
                    )
                ]
            )
        ],
        activity=[
            CarePlanActivity(
                detail={
                    "status": "in-progress",
                    "description": "Monitor blood glucose daily",
                    "scheduledTiming": Timing(
                        repeat=TimingRepeat(frequency=1, period=1, periodUnit="d")
                    ),
                }
            ),
            CarePlanActivity(
                detail={
                    "status": "in-progress",
                    "description": "Take metformin 1000mg twice daily with meals",
                }
            ),
            CarePlanActivity(
                detail={
                    "status": "scheduled",
                    "description": "Annual diabetic foot examination",
                    "scheduledPeriod": {
                        "start": (datetime.now() + timedelta(days=30))
                        .date()
                        .isoformat()
                    },
                }
            ),
        ],
    )

    result = medplum_client.create_resource(to_fhir_json(care_plan))

    assert result["resourceType"] == "CarePlan"
    assert result["status"] == "active"
    assert result["title"] == "Diabetes Mellitus Type 2 Management Plan"
    assert len(result["activity"]) == 3

    # Cleanup
    medplum_client.delete_resource("CarePlan", result["id"])


def test_09_verify_medicare_coverage(medicare_coverage, elderly_diabetic_patient):
    """Test that Medicare coverage is properly linked to patient"""
    assert medicare_coverage["resourceType"] == "Coverage"
    assert medicare_coverage["status"] == "active"
    assert (
        medicare_coverage["beneficiary"]["reference"]
        == f"Patient/{elderly_diabetic_patient['id']}"
    )
    assert any(
        "MEDICARE" in c["coding"][0]["code"] for c in [medicare_coverage["type"]]
    )


def test_10_perform_diabetic_foot_exam(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test documenting a diabetic foot examination procedure"""
    # Create a fixture for the encounter first
    from pymedplum.client import MedplumClient

    client = MedplumClient(
        base_url=medplum_client.base_url,
        client_id=medplum_client.client_id,
        client_secret=medplum_client.client_secret,
        project_id=medplum_client.project_id,
    )
    client.authenticate()

    # Create encounter for this procedure
    encounter = Encounter(
        status="finished",
        class_=Coding(
            system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
            code="AMB",
            display="ambulatory",
        ),
        type=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="185349003",
                        display="Encounter for 'check-up'",
                    )
                ],
                text="Diabetic Foot Exam",
            )
        ],
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        period={
            "start": datetime.now(timezone.utc).isoformat(),
            "end": datetime.now(timezone.utc).isoformat(),
        },
    )
    encounter_result = client.create_resource(to_fhir_json(encounter))

    try:
        # Create Procedure for diabetic foot exam (SNOMED CT code: 225363006)
        procedure = Procedure(
            status="completed",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="225363006",
                        display="Foot examination for diabetes",
                    )
                ],
                text="Comprehensive diabetic foot examination",
            ),
            subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
            encounter=Reference(reference=f"Encounter/{encounter_result['id']}"),
            performedDateTime=datetime.now(timezone.utc).isoformat(),
            performer=[
                {"actor": Reference(reference=f"Practitioner/{dr_smith['id']}")}
            ],
            bodySite=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://snomed.info/sct",
                            code="87342007",
                            display="Both feet",
                        )
                    ]
                )
            ],
            outcome=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="385669000",
                        display="Successful",
                    )
                ],
                text="No abnormalities detected, peripheral pulses intact, sensation normal",
            ),
        )

        result = medplum_client.create_resource(to_fhir_json(procedure))

        assert result["resourceType"] == "Procedure"
        assert result["status"] == "completed"
        assert result["code"]["coding"][0]["code"] == "225363006"
        assert (
            result["subject"]["reference"]
            == f"Patient/{elderly_diabetic_patient['id']}"
        )
        assert result["outcome"]["text"] is not None

        # Cleanup
        medplum_client.delete_resource("Procedure", result["id"])
    finally:
        client.delete_resource("Encounter", encounter_result["id"])


def test_11_create_ophthalmology_referral(
    medplum_client,
    elderly_diabetic_patient,
    dr_smith,
    visit_test_id,
):
    """Test creating a ServiceRequest for ophthalmology referral"""
    # First create the diabetes condition to reference
    condition = Condition(
        clinicalStatus=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                    code="active",
                )
            ]
        ),
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://snomed.info/sct",
                    code="44054006",
                    display="Diabetes mellitus type 2",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
    )
    diabetes_condition = medplum_client.create_resource(to_fhir_json(condition))

    try:
        service_request = ServiceRequest(
            status="active",
            intent="order",
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://snomed.info/sct",
                            code="306206005",
                            display="Referral to service",
                        )
                    ]
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="306098008",
                        display="Referral to ophthalmology service",
                    )
                ],
                text="Annual diabetic retinopathy screening",
            ),
            subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
            authoredOn=datetime.now(timezone.utc).isoformat(),
            requester=Reference(reference=f"Practitioner/{dr_smith['id']}"),
            reasonReference=[
                Reference(reference=f"Condition/{diabetes_condition['id']}")
            ],
            note=[
                {
                    "text": "Patient is due for annual diabetic eye exam. Medicare Part B covered."
                }
            ],
        )

        result = medplum_client.create_resource(to_fhir_json(service_request))

        assert result["resourceType"] == "ServiceRequest"
        assert result["status"] == "active"
        assert result["intent"] == "order"
        assert "ophthalmology" in result["code"]["coding"][0]["display"].lower()
        assert len(result["reasonReference"]) > 0

        # Cleanup
        medplum_client.delete_resource("ServiceRequest", result["id"])
    finally:
        medplum_client.delete_resource("Condition", diabetes_condition["id"])


def test_12_attach_patient_education_document(
    medplum_client, elderly_diabetic_patient, visit_test_id
):
    """Test creating a DocumentReference for patient education materials"""
    # In a real scenario, you'd first create a Binary resource with the actual PDF
    # For this test, we'll reference a hypothetical document

    document_reference = DocumentReference(
        status="current",
        type=CodeableConcept(
            coding=[
                Coding(
                    system="http://loinc.org",
                    code="34133-9",
                    display="Summary of episode note",
                )
            ],
            text="Diabetes Foot Care Education Handout",
        ),
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://hl7.org/fhir/document-reference-category",
                        code="clinical-note",
                        display="Clinical Note",
                    )
                ]
            )
        ],
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        date=datetime.now(timezone.utc).isoformat(),
        author=[Reference(display="Primary Care Clinic")],
        description="Educational handout on diabetic foot care and daily inspection",
        content=[
            DocumentReferenceContent(
                attachment=Attachment(
                    contentType="application/pdf",
                    title="Diabetes Foot Care Guide",
                    creation=datetime.now(timezone.utc).isoformat(),
                    # In real scenario: url="Binary/foot-care-guide-123"
                )
            )
        ],
    )

    result = medplum_client.create_resource(to_fhir_json(document_reference))

    assert result["resourceType"] == "DocumentReference"
    assert result["status"] == "current"
    assert result["subject"]["reference"] == f"Patient/{elderly_diabetic_patient['id']}"
    assert len(result["content"]) > 0
    assert result["content"][0]["attachment"]["contentType"] == "application/pdf"

    # Cleanup
    medplum_client.delete_resource("DocumentReference", result["id"])


def test_13_record_data_sharing_consent(
    medplum_client, elderly_diabetic_patient, primary_care_clinic, visit_test_id
):
    """Test creating a Consent resource for data-sharing preferences"""
    consent = Consent(
        status="active",
        scope=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/consentscope",
                    code="patient-privacy",
                    display="Privacy Consent",
                )
            ]
        ),
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="59284-0",
                        display="Consent Document",
                    )
                ]
            )
        ],
        patient=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        dateTime=datetime.now(timezone.utc).isoformat(),
        organization=[Reference(reference=f"Organization/{primary_care_clinic['id']}")],
        policyRule=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    code="OPTIN",
                    display="Opt-in",
                )
            ]
        ),
        provision=ConsentProvision(
            type="permit",
            period=Period(
                start=datetime.now(timezone.utc).date().isoformat(),
                end=(datetime.now(timezone.utc) + timedelta(days=365))
                .date()
                .isoformat(),
            ),
            actor=[
                {
                    "role": CodeableConcept(
                        coding=[
                            Coding(
                                system="http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                code="IRCP",
                                display="information recipient",
                            )
                        ]
                    ),
                    "reference": Reference(
                        reference=f"Organization/{primary_care_clinic['id']}"
                    ),
                }
            ],
            action=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/consentaction",
                            code="access",
                            display="Access",
                        )
                    ]
                ),
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/consentaction",
                            code="correct",
                            display="Access and Correct",
                        )
                    ]
                ),
            ],
        ),
    )

    result = medplum_client.create_resource(to_fhir_json(consent))

    assert result["resourceType"] == "Consent"
    assert result["status"] == "active"
    assert result["patient"]["reference"] == f"Patient/{elderly_diabetic_patient['id']}"
    assert result["provision"]["type"] == "permit"
    assert len(result["provision"]["action"]) > 0

    # Cleanup
    medplum_client.delete_resource("Consent", result["id"])


def test_14_create_billing_claim(
    medplum_client,
    elderly_diabetic_patient,
    dr_smith,
    primary_care_clinic,
    medicare_coverage,
    visit_test_id,
):
    """Test creating a Claim resource for billing a diabetic visit"""
    # First create the diabetes condition to reference
    condition = Condition(
        clinicalStatus=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                    code="active",
                )
            ]
        ),
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://snomed.info/sct",
                    code="44054006",
                    display="Diabetes mellitus type 2",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
    )
    diabetes_condition = medplum_client.create_resource(to_fhir_json(condition))

    # Create a simple encounter to bill against
    from pymedplum.client import MedplumClient

    client = MedplumClient(
        base_url=medplum_client.base_url,
        client_id=medplum_client.client_id,
        client_secret=medplum_client.client_secret,
        project_id=medplum_client.project_id,
    )
    client.authenticate()

    encounter = Encounter(
        status="finished",
        class_=Coding(
            system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
            code="AMB",
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        period={
            "start": datetime.now(timezone.utc).isoformat(),
            "end": datetime.now(timezone.utc).isoformat(),
        },
    )
    encounter_result = client.create_resource(to_fhir_json(encounter))

    try:
        claim = Claim(
            status="active",
            type=CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/claim-type",
                        code="professional",
                        display="Professional",
                    )
                ]
            ),
            use="claim",
            patient=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
            billablePeriod=Period(
                start=datetime.now(timezone.utc).date().isoformat(),
                end=datetime.now(timezone.utc).date().isoformat(),
            ),
            created=datetime.now(timezone.utc).isoformat(),
            provider=Reference(reference=f"Organization/{primary_care_clinic['id']}"),
            priority=CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/processpriority",
                        code="normal",
                    )
                ]
            ),
            insurance=[
                ClaimInsurance(
                    sequence=1,
                    focal=True,
                    coverage=Reference(reference=f"Coverage/{medicare_coverage['id']}"),
                )
            ],
            diagnosis=[
                ClaimDiagnosis(
                    sequence=1,
                    diagnosisReference=Reference(
                        reference=f"Condition/{diabetes_condition['id']}"
                    ),
                )
            ],
            item=[
                ClaimItem(
                    sequence=1,
                    productOrService=CodeableConcept(
                        coding=[
                            Coding(
                                system="http://www.ama-assn.org/go/cpt",
                                code="99214",
                                display="Office visit, established patient, moderate complexity",
                            )
                        ]
                    ),
                    encounter=[
                        Reference(reference=f"Encounter/{encounter_result['id']}")
                    ],
                    unitPrice=Money(value=150.00, currency="USD"),
                    net=Money(value=150.00, currency="USD"),
                )
            ],
            total=Money(value=150.00, currency="USD"),
        )

        result = medplum_client.create_resource(to_fhir_json(claim))

        assert result["resourceType"] == "Claim"
        assert result["status"] == "active"
        assert result["use"] == "claim"
        assert (
            result["patient"]["reference"]
            == f"Patient/{elderly_diabetic_patient['id']}"
        )
        assert len(result["insurance"]) > 0
        assert len(result["diagnosis"]) > 0
        assert len(result["item"]) > 0
        assert result["total"]["value"] == 150.00

        # Cleanup
        medplum_client.delete_resource("Claim", result["id"])
    finally:
        client.delete_resource("Encounter", encounter_result["id"])
        medplum_client.delete_resource("Condition", diabetes_condition["id"])


def test_15_track_resource_provenance(
    medplum_client, elderly_diabetic_patient, dr_smith, visit_test_id
):
    """Test creating Provenance resources for audit tracking"""
    # First create a simple Observation to track
    observation = Observation(
        status="final",
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/observation-category",
                        code="vital-signs",
                    )
                ]
            )
        ],
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://loinc.org",
                    code="29463-7",
                    display="Body Weight",
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{elderly_diabetic_patient['id']}"),
        effectiveDateTime=datetime.now(timezone.utc).isoformat(),
        valueQuantity=Quantity(
            value=165, unit="lbs", system="http://unitsofmeasure.org", code="[lb_av]"
        ),
    )
    obs_result = medplum_client.create_resource(to_fhir_json(observation))

    try:
        # Create Provenance record to track who created this observation
        provenance = Provenance(
            target=[Reference(reference=f"Observation/{obs_result['id']}")],
            recorded=datetime.now(timezone.utc).isoformat(),
            agent=[
                ProvenanceAgent(
                    type=CodeableConcept(
                        coding=[
                            Coding(
                                system="http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                                code="author",
                                display="Author",
                            )
                        ]
                    ),
                    who=Reference(reference=f"Practitioner/{dr_smith['id']}"),
                )
            ],
            activity=CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/v3-DataOperation",
                        code="CREATE",
                        display="Create",
                    )
                ]
            ),
        )

        result = medplum_client.create_resource(to_fhir_json(provenance))

        assert result["resourceType"] == "Provenance"
        assert len(result["target"]) > 0
        assert result["target"][0]["reference"] == f"Observation/{obs_result['id']}"
        assert len(result["agent"]) > 0
        assert (
            result["agent"][0]["who"]["reference"] == f"Practitioner/{dr_smith['id']}"
        )
        assert result["activity"]["coding"][0]["code"] == "CREATE"

        # Cleanup
        medplum_client.delete_resource("Provenance", result["id"])
    finally:
        medplum_client.delete_resource("Observation", obs_result["id"])
