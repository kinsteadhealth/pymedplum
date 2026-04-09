# Working with FHIR Models

A core feature of `pymedplum` is its set of Pydantic models, which provide fully-typed Python representations of FHIR resources. The model system is designed for an optimal developer experience, balancing three key goals:

1.  **High Performance**: FHIR models are lazy-loaded to ensure fast application startup times, which is critical for environments like serverless functions.
2.  **Full Type Safety**: The library is fully compliant with PEP 561, providing comprehensive type hints through stub files (`.pyi`) for use with tools like `mypy`.
3.  **Excellent Editor Support**: Autocompletion, type-checking, and docstrings work out-of-the-box in modern IDEs like VS Code.

These models are based on Pydantic v2, offering robust data validation and serialization.

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

The entire `pymedplum.fhir` module is auto-generated from Medplum's official TypeScript definitions to ensure accuracy and maintainability. The generation logic resides in the `/scripts` directory.

### Generated Architecture

When you run the generator, it creates a sophisticated, multi-file architecture to achieve the goals of performance and type safety:

1.  **`pymedplum/fhir/{resource}.py`** (e.g., `patient.py`)
    -   Contains the Pydantic model definition for a single FHIR resource.
    -   Uses `if TYPE_CHECKING:` blocks to import dependencies for static analysis without runtime cost.

2.  **`pymedplum/fhir/__init__.py`**
    -   The public-facing module for importing FHIR models.
    -   Implements the **lazy-loading** mechanism using `__getattr__`. When you `from pymedplum.fhir import Patient`, this file intercepts the request and only loads `patient.py` on first access.
    -   Contains helper functions for dependency resolution.

3.  **`pymedplum/fhir/__init__.pyi`** (Stub File)
    -   A type stub file that provides an "eager" view of the module for static analysis tools.
    -   It explicitly imports every single FHIR model so that tools like `mypy` can see the complete module structure.
    -   This file is **never executed** at runtime.

4.  **`pymedplum/py.typed`**
    -   A marker file that signals to type checkers that `pymedplum` is a PEP 561-compliant typed package.

### Regenerating Models

If the upstream Medplum FHIR definitions change, regenerate all Pydantic models with a single command from the project root:

```bash
make generate              # Update to latest @medplum/fhirtypes and regenerate
make generate-no-update    # Regenerate without updating the npm dependency
```

This runs the full pipeline: npm update, TypeScript codegen, ruff formatting, and a validation smoke test. It also automatically removes stale `.py` files if an upstream type was deleted.

**Requirements:** `node`, `npm`, `python3`, and `uvx` must be on your PATH. The script checks for all of these at startup.

The generated `__init__.py` records which `@medplum/fhirtypes` version produced it, so you can always tell what's deployed.

For more details on the generator architecture, see [scripts/README.md](../scripts/README.md).
