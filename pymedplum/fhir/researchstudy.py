# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact


class ResearchStudy(MedplumFHIRBase):
    """A process where a researcher or organization plans and then executes a
    series of steps intended to increase the field of healthcare-related
    knowledge. This includes studies of safety, efficacy, comparative
    effectiveness and other information about medications, devices,
    therapies and other interventional and investigative techniques. A
    ResearchStudy involves the gathering of information about human or
    animal subjects.
    """

    resource_type: Literal["ResearchStudy"] = Field(
        default="ResearchStudy", alias="resourceType"
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
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Identifiers assigned to this research study by the sponsor or other systems.",
    )
    name: str | None = Field(
        default=None, description="Name for this study (computer friendly)."
    )
    title: str | None = Field(
        default=None, description="The human readable name of the research study."
    )
    label: list[ResearchStudyLabel] | None = Field(
        default=None, description="Additional names for the study."
    )
    protocol: list[Reference] | None = Field(
        default=None,
        description="The set of steps expected to be performed as part of the execution of the study.",
    )
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="A larger research study of which this particular study is a component or step.",
    )
    status: Literal[
        "active",
        "administratively-completed",
        "approved",
        "closed-to-accrual",
        "closed-to-accrual-and-intervention",
        "completed",
        "disapproved",
        "in-review",
        "temporarily-closed-to-accrual",
        "temporarily-closed-to-accrual-and-intervention",
        "withdrawn",
    ] = Field(default=..., description="The current state of the study.")
    primary_purpose_type: CodeableConcept | None = Field(
        default=None,
        alias="primaryPurposeType",
        description="The type of study based upon the intent of the study's activities. A classification of the intent of the study.",
    )
    phase: CodeableConcept | None = Field(
        default=None,
        description="The stage in the progression of a therapy from initial experimental use in humans in clinical trials to post-market evaluation.",
    )
    study_design: list[CodeableConcept] | None = Field(
        default=None,
        alias="studyDesign",
        description="Codes categorizing the type of study such as investigational vs. observational, type of blinding, type of randomization, safety vs. efficacy, etc.",
    )
    category: list[CodeableConcept] | None = Field(
        default=None,
        description="Codes categorizing the type of study such as investigational vs. observational, type of blinding, type of randomization, safety vs. efficacy, etc.",
    )
    focus: list[CodeableConcept] | None = Field(
        default=None,
        description="The medication(s), food(s), therapy(ies), device(s) or other concerns or interventions that the study is seeking to gain more information about.",
    )
    condition: list[CodeableConcept] | None = Field(
        default=None,
        description="The condition that is the focus of the study. For example, In a study to examine risk factors for Lupus, might have as an inclusion criterion &quot;healthy volunteer&quot;, but the target condition code would be a Lupus SNOMED code.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in learning more about or engaging with the study.",
    )
    related_artifact: list[RelatedArtifact] | None = Field(
        default=None,
        alias="relatedArtifact",
        description="Citations, references, URLs and other related documents. When using relatedArtifact to share URLs, the relatedArtifact.type will often be set to one of &quot;documentation&quot; or &quot;supported-with&quot; and the URL value will often be in relatedArtifact.document.url but another possible location is relatedArtifact.resource when it is a canonical URL.",
    )
    keyword: list[CodeableConcept] | None = Field(
        default=None,
        description="Key terms to aid in searching for or filtering the study.",
    )
    location: list[CodeableConcept] | None = Field(
        default=None,
        description="Indicates a country, state or other region where the study is taking place.",
    )
    region: list[CodeableConcept] | None = Field(
        default=None,
        description="A country, state or other area where the study is taking place rather than its precise geographic location or address.",
    )
    description_summary: str | None = Field(
        default=None,
        alias="descriptionSummary",
        description="A brief text for explaining the study.",
    )
    description: str | None = Field(
        default=None,
        description="A detailed and human-readable narrative of the study. E.g., study abstract.",
    )
    enrollment: list[Reference] | None = Field(
        default=None,
        description="Reference to a Group that defines the criteria for and quantity of subjects participating in the study. E.g. &quot; 200 female Europeans between the ages of 20 and 45 with early onset diabetes&quot;.",
    )
    period: Period | None = Field(
        default=None,
        description="Identifies the start date and the expected (or actual, depending on status) end date for the study.",
    )
    sponsor: Reference | None = Field(
        default=None,
        description="An organization that initiates the investigation and is legally responsible for the study.",
    )
    principal_investigator: Reference | None = Field(
        default=None,
        alias="principalInvestigator",
        description="A researcher in a study who oversees multiple aspects of the study, such as concept development, protocol writing, protocol submission for IRB approval, participant recruitment, informed consent, data collection, analysis, interpretation and presentation.",
    )
    site: list[Reference] | None = Field(
        default=None, description="A facility in which study activities are conducted."
    )
    reason_stopped: CodeableConcept | None = Field(
        default=None,
        alias="reasonStopped",
        description="A description and/or code explaining the premature termination of the study.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Comments made about the study by the performer, subject or other participants.",
    )
    arm: list[ResearchStudyArm] | None = Field(
        default=None,
        description="Describes an expected sequence of events for one of the participants of a study. E.g. Exposure to drug A, wash-out, exposure to drug B, wash-out, follow-up.",
    )
    classifier: list[CodeableConcept] | None = Field(
        default=None,
        description="Additional grouping mechanism or categorization of a research study. Example: FDA regulated device, FDA regulated drug, MPG Paragraph 23b (a German legal requirement), IRB-exempt, etc. Implementation Note: do not use the classifier element to support existing semantics that are already supported thru explicit elements in the resource.",
    )
    associated_party: list[ResearchStudyAssociatedParty] | None = Field(
        default=None,
        alias="associatedParty",
        description="Sponsors, collaborators, and other parties.",
    )
    progress_status: list[ResearchStudyProgressStatus] | None = Field(
        default=None,
        alias="progressStatus",
        description="Status of study with time for that status.",
    )
    why_stopped: CodeableConcept | None = Field(
        default=None,
        alias="whyStopped",
        description="A description and/or code explaining the premature termination of the study.",
    )
    recruitment: ResearchStudyRecruitment | None = Field(
        default=None,
        description="Target or actual group of participants enrolled in study.",
    )
    comparison_group: list[ResearchStudyComparisonGroup] | None = Field(
        default=None,
        alias="comparisonGroup",
        description="Describes an expected event or sequence of events for one of the subjects of a study. E.g. for a living subject: exposure to drug A, wash-out, exposure to drug B, wash-out, follow-up. E.g. for a stability study: {store sample from lot A at 25 degrees for 1 month}, {store sample from lot A at 40 degrees for 1 month}.",
    )
    objective: list[ResearchStudyObjective] | None = Field(
        default=None,
        description="A goal that the study is aiming to achieve in terms of a scientific question to be answered by the analysis of data collected during the study.",
    )
    outcome_measure: list[ResearchStudyOutcomeMeasure] | None = Field(
        default=None,
        alias="outcomeMeasure",
        description="An &quot;outcome measure&quot;, &quot;endpoint&quot;, &quot;effect measure&quot; or &quot;measure of effect&quot; is a specific measurement or observation used to quantify the effect of experimental variables on the participants in a study, or for observational studies, to describe patterns of diseases or traits or associations with exposures, risk factors or treatment.",
    )
    result: list[Reference] | None = Field(
        default=None,
        description="Link to one or more sets of results generated by the study. Could also link to a research registry holding the results such as ClinicalTrials.gov.",
    )


