# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class FamilyMemberHistory(MedplumFHIRBase):
    """Significant health conditions for a person related to the patient
    relevant in the context of care for the patient.
    """

    resource_type: Literal["FamilyMemberHistory"] = Field(
        default="FamilyMemberHistory",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Business identifiers assigned to this family member history by the performer or other systems which remain constant as the resource is updated and propagates from server to server.")
    instantiates_canonical: Optional[list[str]] = Field(default=None, alias="instantiatesCanonical", description="The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this FamilyMemberHistory.")
    instantiates_uri: Optional[list[str]] = Field(default=None, alias="instantiatesUri", description="The URL pointing to an externally maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this FamilyMemberHistory.")
    status: Literal['partial', 'completed', 'entered-in-error', 'health-unknown'] = Field(default=..., description="A code specifying the status of the record of the family history of a specific family member.")
    data_absent_reason: Optional[CodeableConcept] = Field(default=None, alias="dataAbsentReason", description="Describes why the family member's history is not available.")
    patient: Reference = Field(default=..., description="The person who this history concerns.")
    date: Optional[str] = Field(default=None, description="The date (and possibly time) when the family member history was recorded or last updated.")
    name: Optional[str] = Field(default=None, description="This will either be a name or a description; e.g. &quot;Aunt Susan&quot;, &quot;my cousin with the red hair&quot;.")
    relationship: CodeableConcept = Field(default=..., description="The type of relationship this person has to the patient (father, mother, brother etc.).")
    sex: Optional[CodeableConcept] = Field(default=None, description="The birth sex of the family member.")
    born_period: Optional[Period] = Field(default=None, alias="bornPeriod", description="The actual or approximate date of birth of the relative.")
    born_date: Optional[str] = Field(default=None, alias="bornDate", description="The actual or approximate date of birth of the relative.")
    born_string: Optional[str] = Field(default=None, alias="bornString", description="The actual or approximate date of birth of the relative.")
    age_age: Optional[Age] = Field(default=None, alias="ageAge", description="The age of the relative at the time the family member history is recorded.")
    age_range: Optional[Range] = Field(default=None, alias="ageRange", description="The age of the relative at the time the family member history is recorded.")
    age_string: Optional[str] = Field(default=None, alias="ageString", description="The age of the relative at the time the family member history is recorded.")
    estimated_age: Optional[bool] = Field(default=None, alias="estimatedAge", description="If true, indicates that the age value specified is an estimated value.")
    deceased_boolean: Optional[bool] = Field(default=None, alias="deceasedBoolean", description="Deceased flag or the actual or approximate age of the relative at the time of death for the family member history record.")
    deceased_age: Optional[Age] = Field(default=None, alias="deceasedAge", description="Deceased flag or the actual or approximate age of the relative at the time of death for the family member history record.")
    deceased_range: Optional[Range] = Field(default=None, alias="deceasedRange", description="Deceased flag or the actual or approximate age of the relative at the time of death for the family member history record.")
    deceased_date: Optional[str] = Field(default=None, alias="deceasedDate", description="Deceased flag or the actual or approximate age of the relative at the time of death for the family member history record.")
    deceased_string: Optional[str] = Field(default=None, alias="deceasedString", description="Deceased flag or the actual or approximate age of the relative at the time of death for the family member history record.")
    reason_code: Optional[list[CodeableConcept]] = Field(default=None, alias="reasonCode", description="Describes why the family member history occurred in coded or textual form.")
    reason_reference: Optional[list[Reference]] = Field(default=None, alias="reasonReference", description="Indicates a Condition, Observation, AllergyIntolerance, or QuestionnaireResponse that justifies this family member history event.")
    note: Optional[list[Annotation]] = Field(default=None, description="This property allows a non condition-specific note to the made about the related person. Ideally, the note would be in the condition property, but this is not always possible.")
    condition: Optional[list[FamilyMemberHistoryCondition]] = Field(default=None, description="The significant Conditions (or condition) that the family member had. This is a repeating section to allow a system to represent more than one condition per resource, though there is nothing stopping multiple resources - one per condition.")


class FamilyMemberHistoryCondition(MedplumFHIRBase):
    """The significant Conditions (or condition) that the family member had.
    This is a repeating section to allow a system to represent more than one
    condition per resource, though there is nothing stopping multiple
    resources - one per condition.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: CodeableConcept = Field(default=..., description="The actual condition specified. Could be a coded condition (like MI or Diabetes) or a less specific string like 'cancer' depending on how much is known about the condition and the capabilities of the creating system.")
    outcome: Optional[CodeableConcept] = Field(default=None, description="Indicates what happened following the condition. If the condition resulted in death, deceased date is captured on the relation.")
    contributed_to_death: Optional[bool] = Field(default=None, alias="contributedToDeath", description="This condition contributed to the cause of death of the related person. If contributedToDeath is not populated, then it is unknown.")
    onset_age: Optional[Age] = Field(default=None, alias="onsetAge", description="Either the age of onset, range of approximate age or descriptive string can be recorded. For conditions with multiple occurrences, this describes the first known occurrence.")
    onset_range: Optional[Range] = Field(default=None, alias="onsetRange", description="Either the age of onset, range of approximate age or descriptive string can be recorded. For conditions with multiple occurrences, this describes the first known occurrence.")
    onset_period: Optional[Period] = Field(default=None, alias="onsetPeriod", description="Either the age of onset, range of approximate age or descriptive string can be recorded. For conditions with multiple occurrences, this describes the first known occurrence.")
    onset_string: Optional[str] = Field(default=None, alias="onsetString", description="Either the age of onset, range of approximate age or descriptive string can be recorded. For conditions with multiple occurrences, this describes the first known occurrence.")
    note: Optional[list[Annotation]] = Field(default=None, description="An area where general notes can be placed about this specific condition.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("FamilyMemberHistory", FamilyMemberHistory)
    register_model("FamilyMemberHistoryCondition", FamilyMemberHistoryCondition)
