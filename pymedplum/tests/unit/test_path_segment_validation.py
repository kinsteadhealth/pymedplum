"""Path segment validation tests.

Covers the validators in ``pymedplum._security`` and their integration into
both ``MedplumClient`` and ``AsyncMedplumClient``. The goal is to confirm
that untrusted caller-supplied identifiers can't be smuggled into URLs
via f-string interpolation — same-origin authenticated path traversal,
query-string injection, or CRLF smuggling must all raise before any
HTTP request is issued.
"""

from __future__ import annotations

import httpx
import pytest
from respx import MockRouter

import pymedplum.fhir  # noqa: F401  - trigger model rebuilding
from pymedplum import AsyncMedplumClient, MedplumClient
from pymedplum._security import (
    validate_as_fhir_class,
    validate_operation_name,
    validate_resource_id,
    validate_resource_type,
)

# ---------------------------------------------------------------------------
# validate_resource_type
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        "",
        " ",
        "a/b",
        "a\\b",
        "../../etc",
        "abc?x=1",
        "abc#frag",
        "abc def",
        "abc\x00",
        "abc%2Fdef",
        "abc\r\nX: y",
        "a" * 256,
        "1",
        "patient",  # must start uppercase
        "Patient!",
        "Patient-Extra",
    ],
)
def test_validate_resource_type_rejects_implausible(bad: str) -> None:
    """Hard-reject characters that can't appear in any FHIR type name."""
    with pytest.raises(ValueError):
        validate_resource_type(bad)


@pytest.mark.parametrize(
    "good",
    [
        "Patient",
        "Observation",
        "CodeSystem",
        "Bot",  # Medplum extension resource, emitted by codegen
        "Project",
    ],
)
def test_validate_resource_type_accepts_known(good: str) -> None:
    assert validate_resource_type(good) == good


@pytest.mark.parametrize(
    "plausible_but_unknown",
    [
        "Paitent",  # typo
        "EvilRoute",  # valid PascalCase but not a real type
        "FuturisticResource",  # plausibly a future Medplum addition
    ],
)
def test_validate_resource_type_warns_for_unknown(
    plausible_but_unknown: str, caplog: pytest.LogCaptureFixture
) -> None:
    """Plausible-looking but non-allowlisted types warn and pass through."""
    import logging

    with caplog.at_level(logging.WARNING, logger="pymedplum.security"):
        result = validate_resource_type(plausible_but_unknown)
    assert result == plausible_but_unknown
    assert any("not in the SDK's generated allowlist" in r.message for r in caplog.records)


def test_validate_resource_type_rejects_non_string() -> None:
    with pytest.raises(ValueError):
        validate_resource_type(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_resource_id
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        "",
        " ",
        "a/b",
        "a\\b",
        "../../etc",
        "abc?x=1",
        "abc#frag",
        "abc def",
        "abc\x00",
        "abc%2Fdef",
        "abc\r\nX: y",
        "a" * 65,
        "abc_def",  # underscore not allowed in FHIR id
    ],
)
def test_validate_resource_id_rejects(bad: str) -> None:
    with pytest.raises(ValueError):
        validate_resource_id(bad)


@pytest.mark.parametrize(
    "good",
    [
        "Patient",
        "123",
        "abc-def.ghi",
        "a" * 64,
        "A",
    ],
)
def test_validate_resource_id_accepts(good: str) -> None:
    assert validate_resource_id(good) == good


def test_validate_resource_id_rejects_non_string() -> None:
    with pytest.raises(ValueError):
        validate_resource_id(None)  # type: ignore[arg-type]


def test_validate_resource_id_uses_field_name_in_message() -> None:
    with pytest.raises(ValueError, match="version_id"):
        validate_resource_id("", field="version_id")


# ---------------------------------------------------------------------------
# validate_operation_name
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        "",
        " ",
        "$",
        "a/b",
        "a\\b",
        "../../etc",
        "op?x=1",
        "op#frag",
        "op def",
        "op\x00",
        "op\r\nX: y",
        "1match",  # must start with letter
        "a" * 66,
    ],
)
def test_validate_operation_name_rejects(bad: str) -> None:
    with pytest.raises(ValueError):
        validate_operation_name(bad)


