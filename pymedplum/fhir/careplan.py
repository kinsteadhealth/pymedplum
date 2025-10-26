# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CarePlan(MedplumFHIRBase):
    """Describes the intention of how one or more practitioners intend to
    deliver care for a particular patient, group or community for a period
    of time, possibly limited to care for a specific condition or set of
    conditions.
    """

    resource_type: Literal["CarePlan"] = Field(default="CarePlan", alias="resourceType")

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
        description="Business identifiers assigned to this care plan by the performer or other systems which remain constant as the resource is updated and propagates from server to server.",
    )
    instantiates_canonical: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a FHIR-defined protocol, guideline, questionnaire or other definition that is adhered to in whole or in part by this CarePlan.",
    )
    instantiates_uri: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, questionnaire or other definition that is adhered to in whole or in part by this CarePlan.",
    )
    based_on: Optional[list[Reference]] = Field(
        default=None,
        alias="basedOn",
        description="A care plan that is fulfilled in whole or in part by this care plan.",
    )
    replaces: Optional[list[Reference]] = Field(
        default=None,
        description="Completed or terminated care plan whose function is taken by this new care plan.",
    )
    part_of: Optional[list[Reference]] = Field(
        default=None,
        alias="partOf",
        description="A larger care plan of which this particular care plan is a component or step.",
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
        description="Indicates whether the plan is currently being acted upon, represents future intentions or is now a historical record.",
    )
    intent: Literal["proposal", "plan", "order", "option"] = Field(
        default=...,
        description="Indicates the level of authority/intentionality associated with the care plan and where the care plan fits into the workflow chain.",
    )
    category: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Identifies what &quot;kind&quot; of plan this is to support differentiation between multiple co-existing plans; e.g. &quot;Home health&quot;, &quot;psychiatric&quot;, &quot;asthma&quot;, &quot;disease management&quot;, &quot;wellness plan&quot;, etc.",
    )
    title: Optional[str] = Field(
        default=None, description="Human-friendly name for the care plan."
    )
    description: Optional[str] = Field(
        default=None, description="A description of the scope and nature of the plan."
    )
    subject: Reference = Field(
        default=...,
        description="Identifies the patient or group whose intended care is described by the plan.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The Encounter during which this CarePlan was created or to which the creation of this record is tightly associated.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="Indicates when the plan did (or is intended to) come into effect and end.",
    )
    created: Optional[str] = Field(
        default=None,
        description="Represents when this particular CarePlan record was created in the system, which is often a system-generated date.",
    )
    author: Optional[Reference] = Field(
        default=None,
        description="When populated, the author is responsible for the care plan. The care plan is attributed to the author.",
    )
    contributor: Optional[list[Reference]] = Field(
        default=None,
        description="Identifies the individual(s) or organization who provided the contents of the care plan.",
    )
    care_team: Optional[list[Reference]] = Field(
        default=None,
        alias="careTeam",
        description="Identifies all people and organizations who are expected to be involved in the care envisioned by this plan.",
    )
    addresses: Optional[list[Reference]] = Field(
        default=None,
        description="Identifies the conditions/problems/concerns/diagnoses/etc. whose management and/or mitigation are handled by this plan.",
    )
    supporting_info: Optional[list[Reference]] = Field(
        default=None,
        alias="supportingInfo",
        description="Identifies portions of the patient's record that specifically influenced the formation of the plan. These might include comorbidities, recent procedures, limitations, recent assessments, etc.",
    )
    goal: Optional[list[Reference]] = Field(
        default=None,
        description="Describes the intended objective(s) of carrying out the care plan.",
    )
    activity: Optional[list[CarePlanActivity]] = Field(
        default=None,
        description="Identifies a planned action to occur as part of the plan. For example, a medication to be used, lab tests to perform, self-monitoring, education, etc.",
    )
    note: Optional[list[Annotation]] = Field(
        default=None,
        description="General notes about the care plan not covered elsewhere.",
    )


