# Quickstart

This guide will walk you through the basic, recommended workflow for using `pymedplum`, which leverages Pydantic models for a type-safe and intuitive experience.

## Initializing the Client
First, create an instance of the `MedplumClient` or `AsyncMedplumClient`.
Constructor arguments (other than `base_url`) are keyword-only; unknown
kwargs raise `TypeError` at construction time.

```python
from pymedplum import MedplumClient

client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)
```

If you already have a bearer token, pass `access_token=` instead of
the client-credentials pair.

### HTTPS is required by default

PyMedplum enforces `https://` on the `base_url` unless the host is a
loopback address (`127.0.0.1`, `::1`, `localhost`). If you're running
Medplum locally via Docker, `http://localhost:8103/` works with no
extra flag. Any other `http://` URL raises `InsecureTransportError`
unless you explicitly pass `allow_insecure_http=True` (not recommended
in production; logs a WARNING when enabled).

## Creating a Resource with Pydantic
The best way to create a resource is to instantiate its Pydantic model. This gives you autocompletion and compile-time validation in your editor.

```python
from pymedplum.fhir import Patient

new_patient = Patient(
    name=[{"given": ["Jane"], "family": "Pydantic"}],
    gender="female",
    birth_date="1990-05-20",
)

created_patient = client.create_resource(new_patient, as_fhir=Patient)

print(f"Created patient {created_patient.id} for {created_patient.name[0].given[0]}")
assert isinstance(created_patient, Patient)
```
The client accepts the model instance and returns a new instance representing the resource as it was stored on the server, now including its server-assigned `id`.

## Reading a Resource into a Model
When you read a resource, you should read it directly into its corresponding Pydantic model using the `as_fhir` parameter. This gives you a strongly-typed object to work with.

```python
from pymedplum.fhir import Patient

patient = client.read_resource("Patient", "some-patient-id", as_fhir=Patient)

print(f"Patient's Gender: {patient.gender}")
if patient.birth_date:
    print(f"Birth Date: {patient.birth_date}")
```

## Updating a Resource

`update_resource` auto-attaches an `If-Match` header from the
resource's `meta.versionId` by default, giving you optimistic
concurrency control out of the box.

```python
patient = client.read_resource("Patient", "some-patient-id", as_fhir=Patient)
patient.active = False

# Default: If-Match derived from meta.versionId.
updated = client.update_resource(patient)

# Opt out for last-write-wins behavior.
updated = client.update_resource(patient, if_match=False)

# Or pass a custom value verbatim.
updated = client.update_resource(patient, if_match='W/"5"')
```

If the server's current version has moved on, the default path raises
`PreconditionFailedError` rather than silently overwriting a newer
revision.

## Searching for Resources
The recommended way to search is to use the `search_resource_pages` iterator, which handles pagination for you. You can get results as dicts or as typed Pydantic models.

```python
from pymedplum.fhir import Observation

for observation in client.search_resource_pages(
    "Observation",
    {"subject": "Patient/some-patient-id", "category": "vital-signs"},
    as_fhir=Observation,
):
    print(f"Found Observation {observation.id} with status: {observation.status}")

for observation in client.search_resource_pages(
    "Observation",
    {"subject": "Patient/some-patient-id", "category": "vital-signs"},
):
    print(f"Found Observation {observation['id']} with status: {observation['status']}")
```

The type-safe approach with Pydantic models provides the best developer experience with full IDE autocomplete and validation.

---

For more in-depth examples, see the **Advanced Usage** guide. To learn more about the Pydantic models and client design, see the **Core Concepts** section. For PHI-access audit hooks, see [Audit Logging](advanced/audit_logging.md).
