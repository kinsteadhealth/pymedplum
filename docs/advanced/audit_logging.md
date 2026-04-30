# Audit Logging

PyMedplum exposes a single completion hook, `on_request_complete`, that
fires once per logical SDK request (one call to `read_resource`,
`search_resources`, `create_resource`, etc. — regardless of how many
wire attempts it took to complete). This hook is designed for one job:
producing a durable, long-term PHI-access audit trail.

## What the hook is for

`on_request_complete` is an **audit primitive**, not an observability
primitive. If you want latency histograms, distributed traces, or
error budgets, reach for OpenTelemetry, DataDog APM, or a metrics
library instead. If you need to answer "which user touched which
patient at what time and did it succeed?" — this hook is the right
place to do it.

One hook invocation corresponds to one logical call. Retries are
folded in as `RequestEvent.attempts`; the hook still fires exactly
once.

## `RequestEvent` fields

Every hook invocation receives a single `RequestEvent` dataclass.

| Field | Type | PHI-bearing? | Notes |
|---|---|---|---|
| `method` | `str` | No | HTTP verb (`GET`, `POST`, ...). |
| `path` | `str` | **Yes** | Full wire path, including resource IDs. Safe to emit to a PHI-qualified audit log; never to a metrics pipeline. |
| `path_template` | `str` | No | `path` with concrete IDs substituted for `{id}`. Use this for metric tags and non-PHI logs. |
| `query_params` | `dict[str, list[str]] \| None` | **Yes** | Parsed search parameters. Routinely carries identifiers. Omitted from `to_phi_audit_dict()` unless `include_query_params=True`; never included in `to_non_phi_dict()`. |
| `resource_type` | `str \| None` | No | FHIR resource type (`"Patient"`, `"Observation"`, ...) or `None` for non-FHIR paths. |
| `resource_id` | `str \| None` | **Yes when non-null** | Resource ID parsed out of the path. |
| `operation` | `str \| None` | No | FHIR operation name (`"$match"`, `"$everything"`, ...) or `None`. |
| `started_at` | `datetime` | No | UTC timestamp when the logical call began. |
| `ended_at` | `datetime` | No | UTC timestamp when the logical call finished (success or exception). |
| `attempts` | `list[RequestAttempt]` | Mixed | Per-wire detail. See below. |
| `final_status_code` | `int \| None` | No | Status from the final attempt (or `None` on network exception). |
| `final_exception` | `BaseException \| None` | Mixed | The exception surfaced to the caller, if any. |
| `action` | `RequestAction \| None` | No | FHIR action category: `read`, `search`, `create`, `update`, `patch`, `delete`, `operation`, `batch_or_transaction`, or `None` for non-FHIR calls (auth, system endpoints). Use this to skip non-FHIR calls (auth/system endpoints) without parsing the URL yourself. |
| `outcome` | `RequestOutcome` | No | `"success"` if the request finished with a 2xx/3xx and no exception; `"error"` otherwise (including network failures). |

The event as a whole is **PHI-bearing by design**. Route it to a
destination that is cleared to store PHI (a compliance audit log,
not a shared observability pipeline).

## `RequestAttempt` fields

| Field | Type | Notes |
|---|---|---|
| `attempt_number` | `int` | 1-based. |
| `status_code` | `int \| None` | HTTP status; `None` if the attempt raised a network error before any response. |
| `duration_seconds` | `float` | Wall-clock duration of this one wire attempt. |
| `on_behalf_of` | `str \| None` | The OBO membership sent on the wire for this attempt. **Always `None` for `/oauth2/token` attempts** regardless of client state. |
| `exception` | `BaseException \| None` | The exception raised on this attempt, if any (retried attempts have values here; the final successful attempt does not). |

## Deliberately NOT in the event

The SDK does not surface the following, by design:

- **Bearer tokens.** Never.
- **Request or response bodies.** Any length, any shape.
- **Full stack traces.** The `final_exception` is the caller-visible
  exception only; not the wrapped traceback chain.
- **Arbitrary header values** other than the URL path and the
  on-wire OBO value.

Each of these is either a credential-leak risk or an unbounded
PHI-leak risk.

## Serializing the event

`RequestEvent` exposes two named serializers; the choice is the
explicit decision about whether the destination is contractually
approved for PHI.

```python
from pymedplum.hooks import RequestEvent

def dispatch(event: RequestEvent) -> None:
    # Full PHI-bearing payload for the audit sink.
    phi_payload = event.to_phi_audit_dict()

    # Include parsed search params when the resource type warrants it.
    phi_payload_with_query = event.to_phi_audit_dict(include_query_params=True)

    # Shape-only payload for general observability backends.
    metrics_payload = event.to_non_phi_dict()
```

`to_phi_audit_dict()` includes the resolved `path`, parsed
`resource_id`, and per-attempt `on_behalf_of` — these are PHI- or
access-control-sensitive even with `query_params` omitted. Use it
only for sinks authorized to receive PHI.

