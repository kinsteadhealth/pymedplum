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


class Address(MedplumFHIRBase):
    """An address expressed using postal conventions (as opposed to GPS or
    other location definition formats). This data type may be used to convey
    addresses for use in delivering mail as well as for visiting locations
    which might not be valid for mail delivery. There are a variety of
    postal address formats defined around the world.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    use: Literal["home", "work", "temp", "old", "billing"] | None = Field(
        default=None, description="The purpose of this address."
    )
    type: Literal["postal", "physical", "both"] | None = Field(
        default=None,
        description="Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.",
    )
    text: str | None = Field(
        default=None,
        description="Specifies the entire address as it should be displayed e.g. on a postal label. This may be provided instead of or as well as the specific parts.",
    )
    line: list[str] | None = Field(
        default=None,
        description="This component contains the house number, apartment number, street name, street direction, P.O. Box number, delivery hints, and similar address information.",
    )
    city: str | None = Field(
        default=None,
        description="The name of the city, town, suburb, village or other community or delivery center.",
    )
    district: str | None = Field(
        default=None, description="The name of the administrative area (county)."
    )
    state: str | None = Field(
        default=None,
        description="Sub-unit of a country with limited sovereignty in a federally organized country. A code may be used if codes are in common use (e.g. US 2 letter state codes).",
    )
    postal_code: str | None = Field(
        default=None,
        alias="postalCode",
        description="A postal code designating a region defined by the postal service.",
    )
    country: str | None = Field(
        default=None,
        description="Country - a nation as commonly understood or generally accepted.",
    )
    period: Period | None = Field(
        default=None, description="Time period when address was/is in use."
    )
