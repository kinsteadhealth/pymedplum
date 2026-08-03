# Utility Functions

`pymedplum` includes a `helpers` module with several utility functions to simplify common FHIR operations.

## Reference Handling

### `parse_reference(reference_string)`
Parses a FHIR reference string (e.g., `"Patient/123"`) into its component parts.

-   **Returns**: A tuple of `(resource_type, resource_id)`.
-   **Raises**: `ValueError` if the reference format is invalid.

```python
from pymedplum.helpers import parse_reference

resource_type, resource_id = parse_reference("Practitioner/abc-123")
print(f"Type: {resource_type}, ID: {resource_id}")
# Output: Type: Practitioner, ID: abc-123
```

### `build_reference(resource_type, resource_id)`
Constructs a FHIR reference string from a resource type and ID.

```python
from pymedplum.helpers import build_reference

ref = build_reference("Observation", "obs-456")
print(ref)
# Output: Observation/obs-456
```

## Data Extraction

### `get_patient_display_name(patient_resource)`
Extracts a single, display-friendly full name from a Patient resource, handling the complexity of the `HumanName` data type.

```python
from pymedplum.helpers import get_patient_display_name

patient = {"name": [{"given": ["John", "B."], "family": "Doe"}]}
display_name = get_patient_display_name(patient)
print(display_name)
# Output: John B. Doe
```

### `extract_identifier(resource, system_uri)`
Finds and returns the value of an identifier from a resource's `identifier` list based on its system URI.

```python
from pymedplum.helpers import extract_identifier

patient = {
    "identifier": [
        {"system": "http://hospital.org/mrn", "value": "MRN12345"},
        {"system": "http://acme.com/patient-id", "value": "PID-987"}
    ]
}

mrn = extract_identifier(patient, "http://hospital.org/mrn")
print(mrn)
# Output: MRN12345
```

### `get_code_display(codeable_concept)`
Extracts the display text from a `CodeableConcept`, preferring the `text` field and falling back to the first `coding.display` value.

```python
from pymedplum.helpers import get_code_display

concept = {
  "coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}]
}
display = get_code_display(concept)
print(display)
# Output: Hypertension
```

## Data Conversion

### `to_fhir_json(model)`
Converts a Pydantic model instance into a JSON-serializable dictionary. It correctly uses field aliases (for `camelCase`) and excludes `None` values, making it perfect for API payloads. This is the recommended way to serialize models before sending them to the API.

```python
from pymedplum.helpers import to_fhir_json
from pymedplum.fhir import Patient

patient_model = Patient(birth_date="1990-01-01", active=True)
api_payload = to_fhir_json(patient_model)
print(api_payload)
# Output: {'resourceType': 'Patient', 'birthDate': '1990-01-01', 'active': True}
```

## Extension Helpers

Read, set, and remove FHIR `extension` entries without open-coding URL
walking. Every helper accepts both raw dicts and generated Pydantic
models — they share the `extension` list shape.

```python
from pymedplum import (
    get_extension,        # first entry with the URL, or None
    get_extensions,       # every entry with the URL
    get_extension_value,  # the value[x] of the first entry with the URL
    set_extension,        # replace-or-append a simple value[x] extension
    upsert_extension,     # keyed merge of a complete extension entry
    remove_extension,     # drop every entry with the URL -> bool
    get_nested_value,     # child value[x] inside a complex extension
)

patient = {"resourceType": "Patient"}

set_extension(patient, "https://example.org/flag", valueBoolean=True)
get_extension_value(patient, "https://example.org/flag")  # True
remove_extension(patient, "https://example.org/flag")     # True

# Complex (nested) extensions
ext = {
    "url": "https://example.org/window",
    "extension": [{"url": "start", "valueDateTime": "2026-01-01T09:00:00Z"}],
}
get_nested_value(ext, "start")  # "2026-01-01T09:00:00Z"
```

Notes:

- `set_extension` takes exactly one `value[x]` keyword, in camelCase or
  snake_case form (`valueString=` / `value_string=`). It replaces the
  first entry with the URL (collapsing duplicates) or appends.
- `remove_extension` drops the `extension` key entirely when the list
  empties — FHIR JSON forbids empty arrays.
- On Pydantic models, assignment triggers validation, so dict entries
  are coerced to `Extension` models automatically.

### Medplum service-type references

Medplum tags Slot/Schedule `serviceType` concepts with an embedded
`Reference<HealthcareService>` extension (its R4 stand-in for R5's
`CodeableReference`). Two helpers carry that convention:

```python
from pymedplum import (
    SERVICE_TYPE_REFERENCE_URL,
    read_service_type_references,
    service_type_reference_extension,
)

slot = {
    "resourceType": "Slot",
    "serviceType": [
        service_type_reference_extension("HealthcareService/hs-1"),
    ],
}

read_service_type_references(slot)
# ["HealthcareService/hs-1"]
```

`service_type_reference_extension(reference, codings=None)` builds the
`serviceType` CodeableConcept (optionally carrying `Coding` dicts);
`read_service_type_references(slot_or_schedule)` extracts every tagged
reference from a dict or model.

## Reading `Parameters` Responses

`parameters_to_dict`, `get_parameter`, and `get_parameter_resource`
parse FHIR `Parameters` resources (operation responses) back into plain
Python values — see
[FHIR Operations & Terminology](advanced/operations.md#reading-parameters-responses).

