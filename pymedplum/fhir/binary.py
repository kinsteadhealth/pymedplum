# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.reference import Reference


class Binary(MedplumFHIRBase):
    """A resource that represents the data of a single raw artifact as digital
    content accessible in its native format. A Binary resource can contain
    any content, whether text, image, pdf, zip archive, etc.
    """

    resource_type: Literal["Binary"] = Field(default="Binary", alias="resourceType")

    id: str | None = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Meta | None = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: str | None = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: str | None = Field(
        default=None, description="The base language in which the resource is written."
    )
    content_type: str = Field(
        default=...,
        alias="contentType",
        description="MimeType of the binary content represented as a standard MimeType (BCP 13).",
    )
    security_context: Reference | None = Field(
        default=None,
        alias="securityContext",
        description="This element identifies another resource that can be used as a proxy of the security sensitivity to use when deciding and enforcing access control rules for the Binary resource. Given that the Binary resource contains very few elements that can be used to determine the sensitivity of the data and relationships to individuals, the referenced resource stands in as a proxy equivalent for this purpose. This referenced resource may be related to the Binary (e.g. Media, DocumentReference), or may be some non-related Resource purely as a security proxy. E.g. to identify that the binary resource relates to a patient, and access should only be granted to applications that have access to the patient.",
    )
    data: str | None = Field(
        default=None, description="The actual content, base64 encoded."
    )
    url: str | None = Field(
        default=None, description="A location where the data can be accessed."
    )
