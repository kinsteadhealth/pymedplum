"""FHIR Bundle wrapper with convenience methods.

Simplifies working with FHIR search results and batch operations.
"""

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .exceptions import BundleEntryError

T = TypeVar("T")


def _parse_entry_status(status: Any) -> int | None:
    """Parse ``entry.response.status`` ("201 Created", "404") to an int."""
    if isinstance(status, int):
        return status
    if isinstance(status, str):
        head = status.strip().split(" ", 1)[0]
        try:
            return int(head)
        except ValueError:
            return None
    return None


def _resource_id_from_location(location: Any) -> str | None:
    """Extract the resource ID from ``entry.response.location``.

    Handles relative and absolute forms, with or without a
    ``/_history/<version>`` suffix (e.g.
    ``Patient/123/_history/1`` -> ``"123"``).
    """
    if not isinstance(location, str) or not location:
        return None
    path = location.split("?", 1)[0]
    if "/_history/" in path:
        path = path.split("/_history/", 1)[0]
    segment = path.rstrip("/").rsplit("/", 1)[-1]
    return segment or None


@dataclass(frozen=True)
class BundleEntryResult:
    """Per-entry outcome of a batch/transaction response bundle.

    Attributes:
        index: Position of the entry in ``Bundle.entry``.
        status_code: HTTP status parsed from ``entry.response.status``
            (``None`` when the entry has no parseable response status).
        ok: ``True`` for a 2xx status. ``False`` otherwise — including
            entries with no ``response`` element at all, so a
            search-shaped bundle inspected by mistake reads as failed
            rather than silently succeeded.
        resource_id: Resource ID parsed from ``entry.response.location``
            (``/_history/<version>`` suffix stripped), falling back to
            ``entry.resource.id``. ``None`` when neither is present —
            typical for a bare ``201 Created`` entry from a server not
            echoing bodies.
        resource: ``entry.resource`` when the server returned one
            (GET/read entries, and writes under
            ``Prefer: return=representation``).
        outcome: ``entry.response.outcome`` (an OperationOutcome),
            usually present on failures.
    """

    index: int
    status_code: int | None
    ok: bool
    resource_id: str | None
    resource: dict[str, Any] | None
    outcome: dict[str, Any] | None


@dataclass(frozen=True)
class BatchCreateResult:
    """Classified outcome of a ``conditional_create_batch`` call.

    Entry ``index`` values refer to positions in the caller's original
    ``entries`` sequence, across all chunks.

    Attributes:
        created: Entries the server created (``201 Created``).
        existed: Entries that matched an existing resource
            (``200 OK`` — the conditional create was a no-op).
        failed: Everything else. Collected, never raised — the caller
            decides how to compensate.
    """

    created: list[BundleEntryResult]
    existed: list[BundleEntryResult]
    failed: list[BundleEntryResult]

    @property
    def ok(self) -> bool:
        """True when no entry failed."""
        return not self.failed


