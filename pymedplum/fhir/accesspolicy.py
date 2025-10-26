# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class AccessPolicy(MedplumFHIRBase):
    """Access Policy for user or user group that defines how entities can or
    cannot access resources.
    """

    resource_type: Literal["AccessPolicy"] = Field(
        default="AccessPolicy",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[list[dict[str, Any]]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: Optional[str] = Field(default=None, description="A name associated with the AccessPolicy.")
    based_on: Optional[list[Reference]] = Field(default=None, alias="basedOn", description="Other access policies used to derive this access policy.")
    compartment: Optional[Reference] = Field(default=None, description="Optional compartment for newly created resources. If this field is set, any resources created by a user with this access policy will automatically be included in the specified compartment.")
    resource: Optional[list[AccessPolicyResource]] = Field(default=None, description="Access details for a resource type.")
    ip_access_rule: Optional[list[AccessPolicyIpAccessRule]] = Field(default=None, alias="ipAccessRule", description="Use IP Access Rules to allowlist, block, and challenge traffic based on the visitor IP address.")


class AccessPolicyIpAccessRule(MedplumFHIRBase):
    """Use IP Access Rules to allowlist, block, and challenge traffic based on
    the visitor IP address.
    """

    name: Optional[str] = Field(default=None, description="Friendly name that will make it easy for you to identify the IP Access Rule in the future.")
    value: str = Field(default=..., description="An IP Access rule will apply a certain action to incoming traffic based on the visitor IP address or IP range.")
    action: Literal['allow', 'block'] = Field(default=..., description="Access rule can perform one of the following actions: &quot;allow&quot; | &quot;block&quot;.")


class AccessPolicyResource(MedplumFHIRBase):
    """Access details for a resource type."""

    resource_type: Literal["AccessPolicyResource"] = Field(
        default="AccessPolicyResource",
        alias="resourceType"
    )

    compartment: Optional[Reference] = Field(default=None)
    criteria: Optional[str] = Field(default=None, description="The rules that the server should use to determine which resources to allow.")
    readonly: Optional[bool] = Field(default=None, description="Optional flag to indicate that the resource type is read-only.")
    hidden_fields: Optional[list[str]] = Field(default=None, alias="hiddenFields", description="Optional list of hidden fields. Hidden fields are not readable or writeable.")
    readonly_fields: Optional[list[str]] = Field(default=None, alias="readonlyFields", description="Optional list of read-only fields. Read-only fields are readable but not writeable.")
    write_constraint: Optional[list[Expression]] = Field(default=None, alias="writeConstraint", description="Invariants that must be satisfied for the resource to be written. Can include %before and %after placeholders to refer to the resource before and after the updates are applied.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("AccessPolicy", AccessPolicy)
    register_model("AccessPolicyIpAccessRule", AccessPolicyIpAccessRule)
    register_model("AccessPolicyResource", AccessPolicyResource)
