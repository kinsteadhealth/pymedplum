# Client API Reference

This page provides a comprehensive reference for all methods available on the `MedplumClient` and `AsyncMedplumClient`.

## Synchronous Client (`MedplumClient`)

### Authentication

#### `authenticate() -> str`

Authenticate using client credentials flow.

**Returns**: Access token string

**Raises**:
- `ValueError`: If client_id or client_secret are missing
- `OperationOutcomeError`: On authentication failure

**Example**:
```python
client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
token = client.authenticate()
print(f"Authenticated with token: {token[:20]}...")
```

### Resource Operations

#### `create_resource(resource, headers=None, *, accounts=None, as_fhir=None) -> dict | Model`

Create a new FHIR resource.

**Parameters**:
- `resource` (dict | Pydantic model): The resource to create
- `headers` (dict[str, str], optional): Additional HTTP headers for the request
- `accounts` (str | list[str], optional): Account references to set on `meta.accounts` at creation time for multi-tenant compartment assignment
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response

**Returns**: dict or Pydantic model instance - The created resource with server-assigned ID

**Example**:
```python
from pymedplum.fhir import Patient

# Basic creation
patient_dict = {"resourceType": "Patient", "active": True}
created = client.create_resource(patient_dict)

# With account assignment (multi-tenant)
created = client.create_resource(
    patient_dict,
    accounts="Organization/org-456",
)

# Multiple accounts
created = client.create_resource(
    patient_dict,
    accounts=["Organization/org-456", "Organization/org-789"],
)

# With type-safe response
created_patient = client.create_resource(patient_dict, as_fhir=Patient)
print(created_patient.name[0].family)  # Full IDE autocomplete!
```

#### `create_resource_if_none_exist(resource, if_none_exist, headers=None, *, accounts=None, as_fhir=None) -> dict | Model`

Conditionally create a FHIR resource only if no matching resource exists (If-None-Exist).

This method uses FHIR's conditional create mechanism via the `If-None-Exist` header. If a resource matching the search criteria already exists, the existing resource is returned (HTTP 200). If no match is found, a new resource is created (HTTP 201).

**Parameters**:
- `resource` (dict | Pydantic model): The resource to create
- `if_none_exist` (str): FHIR search query string (e.g., "identifier=MRN|12345"). Accepts plain query strings or strings with a leading `?` (which is automatically stripped). Full URLs are also accepted and the query portion is extracted.
- `headers` (dict[str, str], optional): Additional HTTP headers for the request
- `accounts` (str | list[str], optional): Account references to set on `meta.accounts` at creation time
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response

**Returns**: dict or Pydantic model instance - The created or existing resource

**Note**: The method returns only the resource. The HTTP status code (201 Created vs 200 OK) is not exposed. If you need to determine whether a resource was newly created, compare the returned ID against expected values or check timestamps.

**Raises**:
- `PreconditionFailedError`: If multiple resources match the search criteria (HTTP 412)

**Example**:
```python
from pymedplum.fhir import Patient

# Create patient only if no matching identifier exists
patient = Patient(
    identifier=[{"system": "http://hospital.org/mrn", "value": "12345"}],
    name=[{"family": "Smith", "given": ["John"]}]
)

resource = client.create_resource_if_none_exist(
    patient,
    if_none_exist="identifier=http://hospital.org/mrn|12345"
)
print(f"Patient ID: {resource['id']}")

# With type-safe response
resource = client.create_resource_if_none_exist(
    patient,
    if_none_exist="identifier=http://hospital.org/mrn|12345",
    as_fhir=Patient
)
print(resource.name[0].family)  # Type-safe access

# Leading ? is automatically stripped (both forms work)
resource = client.create_resource_if_none_exist(
    patient,
    if_none_exist="?identifier=http://hospital.org/mrn|12345"  # Also valid
)
```

#### `read_resource(resource_type, resource_id, as_fhir=None, headers=None) -> dict | Model`

Read a FHIR resource by type and ID.

