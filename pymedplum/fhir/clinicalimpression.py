# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ClinicalImpression(MedplumFHIRBase):
    """A record of a clinical assessment performed to determine what problem(s)
    may affect the patient and before planning the treatments or management
    strategies that are best to manage a patient's condition. Assessments
    are often 1:1 with a clinical consultation / encounter, but this varies
    greatly depending on the clinical workflow. This resource is called
    &quot;ClinicalImpression&quot; rather than
    &quot;ClinicalAssessment&quot; to avoid confusion with the recording of
    assessment tools such as Apgar score.
    """

    resource_type: Literal["ClinicalImpression"] = Field(
        default="ClinicalImpression", alias="resourceType"
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
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="Business identifiers assigned to this clinical impression by the performer or other systems which remain constant as the resource is updated and propagates from server to server.",
    )
    status: Literal["in-progress", "completed", "entered-in-error"] = Field(
        default=..., description="Identifies the workflow status of the assessment."
    )
    status_reason: Optional[CodeableConcept] = Field(
        default=None,
        alias="statusReason",
        description="Captures the reason for the current state of the ClinicalImpression.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="Categorizes the type of clinical assessment performed.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A summary of the context and/or cause of the assessment - why / where it was performed, and what patient events/status prompted it.",
    )
    subject: Reference = Field(
        default=...,
        description="The patient or group of individuals assessed as part of this record.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The Encounter during which this ClinicalImpression was created or to which the creation of this record is tightly associated.",
    )
    effective_date_time: Optional[str] = Field(
        default=None,
        alias="effectiveDateTime",
        description="The point in time or period over which the subject was assessed.",
    )
    effective_period: Optional[Period] = Field(
        default=None,
        alias="effectivePeriod",
        description="The point in time or period over which the subject was assessed.",
    )
    date: Optional[str] = Field(
        default=None,
        description="Indicates when the documentation of the assessment was complete.",
    )
    assessor: Optional[Reference] = Field(
        default=None, description="The clinician performing the assessment."
    )
    previous: Optional[Reference] = Field(
        default=None,
        description="A reference to the last assessment that was conducted on this patient. Assessments are often/usually ongoing in nature; a care provider (practitioner or team) will make new assessments on an ongoing basis as new data arises or the patient's conditions changes.",
    )
    problem: Optional[list[Reference]] = Field(
        default=None,
        description="A list of the relevant problems/conditions for a patient.",
    )
    investigation: Optional[list[ClinicalImpressionInvestigation]] = Field(
        default=None,
        description="One or more sets of investigations (signs, symptoms, etc.). The actual grouping of investigations varies greatly depending on the type and context of the assessment. These investigations may include data generated during the assessment process, or data previously generated and recorded that is pertinent to the outcomes.",
    )
    protocol: Optional[list[str]] = Field(
        default=None,
        description="Reference to a specific published clinical protocol that was followed during this assessment, and/or that provides evidence in support of the diagnosis.",
    )
    summary: Optional[str] = Field(
        default=None,
        description="A text summary of the investigations and the diagnosis.",
    )
    finding: Optional[list[ClinicalImpressionFinding]] = Field(
        default=None,
        description="Specific findings or diagnoses that were considered likely or relevant to ongoing treatment.",
    )
    prognosis_codeable_concept: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="prognosisCodeableConcept",
        description="Estimate of likely outcome.",
    )
    prognosis_reference: Optional[list[Reference]] = Field(
        default=None,
        alias="prognosisReference",
        description="RiskAssessment expressing likely outcome.",
    )
    supporting_info: Optional[list[Reference]] = Field(
        default=None,
        alias="supportingInfo",
        description="Information supporting the clinical impression.",
    )
    note: Optional[list[Annotation]] = Field(
        default=None,
        description="Commentary about the impression, typically recorded after the impression itself was made, though supplemental notes by the original author could also appear.",
    )


class ClinicalImpressionFinding(MedplumFHIRBase):
    """Specific findings or diagnoses that were considered likely or relevant
    to ongoing treatment.
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
    item_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="itemCodeableConcept",
        description="Specific text or code for finding or diagnosis, which may include ruled-out or resolved conditions.",
    )
    item_reference: Optional[Reference] = Field(
        default=None,
        alias="itemReference",
        description="Specific reference for finding or diagnosis, which may include ruled-out or resolved conditions.",
    )
    basis: Optional[str] = Field(
        default=None, description="Which investigations support finding or diagnosis."
    )


class ClinicalImpressionInvestigation(MedplumFHIRBase):
    """One or more sets of investigations (signs, symptoms, etc.). The actual
    grouping of investigations varies greatly depending on the type and
    context of the assessment. These investigations may include data
    generated during the assessment process, or data previously generated
    and recorded that is pertinent to the outcomes.
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
    code: CodeableConcept = Field(
        default=...,
        description="A name/code for the group (&quot;set&quot;) of investigations. Typically, this will be something like &quot;signs&quot;, &quot;symptoms&quot;, &quot;clinical&quot;, &quot;diagnostic&quot;, but the list is not constrained, and others such groups such as (exposure|family|travel|nutritional) history may be used.",
    )
    item: Optional[list[Reference]] = Field(
        default=None,
        description="A record of a specific investigation that was undertaken.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ClinicalImpression", ClinicalImpression)
    register_model("ClinicalImpressionFinding", ClinicalImpressionFinding)
    register_model("ClinicalImpressionInvestigation", ClinicalImpressionInvestigation)
