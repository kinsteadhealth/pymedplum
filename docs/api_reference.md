# Client API Reference

This page provides a comprehensive reference for all methods available on the `MedplumClient` and `AsyncMedplumClient`.

## Synchronous Client (`MedplumClient`)

### Constructor

```python
MedplumClient(
    base_url: str = "https://api.medplum.com/",
    *,
    client_id: str | None = None,
    client_secret: str | None = None,
    access_token: str | None = None,
    project_id: str | None = None,
    fhir_url_path: str = "fhir/R4/",
    timeout: float = 30.0,
    http_client: httpx.Client | None = None,
    before_request: BeforeRequestHook | None = None,
    on_request_complete: OnRequestCompleteHook | None = None,
    allow_insecure_http: bool = False,
    failed_refresh_cooldown: float = 1.0,
    default_on_behalf_of: str | None = None,
)
```

All arguments except `base_url` are keyword-only. Unknown kwargs raise
`TypeError` at construction time.

**Parameters**:

- `base_url` (str): Medplum base URL. Defaults to
  `https://api.medplum.com/`. Must be `https://` unless it points at
  a loopback address or `allow_insecure_http=True` is passed.
- `client_id`, `client_secret` (str | None): OAuth client credentials.
  When both are set, the client uses the client-credentials flow with
  automatic refresh.
- `access_token` (str | None): Pre-obtained bearer token. Use instead
  of `client_id`/`client_secret` for externally-managed tokens.
- `project_id` (str | None): Optional Medplum project scope.
- `fhir_url_path` (str): FHIR path prefix under `base_url`. Default
  `fhir/R4/`.
- `timeout` (float): Per-request httpx timeout in seconds.
- `http_client` (httpx.Client | None): Caller-supplied httpx client.
  Must be constructed with `follow_redirects=False` — the SDK rejects
  clients that auto-follow redirects to prevent auth-header leaks to
  unexpected origins.