class ResearchStudyArm(MedplumFHIRBase):
    """Describes an expected sequence of events for one of the participants of
    a study. E.g. Exposure to drug A, wash-out, exposure to drug B,
    wash-out, follow-up.
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
    name: str = Field(
        default=...,
        description="Unique, human-readable label for this arm of the study.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Categorization of study arm, e.g. experimental, active comparator, placebo comparater.",
    )
    description: str | None = Field(
        default=None,
        description="A succinct description of the path through the study that would be followed by a subject adhering to this arm.",
    )


class ResearchStudyAssociatedParty(MedplumFHIRBase):
    """Sponsors, collaborators, and other parties."""

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
    name: str | None = Field(default=None, description="Name of associated party.")
    role: CodeableConcept = Field(default=..., description="Type of association.")
    period: list[Period] | None = Field(
        default=None,
        description="Identifies the start date and the end date of the associated party in the role.",
    )
    classifier: list[CodeableConcept] | None = Field(
        default=None,
        description="A categorization other than role for the associated party.",
    )
    party: Reference | None = Field(
        default=None,
        description="Individual or organization associated with study (use practitionerRole to specify their organisation).",
    )


class ResearchStudyComparisonGroup(MedplumFHIRBase):
    """Describes an expected event or sequence of events for one of the
    subjects of a study. E.g. for a living subject: exposure to drug A,
    wash-out, exposure to drug B, wash-out, follow-up. E.g. for a stability
    study: {store sample from lot A at 25 degrees for 1 month}, {store
    sample from lot A at 40 degrees for 1 month}.
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
        description="Allows the comparisonGroup for the study and the comparisonGroup for the subject to be linked easily.",
    )
    name: str = Field(
        default=...,
        description="Unique, human-readable label for this comparisonGroup of the study.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Categorization of study comparisonGroup, e.g. experimental, active comparator, placebo comparater.",
    )
    description: str | None = Field(
        default=None,
        description="A succinct description of the path through the study that would be followed by a subject adhering to this comparisonGroup.",
    )
    intended_exposure: list[Reference] | None = Field(
        default=None,
        alias="intendedExposure",
        description="Interventions or exposures in this comparisonGroup or cohort.",
    )
    observed_group: Reference | None = Field(
        default=None,
        alias="observedGroup",
        description="Group of participants who were enrolled in study comparisonGroup.",
    )


