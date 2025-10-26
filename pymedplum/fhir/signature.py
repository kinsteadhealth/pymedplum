# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Signature(MedplumFHIRBase):
    """A signature along with supporting context. The signature may be a
    digital signature that is cryptographic in nature, or some other
    signature acceptable to the domain. This other signature may be as
    simple as a graphical image representing a hand-written signature, or a
    signature ceremony Different signature approaches have different
    utilities.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    type: list[Coding] = Field(default=..., description="An indication of the reason that the entity signed this document. This may be explicitly included as part of the signature information and can be used when determining accountability for various actions concerning the document.")
    when: str = Field(default=..., description="When the digital signature was signed.")
    who: Reference = Field(default=..., description="A reference to an application-usable description of the identity that signed (e.g. the signature used their private key).")
    on_behalf_of: Optional[Reference] = Field(default=None, alias="onBehalfOf", description="A reference to an application-usable description of the identity that is represented by the signature.")
    target_format: Optional[str] = Field(default=None, alias="targetFormat", description="A mime type that indicates the technical format of the target resources signed by the signature.")
    sig_format: Optional[str] = Field(default=None, alias="sigFormat", description="A mime type that indicates the technical format of the signature. Important mime types are application/signature+xml for X ML DigSig, application/jose for JWS, and image/* for a graphical image of a signature, etc.")
    data: Optional[str] = Field(default=None, description="The base64 encoding of the Signature content. When signature is not recorded electronically this element would be empty.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("Signature", Signature)
