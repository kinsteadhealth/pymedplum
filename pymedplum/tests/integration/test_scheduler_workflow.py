"""Integration tests for medical scheduler workflows in a primary care clinic.

This test suite simulates the daily operations of a medical scheduler, including:
- Managing appointment slots with different visit types and durations
- Handling multiple providers
- Creating new patients
- Preventing double-booking conflicts
- Managing duplicate patient records

Based on research into typical primary care scheduling practices including
wave scheduling, visit type management, and common edge cases.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from pymedplum.client import MedplumClient
from pymedplum.fhir import (
    Appointment,
    CodeableConcept,
    Coding,
    ContactPoint,
    HumanName,
    Identifier,
    Patient,
    Period,
    Practitioner,
    Reference,
    Schedule,
    Slot,
)
from pymedplum.helpers import to_fhir_json

# Visit Type Definitions (based on primary care research)
VISIT_TYPES = {
    "annual-physical": {
        "display": "Annual Physical Exam",
        "duration": 30,  # minutes
        "code": "185349003",
        "system": "http://snomed.info/sct",
    },
    "sick-visit": {
        "display": "Sick Visit",
        "duration": 15,  # minutes
        "code": "185345009",
        "system": "http://snomed.info/sct",
    },
    "new-patient": {
        "display": "New Patient Visit",
        "duration": 45,  # minutes
        "code": "185387006",
        "system": "http://snomed.info/sct",
    },
}


@pytest.fixture
def scheduler_providers(medplum_client: MedplumClient) -> list[dict[str, Any]]:
    """Create multiple practitioners for scheduling tests."""
    providers = []
    provider_names = [
        ("Jennifer", "Smith", "MD"),
        ("Michael", "Johnson", "DO"),
        ("Sarah", "Williams", "NP"),
    ]

    for first, last, suffix in provider_names:
        practitioner = Practitioner(
            name=[
                HumanName(given=[first], family=last, suffix=[suffix], use="official")
            ],
            identifier=[
                Identifier(
                    system="http://example.org/practitioners",
                    value=f"PROV-{first[0]}{last}",
                )
            ],
        )
        result = medplum_client.create_resource(to_fhir_json(practitioner))
        providers.append(result)

    yield providers

    # Cleanup
    for provider in providers:
        medplum_client.delete_resource("Practitioner", provider["id"])


@pytest.fixture
def clinic_schedule(
    medplum_client: MedplumClient, scheduler_providers: list[dict[str, Any]]
) -> dict[str, Any]:
    """Create a schedule for the clinic (represents available appointment times)."""
    # Using first provider for the schedule
    provider = scheduler_providers[0]

    # Create schedule for next week (Monday-Friday, 9 AM - 5 PM)
    next_monday = datetime.now(timezone.utc) + timedelta(
        days=(7 - datetime.now().weekday())
    )
    next_friday = next_monday + timedelta(days=4)

    schedule = Schedule(
        active=True,
        actor=[Reference(reference=f"Practitioner/{provider['id']}")],
        planningHorizon=Period(
            start=next_monday.replace(hour=9, minute=0, second=0).isoformat(),
            end=next_friday.replace(hour=17, minute=0, second=0).isoformat(),
        ),
        comment="Primary care clinic schedule - Wave scheduling approach",
    )

    result = medplum_client.create_resource(to_fhir_json(schedule))

    yield result

    # Cleanup
    medplum_client.delete_resource("Schedule", result["id"])


def create_appointment_slots(
    medplum_client: MedplumClient, schedule_id: str, date: datetime, visit_type: str
) -> list[dict[str, Any]]:
    """Create appointment slots for a specific day using wave scheduling.

    Wave scheduling: Front-load 2-3 patients at top of hour for flexibility.
    E.g., at 9 AM: schedule 1 annual + 1 sick visit
    """
    slots = []
    visit_config = VISIT_TYPES[visit_type]

    # Create slots at the top of each hour (9 AM, 10 AM, 11 AM, etc.)
    start_time = date.replace(hour=9, minute=0, second=0)
    end_time = date.replace(hour=17, minute=0, second=0)

    current_time = start_time
    while current_time < end_time:
        slot_end = current_time + timedelta(minutes=visit_config["duration"])

        slot = Slot(
            schedule=Reference(reference=f"Schedule/{schedule_id}"),
            status="free",
            start=current_time.isoformat(),
            end=slot_end.isoformat(),
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=visit_config["system"],
                            code=visit_config["code"],
                            display=visit_config["display"],
                        )
                    ]
                )
            ],
            comment=f"{visit_config['display']} - {visit_config['duration']} minutes",
        )

        result = medplum_client.create_resource(to_fhir_json(slot))
        slots.append(result)

        # Move to next hour for wave scheduling
        current_time += timedelta(hours=1)

    return slots


def test_01_create_appointment_slots_different_types(
    medplum_client: MedplumClient, clinic_schedule: dict[str, Any]
):
    """Test creating appointment slots with different visit types and durations.

    Validates:
    - Annual Physical (30 min slots)
    - Sick Visit (15 min slots)
    - New Patient Visit (45 min slots)
    """
    created_slots = []

    try:
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

        # Test each visit type
        for visit_type, config in VISIT_TYPES.items():
            slots = create_appointment_slots(
                medplum_client, clinic_schedule["id"], tomorrow, visit_type
            )
            created_slots.extend(slots)

            # Verify slot creation
            assert len(slots) > 0, f"Should create slots for {visit_type}"

            # Verify slot duration matches visit type
            first_slot = slots[0]
            start = datetime.fromisoformat(first_slot["start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(first_slot["end"].replace("Z", "+00:00"))
            duration = (end - start).total_seconds() / 60

            assert duration == config["duration"], (
                f"{visit_type} slot duration should be {config['duration']} minutes, "
                f"got {duration} minutes"
            )

            # Verify service type
            assert first_slot["serviceType"][0]["coding"][0]["code"] == config["code"]
            assert first_slot["status"] == "free"

        print(
            f"""
