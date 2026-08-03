"""Unit + transport tests for Parameters reading and execute_operation as_fhir."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio
from respx import MockRouter

from pymedplum import (
    AsyncMedplumClient,
    MedplumClient,
    MedplumError,
    get_parameter,
    get_parameter_resource,
    parameters_to_dict,
)
from pymedplum.fhir import Bundle, Parameters

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

_BASE_URL = "https://api.medplum.com/"


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncMedplumClient]:
    client = AsyncMedplumClient(base_url=_BASE_URL, access_token="tkn")
    try:
        yield client
    finally:
        await client.aclose()


def _params() -> dict[str, Any]:
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "result", "valueBoolean": True},
            {"name": "display", "valueString": "Blood pressure"},
            {"name": "count", "valueInteger": 3},
            {
                "name": "resource",
                "resource": {"resourceType": "Patient", "id": "p1"},
            },
            {
                "name": "match",
                "part": [
                    {"name": "score", "valueDecimal": 0.9},
                    {"name": "grade", "valueCode": "certain"},
                ],
            },
        ],
    }


def test_parameters_to_dict_scalars_resources_and_parts() -> None:
    assert parameters_to_dict(_params()) == {
        "result": True,
        "display": "Blood pressure",
        "count": 3,
        "resource": {"resourceType": "Patient", "id": "p1"},
        "match": {"score": 0.9, "grade": "certain"},
    }


def test_parameters_to_dict_repeated_names_collect_into_list() -> None:
    params = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "property", "valueCode": "a"},
            {"name": "property", "valueCode": "b"},
        ],
    }
    assert parameters_to_dict(params) == {"property": ["a", "b"]}


def test_parameters_to_dict_roundtrips_dict_to_parameters() -> None:
    from pymedplum._fhir_ops import dict_to_parameters

    simple = {"code": "12345", "count": 2, "active": True}
    assert parameters_to_dict(dict_to_parameters(simple)) == simple


def test_parameters_to_dict_accepts_model_and_rejects_junk() -> None:
    model = Parameters(**_params())
    assert parameters_to_dict(model)["result"] is True

    with pytest.raises(TypeError, match="Parameters dict or model"):
        parameters_to_dict("not-parameters")

    assert parameters_to_dict({"resourceType": "Parameters"}) == {}


def test_readers_reject_non_parameters_resources() -> None:
    """A Patient/Bundle passed to the readers is an unexpected response
    shape — it must raise, not silently read as an empty result."""
    patient = {"resourceType": "Patient", "id": "p1"}

    with pytest.raises(ValueError, match="Expected a Parameters resource"):
        parameters_to_dict(patient)
    with pytest.raises(ValueError, match="Expected a Parameters resource"):
        get_parameter(patient, "name")
    with pytest.raises(ValueError, match="Expected a Parameters resource"):
        get_parameter_resource(patient, "name")
    with pytest.raises(ValueError, match="resourceType=None"):
        parameters_to_dict({})

    from pymedplum.fhir import Patient

    with pytest.raises(ValueError, match="Expected a Parameters resource"):
        parameters_to_dict(Patient(id="p1"))


def test_get_parameter_and_resource() -> None:
    params = _params()
    assert get_parameter(params, "display") == "Blood pressure"
    assert get_parameter(params, "match") == {"score": 0.9, "grade": "certain"}
    assert get_parameter(params, "missing") is None

    assert get_parameter_resource(params, "resource") == {
        "resourceType": "Patient",
        "id": "p1",
    }
    # Skips same-named entries without a resource.
    assert get_parameter_resource(params, "display") is None


def test_execute_operation_as_fhir_direct_response(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.post(f"{_BASE_URL}fhir/R4/Patient/p1/$everything").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    bundle = sync_client.execute_operation(
        "Patient", "everything", resource_id="p1", as_fhir=Bundle
    )
    assert isinstance(bundle, Bundle)
    assert bundle.type == "searchset"


def test_execute_operation_as_fhir_rejects_wrapped_response(
    sync_client: MedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.post(f"{_BASE_URL}fhir/R4/CodeSystem/$lookup").mock(
        return_value=httpx.Response(200, json=_params())
    )

    from pymedplum.fhir import Patient

    with pytest.raises(MedplumError, match="parameters_to_dict"):
        sync_client.execute_operation("CodeSystem", "lookup", as_fhir=Patient)


async def test_async_execute_operation_as_fhir(
    async_client: AsyncMedplumClient, respx_mock: MockRouter
) -> None:
    respx_mock.get(f"{_BASE_URL}fhir/R4/Patient/p1/$everything").mock(
        return_value=httpx.Response(
            200,
            json={"resourceType": "Bundle", "type": "searchset", "entry": []},
        )
    )

    bundle = await async_client.execute_operation(
        "Patient", "everything", resource_id="p1", method="GET", as_fhir=Bundle
    )
    assert isinstance(bundle, Bundle)

    from pymedplum.fhir import Patient

    respx_mock.get(f"{_BASE_URL}fhir/R4/Patient/p1/$everything").mock(
        return_value=httpx.Response(200, json=_params())
    )
    with pytest.raises(MedplumError, match="as_fhir handles direct"):
        await async_client.execute_operation(
            "Patient", "everything", resource_id="p1", method="GET", as_fhir=Patient
        )
