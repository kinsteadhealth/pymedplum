# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Range(MedplumFHIRBase):
    """A set of ordered Quantities defined by a low and high limit."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    low: Optional[Quantity] = Field(default=None, description="The low limit. The boundary is inclusive.")
    high: Optional[Quantity] = Field(default=None, description="The high limit. The boundary is inclusive.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Range", Range)
