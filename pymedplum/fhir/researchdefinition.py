# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class ResearchDefinition(MedplumFHIRBase):
    """The ResearchDefinition resource describes the conditional state
    (population and any exposures being compared within the population) and
    outcome (if specified) that the knowledge (evidence, assertion,
    recommendation) is about.
    """

    resource_type: Literal["ResearchDefinition"] = Field(
        default="ResearchDefinition",
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
    url: Optional[str] = Field(default=None, description="An absolute URI that is used to identify this research definition when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this research definition is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the research definition is stored on different servers.")
    identifier: Optional[list[Identifier]] = Field(default=None, description="A formal identifier that is used to identify this research definition when it is represented in other formats, or referenced in a specification, model, design or an instance.")
    version: Optional[str] = Field(default=None, description="The identifier that is used to identify this version of the research definition when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the research definition author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. To provide a version consistent with the Decision Support Service specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more information on versioning knowledge assets, refer to the Decision Support Service specification. Note that a version is required for non-experimental active artifacts.")
    name: Optional[str] = Field(default=None, description="A natural language name identifying the research definition. This name should be usable as an identifier for the module by machine processing applications such as code generation.")
    title: Optional[str] = Field(default=None, description="A short, descriptive, user-friendly title for the research definition.")
    short_title: Optional[str] = Field(default=None, alias="shortTitle", description="The short title provides an alternate title for use in informal descriptive contexts where the full, formal title is not necessary.")
    subtitle: Optional[str] = Field(default=None, description="An explanatory or alternate title for the ResearchDefinition giving additional information about its content.")
    status: Literal['draft', 'active', 'retired', 'unknown'] = Field(default=..., description="The status of this research definition. Enables tracking the life-cycle of the content.")
    experimental: Optional[bool] = Field(default=None, description="A Boolean value to indicate that this research definition is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.")
    subject_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="subjectCodeableConcept", description="The intended subjects for the ResearchDefinition. If this element is not provided, a Patient subject is assumed, but the subject of the ResearchDefinition can be anything.")
    subject_reference: Optional[Reference] = Field(default=None, alias="subjectReference", description="The intended subjects for the ResearchDefinition. If this element is not provided, a Patient subject is assumed, but the subject of the ResearchDefinition can be anything.")
    date: Optional[str] = Field(default=None, description="The date (and optionally time) when the research definition was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the research definition changes.")
    publisher: Optional[str] = Field(default=None, description="The name of the organization or individual that published the research definition.")
    contact: Optional[list[ContactDetail]] = Field(default=None, description="Contact details to assist a user in finding and communicating with the publisher.")
    description: Optional[str] = Field(default=None, description="A free text natural language description of the research definition from a consumer's perspective.")
    comment: Optional[list[str]] = Field(default=None, description="A human-readable string to clarify or explain concepts about the resource.")
    use_context: Optional[list[UsageContext]] = Field(default=None, alias="useContext", description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate research definition instances.")
    jurisdiction: Optional[list[CodeableConcept]] = Field(default=None, description="A legal or geographic region in which the research definition is intended to be used.")
    purpose: Optional[str] = Field(default=None, description="Explanation of why this research definition is needed and why it has been designed as it has.")
    usage: Optional[str] = Field(default=None, description="A detailed description, from a clinical perspective, of how the ResearchDefinition is used.")
    copyright: Optional[str] = Field(default=None, description="A copyright statement relating to the research definition and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the research definition.")
    approval_date: Optional[str] = Field(default=None, alias="approvalDate", description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.")
    last_review_date: Optional[str] = Field(default=None, alias="lastReviewDate", description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.")
    effective_period: Optional[Period] = Field(default=None, alias="effectivePeriod", description="The period during which the research definition content was or is planned to be in active use.")
    topic: Optional[list[CodeableConcept]] = Field(default=None, description="Descriptive topics related to the content of the ResearchDefinition. Topics provide a high-level categorization grouping types of ResearchDefinitions that can be useful for filtering and searching.")
    author: Optional[list[ContactDetail]] = Field(default=None, description="An individiual or organization primarily involved in the creation and maintenance of the content.")
    editor: Optional[list[ContactDetail]] = Field(default=None, description="An individual or organization primarily responsible for internal coherence of the content.")
    reviewer: Optional[list[ContactDetail]] = Field(default=None, description="An individual or organization primarily responsible for review of some aspect of the content.")
    endorser: Optional[list[ContactDetail]] = Field(default=None, description="An individual or organization responsible for officially endorsing the content for use in some setting.")
    related_artifact: Optional[list[RelatedArtifact]] = Field(default=None, alias="relatedArtifact", description="Related artifacts such as additional documentation, justification, or bibliographic references.")
    library: Optional[list[str]] = Field(default=None, description="A reference to a Library resource containing the formal logic used by the ResearchDefinition.")
    population: Reference = Field(default=..., description="A reference to a ResearchElementDefinition resource that defines the population for the research.")
    exposure: Optional[Reference] = Field(default=None, description="A reference to a ResearchElementDefinition resource that defines the exposure for the research.")
    exposure_alternative: Optional[Reference] = Field(default=None, alias="exposureAlternative", description="A reference to a ResearchElementDefinition resource that defines the exposureAlternative for the research.")
    outcome: Optional[Reference] = Field(default=None, description="A reference to a ResearchElementDefinition resomece that defines the outcome for the research.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("ResearchDefinition", ResearchDefinition)
