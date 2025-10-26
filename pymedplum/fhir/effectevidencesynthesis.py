# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class EffectEvidenceSynthesis(MedplumFHIRBase):
    """The EffectEvidenceSynthesis resource describes the difference in an
    outcome between exposures states in a population where the effect
    estimate is derived from a combination of research studies.
    """

    resource_type: Literal["EffectEvidenceSynthesis"] = Field(
        default="EffectEvidenceSynthesis", alias="resourceType"
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
    contained: Optional[List[Resource]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    url: Optional[str] = Field(
        default=None,
        description="An absolute URI that is used to identify this effect evidence synthesis when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this effect evidence synthesis is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the effect evidence synthesis is stored on different servers.",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="A formal identifier that is used to identify this effect evidence synthesis when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the effect evidence synthesis when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the effect evidence synthesis author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A natural language name identifying the effect evidence synthesis. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the effect evidence synthesis.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this effect evidence synthesis. Enables tracking the life-cycle of the content.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the effect evidence synthesis was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the effect evidence synthesis changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the effect evidence synthesis.",
    )
    contact: Optional[List[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the effect evidence synthesis from a consumer's perspective.",
    )
    note: Optional[List[Annotation]] = Field(
        default=None,
        description="A human-readable string to clarify or explain concepts about the resource.",
    )
    use_context: Optional[List[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate effect evidence synthesis instances.",
    )
    jurisdiction: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the effect evidence synthesis is intended to be used.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the effect evidence synthesis and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the effect evidence synthesis.",
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
        description="The period during which the effect evidence synthesis content was or is planned to be in active use.",
    )
    topic: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="Descriptive topics related to the content of the EffectEvidenceSynthesis. Topics provide a high-level categorization grouping types of EffectEvidenceSynthesiss that can be useful for filtering and searching.",
    )
    author: Optional[List[ContactDetail]] = Field(
        default=None,
        description="An individiual or organization primarily involved in the creation and maintenance of the content.",
    )
    editor: Optional[List[ContactDetail]] = Field(
        default=None,
        description="An individual or organization primarily responsible for internal coherence of the content.",
    )
    reviewer: Optional[List[ContactDetail]] = Field(
        default=None,
        description="An individual or organization primarily responsible for review of some aspect of the content.",
    )
    endorser: Optional[List[ContactDetail]] = Field(
        default=None,
        description="An individual or organization responsible for officially endorsing the content for use in some setting.",
    )
    related_artifact: Optional[List[RelatedArtifact]] = Field(
        default=None,
        alias="relatedArtifact",
        description="Related artifacts such as additional documentation, justification, or bibliographic references.",
    )
    synthesis_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="synthesisType",
        description="Type of synthesis eg meta-analysis.",
    )
    study_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="studyType",
        description="Type of study eg randomized trial.",
    )
    population: Reference = Field(
        default=...,
        description="A reference to a EvidenceVariable resource that defines the population for the research.",
    )
    exposure: Reference = Field(
        default=...,
        description="A reference to a EvidenceVariable resource that defines the exposure for the research.",
    )
    exposure_alternative: Reference = Field(
        default=...,
        alias="exposureAlternative",
        description="A reference to a EvidenceVariable resource that defines the comparison exposure for the research.",
    )
    outcome: Reference = Field(
        default=...,
        description="A reference to a EvidenceVariable resomece that defines the outcome for the research.",
    )
    sample_size: Optional[EffectEvidenceSynthesisSampleSize] = Field(
        default=None,
        alias="sampleSize",
        description="A description of the size of the sample involved in the synthesis.",
    )
    results_by_exposure: Optional[List[EffectEvidenceSynthesisResultsByExposure]] = (
        Field(
            default=None,
            alias="resultsByExposure",
            description="A description of the results for each exposure considered in the effect estimate.",
        )
    )
    effect_estimate: Optional[List[EffectEvidenceSynthesisEffectEstimate]] = Field(
        default=None,
        alias="effectEstimate",
        description="The estimated effect of the exposure variant.",
    )
    certainty: Optional[List[EffectEvidenceSynthesisCertainty]] = Field(
        default=None,
        description="A description of the certainty of the effect estimate.",
    )


