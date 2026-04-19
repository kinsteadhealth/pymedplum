# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.reference import Reference


class UsageContext(MedplumFHIRBase):
    """Specifies clinical/business/etc. metadata that can be used to retrieve,
    index and/or categorize an artifact. This metadata can either be
    specific to the applicable population (e.g., age category, DRG) or the
    specific context of care (e.g., venue, care setting, provider of care).
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    code: Coding = Field(
        default=...,
        description="A code that identifies the type of context being specified by this usage context.",
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.",
    )
    value_range: Range | None = Field(
        default=None,
        alias="valueRange",
        description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.",
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.",
    )
