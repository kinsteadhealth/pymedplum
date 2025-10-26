# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Measure(MedplumFHIRBase):
    """The Measure resource provides the definition of a quality measure."""

    resource_type: Literal["Measure"] = Field(
        default="Measure",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[list[dict[str, Any]]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    url: Optional[str] = Field(default=None, description="An absolute URI that is used to identify this measure when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this measure is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the measure is stored on different servers.")
    identifier: Optional[list[Identifier]] = Field(default=None, description="A formal identifier that is used to identify this measure when it is represented in other formats, or referenced in a specification, model, design or an instance.")
    version: Optional[str] = Field(default=None, description="The identifier that is used to identify this version of the measure when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the measure author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. To provide a version consistent with the Decision Support Service specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more information on versioning knowledge assets, refer to the Decision Support Service specification. Note that a version is required for non-experimental active artifacts.")
    name: Optional[str] = Field(default=None, description="A natural language name identifying the measure. This name should be usable as an identifier for the module by machine processing applications such as code generation.")
    title: Optional[str] = Field(default=None, description="A short, descriptive, user-friendly title for the measure.")
    subtitle: Optional[str] = Field(default=None, description="An explanatory or alternate title for the measure giving additional information about its content.")
    status: Literal['draft', 'active', 'retired', 'unknown'] = Field(default=..., description="The status of this measure. Enables tracking the life-cycle of the content.")
    experimental: Optional[bool] = Field(default=None, description="A Boolean value to indicate that this measure is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.")
    subject_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="subjectCodeableConcept", description="The intended subjects for the measure. If this element is not provided, a Patient subject is assumed, but the subject of the measure can be anything.")
    subject_reference: Optional[Reference] = Field(default=None, alias="subjectReference", description="The intended subjects for the measure. If this element is not provided, a Patient subject is assumed, but the subject of the measure can be anything.")
    date: Optional[str] = Field(default=None, description="The date (and optionally time) when the measure was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the measure changes.")
    publisher: Optional[str] = Field(default=None, description="The name of the organization or individual that published the measure.")
    contact: Optional[list[ContactDetail]] = Field(default=None, description="Contact details to assist a user in finding and communicating with the publisher.")
    description: Optional[str] = Field(default=None, description="A free text natural language description of the measure from a consumer's perspective.")
    use_context: Optional[list[UsageContext]] = Field(default=None, alias="useContext", description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate measure instances.")
    jurisdiction: Optional[list[CodeableConcept]] = Field(default=None, description="A legal or geographic region in which the measure is intended to be used.")
    purpose: Optional[str] = Field(default=None, description="Explanation of why this measure is needed and why it has been designed as it has.")
    usage: Optional[str] = Field(default=None, description="A detailed description, from a clinical perspective, of how the measure is used.")
    copyright: Optional[str] = Field(default=None, description="A copyright statement relating to the measure and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the measure.")
    approval_date: Optional[str] = Field(default=None, alias="approvalDate", description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.")
    last_review_date: Optional[str] = Field(default=None, alias="lastReviewDate", description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.")
    effective_period: Optional[Period] = Field(default=None, alias="effectivePeriod", description="The period during which the measure content was or is planned to be in active use.")
    topic: Optional[list[CodeableConcept]] = Field(default=None, description="Descriptive topics related to the content of the measure. Topics provide a high-level categorization grouping types of measures that can be useful for filtering and searching.")
    author: Optional[list[ContactDetail]] = Field(default=None, description="An individiual or organization primarily involved in the creation and maintenance of the content.")
    editor: Optional[list[ContactDetail]] = Field(default=None, description="An individual or organization primarily responsible for internal coherence of the content.")
    reviewer: Optional[list[ContactDetail]] = Field(default=None, description="An individual or organization primarily responsible for review of some aspect of the content.")
    endorser: Optional[list[ContactDetail]] = Field(default=None, description="An individual or organization responsible for officially endorsing the content for use in some setting.")
    related_artifact: Optional[list[RelatedArtifact]] = Field(default=None, alias="relatedArtifact", description="Related artifacts such as additional documentation, justification, or bibliographic references.")
    library: Optional[list[str]] = Field(default=None, description="A reference to a Library resource containing the formal logic used by the measure.")
    disclaimer: Optional[str] = Field(default=None, description="Notices and disclaimers regarding the use of the measure or related to intellectual property (such as code systems) referenced by the measure.")
    scoring: Optional[CodeableConcept] = Field(default=None, description="Indicates how the calculation is performed for the measure, including proportion, ratio, continuous-variable, and cohort. The value set is extensible, allowing additional measure scoring types to be represented.")
    composite_scoring: Optional[CodeableConcept] = Field(default=None, alias="compositeScoring", description="If this is a composite measure, the scoring method used to combine the component measures to determine the composite score.")
    type: Optional[list[CodeableConcept]] = Field(default=None, description="Indicates whether the measure is used to examine a process, an outcome over time, a patient-reported outcome, or a structure measure such as utilization.")
    risk_adjustment: Optional[str] = Field(default=None, alias="riskAdjustment", description="A description of the risk adjustment factors that may impact the resulting score for the measure and how they may be accounted for when computing and reporting measure results.")
    rate_aggregation: Optional[str] = Field(default=None, alias="rateAggregation", description="Describes how to combine the information calculated, based on logic in each of several populations, into one summarized result.")
    rationale: Optional[str] = Field(default=None, description="Provides a succinct statement of the need for the measure. Usually includes statements pertaining to importance criterion: impact, gap in care, and evidence.")
    clinical_recommendation_statement: Optional[str] = Field(default=None, alias="clinicalRecommendationStatement", description="Provides a summary of relevant clinical guidelines or other clinical recommendations supporting the measure.")
    improvement_notation: Optional[CodeableConcept] = Field(default=None, alias="improvementNotation", description="Information on whether an increase or decrease in score is the preferred result (e.g., a higher score indicates better quality OR a lower score indicates better quality OR quality is within a range).")
    definition: Optional[list[str]] = Field(default=None, description="Provides a description of an individual term used within the measure.")
    guidance: Optional[str] = Field(default=None, description="Additional guidance for the measure including how it can be used in a clinical context, and the intent of the measure.")
    group: Optional[list[MeasureGroup]] = Field(default=None, description="A group of population criteria for the measure.")
    supplemental_data: Optional[list[MeasureSupplementalData]] = Field(default=None, alias="supplementalData", description="The supplemental data criteria for the measure report, specified as either the name of a valid CQL expression within a referenced library, or a valid FHIR Resource Path.")


class MeasureGroup(MedplumFHIRBase):
    """A group of population criteria for the measure."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="Indicates a meaning for the group. This can be as simple as a unique identifier, or it can establish meaning in a broader context by drawing from a terminology, allowing groups to be correlated across measures.")
    description: Optional[str] = Field(default=None, description="The human readable description of this population group.")
    population: Optional[list[MeasureGroupPopulation]] = Field(default=None, description="A population criteria for the measure.")
    stratifier: Optional[list[MeasureGroupStratifier]] = Field(default=None, description="The stratifier criteria for the measure report, specified as either the name of a valid CQL expression defined within a referenced library or a valid FHIR Resource Path.")


class MeasureGroupPopulation(MedplumFHIRBase):
    """A population criteria for the measure."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="The type of population criteria.")
    description: Optional[str] = Field(default=None, description="The human readable description of this population criteria.")
    criteria: Expression = Field(default=..., description="An expression that specifies the criteria for the population, typically the name of an expression in a library.")


class MeasureGroupStratifier(MedplumFHIRBase):
    """The stratifier criteria for the measure report, specified as either the
    name of a valid CQL expression defined within a referenced library or a
    valid FHIR Resource Path.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="Indicates a meaning for the stratifier. This can be as simple as a unique identifier, or it can establish meaning in a broader context by drawing from a terminology, allowing stratifiers to be correlated across measures.")
    description: Optional[str] = Field(default=None, description="The human readable description of this stratifier criteria.")
    criteria: Optional[Expression] = Field(default=None, description="An expression that specifies the criteria for the stratifier. This is typically the name of an expression defined within a referenced library, but it may also be a path to a stratifier element.")
    component: Optional[list[MeasureGroupStratifierComponent]] = Field(default=None, description="A component of the stratifier criteria for the measure report, specified as either the name of a valid CQL expression defined within a referenced library or a valid FHIR Resource Path.")


class MeasureGroupStratifierComponent(MedplumFHIRBase):
    """A component of the stratifier criteria for the measure report, specified
    as either the name of a valid CQL expression defined within a referenced
    library or a valid FHIR Resource Path.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="Indicates a meaning for the stratifier component. This can be as simple as a unique identifier, or it can establish meaning in a broader context by drawing from a terminology, allowing stratifiers to be correlated across measures.")
    description: Optional[str] = Field(default=None, description="The human readable description of this stratifier criteria component.")
    criteria: Expression = Field(default=..., description="An expression that specifies the criteria for this component of the stratifier. This is typically the name of an expression defined within a referenced library, but it may also be a path to a stratifier element.")


class MeasureSupplementalData(MedplumFHIRBase):
    """The supplemental data criteria for the measure report, specified as
    either the name of a valid CQL expression within a referenced library,
    or a valid FHIR Resource Path.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="Indicates a meaning for the supplemental data. This can be as simple as a unique identifier, or it can establish meaning in a broader context by drawing from a terminology, allowing supplemental data to be correlated across measures.")
    usage: Optional[list[CodeableConcept]] = Field(default=None, description="An indicator of the intended usage for the supplemental data element. Supplemental data indicates the data is additional information requested to augment the measure information. Risk adjustment factor indicates the data is additional information used to calculate risk adjustment factors when applying a risk model to the measure calculation.")
    description: Optional[str] = Field(default=None, description="The human readable description of this supplemental data.")
    criteria: Expression = Field(default=..., description="The criteria for the supplemental data. This is typically the name of a valid expression defined within a referenced library, but it may also be a path to a specific data element. The criteria defines the data to be returned for this element.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Measure", Measure)
    register_model("MeasureGroup", MeasureGroup)
    register_model("MeasureGroupPopulation", MeasureGroupPopulation)
    register_model("MeasureGroupStratifier", MeasureGroupStratifier)
    register_model("MeasureGroupStratifierComponent", MeasureGroupStratifierComponent)
    register_model("MeasureSupplementalData", MeasureSupplementalData)