class CarePlanActivity(MedplumFHIRBase):
    """Identifies a planned action to occur as part of the plan. For example, a
    medication to be used, lab tests to perform, self-monitoring, education,
    etc.
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
    outcome_codeable_concept: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="outcomeCodeableConcept",
        description="Identifies the outcome at the point when the status of the activity is assessed. For example, the outcome of an education activity could be patient understands (or not).",
    )
    outcome_reference: Optional[list[Reference]] = Field(
        default=None,
        alias="outcomeReference",
        description="Details of the outcome or action resulting from the activity. The reference to an &quot;event&quot; resource, such as Procedure or Encounter or Observation, is the result/outcome of the activity itself. The activity can be conveyed using CarePlan.activity.detail OR using the CarePlan.activity.reference (a reference to a &ldquo;request&rdquo; resource).",
    )
    progress: Optional[list[Annotation]] = Field(
        default=None,
        description="Notes about the adherence/status/progress of the activity.",
    )
    reference: Optional[Union[Reference]] = Field(
        default=None,
        description="The details of the proposed activity represented in a specific resource.",
    )
    detail: Optional[CarePlanActivityDetail] = Field(
        default=None,
        description="A simple summary of a planned activity suitable for a general care plan system (e.g. form driven) that doesn't know about specific resources such as procedure etc.",
    )


class CarePlanActivityDetail(MedplumFHIRBase):
    """A simple summary of a planned activity suitable for a general care plan
    system (e.g. form driven) that doesn't know about specific resources
    such as procedure etc.
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
    kind: Optional[
        Literal[
            "Appointment",
            "CommunicationRequest",
            "DeviceRequest",
            "MedicationRequest",
            "NutritionOrder",
            "Task",
            "ServiceRequest",
            "VisionPrescription",
        ]
    ] = Field(
        default=None,
        description="A description of the kind of resource the in-line definition of a care plan activity is representing. The CarePlan.activity.detail is an in-line definition when a resource is not referenced using CarePlan.activity.reference. For example, a MedicationRequest, a ServiceRequest, or a CommunicationRequest.",
    )
    instantiates_canonical: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a FHIR-defined protocol, guideline, questionnaire or other definition that is adhered to in whole or in part by this CarePlan activity.",
    )
    instantiates_uri: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, questionnaire or other definition that is adhered to in whole or in part by this CarePlan activity.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="Detailed description of the type of planned activity; e.g. what lab test, what procedure, what kind of encounter.",
    )
    reason_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="reasonCode",
        description="Provides the rationale that drove the inclusion of this particular activity as part of the plan or the reason why the activity was prohibited.",
    )
    reason_reference: Optional[list[Reference]] = Field(
        default=None,
        alias="reasonReference",
        description="Indicates another resource, such as the health condition(s), whose existence justifies this request and drove the inclusion of this particular activity as part of the plan.",
    )
    goal: Optional[list[Reference]] = Field(
        default=None,
        description="Internal reference that identifies the goals that this activity is intended to contribute towards meeting.",
    )
    status: Literal[
        "not-started",
        "scheduled",
        "in-progress",
        "on-hold",
        "completed",
        "cancelled",
        "stopped",
        "unknown",
        "entered-in-error",
    ] = Field(
        default=...,
        description="Identifies what progress is being made for the specific activity.",
    )
    status_reason: Optional[CodeableConcept] = Field(
        default=None,
        alias="statusReason",
        description="Provides reason why the activity isn't yet started, is on hold, was cancelled, etc.",
    )
    do_not_perform: Optional[bool] = Field(
        default=None,
        alias="doNotPerform",
        description="If true, indicates that the described activity is one that must NOT be engaged in when following the plan. If false, or missing, indicates that the described activity is one that should be engaged in when following the plan.",
    )
    scheduled_timing: Optional[Timing] = Field(
        default=None,
        alias="scheduledTiming",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    scheduled_period: Optional[Period] = Field(
        default=None,
        alias="scheduledPeriod",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    scheduled_string: Optional[str] = Field(
        default=None,
        alias="scheduledString",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    location: Optional[Reference] = Field(
        default=None,
        description="Identifies the facility where the activity will occur; e.g. home, hospital, specific clinic, etc.",
    )
    performer: Optional[list[Reference]] = Field(
        default=None,
        description="Identifies who's expected to be involved in the activity.",
    )
    product_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="productCodeableConcept",
        description="Identifies the food, drug or other product to be consumed or supplied in the activity.",
    )
    product_reference: Optional[Reference] = Field(
        default=None,
        alias="productReference",
        description="Identifies the food, drug or other product to be consumed or supplied in the activity.",
    )
    daily_amount: Optional[Quantity] = Field(
        default=None,
        alias="dailyAmount",
        description="Identifies the quantity expected to be consumed in a given day.",
    )
    quantity: Optional[Quantity] = Field(
        default=None,
        description="Identifies the quantity expected to be supplied, administered or consumed by the subject.",
    )
    description: Optional[str] = Field(
        default=None,
        description="This provides a textual description of constraints on the intended activity occurrence, including relation to other activities. It may also include objectives, pre-conditions and end-conditions. Finally, it may convey specifics about the activity such as body site, method, route, etc.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CarePlan", CarePlan)
    register_model("CarePlanActivity", CarePlanActivity)
    register_model("CarePlanActivityDetail", CarePlanActivityDetail)
