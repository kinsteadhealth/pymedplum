# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.dosage import Dosage
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference


class MedicationKnowledge(MedplumFHIRBase):
    """Information about a medication that is used to support knowledge."""

    resource_type: Literal["MedicationKnowledge"] = Field(
        default="MedicationKnowledge", alias="resourceType"
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
    code: CodeableConcept | None = Field(
        default=None,
        description="A code that specifies this medication, or a textual description if no code is available. Usage note: This could be a standard medication code such as a code from RxNorm, SNOMED CT, IDMP etc. It could also be a national or local formulary code, optionally with translations to other code systems.",
    )
    status: Literal["active", "inactive", "entered-in-error"] | None = Field(
        default=None,
        description="A code to indicate if the medication is in active use. The status refers to the validity about the information of the medication and not to its medicinal properties.",
    )
    manufacturer: Reference | None = Field(
        default=None,
        description="Describes the details of the manufacturer of the medication product. This is not intended to represent the distributor of a medication product.",
    )
    dose_form: CodeableConcept | None = Field(
        default=None,
        alias="doseForm",
        description="Describes the form of the item. Powder; tablets; capsule.",
    )
    amount: Quantity | None = Field(
        default=None,
        description="Specific amount of the drug in the packaged product. For example, when specifying a product that has the same strength (For example, Insulin glargine 100 unit per mL solution for injection), this attribute provides additional clarification of the package amount (For example, 3 mL, 10mL, etc.).",
    )
    synonym: list[str] | None = Field(
        default=None,
        description="Additional names for a medication, for example, the name(s) given to a medication in different countries. For example, acetaminophen and paracetamol or salbutamol and albuterol.",
    )
    related_medication_knowledge: (
        list[MedicationKnowledgeRelatedMedicationKnowledge] | None
    ) = Field(
        default=None,
        alias="relatedMedicationKnowledge",
        description="Associated or related knowledge about a medication.",
    )
    associated_medication: list[Reference] | None = Field(
        default=None,
        alias="associatedMedication",
        description="Associated or related medications. For example, if the medication is a branded product (e.g. Crestor), this is the Therapeutic Moeity (e.g. Rosuvastatin) or if this is a generic medication (e.g. Rosuvastatin), this would link to a branded product (e.g. Crestor).",
    )
    product_type: list[CodeableConcept] | None = Field(
        default=None,
        alias="productType",
        description="Category of the medication or product (e.g. branded product, therapeutic moeity, generic product, innovator product, etc.).",
    )
    monograph: list[MedicationKnowledgeMonograph] | None = Field(
        default=None, description="Associated documentation about the medication."
    )
    ingredient: list[MedicationKnowledgeIngredient] | None = Field(
        default=None,
        description="Identifies a particular constituent of interest in the product.",
    )
    preparation_instruction: str | None = Field(
        default=None,
        alias="preparationInstruction",
        description="The instructions for preparing the medication.",
    )
    intended_route: list[CodeableConcept] | None = Field(
        default=None,
        alias="intendedRoute",
        description="The intended or approved route of administration.",
    )
    cost: list[MedicationKnowledgeCost] | None = Field(
        default=None, description="The price of the medication."
    )
    monitoring_program: list[MedicationKnowledgeMonitoringProgram] | None = Field(
        default=None,
        alias="monitoringProgram",
        description="The program under which the medication is reviewed.",
    )
    administration_guidelines: (
        list[MedicationKnowledgeAdministrationGuidelines] | None
    ) = Field(
        default=None,
        alias="administrationGuidelines",
        description="Guidelines for the administration of the medication.",
    )
    medicine_classification: list[MedicationKnowledgeMedicineClassification] | None = (
        Field(
            default=None,
            alias="medicineClassification",
            description="Categorization of the medication within a formulary or classification system.",
        )
    )
    packaging: MedicationKnowledgePackaging | None = Field(
        default=None,
        description="Information that only applies to packages (not products).",
    )
    drug_characteristic: list[MedicationKnowledgeDrugCharacteristic] | None = Field(
        default=None,
        alias="drugCharacteristic",
        description="Specifies descriptive properties of the medicine, such as color, shape, imprints, etc.",
    )
    contraindication: list[Reference] | None = Field(
        default=None,
        description="Potential clinical issue with or between medication(s) (for example, drug-drug interaction, drug-disease contraindication, drug-allergy interaction, etc.).",
    )
    regulatory: list[MedicationKnowledgeRegulatory] | None = Field(
        default=None, description="Regulatory information about a medication."
    )
    kinetics: list[MedicationKnowledgeKinetics] | None = Field(
        default=None,
        description="The time course of drug absorption, distribution, metabolism and excretion of a medication from the body.",
    )


class MedicationKnowledgeAdministrationGuidelines(MedplumFHIRBase):
    """Guidelines for the administration of the medication."""

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
    dosage: list[MedicationKnowledgeAdministrationGuidelinesDosage] | None = Field(
        default=None,
        description="Dosage for the medication for the specific guidelines.",
    )
    indication_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="indicationCodeableConcept",
        description="Indication for use that apply to the specific administration guidelines.",
    )
    indication_reference: Reference | None = Field(
        default=None,
        alias="indicationReference",
        description="Indication for use that apply to the specific administration guidelines.",
    )
    patient_characteristics: (
        list[MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics] | None
    ) = Field(
        default=None,
        alias="patientCharacteristics",
        description="Characteristics of the patient that are relevant to the administration guidelines (for example, height, weight, gender, etc.).",
    )