`to_non_phi_dict()` strips those fields and keeps shape and timing
data only: `path_template` (e.g. `/Patient/{id}`), `resource_type`,
`operation`, attempt counts, status codes, durations, and
exception type names. Use it for metrics, APM, error trackers, and
any third-party log aggregator not contractually qualified for PHI.

Both methods return JSON-serializable primitives: strings, numbers,
booleans, lists, dicts, and ISO-8601 timestamps.

## Per-resource-type query-param policy

The SDK does not decide which searches are worth auditing verbatim —
that policy belongs in the caller. A typical pattern opts in per
resource type:

```python
from pymedplum.hooks import RequestEvent

PHI_RESOURCE_TYPES = {"Patient", "Observation", "Encounter", "Condition"}

def audit_phi_access(event: RequestEvent) -> None:
    if event.action is None:
        return  # non-FHIR call (auth, system endpoint) — not PHI access
    include_qp = event.resource_type in PHI_RESOURCE_TYPES
    payload = event.to_phi_audit_dict(include_query_params=include_qp)
    phi_audit_log.info("medplum_request_complete", extra={"event": payload})
```

The `action is None` early-return is the canonical way to skip
non-FHIR calls (e.g. `/oauth2/token`) without parsing the URL
yourself.

## Routing two destinations from one hook

A single hook can split the event across a PHI-qualified audit store
and a non-PHI metrics pipeline:

```python
from pymedplum.hooks import RequestEvent

def dispatch(event: RequestEvent) -> None:
    # PHI destination — full path, resource_id, OBO per attempt.
    phi_audit_log.info(
        "phi_access", extra={"event": event.to_phi_audit_dict()}
    )

    # Non-PHI destination — path_template only, no resource_id, no OBO.
    metrics_log.info(
        "medplum_request_metrics", extra={"event": event.to_non_phi_dict()}
    )
    metrics.increment(
        "medplum.request",
        tags={
            "method": event.method,
            "path_template": event.path_template,
            "resource_type": event.resource_type or "none",
            "status": str(event.final_status_code or 0),
        },
    )
    if event.started_at and event.ended_at:
        metrics.timing(
            "medplum.request.duration_ms",
            (event.ended_at - event.started_at).total_seconds() * 1000,
            tags={"path_template": event.path_template},
        )
```

Same hook, two destinations, clean separation. The metrics branch
never sees `event.path` or `event.resource_id`.

## Basic example: sync audit logger

```python
import logging

from pymedplum import MedplumClient
from pymedplum.hooks import RequestEvent

audit_log = logging.getLogger("kinstead.phi_access")


def record_phi_access(event: RequestEvent) -> None:
    audit_log.info(
        "phi_access",
        extra={
            "audit": event.to_phi_audit_dict(),
            "actor": current_user_id(),
        },
    )


client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    on_request_complete=record_phi_access,
)
```

## DataDog example

> **PHI destination only.** The example below ships
> `to_phi_audit_dict()` to a third-party log ingestion endpoint.
> Use this shape only when your DataDog org (or other destination)
> is contractually and operationally approved to store PHI. For a
> non-PHI metrics pipeline, route `to_non_phi_dict()` instead — see
> the "Routing two destinations" section above.
>
> **Production note**: offload the HTTP post to a background worker
> — a failing ingest endpoint should not contribute to SDK latency.
> The example below is illustrative of the payload shape, not a
> production-ready implementation.

```python
import json

import requests

from pymedplum import MedplumClient
from pymedplum.hooks import RequestEvent

DATADOG_LOGS_URL = "https://http-intake.logs.datadoghq.com/api/v2/logs"


def ship_to_datadog(event: RequestEvent) -> None:
    payload = {
        "ddsource": "pymedplum",
        "service": "phi-audit",
        "message": "medplum_request_complete",
        "event": event.to_phi_audit_dict(),
    }
    requests.post(
        DATADOG_LOGS_URL,
        headers={"DD-API-KEY": datadog_api_key()},
        data=json.dumps(payload),
        timeout=2.0,
    )


client = MedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    on_request_complete=ship_to_datadog,
)
```

## Async hook example

Async hooks work only with `AsyncMedplumClient`. Passing an `async
def` hook to the synchronous client raises `TypeError` at
construction time.

```python
import asyncio

from pymedplum import AsyncMedplumClient
from pymedplum.hooks import RequestEvent


async def record_phi_access(event: RequestEvent) -> None:
    await audit_log_writer.write(event.to_phi_audit_dict())


async def main() -> None:
    async with AsyncMedplumClient(
        base_url="https://api.medplum.com/",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        on_request_complete=record_phi_access,
    ) as client:
        await client.read_resource("Patient", "123")


asyncio.run(main())
```

