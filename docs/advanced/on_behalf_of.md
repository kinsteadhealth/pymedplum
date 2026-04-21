# On-Behalf-Of (OBO)

On-behalf-of (OBO) is a Medplum security mechanism that lets an
authenticated service act as a specific `ProjectMembership`. PyMedplum
sends the membership reference in the `X-Medplum-On-Behalf-Of` header
on every outbound request where OBO is active.

There are three ways to set OBO on a PyMedplum client. This page
walks through each, the precedence rules between them, and how OBO
interacts with async tasks and worker pools.

## Three ways to pass OBO

### 1. Per-call kwarg (wins over everything)

Pass `on_behalf_of=` directly to any request method:

```python
from pymedplum import MedplumClient

client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

patient = client.read_resource(
    "Patient",
    "123",
    on_behalf_of="ProjectMembership/abc",
)
```

Use this for security-critical calls where the acting identity must
be obvious at the call site — reviewers should not have to check
ambient state to know who the call was made as.

The empty string `on_behalf_of=""` **clears** the ambient OBO for
that one call (bypasses both the context manager and the client
default, sends no `X-Medplum-On-Behalf-Of` header).

### 2. Context manager (ambient for a block)

```python
with client.on_behalf_of("ProjectMembership/abc"):
    patient = client.read_resource("Patient", "123")
    conditions = client.search_resources("Condition", {"patient": "123"})
```

Async variant:

```python
from pymedplum import AsyncMedplumClient


async def handler():
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
    ) as client:
        async with client.on_behalf_of("ProjectMembership/abc"):
            patient = await client.read_resource("Patient", "123")
```

Use this when you have a logical scope (one HTTP handler, one
background task) that makes several calls as the same acting user.

### 3. Client default (baseline for the client's lifetime)

```python
client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    default_on_behalf_of="ProjectMembership/abc",
)

patient = client.read_resource("Patient", "123")
```

Use this when the client exists specifically to act as one
particular membership (for example, a per-user client in a worker
pool where each task gets its own fresh instance).

## Precedence rules

When more than one source is set, the SDK resolves OBO in this
order:

1. **Per-call kwarg** (explicit `on_behalf_of=...`) — wins if
   passed.
2. **Context manager** (ambient ContextVar set by
   `client.on_behalf_of(...)`).
3. **Client default** (`default_on_behalf_of=` constructor kwarg).
4. **None** — no `X-Medplum-On-Behalf-Of` header sent.

The empty string is treated as a **clear** at the per-call layer:
`client.read_resource("Patient", "123", on_behalf_of="")` sends
no header even if a context manager is active or a client default
is set.

## Per-client isolation

Each `MedplumClient` / `AsyncMedplumClient` instance owns its own
`ContextVar`. Setting OBO on client A never affects client B, even
in the same process and even when clients are rapidly created and
destroyed (a fresh ContextVar name — with a per-instance UUID
suffix — prevents the Python ContextVar machinery from recycling
state across instances).

```python
client_a = MedplumClient(base_url="https://api.medplum.com/")
client_b = MedplumClient(base_url="https://api.medplum.com/")

with client_a.on_behalf_of("ProjectMembership/actor-a"):
    # client_b still has no OBO set — isolation is per-instance.
    client_b.read_resource("Patient", "123")
```

## Async task isolation

Two concurrent `asyncio` tasks can each set different OBO values
on the same client, and each sees only its own — standard
`ContextVar` semantics under `asyncio`.

```python
import asyncio

from pymedplum import AsyncMedplumClient


async def act_as(client: AsyncMedplumClient, membership: str) -> dict:
    async with client.on_behalf_of(membership):
        return await client.read_resource("Patient", "123")


async def main() -> None:
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
    ) as client:
        a, b = await asyncio.gather(
            act_as(client, "ProjectMembership/actor-a"),
            act_as(client, "ProjectMembership/actor-b"),
        )
```

Each coroutine carries its own `ContextVar` state across `await`
points; the two gathered calls do not see each other's OBO.

## Thread propagation caveat

`ThreadPoolExecutor.submit` does **not** copy `ContextVar` state
into the worker thread. This code is broken:

```python
from concurrent.futures import ThreadPoolExecutor

# BROKEN — the submitted function does not see the outer OBO.
with client.on_behalf_of("ProjectMembership/abc"):
    with ThreadPoolExecutor() as pool:
        pool.submit(client.read_resource, "Patient", "123")
```

Safe patterns:

```python
import asyncio
import contextvars
from concurrent.futures import ThreadPoolExecutor


# Option A: asyncio.to_thread — copies context automatically.
async def ok_async():
    async with client.on_behalf_of("ProjectMembership/abc"):
        await asyncio.to_thread(client.read_resource, "Patient", "123")


# Option B: contextvars.copy_context().run — manual propagation.
def ok_threaded():
    with client.on_behalf_of("ProjectMembership/abc"):
        ctx = contextvars.copy_context()
        with ThreadPoolExecutor() as pool:
            pool.submit(ctx.run, client.read_resource, "Patient", "123")


# Option C: pass OBO explicitly — does not rely on propagation.
def ok_explicit():
    with ThreadPoolExecutor() as pool:
        pool.submit(
            client.read_resource,
            "Patient",
            "123",
            on_behalf_of="ProjectMembership/abc",
        )
```

Option C is usually the easiest to reason about in code review —
the acting identity is visible at the submission site.

## Worker / Celery / TaskIQ pattern

In a task-worker setup where each task acts on behalf of a
different user, the recommended pattern is a **fresh client per
task**, constructed with `default_on_behalf_of=` bound to that
task's acting membership:

```python
from pymedplum import AsyncMedplumClient


async def handle_patient_task(membership_id: str, patient_id: str):
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        default_on_behalf_of=membership_id,
    ) as client:
        return await client.read_resource("Patient", patient_id)
```

This is safer than reusing a long-lived shared client across tasks
for two reasons:

- **State isolation.** A fresh client cannot carry OBO state from
  a previous task. If a task forgets to exit a context manager on
  a shared client, that OBO could bleed into the next task running
  on the same worker thread.
- **Explicit identity.** The acting membership is visible at the
  client-construction site, which is the first thing a reviewer or
  debugger looks at.

If you must share a long-lived client, always use the per-call
kwarg or context manager — never rely on `default_on_behalf_of`
to be the right value for the current task.

## When to use which

| Situation | Recommended mechanism |
|---|---|
| Security-critical one-off call; acting identity must be obvious at the call site | Per-call kwarg |
| Handler that makes 5–10 calls as the same user | Context manager |
| Client that exists specifically to act as user X (e.g. per-task worker client) | Client default |
| Threaded code without `ContextVar` propagation | Per-call kwarg (safest) |
| Long-lived shared client across many users | Per-call kwarg or context manager; never rely on default |

## Relation to audit logging

Every `RequestEvent` dispatched to `on_request_complete` records
`on_behalf_of` **per wire attempt** under `event.attempts[i]`, so
your audit log always reflects what was sent on the wire — not a
snapshot taken at hook time. See
[Audit Logging](audit_logging.md) for the full hook contract.
