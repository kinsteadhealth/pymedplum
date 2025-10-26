# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Annotation(MedplumFHIRBase):
    """A text note which also contains information about who made the statement and when."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    author_reference: Optional[Reference] = Field(default=None, alias="authorReference", description="The individual responsible for making the annotation.")
    author_string: Optional[str] = Field(default=None, alias="authorString", description="The individual responsible for making the annotation.")
    time: Optional[str] = Field(default=None, description="Indicates when this particular annotation was made.")
    text: str = Field(default=..., description="The text of the annotation in markdown format.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Annotation", Annotation)
