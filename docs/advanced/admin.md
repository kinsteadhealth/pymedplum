# Administration

If you have the appropriate permissions, you can use the client to manage project-level administrative settings.

## Managing project secrets

```python
project_id = "YOUR_PROJECT_ID"

project = client.get(f"admin/projects/{project_id}")
current_secrets = project.get("project", {}).get("secret", [])

new_secrets = current_secrets + [{"name": "NEW_API_KEY", "valueString": "secret-value"}]
client.post(f"admin/projects/{project_id}/secrets", new_secrets)
```

## Managing project sites

```python
project_id = "YOUR_PROJECT_ID"
project = client.get(f"admin/projects/{project_id}")
current_sites = project.get("project", {}).get("site", [])

new_sites = current_sites + [{"name": "New Site", "domain": ["new-app.example.com"]}]
client.post(f"admin/projects/{project_id}/sites", new_sites)
```

## Private Medplum APIs

For administrative tasks without a dedicated helper method, you can call Medplum’s private endpoints via `get()`, `post()`, `put()`, and `delete()`.

### Example: invite a new user

```python
membership = client.invite_user(
    project_id="YOUR_PROJECT_ID",
    resource_type="Practitioner",
    first_name="Alice",
    last_name="Smith",
    email="alice.smith@example.com",
    send_email=True,
)
print(membership["id"])
```

### Example: repair or replace a user's parameterized access

After invitation (or during a tenant move) the parameterized
`ProjectMembership.access` slice that grants tenant access often
needs to be set or rewritten. Three methods, all on the client and
all atomic with `If-Match`-driven 412 retry:

- `merge_project_membership_access` — replace the whole managed slice
  with a desired list (bulk reconcile).
- `add_project_membership_access_entry` — atomically add one tenant.
- `remove_project_membership_access_entry` — atomically remove one
  tenant.

Use the bulk form when you have the full desired list — typically a
one-shot script during data migration, an admin tool that reads all
of a user's tenant assignments in one query, or a recovery job that
restores a known-good state:

```python
from pymedplum import make_project_membership_access

client.merge_project_membership_access(
    membership["id"],
    managed_access=[
        make_project_membership_access(
            "AccessPolicy/practice-policy",
            {"organization": "Organization/practice-a"},
        ),
        make_project_membership_access(
            "AccessPolicy/practice-policy",
            {"organization": "Organization/practice-b"},
        ),
    ],
    managed_policy_ids={"practice-policy"},
)
```

Use the single-entry forms when reacting to a UI event:

```python
client.add_project_membership_access_entry(
    membership["id"],
    make_project_membership_access(
        "AccessPolicy/practice-policy",
        {"organization": "Organization/practice-c"},
    ),
    managed_policy_ids={"practice-policy"},
)
```

To revoke the entire managed grant in one shot without touching
unrelated entries, call `merge_project_membership_access` with
`managed_access=[]`. See
[ProjectMembership Access](project_membership.md) for the full
contract.

