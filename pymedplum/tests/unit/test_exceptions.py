import pytest

from pymedplum.exceptions import (
    InsecureTransportError,
    MedplumError,
    UnsafeRedirectError,
)


def test_insecure_transport_error_is_medplum_error():
    with pytest.raises(MedplumError):
        raise InsecureTransportError("http://foo")


def test_unsafe_redirect_error_is_medplum_error():
    with pytest.raises(MedplumError):
        raise UnsafeRedirectError("https://evil.com")


def test_insecure_transport_error_message_preserved():
    with pytest.raises(InsecureTransportError) as exc_info:
        raise InsecureTransportError("got http://foo")
    assert "http://foo" in str(exc_info.value)


def test_all_hardening_exceptions_exported_from_top_level():
    import pymedplum

    for name in (
        "MedplumError",
        "AuthorizationError",
        "NotFoundError",
        "BadRequestError",
        "PreconditionFailedError",
        "InsecureTransportError",
        "UnsafeRedirectError",
        "TokenRefreshCooldownError",
        "OperationOutcomeError",
        "ServerError",
    ):
        assert hasattr(pymedplum, name), f"pymedplum.{name} not exported"


def test_resource_not_found_error_removed():
    import pymedplum

    assert not hasattr(pymedplum, "ResourceNotFoundError")
