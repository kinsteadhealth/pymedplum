"""Integration tests simulating a primary care physician's morning EHR workflow.

This test suite models the typical morning routine when a provider logs into their EHR:
1. Review daily schedule and appointments
2. Prepare for patient visits by checking charts
3. Review overnight lab results and critical values
4. Manage inbox/messages from patients and staff
5. Review pending tasks and follow-ups

Based on research showing physicians spend 10-20 minutes on morning preparation
and that inbox management accounts for 24% of EHR time.
"""

from datetime import datetime, timedelta, timezone

import pytest
from fhir.resources.R4B.appointment import Appointment, AppointmentParticipant
from fhir.resources.R4B.attachment import Attachment
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.communication import Communication, CommunicationPayload
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.diagnosticreport import DiagnosticReport
from fhir.resources.R4B.documentreference import (
    DocumentReference,
    DocumentReferenceContent,
)
from fhir.resources.R4B.humanname import HumanName
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.medicationstatement import MedicationStatement
from fhir.resources.R4B.observation import Observation, ObservationReferenceRange
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.period import Period
from fhir.resources.R4B.practitioner import Practitioner
from fhir.resources.R4B.quantity import Quantity
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.servicerequest import ServiceRequest
from fhir.resources.R4B.task import Task, TaskRestriction

from pymedplum import to_fhir_json

# =============================================================================
# Fixtures - Set up morning workflow scenario
# =============================================================================


@pytest.fixture
def dr_morning_provider(medplum_client, test_id):
    """Create the primary care provider logging in for the morning"""
    practitioner = Practitioner(
        name=[HumanName(given=["Sarah"], family="Chen", prefix=["Dr."])],
        identifier=[
            Identifier(
                system="http://example.org/npi",
                value=f"1234567890-{test_id}",
            )
        ],
    )
    result = medplum_client.create_resource(to_fhir_json(practitioner))

    yield result

    # Cleanup
    medplum_client.delete_resource("Practitioner", result["id"])


@pytest.fixture
def morning_patients(medplum_client, test_id):
    """Create 3 patients scheduled for today's appointments"""
    patients = []
    patient_data = [
        ("Robert", "Johnson", "male", 65),  # Diabetic follow-up
        ("Maria", "Garcia", "female", 52),  # Hypertension check
        ("James", "Wilson", "male", 45),  # Annual physical
    ]

    for given, family, gender, age in patient_data:
        patient = Patient(
            name=[HumanName(given=[given], family=f"{family}-{test_id}")],
            gender=gender,
            birthDate=(datetime.now(timezone.utc) - timedelta(days=age * 365)).date(),
            identifier=[
                Identifier(
                    system="http://example.org/mrn",
                    value=f"MRN-{given.lower()}-{test_id}",
                )
            ],
        )
        result = medplum_client.create_resource(to_fhir_json(patient))
        patients.append(result)

    yield patients

    # Cleanup
    for patient in patients:
        medplum_client.delete_resource("Patient", patient["id"])


# =============================================================================
# Test 1: Review Today's Schedule
# =============================================================================


