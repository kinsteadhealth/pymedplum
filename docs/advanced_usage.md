# Advanced Usage

This section covers more advanced features of the `pymedplum` library, including detailed CRUD operations, GraphQL, and administrative functions.

## Table of Contents

- [Advanced FHIR Search](#advanced-fhir-search) - Includes, reverse includes, chaining, modifiers, pagination
- [Conditional Create (If-None-Exist)](#conditional-create-if-none-exist) - Idempotent resource creation
- [Advanced CRUD Operations](#advanced-crud-operations) - Update, patch, optimistic locking, delete
- [FHIR Operations and Special Workflows](#fhir-operations-and-special-workflows) - Execute operations, C-CDA export, terminology, bundles, binaries
- [GraphQL Queries](#graphql-queries)
- ["On-Behalf-Of" Operations](#on-behalf-of-operations) - Act as another user
- [Administrative Features](#administrative-features) - Project secrets, sites
- [Interacting with Private Medplum APIs](#interacting-with-private-medplum-apis)

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

### Recursive Includes (`_include:iterate` / `_revinclude:iterate`)

The `:iterate` modifier allows you to recursively follow references on resources that were themselves included. This is useful when you need to traverse multiple levels of references.

```python
# Get MedicationRequest with Medication, then the manufacturer of the Medication
bundle = client.search_with_options(
    "MedicationRequest",
    {"patient": "Patient/123"},
    include="MedicationRequest:medication",
    include_iterate="Medication:manufacturer"
)

# The bundle now contains:
# - MedicationRequest resources
# - Medication resources (from _include)
# - Organization resources (manufacturers, from _include:iterate)
```

You can also use `_revinclude:iterate` for recursive reverse includes:

```python
# Get Patient, then Observations, then any Provenance records for those Observations
bundle = client.search_with_options(
    "Patient",
    {"identifier": "MRN|12345"},
    revinclude="Observation:patient",
    revinclude_iterate="Provenance:target"
)
```

Multiple iterate values are supported:

```python
bundle = client.search_with_options(
    "MedicationRequest",
    {"patient": "Patient/123"},
    include="MedicationRequest:medication",
    include_iterate=["Medication:manufacturer", "Organization:partof"]
)
```

**Note**: The iterate behavior depends on server support. Not all FHIR servers implement recursive includes identically.

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

### Using `search_with_options` for TypeScript SDK Parity

The `search_with_options` method provides a more ergonomic interface for FHIR search parameters, matching the patterns used in the Medplum TypeScript SDK:

```python
from pymedplum.fhir import Patient, Observation

# Get just the count of matching resources (efficient for dashboards)
result = client.search_with_options(
    "Patient",
    {"active": "true"},
    summary="count"
)
print(f"Active patients: {result.get('total', 0)}")

# Request only specific elements (bandwidth optimization)
result = client.search_with_options(
    "Patient",
    {"family": "Smith"},
    elements=["id", "name", "birthDate", "identifier"]
)

# Get accurate total count (useful for pagination UI)
bundle = client.search_with_options(
    "Observation",
    {"patient": "Patient/123"},
    total="accurate",
    return_bundle=True
)
print(f"Total observations: {bundle.total}")

# Point-in-time query for historical analysis
historical = client.search_with_options(
    "Patient",
    {"family": "Smith"},
    at="2024-01-01T00:00:00Z"  # Query data as of this timestamp
)
```

#### Summary Modes

The `summary` parameter controls what data is returned:

| Mode | Description | Use Case |
|------|-------------|----------|
| `"count"` | Only return the total count | Dashboard metrics, pagination |
| `"true"` | Return summary elements only | List views, quick overviews |
| `"text"` | Return text and mandatory elements | Display purposes |
| `"data"` | Remove text from response | Data processing |
| `"false"` | Return full resources | Full resource access |

```python
# Get summary for list display
bundle = client.search_with_options(
    "Patient",
    {"active": "true"},
    summary="true",
    count=50,
    return_bundle=True
)
```

#### Total Count Modes

The `total` parameter controls total count calculation:

| Mode | Description | Performance |
|------|-------------|-------------|
| `"none"` | Don't calculate total | Fastest |
| `"estimate"` | Return estimated count | Fast |
| `"accurate"` | Return exact count | Slower (full scan) |

```python
# For infinite scroll (don't need exact total)
bundle = client.search_with_options(
    "Observation",
    {"patient": "Patient/123"},
    total="none",
    count=20,
    return_bundle=True
)

# For pagination with page numbers (need accurate total)
bundle = client.search_with_options(
    "Patient",
    {"organization": "Organization/456"},
    total="accurate",
    count=20,
    offset=40,  # Page 3
    return_bundle=True
)
print(f"Showing page 3 of {(bundle.total + 19) // 20} pages")
```

#### Combining Multiple Options

```python
# Complex search with all options
bundle = client.search_with_options(
    "Observation",
    {"code": "http://loinc.org|8867-4"},  # Heart rate
    elements=["id", "effectiveDateTime", "valueQuantity", "subject"],
    total="accurate",
    count=100,
    sort=["-effectiveDateTime"],  # Most recent first
    include="Observation:patient",  # Include referenced patients
    return_bundle=True,
    as_fhir=Observation
)

# Process results
for obs in bundle.get_resources():
    print(f"{obs.effective_date_time}: {obs.value_quantity.value} bpm")
```

## Conditional Create (If-None-Exist)

The conditional create mechanism allows you to create a resource only if no matching resource already exists. This is essential for preventing duplicate resources and implementing idempotent operations.

### Basic Usage

```python
from pymedplum.fhir import Patient

# Create a patient with an identifier
patient = Patient(
    identifier=[{"system": "http://hospital.org/mrn", "value": "MRN-12345"}],
    name=[{"family": "Smith", "given": ["John"]}]
)

# Only create if no patient with this identifier exists
# Returns the created or existing resource
resource = client.create_resource_if_none_exist(
    patient,
    if_none_exist="identifier=http://hospital.org/mrn|MRN-12345"
)

print(f"Patient ID: {resource['id']}")
```

**Note:** The method returns the resource directly. The server returns HTTP 201 for newly created resources and HTTP 200 for existing matches, but this status is not exposed in the return value. If you need to know whether a resource was created, compare the returned ID with the input (if provided) or check a timestamp.

### Use Cases

#### Preventing Duplicate Patient Records

```python
def ensure_patient_exists(mrn: str, name: dict) -> dict:
    """
    Ensure a patient with the given MRN exists.
    Returns the existing patient or creates a new one.
    """
    patient = Patient(
        identifier=[{"system": "http://hospital.org/mrn", "value": mrn}],
        name=[name]
    )

    return client.create_resource_if_none_exist(
        patient,
        if_none_exist=f"identifier=http://hospital.org/mrn|{mrn}"
    )

# Safe to call multiple times - won't create duplicates
patient = ensure_patient_exists("12345", {"family": "Smith", "given": ["John"]})
```

#### Idempotent Device Registration

```python
def register_device(device_serial: str, device_type: str) -> dict:
    """
    Register a device, returning existing if already registered.
    """
    device = {
        "resourceType": "Device",
        "identifier": [{"system": "http://example.org/devices", "value": device_serial}],
        "type": {"text": device_type}
    }

    return client.create_resource_if_none_exist(
        device,
        if_none_exist=f"identifier=http://example.org/devices|{device_serial}"
    )
```

#### Ensuring Reference Data Exists

```python
def ensure_organization_exists(npi: str, name: str) -> dict:
    """
    Ensure an organization with the given NPI exists.
    """
    org = {
        "resourceType": "Organization",
        "identifier": [{"system": "http://hl7.org/fhir/sid/us-npi", "value": npi}],
        "name": name
    }

    return client.create_resource_if_none_exist(
        org,
        if_none_exist=f"identifier=http://hl7.org/fhir/sid/us-npi|{npi}"
    )
```

### Error Handling

If multiple resources match the search criteria, the server returns HTTP 412 (Precondition Failed):

```python
from pymedplum.exceptions import PreconditionFailedError

try:
    resource = client.create_resource_if_none_exist(
        patient,
        if_none_exist="family=Smith"  # Too broad - may match multiple
    )
except PreconditionFailedError:
    # Multiple patients matched - need more specific criteria
    print("Search criteria matched multiple resources")
```

### Best Practices

1. **Use specific identifiers**: Search by unique identifiers (MRN, NPI, UUID) rather than broad criteria
2. **Include system in identifier searches**: Use `identifier=system|value` format for precision
3. **Consider race conditions**: In high-concurrency scenarios, use transactions for related resources
4. **Query string formats**: The `if_none_exist` parameter accepts multiple formats:
   - Plain query strings: `"identifier=http://example.org|12345"` (recommended)
   - With leading `?`: `"?identifier=http://example.org|12345"` (automatically stripped)
   - Full URLs: `"https://example.com/fhir/R4/Patient?identifier=..."` (query portion extracted)
   - Empty strings or just `"?"` will raise `ValueError`

### Async Usage

```python
async def ensure_patient_async(mrn: str):
    patient = Patient(
        identifier=[{"system": "http://hospital.org/mrn", "value": mrn}],
        name=[{"family": "Doe"}]
    )

    # With type-safe response
    resource = await async_client.create_resource_if_none_exist(
        patient,
        if_none_exist=f"identifier=http://hospital.org/mrn|{mrn}",
        as_fhir=Patient
    )
    return resource
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

### Optimistic Locking for Concurrent Updates

PyMedplum supports optimistic locking through the HTTP `If-Match` header, which prevents lost updates when multiple clients modify the same resource concurrently. This is crucial for scenarios like appointment scheduling, inventory management, or any workflow where concurrent modifications can cause conflicts.

#### How Optimistic Locking Works

1. **Read a resource** - Server returns current version in `meta.versionId`
2. **Modify the resource** locally
3. **Update with version check** - Include `If-Match` header with the version
4. **Server validates** - Update succeeds only if version matches
5. **Handle conflicts** - If version doesn't match, resource was modified elsewhere

#### Basic Example

```python
from pymedplum.exceptions import PreconditionFailedError

# Read resource to get current version
patient = client.read_resource("Patient", "123")
current_version = patient["meta"]["versionId"]

# Modify the resource
patient["active"] = False

# Update with version check to prevent concurrent modification
try:
    updated = client.update_resource(
        patient,
        headers={"If-Match": f'W/"{current_version}"'}
    )
    print(f"Successfully updated to version {updated['meta']['versionId']}")
except PreconditionFailedError:
    # Resource was modified by another process
    print("Conflict detected - resource was modified elsewhere")
    # Refetch and retry
    patient = client.read_resource("Patient", "123")
    # ... retry logic
```

#### Preventing Double-Booking with Optimistic Locking

A common use case is preventing two users from booking the same appointment slot:

```python
from pymedplum.exceptions import PreconditionFailedError

def try_book_slot(slot_id: str, patient_id: str, max_retries: int = 3) -> dict:
    """
    Attempt to book a slot with optimistic locking and retry logic.

    Returns the booked slot or raises an exception if booking fails.
    """
    for attempt in range(max_retries):
        # Read current slot state
        slot = client.read_resource("Slot", slot_id)

        # Check if slot is still available
        if slot["status"] != "free":
            raise ValueError(f"Slot {slot_id} is not available")

        # Get current version for optimistic locking
        version = slot["meta"]["versionId"]

        # Mark slot as busy
        slot["status"] = "busy"

        try:
            # Try to update with version check
            updated_slot = client.update_resource(
                slot,
                headers={"If-Match": f'W/"{version}"'}
            )

            # Success! Now create the appointment
            appointment = client.create_resource({
                "resourceType": "Appointment",
                "status": "booked",
                "slot": [{"reference": f"Slot/{slot_id}"}],
                "participant": [{
                    "actor": {"reference": f"Patient/{patient_id}"},
                    "status": "accepted"
                }]
            })

            return appointment

        except PreconditionFailedError:
            # Someone else modified the slot - retry
            if attempt < max_retries - 1:
                print(f"Conflict on attempt {attempt + 1}, retrying...")
                continue
            else:
                raise ValueError("Failed to book slot after maximum retries")

    raise ValueError("Booking failed")

# Usage
try:
    appointment = try_book_slot("slot-123", "patient-456")
    print(f"Successfully booked appointment: {appointment['id']}")
except ValueError as e:
    print(f"Booking failed: {e}")
```

#### Using Optimistic Locking with Patch Operations

```python
# Read resource and get version
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]

# Define patch operations
operations = [
    {"op": "replace", "path": "/active", "value": False}
]

# Apply patch with version check
try:
    patched = client.patch_resource(
        "Patient", "123", operations,
        headers={"If-Match": f'W/"{version}"'}
    )
except PreconditionFailedError:
    # Handle conflict - resource was modified
    patient = client.read_resource("Patient", "123")
    # Decide whether to retry or abort
```

#### Using Optimistic Locking with Delete

```python
# Read resource to ensure it exists and get version
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]

# Delete only if version matches (prevents deleting modified resource)
try:
    client.delete_resource(
        "Patient", "123",
        headers={"If-Match": f'W/"{version}"'}
    )
except PreconditionFailedError:
    print("Resource was modified - cannot delete outdated version")
```

#### Best Practices for Optimistic Locking

1. **Always use optimistic locking for concurrent workflows**
   - Appointment booking
   - Inventory management
   - Slot/schedule management
   - Any shared resource updates

2. **Implement retry logic with exponential backoff**
   ```python
   import time

   def update_with_retry(resource_type, resource_id, update_fn, max_retries=3):
       """Generic retry wrapper for optimistic locking conflicts."""
       for attempt in range(max_retries):
           resource = client.read_resource(resource_type, resource_id)
           version = resource["meta"]["versionId"]

           # Apply updates
           updated_resource = update_fn(resource)

           try:
               return client.update_resource(
                   updated_resource,
                   headers={"If-Match": f'W/"{version}"'}
               )
           except PreconditionFailedError:
               if attempt < max_retries - 1:
                   # Exponential backoff
                   time.sleep(2 ** attempt * 0.1)
                   continue
               raise
   ```

3. **Handle `PreconditionFailedError` appropriately**
   - Refetch the resource to get current state
   - Re-evaluate if the operation should still proceed
   - Consider user intent (was the conflict expected?)

4. **Use for all CRUD operations in concurrent contexts**
   - `create_resource` - Not needed (no existing version)
   - `read_resource` - Not applicable
   - `update_resource` - Use for all concurrent updates
   - `patch_resource` - Use for all concurrent patches
   - `delete_resource` - Use to prevent deleting modified resources

5. **Version format**
   - Always use `W/"version"` format (weak ETag)
   - Example: `W/"1"`, `W/"2"`, etc.
   - The `W/` prefix indicates a weak validator

#### When NOT to Use Optimistic Locking

- Single-user workflows with no concurrent access
- Read-only operations
- Batch operations where conflicts are acceptable
- Initial resource creation (no version exists yet)

### Deleting a Resource
To delete a resource, use the `delete_resource` method.

```python
client.delete_resource("Patient/some-patient-id")
```

## FHIR Operations and Special Workflows

PyMedplum provides dedicated methods for specialized FHIR operations beyond standard CRUD, including clinical document export, terminology validation, atomic transactions, and binary file handling.

### Execute FHIR Operations

The `execute_operation` method provides a generic way to invoke any FHIR operation, including standard operations (like `$match`, `$everything`, `$validate`) and custom Medplum operations.

#### Type-Level Operations

Operations that apply to a resource type (e.g., `Patient/$match`):

```python
# Patient matching using $match operation
result = client.execute_operation(
    "Patient",
    "match",
    params={
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "resource",
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "Smith", "given": ["John"]}],
                    "birthDate": "1990-01-15"
                }
            }
        ]
    }
)

# Result is a Bundle with matching patients and scores
for entry in result.get("entry", []):
    patient = entry["resource"]
    score = entry.get("search", {}).get("score", 0)
    print(f"Match: {patient['id']} (score: {score})")
```

#### Instance-Level Operations

Operations that apply to a specific resource instance (e.g., `Patient/123/$everything`):

```python
# Get all resources related to a patient
bundle = client.execute_operation(
    "Patient",
    "everything",
    resource_id="patient-123"
)

# Bundle contains Patient plus all related resources
for entry in bundle.get("entry", []):
    resource = entry["resource"]
    print(f"{resource['resourceType']}: {resource['id']}")
```

#### Custom Medplum Operations

Invoke custom operations defined via Medplum Bots and OperationDefinitions:

```python
# Call a custom operation with a full Parameters resource
result = client.execute_operation(
    "MedicationRequest",
    "calculate-dose",
    resource_id="med-req-456",
    params={
        "resourceType": "Parameters",
        "parameter": [
            {"name": "weight", "valueDecimal": 70},
            {"name": "unit", "valueString": "kg"}
        ]
    }
)

# With custom headers
result = client.execute_operation(
    "Patient",
    "my-custom-operation",
    params={
        "resourceType": "Parameters",
        "parameter": [{"name": "family", "valueString": "Doe"}]
    },
    headers={"X-Custom-Header": "value"}
)
```

#### Using GET Method for Simple Lookups

Many FHIR operations support both GET (with query parameters) and POST (with a Parameters body). Use `method="GET"` for simple lookups:

```python
# GET with query parameters - simpler for lookups
result = client.execute_operation(
    "CodeSystem",
    "lookup",
    params={"code": "12345", "system": "http://loinc.org"},
    method="GET"  # Parameters become query string
)

# ValueSet expansion with filter
expansion = client.execute_operation(
    "ValueSet",
    "$expand",
    params={"url": "http://hl7.org/fhir/ValueSet/observation-status", "filter": "fin"},
    method="GET"
)
```

#### Auto-Wrapping Parameters

For convenience, you can use `wrap_params=True` to automatically convert a simple dict into a FHIR Parameters resource:

```python
# Without wrap_params - you must build the Parameters resource manually
result = client.execute_operation(
    "Patient",
    "match",
    params={
        "resourceType": "Parameters",
        "parameter": [
            {"name": "onlyCertainMatches", "valueBoolean": True},
            {"name": "count", "valueInteger": 10}
        ]
    }
)

# With wrap_params=True - dict is auto-converted
result = client.execute_operation(
    "Patient",
    "custom-operation",
    params={"onlyCertainMatches": True, "count": 10},
    wrap_params=True  # Converts to Parameters resource
)
```

**Limitations of `wrap_params`:** The auto-conversion handles basic types (string→valueString, int→valueInteger, bool→valueBoolean, float→valueDecimal) and recognizes Coding/Reference dicts. However, for operations requiring specific value types like `valueCode`, `valueUri`, or `valueCanonical`, you should build the Parameters resource manually.

#### Async Usage

```python
# All operations work with AsyncMedplumClient
async def get_patient_everything(patient_id: str):
    bundle = await async_client.execute_operation(
        "Patient",
        "everything",
        resource_id=patient_id
    )
    return bundle
```

**Note:** The operation name can be specified with or without the `$` prefix - both `"match"` and `"$match"` work.

### Setting Resource Accounts (Multi-Compartment Access)

The `set_accounts` method manages `meta.accounts` on FHIR resources using Medplum's `$set-accounts` operation. This is the recommended way to control which organizations have access to a resource when using AccessPolicies.

```python
# Assign an organization to a patient's accounts
result = client.set_accounts(
    resource_ref="Patient/patient-123",
    org_ref="Organization/org-456"
)

# The operation returns a Parameters resource with update count
print(f"Resources updated: {result['parameter'][0]['valueInteger']}")
```

**When to use `set_accounts`:**

- When using compartment-based AccessPolicies that filter by `meta.accounts`
- To grant an organization access to a resource and its compartment
- When you need consistent access control across related resources

**Note:** This method is preferred over automatic organization tagging (`org_mode`) when using AccessPolicies, as it ensures the `meta.accounts` field is properly set for access control checks. The operation can optionally propagate account changes to all resources in a patient's compartment (see Medplum documentation for the `propagate` parameter).

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

### ValueSet Expansion (`$expand`)

Expand a ValueSet to retrieve all codes it contains. This is useful for building dropdown menus, typeahead searches, and populating code pickers.

```python
# Expand a standard FHIR ValueSet
expansion = client.expand_valueset(
    valueset_url="http://hl7.org/fhir/ValueSet/observation-status"
)

# Extract codes from expansion
for concept in expansion.get("expansion", {}).get("contains", []):
    print(f"{concept['code']}: {concept['display']}")
```

#### Filtering and Pagination

For large ValueSets, use filtering and pagination to limit results:

```python
# Search for codes matching a filter
expansion = client.expand_valueset(
    valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
    filter="diabetes",  # Substring match on display
    count=20,           # Max 20 results
    offset=0            # Start from beginning
)

# Build a code picker with pagination
def get_codes_page(filter_text: str, page: int, page_size: int = 20):
    return client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
        filter=filter_text,
        count=page_size,
        offset=page * page_size
    )
