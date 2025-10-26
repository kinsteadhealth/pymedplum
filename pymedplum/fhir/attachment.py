# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Attachment(MedplumFHIRBase):
    """For referring to data content defined in other formats."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    content_type: Optional[str] = Field(
        default=None,
        alias="contentType",
        description="Identifies the type of the data in the attachment and allows a method to be chosen to interpret or render the data. Includes mime type parameters such as charset where appropriate.",
    )
    language: Optional[str] = Field(
        default=None,
        description="The human language of the content. The value can be any valid value according to BCP 47.",
    )
    data: Optional[str] = Field(
        default=None,
        description="The actual data of the attachment - a sequence of bytes, base64 encoded.",
    )
    url: Optional[str] = Field(
        default=None, description="A location where the data can be accessed."
    )
    size: Optional[Union[int, float]] = Field(
        default=None,
        description="The number of bytes of data that make up this attachment (before base64 encoding, if that is done).",
    )
    hash: Optional[str] = Field(
        default=None,
        description="The calculated hash of the data using SHA-1. Represented using base64.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A label or set of text to display in place of the data.",
    )
    creation: Optional[str] = Field(
        default=None, description="The date that the attachment was first created."
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Attachment", Attachment)
