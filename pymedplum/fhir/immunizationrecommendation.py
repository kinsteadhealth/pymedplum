# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class ImmunizationRecommendation(MedplumFHIRBase):
    """A patient's point-in-time set of recommendations (i.e. forecasting)
    according to a published schedule with optional supporting
    justification.
    """

    resource_type: Literal["ImmunizationRecommendation"] = Field(
        default="ImmunizationRecommendation",
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
    identifier: Optional[List[Identifier]] = Field(default=None, description="A unique identifier assigned to this particular recommendation record.")
    patient: Reference = Field(default=..., description="The patient the recommendation(s) are for.")
    date: str = Field(default=..., description="The date the immunization recommendation(s) were created.")
    authority: Optional[Reference] = Field(default=None, description="Indicates the authority who published the protocol (e.g. ACIP).")
    recommendation: List[ImmunizationRecommendationRecommendation] = Field(default=..., description="Vaccine administration recommendations.")


class ImmunizationRecommendationRecommendation(MedplumFHIRBase):
    """Vaccine administration recommendations."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    vaccine_code: Optional[List[CodeableConcept]] = Field(default=None, alias="vaccineCode", description="Vaccine(s) or vaccine group that pertain to the recommendation.")
    target_disease: Optional[CodeableConcept] = Field(default=None, alias="targetDisease", description="The targeted disease for the recommendation.")
    contraindicated_vaccine_code: Optional[List[CodeableConcept]] = Field(default=None, alias="contraindicatedVaccineCode", description="Vaccine(s) which should not be used to fulfill the recommendation.")
    forecast_status: CodeableConcept = Field(default=..., alias="forecastStatus", description="Indicates the patient status with respect to the path to immunity for the target disease.")
    forecast_reason: Optional[List[CodeableConcept]] = Field(default=None, alias="forecastReason", description="The reason for the assigned forecast status.")
    date_criterion: Optional[List[ImmunizationRecommendationRecommendationDateCriterion]] = Field(default=None, alias="dateCriterion", description="Vaccine date recommendations. For example, earliest date to administer, latest date to administer, etc.")
    description: Optional[str] = Field(default=None, description="Contains the description about the protocol under which the vaccine was administered.")
    series: Optional[str] = Field(default=None, description="One possible path to achieve presumed immunity against a disease - within the context of an authority.")
    dose_number_positive_int: Optional[Union[int, float]] = Field(default=None, alias="doseNumberPositiveInt", description="Nominal position of the recommended dose in a series (e.g. dose 2 is the next recommended dose).")
    dose_number_string: Optional[str] = Field(default=None, alias="doseNumberString", description="Nominal position of the recommended dose in a series (e.g. dose 2 is the next recommended dose).")
    series_doses_positive_int: Optional[Union[int, float]] = Field(default=None, alias="seriesDosesPositiveInt", description="The recommended number of doses to achieve immunity.")
    series_doses_string: Optional[str] = Field(default=None, alias="seriesDosesString", description="The recommended number of doses to achieve immunity.")
    supporting_immunization: Optional[List[Reference]] = Field(default=None, alias="supportingImmunization", description="Immunization event history and/or evaluation that supports the status and recommendation.")
    supporting_patient_information: Optional[List[Reference]] = Field(default=None, alias="supportingPatientInformation", description="Patient Information that supports the status and recommendation. This includes patient observations, adverse reactions and allergy/intolerance information.")


class ImmunizationRecommendationRecommendationDateCriterion(MedplumFHIRBase):
    """Vaccine date recommendations. For example, earliest date to administer,
    latest date to administer, etc.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: CodeableConcept = Field(default=..., description="Date classification of recommendation. For example, earliest date to give, latest date to give, etc.")
    value: str = Field(default=..., description="The date whose meaning is specified by dateCriterion.code.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ImmunizationRecommendation", ImmunizationRecommendation)
    register_model("ImmunizationRecommendationRecommendation", ImmunizationRecommendationRecommendation)
    register_model("ImmunizationRecommendationRecommendationDateCriterion", ImmunizationRecommendationRecommendationDateCriterion)
