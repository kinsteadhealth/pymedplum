# On-Behalf-Of (OBO)

On-behalf-of (OBO) is a Medplum security mechanism that lets an authenticated user act as another user by adopting the context of a **`ProjectMembership`**.

## Persistent OBO client

```python
from pymedplum.client import MedplumClient

patient_membership_id = "some-project-membership-id"

obo_client = MedplumClient(
    base_url="https://api.medplum.com/",
    access_token="YOUR_PRACTITIONER_TOKEN",
    default_on_behalf_of=patient_membership_id,
)
```

## Context manager (recommended)

```python
client = MedplumClient(access_token="YOUR_PRACTITIONER_TOKEN")
patient_membership_id = "ab123-cd456-ef789"

with client.on_behalf_of(patient_membership_id) as patient_client:
    patient_client.create_resource(
        {
            "resourceType": "QuestionnaireResponse",
            "status": "completed",
            "subject": {"reference": "Patient/the-patient-id"},
        }
    )

# Automatically restored to practitioner context
client.search_resources("Practitioner")
```

