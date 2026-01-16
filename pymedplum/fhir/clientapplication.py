# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identityprovider import IdentityProvider
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative


class ClientApplication(MedplumFHIRBase):
    """Medplum client application for automated access."""

    resource_type: Literal["ClientApplication"] = Field(
        default="ClientApplication", alias="resourceType"
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
    status: Literal["active", "off", "error"] | None = Field(
        default=None,
        description="The client application status. The status is active by default. The status can be set to error to indicate that the client application is not working properly. The status can be set to off to indicate that the client application is no longer in use.",
    )
    name: str | None = Field(
        default=None, description="A name associated with the ClientApplication."
    )
    description: str | None = Field(
        default=None,
        description="A summary, characterization or explanation of the ClientApplication.",
    )
    sign_in_form: ClientApplicationSignInForm | None = Field(
        default=None,
        alias="signInForm",
        description="Custom values for the Log In form.",
    )
    secret: str | None = Field(
        default=None,
        description="Client secret string used to verify the identity of a client.",
    )
    retiring_secret: str | None = Field(
        default=None,
        alias="retiringSecret",
        description="Old version of the client secret that is being rotated out. Instances of the client using this value should update to use the value in ClientApplication.secret",
    )
    jwks_uri: str | None = Field(
        default=None,
        alias="jwksUri",
        description="Optional JWKS URI for public key verification of JWTs issued by the authorization server (client_secret_jwt).",
    )
    redirect_uri: str | None = Field(default=None, alias="redirectUri")
    redirect_uris: list[str] | None = Field(
        default=None,
        alias="redirectUris",
        description="Optional redirect URI array used when redirecting a client back to the client application.",
    )
    launch_uri: str | None = Field(
        default=None,
        alias="launchUri",
        description="Optional launch URI for SMART EHR launch sequence.",
    )
    pkce_optional: bool | None = Field(
        default=None,
        alias="pkceOptional",
        description="Flag to make PKCE optional for this client application. PKCE is required by default for compliance with Smart App Launch. It can be disabled for compatibility with legacy client applications.",
    )
    identity_provider: IdentityProvider | None = Field(
        default=None,
        alias="identityProvider",
        description="Optional external Identity Provider (IdP) for the client application.",
    )
    access_token_lifetime: str | None = Field(
        default=None,
        alias="accessTokenLifetime",
        description="Optional configuration to set the access token duration",
    )
    refresh_token_lifetime: str | None = Field(
        default=None,
        alias="refreshTokenLifetime",
        description="Optional configuration to set the refresh token duration",
    )
    allowed_origin: list[str] | None = Field(
        default=None,
        alias="allowedOrigin",
        description="Optional CORS allowed origin for the client application. By default, all origins are allowed.",
    )
    default_scope: list[str] | None = Field(
        default=None,
        alias="defaultScope",
        description="Optional default OAuth scope for the client application. This scope is used when the client application does not specify a scope in the authorization request.",
    )


class ClientApplicationSignInForm(MedplumFHIRBase):
    """Custom values for the Log In form."""

    welcome_string: str | None = Field(
        default=None,
        alias="welcomeString",
        description="Welcome string for the Log In Form.",
    )
    logo: Attachment | None = Field(
        default=None, description="Logo for the Log In Form."
    )