def test_01_review_todays_schedule(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test reviewing today's schedule - first thing providers do in the morning.

    Simulates querying for today's appointments to see patient list and visit types.
    This represents the initial 'dashboard view' when logging into the EHR.
    """
    # Create appointments for today
    today = datetime.now(timezone.utc)
    appointment_times = [
        today.replace(hour=9, minute=0, second=0, microsecond=0),
        today.replace(hour=10, minute=0, second=0, microsecond=0),
        today.replace(hour=11, minute=0, second=0, microsecond=0),
    ]

    appointment_types = [
        ("Diabetes Follow-up", "394701000000101"),
        ("Hypertension Check", "162673000"),
        ("Annual Physical", "410620009"),
    ]

    created_appointments = []

    try:
        # Schedule appointments for the morning
        for _i, (patient, start_time, (type_display, type_code)) in enumerate(
            zip(morning_patients, appointment_times, appointment_types)
        ):
            appointment = Appointment(
                status="booked",
                start=start_time,
                end=start_time + timedelta(minutes=30),
                participant=[
                    AppointmentParticipant(
                        actor=Reference(reference=f"Patient/{patient['id']}"),
                        status="accepted",
                    ),
                    AppointmentParticipant(
                        actor=Reference(
                            reference=f"Practitioner/{dr_morning_provider['id']}"
                        ),
                        status="accepted",
                    ),
                ],
                appointmentType=CodeableConcept(
                    coding=[
                        Coding(
                            system="http://snomed.info/sct",
                            code=type_code,
                            display=type_display,
                        )
                    ]
                ),
                description=f"{type_display} - Test {test_id}",
            )
            result = medplum_client.create_resource(to_fhir_json(appointment))
            created_appointments.append(result)

        # Simulate provider checking their schedule
        # In real EHR: GET /Appointment?actor=Practitioner/{id}&date=today
        schedule_response = medplum_client.search_resources(
            "Appointment",
            {
                "actor": f"Practitioner/{dr_morning_provider['id']}",
                "date": f"ge{today.strftime('%Y-%m-%d')}",
            },
        )

        # Verify schedule was retrieved (may be empty if no appointments found)
        appointments_found = schedule_response.get("entry", [])
        assert len(appointments_found) == 3, (
            f"Should find all 3 appointments, found {len(appointments_found)}"
        )

        # Verify appointment details are accessible
        for entry in appointments_found:
            appt = entry["resource"]
            assert appt["status"] == "booked"
            assert "appointmentType" in appt
            assert len(appt["participant"]) == 2

        print(
            f"✓ Morning schedule review: Found {len(appointments_found)} appointments"
        )

    finally:
        # Cleanup
        for appt in created_appointments:
            medplum_client.delete_resource("Appointment", appt["id"])


# =============================================================================
# Test 2: Prepare for Diabetic Patient Visit
# =============================================================================


def test_02_prepare_for_diabetic_patient(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test chart preparation for diabetic patient (Robert Johnson).

    Simulates reviewing patient's chronic conditions, recent vitals, and medications
    before the appointment - the 10-20 minute preparation mentioned in research.
    """
    robert = morning_patients[0]  # First patient is diabetic

    created_resources = []

    try:
        # Create diabetes condition
        diabetes = Condition(
            subject=Reference(reference=f"Patient/{robert['id']}"),
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="44054006",
                        display="Type 2 Diabetes Mellitus",
                    )
                ],
                text="Type 2 Diabetes Mellitus",
            ),
            clinicalStatus=CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                        code="active",
                    )
                ]
            ),
            recordedDate=datetime.now(timezone.utc)
            - timedelta(days=730),  # 2 years ago
        )
        diabetes_result = medplum_client.create_resource(to_fhir_json(diabetes))
        created_resources.append(("Condition", diabetes_result["id"]))

        # Create recent HbA1c observation (from last month)
        hba1c = Observation(
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="4548-4",
                        display="Hemoglobin A1c/Hemoglobin.total in Blood",
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{robert['id']}"),
            effectiveDateTime=datetime.now(timezone.utc) - timedelta(days=30),
            valueQuantity=Quantity(
                value=7.2, unit="%", system="http://unitsofmeasure.org", code="%"
            ),
            referenceRange=[
                ObservationReferenceRange(
                    low=Quantity(value=4.0, unit="%"),
                    high=Quantity(value=6.0, unit="%"),
                    text="Target range",
                )
            ],
        )
        hba1c_result = medplum_client.create_resource(to_fhir_json(hba1c))
        created_resources.append(("Observation", hba1c_result["id"]))

        # Create active metformin prescription
        metformin = MedicationStatement(
            status="active",
            subject=Reference(reference=f"Patient/{robert['id']}"),
            medicationCodeableConcept=CodeableConcept(
                coding=[
                    Coding(
                        system="http://www.nlm.nih.gov/research/umls/rxnorm",
                        code="860975",
                        display="Metformin 500 MG Oral Tablet",
                    )
                ],
                text="Metformin 500mg twice daily",
            ),
            effectivePeriod=Period(
                start=datetime.now(timezone.utc) - timedelta(days=365),
            ),
        )
        metformin_result = medplum_client.create_resource(to_fhir_json(metformin))
        created_resources.append(("MedicationStatement", metformin_result["id"]))

        # Simulate chart review queries
        # Query 1: Get active conditions
        conditions = medplum_client.search_resources(
            "Condition",
            {
                "patient": robert["id"],
                "clinical-status": "active",
            },
        )
        assert "entry" in conditions
        assert len(conditions["entry"]) >= 1

        # Query 2: Get recent lab results
        recent_labs = medplum_client.search_resources(
            "Observation",
            {
                "patient": robert["id"],
                "code": "4548-4",  # HbA1c LOINC code
                "_sort": "-date",
                "_count": "1",
            },
        )
        assert "entry" in recent_labs
        hba1c_value = recent_labs["entry"][0]["resource"]["valueQuantity"]["value"]
        assert hba1c_value == 7.2

        # Query 3: Get active medications
        medications = medplum_client.search_resources(
            "MedicationStatement",
            {
                "patient": robert["id"],
                "status": "active",
            },
        )
        assert "entry" in medications
        assert len(medications["entry"]) >= 1

        print(
            "✓ Chart preparation complete: Reviewed conditions, labs, and medications"
        )

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)


