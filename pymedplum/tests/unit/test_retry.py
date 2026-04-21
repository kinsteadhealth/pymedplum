import json

import httpx

from pymedplum._retry import MAX_RETRY_DELAY_SECONDS, parse_retry_after_429


def _resp(
    body: bytes | str | dict,
    *,
    headers: dict | None = None,
    status: int = 429,
) -> httpx.Response:
    if isinstance(body, dict):
        content = json.dumps(body).encode()
    elif isinstance(body, str):
        content = body.encode()
    else:
        content = body
    return httpx.Response(
        status,
        headers=headers or {},
        content=content,
    )


def test_msBeforeNext_parsed():  # noqa: N802
    body = {
        "resourceType": "OperationOutcome",
        "issue": [{"diagnostics": json.dumps({"_msBeforeNext": 2000})}],
    }
    assert parse_retry_after_429(_resp(body)) == 2.0


def test_msBeforeNext_hostile_value_capped():  # noqa: N802
    body = {
        "resourceType": "OperationOutcome",
        "issue": [{"diagnostics": json.dumps({"_msBeforeNext": 31_536_000_000})}],
    }
    assert parse_retry_after_429(_resp(body)) == MAX_RETRY_DELAY_SECONDS


def test_malformed_diagnostics_fallback():
    body = {
        "resourceType": "OperationOutcome",
        "issue": [{"diagnostics": "not json"}],
    }
    assert parse_retry_after_429(_resp(body)) == 1.0


def test_retry_after_seconds():
    r = _resp(b"not json", headers={"Retry-After": "5"})
    assert parse_retry_after_429(r) == 5.0


def test_retry_after_seconds_capped():
    r = _resp(b"not json", headers={"Retry-After": "86400"})
    assert parse_retry_after_429(r) == MAX_RETRY_DELAY_SECONDS


def test_retry_after_http_date():
    import email.utils
    import time

    future = email.utils.formatdate(time.time() + 10, usegmt=True)
    r = _resp(b"", headers={"Retry-After": future})
    v = parse_retry_after_429(r)
    assert 0 <= v <= MAX_RETRY_DELAY_SECONDS


def test_no_hint_fallback():
    assert parse_retry_after_429(_resp(b"")) == 1.0


def test_max_delay_seconds_kwarg_overrides_default():
    """Caller can tighten the cap to defend against slow upstreams."""
    body = b'{"issue":[{"diagnostics":"{\\"_msBeforeNext\\": 30000}"}]}'
    # Default: capped at 60s; here _msBeforeNext = 30s, so returned as-is
    assert parse_retry_after_429(_resp(body)) == 30.0
    # Tighter cap: returned value clipped to 5s
    assert parse_retry_after_429(_resp(body), max_delay_seconds=5.0) == 5.0


def test_max_delay_seconds_applies_to_retry_after_header():
    r = _resp(b"", headers={"Retry-After": "120"})
    assert parse_retry_after_429(r, max_delay_seconds=10.0) == 10.0


def test_non_utf8_body_no_crash():
    assert parse_retry_after_429(_resp(b"\x00\xff garbage")) == 1.0
