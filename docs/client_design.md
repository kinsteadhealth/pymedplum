# Client Method Design

The `MedplumClient` and `AsyncMedplumClient` are designed to be flexible and developer-friendly, catering to both traditional dictionary-based workflows and modern, type-safe Pydantic model-based workflows. This is achieved through the use of method overloading.

## Universal Input: Dicts and Pydantic Models

For write operations, you can provide the resource data as either a standard Python dictionary or as an initialized Pydantic model instance. The client handles the conversion automatically.

### `create_resource(resource)`
-   **Accepts**: `dict` or a Pydantic model instance.
-   **Returns**: A dictionary of the created resource.

```python
from pymedplum.fhir import Patient

patient_dict = {
    "resourceType": "Patient",
    "name": [{"given": ["John"], "family": "Dict"}],
}
created_from_dict = client.create_resource(patient_dict)

patient_model = Patient(name=[{"given": ["Jane"], "family": "Model"}])
created_from_model = client.create_resource(patient_model)
```

### `update_resource(resource)`
`update_resource` also accepts both formats, and by default attaches
an `If-Match` header from `resource.meta.versionId` for optimistic
concurrency control.

```python
patient_model.active = False
client.update_resource(patient_model)             # default: If-Match on
client.update_resource(patient_model, if_match=False)      # opt out
client.update_resource(patient_model, if_match='W/"5"')    # custom
```

## Flexible Output: Dicts vs. Typed Models

For read operations, you can choose the format of the returned data. By default, you get a dictionary; pass `as_fhir=` to request a fully-typed Pydantic model for a better development experience.

### `read_resource(resource_type, id, as_fhir=...)`
The `as_fhir` parameter controls the return type.

-   **`as_fhir=None` (default)**: Returns a `dict`.
-   **`as_fhir=Patient` (or any model class)**: Returns an instance of that Pydantic model.

```python
from pymedplum.fhir import Patient

patient_dict = client.read_resource("Patient", "some-id")
print(patient_dict["name"][0]["family"])

patient_model = client.read_resource("Patient", "some-id", as_fhir=Patient)
print(patient_model.name[0].family)
```

## Search Result Helpers

### `search_resources(..., return_bundle=...)`
The `search_resources` method can return either a raw bundle dictionary or a helpful `FHIRBundle` wrapper object.

-   **`return_bundle=False` (default)**: Returns a `dict` representing the FHIR Bundle.
-   **`return_bundle=True`**: Returns an instance of `FHIRBundle`, which provides helpful methods for iteration and type conversion.

```python
from pymedplum.fhir import Patient

bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True)

for resource_dict in bundle:
    print(resource_dict["id"])

patients = bundle.get_resources_typed(Patient)
for p in patients:
    print(p.birth_date)
```

This design lets dictionary-based code and Pydantic-forward code coexist in the same codebase, at the granularity of a single call.

## On-Behalf-Of (OBO)

OBO is a design invariant of the client, not an afterthought. The
client resolves the acting `ProjectMembership` in a fixed precedence
order for every request:

1. **Per-call kwarg** — `method(..., on_behalf_of=...)` wins if passed.
   An empty-string kwarg clears ambient state for that one call.
2. **Context manager** — `with client.on_behalf_of(...)` sets an
   ambient value for its scope. Uses a per-instance `ContextVar` (with
   a UUID suffix in the name) so two clients in the same process never
   observe each other's state — even when rapidly constructed and
   garbage-collected.
3. **Client default** — `default_on_behalf_of=` on the constructor is
   the baseline for the client's lifetime.
4. **None** — no `X-Medplum-On-Behalf-Of` header is sent.

Async tasks sharing one client each see only their own context, per
standard `ContextVar` semantics. Threaded code must copy the context
explicitly (`contextvars.copy_context`) or use `asyncio.to_thread`;
plain `ThreadPoolExecutor.submit` does not propagate. See
[On-Behalf-Of](advanced/on_behalf_of.md) for worked examples.

## Retry and throttling

The client retries transient failures with capped exponential backoff.
Two invariants worth knowing:

- **429 handling** parses `Retry-After` (both seconds and HTTP-date
  forms) and respects the server-supplied delay, capped by
  `MAX_RETRY_DELAY_SECONDS` to avoid pathological pauses.
- **Token-refresh cooldown.** If an OAuth refresh fails, the client
  enters a cooldown window (default 1 second, configurable with
  `failed_refresh_cooldown=`). Additional calls that would trigger a
  refresh during the window raise `TokenRefreshCooldownError` with a
  `retry_after` attribute, rather than hammering the token endpoint.
  Refreshes are coordinated single-flight: one in-flight refresh
  serves every concurrent caller, with correct exception propagation.

## Transport security

- **HTTPS by default.** A non-`https://` `base_url` raises
  `InsecureTransportError` at construction unless the host is loopback
  (`127.0.0.1`, `::1`, `localhost`) or `allow_insecure_http=True` is
  passed (logs a WARNING).
- **No auto-follow redirects.** The client is constructed with
  `follow_redirects=False` and rejects caller-supplied `httpx.Client`
  instances that auto-follow. Pagination and async-job polling
  explicitly validate same-origin URLs; cross-origin follow-ups raise
  `UnsafeRedirectError`.

## Hooks

Two public extension points are exposed on the constructor:

- **`before_request`** — receives a frozen `PreparedRequest` with
  pre-redacted headers (bearer token and OBO header already stripped)
  and may return a modified copy. Return values are sanitized: any
  `Authorization` header is stripped, and cross-origin URL mutations
  are rejected and logged at WARNING.
- **`on_request_complete`** — fires once per logical SDK call
  (retries folded into `event.attempts`) with a `RequestEvent`
  dataclass. Intended for PHI-access audit logging. The sync hook
  signature is accepted by both clients; an async hook is only valid
  on `AsyncMedplumClient` (the sync client raises `TypeError` at
  construction). Hook exceptions are caught and logged at WARNING
  under `pymedplum.hooks`; they never fail the calling request.

See [Audit Logging](advanced/audit_logging.md) for the full
`on_request_complete` contract and worked examples.
