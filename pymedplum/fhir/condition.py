# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Condition(MedplumFHIRBase):
    """A clinical condition, problem, diagnosis, or other event, situation,
    issue, or clinical concept that has risen to a level of concern.
    """

    resource_type: Literal["Condition"] = Field(
        default="Condition", alias="resourceType"
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
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="Business identifiers assigned to this condition by the performer or other systems which remain constant as the resource is updated and propagates from server to server.",
    )
    clinical_status: Optional[CodeableConcept] = Field(
        default=None,
        alias="clinicalStatus",
        description="The clinical status of the condition.",
    )
    verification_status: Optional[CodeableConcept] = Field(
        default=None,
        alias="verificationStatus",
        description="The verification status to support the clinical status of the condition.",
    )
    category: Optional[List[CodeableConcept]] = Field(
        default=None, description="A category assigned to the condition."
    )
    severity: Optional[CodeableConcept] = Field(
        default=None,
        description="A subjective assessment of the severity of the condition as evaluated by the clinician.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="Identification of the condition, problem or diagnosis.",
    )
    body_site: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="bodySite",
        description="The anatomical location where this condition manifests itself.",
    )
    subject: Reference = Field(
        default=...,
        description="Indicates the patient or group who the condition record is associated with.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The Encounter during which this Condition was created or to which the creation of this record is tightly associated.",
    )
    onset_date_time: Optional[str] = Field(
        default=None,
        alias="onsetDateTime",
        description="Estimated or actual date or date-time the condition began, in the opinion of the clinician.",
    )
    onset_age: Optional[Age] = Field(
        default=None,
        alias="onsetAge",
        description="Estimated or actual date or date-time the condition began, in the opinion of the clinician.",
    )
    onset_period: Optional[Period] = Field(
        default=None,
        alias="onsetPeriod",
        description="Estimated or actual date or date-time the condition began, in the opinion of the clinician.",
    )
    onset_range: Optional[Range] = Field(
        default=None,
        alias="onsetRange",
        description="Estimated or actual date or date-time the condition began, in the opinion of the clinician.",
    )
    onset_string: Optional[str] = Field(
        default=None,
        alias="onsetString",
        description="Estimated or actual date or date-time the condition began, in the opinion of the clinician.",
    )
    abatement_date_time: Optional[str] = Field(
        default=None,
        alias="abatementDateTime",
        description="The date or estimated date that the condition resolved or went into remission. This is called &quot;abatement&quot; because of the many overloaded connotations associated with &quot;remission&quot; or &quot;resolution&quot; - Conditions are never really resolved, but they can abate.",
    )
    abatement_age: Optional[Age] = Field(
        default=None,
        alias="abatementAge",
        description="The date or estimated date that the condition resolved or went into remission. This is called &quot;abatement&quot; because of the many overloaded connotations associated with &quot;remission&quot; or &quot;resolution&quot; - Conditions are never really resolved, but they can abate.",
    )
    abatement_period: Optional[Period] = Field(
        default=None,
        alias="abatementPeriod",
        description="The date or estimated date that the condition resolved or went into remission. This is called &quot;abatement&quot; because of the many overloaded connotations associated with &quot;remission&quot; or &quot;resolution&quot; - Conditions are never really resolved, but they can abate.",
    )
    abatement_range: Optional[Range] = Field(
        default=None,
        alias="abatementRange",
        description="The date or estimated date that the condition resolved or went into remission. This is called &quot;abatement&quot; because of the many overloaded connotations associated with &quot;remission&quot; or &quot;resolution&quot; - Conditions are never really resolved, but they can abate.",
    )
    abatement_string: Optional[str] = Field(
        default=None,
        alias="abatementString",
        description="The date or estimated date that the condition resolved or went into remission. This is called &quot;abatement&quot; because of the many overloaded connotations associated with &quot;remission&quot; or &quot;resolution&quot; - Conditions are never really resolved, but they can abate.",
    )
    recorded_date: Optional[str] = Field(
        default=None,
        alias="recordedDate",
        description="The recordedDate represents when this particular Condition record was created in the system, which is often a system-generated date.",
    )
    recorder: Optional[Reference] = Field(
        default=None,
        description="Individual who recorded the record and takes responsibility for its content.",
    )
    asserter: Optional[Reference] = Field(
        default=None, description="Individual who is making the condition statement."
    )
    stage: Optional[List[ConditionStage]] = Field(
        default=None,
        description="Clinical stage or grade of a condition. May include formal severity assessments.",
    )
    evidence: Optional[List[ConditionEvidence]] = Field(
        default=None,
        description="Supporting evidence / manifestations that are the basis of the Condition's verification status, such as evidence that confirmed or refuted the condition.",
    )
    note: Optional[List[Annotation]] = Field(
        default=None,
        description="Additional information about the Condition. This is a general notes/comments entry for description of the Condition, its diagnosis and prognosis.",
    )


class ConditionEvidence(MedplumFHIRBase):
    """Supporting evidence / manifestations that are the basis of the
    Condition's verification status, such as evidence that confirmed or
    refuted the condition.
    """

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
    code: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A manifestation or symptom that led to the recording of this condition.",
    )
    detail: Optional[List[Reference]] = Field(
        default=None,
        description="Links to other relevant information, including pathology reports.",
    )


class ConditionStage(MedplumFHIRBase):
    """Clinical stage or grade of a condition. May include formal severity assessments."""

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
    summary: Optional[CodeableConcept] = Field(
        default=None,
        description="A simple summary of the stage such as &quot;Stage 3&quot;. The determination of the stage is disease-specific.",
    )
    assessment: Optional[List[Reference]] = Field(
        default=None,
        description="Reference to a formal record of the evidence on which the staging assessment is based.",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The kind of staging, such as pathological or clinical staging.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Condition", Condition)
    register_model("ConditionEvidence", ConditionEvidence)
    register_model("ConditionStage", ConditionStage)