class FHIRBundle(Generic[T]):
    """Wrapper for FHIR Bundle resources with helper methods.

    Provides convenient access to Bundle entries and resources,
    eliminating boilerplate when working with search results.
    """

    def __init__(self, data: dict[str, Any]):
        """Initialize from raw Bundle data.

        Args:
            data: Raw Bundle dict from API response

        Raises:
            ValueError: If data is not a valid Bundle
        """
        if not isinstance(data, dict):
            raise TypeError("Bundle data must be a dictionary")

        if data.get("resourceType") != "Bundle":
            raise ValueError(f"Expected Bundle, got {data.get('resourceType')}")

        self._data = data
        self._resource_class: type[T] | None = None

    def get_resources(
        self, *, max_resources: int | None = None
    ) -> list[dict[str, Any]]:
        """Extract all resources from Bundle entries.

        Args:
            max_resources: Optional cap on the number of resources returned.
                When supplied and the bundle contains more entries, raises
                ``ValueError`` instead of materializing the full list. Use
                this defensively against pages of unexpected size; leave
                unset for legitimate bulk-data flows.

        Returns:
            List of resource dicts

        Raises:
            ValueError: If ``max_resources`` is set and the bundle exceeds it.

        Example:
            >>> bundle = FHIRBundle(api_response)
            >>> patients = bundle.get_resources()
            >>> for patient in patients:
            ...     print(patient['name'])
        """
        entries = self._data.get("entry", [])
        resources: list[dict[str, Any]] = []
        for entry in entries:
            if "resource" not in entry:
                continue
            if max_resources is not None and len(resources) >= max_resources:
                raise ValueError(
                    f"Bundle contains more than {max_resources} resources, "
                    f"exceeding max_resources={max_resources}"
                )
            resources.append(entry["resource"])
        return resources

    def get_resources_typed(self, resource_class: type[T]) -> list[T]:
        """Extract and parse resources to typed Pydantic models.

        Args:
            resource_class: Pydantic model class to parse into

        Returns:
            List of typed resources

        Example:
            >>> from pymedplum.fhir import Patient
            >>> patients = bundle.get_resources_typed(Patient)
            >>> for patient in patients:
            ...     print(patient.name[0].given)  # Type-safe!
        """
        self._resource_class = resource_class
        return [
            resource_class(**resource_dict) for resource_dict in self.get_resources()
        ]

    def get_total(self) -> int | None:
        """Get the total number of matches for the search, if knowable.

        Uses ``Bundle.total`` when present. Medplum only populates it
        when the search requested ``_total=accurate`` or
        ``_total=estimate`` (e.g. ``search_with_options(total="accurate")``).
        Without it, this falls back to counting match entries — but only
        when the bundle has no ``next`` link, i.e. this single page *is*
        the complete result set. When more pages exist, returns ``None``
        rather than passing off the page size as a total.

        Returns:
            Total match count, or ``None`` when the server omitted
            ``Bundle.total`` and the results are paginated.
        """
        if "total" in self._data:
            total = self._data["total"]
            if isinstance(total, int):
                return total
        if self.get_next_link() is not None:
            return None
        entries = self._data.get("entry", [])
        count = 0
        for entry in entries:
            if "resource" not in entry:
                continue
            search_info = entry.get("search")
            mode = search_info.get("mode") if isinstance(search_info, dict) else None
            if mode is None or mode == "match":
                count += 1
        return count

    def is_empty(self) -> bool:
        """Check if Bundle has no resources."""
        return len(self.get_resources()) == 0

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Iterate over resources directly."""
        return iter(self.get_resources())

    def __len__(self) -> int:
        """Get count of resources."""
        return len(self.get_resources())

    def __bool__(self) -> bool:
        """Bundle is truthy if it has resources."""
        return not self.is_empty()

    @property
    def raw(self) -> dict[str, Any]:
        """Access underlying Bundle data."""
        return self._data

    @property
    def link(self) -> list[dict[str, Any]]:
        """Get Bundle links for pagination."""
        links = self._data.get("link", [])
        return links if isinstance(links, list) else []

    def get_next_link(self) -> str | None:
        """Get next page URL for pagination.

        Returns:
            Next page URL or None if no next page
        """
        for link in self.link:
            if link.get("relation") == "next":
                url = link.get("url")
                return url if isinstance(url, str) else None
        return None

    def entry_results(self) -> list[BundleEntryResult]:
        """Per-entry outcomes of a batch/transaction *response* bundle.

        Unlike :meth:`get_resources` — which skips entries with no
        ``resource`` key, exactly what a bare ``201 Created`` write
        entry looks like — this inspects every entry's ``response``
        element and returns one :class:`BundleEntryResult` per entry.

        Medplum ``type: transaction`` bundles are **not atomic on
        failure**: some entries may have committed while others failed.
        Always inspect per-entry results (or call
        :meth:`raise_for_entry_errors`) after executing a batch or
        transaction — a 200 on the outer request proves nothing about
        the entries.

        Example:
            >>> response = client.execute_batch(bundle)
            >>> for result in FHIRBundle(response).entry_results():
            ...     print(result.index, result.status_code, result.ok)
        """
        results: list[BundleEntryResult] = []
        for index, entry in enumerate(self._data.get("entry", [])):
            if not isinstance(entry, dict):
                results.append(
                    BundleEntryResult(
                        index=index,
                        status_code=None,
                        ok=False,
                        resource_id=None,
                        resource=None,
                        outcome=None,
                    )
                )
                continue
            response = entry.get("response")
            response = response if isinstance(response, dict) else {}
            status_code = _parse_entry_status(response.get("status"))
            resource = entry.get("resource")
            resource = resource if isinstance(resource, dict) else None
            resource_id = _resource_id_from_location(response.get("location"))
            if resource_id is None and resource is not None:
                raw_id = resource.get("id")
                resource_id = raw_id if isinstance(raw_id, str) else None
            outcome = response.get("outcome")
            results.append(
                BundleEntryResult(
                    index=index,
                    status_code=status_code,
                    ok=status_code is not None and 200 <= status_code < 300,
                    resource_id=resource_id,
                    resource=resource,
                    outcome=outcome if isinstance(outcome, dict) else None,
                )
            )
        return results

    def failures(self) -> list[BundleEntryResult]:
        """Entries of a batch/transaction response that did not succeed.

        See :meth:`entry_results` for why per-entry inspection is
        mandatory (transactions are not atomic on failure).
        """
        return [result for result in self.entry_results() if not result.ok]

    def partition(
        self,
    ) -> tuple[list[BundleEntryResult], list[BundleEntryResult]]:
        """Split entry results into ``(successes, failures)``."""
        successes: list[BundleEntryResult] = []
        failures: list[BundleEntryResult] = []
        for result in self.entry_results():
            (successes if result.ok else failures).append(result)
        return successes, failures

    def raise_for_entry_errors(self) -> None:
        """Raise :class:`~pymedplum.exceptions.BundleEntryError` if any entry failed.

        Medplum ``type: transaction`` bundles are **not atomic on
        failure** — the successful entries have already committed, so
        catching this exception is a compensation point, not proof of a
        clean rollback.
        """
        failed = self.failures()
        if failed:
            raise BundleEntryError(failed)