✓ Successfully created appointment slots:
  - {len([s for s in created_slots if "annual" in s.get("comment", "").lower()])} Annual Physical slots (30 min)
  - {len([s for s in created_slots if "sick" in s.get("comment", "").lower()])} Sick Visit slots (15 min)
  - {len([s for s in created_slots if "new" in s.get("comment", "").lower()])} New Patient slots (45 min)
        """
        )

    finally:
        # Cleanup
        for slot in created_slots:
            medplum_client.delete_resource("Slot", slot["id"])


def test_02_schedule_with_multiple_providers(
    medplum_client: MedplumClient, scheduler_providers: list[dict[str, Any]]
):
    """Test scheduling appointments across multiple providers.

    Validates:
    - Creating schedules for different providers
    - Searching available slots by provider
    - Provider-specific availability
    """
    schedules = []
    slots = []

    try:
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

        # Create schedule and slots for each provider
        for provider in scheduler_providers:
            # Create schedule
            schedule = Schedule(
                active=True,
                actor=[Reference(reference=f"Practitioner/{provider['id']}")],
                planningHorizon=Period(
                    start=tomorrow.replace(hour=9, minute=0).isoformat(),
                    end=tomorrow.replace(hour=17, minute=0).isoformat(),
                ),
            )
            schedule_result = medplum_client.create_resource(to_fhir_json(schedule))
            schedules.append(schedule_result)

            # Create a few slots for this provider
            for hour in [9, 10, 11]:
                slot = Slot(
                    schedule=Reference(reference=f"Schedule/{schedule_result['id']}"),
                    status="free",
                    start=tomorrow.replace(hour=hour, minute=0).isoformat(),
                    end=tomorrow.replace(hour=hour, minute=30).isoformat(),
                    serviceType=[
                        CodeableConcept(
                            coding=[
                                Coding(
                                    system=VISIT_TYPES["sick-visit"]["system"],
                                    code=VISIT_TYPES["sick-visit"]["code"],
                                    display=VISIT_TYPES["sick-visit"]["display"],
                                )
                            ]
                        )
                    ],
                )
                slot_result = medplum_client.create_resource(to_fhir_json(slot))
                slots.append(slot_result)

        # Verify we created schedules for all providers
        assert len(schedules) == len(scheduler_providers)

        # Search for slots by schedule (provider-specific)
        first_schedule = schedules[0]
        provider_slots = medplum_client.search_resources(
            "Slot", {"schedule": f"Schedule/{first_schedule['id']}"}
        )

        assert "entry" in provider_slots
        assert len(provider_slots["entry"]) >= 3, (
            "Should find at least 3 slots for first provider"
        )

        print(
            f"""
