# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class AdverseEvent(MedplumFHIRBase):
    """Actual or potential/avoided event causing unintended physical injury
    resulting from or contributed to by medical care, a research study or
    other healthcare setting factors that requires additional monitoring,
    treatment, or hospitalization, or that results in death.
    """

    resource_type: Literal["AdverseEvent"] = Field(
        default="AdverseEvent",
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
    identifier: Optional[Identifier] = Field(default=None, description="Business identifiers assigned to this adverse event by the performer or other systems which remain constant as the resource is updated and propagates from server to server.")
    actuality: Literal['actual', 'potential'] = Field(default=..., description="Whether the event actually happened, or just had the potential to. Note that this is independent of whether anyone was affected or harmed or how severely.")
    category: Optional[list[CodeableConcept]] = Field(default=None, description="The overall type of event, intended for search and filtering purposes.")
    event: Optional[CodeableConcept] = Field(default=None, description="This element defines the specific type of event that occurred or that was prevented from occurring.")
    subject: Reference = Field(default=..., description="This subject or group impacted by the event.")
    encounter: Optional[Reference] = Field(default=None, description="The Encounter during which AdverseEvent was created or to which the creation of this record is tightly associated.")
    date: Optional[str] = Field(default=None, description="The date (and perhaps time) when the adverse event occurred.")
    detected: Optional[str] = Field(default=None, description="Estimated or actual date the AdverseEvent began, in the opinion of the reporter.")
    recorded_date: Optional[str] = Field(default=None, alias="recordedDate", description="The date on which the existence of the AdverseEvent was first recorded.")
    resulting_condition: Optional[list[Reference]] = Field(default=None, alias="resultingCondition", description="Includes information about the reaction that occurred as a result of exposure to a substance (for example, a drug or a chemical).")
    location: Optional[Reference] = Field(default=None, description="The information about where the adverse event occurred.")
    seriousness: Optional[CodeableConcept] = Field(default=None, description="Assessment whether this event was of real importance.")
    severity: Optional[CodeableConcept] = Field(default=None, description="Describes the severity of the adverse event, in relation to the subject. Contrast to AdverseEvent.seriousness - a severe rash might not be serious, but a mild heart problem is.")
    outcome: Optional[CodeableConcept] = Field(default=None, description="Describes the type of outcome from the adverse event.")
    recorder: Optional[Reference] = Field(default=None, description="Information on who recorded the adverse event. May be the patient or a practitioner.")
    contributor: Optional[list[Reference]] = Field(default=None, description="Parties that may or should contribute or have contributed information to the adverse event, which can consist of one or more activities. Such information includes information leading to the decision to perform the activity and how to perform the activity (e.g. consultant), information that the activity itself seeks to reveal (e.g. informant of clinical history), or information about what activity was performed (e.g. informant witness).")
    suspect_entity: Optional[list[AdverseEventSuspectEntity]] = Field(default=None, alias="suspectEntity", description="Describes the entity that is suspected to have caused the adverse event.")
    subject_medical_history: Optional[list[Union[Reference]]] = Field(default=None, alias="subjectMedicalHistory", description="AdverseEvent.subjectMedicalHistory.")
    reference_document: Optional[list[Reference]] = Field(default=None, alias="referenceDocument", description="AdverseEvent.referenceDocument.")
    study: Optional[list[Reference]] = Field(default=None, description="AdverseEvent.study.")


class AdverseEventSuspectEntity(MedplumFHIRBase):
    """Describes the entity that is suspected to have caused the adverse event."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    instance: Reference = Field(default=..., description="Identifies the actual instance of what caused the adverse event. May be a substance, medication, medication administration, medication statement or a device.")
    causality: Optional[list[AdverseEventSuspectEntityCausality]] = Field(default=None, description="Information on the possible cause of the event.")


class AdverseEventSuspectEntityCausality(MedplumFHIRBase):
    """Information on the possible cause of the event."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    assessment: Optional[CodeableConcept] = Field(default=None, description="Assessment of if the entity caused the event.")
    product_relatedness: Optional[str] = Field(default=None, alias="productRelatedness", description="AdverseEvent.suspectEntity.causalityProductRelatedness.")
    author: Optional[Reference] = Field(default=None, description="AdverseEvent.suspectEntity.causalityAuthor.")
    method: Optional[CodeableConcept] = Field(default=None, description="ProbabilityScale | Bayesian | Checklist.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("AdverseEvent", AdverseEvent)
    register_model("AdverseEventSuspectEntity", AdverseEventSuspectEntity)
    register_model("AdverseEventSuspectEntityCausality", AdverseEventSuspectEntityCausality)
