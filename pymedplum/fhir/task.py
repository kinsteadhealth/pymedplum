# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Task(MedplumFHIRBase):
    """A task to be performed."""

    resource_type: Literal["Task"] = Field(default="Task", alias="resourceType")

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
        default=None, description="The business identifier for this task."
    )
    instantiates_canonical: Optional[str] = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a *FHIR*-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this Task.",
    )
    instantiates_uri: Optional[str] = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an *externally* maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this Task.",
    )
    based_on: Optional[list[Reference]] = Field(
        default=None,
        alias="basedOn",
        description="BasedOn refers to a higher-level authorization that triggered the creation of the task. It references a &quot;request&quot; resource such as a ServiceRequest, MedicationRequest, ServiceRequest, CarePlan, etc. which is distinct from the &quot;request&quot; resource the task is seeking to fulfill. This latter resource is referenced by FocusOn. For example, based on a ServiceRequest (= BasedOn), a task is created to fulfill a procedureRequest ( = FocusOn ) to collect a specimen from a patient.",
    )
    group_identifier: Optional[Identifier] = Field(
        default=None,
        alias="groupIdentifier",
        description="An identifier that links together multiple tasks and other requests that were created in the same context.",
    )
    part_of: Optional[list[Reference]] = Field(
        default=None,
        alias="partOf",
        description="Task that this particular task is part of.",
    )
    status: Literal[
        "draft",
        "requested",
        "received",
        "accepted",
        "rejected",
        "ready",
        "cancelled",
        "in-progress",
        "on-hold",
        "failed",
        "completed",
        "entered-in-error",
    ] = Field(default=..., description="The current status of the task.")
    status_reason: Optional[CodeableConcept] = Field(
        default=None,
        alias="statusReason",
        description="An explanation as to why this task is held, failed, was refused, etc.",
    )
    business_status: Optional[CodeableConcept] = Field(
        default=None,
        alias="businessStatus",
        description="Contains business-specific nuances of the business state.",
    )
    intent: Literal[
        "unknown",
        "proposal",
        "plan",
        "order",
        "original-order",
        "reflex-order",
        "filler-order",
        "instance-order",
        "option",
    ] = Field(
        default=...,
        description="Indicates the &quot;level&quot; of actionability associated with the Task, i.e. i+R[9]Cs this a proposed task, a planned task, an actionable task, etc.",
    )
    priority: Optional[Literal["routine", "urgent", "asap", "stat"]] = Field(
        default=None,
        description="Indicates how quickly the Task should be addressed with respect to other requests.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="A name or code (or both) briefly describing what the task involves.",
    )
    description: Optional[str] = Field(
        default=None, description="A free-text description of what is to be performed."
    )
    focus: Optional[Reference] = Field(
        default=None,
        description="The request being actioned or the resource being manipulated by this task.",
    )
    for_: Optional[Reference] = Field(
        default=None,
        alias="for",
        description="The entity who benefits from the performance of the service specified in the task (e.g., the patient).",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The healthcare event (e.g. a patient and healthcare provider interaction) during which this task was created.",
    )
    execution_period: Optional[Period] = Field(
        default=None,
        alias="executionPeriod",
        description="Identifies the time action was first taken against the task (start) and/or the time final action was taken against the task prior to marking it as completed (end).",
    )
    authored_on: Optional[str] = Field(
        default=None,
        alias="authoredOn",
        description="The date and time this task was created.",
    )
    last_modified: Optional[str] = Field(
        default=None,
        alias="lastModified",
        description="The date and time of last modification to this task.",
    )
    requester: Optional[Reference] = Field(
        default=None, description="The creator of the task."
    )
    performer_type: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="performerType",
        description="The kind of participant that should perform the task.",
    )
    owner: Optional[Reference] = Field(
        default=None,
        description="Individual organization or Device currently responsible for task execution.",
    )
    location: Optional[Reference] = Field(
        default=None,
        description="Principal physical location where the this task is performed.",
    )
    reason_code: Optional[CodeableConcept] = Field(
        default=None,
        alias="reasonCode",
        description="A description or code indicating why this task needs to be performed.",
    )
    reason_reference: Optional[Reference] = Field(
        default=None,
        alias="reasonReference",
        description="A resource reference indicating why this task needs to be performed.",
    )
    insurance: Optional[list[Reference]] = Field(
        default=None,
        description="Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be relevant to the Task.",
    )
    note: Optional[list[Annotation]] = Field(
        default=None,
        description="Free-text information captured about the task as it progresses.",
    )
    relevant_history: Optional[list[Reference]] = Field(
        default=None,
        alias="relevantHistory",
        description="Links to Provenance records for past versions of this Task that identify key state transitions or updates that are likely to be relevant to a user looking at the current version of the task.",
    )
    restriction: Optional[TaskRestriction] = Field(
        default=None,
        description="If the Task.focus is a request resource and the task is seeking fulfillment (i.e. is asking for the request to be actioned), this element identifies any limitations on what parts of the referenced request should be actioned.",
    )
    input: Optional[list[TaskInput]] = Field(
        default=None,
        description="Additional information that may be needed in the execution of the task.",
    )
    output: Optional[list[TaskOutput]] = Field(
        default=None, description="Outputs produced by the Task."
    )


