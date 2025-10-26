# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class HumanName(MedplumFHIRBase):
    """A human's name with the ability to identify parts and usage."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    use: Optional[
        Literal["usual", "official", "temp", "nickname", "anonymous", "old", "maiden"]
    ] = Field(default=None, description="Identifies the purpose for this name.")
    text: Optional[str] = Field(
        default=None,
        description="Specifies the entire name as it should be displayed e.g. on an application UI. This may be provided instead of or as well as the specific parts.",
    )
    family: Optional[str] = Field(
        default=None,
        description="The part of a name that links to the genealogy. In some cultures (e.g. Eritrea) the family name of a son is the first name of his father.",
    )
    given: Optional[List[str]] = Field(default=None, description="Given name.")
    prefix: Optional[List[str]] = Field(
        default=None,
        description="Part of the name that is acquired as a title due to academic, legal, employment or nobility status, etc. and that appears at the start of the name.",
    )
    suffix: Optional[List[str]] = Field(
        default=None,
        description="Part of the name that is acquired as a title due to academic, legal, employment or nobility status, etc. and that appears at the end of the name.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="Indicates the period of time when this name was valid for the named person.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("HumanName", HumanName)
