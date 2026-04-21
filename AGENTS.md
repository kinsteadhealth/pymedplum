# Agent Instructions for PyMedplum

This document provides instructions for AI agents to contribute to the PyMedplum project.

## Development Environment

- Use `make install-dev` to install all dependencies, including development and testing tools.
- This project uses `ruff` for linting and formatting, and `mypy` for type checking.

## Python version

This project targets **Python 3.10+**. Use modern syntax:

- `X | Y` union syntax (PEP 604) instead of `Union[X, Y]`.
- `from __future__ import annotations` in new modules when circular
  imports or stringified types are in play.
- `match` statements where they clarify structural dispatch.

## Testing

- Run all tests with `make test`.
- Run unit tests only with `make test-unit`.
- Run integration tests only with `make test-integration`.
- Make sure all tests pass before submitting a pull request.
- **HTTP mocking**: use `respx` for all new tests. Do not add new
  `responses`-based tests — existing ones will migrate separately.

### Integration Tests

- Integration tests require a running Medplum server.
- You must create a `.env` file in the root of the project with the following variables:
  - `MEDPLUM_BASE_URL`
  - `MEDPLUM_CLIENT_ID`
  - `MEDPLUM_CLIENT_SECRET`
- The `passenv` configuration in `tox.ini` will make these environment variables available to the integration tests.

## Code Quality

- Run `make check` to run all code quality checks, including linting, formatting, and type checking.
- Run `make lint` to automatically fix linting issues.
- Run `make format` to format the code.
- Run `make type-check` to run the type checker.

### Typing

- Modules touched by security / auth / transport code
  (`pymedplum._security`, `pymedplum._auth`, `pymedplum._retry`,
  `pymedplum.hooks`, `pymedplum.exceptions`, and client/request
  internals) have `mypy strict = true` via `pyproject.toml` overrides.
  New code in those modules must type-check under `--strict`.
- `pymedplum.fhir.*` is intentionally excluded from strict typing
  until the generator is updated.

## Architecture conventions

### Concurrency primitives

For single-flight refresh patterns, use `concurrent.futures.Future`
(sync) or `asyncio.Task` + `asyncio.shield` (async). Do not hand-roll
coordination with multiple `threading.Event` objects — `Future`
handles exception propagation correctly, `Event` doesn't.

### Hooks

`on_request_complete` hooks must never cause the calling request to
fail. If you add new hook types, follow the same pattern: catch
exceptions at the dispatch site and log at WARNING under
`pymedplum.hooks`. Callers treat audit logs as advisory; a buggy hook
must not break PHI reads.

### OBO

When adding a new request method, accept
`on_behalf_of: str | None = None` as a keyword-only parameter and
resolve via `self._resolve_on_behalf_of(...)`. Never read the ambient
ContextVar directly — the resolver implements the full precedence
order (kwarg > context manager > client default > None) and empty-
string-clears semantics. Doing it yourself will drift.

### Headers

Never log bearer tokens, `X-Medplum-On-Behalf-Of` values, or arbitrary
header dicts in full. If a log line needs an identifier, use an
internal SDK-generated correlation ID or a short non-reversible digest
of the upstream value — not the raw credential.

### Module boundaries

- New URL / transport validators go in `pymedplum/_security.py`.
- New retry / backoff logic goes in `pymedplum/_retry.py`.
- New stateful token or OBO logic goes in `pymedplum/_auth.py`.
- Keep `client.py` / `async_client.py` as thin consumers of these
  modules. Request orchestration belongs in `_base.py`.

## Logging

### Namespace

All SDK logs live under the `pymedplum.*` namespace. Use
`logging.getLogger('pymedplum.auth')`, `'pymedplum.retry'`,
`'pymedplum.request'`, `'pymedplum.security'`, or `'pymedplum.hooks'`
depending on the subsystem. Do not create loggers outside this tree.

### Levels

Pick the level by what the operator needs to see:

- **WARNING** — SDK is degraded or the caller's expectations broke.
  Token refresh failed, cooldown entered, hook raised,
  `OnBehalfOfContext` cross-context reset, explicit
  `allow_insecure_http` opt-in.
- **INFO** — state transition an operator wants to see by default.
  Must be paired with a prior WARNING (recovery signal). Examples:
  "refresh recovered after N prior failures", "cooldown cleared."
  **Routine success is NOT INFO** — that's DEBUG.
- **DEBUG** — routine trace info. Proactive refresh triggered, OBO
  resolution source, 429 `Retry-After` parsing, per-wire attempt
  details, repeated cooldown hits during an already-reported outage.
  Off by default.
- **Do not use ERROR or CRITICAL.** The SDK does not know the
  operator's severity model. Raise an exception and let the caller
  decide.

### PHI discipline

Every log line at every level must be safe to emit in production.
Never log:

- Bearer tokens, `X-Medplum-On-Behalf-Of` values, or any header value
  that might carry credentials.
- Request bodies or response bodies (any length, any shape).
- Resource IDs, MRNs, or any value that could identify a specific
  patient.
- Query strings (FHIR search params routinely include identifiers).
- The `path` field from `RequestEvent` (PHI-bearing by design). Always
  use `path_template` instead.
- Exception messages where the message string might contain
  server-provided content. Use `type(exc).__name__` instead; include
  the message only for a controlled allow-list (`ValueError`,
  `TypeError`, etc. where the SDK constructed the string).

Safe to log: `path_template`, HTTP status codes, duration deltas,
exception class names, cooldown remaining time, structured
state-machine transition names.

If you're tempted to interpolate a variable that *might* carry PHI,
log the shape instead (`len(body)`, `type(exc).__name__`) or drop the
line.

### Testing

`pymedplum/tests/unit/test_logging.py` contains the PHI-in-logs
invariants. New log lines that could plausibly carry sensitive
content should be added to that test's capture-and-assert list. Run
it before merging any change that touches logging.

## Docs

If you change a public API surface, update `docs/api_reference.md`,
the relevant section of `docs/advanced/*`, and any examples in
`README.md` / `docs/quickstart.md`. Run `mkdocs build --strict`
before committing — the nav is checked.

## Pull Requests

- Before submitting a pull request, please run `make check` and `make test`.
- Ensure your PR title and description are clear and concise.
- If your PR addresses an issue, please reference the issue number in the description.

## Coding Style

- Follow the existing coding style.
- Use type hints for all function signatures.
- Keep functions small and focused on a single task.
- Prefer self-explanatory code; use comments sparingly and only where
  they add real context.
- When adding new features, please also add corresponding tests.
