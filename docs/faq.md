# FAQ & Troubleshooting

Common questions and solutions for using `pymedplum`.

## Installation & Setup

### Q: How do I install pymedplum?

```bash
pip install pymedplum
```

For development:
```bash
pip install -e ".[dev]"
```

See [Installation](installation.md) for details.

### Q: What Python versions are supported?

`pymedplum` requires Python 3.8 or higher. It's tested on Python 3.8, 3.9, 3.10, 3.11, and 3.12.

### Q: Do I need to install Pydantic separately?

No, Pydantic v2 is automatically installed as a dependency when you install `pymedplum`.

## Authentication

### Q: How do I get an access token?

There are three ways to authenticate:

1. **Client Credentials** (recommended for server applications):
```python
client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
client.authenticate()  # Obtains token automatically
```

2. **Direct Token** (if you already have one):
```python
client = MedplumClient(
    base_url="https://api.medplum.com/",
    access_token="YOUR_EXISTING_TOKEN"
)
```

3. **Automatic Refresh**: The client automatically refreshes tokens before they expire when using client credentials.

### Q: How do I know when my token expires?

```python
from pymedplum.helpers import decode_jwt_exp

expiration = decode_jwt_exp(client.access_token)
print(f"Token expires at: {expiration}")
```

### Q: I'm getting 401 Unauthorized errors

**Causes**:
- Expired access token
- Invalid client credentials
- Revoked access

**Solutions**:
```python
# Force re-authentication
client.authenticate()

# Or create a new client
client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
```

## Working with Resources

### Q: Should I use dictionaries or Pydantic models?

**Use Pydantic models** for the best developer experience:

```python
from pymedplum.fhir.patient import Patient

# ✅ Recommended: Type-safe, autocomplete, validation
patient = Patient(name=[{"family": "Smith", "given": ["John"]}])
created = client.create_resource(patient)

# ⚠️ Also works: Less type safety
patient_dict = {"resourceType": "Patient", "name": [{"family": "Smith"}]}
created = client.create_resource(patient_dict)
```

Pydantic models provide:
- Autocompletion in your IDE
- Type checking
- Automatic validation
- Better error messages

### Q: How do I handle FHIR fields that are Python keywords?

Use a trailing underscore:

```python
from pymedplum.fhir.coverage import Coverage

coverage = Coverage(
    status="active",
    class_=[  # Note the underscore
        {"type": {...}, "value": "GRP123"}
    ]
)
```

Common Python keywords in FHIR: `class`, `for`, `from`, `import`

### Q: How do I convert between snake_case and camelCase?

The Pydantic models handle this automatically:

```python
# Both work!
patient_a = Patient(birth_date="1990-01-01")  # Pythonic
patient_b = Patient(birthDate="1990-01-01")   # FHIR-style

# Serialize with camelCase for API
from pymedplum.helpers import to_fhir_json
api_payload = to_fhir_json(patient_a)
# Result: {"resourceType": "Patient", "birthDate": "1990-01-01"}
```

### Q: I'm getting ValidationError when creating resources

**Common causes**:

1. **Missing required fields**:
```python
# ❌ Missing required fields
Patient()  # ValidationError!

# ✅ Include required fields
Patient(name=[{"family": "Smith"}])
```

2. **Wrong field types**:
```python
# ❌ Wrong type
Patient(active="yes")  # Should be boolean

# ✅ Correct type
Patient(active=True)
```

3. **Invalid date format**:
```python
# ❌ Wrong format
Patient(birth_date="01/15/1990")

# ✅ ISO 8601 format
Patient(birth_date="1990-01-15")
```

### Q: How do I update only specific fields without overwriting the entire resource?

Use `patch_resource` for partial updates:

```python
# Read current state
patient = client.read_resource("Patient", "123")

# Patch specific fields
operations = [
    {"op": "replace", "path": "/active", "value": False}
]
client.patch_resource("Patient", "123", operations)

# Alternative: Read, modify, update
patient = client.read_resource("Patient", "123", as_fhir=Patient)
patient.active = False
client.update_resource(patient)
```

## Searching

### Q: How do I search for resources?

Three methods depending on your needs:

```python
# 1. Get all results (handles pagination automatically)
for patient in client.search_resource_pages("Patient", {"family": "Smith"}):
    print(patient["id"])

# 2. Get one page
bundle = client.search_resources("Patient", {"family": "Smith"})

# 3. Get single result
patient = client.search_one("Patient", {"identifier": "MRN|12345"})
```

### Q: How do I include related resources in search results?

Use `_include` or `_revinclude`:

```python
# Get patients WITH their organizations
bundle = client.search_resources("Patient", {
    "family": "Smith",
    "_include": "Patient:organization"
})

# Get patients WITH their observations
bundle = client.search_resources("Patient", {
    "family": "Smith",
    "_revinclude": "Observation:patient"
})
```

