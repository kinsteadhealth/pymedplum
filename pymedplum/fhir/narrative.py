# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension


class Narrative(MedplumFHIRBase):
    """A human-readable summary of the resource conveying the essential
    clinical and business information for the resource.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    status: Literal["generated", "extensions", "additional", "empty"] = Field(
        default=...,
        description="The status of the narrative - whether it's entirely generated (from just the defined data or the extensions too), or whether a human authored it and it may contain additional data.",
    )
    div: str = Field(
        default=...,
        description="The actual narrative content, a stripped down version of XHTML.",
    )