def test_validate_operation_name_strips_dollar_prefix() -> None:
    assert validate_operation_name("$everything") == "everything"
    assert validate_operation_name("everything") == "everything"


@pytest.mark.parametrize(
    "good",
    [
        "everything",
        "$everything",
        "set-accounts",
        "$set-accounts",
        "ccda-export",
        "match",
    ],
)
def test_validate_operation_name_accepts(good: str) -> None:
    assert validate_operation_name(good) == good.lstrip("$")


# ---------------------------------------------------------------------------
# validate_as_fhir_class
# ---------------------------------------------------------------------------


def test_validate_as_fhir_class_accepts_resource() -> None:
    from pymedplum.fhir import Patient

    validate_as_fhir_class(Patient)
    validate_as_fhir_class(Patient, expected_resource_type="Patient")


def test_validate_as_fhir_class_rejects_datatype() -> None:
    from pymedplum.fhir import HumanName

    with pytest.raises(TypeError, match="not a top-level FHIR resource"):
        validate_as_fhir_class(HumanName)


def test_validate_as_fhir_class_rejects_non_class() -> None:
    with pytest.raises(TypeError):
        validate_as_fhir_class("Patient")  # type: ignore[arg-type]


def test_validate_as_fhir_class_rejects_non_fhir_class() -> None:
    class NotAFhir:
        pass

    with pytest.raises(TypeError, match="FHIR resource class"):
        validate_as_fhir_class(NotAFhir)


def test_validate_as_fhir_class_rejects_mismatched_resource_type() -> None:
    from pymedplum.fhir import Observation, Patient

    with pytest.raises(TypeError, match="does not match resource_type"):
        validate_as_fhir_class(Observation, expected_resource_type="Patient")
    # Sanity: matching resource type is accepted
    validate_as_fhir_class(Patient, expected_resource_type="Patient")


def test_sync_read_resource_rejects_datatype_as_fhir(respx_mock: MockRouter) -> None:
    from pymedplum.fhir import HumanName

    respx_mock.get("https://api.medplum.com/fhir/R4/Patient/abc").mock(
        return_value=httpx.Response(200, json={"resourceType": "Patient", "id": "abc"})
    )
    client = _sync_client()
    try:
        with pytest.raises(TypeError, match="not a top-level FHIR resource"):
            client.read_resource("Patient", "abc", as_fhir=HumanName)  # type: ignore[type-var]
    finally:
        client.close()


def test_sync_read_resource_rejects_mismatched_as_fhir(respx_mock: MockRouter) -> None:
    from pymedplum.fhir import Observation

    respx_mock.get("https://api.medplum.com/fhir/R4/Patient/abc").mock(
        return_value=httpx.Response(200, json={"resourceType": "Patient", "id": "abc"})
    )
    client = _sync_client()
    try:
        with pytest.raises(TypeError, match="does not match resource_type"):
            client.read_resource("Patient", "abc", as_fhir=Observation)
    finally:
        client.close()


# ---------------------------------------------------------------------------
# Integration: sync client raises BEFORE hitting the wire
# ---------------------------------------------------------------------------


def _sync_client() -> MedplumClient:
    return MedplumClient(access_token="test-token")


def _async_client() -> AsyncMedplumClient:
    return AsyncMedplumClient(access_token="test-token")


def test_sync_read_resource_blocks_traversal(respx_mock: MockRouter) -> None:
    """The documented exploit must ValueError before any HTTP call is made."""
    client = _sync_client()
    with pytest.raises(ValueError):
        client.read_resource("Patient", "../../../oauth2/token")
    assert not respx_mock.calls, "No HTTP request should be issued"


