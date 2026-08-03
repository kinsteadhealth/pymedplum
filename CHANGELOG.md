# Changelog

Notable changes to pymedplum. Older releases are documented on the
[GitHub releases page](https://github.com/kinsteadhealth/pymedplum/releases).

## 0.6.0 (unreleased)

### Behavior change: 503 no longer replays non-idempotent requests

**The headline change.** The retry policy previously treated `503
Service Unavailable` as a pre-processing rejection and replayed it for
every method — including a bare `POST`. That assumption is unsound: a
draining pod mid-deploy can emit a 503 *after* committing the write, so
the replay could create a duplicate resource (a double `$book`, a
duplicate Patient).

503 now joins 502/504 in the ambiguous-commit set: it is retried only
for replay-safe requests — idempotent methods (`GET`/`PUT`/`DELETE`/
etc.) and `POST` carrying a real `If-None-Exist` query (FHIR
conditional create, where a replay is a server-side no-op). A bare
`POST` that draws a 503 now surfaces `ServerError` after one attempt.
`429` still retries every method; the (documented) assumption is that a
rate-limit rejection happens before the server processes the request.

There is no flag: this is the new default and only behavior. If a
create must survive retries, use `create_resource_if_none_exist` or
`conditional_create_batch`.

Related: `NetworkError` gains **`possibly_committed: bool`**,
aggregated across every wire attempt of the request — `False` when no
attempt ever went out (connect-phase failures only), `True` when any
attempt was sent before failing or drew an ambiguous 502/503/504, so
the origin may have committed. Apply the read-before-retry rule when
it's `True`.

### Added

- **Bundle response inspection** (`FHIRBundle`): `entry_results()`,
  `failures()`, `partition()`, and `raise_for_entry_errors()` parse
  per-entry `response.status` / `response.location` / `response.outcome`
  of batch and transaction responses into `BundleEntryResult` records.
  New `BundleEntryError` carries the failed entries with a PHI-safe
  `sanitize_for_logging()`. Documented plainly: Medplum
  `type: transaction` bundles are **not atomic on failure** — always
  inspect per-entry results.
- **`conditional_create_batch`** (sync + async): idempotent bulk
  creation. Builds chunked `type: batch` bundles of `ifNoneExist` POST
  entries and classifies each entry — `201` created, `200` existed,
  anything else collected on `BatchCreateResult.failed` (never raised).
  Replay-safe by construction, so ambiguous 5xx/transport failures
  retry safely mid-batch.
- **`update_with_retry`** (sync + async): the public read-modify-write
  primitive — read, run a mutator, write back with `If-Match` from the
  read's `meta.versionId`, re-read and re-run on 412 up to
  `max_retries`. Skips the PUT when the mutated state equals the remote
  (`UpdateResult.wrote is False`); `force=True` writes anyway. The
  three ProjectMembership access methods are now reimplemented on top
  of it (no behavior change — their suite passes unchanged).
- **`extensions` module**: `get_extension`, `get_extensions`,
  `get_extension_value`, `set_extension`, `upsert_extension`,
  `remove_extension`, `get_nested_value` — operating on raw dicts and
  generated Pydantic models alike — plus Medplum's slot/schedule
  service-tagging convention: `service_type_reference_extension()` /
  `read_service_type_references()` and `SERVICE_TYPE_REFERENCE_URL`
  (the shape of Medplum's `toCodeableReferenceLike`).
- **Parameters output parsing**: `parameters_to_dict`, `get_parameter`,
  `get_parameter_resource` invert `dict_to_parameters` for reading
  operation responses (including nested `part` and repeated names).
- **`execute_operation(..., as_fhir=Model)`**: parse an operation
  response into a typed model — direct responses only; a
  `Parameters`/`Bundle` wrapper raises with a pointer to the explicit
  unwrapping helpers.
- **`if_match="required"`** on `update_resource`: resolve
  `meta.versionId` or raise the new `MissingVersionIdError` — never
  degrade to an unguarded write (with `if_match=True`, a resource
  without a versionId silently sends no `If-Match` header).
- **`patch_resource(..., if_match='W/"<v>"')`**: explicit optimistic
  locking without hand-building headers.
- **`execute_transaction(..., accounts=...)`**: parity with
  `execute_batch` — stamps `meta.accounts` on every entry.

### Fixed

- `execute_transaction` no longer mutates the caller's bundle dict when
  forcing `type: "transaction"`.
- `update_resource` / `patch_resource` honor a caller-supplied
  `If-Match` header **case-insensitively**: a lowercase `if-match` in
  `headers=` now wins over the `if_match` keyword instead of both
  spellings being sent as a joined header value (the `update_resource`
  half of this predates 0.6.0).
