"""Retry policy for transient failures. Extracted from client.py / async_client.py
to dedupe the 429 parsing that originally caused an UnboundLocalError.
"""

from __future__ import annotations

import email.utils
import json
import logging
import time
from typing import Any

import httpx

logger = logging.getLogger("pymedplum.retry")

MAX_RETRY_DELAY_SECONDS: float = 60.0
_FALLBACK_SECONDS: float = 1.0

RETRYABLE_STATUS_CODES: tuple[int, ...] = (429, 502, 503, 504)


def _cap(value: float, max_delay: float = MAX_RETRY_DELAY_SECONDS) -> float:
    return max(0.0, min(value, max_delay))


def _try_ms_before_next(response: httpx.Response) -> float | None:
    try:
        payload: Any = response.json()
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    issues = payload.get("issue")
    if not isinstance(issues, list):
        return None
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        diag = issue.get("diagnostics")
        if not isinstance(diag, str):
            continue
        try:
            parsed = json.loads(diag)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(parsed, dict):
            continue
        ms = parsed.get("_msBeforeNext")
        if isinstance(ms, (int, float)):
            return float(ms) / 1000.0
    return None


def _try_retry_after(response: httpx.Response) -> float | None:
    raw = response.headers.get("Retry-After")
    if not raw:
        return None
    stripped = raw.strip()
    try:
        return float(stripped)
    except ValueError:
        pass
    try:
        target = email.utils.parsedate_to_datetime(stripped)
    except (TypeError, ValueError):
        return None
    if target is None:
        return None
    delta = target.timestamp() - time.time()
    return delta if delta >= 0 else 0.0


def parse_retry_after_429(
    response: httpx.Response,
    *,
    max_delay_seconds: float = MAX_RETRY_DELAY_SECONDS,
) -> float:
    """Determine delay in seconds before retrying a 429 response.

    Consults, in order:
      1. FHIR OperationOutcome diagnostics `_msBeforeNext` (Medplum extension)
      2. `Retry-After` header (seconds or HTTP-date)
      3. Fallback: 1.0 second
    All returned values are capped at ``max_delay_seconds`` so a hostile or
    misbehaving server cannot pin a worker for an arbitrary duration. The
    cap is per-attempt; total time spent retrying scales with retry budget.
    Malformed responses never raise — they fall through to fallback.
    """
    ms = _try_ms_before_next(response)
    if ms is not None:
        capped = _cap(ms, max_delay_seconds)
        if capped < ms:
            logger.debug(
                "429: delay capped at %ss (server requested %ss)",
                max_delay_seconds,
                ms,
            )
        else:
            logger.debug("429: parsed _msBeforeNext -> %.2fs", capped)
        return capped
    ra = _try_retry_after(response)
    if ra is not None:
        capped = _cap(ra, max_delay_seconds)
        logger.debug("429: Retry-After -> %.2fs (capped)", capped)
        return capped
    logger.debug(
        "429: no delay hint in response, using fallback %.2fs",
        _FALLBACK_SECONDS,
    )
    return _FALLBACK_SECONDS