class MedicationKnowledgeAdministrationGuidelinesDosage(MedplumFHIRBase):
    """Dosage for the medication for the specific guidelines."""

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
    type: CodeableConcept = Field(
        default=...,
        description="The type of dosage (for example, prophylaxis, maintenance, therapeutic, etc.).",
    )
    dosage: list[Dosage] = Field(
        default=...,
        description="Dosage for the medication for the specific guidelines.",
    )


class MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics(
    MedplumFHIRBase
):
    """Characteristics of the patient that are relevant to the administration
    guidelines (for example, height, weight, gender, etc.).
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
    characteristic_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="characteristicCodeableConcept",
        description="Specific characteristic that is relevant to the administration guideline (e.g. height, weight, gender).",
    )
    characteristic_quantity: Quantity | None = Field(
        default=None,
        alias="characteristicQuantity",
        description="Specific characteristic that is relevant to the administration guideline (e.g. height, weight, gender).",
    )
    value: list[str] | None = Field(
        default=None,
        description="The specific characteristic (e.g. height, weight, gender, etc.).",
    )


class MedicationKnowledgeCost(MedplumFHIRBase):
    """The price of the medication."""

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
    type: CodeableConcept = Field(
        default=...,
        description="The category of the cost information. For example, manufacturers' cost, patient cost, claim reimbursement cost, actual acquisition cost.",
    )
    source: str | None = Field(
        default=None,
        description="The source or owner that assigns the price to the medication.",
    )
    cost: Money = Field(default=..., description="The price of the medication.")


class MedicationKnowledgeDrugCharacteristic(MedplumFHIRBase):
    """Specifies descriptive properties of the medicine, such as color, shape,
    imprints, etc.
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
    type: CodeableConcept | None = Field(
        default=None,
        description="A code specifying which characteristic of the medicine is being described (for example, colour, shape, imprint).",
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="Description of the characteristic.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="Description of the characteristic.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="Description of the characteristic.",
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="Description of the characteristic.",
    )


class MedicationKnowledgeIngredient(MedplumFHIRBase):
    """Identifies a particular constituent of interest in the product."""

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
    item_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="itemCodeableConcept",
        description="The actual ingredient - either a substance (simple ingredient) or another medication.",
    )
    item_reference: Reference | None = Field(
        default=None,
        alias="itemReference",
        description="The actual ingredient - either a substance (simple ingredient) or another medication.",
    )
    is_active: bool | None = Field(
        default=None,
        alias="isActive",
        description="Indication of whether this ingredient affects the therapeutic action of the drug.",
    )
    strength: Ratio | None = Field(
        default=None,
        description="Specifies how many (or how much) of the items there are in this Medication. For example, 250 mg per tablet. This is expressed as a ratio where the numerator is 250mg and the denominator is 1 tablet.",
    )


