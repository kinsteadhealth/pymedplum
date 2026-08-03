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

## Bulk conditional creates

`conditional_create_batch` creates many resources idempotently in one
call: it builds `type: batch` bundles of POST entries carrying
`ifNoneExist`, chunked (default 50 per bundle), and classifies every
entry's response.

```python
entries = [
    (
        {"resourceType": "Patient", "identifier": [
            {"system": "http://example.org/mrn", "value": str(n)}
        ]},
        f"identifier=http://example.org/mrn|{n}",
    )
    for n in range(200)
]

result = client.conditional_create_batch(entries, chunk_size=50)

for created in result.created:      # 201 — newly created
    print(created.index, created.resource_id)
for existed in result.existed:      # 200 — an existing resource matched
    print(existed.index, existed.resource_id)
for failed in result.failed:        # anything else — collected, not raised
    print(failed.index, failed.status_code, failed.outcome)
```

Entry `index` values refer to positions in your original `entries`
sequence, across all chunks. `accounts=` stamps `meta.accounts` on
every entry's resource; `on_behalf_of=` applies per call.

Two properties worth knowing:

- **Replay-safe by construction.** A conditional create is the one POST
  shape a replay cannot duplicate — the retry is a server-side no-op —
  so the SDK marks these batch requests replay-safe: an ambiguous 5xx
  or mid-batch network failure retries safely, and re-invoking the
  whole call after an error converges (already-committed entries
  classify as `existed` on the second pass).
- **The query is the correctness boundary.** A `200 existed` returns
  *whatever already matched the query* — use a globally unique business
  key you own, and treat a match as **found, not created**: verify
  identity before attaching local state.

## Retry-safety note

The retry policy replays a `POST` on ambiguous statuses (502/503/504)
**only** when it carries a real `If-None-Exist` query — a bare
`create_resource` POST is never replayed there, because those statuses
can arrive after the origin already committed the write. When a create
must be safe under retry, conditional create is the tool, not the
status class.

