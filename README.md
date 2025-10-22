# PyMedplum: The Unofficial Python SDK for Medplum

PyMedplum is a Python client for the Medplum open-source, headless EHR. It provides a convenient and easy-to-use interface for interacting with a Medplum server, allowing developers to build healthcare applications in Python.

This library is inspired by the official Medplum TypeScript SDK and aims to provide a similar developer experience for Python developers.

## Features

- **Authentication**: Authenticate with a Medplum server using client credentials.
- **CRUD Operations**: Create, read, update, and delete FHIR resources.
- **Search**: Search for FHIR resources using a simple and intuitive query syntax.
- **Batch Operations**: Execute batch and transaction bundles.
- **GraphQL**: Execute GraphQL queries against the Medplum server.
- **Bot Execution**: Trigger and execute Medplum Bots with custom input data.
- **On-Behalf-Of Operations**: Perform operations on behalf of another user or a `ProjectMembership`.
- **Asynchronous Support**: `AsyncMedplumClient` provides an asynchronous interface for use with `asyncio`.
- **FHIR Resource Models**: Leverages the `fhir.resources` package, which uses `pydantic` for FHIR resource modeling and validation.

## Installation

### Installing from PyPI

```bash
pip install pymedplum
```

### Installing from AWS CodeArtifact (Internal)

For Kinstead Health team members, you can install from our private CodeArtifact repository:

#### Manual Installation

```bash
# Configure AWS credentials
aws configure

# Login to CodeArtifact
aws codeartifact login --tool pip --domain pymedplum --repository pymedplum --region us-east-1

# Install the package
pip install pymedplum
```

#### In GitHub Actions (Healthcare Repository)

The healthcare repository's GitHub Actions workflows automatically have read access to CodeArtifact. Use this in your workflow:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GitHubActionsRole
    aws-region: us-east-1

- name: Install from CodeArtifact
  run: |
    aws codeartifact login --tool pip --domain pymedplum --repository pymedplum --region us-east-1
    pip install pymedplum
```

The CodeArtifact repository also proxies public PyPI packages, so all dependencies will be automatically resolved.

## Getting Started

### Authentication

First, you need to authenticate with the Medplum server to obtain an access token. You can do this using your client credentials:

```python
from pymedplum import MedplumClient

client = MedplumClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)
client.authenticate()
```

### Creating a Resource

To create a new FHIR resource, you can use the `create_resource` method:

```python
patient = client.create_resource(
    {
        "resourceType": "Patient",
        "name": [{"given": ["John"], "family": "Doe"}],
    }
)

print(patient)
```

### Reading a Resource

You can read a FHIR resource by its `resourceType` and `id`:

```python
patient = client.read_resource("Patient", "your-patient-id")

print(patient)
```

### Updating a Resource

To update an existing resource, use the `update_resource` method:

```python
patient["active"] = True
updated_patient = client.update_resource(patient)

print(updated_patient)
```

### Deleting a Resource

You can delete a resource using the `delete_resource` method:

```python
client.delete_resource("Patient", "your-patient-id")
```

### Searching for Resources

`pymedplum` provides a flexible way to search for resources. You can search for all resources of a certain type:

```python
patients = client.search_resources("Patient")
for patient in patients:
    print(patient)
```

You can also provide a query to filter the results:

```python
patients = client.search_resources("Patient", query={"name": "John Doe"})
```

For more complex queries, you can use a list of tuples:

```python
patients = client.search_resources(
    "Patient", query=[("name", "John"), ("_sort", "-birthDate")]
)
```

### Using `fhir.resources` for Type Hinting and Validation

You can use the `fhir.resources` package to provide type hinting and validation for your FHIR resources. This can help you catch errors early and ensure that your data is compliant with the FHIR specification.

Because the client expects a dictionary, you must use the `to_fhir_json` helper function to convert the pydantic model to a dictionary before sending it to the client.

Here's an example of how to use the `Patient` model from `fhir.resources` when creating a patient:

```python
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.humanname import HumanName
from pymedplum.helpers.fhir import to_fhir_json

patient_model = Patient(
    name=[HumanName(given=["Mary"], family="Johnson", use="official")],
    birthDate="1960-03-25",
)

created_patient = client.create_resource(to_fhir_json(patient_model))

print(created_patient)
```

### Executing Bots

Medplum allows you to create and execute custom automation logic using Bots. You can trigger a Bot using the `execute_bot` method:

```python
# Execute a bot with input data
result = client.execute_bot(
    bot_id="your-bot-id",
    input_data={
        "resourceType": "Patient",
        "id": "patient-123"
    }
)

print(result)
```

The bot execution feature uses Medplum's custom FHIR operation `Bot/{id}/$execute`, which allows you to run serverless functions that can process data, call external APIs, or perform complex business logic.

### Managing Project Secrets

Medplum provides secure storage for sensitive information like API keys and access credentials through project secrets:

```python
# Set project secrets
secrets = [
    {"name": "API_KEY", "valueString": "your-api-key-here"},
    {"name": "DATABASE_URL", "valueString": "postgresql://..."},
]

result = client.post(f"admin/projects/{project_id}/secrets", secrets)

# Retrieve project details (including secrets)
project = client.get(f"admin/projects/{project_id}")
current_secrets = project.get("project", {}).get("secret", [])
```

Secrets are stored as `ProjectSetting` objects with `name` and `valueString` fields, making them accessible to your Bots and other server-side code while keeping them secure.

### Managing Project Sites

Configure your Medplum project to run on separate domains using project sites:

```python
# Configure project sites
sites = [
    {
        "name": "Production Site",
        "domain": ["app.example.com"],
        "requireTwoFactorAuth": True
    },
    {
        "name": "Staging Site",
        "domain": ["staging.example.com"],
        "requireTwoFactorAuth": False
    }
]

result = client.post(f"admin/projects/{project_id}/sites", sites)
```

Sites are stored as `ProjectSite` objects allowing you to configure domain-specific settings for your project.

### Managing Client Applications

Client applications enable OAuth2 authentication flows for your applications:

```python
# Client applications are standard FHIR ClientApplication resources
# List all client applications
clients_bundle = client.search_resources("ClientApplication")

# Create a new client application
new_client = client.create_resource({
    "resourceType": "ClientApplication",
    "name": "My Healthcare App",
    "description": "Patient portal application",
    "redirectUri": "https://myapp.example.com/callback"
})

# Clients can also be created via the admin API
client_app = client.post(f"admin/projects/{project_id}/client", {
    "name": "My App",
    "description": "Application description",
    "redirectUri": "https://myapp.example.com/callback"
})
```

### Asynchronous Client

For asynchronous applications, `pymedplum` provides an `AsyncMedplumClient`:

```python
import asyncio
from pymedplum import AsyncMedplumClient

async def main():
    async with AsyncMedplumClient(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
    ) as client:
        await client.authenticate()

        patient = await client.create_resource(
            {
                "resourceType": "Patient",
                "name": [{"given": ["Jane"], "family": "Doe"}],
            }
        )
        print(patient)

if __name__ == "__main__":
    asyncio.run(main())
```
