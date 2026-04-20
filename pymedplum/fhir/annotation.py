# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.reference import Reference


class Annotation(MedplumFHIRBase):
    """A text note which also contains information about who made the statement and when."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    author_reference: Reference | None = Field(
        default=None,
        alias="authorReference",
        description="The individual responsible for making the annotation.",
    )
    author_string: str | None = Field(
        default=None,
        alias="authorString",
        description="The individual responsible for making the annotation.",
    )
    time: str | None = Field(
        default=None, description="Indicates when this particular annotation was made."
    )
    text: str = Field(
        default=..., description="The text of the annotation in markdown format."
    )