## Attaching caller-side user identity

The hook runs synchronously in the caller's stack, so any
`ContextVar` or thread-local state set before the SDK call is
readable from inside the hook. This is how you correlate an SDK
call back to an end user without the SDK needing to know about
your identity model.

### Django-style example

```python
from contextvars import ContextVar

from pymedplum import AsyncMedplumClient
from pymedplum.hooks import RequestEvent

current_user: ContextVar["User | None"] = ContextVar("current_user", default=None)


def audit_phi_access(event: RequestEvent) -> None:
    actor = current_user.get()
    phi_audit_log.write(
        {
            "actor_user_id": actor.id if actor else None,
            **event.to_phi_audit_dict(),
        }
    )


client = AsyncMedplumClient(
    base_url="https://api.medplum.com/",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    on_request_complete=audit_phi_access,
)


async def patient_detail(request, patient_id):
    current_user.set(request.user)

    patient = await client.read_resource(
        "Patient",
        patient_id,
        on_behalf_of=request.user.medplum_membership_id,
    )
    return patient
```

The per-call `on_behalf_of` kwarg is the safest pattern for
security-critical calls — the acting identity is visible at the
call site, not hidden in ambient state. The hook sees it per
attempt in `event.attempts[i].on_behalf_of`.

### Context manager for handler-scoped code

For a handler that makes multiple PHI-touching calls as the same
acting user, the OBO context manager is ergonomic:

```python
async def sync_patient_data(request, patient_id):
    current_user.set(request.user)

    async with client.on_behalf_of(request.user.medplum_membership_id):
        patient = await client.read_resource("Patient", patient_id)
        conditions = await client.search_resources(
            "Condition", {"patient": patient_id}
        )
        observations = await client.search_resources(
            "Observation", {"patient": patient_id}
        )
```

Each of the three calls fires the hook once, each carrying the
acting membership in `attempts[0].on_behalf_of`. When the `async
with` block exits, the ambient OBO is cleared.

## Threaded / worker-pool code

Plain `ThreadPoolExecutor.submit` does **not** propagate
`ContextVar` state. If you set `current_user.set(...)` in the
caller and then submit a task to a raw thread pool, the hook
running inside that task will see the default `current_user` value,
not the caller's.

Two safe patterns:

```python
import asyncio
import contextvars
from concurrent.futures import ThreadPoolExecutor


# Option A: asyncio.to_thread — copies context automatically.
async def handler(request):
    current_user.set(request.user)
    await asyncio.to_thread(do_phi_work, request)


# Option B: contextvars.copy_context().run — manual propagation.
def submit_with_context(pool: ThreadPoolExecutor, fn, *args):
    ctx = contextvars.copy_context()
    return pool.submit(ctx.run, fn, *args)
```

If you do not want to rely on context propagation at all, pass
`on_behalf_of=` explicitly on every SDK call inside the threaded
work — the hook will still record it per attempt.

## Hook failure semantics

Hook exceptions are caught and logged at WARNING under the
`pymedplum.hooks` logger. They never propagate to the caller. A
buggy audit logger will not cause patient reads to fail.

If you need dead-letter handling or hook-failure metrics, implement
them inside the hook — the SDK does not provide a DLQ. A
defensive template:

```python
def record_phi_access(event: RequestEvent) -> None:
    try:
        phi_audit_log.info(
            "phi_access", extra={"audit": event.to_phi_audit_dict()}
        )
    except Exception:
        hook_failure_counter.increment()
        raise
```

## Retry visibility

A `RequestEvent.attempts` list with three entries — for example,
two 429 responses followed by a 200 — looks roughly like this
(illustrative shape):

```python
# attempt 1: 429, 0.05s wall, OBO "ProjectMembership/abc"
# attempt 2: 429, 0.12s wall, OBO "ProjectMembership/abc"
# attempt 3: 200, 0.08s wall, OBO "ProjectMembership/abc"
```

Aggregate stats from the event:

```python
total_wall = (event.ended_at - event.started_at).total_seconds()
retry_count = len(event.attempts) - 1
per_wire_seconds = sum(a.duration_seconds for a in event.attempts)
backoff_seconds = total_wall - per_wire_seconds
```

## What the hook is NOT for

- Not a transport-tracing hook. Use OpenTelemetry for span emission.
- Not a request-mutation hook. Use `before_request` for that.
- Not a response-body-inspection hook. Do that in caller code
  around the SDK call — the hook never sees bodies.

## Cross-reference: `on_behalf_of`

The event records the OBO membership **as it was sent on the
wire per attempt**, not a snapshot taken at hook time. If the
ambient OBO changes mid-flight (for example, a caller exits a
context manager between retries), each attempt in `event.attempts`
reflects what the SDK actually sent on that attempt.

See [On-Behalf-Of](on_behalf_of.md) for precedence rules and
per-client isolation guarantees.
