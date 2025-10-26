# Client Method Design

The `MedplumClient` and `AsyncMedplumClient` are designed to be flexible and developer-friendly, catering to both traditional dictionary-based workflows and modern, type-safe Pydantic model-based workflows. This is achieved through the use of method overloading.

## Universal Input: Dicts and Pydantic Models

For write operations, you can provide the resource data as either a standard Python dictionary or as an initialized Pydantic model instance. The client handles the conversion automatically.

### `create_resource(resource)`
-   **Accepts**: `dict` or a Pydantic model instance.
-   **Returns**: A dictionary of the created resource.

```python
from pymedplum.fhir.patient import Patient

# Option 1: Using a dictionary
patient_dict = {
    "resourceType": "Patient",
    "name": [{"given": ["John"], "family": "Dict"}]
}
created_from_dict = client.create_resource(patient_dict)

# Option 2: Using a Pydantic model
patient_model = Patient(name=[{"given": ["Jane"], "family": "Model"}])
created_from_model = client.create_resource(patient_model)
```

### `update_resource(resource)`
Similarly, `update_resource` also accepts both formats.

```python
# Assume patient_model is a Pydantic model instance from a read() call
patient_model.active = False
client.update_resource(patient_model)

# Or with a dict
patient_dict["active"] = False
client.update_resource(patient_dict)
```

## Flexible Output: Dicts vs. Typed Models

For read operations, you can choose the format of the returned data. By default, you get a dictionary for backward compatibility, but you can request a fully-typed Pydantic model for a better development experience.

### `read_resource(resource_type, id, as_fhir=...)`
The `as_fhir` parameter controls the return type.

-   **`as_fhir=None` (default)**: Returns a `dict`.
-   **`as_fhir=Patient` (or any model class)**: Returns an instance of that Pydantic model.

```python
from pymedplum.fhir.patient import Patient

# Default: returns a dictionary
patient_dict = client.read_resource("Patient", "some-id")
print(patient_dict["name"][0]["family"])

# Get a typed model back
patient_model = client.read_resource("Patient", "some-id", as_fhir=Patient)
print(patient_model.name[0].family) # Autocompletes and is type-checked
```

## Search Result Helpers

### `search_resources(..., return_bundle=...)`
The `search_resources` method can return either a raw bundle dictionary or a helpful `FHIRBundle` wrapper object.

-   **`return_bundle=False` (default)**: Returns a `dict` representing the FHIR Bundle.
-   **`return_bundle=True`**: Returns an instance of `FHIRBundle`, which provides helpful methods for iteration and type conversion.

```python
from pymedplum.fhir.patient import Patient

# Get a helpful wrapper object
bundle = client.search_resources("Patient", {"family": "Smith"}, return_bundle=True)

# 1. Iterate directly over resources
for resource_dict in bundle:
    print(resource_dict["id"])

# 2. Get a list of strongly-typed Pydantic models
patients = bundle.get_resources_typed(Patient)
for p in patients:
    print(p.birth_date) # Autocompletes!
```

This design provides a smooth migration path from dictionary-based code to a more modern, type-safe, Pydantic-forward style without breaking changes.
