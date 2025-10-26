# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class IdentityProvider(MedplumFHIRBase):
    """External Identity Provider (IdP) configuration details."""

    authorize_url: str = Field(
        default=...,
        alias="authorizeUrl",
        description="Remote URL for the external Identity Provider authorize endpoint.",
    )
    token_url: str = Field(
        default=...,
        alias="tokenUrl",
        description="Remote URL for the external Identity Provider token endpoint.",
    )
    token_auth_method: Optional[
        Literal["client_secret_basic", "client_secret_post"]
    ] = Field(
        default=None,
        alias="tokenAuthMethod",
        description="Client Authentication method used by Clients to authenticate to the Authorization Server when using the Token Endpoint. If no method is registered, the default method is client_secret_basic.",
    )
    user_info_url: str = Field(
        default=...,
        alias="userInfoUrl",
        description="Remote URL for the external Identity Provider userinfo endpoint.",
    )
    client_id: str = Field(
        default=...,
        alias="clientId",
        description="External Identity Provider client ID.",
    )
    client_secret: str = Field(
        default=...,
        alias="clientSecret",
        description="External Identity Provider client secret.",
    )
    use_pkce: Optional[bool] = Field(
        default=None,
        alias="usePkce",
        description="Optional flag to use PKCE in the token request.",
    )
    use_subject: Optional[bool] = Field(
        default=None,
        alias="useSubject",
        description="Optional flag to use the subject field instead of the email field.",
    )
