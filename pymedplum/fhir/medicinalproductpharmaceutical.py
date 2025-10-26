# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference


class MedicinalProductPharmaceutical(MedplumFHIRBase):
    """A pharmaceutical product described in terms of its composition and dose form."""

    resource_type: Literal["MedicinalProductPharmaceutical"] = Field(
        default="MedicinalProductPharmaceutical", alias="resourceType"
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
        description="An identifier for the pharmaceutical medicinal product.",
    )
    administrable_dose_form: CodeableConcept = Field(
        default=...,
        alias="administrableDoseForm",
        description="The administrable dose form, after necessary reconstitution.",
    )
    unit_of_presentation: CodeableConcept | None = Field(
        default=None, alias="unitOfPresentation", description="Todo."
    )
    ingredient: list[Reference] | None = Field(default=None, description="Ingredient.")
    device: list[Reference] | None = Field(
        default=None, description="Accompanying device."
    )
    characteristics: list[MedicinalProductPharmaceuticalCharacteristics] | None = Field(
        default=None, description="Characteristics e.g. a products onset of action."
    )
    route_of_administration: list[
        MedicinalProductPharmaceuticalRouteOfAdministration
    ] = Field(
        default=...,
        alias="routeOfAdministration",
        description="The path by which the pharmaceutical product is taken into or makes contact with the body.",
    )


class MedicinalProductPharmaceuticalCharacteristics(MedplumFHIRBase):
    """Characteristics e.g. a products onset of action."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: CodeableConcept = Field(default=..., description="A coded characteristic.")
    status: CodeableConcept | None = Field(
        default=None,
        description="The status of characteristic e.g. assigned or pending.",
    )


class MedicinalProductPharmaceuticalRouteOfAdministration(MedplumFHIRBase):
    """The path by which the pharmaceutical product is taken into or makes
    contact with the body.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: CodeableConcept = Field(
        default=..., description="Coded expression for the route."
    )
    first_dose: Quantity | None = Field(
        default=None,
        alias="firstDose",
        description="The first dose (dose quantity) administered in humans can be specified, for a product under investigation, using a numerical value and its unit of measurement.",
    )
    max_single_dose: Quantity | None = Field(
        default=None,
        alias="maxSingleDose",
        description="The maximum single dose that can be administered as per the protocol of a clinical trial can be specified using a numerical value and its unit of measurement.",
    )
    max_dose_per_day: Quantity | None = Field(
        default=None,
        alias="maxDosePerDay",
        description="The maximum dose per day (maximum dose quantity to be administered in any one 24-h period) that can be administered as per the protocol referenced in the clinical trial authorisation.",
    )
    max_dose_per_treatment_period: Ratio | None = Field(
        default=None,
        alias="maxDosePerTreatmentPeriod",
        description="The maximum dose per treatment period that can be administered as per the protocol referenced in the clinical trial authorisation.",
    )
    max_treatment_period: Duration | None = Field(
        default=None,
        alias="maxTreatmentPeriod",
        description="The maximum treatment period during which an Investigational Medicinal Product can be administered as per the protocol referenced in the clinical trial authorisation.",
    )
    target_species: (
        list[MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies] | None
    ) = Field(
        default=None,
        alias="targetSpecies",
        description="A species for which this route applies.",
    )


class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies(MedplumFHIRBase):
    """A species for which this route applies."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: CodeableConcept = Field(
        default=..., description="Coded expression for the species."
    )
    withdrawal_period: (
        list[
            MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod
        ]
        | None
    ) = Field(
        default=None,
        alias="withdrawalPeriod",
        description="A species specific time during which consumption of animal product is not appropriate.",
    )


class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod(
    MedplumFHIRBase
):
    """A species specific time during which consumption of animal product is
    not appropriate.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    tissue: CodeableConcept = Field(
        default=...,
        description="Coded expression for the type of tissue for which the withdrawal period applues, e.g. meat, milk.",
    )
    value: Quantity = Field(default=..., description="A value for the time.")
    supporting_information: str | None = Field(
        default=None,
        alias="supportingInformation",
        description="Extra information about the withdrawal period.",
    )
