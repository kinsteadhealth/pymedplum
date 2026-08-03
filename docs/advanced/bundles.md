# Transactions & Batch Bundles

FHIR Bundles allow multiple operations in a single request.

- Use **transactions** when entries reference each other
  (`urn:uuid:` placeholders) and should be processed together
- Use **batches** for independent operations (each entry can succeed/fail independently)

> **Do not assume transactions are atomic on failure.** Medplum
> `type: transaction` bundles have been observed to commit some entries
> while others fail (verify against your server version — never assume
> atomicity). Treat a transaction as "processed together", not
> "all-or-nothing": always [inspect per-entry
> results](#inspecting-batchtransaction-responses) and compensate for
> partial commits instead of trusting a rollback.

## Transaction bundle

```python
bundle = {
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [
        {
            "request": {"method": "POST", "url": "Patient"},
            "resource": {
                "resourceType": "Patient",
                "name": [{"family": "Smith", "given": ["John"]}],
            },
            "fullUrl": "urn:uuid:patient-temp-id",
        },
        {
            "request": {"method": "POST", "url": "Observation"},
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {"text": "Blood Pressure"},
                "subject": {"reference": "urn:uuid:patient-temp-id"},
            },
        },
    ],
}

result = client.execute_transaction(bundle)
```

Both `execute_transaction` and `execute_batch` accept `accounts=` to
stamp `meta.accounts` on every entry's resource before sending:

```python
result = client.execute_transaction(bundle, accounts="Organization/org-a")
```

## Batch bundle (independent)

```python
bundle = {
    "resourceType": "Bundle",
    "type": "batch",
    "entry": [
        {
            "request": {"method": "PUT", "url": "Patient/123"},
            "resource": {"resourceType": "Patient", "id": "123", "active": True},
        },
        {
            "request": {"method": "PUT", "url": "Patient/456"},
            "resource": {"resourceType": "Patient", "id": "456", "active": False},
        },
        {"request": {"method": "DELETE", "url": "Observation/789"}},
    ],
}

result = client.execute_batch(bundle)
```

## Inspecting batch/transaction responses

A `200 OK` on the outer request proves nothing about the entries — each
entry carries its own `response.status`. `FHIRBundle.get_resources()`
is search-shaped and *skips* entries with no `resource` key, which is
exactly what a bare `201 Created` write entry looks like. Use the
entry-inspection API instead:

```python
from pymedplum import BundleEntryError, FHIRBundle

response = FHIRBundle(client.execute_transaction(bundle))

for entry in response.entry_results():
    print(entry.index, entry.status_code, entry.ok, entry.resource_id)

failures = response.failures()          # non-2xx entries only
successes, failures = response.partition()

try:
    response.raise_for_entry_errors()   # raises on any failed entry
except BundleEntryError as exc:
    for failed in exc.entries:
        print(failed.index, failed.status_code, failed.outcome)
```

Each `BundleEntryResult` carries the entry `index`, the parsed
`status_code`, `ok` (2xx), the `resource_id` (parsed from
`response.location` with any `/_history/<version>` suffix stripped,
falling back to `resource.id`), the `resource` body when the server
returned one, and the `outcome` OperationOutcome on failures.

`BundleEntryError.entries` holds the failed results; `str(exc)` carries
only indices and status codes (never server outcome text, which can
echo caller-supplied values), and `sanitize_for_logging()` returns a
log-safe dict — same convention as the rest of the exception family.

Because transactions are not atomic on failure, catching
`BundleEntryError` is a **compensation point**: the successful entries
have already committed.

## Idempotent bulk creation

For creating many resources idempotently, skip hand-building bundles —
see [`conditional_create_batch`](conditional_create.md#bulk-conditional-creates)
which builds chunked batch bundles of conditional creates and
classifies every entry.

