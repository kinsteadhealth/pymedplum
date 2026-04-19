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


class Quantity(MedplumFHIRBase):
    """A measured amount (or an amount that can potentially be measured). Note
    that measured amounts include amounts that are not precisely quantified,
    including amounts involving arbitrary units and floating currencies.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    value: int | float | None = Field(
        default=None,
        description="The value of the measured amount. The value includes an implicit precision in the presentation of the value.",
    )
    comparator: Literal["<", "<=", ">=", ">"] | None = Field(
        default=None,
        description="How the value should be understood and represented - whether the actual value is greater or less than the stated value due to measurement issues; e.g. if the comparator is &quot;&lt;&quot; , then the real value is &lt; stated value.",
    )
    unit: str | None = Field(
        default=None, description="A human-readable form of the unit."
    )
    system: str | None = Field(
        default=None,
        description="The identification of the system that provides the coded form of the unit.",
    )
    code: str | None = Field(
        default=None,
        description="A computer processable form of the unit in some unit representation system.",
    )
