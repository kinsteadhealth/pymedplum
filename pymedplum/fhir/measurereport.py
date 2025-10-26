# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class MeasureReport(MedplumFHIRBase):
    """The MeasureReport resource contains the results of the calculation of a
    measure; and optionally a reference to the resources involved in that
    calculation.
    """

    resource_type: Literal["MeasureReport"] = Field(
        default="MeasureReport",
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
    identifier: Optional[List[Identifier]] = Field(default=None, description="A formal identifier that is used to identify this MeasureReport when it is represented in other formats or referenced in a specification, model, design or an instance.")
    status: Literal['complete', 'pending', 'error'] = Field(default=..., description="The MeasureReport status. No data will be available until the MeasureReport status is complete.")
    type: Literal['individual', 'subject-list', 'summary', 'data-collection'] = Field(default=..., description="The type of measure report. This may be an individual report, which provides the score for the measure for an individual member of the population; a subject-listing, which returns the list of members that meet the various criteria in the measure; a summary report, which returns a population count for each of the criteria in the measure; or a data-collection, which enables the MeasureReport to be used to exchange the data-of-interest for a quality measure.")
    measure: str = Field(default=..., description="A reference to the Measure that was calculated to produce this report.")
    subject: Optional[Reference] = Field(default=None, description="Optional subject identifying the individual or individuals the report is for.")
    date: Optional[str] = Field(default=None, description="The date this measure report was generated.")
    reporter: Optional[Reference] = Field(default=None, description="The individual, location, or organization that is reporting the data.")
    period: Period = Field(default=..., description="The reporting period for which the report was calculated.")
    improvement_notation: Optional[CodeableConcept] = Field(default=None, alias="improvementNotation", description="Whether improvement in the measure is noted by an increase or decrease in the measure score.")
    group: Optional[List[MeasureReportGroup]] = Field(default=None, description="The results of the calculation, one for each population group in the measure.")
    evaluated_resource: Optional[List[Reference]] = Field(default=None, alias="evaluatedResource", description="A reference to a Bundle containing the Resources that were used in the calculation of this measure.")


class MeasureReportGroup(MedplumFHIRBase):
    """The results of the calculation, one for each population group in the measure."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="The meaning of the population group as defined in the measure definition.")
    population: Optional[List[MeasureReportGroupPopulation]] = Field(default=None, description="The populations that make up the population group, one for each type of population appropriate for the measure.")
    measure_score: Optional[Quantity] = Field(default=None, alias="measureScore", description="The measure score for this population group, calculated as appropriate for the measure type and scoring method, and based on the contents of the populations defined in the group.")
    stratifier: Optional[List[MeasureReportGroupStratifier]] = Field(default=None, description="When a measure includes multiple stratifiers, there will be a stratifier group for each stratifier defined by the measure.")


class MeasureReportGroupPopulation(MedplumFHIRBase):
    """The populations that make up the population group, one for each type of
    population appropriate for the measure.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="The type of the population.")
    count: Optional[Union[int, float]] = Field(default=None, description="The number of members of the population.")
    subject_results: Optional[Reference] = Field(default=None, alias="subjectResults", description="This element refers to a List of subject level MeasureReport resources, one for each subject in this population.")


class MeasureReportGroupStratifier(MedplumFHIRBase):
    """When a measure includes multiple stratifiers, there will be a stratifier
    group for each stratifier defined by the measure.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[List[CodeableConcept]] = Field(default=None, description="The meaning of this stratifier, as defined in the measure definition.")
    stratum: Optional[List[MeasureReportGroupStratifierStratum]] = Field(default=None, description="This element contains the results for a single stratum within the stratifier. For example, when stratifying on administrative gender, there will be four strata, one for each possible gender value.")


class MeasureReportGroupStratifierStratum(MedplumFHIRBase):
    """This element contains the results for a single stratum within the
    stratifier. For example, when stratifying on administrative gender,
    there will be four strata, one for each possible gender value.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    value: Optional[CodeableConcept] = Field(default=None, description="The value for this stratum, expressed as a CodeableConcept. When defining stratifiers on complex values, the value must be rendered such that the value for each stratum within the stratifier is unique.")
    component: Optional[List[MeasureReportGroupStratifierStratumComponent]] = Field(default=None, description="A stratifier component value.")
    population: Optional[List[MeasureReportGroupStratifierStratumPopulation]] = Field(default=None, description="The populations that make up the stratum, one for each type of population appropriate to the measure.")
    measure_score: Optional[Quantity] = Field(default=None, alias="measureScore", description="The measure score for this stratum, calculated as appropriate for the measure type and scoring method, and based on only the members of this stratum.")


class MeasureReportGroupStratifierStratumComponent(MedplumFHIRBase):
    """A stratifier component value."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: CodeableConcept = Field(default=..., description="The code for the stratum component value.")
    value: CodeableConcept = Field(default=..., description="The stratum component value.")


class MeasureReportGroupStratifierStratumPopulation(MedplumFHIRBase):
    """The populations that make up the stratum, one for each type of
    population appropriate to the measure.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="The type of the population.")
    count: Optional[Union[int, float]] = Field(default=None, description="The number of members of the population in this stratum.")
    subject_results: Optional[Reference] = Field(default=None, alias="subjectResults", description="This element refers to a List of subject level MeasureReport resources, one for each subject in this population in this stratum.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("MeasureReport", MeasureReport)
    register_model("MeasureReportGroup", MeasureReportGroup)
    register_model("MeasureReportGroupPopulation", MeasureReportGroupPopulation)
    register_model("MeasureReportGroupStratifier", MeasureReportGroupStratifier)
    register_model("MeasureReportGroupStratifierStratum", MeasureReportGroupStratifierStratum)
    register_model("MeasureReportGroupStratifierStratumComponent", MeasureReportGroupStratifierStratumComponent)
    register_model("MeasureReportGroupStratifierStratumPopulation", MeasureReportGroupStratifierStratumPopulation)