class TaskInput(MedplumFHIRBase):
    """Additional information that may be needed in the execution of the task."""

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
    type: CodeableConcept = Field(
        default=...,
        description="A code or description indicating how the input is intended to be used as part of the task execution.",
    )
    value_base64_binary: Optional[str] = Field(
        default=None,
        alias="valueBase64Binary",
        description="The value of the input parameter as a basic type.",
    )
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="The value of the input parameter as a basic type.",
    )
    value_canonical: Optional[str] = Field(
        default=None,
        alias="valueCanonical",
        description="The value of the input parameter as a basic type.",
    )
    value_code: Optional[str] = Field(
        default=None,
        alias="valueCode",
        description="The value of the input parameter as a basic type.",
    )
    value_date: Optional[str] = Field(
        default=None,
        alias="valueDate",
        description="The value of the input parameter as a basic type.",
    )
    value_date_time: Optional[str] = Field(
        default=None,
        alias="valueDateTime",
        description="The value of the input parameter as a basic type.",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="The value of the input parameter as a basic type.",
    )
    value_id: Optional[str] = Field(
        default=None,
        alias="valueId",
        description="The value of the input parameter as a basic type.",
    )
    value_instant: Optional[str] = Field(
        default=None,
        alias="valueInstant",
        description="The value of the input parameter as a basic type.",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="The value of the input parameter as a basic type.",
    )
    value_markdown: Optional[str] = Field(
        default=None,
        alias="valueMarkdown",
        description="The value of the input parameter as a basic type.",
    )
    value_oid: Optional[str] = Field(
        default=None,
        alias="valueOid",
        description="The value of the input parameter as a basic type.",
    )
    value_positive_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="valuePositiveInt",
        description="The value of the input parameter as a basic type.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="The value of the input parameter as a basic type.",
    )
    value_time: Optional[str] = Field(
        default=None,
        alias="valueTime",
        description="The value of the input parameter as a basic type.",
    )
    value_unsigned_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueUnsignedInt",
        description="The value of the input parameter as a basic type.",
    )
    value_uri: Optional[str] = Field(
        default=None,
        alias="valueUri",
        description="The value of the input parameter as a basic type.",
    )
    value_url: Optional[str] = Field(
        default=None,
        alias="valueUrl",
        description="The value of the input parameter as a basic type.",
    )
    value_uuid: Optional[str] = Field(
        default=None,
        alias="valueUuid",
        description="The value of the input parameter as a basic type.",
    )
    value_address: Optional[Address] = Field(
        default=None,
        alias="valueAddress",
        description="The value of the input parameter as a basic type.",
    )
    value_age: Optional[Age] = Field(
        default=None,
        alias="valueAge",
        description="The value of the input parameter as a basic type.",
    )
    value_annotation: Optional[Annotation] = Field(
        default=None,
        alias="valueAnnotation",
        description="The value of the input parameter as a basic type.",
    )
    value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="valueAttachment",
        description="The value of the input parameter as a basic type.",
    )
    value_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="valueCodeableConcept",
        description="The value of the input parameter as a basic type.",
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="The value of the input parameter as a basic type.",
    )
    value_contact_point: Optional[ContactPoint] = Field(
        default=None,
        alias="valueContactPoint",
        description="The value of the input parameter as a basic type.",
    )
    value_count: Optional[Count] = Field(
        default=None,
        alias="valueCount",
        description="The value of the input parameter as a basic type.",
    )
    value_distance: Optional[Distance] = Field(
        default=None,
        alias="valueDistance",
        description="The value of the input parameter as a basic type.",
    )
    value_duration: Optional[Duration] = Field(
        default=None,
        alias="valueDuration",
        description="The value of the input parameter as a basic type.",
    )
    value_human_name: Optional[HumanName] = Field(
        default=None,
        alias="valueHumanName",
        description="The value of the input parameter as a basic type.",
    )
    value_identifier: Optional[Identifier] = Field(
        default=None,
        alias="valueIdentifier",
        description="The value of the input parameter as a basic type.",
    )
    value_money: Optional[Money] = Field(
        default=None,
        alias="valueMoney",
        description="The value of the input parameter as a basic type.",
    )
    value_period: Optional[Period] = Field(
        default=None,
        alias="valuePeriod",
        description="The value of the input parameter as a basic type.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="The value of the input parameter as a basic type.",
    )
    value_range: Optional[Range] = Field(
        default=None,
        alias="valueRange",
        description="The value of the input parameter as a basic type.",
    )
    value_ratio: Optional[Ratio] = Field(
        default=None,
        alias="valueRatio",
        description="The value of the input parameter as a basic type.",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="The value of the input parameter as a basic type.",
    )
    value_sampled_data: Optional[SampledData] = Field(
        default=None,
        alias="valueSampledData",
        description="The value of the input parameter as a basic type.",
    )
    value_signature: Optional[Signature] = Field(
        default=None,
        alias="valueSignature",
        description="The value of the input parameter as a basic type.",
    )
    value_timing: Optional[Timing] = Field(
        default=None,
        alias="valueTiming",
        description="The value of the input parameter as a basic type.",
    )
    value_contact_detail: Optional[ContactDetail] = Field(
        default=None,
        alias="valueContactDetail",
        description="The value of the input parameter as a basic type.",
    )
    value_contributor: Optional[Contributor] = Field(
        default=None,
        alias="valueContributor",
        description="The value of the input parameter as a basic type.",
    )
    value_data_requirement: Optional[DataRequirement] = Field(
        default=None,
        alias="valueDataRequirement",
        description="The value of the input parameter as a basic type.",
    )
    value_expression: Optional[Expression] = Field(
        default=None,
        alias="valueExpression",
        description="The value of the input parameter as a basic type.",
    )
    value_parameter_definition: Optional[ParameterDefinition] = Field(
        default=None,
        alias="valueParameterDefinition",
        description="The value of the input parameter as a basic type.",
    )
    value_related_artifact: Optional[RelatedArtifact] = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="The value of the input parameter as a basic type.",
    )
    value_trigger_definition: Optional[TriggerDefinition] = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="The value of the input parameter as a basic type.",
    )
    value_usage_context: Optional[UsageContext] = Field(
        default=None,
        alias="valueUsageContext",
        description="The value of the input parameter as a basic type.",
    )
    value_dosage: Optional[Dosage] = Field(
        default=None,
        alias="valueDosage",
        description="The value of the input parameter as a basic type.",
    )
    value_meta: Optional[Meta] = Field(
        default=None,
        alias="valueMeta",
        description="The value of the input parameter as a basic type.",
    )


