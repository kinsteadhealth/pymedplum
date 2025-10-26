"""Integration tests for GraphQL functionality.

Tests the execute_graphql method on both sync and async clients.
"""

import pytest

from pymedplum.fhir.patient import Patient


def test_sync_graphql_simple_query(medplum_client):
    """Test sync client execute_graphql with a simple query."""
    # Create a test patient first
    patient = Patient(
        name=[{"family": "GraphQLTest", "given": ["Sync"]}],
        gender="male",
    )
    created = medplum_client.create_resource(patient)

    # Execute GraphQL query to fetch the patient
    query = """
    query GetPatient($id: ID!) {
        Patient(id: $id) {
            resourceType
            id
            name {
                family
                given
            }
        }
    }
    """

    result = medplum_client.execute_graphql(
        query=query, variables={"id": created["id"]}
    )

    # Verify response structure
    assert "data" in result
    assert "Patient" in result["data"]
    patient_data = result["data"]["Patient"]
    assert patient_data["id"] == created["id"]
    assert patient_data["resourceType"] == "Patient"
    assert patient_data["name"][0]["family"] == "GraphQLTest"


def test_sync_graphql_search_query(medplum_client):
    """Test sync client execute_graphql with a search query."""
    # Create multiple test patients
    for i in range(3):
        patient = Patient(
            name=[{"family": "GraphQLSearch", "given": [f"Patient{i}"]}],
            gender="male" if i % 2 == 0 else "female",
        )
        medplum_client.create_resource(patient)

    # Execute GraphQL search query
    query = """
    query SearchPatients {
        PatientList(family: "GraphQLSearch", _count: 10) {
            resourceType
            id
            name {
                family
                given
            }
            gender
        }
    }
    """

    result = medplum_client.execute_graphql(query=query)

    # Verify response
    assert "data" in result
    assert "PatientList" in result["data"]
    patients = result["data"]["PatientList"]
    assert len(patients) >= 3
    assert all(p["name"][0]["family"] == "GraphQLSearch" for p in patients)


def test_sync_graphql_with_fragments(medplum_client):
    """Test sync client execute_graphql with GraphQL fragments."""
    # Create a test patient
    patient = Patient(
        name=[{"family": "FragmentTest", "given": ["GraphQL"]}],
        gender="female",
    )
    created = medplum_client.create_resource(patient)

    # Execute GraphQL query with fragments
    query = """
    fragment PatientFields on Patient {
        id
        resourceType
        name {
            family
            given
        }
    }

    query GetPatientWithFragment($id: ID!) {
        Patient(id: $id) {
            ...PatientFields
            gender
        }
    }
    """

    result = medplum_client.execute_graphql(
        query=query, variables={"id": created["id"]}
    )

    # Verify response
    assert "data" in result
    patient_data = result["data"]["Patient"]
    assert patient_data["id"] == created["id"]
    assert patient_data["gender"] == "female"


@pytest.mark.asyncio
async def test_async_graphql_simple_query(async_medplum_client):
    """Test async client execute_graphql with a simple query."""
    # Create a test patient first
    patient = Patient(
        name=[{"family": "AsyncGraphQLTest", "given": ["Async"]}],
        gender="male",
    )
    created = await async_medplum_client.create_resource(patient)

    # Execute GraphQL query to fetch the patient
    query = """
    query GetPatient($id: ID!) {
        Patient(id: $id) {
            resourceType
            id
            name {
                family
                given
            }
        }
    }
    """

    result = await async_medplum_client.execute_graphql(
        query=query, variables={"id": created["id"]}
    )

    # Verify response structure
    assert "data" in result
    assert "Patient" in result["data"]
    patient_data = result["data"]["Patient"]
    assert patient_data["id"] == created["id"]
    assert patient_data["resourceType"] == "Patient"
    assert patient_data["name"][0]["family"] == "AsyncGraphQLTest"


@pytest.mark.asyncio
async def test_async_graphql_search_query(async_medplum_client):
    """Test async client execute_graphql with a search query."""
    # Create multiple test patients
    for i in range(3):
        patient = Patient(
            name=[{"family": "AsyncGraphQLSearch", "given": [f"Patient{i}"]}],
            gender="male" if i % 2 == 0 else "female",
        )
        await async_medplum_client.create_resource(patient)

    # Execute GraphQL search query
    query = """
    query SearchPatients {
        PatientList(family: "AsyncGraphQLSearch", _count: 10) {
            resourceType
            id
            name {
                family
                given
            }
            gender
        }
    }
    """

    result = await async_medplum_client.execute_graphql(query=query)

    # Verify response
    assert "data" in result
    assert "PatientList" in result["data"]
    patients = result["data"]["PatientList"]
    assert len(patients) >= 3
    assert all(p["name"][0]["family"] == "AsyncGraphQLSearch" for p in patients)


@pytest.mark.asyncio
async def test_sync_async_graphql_parity(medplum_client, async_medplum_client):
    """Verify sync and async GraphQL execution produce identical results."""
    # Create a test patient
    patient = Patient(
        name=[{"family": "GraphQLParity", "given": ["Test"]}],
        gender="male",
    )
    created = medplum_client.create_resource(patient)

    # Same query for both
    query = """
    query GetPatient($id: ID!) {
        Patient(id: $id) {
            id
            resourceType
            name {
                family
            }
        }
    }
    """
    variables = {"id": created["id"]}

    # Execute both
    sync_result = medplum_client.execute_graphql(query, variables)
    async_result = await async_medplum_client.execute_graphql(query, variables)

    # Compare results
    assert sync_result == async_result
    assert sync_result["data"]["Patient"]["id"] == created["id"]
