# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ObservationDefinition(MedplumFHIRBase):
    """Set of definitional characteristics for a kind of observation or
    measurement produced or consumed by an orderable health care service.
    """

    resource_type: Literal["ObservationDefinition"] = Field(
        default="ObservationDefinition", alias="resourceType"
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
    publisher: Optional[Reference] = Field(
        default=None,
        description="Helps establish the &quot;authority/credibility&quot; of the ObservationDefinition. May also allow for contact.",
    )
    category: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A code that classifies the general type of observation.",
    )
    code: CodeableConcept = Field(
        default=...,
        description="Describes what will be observed. Sometimes this is called the observation &quot;name&quot;.",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="A unique identifier assigned to this ObservationDefinition artifact.",
    )
    permitted_data_type: Optional[
        list[
            Literal[
                "Quantity",
                "CodeableConcept",
                "string",
                "boolean",
                "integer",
                "Range",
                "Ratio",
                "SampledData",
                "time",
                "dateTime",
                "Period",
            ]
        ]
    ] = Field(
        default=None,
        alias="permittedDataType",
        description="The data types allowed for the value element of the instance observations conforming to this ObservationDefinition.",
    )
    multiple_results_allowed: Optional[bool] = Field(
        default=None,
        alias="multipleResultsAllowed",
        description="Multiple results allowed for observations conforming to this ObservationDefinition.",
    )
    method: Optional[CodeableConcept] = Field(
        default=None,
        description="The method or technique used to perform the observation.",
    )
    preferred_report_name: Optional[str] = Field(
        default=None,
        alias="preferredReportName",
        description="The preferred name to be used when reporting the results of observations conforming to this ObservationDefinition.",
    )
    quantitative_details: Optional[ObservationDefinitionQuantitativeDetails] = Field(
        default=None,
        alias="quantitativeDetails",
        description="Characteristics for quantitative results of this observation.",
    )
    qualified_interval: Optional[list[ObservationDefinitionQualifiedInterval]] = Field(
        default=None,
        alias="qualifiedInterval",
        description="Multiple ranges of results qualified by different contexts for ordinal or continuous observations conforming to this ObservationDefinition.",
    )
    valid_coded_value_set: Optional[Reference] = Field(
        default=None,
        alias="validCodedValueSet",
        description="The set of valid coded results for the observations conforming to this ObservationDefinition.",
    )
    normal_coded_value_set: Optional[Reference] = Field(
        default=None,
        alias="normalCodedValueSet",
        description="The set of normal coded results for the observations conforming to this ObservationDefinition.",
    )
    abnormal_coded_value_set: Optional[Reference] = Field(
        default=None,
        alias="abnormalCodedValueSet",
        description="The set of abnormal coded results for the observation conforming to this ObservationDefinition.",
    )
    critical_coded_value_set: Optional[Reference] = Field(
        default=None,
        alias="criticalCodedValueSet",
        description="The set of critical coded results for the observation conforming to this ObservationDefinition.",
    )


class ObservationDefinitionQualifiedInterval(MedplumFHIRBase):
    """Multiple ranges of results qualified by different contexts for ordinal
    or continuous observations conforming to this ObservationDefinition.
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
    category: Optional[Literal["reference", "critical", "absolute"]] = Field(
        default=None,
        description="The category of interval of values for continuous or ordinal observations conforming to this ObservationDefinition.",
    )
    range: Optional[Range] = Field(
        default=None,
        description="The low and high values determining the interval. There may be only one of the two.",
    )
    context: Optional[CodeableConcept] = Field(
        default=None,
        description="Codes to indicate the health context the range applies to. For example, the normal or therapeutic range.",
    )
    applies_to: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="appliesTo",
        description="Codes to indicate the target population this reference range applies to.",
    )
    gender: Optional[Literal["male", "female", "other", "unknown"]] = Field(
        default=None, description="Sex of the population the range applies to."
    )
    age: Optional[Range] = Field(
        default=None,
        description="The age at which this reference range is applicable. This is a neonatal age (e.g. number of weeks at term) if the meaning says so.",
    )
    gestational_age: Optional[Range] = Field(
        default=None,
        alias="gestationalAge",
        description="The gestational age to which this reference range is applicable, in the context of pregnancy.",
    )
    condition: Optional[str] = Field(
        default=None,
        description="Text based condition for which the reference range is valid.",
    )


class ObservationDefinitionQuantitativeDetails(MedplumFHIRBase):
    """Characteristics for quantitative results of this observation."""

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
    customary_unit: Optional[CodeableConcept] = Field(
        default=None,
        alias="customaryUnit",
        description="Customary unit used to report quantitative results of observations conforming to this ObservationDefinition.",
    )
    unit: Optional[CodeableConcept] = Field(
        default=None,
        description="SI unit used to report quantitative results of observations conforming to this ObservationDefinition.",
    )
    conversion_factor: Optional[Union[int, float]] = Field(
        default=None,
        alias="conversionFactor",
        description="Factor for converting value expressed with SI unit to value expressed with customary unit.",
    )
    decimal_precision: Optional[Union[int, float]] = Field(
        default=None,
        alias="decimalPrecision",
        description="Number of digits after decimal separator when the results of such observations are of type Quantity.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ObservationDefinition", ObservationDefinition)
    register_model(
        "ObservationDefinitionQualifiedInterval", ObservationDefinitionQualifiedInterval
    )
    register_model(
        "ObservationDefinitionQuantitativeDetails",
        ObservationDefinitionQuantitativeDetails,
    )
