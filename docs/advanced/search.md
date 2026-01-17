# Advanced Search

FHIR search is powerful, but the syntax can be hard to remember. `pymedplum` supports all common FHIR search patterns and makes them easier to compose by letting you pass a Python `dict`.

## Basic search parameters

All search methods accept a `query` parameter that can be a dictionary of search parameters:

```python
# Search by single parameter
patients = client.search_resources("Patient", {"family": "Smith"})

# Search by multiple parameters (AND logic)
patients = client.search_resources(
    "Patient",
    {
        "family": "Smith",
        "given": "John",
        "birthdate": "1980-01-01",
    },
)
```

## Multi-valued query parameters

Some FHIR search parameters accept multiple values for the same key (common for ranges). PyMedplum automatically turns list values into repeated query params:

```python
# Date range search
patients = client.search_resources(
    "Patient",
    {
        "family": "Smith",
        "birthdate": ["ge1990-01-01", "le2000-12-31"],
    },
)

# Generates:
# birthdate=ge1990-01-01&birthdate=le2000-12-31
```

## Including related resources (`_include`)

Fetch referenced resources in the same request:

```python
bundle = client.search_resources(
    "Patient",
    {
        "family": "Smith",
        "_include": "Patient:organization",
    },
)

for entry in bundle.get("entry", []):
    resource = entry["resource"]
    if resource["resourceType"] == "Patient":
        print(f"Patient: {resource['name'][0]['family']}")
    elif resource["resourceType"] == "Organization":
        print(f"  Organization: {resource['name']}")
```

Multiple includes:

```python
bundle = client.search_resources(
    "Encounter",
    {
        "status": "finished",
        "_include": ["Encounter:patient", "Encounter:location"],
    },
)
```

## Reverse includes (`_revinclude`)

Fetch resources that reference your results:

```python
bundle = client.search_resources(
    "Patient",
    {
        "family": "Smith",
        "_revinclude": "Observation:patient",
    },
)
```

## Recursive includes (`:iterate`)

Follow references on included resources:

```python
bundle = client.search_with_options(
    "MedicationRequest",
    {"patient": "Patient/123"},
    include="MedicationRequest:medication",
    include_iterate="Medication:manufacturer",
)
```

## Search parameter chaining

Filter by fields on referenced resources:

```python
observations = client.search_resources(
    "Observation",
    {
        "patient.family": "Smith",
    },
)

appointments = client.search_resources(
    "Appointment",
    {
        "actor.identifier": "NPI|1234567890",
    },
)
```

## Search modifiers

FHIR modifiers change matching semantics:

```python
patients = client.search_resources("Patient", {"family:exact": "Smith"})
patients = client.search_resources("Patient", {"family:contains": "mit"})
patients = client.search_resources("Patient", {"name:text": "John Smith"})
patients = client.search_resources("Patient", {"email:missing": "true"})
```

## Result controls (count, sort, pagination)

```python
results = client.search_resources(
    "Patient",
    {
        "family": "Smith",
        "_count": "10",
    },
)

results = client.search_resources(
    "Observation",
    {
        "patient": "Patient/123",
        "_sort": "-date",
    },
)
```

For full pagination over all pages, use `search_resource_pages()`:

```python
for observation in client.search_resource_pages(
    "Observation",
    {
        "patient.family": "Smith",
        "_sort": "-date",
        "_count": "100",
    },
):
    ...
```

## `search_with_options` (TypeScript SDK parity)

`search_with_options` provides an ergonomic interface for common search knobs:

```python
result = client.search_with_options(
    "Patient",
    {"active": "true"},
    summary="count",
)
print(f"Active patients: {result.get('total', 0)}")
```

