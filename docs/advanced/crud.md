# CRUD & Concurrency

This page covers non-trivial CRUD patterns: patching, optimistic locking, and safe concurrent updates.

## Update a resource

`update_resource` overwrites the existing resource.

```python
patient = client.read_resource("Patient", "123")
patient["active"] = False
updated_patient = client.update_resource(patient)
```

## Patch a resource

Use JSON Patch for partial updates:

```python
patient_id = "some-patient-id"
patch_operations = [
    {"op": "replace", "path": "/gender", "value": "other"},
    {"op": "add", "path": "/telecom/-", "value": {"system": "email", "value": "new@example.com"}},
]

patched_patient = client.patch_resource(
    "Patient",
    patient_id,
    patch_operations,
)
```

## Optimistic locking (`If-Match`)

Optimistic locking prevents lost updates when multiple clients edit the same resource.

`update_resource` attaches `If-Match: W/"<versionId>"` from
`resource.meta.versionId` **by default** (`if_match=True`), so the
normal read-modify-write pattern is concurrency-safe out of the box:

```python
from pymedplum.exceptions import PreconditionFailedError

patient = client.read_resource("Patient", "123")
patient["active"] = False

try:
    updated = client.update_resource(patient)  # If-Match auto-attached
except PreconditionFailedError:
    print("Conflict detected - resource was modified elsewhere")
```

The `if_match` keyword covers the other cases:

```python
# Strict: raise MissingVersionIdError instead of silently writing
# unguarded when the resource has no meta.versionId.
client.update_resource(patient, if_match="required")

# Explicit ETag carried from elsewhere.
client.update_resource(patient, if_match='W/"42"')

# Opt out (last-write-wins) — only when you mean it.
client.update_resource(patient, if_match=False)
```

> **The `if_match=True` default has a silent gap:** a resource without
> `meta.versionId` sends no `If-Match` header at all — an unguarded
> write. Use `if_match="required"` when that degradation must be an
> error (`MissingVersionIdError`) rather than a lost-update window.

### Patching with optimistic locking

`patch_resource` has no resource to read a versionId from, so it takes
an explicit ETag via `if_match`:

```python
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]

operations = [{"op": "replace", "path": "/active", "value": False}]

patched = client.patch_resource(
    "Patient",
    "123",
    operations,
    if_match=f'W/"{version}"',
)
```

### Deleting with optimistic locking

```python
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]

client.delete_resource(
    "Patient",
    "123",
    headers={"If-Match": f'W/"{version}"'},
)
```

## Read-modify-write with retry (`update_with_retry`)

Hand-rolling the read → mutate → `If-Match` write → retry-on-412 loop
is easy to get subtly wrong. `update_with_retry` is that loop as a
primitive:

```python
def deactivate(patient: dict) -> dict:
    patient["active"] = False
    return patient

result = client.update_with_retry("Patient", "123", deactivate)

if result.wrote:
    print(f"now at version {result.version_id}")
else:
    print("already in the desired state — no write sent")
```

Semantics:

- The mutator receives the resource as read (mutate in place or return
  a new dict; returning `None` keeps the input). On a 412 — a
  concurrent writer won the race — the loop re-reads and re-runs the
  mutator against fresh state, up to `max_retries` times (default 1),
  then lets the final `PreconditionFailedError` propagate. **The
  mutator may run more than once**, so keep it a pure function of its
  input.
- When the mutated state is byte-equal to what was read, the PUT is
  skipped (`UpdateResult.wrote` is `False`). `force=True` writes
  regardless (version bump).
- The write is never unguarded: a read with no `meta.versionId` raises
  `MissingVersionIdError`.
- `UpdateResult` carries `wrote`, the resulting `version_id`, and the
  final `resource` state.

The [ProjectMembership access helpers](project_membership.md) are
implemented on this primitive.

