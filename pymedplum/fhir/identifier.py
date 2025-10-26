# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Identifier(MedplumFHIRBase):
    """An identifier - identifies some entity uniquely and unambiguously.
    Typically this is used for business identifiers.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    use: Optional[Literal['usual', 'official', 'temp', 'secondary', 'old']] = Field(default=None, description="The purpose of this identifier.")
    type: Optional[CodeableConcept] = Field(default=None, description="A coded type for the identifier that can be used to determine which identifier to use for a specific purpose.")
    system: Optional[str] = Field(default=None, description="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.")
    value: Optional[str] = Field(default=None, description="The portion of the identifier typically relevant to the user and which is unique within the context of the system.")
    period: Optional[Period] = Field(default=None, description="Time period during which identifier is/was valid for use.")
    assigner: Optional[Reference] = Field(default=None, description="Organization that issued/manages the identifier.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Identifier", Identifier)