def test_sync_read_resource_blocks_query_injection(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.read_resource("Patient", "abc?foo=bar")
    assert not respx_mock.calls


def test_sync_read_resource_blocks_slashed_id(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.read_resource("Patient", "123/Account/abc")
    assert not respx_mock.calls


def test_sync_update_resource_blocks_slashed_id(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.update_resource(
            {"resourceType": "Patient", "id": "123/Account/abc"}
        )
    assert not respx_mock.calls


def test_sync_patch_resource_blocks_traversal(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.patch_resource(
            "Patient",
            "../etc",
            [{"op": "replace", "path": "/active", "value": True}],
        )
    assert not respx_mock.calls


def test_sync_delete_resource_blocks_slashed_id(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.delete_resource("Patient", "abc?x=1")
    assert not respx_mock.calls


def test_sync_vread_resource_blocks_bad_version(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError, match="version_id"):
        client.vread_resource("Patient", "123", "../../oauth2")
    assert not respx_mock.calls


def test_sync_execute_operation_blocks_bad_operation(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.execute_operation("Patient", "../../../something", resource_id="123")
    assert not respx_mock.calls


def test_sync_execute_operation_blocks_bad_resource_type(
    respx_mock: MockRouter,
) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.execute_operation("../oauth2", "everything")
    assert not respx_mock.calls


def test_sync_expunge_resource_blocks_bad_id(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.expunge_resource("Patient", "../admin")
    assert not respx_mock.calls


def test_sync_export_ccda_blocks_bad_id(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.export_ccda("../../../oauth2/token")
    assert not respx_mock.calls


def test_sync_download_binary_blocks_bad_id(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.download_binary("../../../oauth2/token")
    assert not respx_mock.calls


def test_sync_search_resources_blocks_bad_type(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(ValueError):
        client.search_resources("../oauth2")
    assert not respx_mock.calls


def test_sync_get_blocks_traversal(respx_mock: MockRouter) -> None:
    client = _sync_client()
    with pytest.raises(Exception):  # UnsafeRedirectError from build_raw_request_url
        client.get("../oauth2/token")
    assert not respx_mock.calls


# ---------------------------------------------------------------------------
# Integration: async client raises BEFORE hitting the wire
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_read_resource_blocks_traversal(respx_mock: MockRouter) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError):
            await client.read_resource("Patient", "../../../oauth2/token")
        assert not respx_mock.calls
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_async_read_resource_blocks_query_injection(
    respx_mock: MockRouter,
) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError):
            await client.read_resource("Patient", "abc?foo=bar")
        assert not respx_mock.calls
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_async_update_resource_blocks_slashed_id(
    respx_mock: MockRouter,
) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError):
            await client.update_resource(
                {"resourceType": "Patient", "id": "123/Account/abc"}
            )
        assert not respx_mock.calls
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_async_execute_operation_blocks_bad_operation(
    respx_mock: MockRouter,
) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError):
            await client.execute_operation(
                "Patient", "../../../something", resource_id="123"
            )
        assert not respx_mock.calls
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_async_vread_resource_blocks_bad_version(
    respx_mock: MockRouter,
) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError, match="version_id"):
            await client.vread_resource("Patient", "123", "../../oauth2")
        assert not respx_mock.calls
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_async_expunge_resource_blocks_bad_id(
    respx_mock: MockRouter,
) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError):
            await client.expunge_resource("Patient", "../admin")
        assert not respx_mock.calls
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_async_download_binary_blocks_bad_id(
    respx_mock: MockRouter,
) -> None:
    client = _async_client()
    try:
        with pytest.raises(ValueError):
            await client.download_binary("../../../oauth2/token")
        assert not respx_mock.calls
    finally:
        await client.aclose()


# ---------------------------------------------------------------------------
# Sanity check: valid inputs still reach the wire
# ---------------------------------------------------------------------------


def test_sync_read_resource_accepts_valid_id(respx_mock: MockRouter) -> None:
    """Smoke test so we know the integration path is wired, not always raising."""
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient/abc-def.123").mock(
        return_value=httpx.Response(
            200, json={"resourceType": "Patient", "id": "abc-def.123"}
        )
    )
    client = _sync_client()
    try:
        result = client.read_resource("Patient", "abc-def.123")
        assert result["id"] == "abc-def.123"
    finally:
        client.close()


@pytest.mark.asyncio
async def test_async_read_resource_accepts_valid_id(
    respx_mock: MockRouter,
) -> None:
    respx_mock.get("https://api.medplum.com/fhir/R4/Patient/abc-def.123").mock(
        return_value=httpx.Response(
            200, json={"resourceType": "Patient", "id": "abc-def.123"}
        )
    )
    client = _async_client()
    try:
        result = await client.read_resource("Patient", "abc-def.123")
        assert result["id"] == "abc-def.123"
    finally:
        await client.aclose()