```

#### Expansion Options

```python
# Expand with all options
expansion = client.expand_valueset(
    valueset_url="http://hl7.org/fhir/ValueSet/condition-severity",
    include_designations=True,    # Include alternate names/translations
    active_only=True,             # Only active codes
    exclude_nested=True,          # Flatten hierarchy
    exclude_not_for_ui=True,      # Only selectable codes
    display_language="en",        # English display text
    property=["definition"]       # Include code definitions
)
```

#### Expanding by ValueSet ID

```python
# Expand a custom ValueSet stored in Medplum
expansion = client.expand_valueset(valueset_id="my-custom-valueset")
```

### CodeSystem Lookup (`$lookup`)

Look up detailed information about a code in a CodeSystem, including display names, definitions, properties, and designations.

```python
# Look up a LOINC code
result = client.lookup_concept(
    code="8867-4",
    system="http://loinc.org"
)

# Extract information from Parameters response
for param in result.get("parameter", []):
    name = param.get("name")
    if name == "display":
        print(f"Display: {param.get('valueString')}")
    elif name == "name":
        print(f"Code System: {param.get('valueString')}")
    elif name == "version":
        print(f"Version: {param.get('valueString')}")
```

#### Looking Up with Properties

Request specific properties about the code:

```python
# Get SNOMED CT code with hierarchical properties
result = client.lookup_concept(
    code="38341003",  # Hypertension
    system="http://snomed.info/sct",
    property=["parent", "child", "definition"]
)

