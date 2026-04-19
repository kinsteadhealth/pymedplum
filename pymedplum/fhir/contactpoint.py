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
    from pymedplum.fhir.period import Period


class ContactPoint(MedplumFHIRBase):
    """Details for all kinds of technology mediated contact points for a person
    or organization, including telephone, email, etc.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    system: Literal["phone", "fax", "email", "pager", "url", "sms", "other"] | None = (
        Field(
            default=None,
            description="Telecommunications form for contact point - what communications system is required to make use of the contact.",
        )
    )
    value: str | None = Field(
        default=None,
        description="The actual contact point details, in a form that is meaningful to the designated communication system (i.e. phone number or email address).",
    )
    use: Literal["home", "work", "temp", "old", "mobile"] | None = Field(
        default=None, description="Identifies the purpose for the contact point."
    )
    rank: int | float | None = Field(
        default=None,
        description="Specifies a preferred order in which to use a set of contacts. ContactPoints with lower rank values are more preferred than those with higher rank values.",
    )
    period: Period | None = Field(
        default=None, description="Time period when the contact point was/is in use."
    )
