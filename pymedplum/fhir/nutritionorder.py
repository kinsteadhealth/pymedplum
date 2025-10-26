# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.timing import Timing


class NutritionOrder(MedplumFHIRBase):
    """A request to supply a diet, formula feeding (enteral) or oral
    nutritional supplement to a patient/resident.
    """

    resource_type: Literal["NutritionOrder"] = Field(
        default="NutritionOrder", alias="resourceType"
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
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="Identifiers assigned to this order by the order sender or by the order receiver.",
    )
    instantiates_canonical: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this NutritionOrder.",
    )
    instantiates_uri: Optional[list[str]] = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this NutritionOrder.",
    )
    instantiates: Optional[list[str]] = Field(
        default=None,
        description="The URL pointing to a protocol, guideline, orderset or other definition that is adhered to in whole or in part by this NutritionOrder.",
    )
    status: Literal[
        "draft",
        "active",
        "on-hold",
        "revoked",
        "completed",
        "entered-in-error",
        "unknown",
    ] = Field(
        default=..., description="The workflow status of the nutrition order/request."
    )
    intent: Literal[
        "proposal",
        "plan",
        "directive",
        "order",
        "original-order",
        "reflex-order",
        "filler-order",
        "instance-order",
        "option",
    ] = Field(
        default=...,
        description="Indicates the level of authority/intentionality associated with the NutrionOrder and where the request fits into the workflow chain.",
    )
    patient: Reference = Field(
        default=...,
        description="The person (patient) who needs the nutrition order for an oral diet, nutritional supplement and/or enteral or formula feeding.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="An encounter that provides additional information about the healthcare context in which this request is made.",
    )
    date_time: str = Field(
        default=...,
        alias="dateTime",
        description="The date and time that this nutrition order was requested.",
    )
    orderer: Optional[Reference] = Field(
        default=None,
        description="The practitioner that holds legal responsibility for ordering the diet, nutritional supplement, or formula feedings.",
    )
    allergy_intolerance: Optional[list[Reference]] = Field(
        default=None,
        alias="allergyIntolerance",
        description="A link to a record of allergies or intolerances which should be included in the nutrition order.",
    )
    food_preference_modifier: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="foodPreferenceModifier",
        description="This modifier is used to convey order-specific modifiers about the type of food that should be given. These can be derived from patient allergies, intolerances, or preferences such as Halal, Vegan or Kosher. This modifier applies to the entire nutrition order inclusive of the oral diet, nutritional supplements and enteral formula feedings.",
    )
    exclude_food_modifier: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="excludeFoodModifier",
        description="This modifier is used to convey Order-specific modifier about the type of oral food or oral fluids that should not be given. These can be derived from patient allergies, intolerances, or preferences such as No Red Meat, No Soy or No Wheat or Gluten-Free. While it should not be necessary to repeat allergy or intolerance information captured in the referenced AllergyIntolerance resource in the excludeFoodModifier, this element may be used to convey additional specificity related to foods that should be eliminated from the patient&rsquo;s diet for any reason. This modifier applies to the entire nutrition order inclusive of the oral diet, nutritional supplements and enteral formula feedings.",
    )
    oral_diet: Optional[NutritionOrderOralDiet] = Field(
        default=None,
        alias="oralDiet",
        description="Diet given orally in contrast to enteral (tube) feeding.",
    )
    supplement: Optional[list[NutritionOrderSupplement]] = Field(
        default=None,
        description="Oral nutritional products given in order to add further nutritional value to the patient's diet.",
    )
    enteral_formula: Optional[NutritionOrderEnteralFormula] = Field(
        default=None,
        alias="enteralFormula",
        description="Feeding provided through the gastrointestinal tract via a tube, catheter, or stoma that delivers nutrition distal to the oral cavity.",
    )
    note: Optional[list[Annotation]] = Field(
        default=None,
        description="Comments made about the {{title}} by the requester, performer, subject or other participants.",
    )


