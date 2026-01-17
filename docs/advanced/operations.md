# FHIR Operations & Terminology

Use `execute_operation` for standard FHIR operations (e.g. `$everything`, `$match`, `$validate`) and Medplum-specific operations.

## Execute operations

### Type-level operations

```python
result = client.execute_operation(
    "Patient",
    "match",
    params={
        "resourceType": "Parameters",
        "parameter": [
            {
                "name": "resource",
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"family": "Smith", "given": ["John"]}],
                    "birthDate": "1990-01-15",
                },
            }
        ],
    },
)
```

### Instance-level operations

```python
bundle = client.execute_operation(
    "Patient",
    "everything",
    resource_id="patient-123",
)
```

### GET for simple lookups

Many operations support GET with query parameters:

```python
result = client.execute_operation(
    "CodeSystem",
    "lookup",
    params={"code": "12345", "system": "http://loinc.org"},
    method="GET",
)
```

### Auto-wrapping `Parameters`

For convenience, `wrap_params=True` converts a simple dict into a FHIR `Parameters` resource for you:

```python
result = client.execute_operation(
    "Patient",
    "custom-operation",
    params={"onlyCertainMatches": True, "count": 10},
    wrap_params=True,
)
```

## Medplum account compartments (`$set-accounts`)

`set_accounts` uses Medplum’s `$set-accounts` operation to manage `meta.accounts`.

```python
result = client.set_accounts(
    resource_ref="Patient/patient-123",
    org_ref="Organization/org-456",
)
print(f"Resources updated: {result['parameter'][0]['valueInteger']}")
```

## C-CDA export

```python
ccda_xml = client.export_ccda(patient_id="patient-123")
with open("patient_summary.xml", "w") as f:
    f.write(ccda_xml)
```

## Terminology helpers

### Validate against ValueSets

```python
is_valid = client.validate_valueset_code(
    valueset_url="http://hl7.org/fhir/ValueSet/observation-status",
    coding={
        "system": "http://hl7.org/fhir/observation-status",
        "code": "final",
    },
)
```

### Expand ValueSets

```python
expansion = client.expand_valueset(
    valueset_url="http://hl7.org/fhir/ValueSet/observation-status",
)

for concept in expansion.get("expansion", {}).get("contains", []):
    print(f"{concept['code']}: {concept['display']}")
```

### Lookup CodeSystem concepts (`$lookup`)

```python
result = client.lookup_concept(
    code="8867-4",
    system="http://loinc.org",
)
```

### Translate using ConceptMaps (`$translate`)

```python
result = client.translate_concept(
    code="final",
    system="http://hl7.org/fhir/observation-status",
    target_system="http://example.org/local-codes",
)
```

