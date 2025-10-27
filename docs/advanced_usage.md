# Advanced Usage

This section covers more advanced features of the `pymedplum` library, including detailed CRUD operations, GraphQL, and administrative functions.

## Advanced FHIR Search

FHIR provides powerful search capabilities beyond basic parameter matching. This section covers advanced search features including joins, reverse includes, chaining, and search modifiers.

### Basic Search Parameters

All search methods accept a `query` parameter that can be a dictionary of search parameters:

```python
# Search by single parameter
patients = client.search_resources("Patient", {"family": "Smith"})

# Search by multiple parameters (AND logic)
patients = client.search_resources("Patient", {
    "family": "Smith",
    "given": "John",
    "birthdate": "1980-01-01"
})

### Multi-Valued Query Parameters

Some FHIR search parameters accept multiple values for the same parameter name. The most common use case is date range searches, where you need to specify both a lower and upper bound.

PyMedplum automatically handles list values in query dictionaries by creating multiple parameters with the same key:

```python
# Date range search - patients born between 1990 and 2000
patients = client.search_resources("Patient", {
    "family": "Smith",
    "birthdate": ["ge1990-01-01", "le2000-12-31"]
})

# This generates the query string:
# birthdate=ge1990-01-01&birthdate=le2000-12-31

# You can also use this for other multi-valued parameters
observations = client.search_resources("Observation", {
    "code": ["http://loinc.org|8867-4", "http://loinc.org|2339-0"],  # Multiple LOINC codes
    "date": ["ge2024-01-01", "le2024-12-31"]
})
```

The library converts list values into separate parameter tuples automatically, ensuring proper URL encoding for FHIR servers.

### Including Related Resources (`_include`)

The `_include` parameter lets you fetch related resources in a single request, reducing round trips to the server. This is FHIR's equivalent of SQL joins.

```python
# Get patients AND their managing organizations
bundle = client.search_resources("Patient", {
    "family": "Smith",
    "_include": "Patient:organization"
})

# The bundle contains both Patient resources and the referenced Organization resources
for entry in bundle.get("entry", []):
    resource = entry["resource"]
    if resource["resourceType"] == "Patient":
        print(f"Patient: {resource['name'][0]['family']}")
    elif resource["resourceType"] == "Organization":
        print(f"  Organization: {resource['name']}")
```

You can include multiple related resources:

```python
# Get encounters with their patient AND location
bundle = client.search_resources("Encounter", {
    "status": "finished",
    "_include": ["Encounter:patient", "Encounter:location"]
})
```

### Reverse Includes (`_revinclude`)

The `_revinclude` parameter fetches resources that reference the search results. This is like a reverse foreign key lookup.

```python
# Get patients AND all their observations
bundle = client.search_resources("Patient", {
    "family": "Smith",
    "_revinclude": "Observation:patient"
})

# Bundle contains Patient resources AND Observation resources that reference them
patients = []
observations = []

for entry in bundle.get("entry", []):
    resource = entry["resource"]
    if resource["resourceType"] == "Patient":
        patients.append(resource)
    elif resource["resourceType"] == "Observation":
        observations.append(resource)

print(f"Found {len(patients)} patients with {len(observations)} observations")
```

Common `_revinclude` patterns:

```python
# Get practitioner and all their appointments
bundle = client.search_resources("Practitioner", {
    "identifier": "ABC123",
    "_revinclude": "Appointment:actor"
})

# Get patient with all clinical resources
bundle = client.search_resources("Patient", {
    "identifier": "MRN|12345",
    "_revinclude": [
        "Observation:patient",
        "Condition:patient",
        "MedicationStatement:patient",
        "Procedure:patient"
    ]
})
```

### Search Parameter Chaining

Chain search parameters to filter by properties of related resources without retrieving them:

```python
# Find observations for patients with a specific family name
observations = client.search_resources("Observation", {
    "patient.family": "Smith"  # Chain through patient reference
})

# Find appointments for a specific practitioner by their identifier
appointments = client.search_resources("Appointment", {
    "actor.identifier": "NPI|1234567890"
})

# Multiple levels of chaining
observations = client.search_resources("Observation", {
    "patient.organization.name": "General Hospital"
})
```

### Search Modifiers

FHIR supports modifiers that change how search parameters are matched:

```python
# Exact match (case-sensitive)
patients = client.search_resources("Patient", {
    "family:exact": "Smith"
})

