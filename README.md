# PyMedplum: The Unofficial Python SDK for Medplum

PyMedplum is a Python client for the Medplum open-source, headless EHR. It provides a convenient and easy-to-use interface for interacting with a Medplum server, allowing developers to build healthcare applications in Python.

This library is inspired by the official Medplum TypeScript SDK and aims to provide a similar developer experience for Python developers.

## Features

- **Authentication**: Client credentials with automatic token refresh
- **Auto-Authentication**: On-behalf-of operations automatically authenticate when needed
- **Type Safety**: 209 generated Pydantic models from Medplum's TypeScript definitions
- **CRUD Operations**: Create, read, update, delete with optional type-safe responses
- **Advanced Search**: `_include`, `_revinclude`, chaining, modifiers, pagination
- **FHIR Operations**: 
  - C-CDA document export
  - Terminology validation (ValueSet and CodeSystem)
  - Transaction bundles (atomic operations)
  - Batch bundles (independent operations)
  - Binary file upload/download
  - DocumentReference creation
- **Lazy Loading**: FHIR models are loaded on-demand for fast startup times (~50ms for first import vs. 3-5s for all).
- **Thread-Safe**: Lazy loading is fully thread-safe and tested against experimental "no-GIL" builds of Python.
- **GraphQL**: Execute GraphQL queries
- **Bot Execution**: Trigger Medplum Bots with custom input
- **On-Behalf-Of**: Perform operations as another user/ProjectMembership
- **Async Support**: `AsyncMedplumClient` for `asyncio` applications
- **Error Handling**: Specific exceptions (401, 403, 404, 429, 500, etc.)
- **FHIR Helpers**: Parse references, extract identifiers, get display names
- **Medplum Extensions**: Full support for Bot, Project, AccessPolicy, etc.

## Installation

### From AWS CodeArtifact (Internal)

For Kinstead Health team members:

```bash
# Configure AWS credentials
aws configure

# Login to CodeArtifact
aws codeartifact login --tool pip --domain pymedplum --repository pymedplum --region us-east-1

# Install the package
pip install pymedplum
```

#### In GitHub Actions

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

## Quick Start

```python
from pymedplum import MedplumClient

# Create client - authentication happens automatically!
client = MedplumClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

# Create a patient
patient = client.create_resource({
    "resourceType": "Patient",
    "name": [{"given": ["John"], "family": "Doe"}],
    "gender": "male",
    "birthDate": "1990-01-01"
})

# Read a resource
patient = client.read_resource("Patient", "patient-123")

# Search for resources
patients = client.search_resources("Patient", {"family": "Doe"})

# Update a resource
patient["active"] = True
updated = client.update_resource(patient)
```

## Showcase: What You Can Do

### Type-Safe FHIR Models

```python
from pymedplum.fhir import Patient, HumanName

# Create with full type safety and IDE autocomplete
patient = Patient(
    name=[HumanName(given=["Alice"], family="Smith")],
    gender="female"
)

# Read with type safety
typed_patient = client.read_resource("Patient", "123", as_fhir=Patient)
print(typed_patient.name[0].family)  # IDE autocomplete works!
```

### Advanced Search Features

```python
# Include related resources (like SQL joins)
bundle = client.search_resources("Patient", {
    "family": "Smith",
    "_include": "Patient:organization",        # Include the org
    "_revinclude": "Observation:patient",      # Include all observations
    "_count": "50"
})

# Chain through relationships
observations = client.search_resources("Observation", {
    "patient.family": "Smith",  # Find obs for patients named Smith
    "date": "ge2024-01-01"      # After January 1, 2024
})

# Iterate through all pages automatically
for patient in client.search_resource_pages("Patient", {"family": "Smith"}):
    print(patient["name"])

# Type-safe iteration with Pydantic models
from pymedplum.fhir import Patient
for patient in client.search_resource_pages("Patient", {"family": "Smith"}, as_fhir=Patient):
    print(patient.name[0].family)  # Full IDE autocomplete!
```

### Binary Files & Documents

```python
# Upload a PDF
with open("lab_report.pdf", "rb") as f:
    binary = client.upload_binary(f.read(), "application/pdf")

# Download binary
pdf_bytes = client.download_binary(binary["id"])

# Create DocumentReference linking binary to patient
doc_ref = client.create_document_reference(
    patient_id="patient-123",
    binary_id=binary["id"],
    content_type="application/pdf",
    title="Lab Results",
    description="CBC performed on 2024-01-15"
)
```

### C-CDA Document Export

```python
# Export patient data in C-CDA format for interoperability
ccda_xml = client.export_ccda(patient_id="patient-123")

# Save to file
with open("patient_summary.xml", "w") as f:
    f.write(ccda_xml)
```

### Terminology Validation

