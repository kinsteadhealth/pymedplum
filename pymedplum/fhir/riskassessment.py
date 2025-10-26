# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class RiskAssessment(MedplumFHIRBase):
    """An assessment of the likely outcome(s) for a patient or other subject as
    well as the likelihood of each outcome.
    """

    resource_type: Literal["RiskAssessment"] = Field(
        default="RiskAssessment",
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
    identifier: Optional[List[Identifier]] = Field(default=None, description="Business identifier assigned to the risk assessment.")
    based_on: Optional[Reference] = Field(default=None, alias="basedOn", description="A reference to the request that is fulfilled by this risk assessment.")
    parent: Optional[Reference] = Field(default=None, description="A reference to a resource that this risk assessment is part of, such as a Procedure.")
    status: Literal['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown'] = Field(default=..., description="The status of the RiskAssessment, using the same statuses as an Observation.")
    method: Optional[CodeableConcept] = Field(default=None, description="The algorithm, process or mechanism used to evaluate the risk.")
    code: Optional[CodeableConcept] = Field(default=None, description="The type of the risk assessment performed.")
    subject: Reference = Field(default=..., description="The patient or group the risk assessment applies to.")
    encounter: Optional[Reference] = Field(default=None, description="The encounter where the assessment was performed.")
    occurrence_date_time: Optional[str] = Field(default=None, alias="occurrenceDateTime", description="The date (and possibly time) the risk assessment was performed.")
    occurrence_period: Optional[Period] = Field(default=None, alias="occurrencePeriod", description="The date (and possibly time) the risk assessment was performed.")
    condition: Optional[Reference] = Field(default=None, description="For assessments or prognosis specific to a particular condition, indicates the condition being assessed.")
    performer: Optional[Reference] = Field(default=None, description="The provider or software application that performed the assessment.")
    reason_code: Optional[List[CodeableConcept]] = Field(default=None, alias="reasonCode", description="The reason the risk assessment was performed.")
    reason_reference: Optional[List[Reference]] = Field(default=None, alias="reasonReference", description="Resources supporting the reason the risk assessment was performed.")
    basis: Optional[List[Reference]] = Field(default=None, description="Indicates the source data considered as part of the assessment (for example, FamilyHistory, Observations, Procedures, Conditions, etc.).")
    prediction: Optional[List[RiskAssessmentPrediction]] = Field(default=None, description="Describes the expected outcome for the subject.")
    mitigation: Optional[str] = Field(default=None, description="A description of the steps that might be taken to reduce the identified risk(s).")
    note: Optional[List[Annotation]] = Field(default=None, description="Additional comments about the risk assessment.")


class RiskAssessmentPrediction(MedplumFHIRBase):
    """Describes the expected outcome for the subject."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    outcome: Optional[CodeableConcept] = Field(default=None, description="One of the potential outcomes for the patient (e.g. remission, death, a particular condition).")
    probability_decimal: Optional[Union[int, float]] = Field(default=None, alias="probabilityDecimal", description="Indicates how likely the outcome is (in the specified timeframe).")
    probability_range: Optional[Range] = Field(default=None, alias="probabilityRange", description="Indicates how likely the outcome is (in the specified timeframe).")
    qualitative_risk: Optional[CodeableConcept] = Field(default=None, alias="qualitativeRisk", description="Indicates how likely the outcome is (in the specified timeframe), expressed as a qualitative value (e.g. low, medium, or high).")
    relative_risk: Optional[Union[int, float]] = Field(default=None, alias="relativeRisk", description="Indicates the risk for this particular subject (with their specific characteristics) divided by the risk of the population in general. (Numbers greater than 1 = higher risk than the population, numbers less than 1 = lower risk.).")
    when_period: Optional[Period] = Field(default=None, alias="whenPeriod", description="Indicates the period of time or age range of the subject to which the specified probability applies.")
    when_range: Optional[Range] = Field(default=None, alias="whenRange", description="Indicates the period of time or age range of the subject to which the specified probability applies.")
    rationale: Optional[str] = Field(default=None, description="Additional information explaining the basis for the prediction.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("RiskAssessment", RiskAssessment)
    register_model("RiskAssessmentPrediction", RiskAssessmentPrediction)
