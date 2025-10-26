# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.usagecontext import UsageContext


class EvidenceVariable(MedplumFHIRBase):
    """The EvidenceVariable resource describes a &quot;PICO&quot; element that
    knowledge (evidence, assertion, recommendation) is about.
    """

    resource_type: Literal["EvidenceVariable"] = Field(
        default="EvidenceVariable", alias="resourceType"
    )

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
    url: str | None = Field(
        default=None,
        description="An absolute URI that is used to identify this evidence variable when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this evidence variable is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the evidence variable is stored on different servers.",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="A formal identifier that is used to identify this evidence variable when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: str | None = Field(
        default=None,
        description="The identifier that is used to identify this version of the evidence variable when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the evidence variable author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. To provide a version consistent with the Decision Support Service specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more information on versioning knowledge assets, refer to the Decision Support Service specification. Note that a version is required for non-experimental active artifacts.",
    )
    name: str | None = Field(
        default=None,
        description="A natural language name identifying the evidence variable. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: str | None = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the evidence variable.",
    )
    short_title: str | None = Field(
        default=None,
        alias="shortTitle",
        description="The short title provides an alternate title for use in informal descriptive contexts where the full, formal title is not necessary.",
    )
    subtitle: str | None = Field(
        default=None,
        description="An explanatory or alternate title for the EvidenceVariable giving additional information about its content.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this evidence variable. Enables tracking the life-cycle of the content.",
    )
    date: str | None = Field(
        default=None,
        description="The date (and optionally time) when the evidence variable was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the evidence variable changes.",
    )
    publisher: str | None = Field(
        default=None,
        description="The name of the organization or individual that published the evidence variable.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: str | None = Field(
        default=None,
        description="A free text natural language description of the evidence variable from a consumer's perspective.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="A human-readable string to clarify or explain concepts about the resource.",
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate evidence variable instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None,
        description="A legal or geographic region in which the evidence variable is intended to be used.",
    )
    copyright: str | None = Field(
        default=None,
        description="A copyright statement relating to the evidence variable and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the evidence variable.",
    )
    approval_date: str | None = Field(
        default=None,
        alias="approvalDate",
        description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.",
    )
    last_review_date: str | None = Field(
        default=None,
        alias="lastReviewDate",
        description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.",
    )
    effective_period: Period | None = Field(
        default=None,
        alias="effectivePeriod",
        description="The period during which the evidence variable content was or is planned to be in active use.",
    )
    topic: list[CodeableConcept] | None = Field(
        default=None,
        description="Descriptive topics related to the content of the EvidenceVariable. Topics provide a high-level categorization grouping types of EvidenceVariables that can be useful for filtering and searching.",
    )
    author: list[ContactDetail] | None = Field(
        default=None,
        description="An individiual or organization primarily involved in the creation and maintenance of the content.",
    )
    editor: list[ContactDetail] | None = Field(
        default=None,
        description="An individual or organization primarily responsible for internal coherence of the content.",
    )
    reviewer: list[ContactDetail] | None = Field(
        default=None,
        description="An individual or organization primarily responsible for review of some aspect of the content.",
    )
    endorser: list[ContactDetail] | None = Field(
        default=None,
        description="An individual or organization responsible for officially endorsing the content for use in some setting.",
    )
    related_artifact: list[RelatedArtifact] | None = Field(
        default=None,
        alias="relatedArtifact",
        description="Related artifacts such as additional documentation, justification, or bibliographic references.",
    )
    type: Literal["dichotomous", "continuous", "descriptive"] | None = Field(
        default=None,
        description="The type of evidence element, a population, an exposure, or an outcome.",
    )
    characteristic: list[EvidenceVariableCharacteristic] | None = Field(
        default=None,
        description="A defining factor of the EvidenceVariable. Multiple characteristics are applied with &quot;and&quot; semantics.",
    )


