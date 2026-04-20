"""URL and transport validators for the client.

Stateless. Pure functions. No side effects beyond raising and logging warnings.
"""

from __future__ import annotations

import ipaddress
import logging
import re
from urllib.parse import quote, urljoin, urlparse, urlunparse

from pymedplum.exceptions import InsecureTransportError, UnsafeRedirectError
from pymedplum.fhir._resource_types import RESOURCE_TYPES

logger = logging.getLogger("pymedplum.security")

_DEFAULT_PORTS: dict[str, int] = {"http": 80, "https": 443}


def _is_loopback_host(host_lower: str) -> bool:
    """Return True for literal loopback addresses and the ``localhost`` alias.

    ``ipaddress`` canonicalizes decimal / octal / hex / IPv4-mapped IPv6
    spellings so attempts like ``2130706433``, ``0x7f000001``, ``0177.0.0.1``,
    or ``::ffff:127.0.0.1`` no longer need special handling. Hostnames other
    than ``localhost`` fall through to DNS resolution at connect time, which
    the SDK cannot trust, so we deliberately do NOT resolve hostnames here.
    Callers relying on the loopback exemption must use a literal IP or
    ``localhost``; everything else must pass through ``allow_insecure_http``.
    """
    if host_lower == "localhost":
        return True
    stripped = host_lower.strip("[]").split("%", 1)[0]
    try:
        return ipaddress.ip_address(stripped).is_loopback
    except ValueError:
        return False

_DANGEROUS_PATH_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)^\s*https?:"),
    re.compile(r"^\s*//"),
    re.compile(r"\\"),
)


def _check_http_allowed(host_lower: str, *, allow_insecure_http: bool) -> None:
    """Raise or warn when a base URL uses plain http://.

    Loopback hosts are always allowed (with a warning). Non-loopback hosts
    require an explicit ``allow_insecure_http=True`` opt-in or raise.
    """
    if _is_loopback_host(host_lower):
        logger.warning(
            "pymedplum.security: plain HTTP allowed for loopback "
            "host %r. Do not use http:// for non-loopback hosts.",
            host_lower,
        )
        return
    if allow_insecure_http:
        logger.warning(
            "pymedplum.security: plain HTTP allowed via "
            "allow_insecure_http=True for host %r. This is unsafe "
            "for PHI; use HTTPS in production.",
            host_lower,
        )
        return
    raise InsecureTransportError(
        f"Plain http:// is not allowed for {host_lower!r}. "
        f"Use https://, a loopback host, or "
        f"allow_insecure_http=True (not recommended)."
    )


def _normalize_base_netloc_and_path(
    host_lower: str, port: int | None, path: str
) -> tuple[str, str]:
    """Return ``(netloc, path)`` for a validated base URL.

    IPv6 hostnames get bracketed; the path is forced to a single trailing slash.
    """
    port_segment = f":{port}" if port is not None else ""
    host_segment = f"[{host_lower}]" if ":" in host_lower else host_lower
    netloc = f"{host_segment}{port_segment}"
    normalized_path = path or "/"
    if not normalized_path.endswith("/"):
        normalized_path = normalized_path + "/"
    return netloc, normalized_path


def validate_base_url(url: str, *, allow_insecure_http: bool = False) -> str:
    """Normalize and validate a base URL at client construction time.

    Returns the normalized URL (hostname lowercased, single trailing slash).

    - https:// : always allowed
    - http://localhost | 127.0.0.1 | [::1] (+ port) : allowed, warning logged
    - any other http:// : raises InsecureTransportError unless
      allow_insecure_http=True (also warning-logged)
    - non-http(s) schemes / malformed : raises
    """
    if not url or not isinstance(url, str):
        raise ValueError(f"Invalid base_url: {url!r}")

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise InsecureTransportError(
            f"Unsupported URL scheme: {parsed.scheme!r}. Expected http or https."
        )
    if not parsed.hostname:
        raise ValueError(f"Invalid base_url (no host): {url!r}")

    host_lower = parsed.hostname.lower()
    if parsed.scheme == "http":
        _check_http_allowed(host_lower, allow_insecure_http=allow_insecure_http)

    netloc, path = _normalize_base_netloc_and_path(host_lower, parsed.port, parsed.path)
    normalized = urlunparse((parsed.scheme, netloc, path, "", "", ""))
    logger.debug(
        "pymedplum.security: base_url normalized %r -> %r",
        url,
        normalized,
    )
    return normalized