**Parameters**:
- `resource_type` (str): FHIR resource type (e.g., "Patient")
- `resource_id` (str): Resource ID
- `as_fhir` (Type[Model], optional): Pydantic model class to return
- `headers` (dict[str, str], optional): Additional HTTP headers for the request

**Returns**: dict or Pydantic model instance

**Raises**:
- `NotFoundError`: If resource doesn't exist

**Example**:
```python
from pymedplum.fhir.patient import Patient

# Get as dictionary
patient_dict = client.read_resource("Patient", "123")

# Get as typed model
patient = client.read_resource("Patient", "123", as_fhir=Patient)
print(patient.name[0].family)  # Type-safe access
```

#### `update_resource(resource, headers=None, *, accounts=None, as_fhir=None) -> dict | Model`

Update an existing FHIR resource (requires id).

**Parameters**:
- `resource` (dict | Pydantic model): Resource with id field
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)
- `accounts` (str | list[str], optional): Account references to set on `meta.accounts`
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response

**Returns**: dict or Pydantic model instance - The updated resource

**Raises**:
- `ValueError`: If resource lacks resourceType or id
- `PreconditionFailedError`: If `If-Match` header version doesn't match current resource version

**Example**:
```python
from pymedplum.fhir import Patient

# Read, modify, update pattern
patient = client.read_resource("Patient", "123", as_fhir=Patient)
patient.active = False
updated = client.update_resource(patient)

# With type-safe response
patient = client.read_resource("Patient", "123")
patient["active"] = False
updated_patient = client.update_resource(patient, as_fhir=Patient)
print(updated_patient.active)  # Full IDE autocomplete!

# With optimistic locking to prevent concurrent modifications
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]
patient["active"] = False
try:
    updated = client.update_resource(
        patient,
        headers={"If-Match": f'W/"{version}"'},
        as_fhir=Patient
    )
except PreconditionFailedError:
    # Resource was modified by another process - refetch and retry
    patient = client.read_resource("Patient", "123")
```

#### `patch_resource(resource_type, resource_id, operations, headers=None, *, as_fhir=None) -> dict | Model`

Apply JSON Patch operations to a resource.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `resource_id` (str): Resource ID
- `operations` (list[PatchOperation]): JSON Patch operations
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response

**Returns**: dict or Pydantic model instance - The patched resource

**Raises**:
- `PreconditionFailedError`: If `If-Match` header version doesn't match current resource version

**Example**:
```python
from pymedplum.fhir import Patient

# Patch and get as dict
operations = [
    {"op": "replace", "path": "/active", "value": False},
    {"op": "add", "path": "/telecom/-", "value": {"system": "email", "value": "new@example.com"}}
]
patched = client.patch_resource("Patient", "123", operations)

# With type-safe response
operations = [{"op": "replace", "path": "/active", "value": True}]
patched_patient = client.patch_resource("Patient", "123", operations, as_fhir=Patient)
print(patched_patient.active)  # Full IDE autocomplete!

# With optimistic locking
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]
patched = client.patch_resource(
    "Patient", "123", operations,
    headers={"If-Match": f'W/"{version}"'},
    as_fhir=Patient
)
```

#### `delete_resource(resource_type, resource_id, headers=None) -> None`

Delete a FHIR resource. Per the FHIR specification, successful deletion returns HTTP 204 No Content with no response body.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `resource_id` (str): Resource ID
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)

**Returns**: None (FHIR delete operations return HTTP 204 with no content)

**Raises**:
- `PreconditionFailedError`: If `If-Match` header version doesn't match current resource version

**Example**:
```python
client.delete_resource("Patient", "123")

# With optimistic locking to prevent accidental deletion of modified resource
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]
client.delete_resource("Patient", "123", headers={"If-Match": f'W/"{version}"'})
```

**Note**: Deletion in FHIR is a logical delete, not a physical delete. The resource is marked as deleted but previous versions remain accessible in the resource's history. After deletion, attempting to read the resource by its ID will return HTTP 410 Gone with a Location header pointing to the deleted version.