# Contains (substring match)
patients = client.search_resources("Patient", {
    "family:contains": "mit"  # Matches "Smith", "Smithson", etc.
})

# Text search across multiple fields
patients = client.search_resources("Patient", {
    "name:text": "John Smith"  # Searches across all name components
})

# Missing parameter (find resources where field is absent)
patients = client.search_resources("Patient", {
    "email:missing": "true"  # Patients without email
})
```

### Date Range Searches

Use prefixes for date comparisons:

```python
from datetime import datetime, timedelta

today = datetime.now().date()
week_ago = today - timedelta(days=7)

# Observations from the last week
recent_obs = client.search_resources("Observation", {
    "date": f"ge{week_ago.isoformat()}"  # greater than or equal
})

# Appointments in a specific range
appointments = client.search_resources("Appointment", {
    "date": [
        f"ge{today.isoformat()}",      # Start of range
        f"le{(today + timedelta(days=7)).isoformat()}"  # End of range
    ]
})

# Common prefixes: eq (equal), ne (not equal), gt (greater than),
#                  lt (less than), ge (>=), le (<=)
```

### Combining Advanced Features

You can combine multiple advanced search features in a single query:

```python
# Complex query: Get patients named "Smith" born after 1990,
# include their organization, and all their recent observations
bundle = client.search_resources("Patient", {
    "family": "Smith",
    "birthdate": "gt1990-01-01",
    "_include": "Patient:organization",
    "_revinclude": "Observation:patient",
    "_count": "50"  # Limit results per page
})

# Process the different resource types
patients = []
organizations = []
observations = []

for entry in bundle.get("entry", []):
    resource = entry["resource"]
    resource_type = resource["resourceType"]
    
    if resource_type == "Patient":
        patients.append(resource)
    elif resource_type == "Organization":
        organizations.append(resource)
    elif resource_type == "Observation":
        observations.append(resource)
```

### Search Result Controls

Control pagination and sorting:

```python
# Limit results per page
results = client.search_resources("Patient", {
    "family": "Smith",
    "_count": "10"  # Return max 10 results per page
})

# Sort results
results = client.search_resources("Observation", {
    "patient": "Patient/123",
    "_sort": "-date"  # Sort by date, newest first (- for descending)
})

# Multiple sort parameters
results = client.search_resources("Patient", {
    "_sort": ["family", "given"]  # Sort by family name, then given name
})
```

### Pagination with Advanced Searches

Use `search_resource_pages()` to automatically handle pagination with complex queries:

```python
# Iterate through all matching resources across pages
all_observations = []

for observation in client.search_resource_pages("Observation", {
    "patient.family": "Smith",
    "date": f"ge{week_ago.isoformat()}",
    "_sort": "-date",
    "_count": "100"  # Fetch 100 per page
}):
    all_observations.append(observation)
    # Each observation is a dict, process as needed

print(f"Found {len(all_observations)} total observations")
```

## Advanced CRUD Operations

### Updating a Resource
To update an entire resource, use the `update_resource` method. This will overwrite the existing resource with the new data provided.

```python
# Assuming 'patient' is a Patient model instance from a client.read() call
patient.gender = "female"

# The entire resource must be provided
updated_patient = client.update_resource(patient)

print(f"Updated patient gender: {updated_patient.gender}")
```

### Patching a Resource
For partial updates, you can use the `patch_resource` method with a list of JSON Patch operations.

```python
patient_id = "some-patient-id"
patch_operations = [
    {"op": "replace", "path": "/gender", "value": "other"},
    {"op": "add", "path": "/telecom/-", "value": {"system": "email", "value": "new@example.com"}}
]

patched_patient = client.patch_resource(f"Patient/{patient_id}", patch_operations)
```

### Deleting a Resource
To delete a resource, use the `delete_resource` method.

```python
client.delete_resource("Patient/some-patient-id")
```
## FHIR Operations and Special Workflows

PyMedplum provides dedicated methods for specialized FHIR operations beyond standard CRUD, including clinical document export, terminology validation, atomic transactions, and binary file handling.

### C-CDA Document Export

Export patient data in C-CDA (Consolidated Clinical Document Architecture) format for interoperability with other healthcare systems:

```python
# Export a patient's data as a C-CDA document
ccda_xml = client.export_ccda(patient_id="patient-123")

# Save to file
with open("patient_summary.xml", "w") as f:
    f.write(ccda_xml)