class TaskOutput(MedplumFHIRBase):
    """Outputs produced by the Task."""

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
    type: CodeableConcept = Field(
        default=..., description="The name of the Output parameter."
    )
    value_base64_binary: Optional[str] = Field(
        default=None,
        alias="valueBase64Binary",
        description="The value of the Output parameter as a basic type.",
    )
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="The value of the Output parameter as a basic type.",
    )
    value_canonical: Optional[str] = Field(
        default=None,
        alias="valueCanonical",
        description="The value of the Output parameter as a basic type.",
    )
    value_code: Optional[str] = Field(
        default=None,
        alias="valueCode",
        description="The value of the Output parameter as a basic type.",
    )
    value_date: Optional[str] = Field(
        default=None,
        alias="valueDate",
        description="The value of the Output parameter as a basic type.",
    )
    value_date_time: Optional[str] = Field(
        default=None,
        alias="valueDateTime",
        description="The value of the Output parameter as a basic type.",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="The value of the Output parameter as a basic type.",
    )
    value_id: Optional[str] = Field(
        default=None,
        alias="valueId",
        description="The value of the Output parameter as a basic type.",
    )
    value_instant: Optional[str] = Field(
        default=None,
        alias="valueInstant",
        description="The value of the Output parameter as a basic type.",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="The value of the Output parameter as a basic type.",
    )
    value_markdown: Optional[str] = Field(
        default=None,
        alias="valueMarkdown",
        description="The value of the Output parameter as a basic type.",
    )
    value_oid: Optional[str] = Field(
        default=None,
        alias="valueOid",
        description="The value of the Output parameter as a basic type.",
    )
    value_positive_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="valuePositiveInt",
        description="The value of the Output parameter as a basic type.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="The value of the Output parameter as a basic type.",
    )
    value_time: Optional[str] = Field(
        default=None,
        alias="valueTime",
        description="The value of the Output parameter as a basic type.",
    )
    value_unsigned_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueUnsignedInt",
        description="The value of the Output parameter as a basic type.",
    )
    value_uri: Optional[str] = Field(
        default=None,
        alias="valueUri",
        description="The value of the Output parameter as a basic type.",
    )
    value_url: Optional[str] = Field(
        default=None,
        alias="valueUrl",
        description="The value of the Output parameter as a basic type.",
    )
    value_uuid: Optional[str] = Field(
        default=None,
        alias="valueUuid",
        description="The value of the Output parameter as a basic type.",
    )
    value_address: Optional[Address] = Field(
        default=None,
        alias="valueAddress",
        description="The value of the Output parameter as a basic type.",
    )
    value_age: Optional[Age] = Field(
        default=None,
        alias="valueAge",
        description="The value of the Output parameter as a basic type.",
    )
    value_annotation: Optional[Annotation] = Field(
        default=None,
        alias="valueAnnotation",
        description="The value of the Output parameter as a basic type.",
    )
    value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="valueAttachment",
        description="The value of the Output parameter as a basic type.",
    )
    value_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="valueCodeableConcept",
        description="The value of the Output parameter as a basic type.",
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="The value of the Output parameter as a basic type.",
    )
    value_contact_point: Optional[ContactPoint] = Field(
        default=None,
        alias="valueContactPoint",
        description="The value of the Output parameter as a basic type.",
    )
    value_count: Optional[Count] = Field(
        default=None,
        alias="valueCount",
        description="The value of the Output parameter as a basic type.",
    )
    value_distance: Optional[Distance] = Field(
        default=None,
        alias="valueDistance",
        description="The value of the Output parameter as a basic type.",
    )
    value_duration: Optional[Duration] = Field(
        default=None,
        alias="valueDuration",
        description="The value of the Output parameter as a basic type.",
    )
    value_human_name: Optional[HumanName] = Field(
        default=None,
        alias="valueHumanName",
        description="The value of the Output parameter as a basic type.",
    )
    value_identifier: Optional[Identifier] = Field(
        default=None,
        alias="valueIdentifier",
        description="The value of the Output parameter as a basic type.",
    )
    value_money: Optional[Money] = Field(
        default=None,
        alias="valueMoney",
        description="The value of the Output parameter as a basic type.",
    )
    value_period: Optional[Period] = Field(
        default=None,
        alias="valuePeriod",
        description="The value of the Output parameter as a basic type.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="The value of the Output parameter as a basic type.",
    )
    value_range: Optional[Range] = Field(
        default=None,
        alias="valueRange",
        description="The value of the Output parameter as a basic type.",
    )
    value_ratio: Optional[Ratio] = Field(
        default=None,
        alias="valueRatio",
        description="The value of the Output parameter as a basic type.",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="The value of the Output parameter as a basic type.",
    )
    value_sampled_data: Optional[SampledData] = Field(
        default=None,
        alias="valueSampledData",
        description="The value of the Output parameter as a basic type.",
    )
    value_signature: Optional[Signature] = Field(
        default=None,
        alias="valueSignature",
        description="The value of the Output parameter as a basic type.",
    )
    value_timing: Optional[Timing] = Field(
        default=None,
        alias="valueTiming",
        description="The value of the Output parameter as a basic type.",
    )
    value_contact_detail: Optional[ContactDetail] = Field(
        default=None,
        alias="valueContactDetail",
        description="The value of the Output parameter as a basic type.",
    )
    value_contributor: Optional[Contributor] = Field(
        default=None,
        alias="valueContributor",
        description="The value of the Output parameter as a basic type.",
    )
    value_data_requirement: Optional[DataRequirement] = Field(
        default=None,
        alias="valueDataRequirement",
        description="The value of the Output parameter as a basic type.",
    )
    value_expression: Optional[Expression] = Field(
        default=None,
        alias="valueExpression",
        description="The value of the Output parameter as a basic type.",
    )
    value_parameter_definition: Optional[ParameterDefinition] = Field(
        default=None,
        alias="valueParameterDefinition",
        description="The value of the Output parameter as a basic type.",
    )
    value_related_artifact: Optional[RelatedArtifact] = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="The value of the Output parameter as a basic type.",
    )
    value_trigger_definition: Optional[TriggerDefinition] = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="The value of the Output parameter as a basic type.",
    )
    value_usage_context: Optional[UsageContext] = Field(
        default=None,
        alias="valueUsageContext",
        description="The value of the Output parameter as a basic type.",
    )
    value_dosage: Optional[Dosage] = Field(
        default=None,
        alias="valueDosage",
        description="The value of the Output parameter as a basic type.",
    )
    value_meta: Optional[Meta] = Field(
        default=None,
        alias="valueMeta",
        description="The value of the Output parameter as a basic type.",
    )


class TaskRestriction(MedplumFHIRBase):
    """If the Task.focus is a request resource and the task is seeking
    fulfillment (i.e. is asking for the request to be actioned), this
    element identifies any limitations on what parts of the referenced
    request should be actioned.
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
    repetitions: Optional[Union[int, float]] = Field(
        default=None,
        description="Indicates the number of times the requested action should occur.",
    )
    period: Optional[Period] = Field(
        default=None, description="Over what time-period is fulfillment sought."
    )
    recipient: Optional[list[Reference]] = Field(
        default=None,
        description="For requests that are targeted to more than on potential recipient/target, for whom is fulfillment sought?",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Task", Task)
    register_model("TaskInput", TaskInput)
    register_model("TaskOutput", TaskOutput)
    register_model("TaskRestriction", TaskRestriction)
