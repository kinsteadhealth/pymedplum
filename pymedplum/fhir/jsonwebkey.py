# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative


class JsonWebKey(MedplumFHIRBase):
    """A JSON object that represents a cryptographic key. The members of the
    object represent properties of the key, including its value.
    """

    resource_type: Literal["JsonWebKey"] = Field(
        default="JsonWebKey", alias="resourceType"
    )

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
    text: Narrative | None = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: list[dict[str, Any]] | None = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    active: bool | None = Field(
        default=None, description="Whether this key is in active use."
    )
    alg: str = Field(
        default=...,
        description="The specific cryptographic algorithm used with the key.",
    )
    kty: str = Field(
        default=...,
        description="The family of cryptographic algorithms used with the key.",
    )
    use: str | None = Field(
        default=None,
        description="How the key was meant to be used; sig represents the signature.",
    )
    key_ops: list[str] | None = Field(
        default=None,
        description="The operation(s) for which the key is intended to be used.",
    )
    x5c: list[str] | None = Field(
        default=None,
        description="The x.509 certificate chain. The first entry in the array is the certificate to use for token verification; the other certificates can be used to verify this first certificate.",
    )
    n: str | None = Field(
        default=None, description="The modulus for the RSA public key."
    )
    e: str | None = Field(
        default=None, description="The exponent for the RSA public key."
    )
    kid: str | None = Field(
        default=None, description="The unique identifier for the key."
    )
    x5t: str | None = Field(
        default=None, description="The thumbprint of the x.509 cert (SHA-1 thumbprint)."
    )
    d: str | None = Field(
        default=None, description="The exponent for the RSA private key."
    )
    p: str | None = Field(default=None, description="The first prime factor.")
    q: str | None = Field(default=None, description="The second prime factor.")
    dp: str | None = Field(default=None, description="The first factor CRT exponent.")
    dq: str | None = Field(default=None, description="The second factor CRT exponent.")
    qi: str | None = Field(default=None, description="The first CRT coefficient.")
    x: str | None = Field(
        default=None,
        description="The x coordinate of the elliptic curve point (base64url encoded).",
    )
    y: str | None = Field(
        default=None,
        description="The y coordinate of the elliptic curve point (base64url encoded).",
    )
    crv: str | None = Field(
        default=None,
        description="The cryptographic curve identifier (e.g., 'P-256', 'P-384', 'P-521').",
    )
