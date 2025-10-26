# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class SubscriptionStatus(MedplumFHIRBase):
    """The SubscriptionStatus resource describes the state of a Subscription
    during notifications.
    """

    resource_type: Literal["SubscriptionStatus"] = Field(
        default="SubscriptionStatus", alias="resourceType"
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
    status: Optional[Literal["requested", "active", "error", "off"]] = Field(
        default=None,
        description="The status of the subscription, which marks the server state for managing the subscription.",
    )
    type: str = Field(
        default=...,
        description="The type of event being conveyed with this notificaiton.",
    )
    events_since_subscription_start: Optional[str] = Field(
        default=None,
        alias="eventsSinceSubscriptionStart",
        description="The total number of actual events which have been generated since the Subscription was created (inclusive of this notification) - regardless of how many have been successfully communicated. This number is NOT incremented for handshake and heartbeat notifications.",
    )
    notification_event: Optional[list[SubscriptionStatusNotificationEvent]] = Field(
        default=None,
        alias="notificationEvent",
        description="Detailed information about events relevant to this subscription notification.",
    )
    subscription: Reference = Field(
        default=...,
        description="The reference to the Subscription which generated this notification.",
    )
    topic: Optional[str] = Field(
        default=None,
        description="The reference to the SubscriptionTopic for the Subscription which generated this notification.",
    )
    error: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A record of errors that occurred when the server processed a notification.",
    )


class SubscriptionStatusNotificationEvent(MedplumFHIRBase):
    """Detailed information about events relevant to this subscription notification."""

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
    event_number: str = Field(
        default=...,
        alias="eventNumber",
        description="The sequential number of this event in this subscription context. Note that this value is a 64-bit integer value, encoded as a string.",
    )
    timestamp: Optional[str] = Field(
        default=None, description="The actual time this event occured on the server."
    )
    focus: Optional[Reference] = Field(
        default=None,
        description="The focus of this event. While this will usually be a reference to the focus resource of the event, it MAY contain a reference to a non-FHIR object.",
    )
    additional_context: Optional[list[Reference]] = Field(
        default=None,
        alias="additionalContext",
        description="Additional context information for this event. Generally, this will contain references to additional resources included with the event (e.g., the Patient relevant to an Encounter), however it MAY refer to non-FHIR objects.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SubscriptionStatus", SubscriptionStatus)
    register_model(
        "SubscriptionStatusNotificationEvent", SubscriptionStatusNotificationEvent
    )
