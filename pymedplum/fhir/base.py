"""Base classes for Medplum FHIR resources.

This module provides the foundation for all generated FHIR resources,
configured to handle Medplum's server-specific metadata extensions.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MedplumFHIRBase(BaseModel):
    """Base class for all Medplum FHIR resources.

    Configured with:
    - extra='allow': Permits Medplum's metadata extensions (author, project, compartment)
    - populate_by_name=True: Accepts both camelCase (FHIR) and snake_case (Python)
    - validate_assignment=True: Validates when modifying fields after creation

    All generated FHIR resources inherit from this class, ensuring
    consistent behavior for Medplum metadata at all nesting levels.
    """

    model_config = ConfigDict(
        extra="allow",  # KEY: All child classes inherit this
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @property
    def medplum_author(self) -> str | None:
        """Access Medplum's author metadata field.

        The author field identifies who/what created or modified this resource.

        Returns:
            Author reference (e.g., "Practitioner/abc") or None

        Example:
            >>> patient.medplum_author
            'Practitioner/doc-123'
        """
        if not hasattr(self, "meta") or not self.meta:
            return None

        # Handle both dict and object
        meta_data = self.meta if isinstance(self.meta, dict) else self.meta.model_dump()
        author = meta_data.get("author")

        if not author:
            return None

        # Extract reference string
        if isinstance(author, dict):
            return author.get("reference")
        elif hasattr(author, "reference"):
            return author.reference

        return None

    @property
    def medplum_project(self) -> str | None:
        """Access Medplum's project metadata field.

        The project field identifies which Medplum project this resource belongs to.

        Returns:
            Project ID or None

        Example:
            >>> patient.medplum_project
            '7bb0016b-9155-4ce7-8cba-dc6800e74a4b'
        """
        if not hasattr(self, "meta") or not self.meta:
            return None

        meta_data = self.meta if isinstance(self.meta, dict) else self.meta.model_dump()
        return meta_data.get("project")

    @property
    def medplum_compartment(self) -> list | None:
        """Access Medplum's compartment metadata field.

        Compartments define access control boundaries for this resource.

        Returns:
            List of compartment references or None

        Example:
            >>> patient.medplum_compartment
            [{'reference': 'Project/proj-123'}]
        """
        if not hasattr(self, "meta") or not self.meta:
            return None

        meta_data = self.meta if isinstance(self.meta, dict) else self.meta.model_dump()
        return meta_data.get("compartment")