# Asynchronous
async def export_patient_ccda():
    ccda = await async_client.export_ccda(patient_id="patient-456")
    return ccda
```

**Note:** The patient must have sufficient clinical data (encounters, observations, conditions, etc.) for successful C-CDA generation.

### Terminology Validation

Validate clinical codes against FHIR ValueSets and CodeSystems to ensure data quality and standards compliance.

#### ValueSet Validation

Validate that a code exists in a specific ValueSet:

```python
# Validate using ValueSet URL and Coding
is_valid = client.validate_valueset_code(
    url="http://hl7.org/fhir/ValueSet/observation-status",
    coding={
        "system": "http://hl7.org/fhir/observation-status",
        "code": "final"
    }
)
print(f"Code is valid: {is_valid}")  # True

# Validate using ValueSet ID and explicit system/code
is_valid = client.validate_valueset_code(
    valueset_id="observation-status",
    system="http://hl7.org/fhir/observation-status",
    code="preliminary"
)

# Validate using CodeableConcept (useful when validating existing resources)
codeable_concept = {
    "coding": [{
        "system": "http://loinc.org",
        "code": "15074-8",
        "display": "Glucose"
    }]
}
is_valid = client.validate_valueset_code(
    url="http://hl7.org/fhir/ValueSet/observation-codes",
    codeable_concept=codeable_concept
)
```

#### CodeSystem Validation

Validate codes directly against a CodeSystem (without a ValueSet):

```python
# Validate using CodeSystem URL
is_valid = client.validate_codesystem_code(
    url="http://loinc.org",
    code="15074-8"
)

# Validate with specific version
is_valid = client.validate_codesystem_code(
    url="http://snomed.info/sct",
    code="38341003",  # Hypertension
    version="http://snomed.info/sct/731000124108/version/20210901"
)

# Asynchronous
async def validate_code():
    result = await async_client.validate_codesystem_code(
        url="http://loinc.org",
        code="15074-8"
    )
    return result
```

### Transaction and Batch Bundles

FHIR Bundles allow multiple operations in a single request. Use **transactions** for atomic operations (all-or-nothing) or **batches** for independent operations.

#### Transaction Bundles (Atomic)

All operations succeed or all fail together. Ideal for creating related resources that must exist together:

```python
# Create a patient and observation atomically
bundle = {
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [
        {
            "request": {"method": "POST", "url": "Patient"},
            "resource": {
                "resourceType": "Patient",
                "name": [{"family": "Smith", "given": ["John"]}]
            },
            "fullUrl": "urn:uuid:patient-temp-id"  # Temporary reference
        },
        {
            "request": {"method": "POST", "url": "Observation"},
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {"text": "Blood Pressure"},
                "subject": {"reference": "urn:uuid:patient-temp-id"}  # Reference temp ID
            }
        }
    ]
}

# Execute - if either fails, both are rolled back
result = client.execute_transaction(bundle)

# The bundle can also be auto-converted from type "batch" to "transaction"
batch_bundle = {
    "resourceType": "Bundle",
    "type": "batch",  # Will be changed to "transaction"
    "entry": [...]
}
result = client.execute_transaction(batch_bundle)  # Type automatically changed
```

**Key Benefits:**
- Atomic: All operations succeed or none do
- Resource references using `urn:uuid:` are resolved automatically
- Reduces round trips for creating related resources

#### Batch Bundles (Independent)

Each operation succeeds or fails independently:

```python
# Update multiple resources - some may fail without affecting others
bundle = {
    "resourceType": "Bundle",
    "type": "batch",
    "entry": [
        {
            "request": {"method": "PUT", "url": "Patient/123"},
            "resource": {"resourceType": "Patient", "id": "123", "active": True}
        },
        {
            "request": {"method": "PUT", "url": "Patient/456"},
            "resource": {"resourceType": "Patient", "id": "456", "active": False}
        },
        {
            "request": {"method": "DELETE", "url": "Observation/789"}
        }
    ]
}

# Execute - each operation processed independently
result = client.execute_batch(bundle)

# Check individual results
for entry in result.get("entry", []):
    response = entry.get("response", {})
    print(f"Status: {response.get('status')}")
```

### Binary File Operations

Handle binary files (PDFs, images, documents) in a FHIR-compliant way.

#### Upload Binary Files

```python
# Upload a PDF document
with open("lab_report.pdf", "rb") as f:
    pdf_content = f.read()