class EffectEvidenceSynthesisCertainty(MedplumFHIRBase):
    """A description of the certainty of the effect estimate."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    rating: Optional[List[CodeableConcept]] = Field(
        default=None, description="A rating of the certainty of the effect estimate."
    )
    note: Optional[List[Annotation]] = Field(
        default=None,
        description="A human-readable string to clarify or explain concepts about the resource.",
    )
    certainty_subcomponent: Optional[
        List[EffectEvidenceSynthesisCertaintyCertaintySubcomponent]
    ] = Field(
        default=None,
        alias="certaintySubcomponent",
        description="A description of a component of the overall certainty.",
    )


class EffectEvidenceSynthesisCertaintyCertaintySubcomponent(MedplumFHIRBase):
    """A description of a component of the overall certainty."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Optional[CodeableConcept] = Field(
        default=None, description="Type of subcomponent of certainty rating."
    )
    rating: Optional[List[CodeableConcept]] = Field(
        default=None, description="A rating of a subcomponent of rating certainty."
    )
    note: Optional[List[Annotation]] = Field(
        default=None,
        description="A human-readable string to clarify or explain concepts about the resource.",
    )


class EffectEvidenceSynthesisEffectEstimate(MedplumFHIRBase):
    """The estimated effect of the exposure variant."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    description: Optional[str] = Field(
        default=None, description="Human-readable summary of effect estimate."
    )
    type: Optional[CodeableConcept] = Field(
        default=None, description="Examples include relative risk and mean difference."
    )
    variant_state: Optional[CodeableConcept] = Field(
        default=None,
        alias="variantState",
        description="Used to define variant exposure states such as low-risk state.",
    )
    value: Optional[Union[int, float]] = Field(
        default=None, description="The point estimate of the effect estimate."
    )
    unit_of_measure: Optional[CodeableConcept] = Field(
        default=None,
        alias="unitOfMeasure",
        description="Specifies the UCUM unit for the outcome.",
    )
    precision_estimate: Optional[
        List[EffectEvidenceSynthesisEffectEstimatePrecisionEstimate]
    ] = Field(
        default=None,
        alias="precisionEstimate",
        description="A description of the precision of the estimate for the effect.",
    )


class EffectEvidenceSynthesisEffectEstimatePrecisionEstimate(MedplumFHIRBase):
    """A description of the precision of the estimate for the effect."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="Examples include confidence interval and interquartile range.",
    )
    level: Optional[Union[int, float]] = Field(
        default=None, description="Use 95 for a 95% confidence interval."
    )
    from_: Optional[Union[int, float]] = Field(
        default=None, alias="from", description="Lower bound of confidence interval."
    )
    to: Optional[Union[int, float]] = Field(
        default=None, description="Upper bound of confidence interval."
    )


class EffectEvidenceSynthesisResultsByExposure(MedplumFHIRBase):
    """A description of the results for each exposure considered in the effect estimate."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    description: Optional[str] = Field(
        default=None, description="Human-readable summary of results by exposure state."
    )
    exposure_state: Optional[Literal["exposure", "exposure-alternative"]] = Field(
        default=None,
        alias="exposureState",
        description="Whether these results are for the exposure state or alternative exposure state.",
    )
    variant_state: Optional[CodeableConcept] = Field(
        default=None,
        alias="variantState",
        description="Used to define variant exposure states such as low-risk state.",
    )
    risk_evidence_synthesis: Reference = Field(
        default=...,
        alias="riskEvidenceSynthesis",
        description="Reference to a RiskEvidenceSynthesis resource.",
    )


class EffectEvidenceSynthesisSampleSize(MedplumFHIRBase):
    """A description of the size of the sample involved in the synthesis."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    description: Optional[str] = Field(
        default=None, description="Human-readable summary of sample size."
    )
    number_of_studies: Optional[Union[int, float]] = Field(
        default=None,
        alias="numberOfStudies",
        description="Number of studies included in this evidence synthesis.",
    )
    number_of_participants: Optional[Union[int, float]] = Field(
        default=None,
        alias="numberOfParticipants",
        description="Number of participants included in this evidence synthesis.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("EffectEvidenceSynthesis", EffectEvidenceSynthesis)
    register_model("EffectEvidenceSynthesisCertainty", EffectEvidenceSynthesisCertainty)
    register_model(
        "EffectEvidenceSynthesisCertaintyCertaintySubcomponent",
        EffectEvidenceSynthesisCertaintyCertaintySubcomponent,
    )
    register_model(
        "EffectEvidenceSynthesisEffectEstimate", EffectEvidenceSynthesisEffectEstimate
    )
    register_model(
        "EffectEvidenceSynthesisEffectEstimatePrecisionEstimate",
        EffectEvidenceSynthesisEffectEstimatePrecisionEstimate,
    )
    register_model(
        "EffectEvidenceSynthesisResultsByExposure",
        EffectEvidenceSynthesisResultsByExposure,
    )
    register_model(
        "EffectEvidenceSynthesisSampleSize", EffectEvidenceSynthesisSampleSize
    )