# =============================================================================
# Test 3: Review Critical Lab Results
# =============================================================================


def test_03_review_critical_lab_results(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test reviewing critical/abnormal lab results from overnight.

    Simulates the important task of checking for critical values that came in
    after hours. This is a key safety check in the morning routine.
    """
    maria = morning_patients[1]  # Second patient (hypertension)

    created_resources = []

    try:
        # Create elevated potassium result (critical value)
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        potassium = Observation(
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="2823-3",
                        display="Potassium [Moles/volume] in Serum or Plasma",
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{maria['id']}"),
            effectiveDateTime=yesterday.replace(hour=22, minute=0),  # 10 PM yesterday
            valueQuantity=Quantity(
                value=5.8,
                unit="mmol/L",
                system="http://unitsofmeasure.org",
                code="mmol/L",
            ),
            referenceRange=[
                ObservationReferenceRange(
                    low=Quantity(value=3.5, unit="mmol/L"),
                    high=Quantity(value=5.0, unit="mmol/L"),
                    text="Normal range",
                )
            ],
            interpretation=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                            code="H",
                            display="High",
                        )
                    ]
                )
            ],
        )
        potassium_result = medplum_client.create_resource(to_fhir_json(potassium))
        created_resources.append(("Observation", potassium_result["id"]))

        # Create diagnostic report grouping the critical lab
        lab_report = DiagnosticReport(
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="24323-8",
                        display="Comprehensive metabolic panel",
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{maria['id']}"),
            effectiveDateTime=yesterday.replace(hour=22, minute=0),
            issued=yesterday.replace(hour=23, minute=0),
            result=[Reference(reference=f"Observation/{potassium_result['id']}")],
            conclusion="Critical: Elevated potassium level requires follow-up",
        )
        report_result = medplum_client.create_resource(to_fhir_json(lab_report))
        created_resources.append(("DiagnosticReport", report_result["id"]))

        # Simulate morning critical lab review
        # Query for abnormal results from the last 24 hours
        medplum_client.search_resources(
            "Observation",
            {
                "patient": maria["id"],
                "date": f"ge{(datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')}",
                "_filter": "value-quantity gt 5.0",  # Assuming this filter works
            },
        )

        # Alternative: Get all recent observations and filter client-side
        recent_obs = medplum_client.search_resources(
            "Observation",
            {
                "patient": maria["id"],
                "date": f"ge{(datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')}",
            },
        )

        assert "entry" in recent_obs
        # Find the critical potassium result
        critical_found = False
        for entry in recent_obs.get("entry", []):
            obs = entry["resource"]
            if "valueQuantity" in obs and obs["valueQuantity"].get("value") == 5.8:
                critical_found = True
                assert (
                    obs.get("interpretation", [{}])[0]
                    .get("coding", [{}])[0]
                    .get("code")
                    == "H"
                )

        assert critical_found, "Should find the critical potassium result"

        print("✓ Critical lab review: Found elevated potassium requiring follow-up")

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)


# =============================================================================
# Test 4: Process Inbox Messages
# =============================================================================


def test_04_process_inbox_messages(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test processing inbox messages - a major morning task.

    Research shows inbox management takes 24% of physician EHR time.
    This simulates reviewing patient portal messages, nurse triage notes, etc.
    """
    robert = morning_patients[0]
    maria = morning_patients[1]

    created_resources = []

    try:
        # Create patient portal message from Robert about symptoms
        patient_message = Communication(
            status="completed",
            subject=Reference(reference=f"Patient/{robert['id']}"),
            sender=Reference(reference=f"Patient/{robert['id']}"),
            recipient=[
                Reference(reference=f"Practitioner/{dr_morning_provider['id']}")
            ],
            sent=datetime.now(timezone.utc) - timedelta(hours=12),
            received=datetime.now(timezone.utc) - timedelta(hours=12),
            payload=[
                CommunicationPayload(
                    contentString="I've been experiencing increased thirst and urination over the past week. Should I be concerned before my appointment today?"
                )
            ],
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/communication-category",
                            code="notification",
                            display="Notification",
                        )
                    ]
                )
            ],
        )
        patient_msg_result = medplum_client.create_resource(
            to_fhir_json(patient_message)
        )
        created_resources.append(("Communication", patient_msg_result["id"]))

        # Create nurse triage message about Maria's blood pressure
        nurse_message = Communication(
            status="completed",
            subject=Reference(reference=f"Patient/{maria['id']}"),
            sender=Reference(
                reference=f"Practitioner/nurse-{test_id}",
                display="Nurse Johnson",
            ),
            recipient=[
                Reference(reference=f"Practitioner/{dr_morning_provider['id']}")
            ],
            sent=datetime.now(timezone.utc) - timedelta(hours=2),
            received=datetime.now(timezone.utc) - timedelta(hours=2),
            payload=[
                CommunicationPayload(
                    contentString="FYI: Patient called this morning with BP reading of 158/95 at home. She has appointment at 10am today."
                )
            ],
            priority="urgent",
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/communication-category",
                            code="alert",
                            display="Alert",
                        )
                    ]
                )
            ],
        )
        nurse_msg_result = medplum_client.create_resource(to_fhir_json(nurse_message))
        created_resources.append(("Communication", nurse_msg_result["id"]))

        # Simulate inbox review
        # Query for unread messages (in real system, would filter by 'received' status)
        inbox_messages = medplum_client.search_resources(
            "Communication",
            {
                "recipient": f"Practitioner/{dr_morning_provider['id']}",
                "sent": f"ge{(datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')}",
            },
        )

        assert "entry" in inbox_messages
        messages = inbox_messages["entry"]
        assert len(messages) >= 2, "Should find both inbox messages"

        # Verify urgent message is flagged
        urgent_found = False
        for entry in messages:
            msg = entry["resource"]
            if msg.get("priority") == "urgent":
                urgent_found = True
                assert "alert" in str(msg.get("category", []))

        assert urgent_found, "Should find urgent message from nurse"

        print(f"✓ Inbox review: Processed {len(messages)} messages, including 1 urgent")

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)


