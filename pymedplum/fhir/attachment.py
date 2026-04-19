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


class Attachment(MedplumFHIRBase):
    """For referring to data content defined in other formats."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    content_type: str | None = Field(
        default=None,
        alias="contentType",
        description="Identifies the type of the data in the attachment and allows a method to be chosen to interpret or render the data. Includes mime type parameters such as charset where appropriate.",
    )
    language: str | None = Field(
        default=None,
        description="The human language of the content. The value can be any valid value according to BCP 47.",
    )
    data: str | None = Field(
        default=None,
        description="The actual data of the attachment - a sequence of bytes, base64 encoded.",
    )
    url: str | None = Field(
        default=None, description="A location where the data can be accessed."
    )
    size: int | float | None = Field(
        default=None,
        description="The number of bytes of data that make up this attachment (before base64 encoding, if that is done).",
    )
    hash: str | None = Field(
        default=None,
        description="The calculated hash of the data using SHA-1. Represented using base64.",
    )
    title: str | None = Field(
        default=None,
        description="A label or set of text to display in place of the data.",
    )
    creation: str | None = Field(
        default=None, description="The date that the attachment was first created."
    )