- `before_request` (`BeforeRequestHook | None`): Hook that receives a
  sanitized `PreparedRequest` and may return a modified copy. See
  the [Hooks](#hooks) section for the contract.
- `on_request_complete` (`OnRequestCompleteHook | None`): Hook that
  receives a `RequestEvent` once per logical SDK call. Typically
  wired to a PHI-access audit log — see
  [Audit Logging](advanced/audit_logging.md).
- `allow_insecure_http` (bool): Opt-in to plain `http://` base URLs
  for non-loopback hosts. Defaults to `False`. Logs a WARNING when
  enabled.
- `failed_refresh_cooldown` (float): Seconds to cool down after a
  token-refresh failure. Additional refreshes during the cooldown
  window raise `TokenRefreshCooldownError` instead of hammering the
  OAuth endpoint. Default `1.0`.
- `default_on_behalf_of` (str | None): Baseline OBO membership for
  every request made by this client. Overridden by the
  `client.on_behalf_of(...)` context manager and by per-call
  `on_behalf_of=` kwargs. See [On-Behalf-Of](advanced/on_behalf_of.md)
  for precedence rules.

### Authentication

The client authenticates lazily on the first request using the
client-credentials flow and refreshes proactively before expiration.
There is no public `authenticate()` method — construct the client
with `client_id` / `client_secret` and make a request; the SDK
handles token acquisition and refresh internally.

On a `401` response the client force-refreshes the token and replays
the request once. After a refresh failure the client enters a short
cooldown window (see `failed_refresh_cooldown`); further refreshes
during that window raise `TokenRefreshCooldownError`.

### Resource Operations

#### `create_resource(resource, *, headers=None, accounts=None, as_fhir=None, on_behalf_of=None) -> dict | Model`

Create a new FHIR resource.

**Parameters**:
- `resource` (dict | Pydantic model): The resource to create
- `headers` (dict[str, str], optional): Additional HTTP headers for the request
- `accounts` (str | list[str], optional): Account references to set on `meta.accounts` at creation time for multi-tenant compartment assignment
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. `None` (default) uses ambient OBO (context manager or client default); empty string clears it for this call. See [On-Behalf-Of](advanced/on_behalf_of.md) for precedence rules.

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

#### `create_resource_if_none_exist(resource, if_none_exist, *, headers=None, accounts=None, as_fhir=None, on_behalf_of=None) -> dict | Model`

Conditionally create a FHIR resource only if no matching resource exists (If-None-Exist).

This method uses FHIR's conditional create mechanism via the `If-None-Exist` header. If a resource matching the search criteria already exists, the existing resource is returned (HTTP 200). If no match is found, a new resource is created (HTTP 201).

**Parameters**:
- `resource` (dict | Pydantic model): The resource to create
- `if_none_exist` (str): FHIR search query string (e.g., "identifier=MRN|12345"). Accepts plain query strings or strings with a leading `?` (which is automatically stripped). Same-origin absolute URLs are accepted and the query portion is extracted (with a warning); cross-origin URLs are rejected as `UnsafeRedirectError`.
- `headers` (dict[str, str], optional): Additional HTTP headers for the request
- `accounts` (str | list[str], optional): Account references to set on `meta.accounts` at creation time
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. See `create_resource` above.

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

#### `read_resource(resource_type, resource_id, as_fhir=None, *, headers=None, on_behalf_of=None) -> dict | Model`

Read a FHIR resource by type and ID.

**Parameters**:
- `resource_type` (str): FHIR resource type (e.g., "Patient")
- `resource_id` (str): Resource ID
- `as_fhir` (Type[Model], optional): Pydantic model class to return
- `headers` (dict[str, str], optional): Additional HTTP headers for the request
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: dict or Pydantic model instance

**Raises**:
- `NotFoundError`: If resource doesn't exist

**Example**:
```python
from pymedplum.fhir import Patient

# Get as dictionary
patient_dict = client.read_resource("Patient", "123")

# Get as typed model
patient = client.read_resource("Patient", "123", as_fhir=Patient)
print(patient.name[0].family)  # Type-safe access
```

#### `vread_resource(resource_type, resource_id, version_id, as_fhir=None, *, headers=None, on_behalf_of=None) -> dict | Model`

Read a specific historical version of a FHIR resource (`vread`).

**Parameters**:
- `resource_type` (str): FHIR resource type (e.g., "Patient")
- `resource_id` (str): Resource ID
- `version_id` (str): Version ID (found in `meta.versionId`)
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response
- `headers` (dict[str, str], optional): Additional HTTP headers for the request
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: dict or Pydantic model instance - The resource at the given version

**Example**:
```python
from pymedplum.fhir import Patient

# Read a specific version
patient_v1 = client.vread_resource("Patient", "123", "1")

# Type-safe versioned read
patient_v1 = client.vread_resource("Patient", "123", "1", as_fhir=Patient)
```

#### `update_resource(resource, *, headers=None, accounts=None, as_fhir=None, on_behalf_of=None, if_match=True) -> dict | Model`

Update an existing FHIR resource (requires id).

**Parameters**:
- `resource` (dict | Pydantic model): Resource with id field
- `headers` (dict[str, str], optional): Additional HTTP headers for the request. An explicit `If-Match` in `headers` always wins over the `if_match` keyword.
- `accounts` (str | list[str], optional): Account references to set on `meta.accounts`
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. See [On-Behalf-Of](advanced/on_behalf_of.md).
- `if_match` (bool | str, keyword-only, default `True`): Optimistic-concurrency control.
  - `True` (default): auto-attach `If-Match: W/"<versionId>"` from `resource.meta.versionId` if present. If the resource has no versionId, no header is attached.
  - `False`: opt out of If-Match entirely (last-write-wins behavior).
  - `str`: sent verbatim as the `If-Match` header value.

**Returns**: dict or Pydantic model instance - The updated resource

**Raises**:
- `ValueError`: If resource lacks resourceType or id
- `TypeError`: If `if_match` is neither `bool` nor `str`
- `PreconditionFailedError`: If the attached `If-Match` version doesn't match the server's current resource version

**Example**:
```python
from pymedplum.fhir import Patient

# Default behavior: If-Match auto-attaches from meta.versionId.
patient = client.read_resource("Patient", "123", as_fhir=Patient)
patient.active = False
updated = client.update_resource(patient)

# Opt out for last-write-wins semantics.
updated = client.update_resource(patient, if_match=False)

# Or pass a custom If-Match value.
updated = client.update_resource(patient, if_match='W/"5"')

# Handle version conflicts from concurrent updates.
try:
    updated = client.update_resource(patient)
except PreconditionFailedError:
    patient = client.read_resource("Patient", "123", as_fhir=Patient)
    # re-apply changes, then retry
```

#### `patch_resource(resource_type, resource_id, operations, *, headers=None, as_fhir=None, on_behalf_of=None) -> dict | Model`

Apply JSON Patch operations to a resource.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `resource_id` (str): Resource ID
- `operations` (list[PatchOperation]): JSON Patch operations
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)
- `as_fhir` (Type[Model], optional): Pydantic model class to return for typed response
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. See [On-Behalf-Of](advanced/on_behalf_of.md).

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