# =============================================================================
# Test 5: Review Pending Tasks
# =============================================================================


def test_05_review_pending_tasks(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test reviewing pending tasks and follow-ups.

    Simulates checking for incomplete tasks from previous days, such as
    pending referrals, unsigned notes, or follow-up requirements.
    """
    robert = morning_patients[0]
    james = morning_patients[2]

    created_resources = []

    try:
        # Create task: Follow up on Robert's eye exam referral
        referral_task = Task(
            status="requested",
            intent="order",
            priority="routine",
            description="Follow up on ophthalmology referral - ensure appointment scheduled",
            for_fhir=Reference(reference=f"Patient/{robert['id']}"),
            owner=Reference(reference=f"Practitioner/{dr_morning_provider['id']}"),
            authoredOn=datetime.now(timezone.utc) - timedelta(days=7),
            restriction=TaskRestriction(
                period=Period(
                    start=datetime.now(timezone.utc) - timedelta(days=7),
                    end=datetime.now(timezone.utc) + timedelta(days=7),
                )
            ),
        )
        task1_result = medplum_client.create_resource(to_fhir_json(referral_task))
        created_resources.append(("Task", task1_result["id"]))

        # Create task: Review James's pre-visit lab results
        lab_review_task = Task(
            status="requested",
            intent="order",
            priority="urgent",
            description="Review lipid panel results before annual physical appointment",
            for_fhir=Reference(reference=f"Patient/{james['id']}"),
            owner=Reference(reference=f"Practitioner/{dr_morning_provider['id']}"),
            authoredOn=datetime.now(timezone.utc) - timedelta(hours=16),
        )
        task2_result = medplum_client.create_resource(to_fhir_json(lab_review_task))
        created_resources.append(("Task", task2_result["id"]))

        # Create task: Sign yesterday's encounter note
        signing_task = Task(
            status="in-progress",
            intent="order",
            priority="urgent",
            description="Sign encounter note from yesterday's visit",
            owner=Reference(reference=f"Practitioner/{dr_morning_provider['id']}"),
            authoredOn=datetime.now(timezone.utc) - timedelta(days=1),
        )
        task3_result = medplum_client.create_resource(to_fhir_json(signing_task))
        created_resources.append(("Task", task3_result["id"]))

        # Simulate morning task review
        # Query 1: Get all open tasks
        open_tasks = medplum_client.search_resources(
            "Task",
            {
                "owner": f"Practitioner/{dr_morning_provider['id']}",
                "status": "requested,in-progress",
            },
        )

        assert "entry" in open_tasks
        tasks = open_tasks["entry"]
        assert len(tasks) >= 3, "Should find all 3 pending tasks"

        # Query 2: Get urgent tasks
        urgent_tasks = medplum_client.search_resources(
            "Task",
            {
                "owner": f"Practitioner/{dr_morning_provider['id']}",
                "priority": "urgent",
            },
        )

        assert "entry" in urgent_tasks
        urgent_count = len(urgent_tasks["entry"])
        assert urgent_count >= 2, "Should find 2 urgent tasks"

        # Verify task priorities
        routine_count = sum(
            1 for entry in tasks if entry["resource"].get("priority") == "routine"
        )
        assert routine_count >= 1

        print(f"✓ Task review: Found {len(tasks)} open tasks ({urgent_count} urgent)")

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)


# =============================================================================
# Test 6: Check Preventive Care Gaps
# =============================================================================


def test_06_check_preventive_care_gaps(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test checking for preventive care gaps before patient visits.

    Part of chart preparation - ensuring chronic and preventive care is up-to-date
    as mentioned in the research.
    """
    james = morning_patients[2]  # Annual physical patient

    created_resources = []

    try:
        # Create service request for overdue colonoscopy (45 years old, due for screening)
        colonoscopy_request = ServiceRequest(
            status="active",
            intent="proposal",
            priority="routine",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code="73761001",
                        display="Colonoscopy",
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{james['id']}"),
            authoredOn=datetime.now(timezone.utc),
            requester=Reference(reference=f"Practitioner/{dr_morning_provider['id']}"),
            reasonCode=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://snomed.info/sct",
                            code="268548003",
                            display="Screening for malignant neoplasm of colon",
                        )
                    ],
                    text="Colorectal cancer screening - patient is 45 years old",
                )
            ],
        )
        colonoscopy_result = medplum_client.create_resource(
            to_fhir_json(colonoscopy_request)
        )
        created_resources.append(("ServiceRequest", colonoscopy_result["id"]))

        # Query for pending service requests (preventive care gaps)
        pending_services = medplum_client.search_resources(
            "ServiceRequest",
            {
                "patient": james["id"],
                "status": "active",
                "intent": "proposal",
            },
        )

        assert "entry" in pending_services
        services = pending_services["entry"]
        assert len(services) >= 1

        # Verify colonoscopy screening is in the list
        colonoscopy_found = False
        for entry in services:
            sr = entry["resource"]
            if "73761001" in str(sr.get("code", {})):
                colonoscopy_found = True
                assert (
                    "screening" in sr.get("reasonCode", [{}])[0].get("text", "").lower()
                )

        assert colonoscopy_found, "Should identify colonoscopy screening gap"

        print("✓ Preventive care review: Identified colonoscopy screening due")

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)


