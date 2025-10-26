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
from pymedplum.fhir.patient import Patient

patient_model = Patient(birth_date="1990-01-01", active=True)
api_payload = to_fhir_json(patient_model)
print(api_payload)
# Output: {'resourceType': 'Patient', 'birthDate': '1990-01-01', 'active': True}
```

### `to_portable(resource)`
Strips Medplum-specific metadata (like `meta.author` and `meta.project`) and converts Medplum's `meta.accounts` field into standard FHIR extensions. This is useful when you need to share FHIR data with a non-Medplum system.

## Token Handling

### `decode_jwt_exp(token)`
Decodes a JWT token and returns its expiration time as a timezone-aware `datetime` object. Returns `None` if the token is invalid or has no expiration.

```python
from pymedplum.helpers import decode_jwt_exp

# Assume client is an authenticated MedplumClient
token = client.access_token 
expiration_time = decode_jwt_exp(token)
if expiration_time:
    print(f"Token expires at: {expiration_time}")