### Search Operations

#### `search_resources(resource_type, query=None, return_bundle=False, as_fhir=None) -> dict | FHIRBundle`

Search for FHIR resources.

**Parameters**:
- `resource_type` (str): FHIR resource type to search
- `query` (dict | list[tuple], optional): Search parameters
- `return_bundle` (bool): Return FHIRBundle wrapper if True
- `as_fhir` (Type[Model], optional): Pydantic model class for typed resources (only applies when return_bundle=True)

**Returns**: dict or FHIRBundle

**Example**:
```python
# Basic search
results = client.search_resources("Patient", {"family": "Smith"})
for entry in results.get("entry", []):
    print(entry["resource"]["id"])

# With FHIRBundle helper
bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True)
for patient in bundle:
    print(patient["id"])

# With type safety
from pymedplum.fhir import Patient
bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True, as_fhir=Patient)
patients = bundle.get_resources_typed(Patient)
```

#### `search_one(resource_type, query=None) -> dict | None`

Search for a single resource (limit 1).

**Parameters**:
- `resource_type` (str): Type of resource to search
- `query` (dict | list[tuple], optional): Search parameters

**Returns**: First matching resource or None

**Example**:
```python
patient = client.search_one("Patient", {"identifier": "MRN|12345"})
if patient:
    print(f"Found: {patient['id']}")
```

#### `search_resource_pages(resource_type, query=None, as_fhir=None) -> Iterator[dict | Model]`

Search resources with automatic pagination.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `query` (dict | list[tuple], optional): Search parameters
- `as_fhir` (Type[Model], optional): Pydantic model class for typed resources

**Yields**: Individual resources from paginated results

**Example**:
```python
from pymedplum.fhir import Observation

# Iterate over dict resources
for obs in client.search_resource_pages("Observation", {"patient": "Patient/123"}):
    print(f"Observation {obs['id']}: {obs['status']}")

# Type-safe iteration with Pydantic models
for obs in client.search_resource_pages("Observation", {"patient": "Patient/123"}, as_fhir=Observation):
    print(f"Observation {obs.id}: {obs.status}")  # Full IDE autocomplete!
```

#### `search_with_options(resource_type, query=None, *, summary=None, elements=None, total=None, at=None, count=None, offset=None, sort=None, include=None, include_iterate=None, revinclude=None, revinclude_iterate=None, return_bundle=False, as_fhir=None) -> dict | FHIRBundle`

Search for FHIR resources with named parameters for common FHIR search modifiers.

This method provides an ergonomic interface for FHIR search parameters like `_summary`, `_elements`, `_total`, `_include`, and `_at`. An alias `searchWithOptions` is also available for developers familiar with the Medplum TypeScript SDK naming conventions.

**Parameters**:
- `resource_type` (str): FHIR resource type to search
- `query` (dict | list[tuple], optional): Additional search parameters
- `summary` (SummaryMode, optional): Controls how much data is returned per resource:
  - `"true"` - Return only summary elements (id, meta, and elements marked as summary)
  - `"text"` - Return text summary plus id, meta, and top-level mandatory elements
  - `"data"` - Return all data elements but no text
  - `"count"` - Return just the count with no resources (use `bundle.total` or `result.get("total")`)
  - `"false"` - Return complete resources (default behavior)
- `elements` (list[str], optional): Specific elements to include in response
- `total` (TotalMode, optional): Controls how the total count is computed:
  - `"none"` - Do not include total (fastest)
  - `"estimate"` - Include an estimated total (fast but approximate)
  - `"accurate"` - Include an accurate total (slower, requires counting all matches)
