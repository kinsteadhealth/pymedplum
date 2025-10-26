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
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.resourcetype import ResourceType


class Login(MedplumFHIRBase):
    """Login event and session details."""

    resource_type: Literal["Login"] = Field(default="Login", alias="resourceType")

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
    client: Reference | None = Field(
        default=None, description="The client requesting the code."
    )
    profile_type: ResourceType | None = Field(
        default=None,
        alias="profileType",
        description="Optional required profile resource type.",
    )
    project: Reference | None = Field(
        default=None, description="Optional required project for the login."
    )
    user: Reference = Field(default=..., description="The user requesting the code.")
    membership: Reference | None = Field(
        default=None,
        description="Reference to the project membership which includes FHIR identity (patient, practitioner, etc), access policy, and user configuration.",
    )
    scope: str | None = Field(default=None, description="OAuth scope or scopes.")
    auth_method: Literal[
        "client", "exchange", "execute", "external", "google", "password"
    ] = Field(
        default=...,
        alias="authMethod",
        description="The authentication method used to obtain the code (password or google).",
    )
    auth_time: str = Field(
        default=...,
        alias="authTime",
        description="Time when the End-User authentication occurred.",
    )
    cookie: str | None = Field(
        default=None,
        description="The cookie value that can be used for session management.",
    )
    code: str | None = Field(
        default=None,
        description="The authorization code generated by the authorization server. The authorization code MUST expire shortly after it is issued to mitigate the risk of leaks. A maximum authorization code lifetime of 10 minutes is RECOMMENDED. The client MUST NOT use the authorization code more than once. If an authorization code is used more than once, the authorization server MUST deny the request and SHOULD revoke (when possible) all tokens previously issued based on that authorization code. The authorization code is bound to the client identifier and redirection URI.",
    )
    code_challenge: str | None = Field(
        default=None,
        alias="codeChallenge",
        description="PKCE code challenge presented in the authorization request.",
    )
    code_challenge_method: Literal["plain", "S256"] | None = Field(
        default=None,
        alias="codeChallengeMethod",
        description="OPTIONAL, defaults to &quot;plain&quot; if not present in the request. Code verifier transformation method is &quot;S256&quot; or &quot;plain&quot;.",
    )
    refresh_secret: str | None = Field(
        default=None,
        alias="refreshSecret",
        description="Optional secure random string that can be used in an OAuth refresh token.",
    )
    nonce: str | None = Field(
        default=None,
        description="Optional cryptographically random string that your app adds to the initial request and the authorization server includes inside the ID Token, used to prevent token replay attacks.",
    )
    mfa_verified: bool | None = Field(
        default=None,
        alias="mfaVerified",
        description="Whether the user has verified using multi-factor authentication (MFA). This will only be set is the user has MFA enabled (see User.mfaEnrolled).",
    )
    granted: bool | None = Field(
        default=None, description="Whether a token has been granted for this login."
    )
    revoked: bool | None = Field(
        default=None, description="Whether this login has been revoked or invalidated."
    )
    admin: bool | None = Field(default=None)
    super_admin: bool | None = Field(default=None, alias="superAdmin")
    launch: Reference | None = Field(
        default=None, description="Optional SMART App Launch context for this login."
    )
    remote_address: str | None = Field(
        default=None,
        alias="remoteAddress",
        description="The Internet Protocol (IP) address of the client or last proxy that sent the request.",
    )
    user_agent: str | None = Field(
        default=None,
        alias="userAgent",
        description="The User-Agent request header as sent by the client.",
    )
