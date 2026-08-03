"""Unit tests for FHIRBundle batch/transaction response inspection."""

from __future__ import annotations

from typing import Any

import pytest

from pymedplum import BundleEntryError, BundleEntryResult, FHIRBundle


def _response_bundle(entries: list[dict[str, Any]]) -> FHIRBundle:
    return FHIRBundle(
        {
            "resourceType": "Bundle",
            "type": "transaction-response",
            "entry": entries,
        }
    )


def test_entry_results_parses_status_location_and_outcome() -> None:
    bundle = _response_bundle(
        [
            {
                "response": {
                    "status": "201 Created",
                    "location": "Patient/p1/_history/1",
                }
            },
            {
                "resource": {"resourceType": "Patient", "id": "p2"},
                "response": {"status": "200 OK"},
            },
            {
                "response": {
                    "status": "400 Bad Request",
                    "outcome": {
                        "resourceType": "OperationOutcome",
                        "issue": [{"severity": "error", "code": "invalid"}],
                    },
                }
            },
        ]
    )

    results = bundle.entry_results()
    assert [r.index for r in results] == [0, 1, 2]
    assert [r.status_code for r in results] == [201, 200, 400]
    assert [r.ok for r in results] == [True, True, False]
    # location wins, /_history stripped; falls back to resource.id.
    assert results[0].resource_id == "p1"
    assert results[1].resource_id == "p2"
    assert results[0].resource is None
    assert results[1].resource == {"resourceType": "Patient", "id": "p2"}
    assert results[2].outcome is not None
    assert results[2].outcome["resourceType"] == "OperationOutcome"


def test_entry_results_absolute_location_and_bare_status() -> None:
    bundle = _response_bundle(
        [
            {
                "response": {
                    "status": "201",
                    "location": (
                        "https://api.medplum.com/fhir/R4/Observation/obs-1/_history/3"
                    ),
                }
            }
        ]
    )
    (result,) = bundle.entry_results()
    assert result.status_code == 201
    assert result.resource_id == "obs-1"


def test_entry_results_entry_without_response_reads_failed() -> None:
    """A search-shaped bundle inspected by mistake must not read as
    succeeded — entries with no response element are not ok."""
    bundle = _response_bundle([{"resource": {"resourceType": "Patient", "id": "p1"}}])
    (result,) = bundle.entry_results()
    assert result.ok is False
    assert result.status_code is None
    assert result.resource_id == "p1"


def test_entry_results_unparseable_status_is_failed() -> None:
    bundle = _response_bundle([{"response": {"status": "Created"}}])
    (result,) = bundle.entry_results()
    assert result.status_code is None
    assert result.ok is False


def test_failures_and_partition() -> None:
    bundle = _response_bundle(
        [
            {"response": {"status": "201 Created"}},
            {"response": {"status": "409 Conflict"}},
            {"response": {"status": "200 OK"}},
        ]
    )
    failures = bundle.failures()
    assert [f.index for f in failures] == [1]

    successes, failed = bundle.partition()
    assert [s.index for s in successes] == [0, 2]
    assert [f.index for f in failed] == [1]


def test_raise_for_entry_errors_raises_with_failed_entries() -> None:
    bundle = _response_bundle(
        [
            {"response": {"status": "201 Created"}},
            {
                "response": {
                    "status": "412 Precondition Failed",
                    "outcome": {
                        "resourceType": "OperationOutcome",
                        "issue": [
                            {
                                "severity": "error",
                                "code": "conflict",
                                "diagnostics": "patient jane@example.com",
                            }
                        ],
                    },
                }
            },
        ]
    )
    with pytest.raises(BundleEntryError) as exc_info:
        bundle.raise_for_entry_errors()

    exc = exc_info.value
    assert len(exc.entries) == 1
    assert isinstance(exc.entries[0], BundleEntryResult)
    assert exc.entries[0].index == 1
    assert exc.entries[0].status_code == 412
    # str(exc) carries only indices/statuses — never server outcome text.
    assert "entry 1" in str(exc)
    assert "412" in str(exc)
    assert "jane@example.com" not in str(exc)

    sanitized = exc.sanitize_for_logging()
    assert sanitized["failed_count"] == 1
    assert sanitized["entries"] == [{"index": 1, "status_code": 412}]


def test_raise_for_entry_errors_noop_when_all_ok() -> None:
    bundle = _response_bundle([{"response": {"status": "204 No Content"}}])
    bundle.raise_for_entry_errors()


def test_search_api_unchanged_skips_resourceless_entries() -> None:
    """The existing search-shaped API keeps skipping entries with no
    resource key — exactly what entry_results() exists to not do."""
    bundle = _response_bundle(
        [
            {"response": {"status": "201 Created"}},
            {"resource": {"resourceType": "Patient", "id": "p1"}},
        ]
    )
    assert bundle.get_resources() == [{"resourceType": "Patient", "id": "p1"}]
    assert len(bundle.entry_results()) == 2
