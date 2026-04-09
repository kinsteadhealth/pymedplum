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

## Multi-tenant accounts (`$set-accounts`)

In multi-tenant MSO (Management Services Organization) setups, Medplum uses `meta.accounts` to assign resources to accounts — typically Organizations — which drive compartment-based access control via AccessPolicies.

`set_accounts` wraps Medplum’s `$set-accounts` operation:

```python
# Assign a patient to an organization
client.set_accounts("Patient/patient-123", "Organization/org-456")

# Assign to multiple accounts (e.g., an org and a specific practitioner)
client.set_accounts(
    "Patient/patient-123",
    ["Organization/org-456", "Practitioner/prac-789"],
)

# Propagate account assignments to all related resources
# in the patient’s FHIR compartment (Observations, Encounters, etc.)
client.set_accounts(
    "Patient/patient-123",
    "Organization/org-456",
    propagate=True,
)

# For large compartments, use prefer_async to avoid timeouts
# (only takes effect when propagate is also True)
result = client.set_accounts(
    "Patient/patient-123",
    "Organization/org-456",
    propagate=True,
    prefer_async=True,
)
# Server returns an OperationOutcome — wait for completion
job = client.wait_for_async_job(result, timeout=60)
print(job["status"])  # "completed"

# Or check once without waiting
job = client.get_async_job_status(result)
if job["status"] == "completed":
    print(job["output"])
```

### How Medplum assigns accounts

Most of the time, you don't need to set accounts yourself. Medplum
handles it:

- **Creating a Patient via OBO**: The server assigns accounts from the
  user's AccessPolicy `compartment` field automatically.
- **Creating resources linked to a Patient** (Encounter, Observation,
  etc.): The server copies the Patient's `meta.accounts` onto the new
  resource. If the Patient is in multiple orgs, the new resource
  inherits all of them.
- **Updating a resource**: Accounts are preserved for Patients and
  re-derived from the linked Patient for other resources. The updater's
  org is never added automatically.

### When you need to set accounts explicitly

**Admin/ClientApplication creating a Patient** — the server has no
AccessPolicy compartment to auto-assign from, so use `accounts=` on
`create_resource()` or call `set_accounts()` after.

**Enrolling a Patient in a second org** — an admin calls
`set_accounts()` with both org refs. Use `propagate=True` to cascade
to existing related resources. `$set-accounts` requires projectAdmin
or superAdmin (returns 403 otherwise).

**Overriding accounts on update** — only admin/ClientApplication
callers can do this via `accounts=` on `update_resource()`. The server
ignores client-provided accounts from non-admin callers.

| Scenario | How accounts are set | Notes |
|----------|---------------------|-------|
| OBO creates Patient | Automatic from AccessPolicy compartment | Single org |
| Any caller creates resource linked to Patient | Inherited from Patient's accounts | Multi-org if Patient has multiple |
| Admin creates Patient or unlinked resource | `accounts=` or `set_accounts()` | Must be explicit |
| Any caller updates a resource | Preserved (Patient) or re-derived (others) | Never re-compartmentalized to updater's org |
| Admin updates with `accounts=` | Overrides accounts | Admin-only |
| Enroll Patient in additional org | Admin calls `set_accounts()` | `propagate=True` to update existing related resources |
| Enroll Patient in new org | Admin calls `set_accounts()` | Use `propagate=True` to update existing related resources |

### Helpers for inspecting account assignments

```python
from pymedplum import get_resource_accounts, resource_has_account

patient = client.read_resource("Patient", "patient-123")

# Check if a resource is assigned to a specific account
resource_has_account(patient, "Organization/org-456")  # True/False

# List all account references on a resource
get_resource_accounts(patient)  # ["Organization/org-456", ...]
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

