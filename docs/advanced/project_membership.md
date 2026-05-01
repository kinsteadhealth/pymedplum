# ProjectMembership Access

Three client methods for managing the parameterized AccessPolicy slice
of `ProjectMembership.access` — bulk replace, atomic add, atomic
remove — backed by `If-Match` optimistic concurrency and a 412 retry
loop. The end of this page has an
[About ProjectMembership](#about-projectmembership) appendix for
readers new to the resource model.

If you're skimming: jump to [What these methods do](#what-these-methods-do).

## What these methods do

Three methods, all on `MedplumClient` and `AsyncMedplumClient` with
identical signatures:

- `merge_project_membership_access` — replace the whole managed slice
  with a desired list. Use when you have the full intended state.
- `add_project_membership_access_entry` — atomically append one entry.
- `remove_project_membership_access_entry` — atomically remove one
  structurally-equal entry.

All three share the same contract:

1. **One atomic write.** Read the membership, compute the new
   `access` list, write it back with `If-Match` from `meta.versionId`.
   No partial states; no risk of clobbering a concurrent writer's
   changes silently.
2. **412 retry.** If a concurrent writer bumped the version between
   our read and our write, Medplum returns 412
   (`PreconditionFailedError`). The helper re-reads, re-applies the
   mutation against the new state, and retries up to `max_retries`
   times (default `1`, so two attempts total) before letting the
   exception propagate.
3. **Skip the PUT when nothing changed.** If the desired `access`
   list is byte-equal to what's already on the server, no write is
   sent and `result.updated` is `False`. Calling these helpers from
   a retry loop or a recovery script is therefore cheap.

## Calling merge

The realistic shape is "user belongs to N tenants" — pass one entry
per tenant. All entries reuse the same parameterized AccessPolicy;
only the `parameter` differs. Here Alice belongs to three practices:

```python
from pymedplum import (
    MedplumClient,
    make_project_membership_access,
)

client = MedplumClient(...)

result = client.merge_project_membership_access(
    "alice-membership-id",
    managed_access=[
        make_project_membership_access(
            "AccessPolicy/practice-policy",
            {"organization": "Organization/practice-a"},
        ),
        make_project_membership_access(
            "AccessPolicy/practice-policy",
            {"organization": "Organization/practice-b"},
        ),
        make_project_membership_access(
            "AccessPolicy/practice-policy",
            {"organization": "Organization/practice-c"},
        ),
    ],
    managed_policy_ids={"practice-policy"},
)
print(result.updated, result.version_id, result.managed_count)  # ... 3
```

To reassign Alice (drop practice-c, add practice-d), call merge again
with the new desired list. The helper diffs against the remote list
internally; the caller does not have to compute the diff. This is one
PUT regardless of how many entries change. An MSO staff member with
1000 active practice assignments writes 1000 entries on the days the
assignment changes and sends zero PUTs on the days it doesn't
(byte-equal short-circuit).

The async client mirrors the sync API exactly:

```python
from pymedplum import AsyncMedplumClient, make_project_membership_access

async with AsyncMedplumClient(...) as client:
    result = await client.merge_project_membership_access(
        "alice-membership-id",
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

## Adding or removing a single tenant

When you don't have the full desired list cached — a UI button click,
say — use the atomic single-entry methods. They do the read, take
the managed slice, mutate it, and write back inside the same 412
retry loop, so concurrent writes by other callers are preserved.

**Add a tenant:**

```python
client.add_project_membership_access_entry(
    membership_id,
    make_project_membership_access(
        "AccessPolicy/practice-policy",
        {"organization": "Organization/practice-d"},
    ),
    managed_policy_ids={"practice-policy"},
)
```

Idempotent: if a structurally-equal entry already exists in the
managed slice, no PUT is sent.

**Remove a tenant:** build the entry the same way the original was
built (the builder is canonical) and pass it in:

```python
client.remove_project_membership_access_entry(
    membership_id,
    make_project_membership_access(
        "AccessPolicy/practice-policy",
        {"organization": "Organization/practice-c"},
    ),
    managed_policy_ids={"practice-policy"},
)
```

Idempotent: if no matching entry exists, no PUT is sent.

Both methods send 1 GET + 1 PUT (or 1 GET + 0 PUTs if the operation
is a no-op). They are safe under concurrent writers: if another
caller adds or removes a different entry between the GET and the
PUT, Medplum returns 412, the helper re-reads, re-applies the
mutation against the new state, and retries. The other writer's
change is preserved.

## Building an access entry

```python
from pymedplum import make_project_membership_access

entry = make_project_membership_access(
    "AccessPolicy/abc",
    {"organization": "Organization/org-a"},
)
# {
#   "policy": {"reference": "AccessPolicy/abc"},
#   "parameter": [{
#     "name": "organization",
#     "valueReference": {"reference": "Organization/org-a"},
#   }]
# }
```

Policy and parameter values accept several shapes:

| Input | Result |
|-------|--------|
| `"abc"` (bare ID) | `{"reference": "AccessPolicy/abc"}` |
| `"AccessPolicy/abc"` | `{"reference": "AccessPolicy/abc"}` |
| `Reference(reference="AccessPolicy/abc")` | `{"reference": "AccessPolicy/abc"}` |
| `{"reference": "AccessPolicy/abc"}` | `{"reference": "AccessPolicy/abc"}` |

Parameter values:

- `"Organization/org-a"` (or any `ResourceType/id`) emits
  `valueReference`.
- `"active"` (no slash) emits `valueString`.
- `Reference(...)` and `{"reference": ...}` emit `valueReference`.

Other parameter shapes (CareTeam, HealthcareService, etc.) work
identically:

```python
make_project_membership_access(
    "AccessPolicy/care-team-policy",
    {"careTeam": "CareTeam/team-1"},
)
make_project_membership_access(
    "AccessPolicy/practice-policy",
    {"healthcareService": "HealthcareService/svc-9"},
)
```

If you already have a generated `ProjectMembershipAccess` model, pass
it through `merge_project_membership_access` directly — the helper
normalizes both shapes through `to_fhir_json`:

```python
from pymedplum.fhir import (
    ProjectMembershipAccess,
    ProjectMembershipAccessParameter,
    Reference,
)

entry = ProjectMembershipAccess(
    policy=Reference(reference="AccessPolicy/abc"),
    parameter=[
        ProjectMembershipAccessParameter(
            name="organization",
            value_reference=Reference(reference="Organization/org-a"),
        ),
    ],
)
```

## Inspecting existing entries

```python
from pymedplum import (
    get_project_membership_access_parameter,
    get_project_membership_access_policy_id,
)

membership = client.read_resource("ProjectMembership", "abc")
for entry in membership.get("access", []):
    policy_id = get_project_membership_access_policy_id(entry)
    org = get_project_membership_access_parameter(entry, "organization")
```

`get_project_membership_access_policy_id` returns `None` for malformed
entries (missing `policy`, non-`AccessPolicy` reference, etc.) instead
of raising.

## `managed_policy_ids` — what it is and why it's there

`managed_policy_ids` is a set of AccessPolicy IDs that your
application owns. Most apps in practice are the **only** writer of
`ProjectMembership.access` for the users they manage, so this is a
singleton like `{practice_policy_id}` and never grows.

When you call merge:

- Existing entries pointing at a policy in this set get **replaced**
  by `managed_access`.
- Entries pointing at any other policy are **preserved untouched**.

If your app is the only writer (the common case), the "other policy"
branch is dead code — there are no other entries, so the partition
has nothing to preserve. You can verify this with `git grep` or a
one-time read of representative memberships before going live.

The branch exists for two reasons that are cheap to defend against
and expensive to debug if they happen:

1. **Manual admin edits.** If somebody opens Medplum's admin UI and
   adds an entry by hand to debug a permissions issue, a later sync
   from your application won't silently delete it.
2. **Policy rotation.** If you ever recreate the AccessPolicy
   resource (different ID), pass `{old_id, new_id}` during the
   rollout window. Entries pointing at the old ID get cleaned up
   the first time the new policy is the only one in `managed_access`.

If neither concern applies, you can effectively ignore
`managed_policy_ids` after wiring it once — pass the same singleton
on every call.

Empty sets are rejected, because "manage no policies" plus "write
this list of entries" can't be reconciled — the helper would have
no way to clean up entries it later wrote.

## Removing all managed access (lockout)

Pass `managed_access=[]` to revoke every entry your app previously
wrote, while leaving anything else alone:

```python
client.merge_project_membership_access(
    "abc",
    managed_access=[],
    managed_policy_ids={"practice-policy"},
)
```

The helper rejects entries in `managed_access` whose policies are
*outside* `managed_policy_ids` for exactly this reason: if it ever
created an entry with an unmanaged policy, a later
`managed_access=[]` couldn't clean it up.

## Idempotency

`force=False` (the default) compares the merged list to the remote
`access` via canonical JSON. If they match, no PUT is sent and
`result.updated` is `False`. At-least-once event handlers and
recovery scripts can call merge repeatedly without churning
`versionId`.

```python
# Safe to re-run on the same desired_entries: only writes when
# something actually changed.
client.merge_project_membership_access(
    membership_id,
    managed_access=desired_entries,
    managed_policy_ids={"practice-policy"},
)
```

`force=True` writes regardless. Useful when you specifically need a
fresh `versionId` for downstream auditing.

## 412 retry contract

The helper auto-attaches `If-Match: W/"<versionId>"` from the read
membership. A 412 (`PreconditionFailedError`) means a concurrent
writer landed between our read and our write — the helper re-reads,
rebuilds the merged list against the new state, and retries up to
`max_retries` times (default `1` — so two attempts total). After
that, the exception propagates:

```python
from pymedplum import PreconditionFailedError

try:
    client.merge_project_membership_access(
        membership_id,
        managed_access=desired_entries,
        managed_policy_ids={"practice-policy"},
        max_retries=3,
    )
except PreconditionFailedError:
    # Sustained contention. Back off and try later, or accept
    # eventual consistency and move on.
    ...
```

If the read response lacks `meta.versionId`, the helper raises
`ValueError` *before* writing. It will not PUT without optimistic
concurrency.

## Patient-scoped memberships

Everything above used Practitioner profiles and Organization tenants
because that's the most concrete MSO example. The same primitives
apply when the parameterized AccessPolicy is patient-scoped instead
of organization-scoped — only the policy and the parameter name
change.

Two patient-scoped patterns matter in practice. Medplum documents
both in
[Access Policies → Patient Access / Caregiver Access](https://www.medplum.com/docs/access/access-policies#patient-access).

**Special-case behavior to know about.** Medplum's access-policy
resolver auto-injects two parameters when it builds the effective
policy at request time
(see
[`server/src/fhir/accesspolicy.ts`](https://github.com/medplum/medplum/blob/main/packages/server/src/fhir/accesspolicy.ts)):

- `profile` — always set to the membership's `profile` reference.
- `patient` — set to the membership's `profile` reference *unless*
  the access entry already provides a `patient` parameter.

The `patient` default is the source of two patterns below.

**1. Patient self-access.** A Patient User logs in to a portal
scoped to their own record via a templated policy whose compartment
is `%patient`. Because Medplum auto-defaults `patient` to the
profile reference (and the profile is `Patient/<id>`), the
application does *not* need to write any `access` entry — the
default does the right thing. Medplum's
[open patient registration](https://www.medplum.com/docs/user-management/open-patient-registration)
flow leans on this. If you do manage it explicitly anyway:

```python
make_project_membership_access(
    "AccessPolicy/patient-access-policy-template",
    {"patient": "Patient/<patient-id>"},
)
```

In short: don't reach for these helpers for self-access patient
memberships unless you're consciously overriding Medplum's default.

**2. Caregiver access.** A parent, guardian, or proxy gets one
access entry per Patient they're authorized to see, all referencing
the same templated patient-access policy. The
[Medplum invite docs](https://www.medplum.com/docs/app/invite) name
`RelatedPerson` as the natural profile for a caregiver who isn't
themselves a patient.

For this case the application *must* specify `patient` explicitly on
each entry — Medplum's auto-default would otherwise resolve
`%patient` to the RelatedPerson reference, which is the wrong
compartment.

The wire shape and our helpers are identical to the
practice-assignment example — substitute `Patient` for `Organization`
and the patient-access policy for the practice policy:

```python
client.merge_project_membership_access(
    caregiver_membership_id,
    managed_access=[
        make_project_membership_access(
            "AccessPolicy/patient-access-policy-template",
            {"patient": "Patient/child-a"},
        ),
        make_project_membership_access(
            "AccessPolicy/patient-access-policy-template",
            {"patient": "Patient/child-b"},
        ),
    ],
    managed_policy_ids={"patient-access-policy-template"},
)
```

`add_project_membership_access_entry` and
`remove_project_membership_access_entry` work the same way for
adding or revoking access to one Patient at a time, with the same
atomic concurrency guarantees.

**One caveat for both patterns:** the parameter *name* must match
the AccessPolicy template's variable. A policy using `%patient`
requires `{"patient": "Patient/..."}`; a policy using `%care_team`
requires `{"careTeam": "CareTeam/..."}`. Mismatches don't fail
client-side — Medplum accepts the entry but the variable just
doesn't get bound — so verify against the AccessPolicy you
reference.

## What these helpers do NOT do

- They do not modify `ProjectMembership.accessPolicy`. That legacy
  single-policy field has been superseded by `access`; if you have
  callers still using it, migrate them — these helpers won't.
- They do not change `ProjectMembership.admin` or
  `ProjectMembership.active`. Admin elevation and membership
  revocation are separate operations.
- They do not assign account compartments. Use
  [`set_accounts`](operations.md#multi-tenant-accounts-set-accounts)
  for that. The two are complementary: `set_accounts` puts a Patient
  under a tenant; `merge_project_membership_access` gives a user
  access to that tenant.

---

## About ProjectMembership

The rest of this page is orientation for readers new to the
ProjectMembership resource model. Skip if you already know it.

A Medplum server hosts multiple **Projects**, each isolated from the
others — a Project is the unit of multi-tenancy at the server level.
Each Project has its own set of resources, its own AccessPolicies, and
its own users.

A **ProjectMembership** is the resource that grants a principal
access to a Project. The principal (the membership's `user` field)
is one of:

- `User` — a human login identity
- `Bot` — an automation script that runs inside the project
- `ClientApplication` — a machine-to-machine integration identity

Each membership also pins the principal to a **profile** within the
project — the FHIR resource that represents how they participate.
Allowed profile types are:

- `Practitioner` — clinicians and staff
- `Patient` — patients with portal logins
- `RelatedPerson` — family members, caregivers, or other delegated
  parties
- `Bot` and `ClientApplication` — for non-human principals, where
  `user` and `profile` typically reference the same resource

The membership also carries the principal's permission shape inside
the project:

- `accessPolicy` — a single AccessPolicy reference (legacy field,
  superseded by `access`)
- `access` — the list of parameterized AccessPolicy bindings this
  page is about
- `admin` — project-admin flag
- `active` — whether the membership is currently usable

A single `User` can belong to multiple Projects via separate
ProjectMembership resources.

`ProjectMembership.access` is a list on that row. Each entry binds the
principal to a parameterized AccessPolicy with specific parameter
values. For multi-tenancy *within a Project* (e.g., one Project per
customer, many Organizations representing practices inside it), each
entry represents one tenant the user can see. See Medplum's
[Multi-Tenant Access Policy guide](https://www.medplum.com/docs/access/multi-tenant-access-policy)
for the data model — what entries look like, how `%organization` /
`%care_team` / `%healthcare_service` parameters get substituted at
runtime, and how the resulting compartments restrict reads.

### Why `access` matters in practice

Whenever a request is authenticated as a particular ProjectMembership,
Medplum applies that membership's `accessPolicy` plus each entry in
`access` (with parameter substitution) to the call. That happens in
two situations:

- **A user logging in directly** — through Medplum's web app, a
  custom UI you've built against Medplum's auth, or any OAuth/OIDC
  flow that resolves to a ProjectMembership. Their search results,
  reads, writes, and GraphQL queries are all filtered by their
  membership's access rules.
- **Your code acting on their behalf** — via PyMedplum's OBO context
  manager (`client.on_behalf_of(membership_id)`) or a client-wide
  `default_on_behalf_of`. PyMedplum sends `X-Medplum-On-Behalf-Of`
  with the membership ID, and Medplum applies *that* membership's
  rules instead of the calling client's. The calling identity's own
  permissions act as a ceiling, but within the ceiling the effective
  policy is the OBO target's.

Either way, `ProjectMembership.access` is what determines what the
principal can see and do. Getting this list right is the point. See
[On-Behalf-Of](on_behalf_of.md) for the OBO mechanics themselves.

### Where ProjectMembership IDs come from

You'll typically have an ID handy because you got it from
`invite_user`:

```python
membership = client.invite_user(
    project_id="...",
    resource_type="Practitioner",
    first_name="Alice", last_name="Smith",
    email="alice@example.com",
)
membership_id = membership["id"]   # this is what merge takes
```

Or by searching for an existing membership when you don't have it
cached:

```python
result = client.search_one(
    "ProjectMembership",
    {"user": f"User/{user_id}", "project": f"Project/{project_id}"},
)
membership_id = result["id"]
```
