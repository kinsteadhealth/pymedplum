"""Shared pytest fixtures and helpers for pymedplum tests."""

import os
import secrets
import uuid

import pytest
from dotenv import load_dotenv

# Import from pymedplum.fhir first to trigger model rebuilding
import pymedplum.fhir  # noqa: F401
from pymedplum import MedplumClient
from pymedplum.fhir import (
    HumanName,
    Identifier,
    Organization,
    Patient,
    Practitioner,
)

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def medplum_credentials():
    """Get Medplum credentials from environment."""
    client_id = os.getenv("MEDPLUM_CLIENT_ID")
    client_secret = os.getenv("MEDPLUM_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip(
            "MEDPLUM_CLIENT_ID and MEDPLUM_CLIENT_SECRET must be set in .env file"
        )

    return {"client_id": client_id, "client_secret": client_secret}


@pytest.fixture
def medplum_client(medplum_credentials):
    """Create an authenticated Medplum client."""
    project_id = os.getenv("MEDPLUM_PROJECT_ID")

    client = MedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
        project_id=project_id,
    )
    client.authenticate()

    yield client

    client.close()


@pytest.fixture
async def async_medplum_client(medplum_credentials):
    """Create an authenticated async Medplum client."""
    from pymedplum import AsyncMedplumClient

    project_id = os.getenv("MEDPLUM_PROJECT_ID")

    client = AsyncMedplumClient(
        client_id=medplum_credentials["client_id"],
        client_secret=medplum_credentials["client_secret"],
        project_id=project_id,
    )
    await client.authenticate()

    yield client

    await client.close()


@pytest.fixture
def medplum_membership(
    medplum_client,
    create_test_org,
    create_test_access_policy,
    create_test_membership,
    test_id,
):
    """Create a test membership for on_behalf_of testing."""
    project_id = os.getenv("MEDPLUM_PROJECT_ID")

    if not project_id:
        pytest.skip("MEDPLUM_PROJECT_ID must be set for this test")

    # Create test resources
    create_test_org("Coverage", test_id)
    policy = create_test_access_policy("Test Policy", test_id)

    # Create membership (creates User + Practitioner + ProjectMembership)
    membership = create_test_membership(
        project_id, "Test", "User", policy["id"], test_id
    )

    if not membership:
        pytest.skip("Could not create test membership")

    return membership["id"]


@pytest.fixture
def create_scoped_client(medplum_credentials):
    """Factory fixture to create authenticated clients with default_on_behalf_of."""

    def _create(membership_id: str):
        """Create a client scoped to a specific membership."""
        project_id = os.getenv("MEDPLUM_PROJECT_ID")

        client = MedplumClient(
            client_id=medplum_credentials["client_id"],
            client_secret=medplum_credentials["client_secret"],
            project_id=project_id,
            default_on_behalf_of=f"ProjectMembership/{membership_id}",
        )
        client.authenticate()
        return client

    return _create


@pytest.fixture
def test_id():
    """Generate a unique test ID for resource naming."""
    return str(uuid.uuid4())[:8]


# =============================================================================
# Factory Fixtures - Return callable functions for creating test resources
# =============================================================================


@pytest.fixture
def create_test_org(medplum_client):
    """Factory fixture that returns a function to create test organizations."""

    def _create(name_suffix, test_id):
        """Helper to create an organization using pymedplum.fhir models."""
        org = Organization(
            name=f"Test Org {name_suffix} - {test_id}",
            identifier=[
                Identifier(
                    system="http://example.org/test-orgs",
                    value=f"test-org-{name_suffix.lower()}-{test_id}",
                )
            ],
        )
        # Convert to dict for API
        org_data = org.model_dump(by_alias=True, exclude_none=True)
        return medplum_client.create_resource(org_data)

    return _create


@pytest.fixture
def create_test_practitioner(medplum_client):
    """Factory fixture that returns a function to create test practitioners."""

    def _create(name, test_id):
        """Helper to create a practitioner using pymedplum.fhir models."""
        given, family = name.split()[0], name.split()[-1]
        practitioner = Practitioner(
            name=[HumanName(given=[given], family=family)],
            identifier=[
                Identifier(
                    system="http://example.org/test-practitioners",
                    value=f"{name.lower().replace(' ', '-')}-{test_id}",
                )
            ],
        )
        # Convert to dict for API
        prac_data = practitioner.model_dump(by_alias=True, exclude_none=True)
        return medplum_client.create_resource(prac_data)

    return _create


@pytest.fixture
def create_test_patient(medplum_client):
    """Factory fixture that returns a function to create test patients."""

    def _create(given_name, family_suffix, org_id, test_id):
        """Helper to create a patient using pymedplum.fhir models."""
        patient = Patient(
            name=[HumanName(given=[given_name], family=f"{family_suffix}-{test_id}")],
            gender="female" if given_name == "Alice" else "male",
        )
        patient_data = patient.model_dump(by_alias=True, exclude_none=True)
        return medplum_client.create_resource(
            patient_data, accounts=f"Organization/{org_id}"
        )

    return _create


@pytest.fixture
def create_test_access_policy(medplum_client):
    """Factory fixture that returns a function to create test access policies."""

    def _create(name, test_id):
        """Helper to create a basic access policy for testing.

        Note: Uses a simple policy allowing all resources.
        In production, use compartment-based access or _account search parameter.
        """
        return medplum_client.create_resource(
            {
                "resourceType": "AccessPolicy",
                "name": f"{name} - {test_id}",
                "resource": [
                    {"resourceType": "Patient"},
                    {"resourceType": "Organization"},
                    {"resourceType": "Practitioner"},
                    {"resourceType": "AccessPolicy"},
                ],
            }
        )

    return _create


@pytest.fixture
def create_test_membership(medplum_client):
    """Factory fixture that returns a function to create test memberships."""

    def _create(project_id, first_name, last_name, policy_id, test_id):
        """Helper to create ProjectMembership using invite API with secure credentials.

        Creates User, profile, and ProjectMembership silently (no email).
        Uses cryptographically secure random password for security.
        """
        # Generate unique, secure credentials
        email = f"{first_name.lower()}.{last_name.lower()}.{test_id}@test.example.com"
        password = secrets.token_urlsafe(
            32
        )  # 32-char cryptographically secure password

        try:
            return medplum_client.invite_user(
                project_id=project_id,
                resource_type="Practitioner",
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                send_email=False,  # Silent creation
                access_policy=f"AccessPolicy/{policy_id}",
            )
        except Exception as e:
            print(f"Note: ProjectMembership creation failed: {e}")
            return None

    return _create


# Note: to_fhir_json helper is now imported from pymedplum.helpers above
