# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class ClientApplication(MedplumFHIRBase):
    """Medplum client application for automated access."""

    resource_type: Literal["ClientApplication"] = Field(
        default="ClientApplication",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    status: Optional[Literal['active', 'off', 'error']] = Field(default=None, description="The client application status. The status is active by default. The status can be set to error to indicate that the client application is not working properly. The status can be set to off to indicate that the client application is no longer in use.")
    name: Optional[str] = Field(default=None, description="A name associated with the ClientApplication.")
    description: Optional[str] = Field(default=None, description="A summary, characterization or explanation of the ClientApplication.")
    sign_in_form: Optional[ClientApplicationSignInForm] = Field(default=None, alias="signInForm", description="Custom values for the Log In form.")
    secret: Optional[str] = Field(default=None, description="Client secret string used to verify the identity of a client.")
    jwks_uri: Optional[str] = Field(default=None, alias="jwksUri", description="Optional JWKS URI for public key verification of JWTs issued by the authorization server (client_secret_jwt).")
    redirect_uri: Optional[str] = Field(default=None, alias="redirectUri", description="Optional redirect URI used when redirecting a client back to the client application.")
    launch_uri: Optional[str] = Field(default=None, alias="launchUri", description="Optional launch URI for SMART EHR launch sequence.")
    pkce_optional: Optional[bool] = Field(default=None, alias="pkceOptional", description="Flag to make PKCE optional for this client application. PKCE is required by default for compliance with Smart App Launch. It can be disabled for compatibility with legacy client applications.")
    identity_provider: Optional[IdentityProvider] = Field(default=None, alias="identityProvider", description="Optional external Identity Provider (IdP) for the client application.")
    access_token_lifetime: Optional[str] = Field(default=None, alias="accessTokenLifetime", description="Optional configuration to set the access token duration")
    refresh_token_lifetime: Optional[str] = Field(default=None, alias="refreshTokenLifetime", description="Optional configuration to set the refresh token duration")


class ClientApplicationSignInForm(MedplumFHIRBase):
    """Custom values for the Log In form."""

    welcome_string: Optional[str] = Field(default=None, alias="welcomeString", description="Welcome string for the Log In Form.")
    logo: Optional[Attachment] = Field(default=None, description="Logo for the Log In Form.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ClientApplication", ClientApplication)
    register_model("ClientApplicationSignInForm", ClientApplicationSignInForm)