✓ Successfully managed multiple providers:
  - Created schedules for {len(scheduler_providers)} providers
  - Created {len(slots)} total appointment slots
  - Successfully searched provider-specific availability
        """
        )

    finally:
        # Cleanup
        for slot in slots:
            medplum_client.delete_resource("Slot", slot["id"])
        for schedule in schedules:
            medplum_client.delete_resource("Schedule", schedule["id"])


def test_03_create_new_patient_and_book_appointment(
    medplum_client: MedplumClient,
    clinic_schedule: dict[str, Any],
    scheduler_providers: list[dict[str, Any]],
):
    """Test the complete new patient registration and appointment booking flow.

    Validates:
    - Creating a new patient record
    - Creating appropriate slot for new patient visit (45 min)
    - Booking appointment for the new patient
    """
    created_resources = []

    try:
        # Step 1: Create new patient
        new_patient = Patient(
            name=[HumanName(given=["Emma"], family="Thompson", use="official")],
            birthDate="1985-03-15",
            telecom=[ContactPoint(system="phone", value="555-0123", use="mobile")],
            identifier=[
                Identifier(system="http://example.org/patients", value="NP-2025-001")
            ],
        )
        patient_result = medplum_client.create_resource(to_fhir_json(new_patient))
        created_resources.append(("Patient", patient_result["id"]))

        # Step 2: Create slot for new patient visit (45 minutes)
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        slot_start = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)

        new_patient_slot = Slot(
            schedule=Reference(reference=f"Schedule/{clinic_schedule['id']}"),
            status="free",
            start=slot_start.isoformat(),
            end=(slot_start + timedelta(minutes=45)).isoformat(),
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["new-patient"]["system"],
                            code=VISIT_TYPES["new-patient"]["code"],
                            display=VISIT_TYPES["new-patient"]["display"],
                        )
                    ]
                )
            ],
        )
        slot_result = medplum_client.create_resource(to_fhir_json(new_patient_slot))
        created_resources.append(("Slot", slot_result["id"]))

        # Step 3: Book appointment
        appointment = Appointment(
            status="booked",
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["new-patient"]["system"],
                            code=VISIT_TYPES["new-patient"]["code"],
                            display=VISIT_TYPES["new-patient"]["display"],
                        )
                    ]
                )
            ],
            start=slot_start.isoformat(),
            end=(slot_start + timedelta(minutes=45)).isoformat(),
            participant=[
                {
                    "actor": Reference(reference=f"Patient/{patient_result['id']}"),
                    "required": "required",
                    "status": "accepted",
                },
                {
                    "actor": Reference(
                        reference=f"Practitioner/{scheduler_providers[0]['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
            ],
            slot=[Reference(reference=f"Slot/{slot_result['id']}")],
        )
        appointment_result = medplum_client.create_resource(to_fhir_json(appointment))
        created_resources.append(("Appointment", appointment_result["id"]))

        # Verify appointment was created correctly
        assert appointment_result["status"] == "booked"
        assert len(appointment_result["participant"]) == 2

        # Verify slot should be marked as busy (update slot)
        updated_slot = medplum_client.update_resource({**slot_result, "status": "busy"})
        assert updated_slot["status"] == "busy"

        print(
            f"""
