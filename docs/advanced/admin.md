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

