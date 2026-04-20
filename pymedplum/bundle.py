"""FHIR Bundle wrapper with convenience methods.

Simplifies working with FHIR search results and batch operations.
"""

from collections.abc import Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


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
        resources = [entry["resource"] for entry in entries if "resource" in entry]
        if max_resources is not None and len(resources) > max_resources:
            raise ValueError(
                f"Bundle contains {len(resources)} resources, exceeding "
                f"max_resources={max_resources}"
            )
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

    def get_total(self) -> int:
        """Get total count of resources.

        Uses Bundle.total if available, otherwise counts entries.

        Returns:
            Total count of resources
        """
        if "total" in self._data:
            total = self._data["total"]
            if isinstance(total, int):
                return total
        return len(self.get_resources())

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