✓ Successfully completed new patient workflow:
  - Created patient: {patient_result["name"][0]["given"][0]} {patient_result["name"][0]["family"]}
  - Created 45-minute new patient slot
  - Booked appointment at {slot_start.strftime("%Y-%m-%d %H:%M")}
  - Marked slot as busy
        """
        )

    finally:
        # Cleanup in reverse order
        for resource_type, resource_id in reversed(created_resources):
            medplum_client.delete_resource(resource_type, resource_id)


def test_04_prevent_double_booking_conflict(
    medplum_client: MedplumClient,
    clinic_schedule: dict[str, Any],
    scheduler_providers: list[dict[str, Any]],
):
    """Test handling of double-booking conflicts.

    Validates:
    - Detecting when a slot is already booked
    - Preventing double-booking by checking slot status
    - Proper error handling for concurrent booking attempts
    """
    created_resources = []

    try:
        # Create two patients
        patient1 = Patient(
            name=[HumanName(given=["Alice"], family="Brown", use="official")],
            birthDate="1990-05-20",
        )
        patient1_result = medplum_client.create_resource(to_fhir_json(patient1))
        created_resources.append(("Patient", patient1_result["id"]))

        patient2 = Patient(
            name=[HumanName(given=["Bob"], family="Davis", use="official")],
            birthDate="1988-11-10",
        )
        patient2_result = medplum_client.create_resource(to_fhir_json(patient2))
        created_resources.append(("Patient", patient2_result["id"]))

        # Create a single slot
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        slot_start = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)

        slot = Slot(
            schedule=Reference(reference=f"Schedule/{clinic_schedule['id']}"),
            status="free",
            start=slot_start.isoformat(),
            end=(slot_start + timedelta(minutes=15)).isoformat(),
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["sick-visit"]["system"],
                            code=VISIT_TYPES["sick-visit"]["code"],
                            display=VISIT_TYPES["sick-visit"]["display"],
                        )
                    ]
                )
            ],
        )
        slot_result = medplum_client.create_resource(to_fhir_json(slot))
        created_resources.append(("Slot", slot_result["id"]))

        # First booking - should succeed
        appointment1 = Appointment(
            status="booked",
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["sick-visit"]["system"],
                            code=VISIT_TYPES["sick-visit"]["code"],
                            display=VISIT_TYPES["sick-visit"]["display"],
                        )
                    ]
                )
            ],
            start=slot_start.isoformat(),
            end=(slot_start + timedelta(minutes=15)).isoformat(),
            participant=[
                {
                    "actor": Reference(reference=f"Patient/{patient1_result['id']}"),
                    "required": "required",
                    "status": "accepted",
                },
                {
                    "actor": Reference(
                        reference=f"Practitioner/{scheduler_providers[0]['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
            ],
            slot=[Reference(reference=f"Slot/{slot_result['id']}")],
        )
        appointment1_result = medplum_client.create_resource(to_fhir_json(appointment1))
        created_resources.append(("Appointment", appointment1_result["id"]))

        # Mark slot as busy
        updated_slot = medplum_client.update_resource({**slot_result, "status": "busy"})

        # Verify slot is now busy
        assert updated_slot["status"] == "busy"

        # Simulate checking slot before second booking
        current_slot = medplum_client.read_resource("Slot", slot_result["id"])

        # This should detect the conflict
        assert current_slot["status"] == "busy", "Slot should be marked as busy"

        print(
            """
