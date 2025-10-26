# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Address(MedplumFHIRBase):
    """An address expressed using postal conventions (as opposed to GPS or
    other location definition formats). This data type may be used to convey
    addresses for use in delivering mail as well as for visiting locations
    which might not be valid for mail delivery. There are a variety of
    postal address formats defined around the world.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    use: Optional[Literal["home", "work", "temp", "old", "billing"]] = Field(
        default=None, description="The purpose of this address."
    )
    type: Optional[Literal["postal", "physical", "both"]] = Field(
        default=None,
        description="Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.",
    )
    text: Optional[str] = Field(
        default=None,
        description="Specifies the entire address as it should be displayed e.g. on a postal label. This may be provided instead of or as well as the specific parts.",
    )
    line: Optional[List[str]] = Field(
        default=None,
        description="This component contains the house number, apartment number, street name, street direction, P.O. Box number, delivery hints, and similar address information.",
    )
    city: Optional[str] = Field(
        default=None,
        description="The name of the city, town, suburb, village or other community or delivery center.",
    )
    district: Optional[str] = Field(
        default=None, description="The name of the administrative area (county)."
    )
    state: Optional[str] = Field(
        default=None,
        description="Sub-unit of a country with limited sovereignty in a federally organized country. A code may be used if codes are in common use (e.g. US 2 letter state codes).",
    )
    postal_code: Optional[str] = Field(
        default=None,
        alias="postalCode",
        description="A postal code designating a region defined by the postal service.",
    )
    country: Optional[str] = Field(
        default=None,
        description="Country - a nation as commonly understood or generally accepted.",
    )
    period: Optional[Period] = Field(
        default=None, description="Time period when address was/is in use."
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Address", Address)
