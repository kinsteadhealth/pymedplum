# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class PlanDefinition(MedplumFHIRBase):
    """This resource allows for the definition of various types of plans as a
    sharable, consumable, and executable artifact. The resource is general
    enough to support the description of a broad range of clinical artifacts
    such as clinical decision support rules, order sets and protocols.
    """

    resource_type: Literal["PlanDefinition"] = Field(
        default="PlanDefinition", alias="resourceType"
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
        description="An absolute URI that is used to identify this plan definition when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this plan definition is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the plan definition is stored on different servers.",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="A formal identifier that is used to identify this plan definition when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the plan definition when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the plan definition author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. To provide a version consistent with the Decision Support Service specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more information on versioning knowledge assets, refer to the Decision Support Service specification. Note that a version is required for non-experimental active artifacts.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A natural language name identifying the plan definition. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the plan definition.",
    )
    subtitle: Optional[str] = Field(
        default=None,
        description="An explanatory or alternate title for the plan definition giving additional information about its content.",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="A high-level category for the plan definition that distinguishes the kinds of systems that would be interested in the plan definition.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this plan definition. Enables tracking the life-cycle of the content.",
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this plan definition is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    subject_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="subjectCodeableConcept",
        description="A code or group definition that describes the intended subject of the plan definition.",
    )
    subject_reference: Optional[Reference] = Field(
        default=None,
        alias="subjectReference",
        description="A code or group definition that describes the intended subject of the plan definition.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the plan definition was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the plan definition changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the plan definition.",
    )
    contact: Optional[list[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the plan definition from a consumer's perspective.",
    )
    use_context: Optional[list[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate plan definition instances.",
    )
    jurisdiction: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the plan definition is intended to be used.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Explanation of why this plan definition is needed and why it has been designed as it has.",
    )
    usage: Optional[str] = Field(
        default=None,
        description="A detailed description of how the plan definition is used from a clinical perspective.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the plan definition and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the plan definition.",
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
        description="The period during which the plan definition content was or is planned to be in active use.",
    )
    topic: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Descriptive topics related to the content of the plan definition. Topics provide a high-level categorization of the definition that can be useful for filtering and searching.",
    )
    author: Optional[list[ContactDetail]] = Field(
        default=None,
        description="An individiual or organization primarily involved in the creation and maintenance of the content.",
    )
    editor: Optional[list[ContactDetail]] = Field(
        default=None,
        description="An individual or organization primarily responsible for internal coherence of the content.",
    )
    reviewer: Optional[list[ContactDetail]] = Field(
        default=None,
        description="An individual or organization primarily responsible for review of some aspect of the content.",
    )
    endorser: Optional[list[ContactDetail]] = Field(
        default=None,
        description="An individual or organization responsible for officially endorsing the content for use in some setting.",
    )
    related_artifact: Optional[list[RelatedArtifact]] = Field(
        default=None,
        alias="relatedArtifact",
        description="Related artifacts such as additional documentation, justification, or bibliographic references.",
    )
    library: Optional[list[str]] = Field(
        default=None,
        description="A reference to a Library resource containing any formal logic used by the plan definition.",
    )
    goal: Optional[list[PlanDefinitionGoal]] = Field(
        default=None,
        description="Goals that describe what the activities within the plan are intended to achieve. For example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, etc.",
    )
    action: Optional[list[PlanDefinitionAction]] = Field(
        default=None,
        description="An action or group of actions to be taken as part of the plan.",
    )