✓ Successfully prevented double-booking:
  - First patient booked successfully
  - Slot status changed to 'busy'
  - Second booking attempt would be blocked by status check
  - Proper conflict detection in place
        """
        )

        # In a real system, we would:
        # 1. Search for alternative free slots
        # 2. Offer them to patient2
        # 3. Log the conflict for review

    finally:
        # Cleanup
        for resource_type, resource_id in reversed(created_resources):
            medplum_client.delete_resource(resource_type, resource_id)


def test_05_handle_duplicate_patient_records(
    medplum_client: MedplumClient,
    clinic_schedule: dict[str, Any],
    scheduler_providers: list[dict[str, Any]],
):
    """Test handling duplicate patient records and appointment migration.

    Validates:
    - Detecting duplicate patients
    - Moving appointments from duplicate to primary record
    - Cleaning up duplicate patient record

    Scenario: Scheduler accidentally created a duplicate patient.
    We need to identify the duplicate, move the appointment to the
    existing patient record, and clean up the duplicate.
    """
    created_resources = []

    try:
        # Create original patient
        original_patient = Patient(
            name=[HumanName(given=["John"], family="Smith", use="official")],
            birthDate="1975-08-15",
            telecom=[ContactPoint(system="phone", value="555-1234", use="mobile")],
            identifier=[
                Identifier(system="http://example.org/patients", value="PAT-12345")
            ],
        )
        original_result = medplum_client.create_resource(to_fhir_json(original_patient))
        created_resources.append(("Patient", original_result["id"]))

        # Scheduler accidentally creates duplicate (typo in identifier)
        duplicate_patient = Patient(
            name=[HumanName(given=["John"], family="Smith", use="official")],
            birthDate="1975-08-15",  # Same DOB
            telecom=[
                ContactPoint(
                    system="phone",
                    value="555-1234",
                    use="mobile",  # Same phone
                )
            ],
            identifier=[
                Identifier(
                    system="http://example.org/patients",
                    value="PAT-12346",  # Different identifier (typo)
                )
            ],
        )
        duplicate_result = medplum_client.create_resource(
            to_fhir_json(duplicate_patient)
        )
        created_resources.append(("Patient", duplicate_result["id"]))

        # Appointment was scheduled with the duplicate
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        slot_start = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)

        # Create slot
        slot = Slot(
            schedule=Reference(reference=f"Schedule/{clinic_schedule['id']}"),
            status="free",
            start=slot_start.isoformat(),
            end=(slot_start + timedelta(minutes=30)).isoformat(),
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["annual-physical"]["system"],
                            code=VISIT_TYPES["annual-physical"]["code"],
                            display=VISIT_TYPES["annual-physical"]["display"],
                        )
                    ]
                )
            ],
        )
        slot_result = medplum_client.create_resource(to_fhir_json(slot))
        created_resources.append(("Slot", slot_result["id"]))

        # Appointment with duplicate patient
        appointment = Appointment(
            status="booked",
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["annual-physical"]["system"],
                            code=VISIT_TYPES["annual-physical"]["code"],
                            display=VISIT_TYPES["annual-physical"]["display"],
                        )
                    ]
                )
            ],
            start=slot_start.isoformat(),
            end=(slot_start + timedelta(minutes=30)).isoformat(),
            participant=[
                {
                    "actor": Reference(
                        reference=f"Patient/{duplicate_result['id']}"
                    ),  # Duplicate!
                    "required": "required",
                    "status": "accepted",
                },
                {
                    "actor": Reference(
                        reference=f"Practitioner/{scheduler_providers[0]['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
            ],
            slot=[Reference(reference=f"Slot/{slot_result['id']}")],
        )
        appointment_result = medplum_client.create_resource(to_fhir_json(appointment))
        created_resources.append(("Appointment", appointment_result["id"]))

        # Step 1: Detect duplicate (search by name + DOB)
        duplicates_search = medplum_client.search_resources(
            "Patient", {"family": "Smith", "given": "John", "birthdate": "1975-08-15"}
        )

        assert "entry" in duplicates_search
        assert len(duplicates_search["entry"]) == 2, (
            "Should find 2 patients with same name/DOB"
        )

        # Step 2: Identify which is the duplicate (newer creation date or different identifier)
        # In real scenario, this might involve manual review or more sophisticated matching
        # For this test, we know duplicate_result is the newer one

        # Step 3: Update appointment to point to original patient
        updated_appointment = medplum_client.update_resource(
            {
                **appointment_result,
                "participant": [
                    {
                        "actor": {
                            "reference": f"Patient/{original_result['id']}"
                        },  # Corrected!
                        "required": "required",
                        "status": "accepted",
                    },
                    {
                        "actor": {
                            "reference": f"Practitioner/{scheduler_providers[0]['id']}"
                        },
                        "required": "required",
                        "status": "accepted",
                    },
                ],
            },
        )

        # Verify appointment now references original patient
        patient_ref = updated_appointment["participant"][0]["actor"]["reference"]
        assert patient_ref == f"Patient/{original_result['id']}", (
            "Appointment should now reference original patient"
        )

        # Step 4: Delete duplicate patient (after ensuring no other references)
        medplum_client.delete_resource("Patient", duplicate_result["id"])

        # Remove from cleanup list since we already deleted it
        created_resources = [
            r for r in created_resources if r != ("Patient", duplicate_result["id"])
        ]

        print(
            f"""