# Extract properties
for param in result.get("parameter", []):
    if param.get("name") == "property":
        for part in param.get("part", []):
            if part.get("name") == "code":
                prop_code = part.get("valueCode")
            elif part.get("name") == "value":
                prop_value = part.get("valueCode") or part.get("valueString")
        print(f"Property {prop_code}: {prop_value}")
```

#### Looking Up with Display Language

```python
# Get display in specific language
result = client.lookup_concept(
    code="38341003",
    system="http://snomed.info/sct",
    display_language="es"  # Spanish
)
```

### ConceptMap Translation (`$translate`)

Translate codes between different code systems using ConceptMaps. This is essential for interoperability when mapping between local codes and standard terminologies.

```python
# Translate using a ConceptMap URL
result = client.translate_concept(
    code="final",
    system="http://hl7.org/fhir/observation-status",
    conceptmap_url="http://example.org/ConceptMap/obs-status-to-local",
    target_system="http://example.org/local-codes"
)

# Check translation results
for param in result.get("parameter", []):
    if param.get("name") == "result":
        found = param.get("valueBoolean")
        print(f"Translation found: {found}")
    elif param.get("name") == "match":
        # Extract matched concept
        for part in param.get("part", []):
            if part.get("name") == "concept":
                coding = part.get("valueCoding", {})
                print(f"Mapped to: {coding.get('code')} ({coding.get('display')})")
            elif part.get("name") == "equivalence":
                equiv = part.get("valueCode")
                print(f"Equivalence: {equiv}")
