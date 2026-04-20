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

`pymedplum` requires Python 3.10 or higher. It's tested on 3.10, 3.11,
3.12, and 3.13 (including the experimental no-GIL build).

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
# The client authenticates automatically on the first request and
# refreshes the token proactively before expiration.
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

The client tracks expiry from the OAuth ``expires_in`` field on the token
response and refreshes proactively. If you supplied an externally-acquired
``access_token`` without an ``expires_at``, the SDK does not parse the
token; it simply waits for the server to return ``401`` and reactively
refreshes. Read ``client.token_expires_at`` to check the currently-known
expiry (``None`` means "no hint, will refresh on rejection").

### Q: I'm getting 401 Unauthorized errors

**Causes**:
- Expired access token
- Invalid client credentials
- Revoked access

**Solutions**:

The client auto-retries on `401 Unauthorized` with a forced token
refresh, so transient expirations are handled for you. You only need
to intervene if the underlying credentials are bad or revoked.

```python
# If credentials have been rotated or revoked, construct a new client
# with the new values.
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
from pymedplum.fhir import Patient

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

### Q: Can I import models from their submodules directly?

**No — always import from `pymedplum.fhir`.** The generated resource
modules (e.g. `pymedplum.fhir.patient`) only import their dependencies
under `TYPE_CHECKING` to avoid circular imports, so the class isn't
fully defined at runtime:

```python
# ❌ Will fail at instantiation with
#    "PydanticUserError: <Model> is not fully defined"
from pymedplum.fhir.patient import Patient

# ✅ Use the package-level import — the lazy loader resolves
#    forward references before returning the class.
from pymedplum.fhir import Patient
```

### Q: How do I handle FHIR fields that are Python keywords?

Use a trailing underscore:

```python
from pymedplum.fhir import Coverage

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

See [Advanced Search](advanced/search.md) for more examples.

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
from pymedplum import (
    AuthorizationError,
    InsecureTransportError,
    NotFoundError,
    OperationOutcomeError,
    PreconditionFailedError,
    RateLimitError,
    ServerError,
    TokenRefreshCooldownError,
    UnsafeRedirectError,
    ValidationError,
)

try:
    patient = client.read_resource("Patient", "123")
except NotFoundError:
    ...
except AuthorizationError:
    ...
except ValidationError:
    ...
except RateLimitError:
    ...
except PreconditionFailedError:
    # If-Match / If-None-Exist version mismatch
    ...
except (OperationOutcomeError, ServerError) as exc:
    # exc.sanitize_for_logging() returns a PHI-safe dict for logs.
    raise
except TokenRefreshCooldownError as exc:
    # Retry later; exc.retry_after tells you how long to wait.
    raise
```

`pymedplum.*` also re-exports `InsecureTransportError` (raised at
construction for a non-HTTPS URL without opt-in) and
`UnsafeRedirectError` (raised when a follow-up URL — pagination, async
job polling, or a same-origin extraction from `if_none_exist` — points
at a different origin).

### Q: I'm getting rate limited (429 errors)

The client automatically retries with exponential backoff for rate limit errors. If you're still hitting limits:

1. Reduce request frequency
2. Use batch operations (GraphQL)
3. Implement application-level caching
4. Contact Medplum support for higher rate limits

## Advanced Topics

### Q: How do I use on-behalf-of functionality?

There are three ways to pass OBO, with a well-defined precedence order:
per-call kwarg beats the context manager, which beats the client
default. The empty-string kwarg (`on_behalf_of=""`) clears ambient OBO
for one call.

```python
# Per-call (wins over ambient state)
client.read_resource("Patient", "123", on_behalf_of="ProjectMembership/abc")

# Context manager (ambient for a block)
with client.on_behalf_of("ProjectMembership/abc"):
    client.read_resource("Patient", "123")

# Client default (baseline for the client's lifetime)
client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="...",
    client_secret="...",
    default_on_behalf_of="ProjectMembership/abc",
)
```

See [On-Behalf-Of](advanced/on_behalf_of.md) for the full precedence
rules, per-client isolation guarantees, and the `ThreadPoolExecutor`
propagation caveat.

### Q: How do I log every FHIR call for a PHI access audit trail?

Register an `on_request_complete` hook on the client. The hook fires
once per logical SDK call and receives a `RequestEvent` with method,
path, resource type/ID, OBO-as-sent per attempt, timings, and outcome.
Bodies and bearer tokens are never exposed. See
[Audit Logging](advanced/audit_logging.md) for the full contract and
worked examples (including DataDog and async hook variants).

### Q: What's `TokenRefreshCooldownError` and how should I handle it?

After a token-refresh failure, the client enters a cooldown window
(default 1 second, configurable via `failed_refresh_cooldown=`).
Subsequent calls that would trigger a refresh raise
`TokenRefreshCooldownError` instead of hammering the OAuth endpoint.
The exception carries `retry_after: float` (seconds remaining).

**Do not catch and retry in a tight loop.** Surface the error to your
caller or framework and respect `retry_after`:

```python
from pymedplum import TokenRefreshCooldownError

try:
    patient = client.read_resource("Patient", "123")
except TokenRefreshCooldownError as exc:
    raise TransientAuthError(retry_after=exc.retry_after) from exc
```

### Q: Why does my `http://` URL raise `InsecureTransportError`?

PyMedplum requires `https://` on `base_url` by default. Loopback hosts
(`127.0.0.1`, `::1`, `localhost`) are allowed without a flag — so
`http://localhost:8103/` works for local Docker setups. For any other
plain-HTTP URL, pass `allow_insecure_http=True` explicitly (logs a
WARNING). This is not recommended for production.

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

See [Administration](advanced/admin.md) for more examples.

## Still Need Help?

- Check the [API Reference](api_reference.md) for detailed method documentation
- Review [Advanced Usage](advanced_usage.md) for complex scenarios
- Consult the [FHIR Specification](https://hl7.org/fhir/) for FHIR-specific questions
- Open an issue on [GitHub](https://github.com/kinsteadhealth/pymedplum) for bugs or feature requests