#### `delete_resource(resource_type, resource_id, *, headers=None, on_behalf_of=None) -> None`

Delete a FHIR resource. Per the FHIR specification, successful deletion returns HTTP 204 No Content with no response body.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `resource_id` (str): Resource ID
- `headers` (dict[str, str], optional): Additional HTTP headers for the request (e.g., `If-Match` for optimistic locking)
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. See [On-Behalf-Of](advanced/on_behalf_of.md).

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

#### `search_resources(resource_type, query=None, return_bundle=False, as_fhir=None, *, on_behalf_of=None) -> dict | FHIRBundle`

Search for FHIR resources.

**Parameters**:
- `resource_type` (str): FHIR resource type to search
- `query` (dict | list[tuple], optional): Search parameters
- `return_bundle` (bool): Return FHIRBundle wrapper if True
- `as_fhir` (Type[Model], optional): Pydantic model class for typed resources (only applies when return_bundle=True)
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. See [On-Behalf-Of](advanced/on_behalf_of.md).

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

#### `search_one(resource_type, query=None, *, on_behalf_of=None) -> dict | None`

Search for a single resource (limit 1).

**Parameters**:
- `resource_type` (str): Type of resource to search
- `query` (dict | list[tuple], optional): Search parameters
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: First matching resource or None

**Example**:
```python
patient = client.search_one("Patient", {"identifier": "MRN|12345"})
if patient:
    print(f"Found: {patient['id']}")
```

#### `search_resource_pages(resource_type, query=None, as_fhir=None, *, on_behalf_of=None) -> Iterator[dict | Model]`

Search resources with automatic pagination.

**Parameters**:
- `resource_type` (str): FHIR resource type
- `query` (dict | list[tuple], optional): Search parameters
- `as_fhir` (Type[Model], optional): Pydantic model class for typed resources
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

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

#### `search_with_options(resource_type, query=None, *, summary=None, elements=None, total=None, at=None, count=None, offset=None, sort=None, include=None, include_iterate=None, revinclude=None, revinclude_iterate=None, return_bundle=False, as_fhir=None, on_behalf_of=None) -> dict | FHIRBundle`

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
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

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

### Bundle Operations

#### `execute_batch(bundle, *, accounts=None, on_behalf_of=None) -> dict`

Execute a FHIR batch bundle. Each entry is executed independently; failures in one entry do not roll back the rest.

**Parameters**:
- `bundle` (dict | Pydantic model): FHIR Bundle resource
- `accounts` (str | list[str], optional): Account references to set on each bundle entry's `meta.accounts`
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: dict - Bundle of type `batch-response`

#### `execute_transaction(bundle, *, on_behalf_of=None) -> dict`

Execute a FHIR transaction bundle atomically. All operations succeed or fail together. Use `urn:uuid:` placeholders to reference resources created within the bundle.

**Parameters**:
- `bundle` (dict | Pydantic model): Bundle with `type="transaction"` (coerced if missing)
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: dict - Bundle of type `transaction-response`

### GraphQL

#### `execute_graphql(query, variables=None, *, on_behalf_of=None) -> dict`

Execute a GraphQL query.

**Parameters**:
- `query` (str): GraphQL query string
- `variables` (dict, optional): Query variables
- `on_behalf_of` (str | None, keyword-only): Per-call OBO override. `None` (default) uses ambient OBO (context manager or client default); empty string clears it for this call. See [On-Behalf-Of](advanced/on_behalf_of.md) for precedence rules.

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

Create a context manager that sets the ambient OBO membership for
the client. Exiting the block restores the prior ambient value.

**Parameters**:
- `membership` (str | ProjectMembership): ProjectMembership resource or ID

**Returns**: Context manager that sets `X-Medplum-On-Behalf-Of` on every
request within its scope

**Example**:
```python
with client.on_behalf_of("ProjectMembership/123"):
    patient = client.read_resource("Patient", "456")
```

OBO has a defined precedence order across per-call kwargs, the
context manager, and the client default. See
[On-Behalf-Of](advanced/on_behalf_of.md) for the full precedence
rules, per-client isolation guarantees, and the
`ThreadPoolExecutor` propagation caveat.

### Multi-Tenant Accounts

#### `set_accounts(resource_ref, account_refs, *, propagate=False, prefer_async=False) -> dict`

Assign a resource to one or more accounts using Medplum's `$set-accounts` operation. Account assignments (stored in `meta.accounts`) drive compartment-based access control in multi-tenant MSO setups.