class ResearchStudyLabel(MedplumFHIRBase):
    """Additional names for the study."""

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
    type: CodeableConcept | None = Field(default=None, description="Kind of name.")
    value: str | None = Field(default=None, description="The name.")


class ResearchStudyObjective(MedplumFHIRBase):
    """A goal that the study is aiming to achieve in terms of a scientific
    question to be answered by the analysis of data collected during the
    study.
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
    name: str | None = Field(
        default=None,
        description="Unique, human-readable label for this objective of the study.",
    )
    type: CodeableConcept | None = Field(
        default=None, description="The kind of study objective."
    )
    description: str | None = Field(
        default=None,
        description="Free text description of the objective of the study. This is what the study is trying to achieve rather than how it is going to achieve it (see ResearchStudy.description).",
    )


class ResearchStudyOutcomeMeasure(MedplumFHIRBase):
    """An &quot;outcome measure&quot;, &quot;endpoint&quot;, &quot;effect
    measure&quot; or &quot;measure of effect&quot; is a specific measurement
    or observation used to quantify the effect of experimental variables on
    the participants in a study, or for observational studies, to describe
    patterns of diseases or traits or associations with exposures, risk
    factors or treatment.
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
    name: str | None = Field(default=None, description="Label for the outcome.")
    type: list[CodeableConcept] | None = Field(
        default=None,
        description="The parameter or characteristic being assessed as one of the values by which the study is assessed.",
    )
    description: str | None = Field(
        default=None, description="Description of the outcome."
    )
    reference: Reference | None = Field(
        default=None, description="Structured outcome definition."
    )


class ResearchStudyProgressStatus(MedplumFHIRBase):
    """Status of study with time for that status."""

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
    state: CodeableConcept = Field(
        default=..., description="Label for status or state (e.g. recruitment status)."
    )
    actual: bool | None = Field(
        default=None,
        description="An indication of whether or not the date is a known date when the state changed or will change. A value of true indicates a known date. A value of false indicates an estimated date.",
    )
    period: Period | None = Field(default=None, description="Date range.")


class ResearchStudyRecruitment(MedplumFHIRBase):
    """Target or actual group of participants enrolled in study."""

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
    target_number: int | float | None = Field(
        default=None,
        alias="targetNumber",
        description="Estimated total number of participants to be enrolled.",
    )
    actual_number: int | float | None = Field(
        default=None,
        alias="actualNumber",
        description="Actual total number of participants enrolled in study.",
    )
    eligibility: Reference | None = Field(
        default=None, description="Inclusion and exclusion criteria."
    )
    actual_group: Reference | None = Field(
        default=None,
        alias="actualGroup",
        description="Group of participants who were enrolled in study.",
    )
