# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class ContactDetail(MedplumFHIRBase):
    """Specifies contact information for a person or organization."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    name: Optional[str] = Field(default=None, description="The name of an individual to contact.")
    telecom: Optional[List[ContactPoint]] = Field(default=None, description="The contact details for the individual (if a name was provided) or the organization.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ContactDetail", ContactDetail)