See [Advanced Search](advanced_usage.md#advanced-fhir-search) for more examples.

### Q: Search returns too many/few results

**Control pagination**:
```python
# Limit results per page
results = client.search_resources("Patient", {
    "family": "Smith",
    "_count": "50"  # Max 50 per page
})

# Sort results
results = client.search_resources("Observation", {
    "patient": "Patient/123",
    "_sort": "-date"  # Newest first (- for descending)
})
```

### Q: How do I search by date ranges?

Use date prefixes:

```python
from datetime import datetime, timedelta

today = datetime.now().date()
week_ago = today - timedelta(days=7)

# Observations from the last week
recent = client.search_resources("Observation", {
    "date": f"ge{week_ago.isoformat()}"  # ge = greater than or equal
})

# Available prefixes: eq, ne, gt, lt, ge, le
```

## Async Operations

### Q: When should I use AsyncMedplumClient?

Use async when:
- Building async web applications (FastAPI, Sanic)
- Making many concurrent API calls
- Integrating with other async libraries

```python
from pymedplum.async_client import AsyncMedplumClient

async def fetch_multiple_patients(patient_ids):
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        access_token="TOKEN"
    ) as client:
        tasks = [
            client.read_resource("Patient", pid)
            for pid in patient_ids
        ]
        return await asyncio.gather(*tasks)
```

### Q: Can I use both sync and async clients in the same application?

Yes, but don't share connections. Create separate client instances:

```python
# Synchronous operations
sync_client = MedplumClient(...)

# Asynchronous operations
async def async_operations():
    async with AsyncMedplumClient(...) as async_client:
        await async_client.read_resource("Patient", "123")
```

## Performance

### Q: Why is `from pymedplum.fhir import Patient` so fast? It seems like it should be slow.

`pymedplum` uses a **lazy loading** mechanism for its FHIR models. This means:
- When you first `import Patient`, only a lightweight placeholder is created.
- The actual `Patient` model and its dependencies are only loaded from their files and parsed by Pydantic the first time you access the class.
- This "first access" cost is around **50-300ms**, depending on the model's complexity.
- Every subsequent access is nearly instant (~1 microsecond), as the loaded class is cached.

This provides the best of both worlds:
-   **Fast Startup**: Your application starts quickly because it doesn't parse ~300 FHIR models upfront (which would take 3-5 seconds).
-   **Full Type Safety**: Thanks to generated stub files (`.pyi`), your IDE and type checkers like `mypy` have full type information without needing to execute the slow import.

### Q: Is the lazy loader thread-safe, especially with the upcoming "no-GIL" Python?
Yes. The lazy-loading mechanism is designed with robust, multi-layered locking to be fully thread-safe. This prevents race conditions when multiple threads attempt to import FHIR models concurrently.

We validate this guarantee by running a dedicated thread-safety test suite on an experimental "no-GIL" build of Python (`3.13-nogil`) as part of our continuous integration (CI) pipeline. This ensures that `pymedplum` is prepared for the future of concurrent Python.

### Q: How can I speed up batch operations?

**Use async for concurrent requests**:

```python
async def create_many_patients(patients):
    async with AsyncMedplumClient(...) as client:
        tasks = [client.create_resource(p) for p in patients]
        return await asyncio.gather(*tasks)
```

**Use GraphQL for complex queries**:

```python
# Instead of multiple read_resource calls
query = """
query {
    Patient(id: "123") {
        id
        name { family given }
        observation: ObservationList(_reference: patient) {
            id
            code { text }
        }
    }
}
"""
result = client.execute_graphql(query)
```

### Q: My searches are slow

**Tips**:
1. Use specific search parameters to reduce result set
2. Use `_count` to limit page size
3. Use `_elements` to return only needed fields
4. Consider GraphQL for complex queries

```python
# Faster: specific search with limited fields
results = client.search_resources("Observation", {
    "patient": "Patient/123",
    "category": "vital-signs",
    "date": f"ge{recent_date}",
    "_count": "100",
    "_elements": "id,code,value"
})
```

## Errors & Debugging

### Q: How do I see the actual HTTP requests?

Enable httpx logging:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### Q: How do I handle errors gracefully?

```python
from pymedplum.exceptions import (
    NotFoundError,
    AuthorizationError,
    ValidationError,
    RateLimitError
)

try:
    patient = client.read_resource("Patient", "123")
except NotFoundError:
    print("Patient not found")
except AuthorizationError:
    print("Access denied")
except ValidationError as e:
    print(f"Invalid data: {e}")
except RateLimitError:
    print("Rate limited, wait before retrying")
```

### Q: I'm getting rate limited (429 errors)

The client automatically retries with exponential backoff for rate limit errors. If you're still hitting limits:

1. Reduce request frequency
2. Use batch operations (GraphQL)
3. Implement application-level caching
4. Contact Medplum support for higher rate limits

## Advanced Topics

### Q: How do I use on-behalf-of functionality?

```python
# Get the patient's ProjectMembership ID
membership_id = "ProjectMembership/abc123"

# Execute operations as that user
with client.on_behalf_of(membership_id) as obo_client:
    # This read uses the patient's permissions
    result = obo_client.read_resource("Questionnaire", "456")
```

See [On-Behalf-Of Operations](advanced_usage.md#on-behalf-of-operations) for details.

### Q: How do I access admin APIs?

Use the low-level HTTP methods:

```python
# Invite a new user
membership = client.invite_user(
    project_id="PROJECT_ID",
    resource_type="Practitioner",
    first_name="Alice",
    last_name="Smith",
    email="alice@example.com"
)
```

See [Administrative Features](advanced_usage.md#administrative-features) for more examples.

## Still Need Help?

- Check the [API Reference](api_reference.md) for detailed method documentation
- Review [Advanced Usage](advanced_usage.md) for complex scenarios
- Consult the [FHIR Specification](https://hl7.org/fhir/) for FHIR-specific questions
- Open an issue on [GitHub](https://github.com/medplum/pymedplum) for bugs or feature requests