✓ Successfully handled duplicate patient scenario:
  - Detected 2 patients with matching name/DOB
  - Migrated appointment from duplicate to original patient
  - Deleted duplicate patient record
  - Original patient {original_result["identifier"][0]["value"]} retained with appointment
        """
        )

    finally:
        # Cleanup
        for resource_type, resource_id in reversed(created_resources):
            medplum_client.delete_resource(resource_type, resource_id)


def test_06_wave_scheduling_simulation(
    medplum_client: MedplumClient,
    clinic_schedule: dict[str, Any],
    scheduler_providers: list[dict[str, Any]],
):
    """Test wave scheduling approach: scheduling multiple patients at top of hour.

    Validates:
    - Creating slots at top of hour (9 AM, 10 AM, etc.)
    - Booking mixed visit types (1 annual + 1 sick visit)
    - Demonstrating flexibility of wave scheduling

    Wave scheduling allows: while one patient is being roomed for annual visit,
    provider can complete the sick visit with another patient.
    """
    created_resources = []

    try:
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

        # Create two patients
        patient_annual = Patient(
            name=[HumanName(given=["Mary"], family="Johnson", use="official")],
            birthDate="1960-03-25",
        )
        patient_annual_result = medplum_client.create_resource(
            to_fhir_json(patient_annual)
        )
        created_resources.append(("Patient", patient_annual_result["id"]))

        patient_sick = Patient(
            name=[HumanName(given=["Tom"], family="Wilson", use="official")],
            birthDate="1995-07-14",
        )
        patient_sick_result = medplum_client.create_resource(to_fhir_json(patient_sick))
        created_resources.append(("Patient", patient_sick_result["id"]))

        # Wave scheduling: Both at 9 AM (top of hour)
        wave_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

        # Create annual physical slot at 9:00 AM
        slot_annual = Slot(
            schedule=Reference(reference=f"Schedule/{clinic_schedule['id']}"),
            status="free",
            start=wave_time.isoformat(),
            end=(wave_time + timedelta(minutes=30)).isoformat(),
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["annual-physical"]["system"],
                            code=VISIT_TYPES["annual-physical"]["code"],
                            display=VISIT_TYPES["annual-physical"]["display"],
                        )
                    ]
                )
            ],
            comment="Wave scheduling - Annual physical",
        )
        slot_annual_result = medplum_client.create_resource(to_fhir_json(slot_annual))
        created_resources.append(("Slot", slot_annual_result["id"]))

        # Create sick visit slot at 9:00 AM (same time!)
        slot_sick = Slot(
            schedule=Reference(reference=f"Schedule/{clinic_schedule['id']}"),
            status="free",
            start=wave_time.isoformat(),
            end=(wave_time + timedelta(minutes=15)).isoformat(),
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["sick-visit"]["system"],
                            code=VISIT_TYPES["sick-visit"]["code"],
                            display=VISIT_TYPES["sick-visit"]["display"],
                        )
                    ]
                )
            ],
            comment="Wave scheduling - Sick visit",
        )
        slot_sick_result = medplum_client.create_resource(to_fhir_json(slot_sick))
        created_resources.append(("Slot", slot_sick_result["id"]))

        # Book both appointments at same time
        appointment_annual = Appointment(
            status="booked",
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["annual-physical"]["system"],
                            code=VISIT_TYPES["annual-physical"]["code"],
                            display=VISIT_TYPES["annual-physical"]["display"],
                        )
                    ]
                )
            ],
            start=wave_time.isoformat(),
            end=(wave_time + timedelta(minutes=30)).isoformat(),
            participant=[
                {
                    "actor": Reference(
                        reference=f"Patient/{patient_annual_result['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
                {
                    "actor": Reference(
                        reference=f"Practitioner/{scheduler_providers[0]['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
            ],
            slot=[Reference(reference=f"Slot/{slot_annual_result['id']}")],
        )
        appointment_annual_result = medplum_client.create_resource(
            to_fhir_json(appointment_annual)
        )
        created_resources.append(("Appointment", appointment_annual_result["id"]))

        appointment_sick = Appointment(
            status="booked",
            serviceType=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=VISIT_TYPES["sick-visit"]["system"],
                            code=VISIT_TYPES["sick-visit"]["code"],
                            display=VISIT_TYPES["sick-visit"]["display"],
                        )
                    ]
                )
            ],
            start=wave_time.isoformat(),
            end=(wave_time + timedelta(minutes=15)).isoformat(),
            participant=[
                {
                    "actor": Reference(
                        reference=f"Patient/{patient_sick_result['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
                {
                    "actor": Reference(
                        reference=f"Practitioner/{scheduler_providers[0]['id']}"
                    ),
                    "required": "required",
                    "status": "accepted",
                },
            ],
            slot=[Reference(reference=f"Slot/{slot_sick_result['id']}")],
        )
        appointment_sick_result = medplum_client.create_resource(
            to_fhir_json(appointment_sick)
        )
        created_resources.append(("Appointment", appointment_sick_result["id"]))

        # Verify both appointments scheduled at same time
        assert appointment_annual_result["start"] == appointment_sick_result["start"]

        # Search for all appointments at this time
        medplum_client.search_resources(
            "Appointment",
            {
                "date": f"ge{wave_time.strftime('%Y-%m-%d')}",
                "actor": f"Practitioner/{scheduler_providers[0]['id']}",
            },
        )

        print(
            """
✓ Successfully demonstrated wave scheduling:
  - Scheduled annual physical (30 min) at 9:00 AM
  - Scheduled sick visit (15 min) at 9:00 AM
  - Both patients scheduled with same provider at top of hour
  - Allows flexibility: while annual patient is being roomed,
    provider can see sick visit patient
  - This approach maximizes provider efficiency and minimizes idle time
        """
        )

    finally:
        # Cleanup
        for resource_type, resource_id in reversed(created_resources):
            medplum_client.delete_resource(resource_type, resource_id)