def _origin_tuple(url: str) -> tuple[str, str, int]:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise UnsafeRedirectError(f"Unsupported scheme in {url!r}")
    if parsed.username is not None or parsed.password is not None:
        raise UnsafeRedirectError(f"URL with userinfo is not allowed: {url!r}")
    if not parsed.hostname:
        raise UnsafeRedirectError(f"URL has no host: {url!r}")
    port = parsed.port if parsed.port is not None else _DEFAULT_PORTS[parsed.scheme]
    return (parsed.scheme.lower(), parsed.hostname.lower(), port)


def assert_same_origin(base_url: str, candidate_url: str) -> None:
    """Raise UnsafeRedirectError if candidate's origin does not match base's."""
    try:
        base = _origin_tuple(base_url)
        cand = _origin_tuple(candidate_url)
    except UnsafeRedirectError:
        raise
    except Exception as exc:
        raise UnsafeRedirectError(
            f"Could not parse candidate URL {candidate_url!r}: {exc}"
        ) from exc
    if base != cand:
        raise UnsafeRedirectError(
            f"Cross-origin URL rejected. Expected origin "
            f"{base[0]}://{base[1]}:{base[2]}, got "
            f"{cand[0]}://{cand[1]}:{cand[2]}."
        )


def _reject_if_dangerous(path: str, raw: str, *, stage: str) -> None:
    """Raise ``UnsafeRedirectError`` if ``raw`` matches any dangerous pattern.

    ``path`` is the caller's original input (used for error messages);
    ``raw`` is the value actually scanned (original or decoded).
    """
    for pat in _DANGEROUS_PATH_PATTERNS:
        if pat.search(raw):
            raise UnsafeRedirectError(f"Unsafe raw_request path{stage}: {path!r}")


def build_raw_request_url(base_url: str, path: str) -> str:
    """Safely join base_url + caller-supplied path for the raw_request escape hatch.

    The security boundary here is **same-origin**: regardless of any path
    traversal the caller writes, the resulting URL must address the same
    server we're already authenticated against. Within-origin endpoint
    selection is the caller's call — they have the same credentials no
    matter which path they use.

    Rejects:
    - absolute URLs (``https://...``)
    - protocol-relative forms (``//host/path``)
    - backslash smuggling
    - cross-origin destinations after URL resolution
    """
    if not isinstance(path, str) or not path.strip():
        raise UnsafeRedirectError(
            f"raw_request path must be a non-empty string: {path!r}"
        )

    _reject_if_dangerous(path, path, stage="")

    candidate = urljoin(base_url, quote(path.lstrip("/"), safe="/$?&=#"))
    assert_same_origin(base_url, candidate)
    return candidate


def sanitize_if_none_exist(value: str, base_url: str) -> str:
    """Normalize a caller-supplied if_none_exist query string."""
    if not isinstance(value, str):
        raise ValueError(  # noqa: TRY004 — public API contract
            f"if_none_exist must be str: {type(value).__name__}"
        )

    stripped = value.strip()
    if not stripped or stripped == "?":
        raise ValueError("if_none_exist must be a non-empty query string")

    if stripped.lower().startswith(("http://", "https://")):
        assert_same_origin(base_url, stripped)
        parsed = urlparse(stripped)
        query = parsed.query
        if not query:
            raise ValueError("if_none_exist absolute URL had no query string")
        logger.warning(
            "pymedplum.security: if_none_exist was passed as a full URL. "
            "Stripping to query string only. "
            "Pass just the query string to silence this warning."
        )
        return query

    if stripped.startswith("?"):
        stripped = stripped[1:].strip()
        if not stripped:
            raise ValueError("if_none_exist must contain a query")
    return stripped


