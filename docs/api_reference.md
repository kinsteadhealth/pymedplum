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

#### `create_resource(resource, org_mode=None, org_ref=None, headers=None) -> dict`

Create a new FHIR resource.

**Parameters**:
- `resource` (dict | Pydantic model): The resource to create
- `org_mode` (OrgMode, optional): Override client org_mode for this request
- `org_ref` (str, optional): Override client org_ref for this request
- `headers` (dict[str, str], optional): Additional HTTP headers for the request

**Returns**: dict - The created resource with server-assigned ID

**Example**:
```python
from pymedplum.fhir.patient import Patient

# Using Pydantic model
patient = Patient(name=[{"family": "Smith", "given": ["John"]}])
created = client.create_resource(patient)
print(f"Created patient with ID: {created['id']}")

# Using dictionary
patient_dict = {"resourceType": "Patient", "active": True}
created = client.create_resource(patient_dict)

# With custom headers
created = client.create_resource(patient, headers={"X-Custom-Header": "value"})
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

#### `update_resource(resource, org_mode=None, org_ref=None, headers=None) -> dict`

Update an existing FHIR resource (requires id).

**Parameters**:
- `resource` (dict | Pydantic model): Resource with id field
- `org_mode` (OrgMode, optional): Override client org_mode
- `org_ref` (str, optional): Override client org_ref
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)

**Returns**: dict - The updated resource

**Raises**:
- `ValueError`: If resource lacks resourceType or id
- `PreconditionFailedError`: If `If-Match` header version doesn't match current resource version

**Example**:
```python
# Read, modify, update pattern
patient = client.read_resource("Patient", "123", as_fhir=Patient)
patient.active = False
updated = client.update_resource(patient)

# With optimistic locking to prevent concurrent modifications
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]
patient["active"] = False
try:
    updated = client.update_resource(patient, headers={"If-Match": f'W/"{version}"'})
except PreconditionFailedError:
    # Resource was modified by another process - refetch and retry
    patient = client.read_resource("Patient", "123")
```

#### `patch_resource(resource_type, resource_id, operations, headers=None) -> dict`

Apply JSON Patch operations to a resource.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `resource_id` (str): Resource ID
- `operations` (list[PatchOperation]): JSON Patch operations
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)

**Returns**: dict - The patched resource

**Raises**:
- `PreconditionFailedError`: If `If-Match` header version doesn't match current resource version

**Example**:
```python
operations = [
    {"op": "replace", "path": "/active", "value": False},
    {"op": "add", "path": "/telecom/-", "value": {"system": "email", "value": "new@example.com"}}
]
patched = client.patch_resource("Patient", "123", operations)

# With optimistic locking
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]
patched = client.patch_resource(
    "Patient", "123", operations,
    headers={"If-Match": f'W/"{version}"'}
)
```

#### `delete_resource(resource_type, resource_id, headers=None) -> None`

Delete a FHIR resource.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `resource_id` (str): Resource ID
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)

**Returns**: None

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
