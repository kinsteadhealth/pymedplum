# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Observation(MedplumFHIRBase):
    """Measurements and simple assertions made about a patient, device or other subject."""

    resource_type: Literal["Observation"] = Field(
        default="Observation",
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
    identifier: Optional[List[Identifier]] = Field(default=None, description="A unique identifier assigned to this observation.")
    based_on: Optional[List[Reference]] = Field(default=None, alias="basedOn", description="A plan, proposal or order that is fulfilled in whole or in part by this event. For example, a MedicationRequest may require a patient to have laboratory test performed before it is dispensed.")
    part_of: Optional[List[Reference]] = Field(default=None, alias="partOf", description="A larger event of which this particular Observation is a component or step. For example, an observation as part of a procedure.")
    status: Literal['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown'] = Field(default=..., description="The status of the result value.")
    category: Optional[List[CodeableConcept]] = Field(default=None, description="A code that classifies the general type of observation being made.")
    code: CodeableConcept = Field(default=..., description="Describes what was observed. Sometimes this is called the observation &quot;name&quot;.")
    subject: Optional[Reference] = Field(default=None, description="The patient, or group of patients, location, or device this observation is about and into whose record the observation is placed. If the actual focus of the observation is different from the subject (or a sample of, part, or region of the subject), the `focus` element or the `code` itself specifies the actual focus of the observation.")
    focus: Optional[List[Reference]] = Field(default=None, description="The actual focus of an observation when it is not the patient of record representing something or someone associated with the patient such as a spouse, parent, fetus, or donor. For example, fetus observations in a mother's record. The focus of an observation could also be an existing condition, an intervention, the subject's diet, another observation of the subject, or a body structure such as tumor or implanted device. An example use case would be using the Observation resource to capture whether the mother is trained to change her child's tracheostomy tube. In this example, the child is the patient of record and the mother is the focus.")
    encounter: Optional[Reference] = Field(default=None, description="The healthcare event (e.g. a patient and healthcare provider interaction) during which this observation is made.")
    effective_date_time: Optional[str] = Field(default=None, alias="effectiveDateTime", description="The time or time-period the observed value is asserted as being true. For biological subjects - e.g. human patients - this is usually called the &quot;physiologically relevant time&quot;. This is usually either the time of the procedure or of specimen collection, but very often the source of the date/time is not known, only the date/time itself.")
    effective_period: Optional[Period] = Field(default=None, alias="effectivePeriod", description="The time or time-period the observed value is asserted as being true. For biological subjects - e.g. human patients - this is usually called the &quot;physiologically relevant time&quot;. This is usually either the time of the procedure or of specimen collection, but very often the source of the date/time is not known, only the date/time itself.")
    effective_timing: Optional[Timing] = Field(default=None, alias="effectiveTiming", description="The time or time-period the observed value is asserted as being true. For biological subjects - e.g. human patients - this is usually called the &quot;physiologically relevant time&quot;. This is usually either the time of the procedure or of specimen collection, but very often the source of the date/time is not known, only the date/time itself.")
    effective_instant: Optional[str] = Field(default=None, alias="effectiveInstant", description="The time or time-period the observed value is asserted as being true. For biological subjects - e.g. human patients - this is usually called the &quot;physiologically relevant time&quot;. This is usually either the time of the procedure or of specimen collection, but very often the source of the date/time is not known, only the date/time itself.")
    issued: Optional[str] = Field(default=None, description="The date and time this version of the observation was made available to providers, typically after the results have been reviewed and verified.")
    performer: Optional[List[Reference]] = Field(default=None, description="Who was responsible for asserting the observed value as &quot;true&quot;.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_string: Optional[str] = Field(default=None, alias="valueString", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_integer: Optional[Union[int, float]] = Field(default=None, alias="valueInteger", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_ratio: Optional[Ratio] = Field(default=None, alias="valueRatio", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_sampled_data: Optional[SampledData] = Field(default=None, alias="valueSampledData", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_time: Optional[str] = Field(default=None, alias="valueTime", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_date_time: Optional[str] = Field(default=None, alias="valueDateTime", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_period: Optional[Period] = Field(default=None, alias="valuePeriod", description="The information determined as a result of making the observation, if the information has a simple value.")
    data_absent_reason: Optional[CodeableConcept] = Field(default=None, alias="dataAbsentReason", description="Provides a reason why the expected value in the element Observation.value[x] is missing.")
    interpretation: Optional[List[CodeableConcept]] = Field(default=None, description="A categorical assessment of an observation value. For example, high, low, normal.")
    note: Optional[List[Annotation]] = Field(default=None, description="Comments about the observation or the results.")
    body_site: Optional[CodeableConcept] = Field(default=None, alias="bodySite", description="Indicates the site on the subject's body where the observation was made (i.e. the target site).")
    method: Optional[CodeableConcept] = Field(default=None, description="Indicates the mechanism used to perform the observation.")
    specimen: Optional[Reference] = Field(default=None, description="The specimen that was used when this observation was made.")
    device: Optional[Reference] = Field(default=None, description="The device used to generate the observation data.")
    reference_range: Optional[List[ObservationReferenceRange]] = Field(default=None, alias="referenceRange", description="Guidance on how to interpret the value by comparison to a normal or recommended range. Multiple reference ranges are interpreted as an &quot;OR&quot;. In other words, to represent two distinct target populations, two `referenceRange` elements would be used.")
    has_member: Optional[List[Reference]] = Field(default=None, alias="hasMember", description="This observation is a group observation (e.g. a battery, a panel of tests, a set of vital sign measurements) that includes the target as a member of the group.")
    derived_from: Optional[List[Reference]] = Field(default=None, alias="derivedFrom", description="The target resource that represents a measurement from which this observation value is derived. For example, a calculated anion gap or a fetal measurement based on an ultrasound image.")
    component: Optional[List[ObservationComponent]] = Field(default=None, description="Some observations have multiple component observations. These component observations are expressed as separate code value pairs that share the same attributes. Examples include systolic and diastolic component observations for blood pressure measurement and multiple component observations for genetics observations.")


class ObservationComponent(MedplumFHIRBase):
    """Some observations have multiple component observations. These component
    observations are expressed as separate code value pairs that share the
    same attributes. Examples include systolic and diastolic component
    observations for blood pressure measurement and multiple component
    observations for genetics observations.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: CodeableConcept = Field(default=..., description="Describes what was observed. Sometimes this is called the observation &quot;code&quot;.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_string: Optional[str] = Field(default=None, alias="valueString", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_integer: Optional[Union[int, float]] = Field(default=None, alias="valueInteger", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_ratio: Optional[Ratio] = Field(default=None, alias="valueRatio", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_sampled_data: Optional[SampledData] = Field(default=None, alias="valueSampledData", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_time: Optional[str] = Field(default=None, alias="valueTime", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_date_time: Optional[str] = Field(default=None, alias="valueDateTime", description="The information determined as a result of making the observation, if the information has a simple value.")
    value_period: Optional[Period] = Field(default=None, alias="valuePeriod", description="The information determined as a result of making the observation, if the information has a simple value.")
    data_absent_reason: Optional[CodeableConcept] = Field(default=None, alias="dataAbsentReason", description="Provides a reason why the expected value in the element Observation.component.value[x] is missing.")
    interpretation: Optional[List[CodeableConcept]] = Field(default=None, description="A categorical assessment of an observation value. For example, high, low, normal.")
    reference_range: Optional[List[ObservationReferenceRange]] = Field(default=None, alias="referenceRange", description="Guidance on how to interpret the value by comparison to a normal or recommended range.")


class ObservationReferenceRange(MedplumFHIRBase):
    """Guidance on how to interpret the value by comparison to a normal or
    recommended range. Multiple reference ranges are interpreted as an
    &quot;OR&quot;. In other words, to represent two distinct target
    populations, two `referenceRange` elements would be used.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    low: Optional[Quantity] = Field(default=None, description="The value of the low bound of the reference range. The low bound of the reference range endpoint is inclusive of the value (e.g. reference range is &gt;=5 - &lt;=9). If the low bound is omitted, it is assumed to be meaningless (e.g. reference range is &lt;=2.3).")
    high: Optional[Quantity] = Field(default=None, description="The value of the high bound of the reference range. The high bound of the reference range endpoint is inclusive of the value (e.g. reference range is &gt;=5 - &lt;=9). If the high bound is omitted, it is assumed to be meaningless (e.g. reference range is &gt;= 2.3).")
    type: Optional[CodeableConcept] = Field(default=None, description="Codes to indicate the what part of the targeted reference population it applies to. For example, the normal or therapeutic range.")
    applies_to: Optional[List[CodeableConcept]] = Field(default=None, alias="appliesTo", description="Codes to indicate the target population this reference range applies to. For example, a reference range may be based on the normal population or a particular sex or race. Multiple `appliesTo` are interpreted as an &quot;AND&quot; of the target populations. For example, to represent a target population of African American females, both a code of female and a code for African American would be used.")
    age: Optional[Range] = Field(default=None, description="The age at which this reference range is applicable. This is a neonatal age (e.g. number of weeks at term) if the meaning says so.")
    text: Optional[str] = Field(default=None, description="Text based reference range in an observation which may be used when a quantitative range is not appropriate for an observation. An example would be a reference value of &quot;Negative&quot; or a list or table of &quot;normals&quot;.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Observation", Observation)
    register_model("ObservationComponent", ObservationComponent)
    register_model("ObservationReferenceRange", ObservationReferenceRange)