# FHIR R4 §id type rule: https://www.hl7.org/fhir/R4/datatypes.html#id
_VALID_FHIR_ID = re.compile(r"^[A-Za-z0-9\-\.]{1,64}$")
# Operation names; leading $ is optional because callers pass both forms
_VALID_OPERATION_NAME = re.compile(r"^\$?[a-zA-Z][a-zA-Z0-9\-]{0,63}$")
# Plausibility check for resource type names. Stricter than "any string", to
# block path-traversal characters being smuggled in via the type segment
# (e.g. ``read_resource("../oauth2", "abc")``); looser than the codegen
# allowlist, which would otherwise reject any new server-side type the SDK
# hasn't been regenerated against.
_PLAUSIBLE_RESOURCE_TYPE = re.compile(r"^[A-Z][A-Za-z0-9]{0,254}$")


def validate_resource_type(resource_type: str) -> str:
    """Validate a FHIR resource type name.

    Two-tier check:

    1. **Hard reject** anything that doesn't look like a FHIR type name —
       slashes, dots, query/fragment characters, control chars, etc. This
       blocks path-traversal attacks via the type segment.
    2. **Warn** when the type passes plausibility but isn't in the codegen-
       emitted ``RESOURCE_TYPES`` allowlist. The request still goes through;
       Medplum will return a clean 404 if the type is genuinely unknown,
       and the warning surfaces typos (``"Paitent"``) plus genuine new
       upstream types the SDK hasn't been regenerated for yet.
    """
    if not isinstance(resource_type, str) or not _PLAUSIBLE_RESOURCE_TYPE.match(
        resource_type
    ):
        raise ValueError(f"Invalid FHIR resource_type: {resource_type!r}")
    if resource_type not in RESOURCE_TYPES:
        logger.warning(
            "pymedplum.security: resource_type %r is not in the SDK's "
            "generated allowlist. The request will proceed; the server "
            "will reject with 404 if the type is genuinely unknown. "
            "If this is a new Medplum type, regenerate the FHIR module.",
            resource_type,
        )
    return resource_type


def validate_resource_id(resource_id: str, *, field: str = "resource_id") -> str:
    if not isinstance(resource_id, str) or not _VALID_FHIR_ID.match(resource_id):
        raise ValueError(f"Invalid FHIR {field}: {resource_id!r}")
    return resource_id


def validate_operation_name(operation: str) -> str:
    if not isinstance(operation, str) or not _VALID_OPERATION_NAME.match(operation):
        raise ValueError(f"Invalid FHIR operation name: {operation!r}")
    # Return without leading '$' so callers can re-prefix consistently
    return operation.lstrip("$")


def validate_as_fhir_class(
    cls: type, *, expected_resource_type: str | None = None
) -> None:
    """Validate an ``as_fhir=`` argument names a real FHIR resource class.

    The ``ResourceT`` TypeVar on client methods is bound to ``MedplumFHIRBase``,
    which accepts every generated class — including datatypes like ``HumanName``
    and backbone elements. Passing one of those to ``as_fhir`` would yield a
    cryptic Pydantic error far from the call site. This check rejects them
    eagerly and, when we know the expected route resource type, also verifies
    the class matches so ``read_resource("Patient", id, as_fhir=Observation)``
    fails fast.
    """
    from pymedplum.fhir.base import MedplumFHIRBase

    if not isinstance(cls, type) or not issubclass(cls, MedplumFHIRBase):
        raise TypeError(
            f"as_fhir must be a FHIR resource class, got {cls!r}"
        )
    if cls.__name__ not in RESOURCE_TYPES:
        raise TypeError(
            f"as_fhir={cls.__name__!r} is not a top-level FHIR resource type "
            f"(datatypes and backbone elements are not valid here)"
        )
    if expected_resource_type and cls.__name__ != expected_resource_type:
        raise TypeError(
            f"as_fhir={cls.__name__!r} does not match resource_type="
            f"{expected_resource_type!r}"
        )


