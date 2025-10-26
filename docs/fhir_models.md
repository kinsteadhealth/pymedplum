# Working with FHIR Models

A core feature of `pymedplum` is its set of Pydantic models, which provide fully-typed Python representations of FHIR resources. These models were completely refactored to be based on Pydantic v2, offering robust data validation, serialization, and excellent editor support.

## Key Pydantic Features

### Data Validation
When you create or receive a resource, Pydantic automatically validates the data. If any fields are of the wrong type or are missing required values, a `ValidationError` is raised.

```python
from pymedplum.fhir.patient import Patient

# This will raise a ValidationError because 'gender' is required
invalid_data = {"resourceType": "Patient"}
try:
    Patient(**invalid_data)
except ValueError as e:
    print(e)
```

### Field Aliases (camelCase vs. snake_case)
FHIR APIs use `camelCase` for field names (e.g., `birthDate`), while Python's convention is `snake_case` (e.g., `birth_date`). The Pydantic models handle this conversion automatically using field aliases.

You can instantiate models using either convention:
```python
# Using snake_case (Pythonic)
patient_a = Patient(birth_date="1985-01-15")

# Using camelCase (API-style)
patient_b = Patient(birthDate="1985-01-15")

assert patient_a.birth_date == patient_b.birth_date
```

### Serialization with `to_fhir_json()`
When sending data back to the Medplum API, it must be in a JSON format with `camelCase` keys. The `to_fhir_json()` helper function is provided for this purpose.

```python
from pymedplum.helpers import to_fhir_json

patient = Patient(resource_type="Patient", birth_date="1985-01-15", active=True)

# Convert the model to a JSON-compatible dictionary
fhir_dict = to_fhir_json(patient)

# Produces: {'resourceType': 'Patient', 'birthDate': '1985-01-15', 'active': True}
print(fhir_dict)
```
This function is equivalent to calling `model.model_dump(by_alias=True, exclude_none=True)`.

### Handling Python Keywords
Some FHIR fields have names that are reserved keywords in Python (e.g., `class`, `for`). The models use a trailing underscore (`_`) for these fields.

```python
from pymedplum.fhir.coverage import Coverage

# Use 'class_' for the 'class' field
coverage = Coverage(
    resource_type="Coverage",
    status="active",
    class_=[
        {
            "type": {"system": "http://terminology.hl7.org/CodeSystem/coverage-class", "code": "group"},
            "value": "GRP12345"
        }
    ]
)

# Serializes to: {'resourceType': 'Coverage', 'status': 'active', 'class': [...]}
print(to_fhir_json(coverage))
```

## Pydantic-Forward Operations
While you can always work with dictionaries, the real power of `pymedplum` comes from using the Pydantic models throughout your workflow. This provides better type safety, autocompletion, and a more object-oriented feel.

### Creating Resources from Models
Instead of passing a dictionary to `create()`, you can instantiate a model and pass it to `create_resource()`.

```python
from pymedplum.fhir.patient import Patient

# Create a Patient model instance
new_patient = Patient(
    name=[{"family": "ModelCreate", "given": ["Pydantic"]}],
    gender="female",
    birth_date="1995-10-16"
)

# Pass the model directly to the client
created_patient = client.create_resource(new_patient)

# The returned object is also a Pydantic model
print(f"Created patient {created_patient.id} for {created_patient.name[0].given[0]}")
assert isinstance(created_patient, Patient)
```

### Reading and Updating Models
When you read a resource, you get a Pydantic model back. You can modify its attributes and then pass it to `update_resource`.

```python
# Read a patient and get a model instance
patient_to_update = client.read_resource("Patient", "some-patient-id")

# Modify attributes directly
patient_to_update.gender = "male"
patient_to_update.active = True

# Pass the updated model back to the client
updated_patient = client.update_resource(patient_to_update)

print(f"Patient is now active: {updated_patient.active}")
```

### Model-Driven Search
The client provides helper methods for searching that yield Pydantic models directly, saving you from parsing the `Bundle` manually.

#### `search_one()`
If you expect only one result from a search, `search_one()` is ideal. It returns the single resource model or `None`.

```python
# Find a unique patient
unique_patient = client.search_one("Patient", {"identifier": "urn:oid:1.2.3.4|12345"})

if unique_patient:
    print(f"Found patient: {unique_patient.name[0].family}")
    assert isinstance(unique_patient, Patient)
```

#### `search_resource_pages()`
To iterate through all resources from a search query without worrying about pagination, use `search_resource_pages()`.

```python
# Find all patients with a specific name
for patient in client.search_resource_pages("Patient", {"family": "Smith"}):
    # Each item is a fully-validated Patient model
    print(f"Processing patient {patient.id}...")
    assert isinstance(patient, Patient)
```

## For Developers: Model Generation
The FHIR models are automatically generated from the Medplum TypeScript definitions. This ensures they are always up-to-date with the official FHIR specification as supported by Medplum. The generation logic resides in the `/scripts` directory.

### Regenerating Models
If the Medplum FHIR definitions change, developers can regenerate the Pydantic models. This is a two-step process.

#### Step 1: Run the Code Generator
The TypeScript-based generator script parses the source files and writes the Python model files.

1.  **Navigate to the scripts directory:**
    ```bash
    cd scripts
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Run the generator:**
    ```bash
    npm run generate
    ```
This will overwrite the Python files in `pymedplum/fhir/`.

#### Step 2: Lint and Format the New Files
The auto-generated code may not be perfectly formatted. Use `ruff` to automatically fix import sorting, formatting, and other linting issues. From the project root directory:

```bash
ruff check pymedplum/fhir/ --fix
ruff format pymedplum/fhir/
```

After these steps, the models will be up-to-date and correctly formatted.
