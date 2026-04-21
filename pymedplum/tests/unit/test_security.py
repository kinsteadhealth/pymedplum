import logging

import pytest

from pymedplum._security import (
    assert_same_origin,
    build_raw_request_url,
    sanitize_if_none_exist,
    validate_base_url,
)
from pymedplum.exceptions import InsecureTransportError, UnsafeRedirectError


def test_https_url_ok():
    assert validate_base_url("https://api.medplum.com/") == "https://api.medplum.com/"


def test_https_url_missing_trailing_slash_normalized():
    assert validate_base_url("https://api.medplum.com") == "https://api.medplum.com/"


def test_https_url_host_lowercased():
    assert validate_base_url("https://API.Medplum.com/") == "https://api.medplum.com/"


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost:8103/",
        "http://127.0.0.1:8103/",
        "http://[::1]:8103/",
    ],
)
def test_loopback_http_allowed_with_warning(url, caplog):
    with caplog.at_level(logging.WARNING, logger="pymedplum.security"):
        validate_base_url(url)
    assert any("loopback" in r.message.lower() for r in caplog.records)


def test_plain_http_rejected():
    with pytest.raises(InsecureTransportError):
        validate_base_url("http://api.medplum.com/")


def test_ipv4_mapped_ipv6_loopback_allowed_with_warning(caplog):
    """``[::ffff:127.0.0.1]`` is a loopback per ipaddress.is_loopback."""
    with caplog.at_level(logging.WARNING, logger="pymedplum.security"):
        validate_base_url("http://[::ffff:127.0.0.1]/")
    assert any("loopback" in r.message.lower() for r in caplog.records)


@pytest.mark.parametrize(
    "url",
    [
        # DNS-rebinding / hostname-spoofing attempts — not literal IPs.
        "http://127.0.0.1.nip.io/",
        "http://localhost.evil.com/",
        # ipaddress.ip_address() only accepts dotted-decimal / IPv6 literal
        # string forms. Decimal/hex/octal integer encodings fail closed here,
        # which is the desired behavior: we refuse to reason about hostnames
        # whose interpretation differs between our validator and libc/socket.
        "http://2130706433/",
        "http://0x7f000001/",
        "http://0177.0.0.1/",
    ],
)
def test_pseudo_loopback_forms_rejected(url):
    with pytest.raises(InsecureTransportError):
        validate_base_url(url)


def test_plain_http_allowed_with_opt_in_warning(caplog):
    with caplog.at_level(logging.WARNING, logger="pymedplum.security"):
        validate_base_url("http://api.medplum.com/", allow_insecure_http=True)
    assert any("allow_insecure_http" in r.message for r in caplog.records)


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://host/p",
        "ws://host/",
        "",
        "not-a-url",
    ],
)
def test_non_http_schemes_rejected(url):
    with pytest.raises((InsecureTransportError, ValueError)):
        validate_base_url(url)


def test_urlparse_ipv6_bracket_behavior():
    """Python stdlib invariant our loopback check depends on."""
    from urllib.parse import urlparse

    assert urlparse("http://[::1]/").hostname == "::1"


def test_same_origin_ok():
    assert_same_origin("https://api.medplum.com/", "https://api.medplum.com/x")


def test_different_host_raises():
    with pytest.raises(UnsafeRedirectError):
        assert_same_origin("https://api.medplum.com/", "https://evil.com/x")


def test_different_port_raises():
    with pytest.raises(UnsafeRedirectError):
        assert_same_origin("https://api.medplum.com/", "https://api.medplum.com:8443/x")


def test_different_scheme_raises():
    with pytest.raises(UnsafeRedirectError):
        assert_same_origin("https://api.medplum.com/", "http://api.medplum.com/x")


def test_case_insensitive_host():
    assert_same_origin("https://API.medplum.com/", "https://api.MEDPLUM.com/x")


def test_default_port_normalized():
    assert_same_origin("https://api.medplum.com/", "https://api.medplum.com:443/x")
    assert_same_origin("http://localhost/", "http://localhost:80/x")


