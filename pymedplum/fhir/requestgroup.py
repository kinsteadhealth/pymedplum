# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class RequestGroup(MedplumFHIRBase):
    """A group of related requests that can be used to capture intended
    activities that have inter-dependencies such as &quot;give this
    medication after that one&quot;.
    """

    resource_type: Literal["RequestGroup"] = Field(
        default="RequestGroup", alias="resourceType"
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
        default=None,
        description="Allows a service to provide a unique, business identifier for the request.",
    )
    instantiates_canonical: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesCanonical",
        description="A canonical URL referencing a FHIR-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this request.",
    )
    instantiates_uri: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesUri",
        description="A URL referencing an externally defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this request.",
    )
    based_on: Optional[list[Reference]] = Field(
        default=None,
        alias="basedOn",
        description="A plan, proposal or order that is fulfilled in whole or in part by this request.",
    )
    replaces: Optional[list[Reference]] = Field(
        default=None,
        description="Completed or terminated request(s) whose function is taken by this new request.",
    )
    group_identifier: Optional[Identifier] = Field(
        default=None,
        alias="groupIdentifier",
        description="A shared identifier common to all requests that were authorized more or less simultaneously by a single author, representing the identifier of the requisition, prescription or similar form.",
    )
    status: Literal[
        "draft",
        "active",
        "on-hold",
        "revoked",
        "completed",
        "entered-in-error",
        "unknown",
    ] = Field(
        default=...,
        description="The current state of the request. For request groups, the status reflects the status of all the requests in the group.",
    )
    intent: Literal[
        "proposal",
        "plan",
        "directive",
        "order",
        "original-order",
        "reflex-order",
        "filler-order",
        "instance-order",
        "option",
    ] = Field(
        default=...,
        description="Indicates the level of authority/intentionality associated with the request and where the request fits into the workflow chain.",
    )
    priority: Optional[Literal["routine", "urgent", "asap", "stat"]] = Field(
        default=None,
        description="Indicates how quickly the request should be addressed with respect to other requests.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="A code that identifies what the overall request group is.",
    )
    subject: Optional[Reference] = Field(
        default=None, description="The subject for which the request group was created."
    )
    encounter: Optional[Reference] = Field(
        default=None, description="Describes the context of the request group, if any."
    )
    authored_on: Optional[str] = Field(
        default=None,
        alias="authoredOn",
        description="Indicates when the request group was created.",
    )
    author: Optional[Reference] = Field(
        default=None,
        description="Provides a reference to the author of the request group.",
    )
    reason_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="reasonCode",
        description="Describes the reason for the request group in coded or textual form.",
    )
    reason_reference: Optional[list[Reference]] = Field(
        default=None,
        alias="reasonReference",
        description="Indicates another resource whose existence justifies this request group.",
    )
    note: Optional[list[Annotation]] = Field(
        default=None,
        description="Provides a mechanism to communicate additional information about the response.",
    )
    action: Optional[list[RequestGroupAction]] = Field(
        default=None,
        description="The actions, if any, produced by the evaluation of the artifact.",
    )