- `at` (str, optional): Point-in-time snapshot (ISO datetime)
- `count` (int, optional): Number of results per page (alias for _count)
- `offset` (int, optional): Starting offset for pagination (alias for _offset)
- `sort` (str | list[str], optional): Sort field(s), prefix with - for descending
- `include` (str | list[str], optional): Related resources to include (_include)
- `include_iterate` (str | list[str], optional): Recursive includes (_include:iterate) - follows references on included resources
- `revinclude` (str | list[str], optional): Reverse includes (_revinclude)
- `revinclude_iterate` (str | list[str], optional): Recursive reverse includes (_revinclude:iterate)
- `return_bundle` (bool): Return FHIRBundle wrapper if True
- `as_fhir` (Type[Model], optional): Pydantic model class for typed resources

**Alias**: `searchWithOptions` - identical method with camelCase naming

**Returns**: dict or FHIRBundle

**Example**:
```python
from pymedplum.fhir import Patient

# Get just a count of matching resources
result = client.search_with_options("Patient", {"family": "Smith"}, summary="count")
print(f"Total patients: {result.get('total', 0)}")

# Request specific elements only
result = client.search_with_options(
    "Patient",
    {"active": "true"},
    elements=["id", "name", "birthDate"]
)

# Get accurate total count (may be slower)
bundle = client.search_with_options(
    "Patient",
    {"family": "Smith"},
    total="accurate",
    return_bundle=True
)
print(f"Accurate count: {bundle.total}")

# Point-in-time query (historical data)
result = client.search_with_options(
    "Patient",
    {"family": "Smith"},
    at="2024-01-01T00:00:00Z"
)

# Pagination and sorting with includes
bundle = client.search_with_options(
    "Observation",
    {"patient": "Patient/123"},
    count=50,
    offset=100,
    sort=["-date", "code"],
    include="Observation:patient",
    return_bundle=True,
    as_fhir=Observation
)
```

### GraphQL

#### `execute_graphql(query, variables=None, operation_name=None) -> dict`

Execute a GraphQL query.

**Parameters**:
- `query` (str): GraphQL query string
- `variables` (dict, optional): Query variables
- `operation_name` (str, optional): Operation name for multi-operation queries

**Returns**: dict - GraphQL response with data/errors

**Example**:
```python
query = """
query GetPatient($id: ID!) {
    Patient(id: $id) {
        id
        name { given family }
    }
}
"""
result = client.execute_graphql(query, variables={"id": "123"})
print(result["data"]["Patient"])
```

### Low-Level HTTP Methods

#### `get(path, **kwargs) -> dict | None`

Make a GET request to a Medplum API endpoint.

**Parameters**:
- `path` (str): API path (relative to base_url)
- `**kwargs`: Additional arguments for httpx.request

**Returns**: Parsed JSON response or None

#### `post(path, json=None, **kwargs) -> dict | None`

Make a POST request.

**Parameters**:
- `path` (str): API path
- `json` (dict, optional): JSON payload
- `**kwargs`: Additional httpx arguments

**Returns**: Parsed JSON response or None

#### `put(path, json=None, **kwargs) -> dict | None`

Make a PUT request (similar parameters to post).

#### `delete(path, **kwargs) -> dict | None`

Make a DELETE request (similar parameters to get).

### Context Managers

#### `on_behalf_of(membership) -> OnBehalfOfContext`

Create context manager for on-behalf-of operations.

**Parameters**:
- `membership` (str | ProjectMembership): ProjectMembership resource or ID

**Returns**: Context manager that sets X-Medplum-On-Behalf-Of header

**Example**:
```python
with client.on_behalf_of("ProjectMembership/123") as obo_client:
    # Operations here execute with the permissions of membership 123
    patient = obo_client.read_resource("Patient", "456")
```

### Multi-Tenant Accounts

#### `set_accounts(resource_ref, account_refs, *, propagate=False, prefer_async=False) -> dict`

Assign a resource to one or more accounts using Medplum's `$set-accounts` operation. Account assignments (stored in `meta.accounts`) drive compartment-based access control in multi-tenant MSO setups.

