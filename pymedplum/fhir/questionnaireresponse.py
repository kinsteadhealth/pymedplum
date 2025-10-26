# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class QuestionnaireResponse(MedplumFHIRBase):
    """A structured set of questions and their answers. The questions are
    ordered and grouped into coherent subsets, corresponding to the
    structure of the grouping of the questionnaire being responded to.
    """

    resource_type: Literal["QuestionnaireResponse"] = Field(
        default="QuestionnaireResponse", alias="resourceType"
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
    identifier: Optional[Identifier] = Field(
        default=None,
        description="A business identifier assigned to a particular completed (or partially completed) questionnaire.",
    )
    based_on: Optional[list[Reference]] = Field(
        default=None,
        alias="basedOn",
        description="The order, proposal or plan that is fulfilled in whole or in part by this QuestionnaireResponse. For example, a ServiceRequest seeking an intake assessment or a decision support recommendation to assess for post-partum depression.",
    )
    part_of: Optional[list[Reference]] = Field(
        default=None,
        alias="partOf",
        description="A procedure or observation that this questionnaire was performed as part of the execution of. For example, the surgery a checklist was executed as part of.",
    )
    questionnaire: Optional[str] = Field(
        default=None,
        description="The Questionnaire that defines and organizes the questions for which answers are being provided.",
    )
    status: Literal[
        "in-progress", "completed", "amended", "entered-in-error", "stopped"
    ] = Field(
        default=...,
        description="The position of the questionnaire response within its overall lifecycle.",
    )
    subject: Optional[Reference] = Field(
        default=None,
        description="The subject of the questionnaire response. This could be a patient, organization, practitioner, device, etc. This is who/what the answers apply to, but is not necessarily the source of information.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The Encounter during which this questionnaire response was created or to which the creation of this record is tightly associated.",
    )
    authored: Optional[str] = Field(
        default=None,
        description="The date and/or time that this set of answers were last changed.",
    )
    author: Optional[Reference] = Field(
        default=None,
        description="Person who received the answers to the questions in the QuestionnaireResponse and recorded them in the system.",
    )
    source: Optional[Reference] = Field(
        default=None,
        description="The person who answered the questions about the subject.",
    )
    item: Optional[list[QuestionnaireResponseItem]] = Field(
        default=None,
        description="A group or question item from the original questionnaire for which answers are provided.",
    )


class QuestionnaireResponseItem(MedplumFHIRBase):
    """A group or question item from the original questionnaire for which
    answers are provided.
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
    link_id: str = Field(
        default=...,
        alias="linkId",
        description="The item from the Questionnaire that corresponds to this item in the QuestionnaireResponse resource.",
    )
    definition: Optional[str] = Field(
        default=None,
        description="A reference to an [ElementDefinition](elementdefinition.html) that provides the details for the item.",
    )
    text: Optional[str] = Field(
        default=None,
        description="Text that is displayed above the contents of the group or as the text of the question being answered.",
    )
    answer: Optional[list[QuestionnaireResponseItemAnswer]] = Field(
        default=None, description="The respondent's answer(s) to the question."
    )
    item: Optional[list[QuestionnaireResponseItem]] = Field(
        default=None,
        description="Questions or sub-groups nested beneath a question or group.",
    )


class QuestionnaireResponseItemAnswer(MedplumFHIRBase):
    """The respondent's answer(s) to the question."""

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
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_date: Optional[str] = Field(
        default=None,
        alias="valueDate",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_date_time: Optional[str] = Field(
        default=None,
        alias="valueDateTime",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_time: Optional[str] = Field(
        default=None,
        alias="valueTime",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_uri: Optional[str] = Field(
        default=None,
        alias="valueUri",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="valueAttachment",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="The answer (or one of the answers) provided by the respondent to the question.",
    )
    item: Optional[list[QuestionnaireResponseItem]] = Field(
        default=None,
        description="Nested groups and/or questions found within this particular answer.",
    )
