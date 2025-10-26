# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class ImmunizationEvaluation(MedplumFHIRBase):
    """Describes a comparison of an immunization event against published
    recommendations to determine if the administration is &quot;valid&quot;
    in relation to those recommendations.
    """

    resource_type: Literal["ImmunizationEvaluation"] = Field(
        default="ImmunizationEvaluation", alias="resourceType"
    )

    id: str | None = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Meta | None = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: str | None = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: str | None = Field(
        default=None, description="The base language in which the resource is written."
    )
    text: Narrative | None = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: list[dict[str, Any]] | None = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="A unique identifier assigned to this immunization evaluation record.",
    )
    status: Literal["completed", "entered-in-error"] = Field(
        default=...,
        description="Indicates the current status of the evaluation of the vaccination administration event.",
    )
    patient: Reference = Field(
        default=..., description="The individual for whom the evaluation is being done."
    )
    date: str | None = Field(
        default=None,
        description="The date the evaluation of the vaccine administration event was performed.",
    )
    authority: Reference | None = Field(
        default=None,
        description="Indicates the authority who published the protocol (e.g. ACIP).",
    )
    target_disease: CodeableConcept = Field(
        default=...,
        alias="targetDisease",
        description="The vaccine preventable disease the dose is being evaluated against.",
    )
    immunization_event: Reference = Field(
        default=...,
        alias="immunizationEvent",
        description="The vaccine administration event being evaluated.",
    )
    dose_status: CodeableConcept = Field(
        default=...,
        alias="doseStatus",
        description="Indicates if the dose is valid or not valid with respect to the published recommendations.",
    )
    dose_status_reason: list[CodeableConcept] | None = Field(
        default=None,
        alias="doseStatusReason",
        description="Provides an explanation as to why the vaccine administration event is valid or not relative to the published recommendations.",
    )
    description: str | None = Field(
        default=None, description="Additional information about the evaluation."
    )
    series: str | None = Field(
        default=None,
        description="One possible path to achieve presumed immunity against a disease - within the context of an authority.",
    )
    dose_number_positive_int: int | float | None = Field(
        default=None,
        alias="doseNumberPositiveInt",
        description="Nominal position in a series.",
    )
    dose_number_string: str | None = Field(
        default=None,
        alias="doseNumberString",
        description="Nominal position in a series.",
    )
    series_doses_positive_int: int | float | None = Field(
        default=None,
        alias="seriesDosesPositiveInt",
        description="The recommended number of doses to achieve immunity.",
    )
    series_doses_string: str | None = Field(
        default=None,
        alias="seriesDosesString",
        description="The recommended number of doses to achieve immunity.",
    )
