# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Encounter(MedplumFHIRBase):
    """An interaction between a patient and healthcare provider(s) for the
    purpose of providing healthcare service(s) or assessing the health
    status of a patient.
    """

    resource_type: Literal["Encounter"] = Field(
        default="Encounter",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[List[Identifier]] = Field(default=None, description="Identifier(s) by which this encounter is known.")
    status: Literal['planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown'] = Field(default=..., description="planned | arrived | triaged | in-progress | onleave | finished | cancelled +.")
    status_history: Optional[List[EncounterStatusHistory]] = Field(default=None, alias="statusHistory", description="The status history permits the encounter resource to contain the status history without needing to read through the historical versions of the resource, or even have the server store them.")
    class_: Coding = Field(default=..., alias="class", description="Concepts representing classification of patient encounter such as ambulatory (outpatient), inpatient, emergency, home health or others due to local variations.")
    class_history: Optional[List[EncounterClassHistory]] = Field(default=None, alias="classHistory", description="The class history permits the tracking of the encounters transitions without needing to go through the resource history. This would be used for a case where an admission starts of as an emergency encounter, then transitions into an inpatient scenario. Doing this and not restarting a new encounter ensures that any lab/diagnostic results can more easily follow the patient and not require re-processing and not get lost or cancelled during a kind of discharge from emergency to inpatient.")
    type: Optional[List[CodeableConcept]] = Field(default=None, description="Specific type of encounter (e.g. e-mail consultation, surgical day-care, skilled nursing, rehabilitation).")
    service_type: Optional[CodeableConcept] = Field(default=None, alias="serviceType", description="Broad categorization of the service that is to be provided (e.g. cardiology).")
    priority: Optional[CodeableConcept] = Field(default=None, description="Indicates the urgency of the encounter.")
    subject: Optional[Reference] = Field(default=None, description="The patient or group present at the encounter.")
    episode_of_care: Optional[List[Reference]] = Field(default=None, alias="episodeOfCare", description="Where a specific encounter should be classified as a part of a specific episode(s) of care this field should be used. This association can facilitate grouping of related encounters together for a specific purpose, such as government reporting, issue tracking, association via a common problem. The association is recorded on the encounter as these are typically created after the episode of care and grouped on entry rather than editing the episode of care to append another encounter to it (the episode of care could span years).")
    based_on: Optional[List[Reference]] = Field(default=None, alias="basedOn", description="The request this encounter satisfies (e.g. incoming referral or procedure request).")
    participant: Optional[List[EncounterParticipant]] = Field(default=None, description="The list of people responsible for providing the service.")
    appointment: Optional[List[Reference]] = Field(default=None, description="The appointment that scheduled this encounter.")
    period: Optional[Period] = Field(default=None, description="The start and end time of the encounter.")
    length: Optional[Duration] = Field(default=None, description="Quantity of time the encounter lasted. This excludes the time during leaves of absence.")
    reason_code: Optional[List[CodeableConcept]] = Field(default=None, alias="reasonCode", description="Reason the encounter takes place, expressed as a code. For admissions, this can be used for a coded admission diagnosis.")
    reason_reference: Optional[List[Reference]] = Field(default=None, alias="reasonReference", description="Reason the encounter takes place, expressed as a code. For admissions, this can be used for a coded admission diagnosis.")
    diagnosis: Optional[List[EncounterDiagnosis]] = Field(default=None, description="The list of diagnosis relevant to this encounter.")
    account: Optional[List[Reference]] = Field(default=None, description="The set of accounts that may be used for billing for this Encounter.")
    hospitalization: Optional[EncounterHospitalization] = Field(default=None, description="Details about the admission to a healthcare service.")
    location: Optional[List[EncounterLocation]] = Field(default=None, description="List of locations where the patient has been during this encounter.")
    service_provider: Optional[Reference] = Field(default=None, alias="serviceProvider", description="The organization that is primarily responsible for this Encounter's services. This MAY be the same as the organization on the Patient record, however it could be different, such as if the actor performing the services was from an external organization (which may be billed seperately) for an external consultation. Refer to the example bundle showing an abbreviated set of Encounters for a colonoscopy.")
    part_of: Optional[Reference] = Field(default=None, alias="partOf", description="Another Encounter of which this encounter is a part of (administratively or in time).")


class EncounterClassHistory(MedplumFHIRBase):
    """The class history permits the tracking of the encounters transitions
    without needing to go through the resource history. This would be used
    for a case where an admission starts of as an emergency encounter, then
    transitions into an inpatient scenario. Doing this and not restarting a
    new encounter ensures that any lab/diagnostic results can more easily
    follow the patient and not require re-processing and not get lost or
    cancelled during a kind of discharge from emergency to inpatient.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    class_: Coding = Field(default=..., alias="class", description="inpatient | outpatient | ambulatory | emergency +.")
    period: Period = Field(default=..., description="The time that the episode was in the specified class.")


class EncounterDiagnosis(MedplumFHIRBase):
    """The list of diagnosis relevant to this encounter."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    condition: Reference = Field(default=..., description="Reason the encounter takes place, as specified using information from another resource. For admissions, this is the admission diagnosis. The indication will typically be a Condition (with other resources referenced in the evidence.detail), or a Procedure.")
    use: Optional[CodeableConcept] = Field(default=None, description="Role that this diagnosis has within the encounter (e.g. admission, billing, discharge &hellip;).")
    rank: Optional[Union[int, float]] = Field(default=None, description="Ranking of the diagnosis (for each role type).")


class EncounterHospitalization(MedplumFHIRBase):
    """Details about the admission to a healthcare service."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    pre_admission_identifier: Optional[Identifier] = Field(default=None, alias="preAdmissionIdentifier", description="Pre-admission identifier.")
    origin: Optional[Reference] = Field(default=None, description="The location/organization from which the patient came before admission.")
    admit_source: Optional[CodeableConcept] = Field(default=None, alias="admitSource", description="From where patient was admitted (physician referral, transfer).")
    re_admission: Optional[CodeableConcept] = Field(default=None, alias="reAdmission", description="Whether this hospitalization is a readmission and why if known.")
    diet_preference: Optional[List[CodeableConcept]] = Field(default=None, alias="dietPreference", description="Diet preferences reported by the patient.")
    special_courtesy: Optional[List[CodeableConcept]] = Field(default=None, alias="specialCourtesy", description="Special courtesies (VIP, board member).")
    special_arrangement: Optional[List[CodeableConcept]] = Field(default=None, alias="specialArrangement", description="Any special requests that have been made for this hospitalization encounter, such as the provision of specific equipment or other things.")
    destination: Optional[Reference] = Field(default=None, description="Location/organization to which the patient is discharged.")
    discharge_disposition: Optional[CodeableConcept] = Field(default=None, alias="dischargeDisposition", description="Category or kind of location after discharge.")


class EncounterLocation(MedplumFHIRBase):
    """List of locations where the patient has been during this encounter."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    location: Reference = Field(default=..., description="The location where the encounter takes place.")
    status: Optional[Literal['planned', 'active', 'reserved', 'completed']] = Field(default=None, description="The status of the participants' presence at the specified location during the period specified. If the participant is no longer at the location, then the period will have an end date/time.")
    physical_type: Optional[CodeableConcept] = Field(default=None, alias="physicalType", description="This will be used to specify the required levels (bed/ward/room/etc.) desired to be recorded to simplify either messaging or query.")
    period: Optional[Period] = Field(default=None, description="Time period during which the patient was present at the location.")


class EncounterParticipant(MedplumFHIRBase):
    """The list of people responsible for providing the service."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: Optional[List[CodeableConcept]] = Field(default=None, description="Role of participant in encounter.")
    period: Optional[Period] = Field(default=None, description="The period of time that the specified participant participated in the encounter. These can overlap or be sub-sets of the overall encounter's period.")
    individual: Optional[Reference] = Field(default=None, description="Persons involved in the encounter other than the patient.")


class EncounterStatusHistory(MedplumFHIRBase):
    """The status history permits the encounter resource to contain the status
    history without needing to read through the historical versions of the
    resource, or even have the server store them.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    status: Literal['planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown'] = Field(default=..., description="planned | arrived | triaged | in-progress | onleave | finished | cancelled +.")
    period: Period = Field(default=..., description="The time that the episode was in the specified status.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Encounter", Encounter)
    register_model("EncounterClassHistory", EncounterClassHistory)
    register_model("EncounterDiagnosis", EncounterDiagnosis)
    register_model("EncounterHospitalization", EncounterHospitalization)
    register_model("EncounterLocation", EncounterLocation)
    register_model("EncounterParticipant", EncounterParticipant)
    register_model("EncounterStatusHistory", EncounterStatusHistory)
