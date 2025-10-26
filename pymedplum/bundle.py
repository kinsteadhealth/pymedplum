"""FHIR Bundle wrapper with convenience methods.

Simplifies working with FHIR search results and batch operations.
"""

from collections.abc import Iterator
from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar("T")


class FHIRBundle:
    """Wrapper for FHIR Bundle resources with helper methods.

    Provides convenient access to Bundle entries and resources,
    eliminating boilerplate when working with search results.
    """

    def __init__(self, data: Dict[str, Any]):
        """Initialize from raw Bundle data.

        Args:
            data: Raw Bundle dict from API response

        Raises:
            ValueError: If data is not a valid Bundle
        """
        if not isinstance(data, dict):
            raise ValueError("Bundle data must be a dictionary")

        if data.get("resourceType") != "Bundle":
            raise ValueError(f"Expected Bundle, got {data.get('resourceType')}")

        self._data = data

    def get_resources(self) -> List[Dict[str, Any]]:
        """Extract all resources from Bundle entries.

        Returns:
            List of resource dicts

        Example:
            >>> bundle = FHIRBundle(api_response)
            >>> patients = bundle.get_resources()
            >>> for patient in patients:
            ...     print(patient['name'])
        """
        entries = self._data.get("entry", [])
        return [entry["resource"] for entry in entries if "resource" in entry]

    def get_resources_typed(self, resource_class: Type[T]) -> List[T]:
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
            return self._data["total"]
        return len(self.get_resources())

    def is_empty(self) -> bool:
        """Check if Bundle has no resources."""
        return len(self.get_resources()) == 0

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterate over resources directly."""
        return iter(self.get_resources())

    def __len__(self) -> int:
        """Get count of resources."""
        return len(self.get_resources())

    def __bool__(self) -> bool:
        """Bundle is truthy if it has resources."""
        return not self.is_empty()

    @property
    def raw(self) -> Dict[str, Any]:
        """Access underlying Bundle data."""
        return self._data

    @property
    def link(self) -> List[Dict[str, Any]]:
        """Get Bundle links for pagination."""
        return self._data.get("link", [])

    def get_next_link(self) -> Optional[str]:
        """Get next page URL for pagination.

        Returns:
            Next page URL or None if no next page
        """
        for link in self.link:
            if link.get("relation") == "next":
                return link.get("url")
        return None
