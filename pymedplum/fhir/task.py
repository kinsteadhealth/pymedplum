# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.age import Age
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.contributor import Contributor
    from pymedplum.fhir.count import Count
    from pymedplum.fhir.datarequirement import DataRequirement
    from pymedplum.fhir.distance import Distance
    from pymedplum.fhir.dosage import Dosage
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.parameterdefinition import ParameterDefinition
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.sampleddata import SampledData
    from pymedplum.fhir.signature import Signature
    from pymedplum.fhir.timing import Timing
    from pymedplum.fhir.triggerdefinition import TriggerDefinition
    from pymedplum.fhir.usagecontext import UsageContext


class Task(MedplumFHIRBase):
    """A task to be performed."""

    resource_type: Literal["Task"] = Field(default="Task", alias="resourceType")

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
    identifier: list[Identifier] | None = Field(
        default=None, description="The business identifier for this task."
    )
    instantiates_canonical: str | None = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a *FHIR*-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this Task.",
    )
    instantiates_uri: str | None = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an *externally* maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this Task.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="BasedOn refers to a higher-level authorization that triggered the creation of the task. It references a &quot;request&quot; resource such as a ServiceRequest, MedicationRequest, ServiceRequest, CarePlan, etc. which is distinct from the &quot;request&quot; resource the task is seeking to fulfill. This latter resource is referenced by FocusOn. For example, based on a ServiceRequest (= BasedOn), a task is created to fulfill a procedureRequest ( = FocusOn ) to collect a specimen from a patient.",
    )
    group_identifier: Identifier | None = Field(
        default=None,
        alias="groupIdentifier",
        description="An identifier that links together multiple tasks and other requests that were created in the same context.",
    )
    part_of: list[Reference] | None = Field(
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
    status_reason: CodeableConcept | None = Field(
        default=None,
        alias="statusReason",
        description="An explanation as to why this task is held, failed, was refused, etc.",
    )
    business_status: CodeableConcept | None = Field(
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
    priority: Literal["routine", "urgent", "asap", "stat"] | None = Field(
        default=None,
        description="Indicates how quickly the Task should be addressed with respect to other requests.",
    )
    code: CodeableConcept | None = Field(
        default=None,
        description="A name or code (or both) briefly describing what the task involves.",
    )
    description: str | None = Field(
        default=None, description="A free-text description of what is to be performed."
    )
    focus: Reference | None = Field(
        default=None,
        description="The request being actioned or the resource being manipulated by this task.",
    )
    for_: Reference | None = Field(
        default=None,
        alias="for",
        description="The entity who benefits from the performance of the service specified in the task (e.g., the patient).",
    )
    encounter: Reference | None = Field(
        default=None,
        description="The healthcare event (e.g. a patient and healthcare provider interaction) during which this task was created.",
    )
    execution_period: Period | None = Field(
        default=None,
        alias="executionPeriod",
        description="Identifies the time action was first taken against the task (start) and/or the time final action was taken against the task prior to marking it as completed (end).",
    )
    authored_on: str | None = Field(
        default=None,
        alias="authoredOn",
        description="The date and time this task was created.",
    )
    last_modified: str | None = Field(
        default=None,
        alias="lastModified",
        description="The date and time of last modification to this task.",
    )
    requester: Reference | None = Field(
        default=None, description="The creator of the task."
    )
    performer_type: list[CodeableConcept] | None = Field(
        default=None,
        alias="performerType",
        description="The kind of participant that should perform the task.",
    )
    owner: Reference | None = Field(
        default=None,
        description="Individual organization or Device currently responsible for task execution.",
    )
    location: Reference | None = Field(
        default=None,
        description="Principal physical location where the this task is performed.",
    )
    reason_code: CodeableConcept | None = Field(
        default=None,
        alias="reasonCode",
        description="A description or code indicating why this task needs to be performed.",
    )
    reason_reference: Reference | None = Field(
        default=None,
        alias="reasonReference",
        description="A resource reference indicating why this task needs to be performed.",
    )
    insurance: list[Reference] | None = Field(
        default=None,
        description="Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be relevant to the Task.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Free-text information captured about the task as it progresses.",
    )
    relevant_history: list[Reference] | None = Field(
        default=None,
        alias="relevantHistory",
        description="Links to Provenance records for past versions of this Task that identify key state transitions or updates that are likely to be relevant to a user looking at the current version of the task.",
    )
    restriction: TaskRestriction | None = Field(
        default=None,
        description="If the Task.focus is a request resource and the task is seeking fulfillment (i.e. is asking for the request to be actioned), this element identifies any limitations on what parts of the referenced request should be actioned.",
    )
    input: list[TaskInput] | None = Field(
        default=None,
        description="Additional information that may be needed in the execution of the task.",
    )
    output: list[TaskOutput] | None = Field(
        default=None, description="Outputs produced by the Task."
    )


class TaskInput(MedplumFHIRBase):
    """Additional information that may be needed in the execution of the task."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=...,
        description="A code or description indicating how the input is intended to be used as part of the task execution.",
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="The value of the input parameter as a basic type.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="The value of the input parameter as a basic type.",
    )
    value_canonical: str | None = Field(
        default=None,
        alias="valueCanonical",
        description="The value of the input parameter as a basic type.",
    )
    value_code: str | None = Field(
        default=None,
        alias="valueCode",
        description="The value of the input parameter as a basic type.",
    )
    value_date: str | None = Field(
        default=None,
        alias="valueDate",
        description="The value of the input parameter as a basic type.",
    )
    value_date_time: str | None = Field(
        default=None,
        alias="valueDateTime",
        description="The value of the input parameter as a basic type.",
    )
    value_decimal: float | None = Field(
        default=None,
        alias="valueDecimal",
        description="The value of the input parameter as a basic type.",
    )
    value_id: str | None = Field(
        default=None,
        alias="valueId",
        description="The value of the input parameter as a basic type.",
    )
    value_instant: str | None = Field(
        default=None,
        alias="valueInstant",
        description="The value of the input parameter as a basic type.",
    )
    value_integer: int | None = Field(
        default=None,
        alias="valueInteger",
        description="The value of the input parameter as a basic type.",
    )
    value_markdown: str | None = Field(
        default=None,
        alias="valueMarkdown",
        description="The value of the input parameter as a basic type.",
    )
    value_oid: str | None = Field(
        default=None,
        alias="valueOid",
        description="The value of the input parameter as a basic type.",
    )
    value_positive_int: int | None = Field(
        default=None,
        alias="valuePositiveInt",
        description="The value of the input parameter as a basic type.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="The value of the input parameter as a basic type.",
    )
    value_time: str | None = Field(
        default=None,
        alias="valueTime",
        description="The value of the input parameter as a basic type.",
    )
    value_unsigned_int: int | None = Field(
        default=None,
        alias="valueUnsignedInt",
        description="The value of the input parameter as a basic type.",
    )
    value_uri: str | None = Field(
        default=None,
        alias="valueUri",
        description="The value of the input parameter as a basic type.",
    )
    value_url: str | None = Field(
        default=None,
        alias="valueUrl",
        description="The value of the input parameter as a basic type.",
    )
    value_uuid: str | None = Field(
        default=None,
        alias="valueUuid",
        description="The value of the input parameter as a basic type.",
    )
    value_address: Address | None = Field(
        default=None,
        alias="valueAddress",
        description="The value of the input parameter as a basic type.",
    )
    value_age: Age | None = Field(
        default=None,
        alias="valueAge",
        description="The value of the input parameter as a basic type.",
    )
    value_annotation: Annotation | None = Field(
        default=None,
        alias="valueAnnotation",
        description="The value of the input parameter as a basic type.",
    )
    value_attachment: Attachment | None = Field(
        default=None,
        alias="valueAttachment",
        description="The value of the input parameter as a basic type.",
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="The value of the input parameter as a basic type.",
    )
    value_coding: Coding | None = Field(
        default=None,
        alias="valueCoding",
        description="The value of the input parameter as a basic type.",
    )
    value_contact_point: ContactPoint | None = Field(
        default=None,
        alias="valueContactPoint",
        description="The value of the input parameter as a basic type.",
    )
    value_count: Count | None = Field(
        default=None,
        alias="valueCount",
        description="The value of the input parameter as a basic type.",
    )
    value_distance: Distance | None = Field(
        default=None,
        alias="valueDistance",
        description="The value of the input parameter as a basic type.",
    )
    value_duration: Duration | None = Field(
        default=None,
        alias="valueDuration",
        description="The value of the input parameter as a basic type.",
    )
    value_human_name: HumanName | None = Field(
        default=None,
        alias="valueHumanName",
        description="The value of the input parameter as a basic type.",
    )
    value_identifier: Identifier | None = Field(
        default=None,
        alias="valueIdentifier",
        description="The value of the input parameter as a basic type.",
    )
    value_money: Money | None = Field(
        default=None,
        alias="valueMoney",
        description="The value of the input parameter as a basic type.",
    )
    value_period: Period | None = Field(
        default=None,
        alias="valuePeriod",
        description="The value of the input parameter as a basic type.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="The value of the input parameter as a basic type.",
    )
    value_range: Range | None = Field(
        default=None,
        alias="valueRange",
        description="The value of the input parameter as a basic type.",
    )
    value_ratio: Ratio | None = Field(
        default=None,
        alias="valueRatio",
        description="The value of the input parameter as a basic type.",
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="The value of the input parameter as a basic type.",
    )
    value_sampled_data: SampledData | None = Field(
        default=None,
        alias="valueSampledData",
        description="The value of the input parameter as a basic type.",
    )
    value_signature: Signature | None = Field(
        default=None,
        alias="valueSignature",
        description="The value of the input parameter as a basic type.",
    )
    value_timing: Timing | None = Field(
        default=None,
        alias="valueTiming",
        description="The value of the input parameter as a basic type.",
    )
    value_contact_detail: ContactDetail | None = Field(
        default=None,
        alias="valueContactDetail",
        description="The value of the input parameter as a basic type.",
    )
    value_contributor: Contributor | None = Field(
        default=None,
        alias="valueContributor",
        description="The value of the input parameter as a basic type.",
    )
    value_data_requirement: DataRequirement | None = Field(
        default=None,
        alias="valueDataRequirement",
        description="The value of the input parameter as a basic type.",
    )
    value_expression: Expression | None = Field(
        default=None,
        alias="valueExpression",
        description="The value of the input parameter as a basic type.",
    )
    value_parameter_definition: ParameterDefinition | None = Field(
        default=None,
        alias="valueParameterDefinition",
        description="The value of the input parameter as a basic type.",
    )
    value_related_artifact: RelatedArtifact | None = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="The value of the input parameter as a basic type.",
    )
    value_trigger_definition: TriggerDefinition | None = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="The value of the input parameter as a basic type.",
    )
    value_usage_context: UsageContext | None = Field(
        default=None,
        alias="valueUsageContext",
        description="The value of the input parameter as a basic type.",
    )
    value_dosage: Dosage | None = Field(
        default=None,
        alias="valueDosage",
        description="The value of the input parameter as a basic type.",
    )
    value_meta: Meta | None = Field(
        default=None,
        alias="valueMeta",
        description="The value of the input parameter as a basic type.",
    )


class TaskOutput(MedplumFHIRBase):
    """Outputs produced by the Task."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=..., description="The name of the Output parameter."
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="The value of the Output parameter as a basic type.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="The value of the Output parameter as a basic type.",
    )
    value_canonical: str | None = Field(
        default=None,
        alias="valueCanonical",
        description="The value of the Output parameter as a basic type.",
    )
    value_code: str | None = Field(
        default=None,
        alias="valueCode",
        description="The value of the Output parameter as a basic type.",
    )
    value_date: str | None = Field(
        default=None,
        alias="valueDate",
        description="The value of the Output parameter as a basic type.",
    )
    value_date_time: str | None = Field(
        default=None,
        alias="valueDateTime",
        description="The value of the Output parameter as a basic type.",
    )
    value_decimal: float | None = Field(
        default=None,
        alias="valueDecimal",
        description="The value of the Output parameter as a basic type.",
    )
    value_id: str | None = Field(
        default=None,
        alias="valueId",
        description="The value of the Output parameter as a basic type.",
    )
    value_instant: str | None = Field(
        default=None,
        alias="valueInstant",
        description="The value of the Output parameter as a basic type.",
    )
    value_integer: int | None = Field(
        default=None,
        alias="valueInteger",
        description="The value of the Output parameter as a basic type.",
    )
    value_markdown: str | None = Field(
        default=None,
        alias="valueMarkdown",
        description="The value of the Output parameter as a basic type.",
    )
    value_oid: str | None = Field(
        default=None,
        alias="valueOid",
        description="The value of the Output parameter as a basic type.",
    )
    value_positive_int: int | None = Field(
        default=None,
        alias="valuePositiveInt",
        description="The value of the Output parameter as a basic type.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="The value of the Output parameter as a basic type.",
    )
    value_time: str | None = Field(
        default=None,
        alias="valueTime",
        description="The value of the Output parameter as a basic type.",
    )
    value_unsigned_int: int | None = Field(
        default=None,
        alias="valueUnsignedInt",
        description="The value of the Output parameter as a basic type.",
    )
    value_uri: str | None = Field(
        default=None,
        alias="valueUri",
        description="The value of the Output parameter as a basic type.",
    )
    value_url: str | None = Field(
        default=None,
        alias="valueUrl",
        description="The value of the Output parameter as a basic type.",
    )
    value_uuid: str | None = Field(
        default=None,
        alias="valueUuid",
        description="The value of the Output parameter as a basic type.",
    )
    value_address: Address | None = Field(
        default=None,
        alias="valueAddress",
        description="The value of the Output parameter as a basic type.",
    )
    value_age: Age | None = Field(
        default=None,
        alias="valueAge",
        description="The value of the Output parameter as a basic type.",
    )
    value_annotation: Annotation | None = Field(
        default=None,
        alias="valueAnnotation",
        description="The value of the Output parameter as a basic type.",
    )
    value_attachment: Attachment | None = Field(
        default=None,
        alias="valueAttachment",
        description="The value of the Output parameter as a basic type.",
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="The value of the Output parameter as a basic type.",
    )
    value_coding: Coding | None = Field(
        default=None,
        alias="valueCoding",
        description="The value of the Output parameter as a basic type.",
    )
    value_contact_point: ContactPoint | None = Field(
        default=None,
        alias="valueContactPoint",
        description="The value of the Output parameter as a basic type.",
    )
    value_count: Count | None = Field(
        default=None,
        alias="valueCount",
        description="The value of the Output parameter as a basic type.",
    )
    value_distance: Distance | None = Field(
        default=None,
        alias="valueDistance",
        description="The value of the Output parameter as a basic type.",
    )
    value_duration: Duration | None = Field(
        default=None,
        alias="valueDuration",
        description="The value of the Output parameter as a basic type.",
    )
    value_human_name: HumanName | None = Field(
        default=None,
        alias="valueHumanName",
        description="The value of the Output parameter as a basic type.",
    )
    value_identifier: Identifier | None = Field(
        default=None,
        alias="valueIdentifier",
        description="The value of the Output parameter as a basic type.",
    )
    value_money: Money | None = Field(
        default=None,
        alias="valueMoney",
        description="The value of the Output parameter as a basic type.",
    )
    value_period: Period | None = Field(
        default=None,
        alias="valuePeriod",
        description="The value of the Output parameter as a basic type.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="The value of the Output parameter as a basic type.",
    )
    value_range: Range | None = Field(
        default=None,
        alias="valueRange",
        description="The value of the Output parameter as a basic type.",
    )
    value_ratio: Ratio | None = Field(
        default=None,
        alias="valueRatio",
        description="The value of the Output parameter as a basic type.",
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="The value of the Output parameter as a basic type.",
    )
    value_sampled_data: SampledData | None = Field(
        default=None,
        alias="valueSampledData",
        description="The value of the Output parameter as a basic type.",
    )
    value_signature: Signature | None = Field(
        default=None,
        alias="valueSignature",
        description="The value of the Output parameter as a basic type.",
    )
    value_timing: Timing | None = Field(
        default=None,
        alias="valueTiming",
        description="The value of the Output parameter as a basic type.",
    )
    value_contact_detail: ContactDetail | None = Field(
        default=None,
        alias="valueContactDetail",
        description="The value of the Output parameter as a basic type.",
    )
    value_contributor: Contributor | None = Field(
        default=None,
        alias="valueContributor",
        description="The value of the Output parameter as a basic type.",
    )
    value_data_requirement: DataRequirement | None = Field(
        default=None,
        alias="valueDataRequirement",
        description="The value of the Output parameter as a basic type.",
    )
    value_expression: Expression | None = Field(
        default=None,
        alias="valueExpression",
        description="The value of the Output parameter as a basic type.",
    )
    value_parameter_definition: ParameterDefinition | None = Field(
        default=None,
        alias="valueParameterDefinition",
        description="The value of the Output parameter as a basic type.",
    )
    value_related_artifact: RelatedArtifact | None = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="The value of the Output parameter as a basic type.",
    )
    value_trigger_definition: TriggerDefinition | None = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="The value of the Output parameter as a basic type.",
    )
    value_usage_context: UsageContext | None = Field(
        default=None,
        alias="valueUsageContext",
        description="The value of the Output parameter as a basic type.",
    )
    value_dosage: Dosage | None = Field(
        default=None,
        alias="valueDosage",
        description="The value of the Output parameter as a basic type.",
    )
    value_meta: Meta | None = Field(
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

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    repetitions: int | float | None = Field(
        default=None,
        description="Indicates the number of times the requested action should occur.",
    )
    period: Period | None = Field(
        default=None, description="Over what time-period is fulfillment sought."
    )
    recipient: list[Reference] | None = Field(
        default=None,
        description="For requests that are targeted to more than on potential recipient/target, for whom is fulfillment sought?",
    )