def test_userinfo_rejected():
    with pytest.raises(UnsafeRedirectError):
        assert_same_origin(
            "https://api.medplum.com/",
            "https://user:pass@api.medplum.com/x",
        )


def test_malformed_candidate_raises():
    with pytest.raises(UnsafeRedirectError):
        assert_same_origin("https://api.medplum.com/", "not a url")


def test_raw_request_simple_path():
    assert build_raw_request_url("https://api.medplum.com/", "Patient").startswith(
        "https://api.medplum.com/"
    )
    assert build_raw_request_url("https://api.medplum.com/", "Patient").endswith(
        "/Patient"
    )


def test_raw_request_leading_slash_ok():
    assert build_raw_request_url("https://api.medplum.com/", "/Patient").endswith(
        "/Patient"
    )


def test_raw_request_nested_path_and_operation():
    got = build_raw_request_url("https://api.medplum.com/", "Patient/123/$everything")
    assert got == "https://api.medplum.com/Patient/123/$everything"


@pytest.mark.parametrize(
    "bad",
    [
        "https://evil.com/x",  # absolute URL → cross-origin
        "HTTPS://evil.com/x",  # case-insensitive scheme
        "//evil.com/x",  # protocol-relative → cross-origin after resolution
        "..\\evil.com",  # backslash smuggling
        "",
        "   ",
    ],
)
def test_raw_request_rejects_dangerous_paths(bad):
    """The security boundary is same-origin and absolute-URL rejection.

    Within-origin path navigation (including ``..`` and percent-encoded
    traversal) is no longer blocked — the operator has already enabled the
    raw_request escape hatch and can address any same-origin endpoint
    directly. Same-origin enforcement remains the actual defense against
    cross-origin token exfiltration.
    """
    with pytest.raises(UnsafeRedirectError):
        build_raw_request_url("https://api.medplum.com/", bad)


@pytest.mark.parametrize(
    "within_origin",
    [
        "..%2f..%2fetc%2fpasswd",  # URL-encoded traversal stays same-origin
        "....//Patient",  # double-dot navigation
        "..%20/Patient",  # escaped space + dots
        "../oauth2/token",  # traversal to a non-FHIR endpoint
    ],
)
def test_raw_request_passes_within_origin_traversal(within_origin):
    """Same-origin paths pass through regardless of traversal characters."""
    candidate = build_raw_request_url("https://api.medplum.com/", within_origin)
    assert candidate.startswith("https://api.medplum.com/")


def test_plain_query_string_unchanged():
    assert (
        sanitize_if_none_exist("identifier=mrn|123", "https://api.medplum.com/")
        == "identifier=mrn|123"
    )


def test_leading_question_mark_stripped():
    assert (
        sanitize_if_none_exist("?identifier=mrn|123", "https://api.medplum.com/")
        == "identifier=mrn|123"
    )


def test_whitespace_trimmed():
    assert (
        sanitize_if_none_exist("  ?identifier=mrn|123  ", "https://api.medplum.com/")
        == "identifier=mrn|123"
    )


def test_same_origin_absolute_url_warns_and_strips(caplog):
    with caplog.at_level(logging.WARNING, logger="pymedplum.security"):
        result = sanitize_if_none_exist(
            "https://api.medplum.com/fhir/R4/Patient?identifier=mrn|123",
            "https://api.medplum.com/",
        )
    assert result == "identifier=mrn|123"
    warnings_ = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert any("if_none_exist" in r.getMessage() for r in warnings_)
    joined = "\n".join(r.getMessage() for r in warnings_)
    # Query string is PHI-bearing (may carry MRN, identifier values); must
    # not leak into log output. Nor may the host/path.
    assert "mrn|123" not in joined
    assert "/fhir/R4/Patient" not in joined


def test_cross_origin_absolute_url_raises():
    with pytest.raises(UnsafeRedirectError):
        sanitize_if_none_exist(
            "https://evil.com?x=y",
            "https://api.medplum.com/",
        )


@pytest.mark.parametrize("empty", ["", "   ", "?", "   ?   "])
def test_empty_raises(empty):
    with pytest.raises(ValueError):
        sanitize_if_none_exist(empty, "https://api.medplum.com/")
