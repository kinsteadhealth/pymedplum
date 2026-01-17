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

```python
from pymedplum.exceptions import PreconditionFailedError

patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]

patient["active"] = False

try:
    updated = client.update_resource(
        patient,
        headers={"If-Match": f'W/"{version}"'},
    )
except PreconditionFailedError:
    print("Conflict detected - resource was modified elsewhere")
```

### Patching with optimistic locking

```python
patient = client.read_resource("Patient", "123")
version = patient["meta"]["versionId"]

operations = [{"op": "replace", "path": "/active", "value": False}]

patched = client.patch_resource(
    "Patient",
    "123",
    operations,
    headers={"If-Match": f'W/"{version}"'},
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