class RequestGroupAction(MedplumFHIRBase):
    """The actions, if any, produced by the evaluation of the artifact."""

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
    prefix: Optional[str] = Field(
        default=None, description="A user-visible prefix for the action."
    )
    title: Optional[str] = Field(
        default=None, description="The title of the action displayed to a user."
    )
    description: Optional[str] = Field(
        default=None,
        description="A short description of the action used to provide a summary to display to the user.",
    )
    text_equivalent: Optional[str] = Field(
        default=None,
        alias="textEquivalent",
        description="A text equivalent of the action to be performed. This provides a human-interpretable description of the action when the definition is consumed by a system that might not be capable of interpreting it dynamically.",
    )
    priority: Optional[Literal["routine", "urgent", "asap", "stat"]] = Field(
        default=None,
        description="Indicates how quickly the action should be addressed with respect to other actions.",
    )
    code: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A code that provides meaning for the action or action group. For example, a section may have a LOINC code for a section of a documentation template.",
    )
    documentation: Optional[list[RelatedArtifact]] = Field(
        default=None,
        description="Didactic or other informational resources associated with the action that can be provided to the CDS recipient. Information resources can include inline text commentary and links to web resources.",
    )
    condition: Optional[list[RequestGroupActionCondition]] = Field(
        default=None,
        description="An expression that describes applicability criteria, or start/stop conditions for the action.",
    )
    related_action: Optional[list[RequestGroupActionRelatedAction]] = Field(
        default=None,
        alias="relatedAction",
        description="A relationship to another action such as &quot;before&quot; or &quot;30-60 minutes after start of&quot;.",
    )
    timing_date_time: Optional[str] = Field(
        default=None,
        alias="timingDateTime",
        description="An optional value describing when the action should be performed.",
    )
    timing_age: Optional[Age] = Field(
        default=None,
        alias="timingAge",
        description="An optional value describing when the action should be performed.",
    )
    timing_period: Optional[Period] = Field(
        default=None,
        alias="timingPeriod",
        description="An optional value describing when the action should be performed.",
    )
    timing_duration: Optional[Duration] = Field(
        default=None,
        alias="timingDuration",
        description="An optional value describing when the action should be performed.",
    )
    timing_range: Optional[Range] = Field(
        default=None,
        alias="timingRange",
        description="An optional value describing when the action should be performed.",
    )
    timing_timing: Optional[Timing] = Field(
        default=None,
        alias="timingTiming",
        description="An optional value describing when the action should be performed.",
    )
    participant: Optional[list[Reference]] = Field(
        default=None,
        description="The participant that should perform or be responsible for this action.",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The type of action to perform (create, update, remove).",
    )
    grouping_behavior: Optional[
        Literal["visual-group", "logical-group", "sentence-group"]
    ] = Field(
        default=None,
        alias="groupingBehavior",
        description="Defines the grouping behavior for the action and its children.",
    )
    selection_behavior: Optional[
        Literal[
            "any", "all", "all-or-none", "exactly-one", "at-most-one", "one-or-more"
        ]
    ] = Field(
        default=None,
        alias="selectionBehavior",
        description="Defines the selection behavior for the action and its children.",
    )
    required_behavior: Optional[Literal["must", "could", "must-unless-documented"]] = (
        Field(
            default=None,
            alias="requiredBehavior",
            description="Defines expectations around whether an action is required.",
        )
    )
    precheck_behavior: Optional[Literal["yes", "no"]] = Field(
        default=None,
        alias="precheckBehavior",
        description="Defines whether the action should usually be preselected.",
    )
    cardinality_behavior: Optional[Literal["single", "multiple"]] = Field(
        default=None,
        alias="cardinalityBehavior",
        description="Defines whether the action can be selected multiple times.",
    )
    resource: Optional[Reference] = Field(
        default=None,
        description="The resource that is the target of the action (e.g. CommunicationRequest).",
    )
    action: Optional[list[RequestGroupAction]] = Field(
        default=None, description="Sub actions."
    )


class RequestGroupActionCondition(MedplumFHIRBase):
    """An expression that describes applicability criteria, or start/stop
    conditions for the action.
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
    kind: Literal["applicability", "start", "stop"] = Field(
        default=..., description="The kind of condition."
    )
    expression: Optional[Expression] = Field(
        default=None,
        description="An expression that returns true or false, indicating whether or not the condition is satisfied.",
    )


class RequestGroupActionRelatedAction(MedplumFHIRBase):
    """A relationship to another action such as &quot;before&quot; or
    &quot;30-60 minutes after start of&quot;.
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
    action_id: str = Field(
        default=...,
        alias="actionId",
        description="The element id of the action this is related to.",
    )
    relationship: Literal[
        "before-start",
        "before",
        "before-end",
        "concurrent-with-start",
        "concurrent",
        "concurrent-with-end",
        "after-start",
        "after",
        "after-end",
    ] = Field(
        default=...,
        description="The relationship of this action to the related action.",
    )
    offset_duration: Optional[Duration] = Field(
        default=None,
        alias="offsetDuration",
        description="A duration or range of durations to apply to the relationship. For example, 30-60 minutes before.",
    )
    offset_range: Optional[Range] = Field(
        default=None,
        alias="offsetRange",
        description="A duration or range of durations to apply to the relationship. For example, 30-60 minutes before.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("RequestGroup", RequestGroup)
    register_model("RequestGroupAction", RequestGroupAction)
    register_model("RequestGroupActionCondition", RequestGroupActionCondition)
    register_model("RequestGroupActionRelatedAction", RequestGroupActionRelatedAction)
