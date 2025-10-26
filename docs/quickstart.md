# Quickstart

This guide will walk you through the basic, recommended workflow for using `pymedplum`, which leverages Pydantic models for a type-safe and intuitive experience.

## Initializing the Client
First, create an instance of the `MedplumClient` or `AsyncMedplumClient`.

```python
from pymedplum.client import MedplumClient

# This client will be used for all synchronous examples
client = MedplumClient(
    base_url="https://api.medplum.com/",
    access_token="YOUR_ACCESS_TOKEN"
)
```

## Creating a Resource with Pydantic
The best way to create a resource is to instantiate its Pydantic model. This gives you autocompletion and compile-time validation in your editor.

```python
from pymedplum.fhir.patient import Patient

# Create a Patient model instance
new_patient = Patient(
    name=[{"given": ["Jane"], "family": "Pydantic"}],
    gender="female",
    birth_date="1990-05-20"
)

# Pass the model directly to the client
created_patient = client.create_resource(new_patient)

print(f"Created patient {created_patient.id} for {created_patient.name[0].given[0]}")
assert isinstance(created_patient, Patient)
```
The client accepts the model instance and returns a new instance representing the resource as it was stored on the server, now including its server-assigned `id`.

## Reading a Resource into a Model
When you read a resource, you should read it directly into its corresponding Pydantic model using the `as_fhir` parameter. This gives you a strongly-typed object to work with.

```python
from pymedplum.fhir.patient import Patient

# Read a resource and get a typed model back
patient = client.read_resource("Patient", "some-patient-id", as_fhir=Patient)

# Now you can access its attributes with type-safety
print(f"Patient's Gender: {patient.gender}")
if patient.birth_date:
    print(f"Birth Date: {patient.birth_date}")
```

## Searching for Resources
The recommended way to search is to use the `search_resource_pages` iterator, which handles pagination for you and yields Pydantic models directly.

```python
from pymedplum.fhir.observation import Observation

# Search for all of a patient's vital signs
for observation in client.search_resource_pages(
    "Observation", 
    {"subject": "Patient/some-patient-id", "category": "vital-signs"},
    as_fhir=Observation
):
    # Each item is a fully-validated Observation model
    print(f"Found Observation {observation.id} with status: {observation.status}")
```

This Pydantic-first approach is the core design philosophy of `pymedplum` and provides the best developer experience.

---

For more in-depth examples, see the **Advanced Usage** guide. To learn more about the Pydantic models and client design, see the **Core Concepts** section.
