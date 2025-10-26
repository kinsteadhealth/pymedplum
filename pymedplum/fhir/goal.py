# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Goal(MedplumFHIRBase):
    """Describes the intended objective(s) for a patient, group or organization
    care, for example, weight loss, restoring an activity of daily living,
    obtaining herd immunity via immunization, meeting a process improvement
    objective, etc.
    """

    resource_type: Literal["Goal"] = Field(
        default="Goal",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[List[Identifier]] = Field(default=None, description="Business identifiers assigned to this goal by the performer or other systems which remain constant as the resource is updated and propagates from server to server.")
    lifecycle_status: Literal['proposed', 'planned', 'accepted', 'active', 'on-hold', 'completed', 'cancelled', 'entered-in-error', 'rejected'] = Field(default=..., alias="lifecycleStatus", description="The state of the goal throughout its lifecycle.")
    achievement_status: Optional[CodeableConcept] = Field(default=None, alias="achievementStatus", description="Describes the progression, or lack thereof, towards the goal against the target.")
    category: Optional[List[CodeableConcept]] = Field(default=None, description="Indicates a category the goal falls within.")
    priority: Optional[CodeableConcept] = Field(default=None, description="Identifies the mutually agreed level of importance associated with reaching/sustaining the goal.")
    description: CodeableConcept = Field(default=..., description="Human-readable and/or coded description of a specific desired objective of care, such as &quot;control blood pressure&quot; or &quot;negotiate an obstacle course&quot; or &quot;dance with child at wedding&quot;.")
    subject: Reference = Field(default=..., description="Identifies the patient, group or organization for whom the goal is being established.")
    start_date: Optional[str] = Field(default=None, alias="startDate", description="The date or event after which the goal should begin being pursued.")
    start_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="startCodeableConcept", description="The date or event after which the goal should begin being pursued.")
    target: Optional[List[GoalTarget]] = Field(default=None, description="Indicates what should be done by when.")
    status_date: Optional[str] = Field(default=None, alias="statusDate", description="Identifies when the current status. I.e. When initially created, when achieved, when cancelled, etc.")
    status_reason: Optional[str] = Field(default=None, alias="statusReason", description="Captures the reason for the current status.")
    expressed_by: Optional[Reference] = Field(default=None, alias="expressedBy", description="Indicates whose goal this is - patient goal, practitioner goal, etc.")
    addresses: Optional[List[Reference]] = Field(default=None, description="The identified conditions and other health record elements that are intended to be addressed by the goal.")
    note: Optional[List[Annotation]] = Field(default=None, description="Any comments related to the goal.")
    outcome_code: Optional[List[CodeableConcept]] = Field(default=None, alias="outcomeCode", description="Identifies the change (or lack of change) at the point when the status of the goal is assessed.")
    outcome_reference: Optional[List[Reference]] = Field(default=None, alias="outcomeReference", description="Details of what's changed (or not changed).")


class GoalTarget(MedplumFHIRBase):
    """Indicates what should be done by when."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    measure: Optional[CodeableConcept] = Field(default=None, description="The parameter whose value is being tracked, e.g. body weight, blood pressure, or hemoglobin A1c level.")
    detail_quantity: Optional[Quantity] = Field(default=None, alias="detailQuantity", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    detail_range: Optional[Range] = Field(default=None, alias="detailRange", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    detail_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="detailCodeableConcept", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    detail_string: Optional[str] = Field(default=None, alias="detailString", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    detail_boolean: Optional[bool] = Field(default=None, alias="detailBoolean", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    detail_integer: Optional[Union[int, float]] = Field(default=None, alias="detailInteger", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    detail_ratio: Optional[Ratio] = Field(default=None, alias="detailRatio", description="The target value of the focus to be achieved to signify the fulfillment of the goal, e.g. 150 pounds, 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any focus value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any focus value at or above the low value.")
    due_date: Optional[str] = Field(default=None, alias="dueDate", description="Indicates either the date or the duration after start by which the goal should be met.")
    due_duration: Optional[Duration] = Field(default=None, alias="dueDuration", description="Indicates either the date or the duration after start by which the goal should be met.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Goal", Goal)
    register_model("GoalTarget", GoalTarget)