```python
# Validate codes against ValueSets
is_valid = client.validate_valueset_code(
    url="http://hl7.org/fhir/ValueSet/observation-status",
    coding={
        "system": "http://hl7.org/fhir/observation-status",
        "code": "final"
    }
)

# Validate against CodeSystems
is_valid = client.validate_codesystem_code(
    url="http://loinc.org",
    code="15074-8"  # Glucose
)
```

### Transaction & Batch Bundles

```python
# Atomic transaction - all succeed or all fail
bundle = {
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [
        {
            "request": {"method": "POST", "url": "Patient"},
            "resource": {"resourceType": "Patient", "name": [...]},
            "fullUrl": "urn:uuid:patient-temp-id"
        },
        {
            "request": {"method": "POST", "url": "Observation"},
            "resource": {
                "resourceType": "Observation",
                "subject": {"reference": "urn:uuid:patient-temp-id"}  # Refs resolved!
            }
        }
    ]
}

result = client.execute_transaction(bundle)

# Batch - operations processed independently
result = client.execute_batch(batch_bundle)
```

### GraphQL Queries

```python
query = """
query GetPatientWithObs($id: ID!) {
    Patient(id: $id) {
        name { family given }
        ObservationList(_reference: patient) {
            code { text }
            valueQuantity { value unit }
        }
    }
}
"""

result = client.execute_graphql(query, {"id": "patient-123"})
print(result["data"]["Patient"])
```

### On-Behalf-Of Operations

```python
# Temporarily act on behalf of a patient's membership
with client.on_behalf_of("ProjectMembership/membership-123") as patient_client:
    # This operation has the patient's permissions
    response = patient_client.create_resource({
        "resourceType": "QuestionnaireResponse",
        "status": "completed",
        # ...
    })

# Back to original user context
practitioner_note = client.create_resource({"resourceType": "Observation", ...})
```

### Bot Execution

```python
# Execute serverless functions on Medplum
result = client.execute_bot(
    bot_id="send-welcome-email",
    input_data={"resourceType": "Patient", "id": "patient-123"}
)
```

### Async/Await Support

```python
from pymedplum import AsyncMedplumClient

async def create_patient():
    async with AsyncMedplumClient(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
    ) as client:
        patient = await client.create_resource({
            "resourceType": "Patient",
            "name": [{"given": ["Jane"], "family": "Doe"}]
        })
        return patient
```

### FHIRBundle Wrapper

```python
# Get wrapper with helper methods
bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True)

# Iterate directly over resources
for patient in bundle:
    print(patient['name'])

# Get typed resources with as_fhir parameter
from pymedplum.fhir import Patient
bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True, as_fhir=Patient)
patients = bundle.get_resources_typed(Patient)

# Or use get_resources_typed on any bundle
bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True)
patients = bundle.get_resources_typed(Patient)

# Check if empty, get total, access pagination
if not bundle.is_empty():
    print(f"Found {bundle.get_total()} results")
    next_page = bundle.get_next_link()
```

### Enhanced Error Handling

```python
from pymedplum import (
    ResourceNotFoundError,
    AuthorizationError,
    ValidationError,
    RateLimitError
)

try:
    patient = client.read_resource("Patient", "123")
except ResourceNotFoundError:
    print("Patient not found")
except AuthorizationError:
    print("Access denied")
except ValidationError as e:
    print(f"Invalid data: {e.response_data}")
except RateLimitError:
    print("Rate limited - slow down!")
```

### FHIR Helpers

```python
from pymedplum import (
    parse_reference,
    build_reference,
    get_patient_display_name,
    extract_identifier,
    get_code_display
)

# Parse references
resource_type, resource_id = parse_reference("Patient/123")

# Build references
ref = build_reference("Patient", "123")

# Get patient name
patient = client.read_resource("Patient", "123")
name = get_patient_display_name(patient)  # "John Doe"

# Extract identifiers
mrn = extract_identifier(patient, "http://hospital.org/mrn")

# Get code display
concept = {"coding": [{"display": "Hypertension"}]}
display = get_code_display(concept)
```

## Documentation

For complete documentation, see:

- **[Installation Guide](docs/installation.md)** - Detailed setup instructions
- **[Quickstart](docs/quickstart.md)** - Get up and running quickly
- **[Advanced Usage](docs/advanced_usage.md)** - Advanced search, FHIR operations, bundles, binaries
- **[API Reference](docs/api_reference.md)** - Complete API documentation
- **[FHIR Models](docs/fhir_models.md)** - Type-safe FHIR model usage
- **[FAQ](docs/faq.md)** - Frequently asked questions

## Contributing

Contributions are welcome! Please see our development guidelines:

```bash
# Install development dependencies
make install-dev

# Run all quality checks
make check

# Run tests
make test
make test-unit
make test-integration
```

See [AGENTS.md](AGENTS.md) for detailed contributor guidelines.

## License

Copyright 2025 Kinstead Health

## Acknowledgments

This library is inspired by the official [Medplum TypeScript SDK](https://github.com/medplum/medplum) and aims to provide a similar developer experience for Python developers.
