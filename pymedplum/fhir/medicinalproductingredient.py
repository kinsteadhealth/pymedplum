# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

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
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference


class MedicinalProductIngredient(MedplumFHIRBase):
    """An ingredient of a manufactured item or pharmaceutical product."""

    resource_type: Literal["MedicinalProductIngredient"] = Field(
        default="MedicinalProductIngredient", alias="resourceType"
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
    identifier: Identifier | None = Field(
        default=None,
        description="The identifier(s) of this Ingredient that are assigned by business processes and/or used to refer to it when a direct URL reference to the resource itself is not appropriate.",
    )
    role: CodeableConcept = Field(
        default=..., description="Ingredient role e.g. Active ingredient, excipient."
    )
    allergenic_indicator: bool | None = Field(
        default=None,
        alias="allergenicIndicator",
        description="If the ingredient is a known or suspected allergen.",
    )
    manufacturer: list[Reference] | None = Field(
        default=None, description="Manufacturer of this Ingredient."
    )
    specified_substance: list[MedicinalProductIngredientSpecifiedSubstance] | None = (
        Field(
            default=None,
            alias="specifiedSubstance",
            description="A specified substance that comprises this ingredient.",
        )
    )
    substance: MedicinalProductIngredientSubstance | None = Field(
        default=None, description="The ingredient substance."
    )


class MedicinalProductIngredientSpecifiedSubstance(MedplumFHIRBase):
    """A specified substance that comprises this ingredient."""

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
    code: CodeableConcept = Field(default=..., description="The specified substance.")
    group: CodeableConcept = Field(
        default=..., description="The group of specified substance, e.g. group 1 to 4."
    )
    confidentiality: CodeableConcept | None = Field(
        default=None,
        description="Confidentiality level of the specified substance as the ingredient.",
    )
    strength: list[MedicinalProductIngredientSpecifiedSubstanceStrength] | None = Field(
        default=None,
        description="Quantity of the substance or specified substance present in the manufactured item or pharmaceutical product.",
    )


class MedicinalProductIngredientSpecifiedSubstanceStrength(MedplumFHIRBase):
    """Quantity of the substance or specified substance present in the
    manufactured item or pharmaceutical product.
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
    presentation: Ratio = Field(
        default=...,
        description="The quantity of substance in the unit of presentation, or in the volume (or mass) of the single pharmaceutical product or manufactured item.",
    )
    presentation_low_limit: Ratio | None = Field(
        default=None,
        alias="presentationLowLimit",
        description="A lower limit for the quantity of substance in the unit of presentation. For use when there is a range of strengths, this is the lower limit, with the presentation attribute becoming the upper limit.",
    )
    concentration: Ratio | None = Field(
        default=None, description="The strength per unitary volume (or mass)."
    )
    concentration_low_limit: Ratio | None = Field(
        default=None,
        alias="concentrationLowLimit",
        description="A lower limit for the strength per unitary volume (or mass), for when there is a range. The concentration attribute then becomes the upper limit.",
    )
    measurement_point: str | None = Field(
        default=None,
        alias="measurementPoint",
        description="For when strength is measured at a particular point or distance.",
    )
    country: list[CodeableConcept] | None = Field(
        default=None,
        description="The country or countries for which the strength range applies.",
    )
    reference_strength: (
        list[MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength]
        | None
    ) = Field(
        default=None,
        alias="referenceStrength",
        description="Strength expressed in terms of a reference substance.",
    )


class MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength(
    MedplumFHIRBase
):
    """Strength expressed in terms of a reference substance."""

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
    substance: CodeableConcept | None = Field(
        default=None, description="Relevant reference substance."
    )
    strength: Ratio = Field(
        default=..., description="Strength expressed in terms of a reference substance."
    )
    strength_low_limit: Ratio | None = Field(
        default=None,
        alias="strengthLowLimit",
        description="Strength expressed in terms of a reference substance.",
    )
    measurement_point: str | None = Field(
        default=None,
        alias="measurementPoint",
        description="For when strength is measured at a particular point or distance.",
    )
    country: list[CodeableConcept] | None = Field(
        default=None,
        description="The country or countries for which the strength range applies.",
    )


class MedicinalProductIngredientSubstance(MedplumFHIRBase):
    """The ingredient substance."""

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
    code: CodeableConcept = Field(default=..., description="The ingredient substance.")
    strength: list[MedicinalProductIngredientSpecifiedSubstanceStrength] | None = Field(
        default=None,
        description="Quantity of the substance or specified substance present in the manufactured item or pharmaceutical product.",
    )
