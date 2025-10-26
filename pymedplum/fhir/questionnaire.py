# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Questionnaire(MedplumFHIRBase):
    """A structured set of questions intended to guide the collection of
    answers from end-users. Questionnaires provide detailed control over
    order, presentation, phraseology and grouping to allow coherent,
    consistent data collection.
    """

    resource_type: Literal["Questionnaire"] = Field(
        default="Questionnaire", alias="resourceType"
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
    url: Optional[str] = Field(
        default=None,
        description="An absolute URI that is used to identify this questionnaire when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this questionnaire is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the questionnaire is stored on different servers.",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="A formal identifier that is used to identify this questionnaire when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the questionnaire when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the questionnaire author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A natural language name identifying the questionnaire. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the questionnaire.",
    )
    derived_from: Optional[list[str]] = Field(
        default=None,
        alias="derivedFrom",
        description="The URL of a Questionnaire that this Questionnaire is based on.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this questionnaire. Enables tracking the life-cycle of the content.",
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this questionnaire is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    subject_type: Optional[list[ResourceType]] = Field(
        default=None,
        alias="subjectType",
        description="The types of subjects that can be the subject of responses created for the questionnaire.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the questionnaire was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the questionnaire changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the questionnaire.",
    )
    contact: Optional[list[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the questionnaire from a consumer's perspective.",
    )
    use_context: Optional[list[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate questionnaire instances.",
    )
    jurisdiction: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the questionnaire is intended to be used.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Explanation of why this questionnaire is needed and why it has been designed as it has.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the questionnaire and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the questionnaire.",
    )
    approval_date: Optional[str] = Field(
        default=None,
        alias="approvalDate",
        description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.",
    )
    last_review_date: Optional[str] = Field(
        default=None,
        alias="lastReviewDate",
        description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.",
    )
    effective_period: Optional[Period] = Field(
        default=None,
        alias="effectivePeriod",
        description="The period during which the questionnaire content was or is planned to be in active use.",
    )
    code: Optional[list[Coding]] = Field(
        default=None,
        description="An identifier for this question or group of questions in a particular terminology such as LOINC.",
    )
    item: Optional[list[QuestionnaireItem]] = Field(
        default=None,
        description="A particular question, question grouping or display text that is part of the questionnaire.",
    )


class QuestionnaireItem(MedplumFHIRBase):
    """A particular question, question grouping or display text that is part of
    the questionnaire.
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
        description="An identifier that is unique within the Questionnaire allowing linkage to the equivalent item in a QuestionnaireResponse resource.",
    )
    definition: Optional[str] = Field(
        default=None,
        description="This element is a URI that refers to an [ElementDefinition](elementdefinition.html) that provides information about this item, including information that might otherwise be included in the instance of the Questionnaire resource. A detailed description of the construction of the URI is shown in Comments, below. If this element is present then the following element values MAY be derived from the Element Definition if the corresponding elements of this Questionnaire resource instance have no value: * code (ElementDefinition.code) * type (ElementDefinition.type) * required (ElementDefinition.min) * repeats (ElementDefinition.max) * maxLength (ElementDefinition.maxLength) * answerValueSet (ElementDefinition.binding) * options (ElementDefinition.binding).",
    )
    code: Optional[list[Coding]] = Field(
        default=None,
        description="A terminology code that corresponds to this group or question (e.g. a code from LOINC, which defines many questions and answers).",
    )
    prefix: Optional[str] = Field(
        default=None,
        description="A short label for a particular group, question or set of display text within the questionnaire used for reference by the individual completing the questionnaire.",
    )
    text: Optional[str] = Field(
        default=None,
        description="The name of a section, the text of a question or text content for a display item.",
    )
    type: Literal[
        "group",
        "display",
        "question",
        "boolean",
        "decimal",
        "integer",
        "date",
        "dateTime",
        "time",
        "string",
        "text",
        "url",
        "choice",
        "open-choice",
        "attachment",
        "reference",
        "quantity",
    ] = Field(
        default=...,
        description="The type of questionnaire item this is - whether text for display, a grouping of other items or a particular type of data to be captured (string, integer, coded choice, etc.).",
    )
    enable_when: Optional[list[QuestionnaireItemEnableWhen]] = Field(
        default=None,
        alias="enableWhen",
        description="A constraint indicating that this item should only be enabled (displayed/allow answers to be captured) when the specified condition is true.",
    )
    enable_behavior: Optional[Literal["all", "any"]] = Field(
        default=None,
        alias="enableBehavior",
        description="Controls how multiple enableWhen values are interpreted - whether all or any must be true.",
    )
    required: Optional[bool] = Field(
        default=None,
        description="An indication, if true, that the item must be present in a &quot;completed&quot; QuestionnaireResponse. If false, the item may be skipped when answering the questionnaire.",
    )
    repeats: Optional[bool] = Field(
        default=None,
        description="An indication, if true, that the item may occur multiple times in the response, collecting multiple answers for questions or multiple sets of answers for groups.",
    )
    read_only: Optional[bool] = Field(
        default=None,
        alias="readOnly",
        description="An indication, when true, that the value cannot be changed by a human respondent to the Questionnaire.",
    )
    max_length: Optional[Union[int, float]] = Field(
        default=None,
        alias="maxLength",
        description="The maximum number of characters that are permitted in the answer to be considered a &quot;valid&quot; QuestionnaireResponse.",
    )
    answer_value_set: Optional[str] = Field(
        default=None,
        alias="answerValueSet",
        description="A reference to a value set containing a list of codes representing permitted answers for a &quot;choice&quot; or &quot;open-choice&quot; question.",
    )
    answer_option: Optional[list[QuestionnaireItemAnswerOption]] = Field(
        default=None,
        alias="answerOption",
        description="One of the permitted answers for a &quot;choice&quot; or &quot;open-choice&quot; question.",
    )
    initial: Optional[list[QuestionnaireItemInitial]] = Field(
        default=None,
        description="One or more values that should be pre-populated in the answer when initially rendering the questionnaire for user input.",
    )
    item: Optional[list[QuestionnaireItem]] = Field(
        default=None,
        description="Text, questions and other groups to be nested beneath a question or group.",
    )


class QuestionnaireItemAnswerOption(MedplumFHIRBase):
    """One of the permitted answers for a &quot;choice&quot; or
    &quot;open-choice&quot; question.
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
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="A potential answer that's allowed as the answer to this question.",
    )
    value_date: Optional[str] = Field(
        default=None,
        alias="valueDate",
        description="A potential answer that's allowed as the answer to this question.",
    )
    value_time: Optional[str] = Field(
        default=None,
        alias="valueTime",
        description="A potential answer that's allowed as the answer to this question.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="A potential answer that's allowed as the answer to this question.",
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="A potential answer that's allowed as the answer to this question.",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="A potential answer that's allowed as the answer to this question.",
    )
    initial_selected: Optional[bool] = Field(
        default=None,
        alias="initialSelected",
        description="Indicates whether the answer value is selected when the list of possible answers is initially shown.",
    )


class QuestionnaireItemEnableWhen(MedplumFHIRBase):
    """A constraint indicating that this item should only be enabled
    (displayed/allow answers to be captured) when the specified condition is
    true.
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
    question: str = Field(
        default=...,
        description="The linkId for the question whose answer (or lack of answer) governs whether this item is enabled.",
    )
    operator: Literal["exists", "=", "!=", ">", "<", ">=", "<="] = Field(
        default=...,
        description="Specifies the criteria by which the question is enabled.",
    )
    answer_boolean: Optional[bool] = Field(
        default=None,
        alias="answerBoolean",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="answerDecimal",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="answerInteger",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_date: Optional[str] = Field(
        default=None,
        alias="answerDate",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_date_time: Optional[str] = Field(
        default=None,
        alias="answerDateTime",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_time: Optional[str] = Field(
        default=None,
        alias="answerTime",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_string: Optional[str] = Field(
        default=None,
        alias="answerString",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_coding: Optional[Coding] = Field(
        default=None,
        alias="answerCoding",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_quantity: Optional[Quantity] = Field(
        default=None,
        alias="answerQuantity",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )
    answer_reference: Optional[Reference] = Field(
        default=None,
        alias="answerReference",
        description="A value that the referenced question is tested using the specified operator in order for the item to be enabled.",
    )


class QuestionnaireItemInitial(MedplumFHIRBase):
    """One or more values that should be pre-populated in the answer when
    initially rendering the questionnaire for user input.
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
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="The actual value to for an initial answer.",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="The actual value to for an initial answer.",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="The actual value to for an initial answer.",
    )
    value_date: Optional[str] = Field(
        default=None,
        alias="valueDate",
        description="The actual value to for an initial answer.",
    )
    value_date_time: Optional[str] = Field(
        default=None,
        alias="valueDateTime",
        description="The actual value to for an initial answer.",
    )
    value_time: Optional[str] = Field(
        default=None,
        alias="valueTime",
        description="The actual value to for an initial answer.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="The actual value to for an initial answer.",
    )
    value_uri: Optional[str] = Field(
        default=None,
        alias="valueUri",
        description="The actual value to for an initial answer.",
    )
    value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="valueAttachment",
        description="The actual value to for an initial answer.",
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="The actual value to for an initial answer.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="The actual value to for an initial answer.",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="The actual value to for an initial answer.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Questionnaire", Questionnaire)
    register_model("QuestionnaireItem", QuestionnaireItem)
    register_model("QuestionnaireItemAnswerOption", QuestionnaireItemAnswerOption)
    register_model("QuestionnaireItemEnableWhen", QuestionnaireItemEnableWhen)
    register_model("QuestionnaireItemInitial", QuestionnaireItemInitial)
