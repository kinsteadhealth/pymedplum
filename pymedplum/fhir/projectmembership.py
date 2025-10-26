# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ProjectMembership(MedplumFHIRBase):
    """Medplum project membership. A project membership grants a user access to a project."""

    resource_type: Literal["ProjectMembership"] = Field(
        default="ProjectMembership", alias="resourceType"
    )

    id: Optional[str] = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Optional[Meta] = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: Optional[str] = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: Optional[str] = Field(
        default=None, description="The base language in which the resource is written."
    )
    text: Optional[Narrative] = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None, description="An identifier for this ProjectMembership."
    )
    active: Optional[bool] = Field(
        default=None,
        description="Whether this project membership record is in active use.",
    )
    project: Reference = Field(
        default=..., description="Project where the memberships are available."
    )
    invited_by: Optional[Reference] = Field(
        default=None,
        alias="invitedBy",
        description="The project administrator who invited the user to the project.",
    )
    user: Reference = Field(
        default=..., description="User that is granted access to the project."
    )
    profile: Reference = Field(
        default=...,
        description="Reference to the resource that represents the user profile within the project.",
    )
    user_name: Optional[str] = Field(
        default=None,
        alias="userName",
        description="SCIM userName. A service provider's unique identifier for the user, typically used by the user to directly authenticate to the service provider. Often displayed to the user as their unique identifier within the system (as opposed to &quot;id&quot; or &quot;externalId&quot;, which are generally opaque and not user-friendly identifiers). Each User MUST include a non-empty userName value. This identifier MUST be unique across the service provider's entire set of Users. This attribute is REQUIRED and is case insensitive.",
    )
    external_id: Optional[str] = Field(
        default=None,
        alias="externalId",
        description="SCIM externalId. A String that is an identifier for the resource as defined by the provisioning client. The &quot;externalId&quot; may simplify identification of a resource between the provisioning client and the service provider by allowing the client to use a filter to locate the resource with an identifier from the provisioning domain, obviating the need to store a local mapping between the provisioning domain's identifier of the resource and the identifier used by the service provider. Each resource MAY include a non-empty &quot;externalId&quot; value. The value of the &quot;externalId&quot; attribute is always issued by the provisioning client and MUST NOT be specified by the service provider. The service provider MUST always interpret the externalId as scoped to the provisioning domain.",
    )
    access_policy: Optional[Reference] = Field(
        default=None,
        alias="accessPolicy",
        description="The access policy for the user within the project memebership.",
    )
    access: Optional[list[ProjectMembershipAccess]] = Field(
        default=None,
        description="Extended access configuration using parameterized access policies.",
    )
    user_configuration: Optional[Reference] = Field(
        default=None,
        alias="userConfiguration",
        description="The user configuration for the user within the project memebership such as menu links, saved searches, and features.",
    )
    admin: Optional[bool] = Field(
        default=None, description="Whether this user is a project administrator."
    )


class ProjectMembershipAccess(MedplumFHIRBase):
    """Extended access configuration using parameterized access policies."""

    policy: Reference = Field(
        default=...,
        description="The base access policy used as a template. Variables in the template access policy are replaced by the values in the parameter.",
    )
    parameter: Optional[list[ProjectMembershipAccessParameter]] = Field(
        default=None,
        description="User options that control the display of the application.",
    )


class ProjectMembershipAccessParameter(MedplumFHIRBase):
    """User options that control the display of the application."""

    name: str = Field(default=..., description="The unique name of the parameter.")
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="Value of the parameter - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="Value of the parameter - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ProjectMembership", ProjectMembership)
    register_model("ProjectMembershipAccess", ProjectMembershipAccess)
    register_model("ProjectMembershipAccessParameter", ProjectMembershipAccessParameter)