class EvidenceVariableCharacteristic(MedplumFHIRBase):
    """A defining factor of the EvidenceVariable. Multiple characteristics are
    applied with &quot;and&quot; semantics.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    link_id: str | None = Field(
        default=None,
        alias="linkId",
        description="Label used for when a characteristic refers to another characteristic.",
    )
    description: str | None = Field(
        default=None,
        description="A short, natural language description of the characteristic that could be used to communicate the criteria to an end-user.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="A human-readable string to clarify or explain concepts about the characteristic.",
    )
    exclude: bool | None = Field(
        default=None,
        description="When true, this characteristic is an exclusion criterion. In other words, not matching this characteristic definition is equivalent to meeting this criterion.",
    )
    definition_reference: Reference | None = Field(
        default=None,
        alias="definitionReference",
        description="Defines the characteristic using a Reference.",
    )
    definition_canonical: str | None = Field(
        default=None,
        alias="definitionCanonical",
        description="Defines the characteristic using Canonical.",
    )
    definition_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="definitionCodeableConcept",
        description="Defines the characteristic using CodeableConcept.",
    )
    definition_expression: Expression | None = Field(
        default=None,
        alias="definitionExpression",
        description="Defines the characteristic using Expression.",
    )
    definition_id: str | None = Field(
        default=None,
        alias="definitionId",
        description="Defines the characteristic using id.",
    )
    definition_by_type_and_value: (
        EvidenceVariableCharacteristicDefinitionByTypeAndValue | None
    ) = Field(
        default=None,
        alias="definitionByTypeAndValue",
        description="Defines the characteristic using both a type and value[x] elements.",
    )
    definition_by_combination: (
        EvidenceVariableCharacteristicDefinitionByCombination | None
    ) = Field(
        default=None,
        alias="definitionByCombination",
        description="Defines the characteristic as a combination of two or more characteristics.",
    )
    instances_quantity: Quantity | None = Field(
        default=None,
        alias="instancesQuantity",
        description="Number of occurrences meeting the characteristic.",
    )
    instances_range: Range | None = Field(
        default=None,
        alias="instancesRange",
        description="Number of occurrences meeting the characteristic.",
    )
    duration_quantity: Quantity | None = Field(
        default=None,
        alias="durationQuantity",
        description="Length of time in which the characteristic is met.",
    )
    duration_range: Range | None = Field(
        default=None,
        alias="durationRange",
        description="Length of time in which the characteristic is met.",
    )
    time_from_event: list[EvidenceVariableCharacteristicTimeFromEvent] | None = Field(
        default=None,
        alias="timeFromEvent",
        description="Timing in which the characteristic is determined.",
    )


class EvidenceVariableCharacteristicDefinitionByCombination(MedplumFHIRBase):
    """Defines the characteristic as a combination of two or more characteristics."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: str = Field(
        default=...,
        description="Used to specify if two or more characteristics are combined with OR or AND.",
    )
    threshold: int | float | None = Field(
        default=None,
        description="Provides the value of &quot;n&quot; when &quot;at-least&quot; or &quot;at-most&quot; codes are used.",
    )
    characteristic: list[EvidenceVariableCharacteristic] = Field(
        default=..., description="A defining factor of the characteristic."
    )


class EvidenceVariableCharacteristicDefinitionByTypeAndValue(MedplumFHIRBase):
    """Defines the characteristic using both a type and value[x] elements."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=..., description="Used to express the type of characteristic."
    )
    method: list[CodeableConcept] | None = Field(
        default=None,
        description="Method for how the characteristic value was determined.",
    )
    device: Reference | None = Field(
        default=None, description="Device used for determining characteristic."
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="Defines the characteristic when paired with characteristic.type.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="Defines the characteristic when paired with characteristic.type.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="Defines the characteristic when paired with characteristic.type.",
    )
    value_range: Range | None = Field(
        default=None,
        alias="valueRange",
        description="Defines the characteristic when paired with characteristic.type.",
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="Defines the characteristic when paired with characteristic.type.",
    )
    value_id: str | None = Field(
        default=None,
        alias="valueId",
        description="Defines the characteristic when paired with characteristic.type.",
    )
    offset: CodeableConcept | None = Field(
        default=None,
        description="Defines the reference point for comparison when valueQuantity or valueRange is not compared to zero.",
    )


class EvidenceVariableCharacteristicTimeFromEvent(MedplumFHIRBase):
    """Timing in which the characteristic is determined."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    description: str | None = Field(
        default=None, description="Human readable description."
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="A human-readable string to clarify or explain concepts about the timeFromEvent.",
    )
    event_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="eventCodeableConcept",
        description="The event used as a base point (reference point) in time.",
    )
    event_reference: Reference | None = Field(
        default=None,
        alias="eventReference",
        description="The event used as a base point (reference point) in time.",
    )
    event_date_time: str | None = Field(
        default=None,
        alias="eventDateTime",
        description="The event used as a base point (reference point) in time.",
    )
    event_id: str | None = Field(
        default=None,
        alias="eventId",
        description="The event used as a base point (reference point) in time.",
    )
    quantity: Quantity | None = Field(
        default=None,
        description="Used to express the observation at a defined amount of time before or after the event.",
    )
    range: Range | None = Field(
        default=None,
        description="Used to express the observation within a period before and/or after the event.",
    )
