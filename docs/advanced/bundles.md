# Transactions & Batch Bundles

FHIR Bundles allow multiple operations in a single request.

- Use **transactions** for atomic operations (all-or-nothing)
- Use **batches** for independent operations (each entry can succeed/fail independently)

## Transaction bundle (atomic)

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

