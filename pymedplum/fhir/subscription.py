# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative


class Subscription(MedplumFHIRBase):
    """The subscription resource is used to define a push-based subscription
    from a server to another system. Once a subscription is registered with
    the server, the server checks every resource that is created or updated,
    and if the resource matches the given criteria, it sends a message on
    the defined &quot;channel&quot; so that another system can take an
    appropriate action.
    """

    resource_type: Literal["Subscription"] = Field(
        default="Subscription", alias="resourceType"
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
    status: Literal["requested", "active", "error", "off"] = Field(
        default=...,
        description="The status of the subscription, which marks the server state for managing the subscription.",
    )
    contact: Optional[list[ContactPoint]] = Field(
        default=None,
        description="Contact details for a human to contact about the subscription. The primary use of this for system administrator troubleshooting.",
    )
    end: Optional[str] = Field(
        default=None,
        description="The time for the server to turn the subscription off.",
    )
    reason: str = Field(
        default=..., description="A description of why this subscription is defined."
    )
    criteria: str = Field(
        default=...,
        description="The rules that the server should use to determine when to generate notifications for this subscription.",
    )
    error: Optional[str] = Field(
        default=None,
        description="A record of the last error that occurred when the server processed a notification.",
    )
    channel: SubscriptionChannel = Field(
        default=...,
        description="Details where to send notifications when resources are received that meet the criteria.",
    )


class SubscriptionChannel(MedplumFHIRBase):
    """Details where to send notifications when resources are received that
    meet the criteria.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Literal["rest-hook", "websocket", "email", "sms", "message"] = Field(
        default=..., description="The type of channel to send notifications on."
    )
    endpoint: Optional[str] = Field(
        default=None,
        description="The url that describes the actual end-point to send messages to.",
    )
    payload: Optional[str] = Field(
        default=None,
        description="The mime type to send the payload in - either application/fhir+xml, or application/fhir+json. If the payload is not present, then there is no payload in the notification, just a notification. The mime type &quot;text/plain&quot; may also be used for Email and SMS subscriptions.",
    )
    header: Optional[list[str]] = Field(
        default=None,
        description="Additional headers / information to send as part of the notification.",
    )