**Parameters**:
- `resource_ref` (str): Reference like `"Patient/123"`
- `account_refs` (str | list[str]): Account references to assign (typically Organizations or Practitioners)
- `propagate` (bool): If True, cascade assignments to all resources in the target's FHIR compartment (Observations, Encounters, etc.)
- `prefer_async` (bool): If True, send `Prefer: respond-async` header for large compartments

**Returns**: dict - FHIR Parameters with `resourcesUpdated` count, or the resource itself

**Example**:
```python
# Assign patient to an organization
client.set_accounts("Patient/123", "Organization/org-456")

# Multiple accounts with propagation to related resources
client.set_accounts(
    "Patient/123",
    ["Organization/org-456", "Practitioner/prac-789"],
    propagate=True,
)
```

#### `get_resource_accounts(resource) -> list[str]`

Return list of account reference strings from a resource's `meta.accounts`.

#### `resource_has_account(resource, account_ref) -> bool`

Check if a resource is assigned to a given account.

**Example**:
```python
from pymedplum import get_resource_accounts, resource_has_account

patient = client.read_resource("Patient", "123")
resource_has_account(patient, "Organization/org-456")  # True/False
get_resource_accounts(patient)  # ["Organization/org-456", ...]
```

### Terminology Operations

PyMedplum provides methods for FHIR terminology operations including ValueSet expansion, CodeSystem lookup, and ConceptMap translation.

#### `expand_valueset(valueset_url=None, valueset_id=None, filter=None, offset=None, count=None, include_designations=None, active_only=None, exclude_nested=None, exclude_not_for_ui=None, exclude_post_coordinated=None, display_language=None, property=None) -> dict`

Expand a ValueSet to get all matching codes.

**Parameters**:
- `valueset_url` (str, optional): Canonical URL of the ValueSet
- `valueset_id` (str, optional): ID of a specific ValueSet resource
- `filter` (str, optional): Text filter to apply (substring match on display)
- `offset` (int, optional): Starting index for paging (0-based)
- `count` (int, optional): Maximum number of concepts to return
- `include_designations` (bool, optional): Include code system designations
- `active_only` (bool, optional): Only include active codes
- `exclude_nested` (bool, optional): Exclude nested codes
- `exclude_not_for_ui` (bool, optional): Exclude codes marked as notSelectable
- `exclude_post_coordinated` (bool, optional): Exclude post-coordinated codes
- `display_language` (str, optional): Language for display text (e.g., "en", "de")
- `property` (list[str], optional): Properties to include for each concept

**Returns**: dict - Expanded ValueSet with contains array

**Example**:
```python
# Expand by URL
expansion = client.expand_valueset(
    valueset_url="http://hl7.org/fhir/ValueSet/observation-status"
)
for concept in expansion.get("expansion", {}).get("contains", []):
    print(f"{concept['code']}: {concept['display']}")

# Expand with filter and pagination
expansion = client.expand_valueset(
    valueset_url="http://hl7.org/fhir/ValueSet/condition-code",
    filter="diabetes",
    count=20,
    offset=0
)

# Expand a specific ValueSet by ID
expansion = client.expand_valueset(valueset_id="my-custom-valueset")
```

#### `lookup_concept(code, system=None, codesystem_id=None, version=None, coding=None, date=None, display_language=None, property=None) -> dict`

Look up details about a code in a CodeSystem.

**Parameters**:
- `code` (str): Code to look up
- `system` (str, optional): Code system URL (required unless using codesystem_id)
- `codesystem_id` (str, optional): ID of a specific CodeSystem resource
- `version` (str, optional): Specific version of the code system
- `coding` (dict, optional): Full Coding object (alternative to code+system)
- `date` (str, optional): Date for which the code should be valid
- `display_language` (str, optional): Language for display text
- `property` (list[str], optional): Properties to return for the code

**Returns**: dict - Parameters resource with code details (name, display, version, etc.)