class NutritionOrderEnteralFormula(MedplumFHIRBase):
    """Feeding provided through the gastrointestinal tract via a tube,
    catheter, or stoma that delivers nutrition distal to the oral cavity.
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
    base_formula_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="baseFormulaType",
        description="The type of enteral or infant formula such as an adult standard formula with fiber or a soy-based infant formula.",
    )
    base_formula_product_name: Optional[str] = Field(
        default=None,
        alias="baseFormulaProductName",
        description="The product or brand name of the enteral or infant formula product such as &quot;ACME Adult Standard Formula&quot;.",
    )
    additive_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="additiveType",
        description="Indicates the type of modular component such as protein, carbohydrate, fat or fiber to be provided in addition to or mixed with the base formula.",
    )
    additive_product_name: Optional[str] = Field(
        default=None,
        alias="additiveProductName",
        description="The product or brand name of the type of modular component to be added to the formula.",
    )
    caloric_density: Optional[Quantity] = Field(
        default=None,
        alias="caloricDensity",
        description="The amount of energy (calories) that the formula should provide per specified volume, typically per mL or fluid oz. For example, an infant may require a formula that provides 24 calories per fluid ounce or an adult may require an enteral formula that provides 1.5 calorie/mL.",
    )
    routeof_administration: Optional[CodeableConcept] = Field(
        default=None,
        alias="routeofAdministration",
        description="The route or physiological path of administration into the patient's gastrointestinal tract for purposes of providing the formula feeding, e.g. nasogastric tube.",
    )
    administration: Optional[list[NutritionOrderEnteralFormulaAdministration]] = Field(
        default=None,
        description="Formula administration instructions as structured data. This repeating structure allows for changing the administration rate or volume over time for both bolus and continuous feeding. An example of this would be an instruction to increase the rate of continuous feeding every 2 hours.",
    )
    max_volume_to_deliver: Optional[Quantity] = Field(
        default=None,
        alias="maxVolumeToDeliver",
        description="The maximum total quantity of formula that may be administered to a subject over the period of time, e.g. 1440 mL over 24 hours.",
    )
    administration_instruction: Optional[str] = Field(
        default=None,
        alias="administrationInstruction",
        description="Free text formula administration, feeding instructions or additional instructions or information.",
    )


class NutritionOrderEnteralFormulaAdministration(MedplumFHIRBase):
    """Formula administration instructions as structured data. This repeating
    structure allows for changing the administration rate or volume over
    time for both bolus and continuous feeding. An example of this would be
    an instruction to increase the rate of continuous feeding every 2 hours.
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
    schedule: Optional[Timing] = Field(
        default=None,
        description="The time period and frequency at which the enteral formula should be delivered to the patient.",
    )
    quantity: Optional[Quantity] = Field(
        default=None,
        description="The volume of formula to provide to the patient per the specified administration schedule.",
    )
    rate_quantity: Optional[Quantity] = Field(
        default=None,
        alias="rateQuantity",
        description="The rate of administration of formula via a feeding pump, e.g. 60 mL per hour, according to the specified schedule.",
    )
    rate_ratio: Optional[Ratio] = Field(
        default=None,
        alias="rateRatio",
        description="The rate of administration of formula via a feeding pump, e.g. 60 mL per hour, according to the specified schedule.",
    )


class NutritionOrderOralDiet(MedplumFHIRBase):
    """Diet given orally in contrast to enteral (tube) feeding."""

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
    type: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="The kind of diet or dietary restriction such as fiber restricted diet or diabetic diet.",
    )
    schedule: Optional[list[Timing]] = Field(
        default=None,
        description="The time period and frequency at which the diet should be given. The diet should be given for the combination of all schedules if more than one schedule is present.",
    )
    nutrient: Optional[list[NutritionOrderOralDietNutrient]] = Field(
        default=None,
        description="Class that defines the quantity and type of nutrient modifications (for example carbohydrate, fiber or sodium) required for the oral diet.",
    )
    texture: Optional[list[NutritionOrderOralDietTexture]] = Field(
        default=None,
        description="Class that describes any texture modifications required for the patient to safely consume various types of solid foods.",
    )
    fluid_consistency_type: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="fluidConsistencyType",
        description="The required consistency (e.g. honey-thick, nectar-thick, thin, thickened.) of liquids or fluids served to the patient.",
    )
    instruction: Optional[str] = Field(
        default=None,
        description="Free text or additional instructions or information pertaining to the oral diet.",
    )


class NutritionOrderOralDietNutrient(MedplumFHIRBase):
    """Class that defines the quantity and type of nutrient modifications (for
    example carbohydrate, fiber or sodium) required for the oral diet.
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
    modifier: Optional[CodeableConcept] = Field(
        default=None,
        description="The nutrient that is being modified such as carbohydrate or sodium.",
    )
    amount: Optional[Quantity] = Field(
        default=None,
        description="The quantity of the specified nutrient to include in diet.",
    )


class NutritionOrderOralDietTexture(MedplumFHIRBase):
    """Class that describes any texture modifications required for the patient
    to safely consume various types of solid foods.
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
    modifier: Optional[CodeableConcept] = Field(
        default=None,
        description="Any texture modifications (for solid foods) that should be made, e.g. easy to chew, chopped, ground, and pureed.",
    )
    food_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="foodType",
        description="The food type(s) (e.g. meats, all foods) that the texture modification applies to. This could be all foods types.",
    )


class NutritionOrderSupplement(MedplumFHIRBase):
    """Oral nutritional products given in order to add further nutritional
    value to the patient's diet.
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
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The kind of nutritional supplement product required such as a high protein or pediatric clear liquid supplement.",
    )
    product_name: Optional[str] = Field(
        default=None,
        alias="productName",
        description="The product or brand name of the nutritional supplement such as &quot;Acme Protein Shake&quot;.",
    )
    schedule: Optional[list[Timing]] = Field(
        default=None,
        description="The time period and frequency at which the supplement(s) should be given. The supplement should be given for the combination of all schedules if more than one schedule is present.",
    )
    quantity: Optional[Quantity] = Field(
        default=None,
        description="The amount of the nutritional supplement to be given.",
    )
    instruction: Optional[str] = Field(
        default=None,
        description="Free text or additional instructions or information pertaining to the oral supplement.",
    )