class MedicationKnowledgeKinetics(MedplumFHIRBase):
    """The time course of drug absorption, distribution, metabolism and
    excretion of a medication from the body.
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
    area_under_curve: list[Quantity] | None = Field(
        default=None,
        alias="areaUnderCurve",
        description="The drug concentration measured at certain discrete points in time.",
    )
    lethal_dose50: list[Quantity] | None = Field(
        default=None,
        alias="lethalDose50",
        description="The median lethal dose of a drug.",
    )
    half_life_period: Duration | None = Field(
        default=None,
        alias="halfLifePeriod",
        description="The time required for any specified property (e.g., the concentration of a substance in the body) to decrease by half.",
    )


class MedicationKnowledgeMedicineClassification(MedplumFHIRBase):
    """Categorization of the medication within a formulary or classification system."""

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
    type: CodeableConcept = Field(
        default=...,
        description="The type of category for the medication (for example, therapeutic classification, therapeutic sub-classification).",
    )
    classification: list[CodeableConcept] | None = Field(
        default=None,
        description="Specific category assigned to the medication (e.g. anti-infective, anti-hypertensive, antibiotic, etc.).",
    )


class MedicationKnowledgeMonitoringProgram(MedplumFHIRBase):
    """The program under which the medication is reviewed."""

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
    type: CodeableConcept | None = Field(
        default=None,
        description="Type of program under which the medication is monitored.",
    )
    name: str | None = Field(default=None, description="Name of the reviewing program.")


class MedicationKnowledgeMonograph(MedplumFHIRBase):
    """Associated documentation about the medication."""

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
    type: CodeableConcept | None = Field(
        default=None,
        description="The category of documentation about the medication. (e.g. professional monograph, patient education monograph).",
    )
    source: Reference | None = Field(
        default=None, description="Associated documentation about the medication."
    )


class MedicationKnowledgePackaging(MedplumFHIRBase):
    """Information that only applies to packages (not products)."""

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
    type: CodeableConcept | None = Field(
        default=None,
        description="A code that defines the specific type of packaging that the medication can be found in (e.g. blister sleeve, tube, bottle).",
    )
    quantity: Quantity | None = Field(
        default=None,
        description="The number of product units the package would contain if fully loaded.",
    )


class MedicationKnowledgeRegulatory(MedplumFHIRBase):
    """Regulatory information about a medication."""

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
    regulatory_authority: Reference = Field(
        default=...,
        alias="regulatoryAuthority",
        description="The authority that is specifying the regulations.",
    )
    substitution: list[MedicationKnowledgeRegulatorySubstitution] | None = Field(
        default=None,
        description="Specifies if changes are allowed when dispensing a medication from a regulatory perspective.",
    )
    schedule: list[MedicationKnowledgeRegulatorySchedule] | None = Field(
        default=None,
        description="Specifies the schedule of a medication in jurisdiction.",
    )
    max_dispense: MedicationKnowledgeRegulatoryMaxDispense | None = Field(
        default=None,
        alias="maxDispense",
        description="The maximum number of units of the medication that can be dispensed in a period.",
    )


class MedicationKnowledgeRegulatoryMaxDispense(MedplumFHIRBase):
    """The maximum number of units of the medication that can be dispensed in a period."""

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
    quantity: Quantity = Field(
        default=...,
        description="The maximum number of units of the medication that can be dispensed.",
    )
    period: Duration | None = Field(
        default=None,
        description="The period that applies to the maximum number of units.",
    )


class MedicationKnowledgeRegulatorySchedule(MedplumFHIRBase):
    """Specifies the schedule of a medication in jurisdiction."""

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
    schedule: CodeableConcept = Field(
        default=..., description="Specifies the specific drug schedule."
    )


class MedicationKnowledgeRegulatorySubstitution(MedplumFHIRBase):
    """Specifies if changes are allowed when dispensing a medication from a
    regulatory perspective.
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
    type: CodeableConcept = Field(
        default=..., description="Specifies the type of substitution allowed."
    )
    allowed: bool = Field(
        default=...,
        description="Specifies if regulation allows for changes in the medication when dispensing.",
    )


class MedicationKnowledgeRelatedMedicationKnowledge(MedplumFHIRBase):
    """Associated or related knowledge about a medication."""

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
    type: CodeableConcept = Field(
        default=...,
        description="The category of the associated medication knowledge reference.",
    )
    reference: list[Reference] = Field(
        default=...,
        description="Associated documentation about the associated medication knowledge.",
    )