**Example**:
```python
# Look up a LOINC code
result = client.lookup_concept(
    code="8867-4",
    system="http://loinc.org"
)

# Extract display name from parameters
for param in result.get("parameter", []):
    if param.get("name") == "display":
        print(f"Display: {param.get('valueString')}")

# Look up with specific properties
result = client.lookup_concept(
    code="38341003",
    system="http://snomed.info/sct",
    property=["parent", "child", "designation"]
)
```

#### `translate_concept(code=None, system=None, conceptmap_url=None, conceptmap_id=None, version=None, source=None, target=None, coding=None, codeable_concept=None, target_system=None, reverse=None) -> dict`

Translate a code from one code system to another using a ConceptMap.

**Parameters**:
- `code` (str, optional): Code to translate
- `system` (str, optional): Source code system URL
- `conceptmap_url` (str, optional): Canonical URL of the ConceptMap
- `conceptmap_id` (str, optional): ID of a specific ConceptMap resource
- `version` (str, optional): Version of the ConceptMap
- `source` (str, optional): Source value set URL (filter for mappings)
- `target` (str, optional): Target value set URL (filter for mappings)
- `coding` (dict, optional): Full Coding object (alternative to code+system)
- `codeable_concept` (dict, optional): CodeableConcept to translate
- `target_system` (str, optional): Target code system URL
- `reverse` (bool, optional): Reverse the direction of the mapping

**Returns**: dict - Parameters resource with translation results

**Example**:
```python
# Translate using a ConceptMap URL
result = client.translate_concept(
    code="final",
    system="http://hl7.org/fhir/observation-status",
    conceptmap_url="http://example.org/ConceptMap/status-mapping",
    target_system="http://example.org/local-codes"
)

# Check if translation found matches
for param in result.get("parameter", []):
    if param.get("name") == "result" and param.get("valueBoolean"):
        print("Translation found!")
    elif param.get("name") == "match":
        for part in param.get("part", []):
            if part.get("name") == "concept":
                coding = part.get("valueCoding", {})
                print(f"Mapped to: {coding.get('code')} ({coding.get('display')})")

# Translate using a specific ConceptMap by ID
result = client.translate_concept(
    code="active",
    system="http://hl7.org/fhir/patient-status",
    conceptmap_id="my-status-map"
)
```

## Asynchronous Client (`AsyncMedplumClient`)

The `AsyncMedplumClient` provides the same methods as `MedplumClient`, but all methods are `async` and must be awaited.

**Example**:
```python
from pymedplum.async_client import AsyncMedplumClient

async def main():
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        access_token="YOUR_TOKEN"
    ) as client:
        # All methods are async
        patient = await client.read_resource("Patient", "123")
        
        # Async iteration for search
        async for obs in client.search_resource_pages("Observation", {"patient": "Patient/123"}):
            print(obs["id"])
```

### Key Differences

- All methods are `async def` and must be `await`ed
- `search_resource_pages` returns an async iterator (use `async for`)
- Use `async with` for the `on_behalf_of` context manager
- The client itself supports `async with` for automatic cleanup

## Error Handling

All client methods may raise these exceptions:

- `AuthenticationError` (401): Invalid or expired credentials
- `AuthorizationError` (403): Insufficient permissions
- `NotFoundError` (404): Resource not found
- `BadRequestError` (400): Invalid request data
- `PreconditionFailedError` (412): Precondition failed (e.g., `If-Match` version conflict during optimistic locking)
- `RateLimitError` (429): Too many requests
- `ServerError` (500+): Server-side issues
- `OperationOutcomeError`: FHIR operation outcome errors
- `NetworkError`: Connection/network issues

**Example**:
```python
from pymedplum.exceptions import NotFoundError, AuthorizationError

try:
    patient = client.read_resource("Patient", "nonexistent-id")
except NotFoundError:
    print("Patient not found")
except AuthorizationError:
    print("Access denied")
```

## Next Steps

- See [Advanced Usage](advanced_usage.md) for GraphQL, patching, and administrative features
- Review [Utility Functions](utils.md) for helper methods
- Check [FHIR Models](fhir_models.md) for working with Pydantic models