```

#### Translation Helpers

```python
def translate_to_local_code(
    code: str,
    source_system: str,
    target_system: str
) -> str | None:
    """
    Translate a standard code to a local system code.
    Returns None if no translation found.
    """
    result = client.translate_concept(
        code=code,
        system=source_system,
        target_system=target_system
    )

    # Check if translation was successful
    for param in result.get("parameter", []):
        if param.get("name") == "result" and not param.get("valueBoolean"):
            return None
        if param.get("name") == "match":
            for part in param.get("part", []):
                if part.get("name") == "concept":
                    return part.get("valueCoding", {}).get("code")

    return None


# Usage
local_code = translate_to_local_code(
    code="final",
    source_system="http://hl7.org/fhir/observation-status",
    target_system="http://hospital.org/codes"
)
```

#### Reverse Translation

Translate from target back to source system:

```python
# Reverse translation (target to source)
result = client.translate_concept(
    code="LOC-001",
    system="http://hospital.org/local-codes",
    conceptmap_url="http://example.org/ConceptMap/status-mapping",
    reverse=True  # Reverse direction
)
```

#### Using Full Coding or CodeableConcept

```python
# Translate using a Coding object
result = client.translate_concept(
    coding={
        "system": "http://hl7.org/fhir/observation-status",
        "code": "final",
        "display": "Final"
    },
    target_system="http://hospital.org/local-codes"
)

# Translate using a CodeableConcept
result = client.translate_concept(
    codeable_concept={
        "coding": [{
            "system": "http://snomed.info/sct",
            "code": "38341003",
            "display": "Hypertensive disorder"
        }],
        "text": "Hypertension"
    },
    target_system="http://hl7.org/fhir/sid/icd-10"
)
```

#### Async Terminology Operations

All terminology operations are available in async form:

```python
async def get_condition_codes(filter_text: str):
    """Search for condition codes asynchronously."""
    expansion = await async_client.expand_valueset(
        valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
        filter=filter_text,
        count=20
    )
    return [
        {"code": c["code"], "display": c["display"]}
        for c in expansion.get("expansion", {}).get("contains", [])
    ]


async def lookup_snomed_code(code: str):
    """Look up SNOMED code details asynchronously."""
    result = await async_client.lookup_concept(
        code=code,
        system="http://snomed.info/sct"
    )
    for param in result.get("parameter", []):
        if param.get("name") == "display":
            return param.get("valueString")
    return None
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
