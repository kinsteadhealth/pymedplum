# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class Identifier(MedplumFHIRBase):
    """An identifier - identifies some entity uniquely and unambiguously.
    Typically this is used for business identifiers.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    use: Literal["usual", "official", "temp", "secondary", "old"] | None = Field(
        default=None, description="The purpose of this identifier."
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="A coded type for the identifier that can be used to determine which identifier to use for a specific purpose.",
    )
    system: str | None = Field(
        default=None,
        description="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    value: str | None = Field(
        default=None,
        description="The portion of the identifier typically relevant to the user and which is unique within the context of the system.",
    )
    period: Period | None = Field(
        default=None,
        description="Time period during which identifier is/was valid for use.",
    )
    assigner: Reference | None = Field(
        default=None, description="Organization that issued/manages the identifier."
    )