**Parameters**:
- `resource_ref` (str): Reference like `"Patient/123"`
- `account_refs` (str | list[str]): Account references to assign (typically Organizations or Practitioners)
- `propagate` (bool): If True, cascade assignments to all resources in the target's FHIR compartment (Observations, Encounters, etc.)
- `prefer_async` (bool): If True, send `Prefer: respond-async` header. Only takes effect when `propagate` is also True. Server returns an OperationOutcome with the async job URL in `issue[0].diagnostics`.

**Returns**: Synchronous: FHIR Parameters with `resourcesUpdated` count. Async (202): OperationOutcome with job URL in `issue[0].diagnostics`.

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

### Async Jobs

#### `get_async_job_status(job) -> dict`

Get the current status of an async job.

**Parameters**:
- `job` (str | dict | OperationOutcome): Job ID, full status URL, OperationOutcome dict, or OperationOutcome Pydantic model

**Returns**: AsyncJob resource with current status

**Example**:
```python
# Check once without waiting
job = client.get_async_job_status(result)
if job["status"] == "completed":
    print(job["output"])
elif job["status"] in ("accepted", "active"):
    print("Still running")
```

#### `wait_for_async_job(job, poll_interval=1.0, timeout=None) -> dict`

Poll an async job until it reaches a terminal state.

**Parameters**:
- `job` (str | dict | OperationOutcome): Same as `get_async_job_status`
- `poll_interval` (float): Seconds between polls (default: 1.0)
- `timeout` (float | None): Maximum seconds to wait (default: None = indefinite)

**Returns**: AsyncJob resource with final status

**Raises**: `TimeoutError` if timeout is reached

**Example**:
```python
# Start an async operation
result = client.set_accounts(
    "Patient/123", "Organization/org-456",
    propagate=True, prefer_async=True,
)

# Wait for completion — accepts the OperationOutcome directly
job = client.wait_for_async_job(result, timeout=60)
print(job["status"])  # "completed"
print(job["output"])  # Parameters with resourcesUpdated
```

### Binary & Document Export

#### `upload_binary(content, content_type, *, on_behalf_of=None) -> dict`

Upload raw binary content (PDF, image, XML, etc.) as a FHIR `Binary` resource.

**Parameters**:
- `content` (bytes): Binary content
- `content_type` (str): MIME type (e.g., `"application/pdf"`)
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: dict - The created `Binary` resource

**Example**:
```python
with open("document.pdf", "rb") as f:
    binary = client.upload_binary(f.read(), "application/pdf")
```

#### `download_binary(binary_id, *, on_behalf_of=None) -> bytes`

Download raw bytes for a `Binary` resource.

**Parameters**:
- `binary_id` (str): ID of the `Binary` resource
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: bytes - Raw content

**Example**:
```python
content = client.download_binary("binary-123")
```

#### `export_ccda(patient_id, *, on_behalf_of=None) -> str`

Export a patient's complete record as a C-CDA XML document via `Patient/{id}/$ccda-export`.

**Parameters**:
- `patient_id` (str): ID of the patient to export
- `on_behalf_of` (str, optional): ProjectMembership reference to act on behalf of for this call. See [On-Behalf-Of](advanced/on_behalf_of.md).

**Returns**: str - C-CDA XML document

**Example**:
```python
ccda_xml = client.export_ccda("patient-123")
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

## Hooks

PyMedplum exposes two public extension points on the constructor:
`before_request` (request mutation) and `on_request_complete`
(completion dispatch, typically wired to a PHI audit log).

### Type aliases

```python
from pymedplum.hooks import (
    BeforeRequestHook,
    OnRequestCompleteHook,
    PreparedRequest,
    RequestAttempt,
    RequestEvent,
)

BeforeRequestHook = Callable[[PreparedRequest], PreparedRequest | None]
OnRequestCompleteHook = Callable[[RequestEvent], None]
```

`AsyncMedplumClient` additionally accepts an async-callable
`on_request_complete`:

```python
from collections.abc import Awaitable, Callable