binary_resource = client.upload_binary(
    content=pdf_content,
    content_type="application/pdf"
)

print(f"Binary ID: {binary_resource['id']}")
print(f"Content Type: {binary_resource['contentType']}")

# Upload an image
with open("xray.png", "rb") as f:
    image_content = f.read()

binary = client.upload_binary(
    content=image_content,
    content_type="image/png"
)
```

#### Download Binary Files

The download method uses FHIR-compliant content negotiation to retrieve raw binary data efficiently:

```python
# Download binary content
pdf_bytes = client.download_binary(binary_id="binary-123")

# Save to file
with open("downloaded_report.pdf", "wb") as f:
    f.write(pdf_bytes)

# Asynchronous
async def download_file(binary_id):
    content = await async_client.download_binary(binary_id)
    return content
```

**Technical Note:** PyMedplum uses `Accept: */*` header to request raw binary content directly from the server, which is more efficient than fetching the FHIR resource and decoding base64 data.

### DocumentReference Creation

Create FHIR DocumentReferences that link binary content to patients with proper metadata:

```python
# Complete workflow: Upload binary and create DocumentReference
with open("discharge_summary.pdf", "rb") as f:
    pdf_content = f.read()

# Step 1: Upload the binary
binary = client.upload_binary(pdf_content, "application/pdf")

# Step 2: Create DocumentReference
doc_ref = client.create_document_reference(
    patient_id="patient-123",
    binary_id=binary["id"],
    content_type="application/pdf",
    title="Discharge Summary",
    description="Summary of hospital stay and discharge instructions"
)

print(f"DocumentReference ID: {doc_ref['id']}")
print(f"Linked to patient: {doc_ref['subject']['reference']}")
```

#### With Additional Metadata

Include document type coding and other FHIR metadata:

```python
doc_ref = client.create_document_reference(
    patient_id="patient-456",
    binary_id=binary["id"],
    content_type="application/pdf",
    title="Lab Results - Complete Blood Count",
    description="CBC performed on 2024-01-15",
    doc_type_code={
        "coding": [{
            "system": "http://loinc.org",
            "code": "11502-2",
            "display": "Laboratory report"
        }],
        "text": "Laboratory report"
    }
)
```

#### Asynchronous Workflow

```python
async def upload_patient_document(patient_id: str, file_path: str):
    # Read file
    with open(file_path, "rb") as f:
        content = f.read()
    
    # Upload binary
    binary = await async_client.upload_binary(content, "application/pdf")
    
    # Create document reference
    doc_ref = await async_client.create_document_reference(
        patient_id=patient_id,
        binary_id=binary["id"],
        content_type="application/pdf",
        title="Patient Document"
    )
    
    return doc_ref

# Usage
doc_ref = await upload_patient_document("patient-789", "document.pdf")
```

### Best Practices

1. **C-CDA Export**: Cache exports when possible; generation can be resource-intensive
2. **Terminology Validation**: Validate codes before creating resources to ensure data quality
3. **Transactions**: Use for creating related resources that must exist together
4. **Batches**: Use for bulk operations where individual failures are acceptable
5. **Binary Files**: Always create a DocumentReference after uploading to maintain proper medical record linkage
6. **Error Handling**: All operations may raise `MedplumError` exceptions - wrap in try/except blocks


## GraphQL Queries
The Medplum API supports GraphQL for complex data queries. The `execute_graphql` method allows you to send these queries.

```python
query = """
query GetPatient($id: ID!) {
    Patient(id: $id) {
        id
        name { family given }
    }
}
"""

variables = {"id": "some-patient-id"}

# Synchronous
result = client.execute_graphql(query, variables)
print(result["data"]["Patient"])

# Asynchronous
async def get_patient_graphql():
    result = await async_client.execute_graphql(query, variables)
    print(result["data"]["Patient"])
```

## "On-Behalf-Of" Operations

The "on-behalf-of" (OBO) feature is a powerful security mechanism for scenarios where one authenticated user (e.g., a practitioner) needs to perform actions as another user (e.g., a patient). This is not done by referencing the patient directly, but by referencing a **`ProjectMembership`**.

A `ProjectMembership` is a critical resource that links a user, their profile (like a `Patient` or `Practitioner` resource), and an access policy that defines their permissions. When you use OBO, you are temporarily adopting the context and permissions of that specific membership.

### 1. Persistent OBO Client
You can initialize a client that will perform *all* its operations on behalf of a specific `ProjectMembership`. This is useful for services that consistently act within a single role.

```python
from pymedplum.client import MedplumClient

# First, you need the ID of the patient's ProjectMembership
patient_membership_id = "some-project-membership-id" # e.g., from a search

# This client will ALWAYS act on behalf of the specified membership
obo_client = MedplumClient(
    base_url="https://api.medplum.com/",
    access_token="YOUR_PRACTITIONER_TOKEN",
    default_on_behalf_of=patient_membership_id
)

# This operation is now performed with the patient's permissions
questionnaire = obo_client.read("Questionnaire", "some-questionnaire-id")
```

### 2. Temporary OBO with Context Managers (Recommended)
For most use cases, the safest and most flexible approach is to use the `on_behalf_of()` context manager. It temporarily applies the OBO context only for the operations within the `with` block, and automatically reverts the client to its original state afterward.

This is ideal for a practitioner switching between different patients in a single session.

#### Synchronous Example
```python
# The base client is authenticated as the practitioner
client = MedplumClient(access_token="YOUR_PRACTITIONER_TOKEN")

# Assume you have fetched the patient's ProjectMembership ID
patient_membership_id = "ab123-cd456-ef789" # Example ID

# Temporarily act on behalf of the patient's membership
with client.on_behalf_of(patient_membership_id) as patient_context_client:
    # All actions here are performed "as the patient"
    patient_response = patient_context_client.create_resource({
        "resourceType": "QuestionnaireResponse",
        "status": "completed",
        "subject": {"reference": "Patient/the-patient-id"},
        # ... other response data
    })
    print("Submitted response on behalf of patient.")

# Outside the `with` block, the client is back to being the practitioner
practitioner_note = client.create_resource({
    "resourceType": "Observation",
    "status": "final",
    "code": {"text": "Practitioner review of patient submission"}
})
print("Practitioner created a follow-up note.")
```

#### Asynchronous Example
The same secure pattern applies to the `AsyncMedplumClient` using `async with`.

```python
async_client = AsyncMedplumClient(access_token="YOUR_PRACTITIONER_TOKEN")
patient_membership_id = "ab123-cd456-ef789"

async with async_client.on_behalf_of(patient_membership_id) as patient_context_client:
    await patient_context_client.create_resource(...)

# Code here executes as the practitioner again
await async_client.search_resources("Practitioner")
```

## Administrative Features
The client can be used to manage project-level administrative settings if you have the appropriate permissions.

### Managing Project Secrets
You can add, update, or remove project secrets.

```python
project_id = "YOUR_PROJECT_ID"

# Get current secrets
project = client.get(f"admin/projects/{project_id}")
current_secrets = project.get("project", {}).get("secret", [])

# Add a new secret
new_secrets = current_secrets + [{"name": "NEW_API_KEY", "valueString": "secret-value"}]

# Update
client.post(f"admin/projects/{project_id}/secrets", new_secrets)
```

### Managing Project Sites
Similarly, you can manage the sites (domains) associated with your project.

```python
project_id = "YOUR_PROJECT_ID"
project = client.get(f"admin/projects/{project_id}")
current_sites = project.get("project", {}).get("site", [])

new_sites = current_sites + [{"name": "New Site", "domain": ["new-app.example.com"]}]

client.post(f"admin/projects/{project_id}/sites", new_sites)
```
## Interacting with Private Medplum APIs
While most interactions should use the FHIR-specific methods (`create_resource`, `search_one`, etc.), you can also interact with any of Medplum's private administrative APIs using the generic `get()`, `post()`, `put()`, and `delete()` methods.

This is particularly useful for administrative tasks that don't have a dedicated helper method.

### Example: Inviting a New User
A common administrative task is inviting a new user to a project. While you can use the generic `post()` method, the client provides a dedicated `invite_user()` helper function that simplifies this entire process.

This high-level method handles the API call and payload construction for you.

```python
try:
    # Use the dedicated helper method
    membership = client.invite_user(
        project_id="YOUR_PROJECT_ID",
        resource_type="Practitioner",
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com",
        send_email=True,  # Send a welcome email to the user
    )
    print(f"Successfully invited practitioner. Membership ID: {membership['id']}")

except MedplumError as e:
    print(f"Error inviting user: {e}")
```

The `invite_user` method has additional parameters for setting a user's password, scope, and access policy, making it a powerful tool for user provisioning.