# =============================================================================
# Test 7: Review Overnight Documents/Faxes
# =============================================================================


def test_07_review_overnight_documents(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test reviewing documents/faxes that arrived overnight.

    Research mentions physicians review faxes in the morning. This simulates
    checking for new consultation reports, lab results, or hospital records.
    """
    robert = morning_patients[0]

    created_resources = []

    try:
        # Create document reference for cardiology consultation report (faxed overnight)
        overnight_fax = DocumentReference(
            status="current",
            docStatus="final",
            type=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="34117-2",
                        display="History and physical note",
                    )
                ]
            ),
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category",
                            code="clinical-note",
                        )
                    ]
                )
            ],
            subject=Reference(reference=f"Patient/{robert['id']}"),
            date=datetime.now(timezone.utc)
            - timedelta(hours=8),  # 8 hours ago (midnight)
            author=[
                Reference(
                    reference="Practitioner/cardiologist-123",
                    display="Dr. Patel, Cardiology",
                )
            ],
            description="Cardiology consultation for evaluation of diabetic patient with chest pain - ECG normal, stress test recommended",
            content=[
                DocumentReferenceContent(
                    attachment=Attachment(
                        contentType="application/pdf",
                        title="Cardiology Consultation Report",
                        creation=datetime.now(timezone.utc) - timedelta(hours=8),
                        size=1024,
                    )
                )
            ],
        )
        fax_result = medplum_client.create_resource(to_fhir_json(overnight_fax))
        created_resources.append(("DocumentReference", fax_result["id"]))

        # Query for new documents received in last 24 hours
        recent_documents = medplum_client.search_resources(
            "DocumentReference",
            {
                "patient": robert["id"],
                "date": f"ge{(datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')}",
            },
        )

        assert "entry" in recent_documents
        docs = recent_documents["entry"]
        assert len(docs) >= 1

        # Verify cardiology consultation is in the list
        consultation_found = False
        for entry in docs:
            doc = entry["resource"]
            if "Cardiology" in doc.get("description", ""):
                consultation_found = True
                assert doc["status"] == "current"
                assert "clinical-note" in str(doc.get("category", []))

        assert consultation_found, "Should find overnight cardiology consultation"

        print("✓ Document review: Found cardiology consultation received overnight")

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)


# =============================================================================
# Test 8: Comprehensive Morning Workflow
# =============================================================================


def test_08_comprehensive_morning_workflow(
    medplum_client,
    dr_morning_provider,
    morning_patients,
    test_id,
):
    """Test the complete morning workflow in sequence.

    Simulates the full 10-20 minute morning preparation routine:
    1. Check schedule
    2. Review patient charts
    3. Check critical labs
    4. Process messages
    5. Review tasks

    This integration test validates that all morning queries work together.
    """
    robert = morning_patients[0]
    maria = morning_patients[1]
    james = morning_patients[2]

    workflow_stats = {
        "appointments": 0,
        "critical_labs": 0,
        "messages": 0,
        "tasks": 0,
        "preventive_gaps": 0,
    }

    created_resources = []

    try:
        # Step 1: Create morning schedule
        today = datetime.now(timezone.utc)
        for i, patient in enumerate(morning_patients):
            appt = Appointment(
                status="booked",
                start=today.replace(hour=9 + i, minute=0, second=0, microsecond=0),
                end=today.replace(hour=9 + i, minute=30, second=0, microsecond=0),
                participant=[
                    AppointmentParticipant(
                        actor=Reference(reference=f"Patient/{patient['id']}"),
                        status="accepted",
                    ),
                    AppointmentParticipant(
                        actor=Reference(
                            reference=f"Practitioner/{dr_morning_provider['id']}"
                        ),
                        status="accepted",
                    ),
                ],
            )
            result = medplum_client.create_resource(to_fhir_json(appt))
            created_resources.append(("Appointment", result["id"]))
            workflow_stats["appointments"] += 1

        # Step 2: Create critical lab for review
        critical_glucose = Observation(
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(system="http://loinc.org", code="2345-7", display="Glucose")
                ]
            ),
            subject=Reference(reference=f"Patient/{robert['id']}"),
            effectiveDateTime=datetime.now(timezone.utc) - timedelta(hours=10),
            valueQuantity=Quantity(value=250, unit="mg/dL"),
            interpretation=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                            code="HH",
                            display="Critical high",
                        )
                    ]
                )
            ],
        )
        glucose_result = medplum_client.create_resource(to_fhir_json(critical_glucose))
        created_resources.append(("Observation", glucose_result["id"]))
        workflow_stats["critical_labs"] += 1

        # Step 3: Create inbox message
        msg = Communication(
            status="completed",
            subject=Reference(reference=f"Patient/{maria['id']}"),
            sender=Reference(reference=f"Patient/{maria['id']}"),
            recipient=[
                Reference(reference=f"Practitioner/{dr_morning_provider['id']}")
            ],
            sent=datetime.now(timezone.utc) - timedelta(hours=6),
            payload=[
                CommunicationPayload(
                    contentString="Question about medication side effects"
                )
            ],
        )
        msg_result = medplum_client.create_resource(to_fhir_json(msg))
        created_resources.append(("Communication", msg_result["id"]))
        workflow_stats["messages"] += 1

        # Step 4: Create pending task
        task = Task(
            status="requested",
            intent="order",
            priority="urgent",
            description="Review pre-visit labs",
            for_fhir=Reference(reference=f"Patient/{james['id']}"),
            owner=Reference(reference=f"Practitioner/{dr_morning_provider['id']}"),
            authoredOn=datetime.now(timezone.utc) - timedelta(hours=12),
        )
        task_result = medplum_client.create_resource(to_fhir_json(task))
        created_resources.append(("Task", task_result["id"]))
        workflow_stats["tasks"] += 1

        # Now simulate the morning workflow queries

        # Query 1: Get today's schedule
        schedule = medplum_client.search_resources(
            "Appointment",
            {
                "actor": f"Practitioner/{dr_morning_provider['id']}",
                "date": f"ge{today.strftime('%Y-%m-%d')}",
            },
        )
        assert len(schedule.get("entry", [])) == workflow_stats["appointments"]

        # Query 2: Get critical labs from last 24 hours
        critical_labs = medplum_client.search_resources(
            "Observation",
            {
                "date": f"ge{(datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')}",
            },
        )
        # Note: In production, would filter by interpretation=HH|H
        assert "entry" in critical_labs

        # Query 3: Get unread messages
        messages = medplum_client.search_resources(
            "Communication",
            {
                "recipient": f"Practitioner/{dr_morning_provider['id']}",
                "sent": f"ge{(datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')}",
            },
        )
        assert len(messages.get("entry", [])) >= workflow_stats["messages"]

        # Query 4: Get pending tasks
        tasks = medplum_client.search_resources(
            "Task",
            {
                "owner": f"Practitioner/{dr_morning_provider['id']}",
                "status": "requested",
            },
        )
        assert len(tasks.get("entry", [])) >= workflow_stats["tasks"]

        print(
            f"""
✓ Comprehensive morning workflow completed:
  - {workflow_stats["appointments"]} appointments on schedule
  - {workflow_stats["critical_labs"]} critical lab result to review
  - {workflow_stats["messages"]} inbox message to process
  - {workflow_stats["tasks"]} pending task to complete

  Total preparation time: ~10-20 minutes (simulated)
        """
        )

    finally:
        # Cleanup
        for resource_type, resource_id in created_resources:
            medplum_client.delete_resource(resource_type, resource_id)
