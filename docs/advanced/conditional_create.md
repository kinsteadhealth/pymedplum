# Conditional Create (If-None-Exist)

Conditional create lets you create a resource only if no matching resource exists. This is the core primitive for idempotent writes.

## Basic usage

```python
from pymedplum.fhir import Patient

patient = Patient(
    identifier=[{"system": "http://hospital.org/mrn", "value": "MRN-12345"}],
    name=[{"family": "Smith", "given": ["John"]}],
)

resource = client.create_resource_if_none_exist(
    patient,
    if_none_exist="identifier=http://hospital.org/mrn|MRN-12345",
)

print(f"Patient ID: {resource['id']}")
```

Notes:

- The return value is the resource (dict or model), not the HTTP status. The server may return **201** (created) or **200** (existing).
- `if_none_exist` accepts:
  - a plain query string (`"identifier=system|value"`)
  - a leading `?` (stripped automatically)
  - a full URL (query portion extracted)

## Common patterns

### Prevent duplicate patient records

```python
def ensure_patient_exists(mrn: str, name: dict) -> dict:
    patient = Patient(
        identifier=[{"system": "http://hospital.org/mrn", "value": mrn}],
        name=[name],
    )
    return client.create_resource_if_none_exist(
        patient,
        if_none_exist=f"identifier=http://hospital.org/mrn|{mrn}",
    )
```

### Reference data

```python
def ensure_organization_exists(npi: str, name: str) -> dict:
    org = {
        "resourceType": "Organization",
        "identifier": [{"system": "http://hl7.org/fhir/sid/us-npi", "value": npi}],
        "name": name,
    }
    return client.create_resource_if_none_exist(
        org,
        if_none_exist=f"identifier=http://hl7.org/fhir/sid/us-npi|{npi}",
    )
```

## Error handling

If multiple resources match, the server returns HTTP 412 (Precondition Failed):

```python
from pymedplum.exceptions import PreconditionFailedError

try:
    client.create_resource_if_none_exist(
        patient,
        if_none_exist="family=Smith",
    )
except PreconditionFailedError:
    print("Search criteria matched multiple resources")
```

