"""Integration tests for Medplum admin features: secrets, sites, and client applications.

Tests the project admin API endpoints for managing:
- Project secrets (sensitive configuration)
- Project sites (domain configuration)
- Client applications (OAuth2 apps)
"""

import os

import pytest


@pytest.fixture
def project_id():
    """Get project ID from environment"""
    pid = os.getenv("MEDPLUM_PROJECT_ID")
    if not pid:
        pytest.skip("MEDPLUM_PROJECT_ID must be set for admin feature tests")
    return pid


# =============================================================================
# PROJECT SECRETS TESTS
# =============================================================================


def test_sync_manage_project_secrets(medplum_client, project_id, test_id):
    """Test managing project secrets with sync client."""
    # Get current project details
    project_details = medplum_client.get(f"admin/projects/{project_id}")
    original_secrets = project_details.get("project", {}).get("secret", [])

    # Create test secrets
    test_secrets = [
        {"name": f"TEST_API_KEY_{test_id}", "valueString": "test-api-key-value"},
        {
            "name": f"TEST_DATABASE_URL_{test_id}",
            "valueString": "postgresql://test",
        },
    ]

    # Combine with existing secrets (don't overwrite production secrets)
    all_secrets = original_secrets + test_secrets

    # Update secrets
    result = medplum_client.post(f"admin/projects/{project_id}/secrets", all_secrets)
    assert result is not None

    # Verify secrets were saved
    updated_project = medplum_client.get(f"admin/projects/{project_id}")
    saved_secrets = updated_project.get("project", {}).get("secret", [])

    # Check our test secrets are present
    secret_names = [s["name"] for s in saved_secrets]
    assert f"TEST_API_KEY_{test_id}" in secret_names
    assert f"TEST_DATABASE_URL_{test_id}" in secret_names

    # Cleanup - restore original secrets
    medplum_client.post(f"admin/projects/{project_id}/secrets", original_secrets)


@pytest.mark.asyncio
async def test_async_manage_project_secrets(async_medplum_client, project_id, test_id):
    """Test managing project secrets with async client."""
    # Get current project details
    project_details = await async_medplum_client.get(f"admin/projects/{project_id}")
    original_secrets = project_details.get("project", {}).get("secret", [])

    # Create test secret
    test_secrets = [
        {
            "name": f"ASYNC_TEST_SECRET_{test_id}",
            "valueString": "async-secret-value",
        },
    ]

    all_secrets = original_secrets + test_secrets

    # Update secrets
    result = await async_medplum_client.post(
        f"admin/projects/{project_id}/secrets", all_secrets
    )
    assert result is not None

    # Verify
    updated_project = await async_medplum_client.get(f"admin/projects/{project_id}")
    saved_secrets = updated_project.get("project", {}).get("secret", [])
    secret_names = [s["name"] for s in saved_secrets]
    assert f"ASYNC_TEST_SECRET_{test_id}" in secret_names

    # Cleanup
    await async_medplum_client.post(
        f"admin/projects/{project_id}/secrets", original_secrets
    )


# =============================================================================
# PROJECT SITES TESTS
# =============================================================================


def test_sync_manage_project_sites(medplum_client, project_id, test_id):
    """Test managing project sites with sync client."""
    # Get current project details
    project_details = medplum_client.get(f"admin/projects/{project_id}")
    original_sites = project_details.get("project", {}).get("site", [])

    # Create test site
    test_sites = [
        {
            "name": f"Test Site {test_id}",
            "domain": [f"test-{test_id}.example.com"],
        }
    ]

    all_sites = original_sites + test_sites

    # Update sites
    result = medplum_client.post(f"admin/projects/{project_id}/sites", all_sites)
    assert result is not None

    # Verify sites were saved
    updated_project = medplum_client.get(f"admin/projects/{project_id}")
    saved_sites = updated_project.get("project", {}).get("site", [])

    # Check our test site is present
    site_names = [s["name"] for s in saved_sites]
    assert f"Test Site {test_id}" in site_names

    # Cleanup - restore original sites
    medplum_client.post(f"admin/projects/{project_id}/sites", original_sites)


@pytest.mark.asyncio
async def test_async_manage_project_sites(async_medplum_client, project_id, test_id):
    """Test managing project sites with async client."""
    # Get current project details
    project_details = await async_medplum_client.get(f"admin/projects/{project_id}")
    original_sites = project_details.get("project", {}).get("site", [])

    # Create test site
    test_sites = [
        {
            "name": f"Async Test Site {test_id}",
            "domain": [f"async-test-{test_id}.example.com"],
        }
    ]

    all_sites = original_sites + test_sites

    # Update sites
    result = await async_medplum_client.post(
        f"admin/projects/{project_id}/sites", all_sites
    )
    assert result is not None

    # Verify
    updated_project = await async_medplum_client.get(f"admin/projects/{project_id}")
    saved_sites = updated_project.get("project", {}).get("site", [])
    site_names = [s["name"] for s in saved_sites]
    assert f"Async Test Site {test_id}" in site_names

    # Cleanup
    await async_medplum_client.post(
        f"admin/projects/{project_id}/sites", original_sites
    )


# =============================================================================
# CLIENT APPLICATIONS TESTS
# =============================================================================


def test_sync_create_client_application_via_fhir(medplum_client, test_id):
    """Test creating client application via standard FHIR resource creation."""
    # Create via standard FHIR resource
    client_app = medplum_client.create_resource(
        {
            "resourceType": "ClientApplication",
            "name": f"Test App {test_id}",
            "description": "Integration test client application",
            "redirectUri": f"https://test-{test_id}.example.com/callback",
        }
    )

    assert client_app["resourceType"] == "ClientApplication"
    assert client_app["name"] == f"Test App {test_id}"
    assert "id" in client_app

    # Verify we can read it back
    retrieved = medplum_client.read_resource("ClientApplication", client_app["id"])
    assert retrieved["id"] == client_app["id"]
    assert retrieved["name"] == f"Test App {test_id}"


@pytest.mark.asyncio
async def test_async_create_client_application_via_fhir(async_medplum_client, test_id):
    """Test creating client application via standard FHIR resource creation (async)."""
    client_app = await async_medplum_client.create_resource(
        {
            "resourceType": "ClientApplication",
            "name": f"Async Test App {test_id}",
            "description": "Async integration test client",
            "redirectUri": f"https://async-test-{test_id}.example.com/callback",
        }
    )

    assert client_app["resourceType"] == "ClientApplication"
    assert client_app["name"] == f"Async Test App {test_id}"
    assert "id" in client_app

    # Verify
    retrieved = await async_medplum_client.read_resource(
        "ClientApplication", client_app["id"]
    )
    assert retrieved["id"] == client_app["id"]


def test_sync_search_client_applications(medplum_client):
    """Test searching for client applications."""
    # Search for client applications
    results = medplum_client.search_resources("ClientApplication", {"_count": "5"})

    assert results["resourceType"] == "Bundle"
    assert "entry" in results or results.get("total", 0) == 0


@pytest.mark.asyncio
async def test_async_search_client_applications(async_medplum_client):
    """Test searching for client applications (async)."""
    results = await async_medplum_client.search_resources(
        "ClientApplication", {"_count": "5"}
    )

    assert results["resourceType"] == "Bundle"
    assert "entry" in results or results.get("total", 0) == 0