AsyncOnRequestCompleteHook = Callable[[RequestEvent], Awaitable[None]]
```

Passing an async hook to the synchronous `MedplumClient` raises
`TypeError` at construction.

### `PreparedRequest`

Frozen dataclass presented to a `before_request` hook. Hooks may
return `None` (no mutation) or a new `PreparedRequest` with
adjusted fields. The SDK sanitizes the return value — it strips
`Authorization` headers and enforces same-origin URL mutations.

| Field | Type | Notes |
|---|---|---|
| `method` | `str` | HTTP verb. May be changed only to a safe alternative. |
| `url` | `str` | Full wire URL. Hook mutations must stay same-origin. |
| `headers` | `dict[str, str]` | Pre-redacted: bearer token and OBO header are not present. |
| `json_body` | `Any \| None` | Parsed JSON body, if any. |

### `RequestAttempt`

Per-wire attempt record.

| Field | Type | Notes |
|---|---|---|
| `attempt_number` | `int` | 1-based. |
| `status_code` | `int \| None` | `None` on network exceptions. |
| `duration_seconds` | `float` | Wall-clock for this attempt. |
| `on_behalf_of` | `str \| None` | Membership sent on this attempt. Always `None` for `/oauth2/token` attempts. |
| `exception` | `BaseException \| None` | Raised exception, if any. |

### `RequestEvent`

Fires once per logical SDK call. See
[Audit Logging](advanced/audit_logging.md) for the full field
reference, PHI notes, and worked examples.

Key methods:

```python
event.to_phi_audit_dict()                              # PHI-bearing; for HIPAA-approved audit sinks
event.to_phi_audit_dict(include_query_params=True)     # also includes parsed search params
event.to_non_phi_dict()                                # shape-only; for metrics / general observability
```

### Hook failure semantics

- `on_request_complete` exceptions are caught and logged at
  WARNING under `pymedplum.hooks`. They never propagate to the
  caller.
- `before_request` return values that violate the sanitization
  rules (cross-origin URL, injected auth headers) are logged at
  WARNING and discarded; the original request proceeds.

## Exceptions

The full public exception tree, all re-exported at
`pymedplum.*` and available under `pymedplum.exceptions.*`.

| Exception | Raised when |
|---|---|
| `MedplumError` | Base class for every SDK exception. |
| `AuthenticationError` | 401 Unauthorized, or credentials-flow failure. |
| `AuthorizationError` | 403 Forbidden. |
| `NotFoundError` | 404 Not Found. |
| `BadRequestError` | 400 Bad Request. |
| `PreconditionFailedError` | 412 Precondition Failed (If-Match / If-None-Exist mismatch). |
| `RateLimitError` | 429 Too Many Requests. |
| `ServerError` | 5xx. String form omits the response body; access `exc.response` for the raw body, or `exc.sanitize_for_logging()` for a safe dict. |
| `OperationOutcomeError` | FHIR OperationOutcome returned with non-success issues. String form omits `diagnostics` / `details.text`; access `exc.outcome` or `exc.sanitize_for_logging()`. |
| `ValidationError` | Resource validation failure (surfaced from 400s that carry OperationOutcome). |
| `NetworkError` | Connection/timeout/DNS failure. |
| `InsecureTransportError` | Constructor received a non-`https://` URL without `allow_insecure_http=True` and without a loopback host. |
| `UnsafeRedirectError` | Follow-up URL (pagination, async job polling, `if_none_exist` absolute URL) is outside the configured origin. |
| `TokenRefreshCooldownError` | Token refresh attempted during the cooldown window after a prior refresh failure. Has `retry_after: float` (seconds). |

### Safe logging pattern

`ServerError` and `OperationOutcomeError` both provide
`sanitize_for_logging()`, which returns a PHI-safe dict (no
response body, no `diagnostics`, no `details.text`). Prefer this
over `str(exc)` or `repr(exc)` in logs:

```python
import logging

from pymedplum import OperationOutcomeError, ServerError

log = logging.getLogger(__name__)

try:
    patient = client.read_resource("Patient", "123")
except (OperationOutcomeError, ServerError) as exc:
    log.warning("medplum_call_failed", extra=exc.sanitize_for_logging())
    raise
```

### Handling `TokenRefreshCooldownError`

The cooldown exists to prevent hammering an OAuth endpoint that
has already failed. **Do not catch and retry in a tight loop.**
Surface the error to your caller and respect `retry_after`:

```python
from pymedplum import TokenRefreshCooldownError

try:
    patient = client.read_resource("Patient", "123")
except TokenRefreshCooldownError as exc:
    # Transient auth failure — push back and let a higher layer
    # decide when to retry.
    raise TransientAuthError(retry_after=exc.retry_after) from exc
```

## Error-handling example

```python
from pymedplum import (
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

try:
    patient = client.read_resource("Patient", "nonexistent-id")
except NotFoundError:
    ...
except AuthorizationError:
    ...
except ValidationError:
    ...
except RateLimitError:
    ...
```

## Next Steps

- See [Advanced Usage](advanced_usage.md) for GraphQL, patching, and administrative features
- Review [Utility Functions](utils.md) for helper methods
- Check [FHIR Models](fhir_models.md) for working with Pydantic models
- Read [Audit Logging](advanced/audit_logging.md) for the `on_request_complete` hook contract