class PlanDefinitionAction(MedplumFHIRBase):
    """An action or group of actions to be taken as part of the plan."""

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
        description="A brief description of the action used to provide a summary to display to the user.",
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
        description="A code that provides meaning for the action or action group. For example, a section may have a LOINC code for the section of a documentation template.",
    )
    reason: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A description of why this action is necessary or appropriate.",
    )
    documentation: Optional[list[RelatedArtifact]] = Field(
        default=None,
        description="Didactic or other informational resources associated with the action that can be provided to the CDS recipient. Information resources can include inline text commentary and links to web resources.",
    )
    goal_id: Optional[list[str]] = Field(
        default=None,
        alias="goalId",
        description="Identifies goals that this action supports. The reference must be to a goal element defined within this plan definition.",
    )
    subject_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="subjectCodeableConcept",
        description="A code or group definition that describes the intended subject of the action and its children, if any.",
    )
    subject_reference: Optional[Reference] = Field(
        default=None,
        alias="subjectReference",
        description="A code or group definition that describes the intended subject of the action and its children, if any.",
    )
    trigger: Optional[list[TriggerDefinition]] = Field(
        default=None,
        description="A description of when the action should be triggered.",
    )
    condition: Optional[list[PlanDefinitionActionCondition]] = Field(
        default=None,
        description="An expression that describes applicability criteria or start/stop conditions for the action.",
    )
    input: Optional[list[DataRequirement]] = Field(
        default=None, description="Defines input data requirements for the action."
    )
    output: Optional[list[DataRequirement]] = Field(
        default=None, description="Defines the outputs of the action, if any."
    )
    related_action: Optional[list[PlanDefinitionActionRelatedAction]] = Field(
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
    participant: Optional[list[PlanDefinitionActionParticipant]] = Field(
        default=None,
        description="Indicates who should participate in performing the action described.",
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
            description="Defines the required behavior for the action.",
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
    definition_canonical: Optional[str] = Field(
        default=None,
        alias="definitionCanonical",
        description="A reference to an ActivityDefinition that describes the action to be taken in detail, or a PlanDefinition that describes a series of actions to be taken.",
    )
    definition_uri: Optional[str] = Field(
        default=None,
        alias="definitionUri",
        description="A reference to an ActivityDefinition that describes the action to be taken in detail, or a PlanDefinition that describes a series of actions to be taken.",
    )
    transform: Optional[str] = Field(
        default=None,
        description="A reference to a StructureMap resource that defines a transform that can be executed to produce the intent resource using the ActivityDefinition instance as the input.",
    )
    dynamic_value: Optional[list[PlanDefinitionActionDynamicValue]] = Field(
        default=None,
        alias="dynamicValue",
        description="Customizations that should be applied to the statically defined resource. For example, if the dosage of a medication must be computed based on the patient's weight, a customization would be used to specify an expression that calculated the weight, and the path on the resource that would contain the result.",
    )
    action: Optional[list[PlanDefinitionAction]] = Field(
        default=None,
        description="Sub actions that are contained within the action. The behavior of this action determines the functionality of the sub-actions. For example, a selection behavior of at-most-one indicates that of the sub-actions, at most one may be chosen as part of realizing the action definition.",
    )


class PlanDefinitionActionCondition(MedplumFHIRBase):
    """An expression that describes applicability criteria or start/stop
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
        description="An expression that returns true or false, indicating whether the condition is satisfied.",
    )


class PlanDefinitionActionDynamicValue(MedplumFHIRBase):
    """Customizations that should be applied to the statically defined
    resource. For example, if the dosage of a medication must be computed
    based on the patient's weight, a customization would be used to specify
    an expression that calculated the weight, and the path on the resource
    that would contain the result.
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
    path: Optional[str] = Field(
        default=None,
        description="The path to the element to be customized. This is the path on the resource that will hold the result of the calculation defined by the expression. The specified path SHALL be a FHIRPath resolveable on the specified target type of the ActivityDefinition, and SHALL consist only of identifiers, constant indexers, and a restricted subset of functions. The path is allowed to contain qualifiers (.) to traverse sub-elements, as well as indexers ([x]) to traverse multiple-cardinality sub-elements (see the [Simple FHIRPath Profile](fhirpath.html#simple) for full details).",
    )
    expression: Optional[Expression] = Field(
        default=None,
        description="An expression specifying the value of the customized element.",
    )


class PlanDefinitionActionParticipant(MedplumFHIRBase):
    """Indicates who should participate in performing the action described."""

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
    type: Literal["patient", "practitioner", "related-person", "device"] = Field(
        default=..., description="The type of participant in the action."
    )
    role: Optional[CodeableConcept] = Field(
        default=None,
        description="The role the participant should play in performing the described action.",
    )


class PlanDefinitionActionRelatedAction(MedplumFHIRBase):
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
        description="The element id of the related action.",
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


class PlanDefinitionGoal(MedplumFHIRBase):
    """Goals that describe what the activities within the plan are intended to
    achieve. For example, weight loss, restoring an activity of daily
    living, obtaining herd immunity via immunization, meeting a process
    improvement objective, etc.
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
    category: Optional[CodeableConcept] = Field(
        default=None, description="Indicates a category the goal falls within."
    )
    description: CodeableConcept = Field(
        default=...,
        description="Human-readable and/or coded description of a specific desired objective of care, such as &quot;control blood pressure&quot; or &quot;negotiate an obstacle course&quot; or &quot;dance with child at wedding&quot;.",
    )
    priority: Optional[CodeableConcept] = Field(
        default=None,
        description="Identifies the expected level of importance associated with reaching/sustaining the defined goal.",
    )
    start: Optional[CodeableConcept] = Field(
        default=None,
        description="The event after which the goal should begin being pursued.",
    )
    addresses: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Identifies problems, conditions, issues, or concerns the goal is intended to address.",
    )
    documentation: Optional[list[RelatedArtifact]] = Field(
        default=None,
        description="Didactic or other informational resources associated with the goal that provide further supporting information about the goal. Information resources can include inline text commentary and links to web resources.",
    )
    target: Optional[list[PlanDefinitionGoalTarget]] = Field(
        default=None,
        description="Indicates what should be done and within what timeframe.",
    )


class PlanDefinitionGoalTarget(MedplumFHIRBase):
    """Indicates what should be done and within what timeframe."""

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
    measure: Optional[CodeableConcept] = Field(
        default=None,
        description="The parameter whose value is to be tracked, e.g. body weight, blood pressure, or hemoglobin A1c level.",
    )
    detail_quantity: Optional[Quantity] = Field(
        default=None,
        alias="detailQuantity",
        description="The target value of the measure to be achieved to signify fulfillment of the goal, e.g. 150 pounds or 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any value at or above the low value.",
    )
    detail_range: Optional[Range] = Field(
        default=None,
        alias="detailRange",
        description="The target value of the measure to be achieved to signify fulfillment of the goal, e.g. 150 pounds or 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any value at or above the low value.",
    )
    detail_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="detailCodeableConcept",
        description="The target value of the measure to be achieved to signify fulfillment of the goal, e.g. 150 pounds or 7.0%. Either the high or low or both values of the range can be specified. When a low value is missing, it indicates that the goal is achieved at any value at or below the high value. Similarly, if the high value is missing, it indicates that the goal is achieved at any value at or above the low value.",
    )
    due: Optional[Duration] = Field(
        default=None,
        description="Indicates the timeframe after the start of the goal in which the goal should be met.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("PlanDefinition", PlanDefinition)
    register_model("PlanDefinitionAction", PlanDefinitionAction)
    register_model("PlanDefinitionActionCondition", PlanDefinitionActionCondition)
    register_model("PlanDefinitionActionDynamicValue", PlanDefinitionActionDynamicValue)
    register_model("PlanDefinitionActionParticipant", PlanDefinitionActionParticipant)
    register_model(
        "PlanDefinitionActionRelatedAction", PlanDefinitionActionRelatedAction
    )
    register_model("PlanDefinitionGoal", PlanDefinitionGoal)
    register_model("PlanDefinitionGoalTarget", PlanDefinitionGoalTarget)
