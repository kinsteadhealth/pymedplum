# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class MedicationKnowledge(MedplumFHIRBase):
    """Information about a medication that is used to support knowledge."""

    resource_type: Literal["MedicationKnowledge"] = Field(
        default="MedicationKnowledge", alias="resourceType"
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
    contained: Optional[List[Resource]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="A code that specifies this medication, or a textual description if no code is available. Usage note: This could be a standard medication code such as a code from RxNorm, SNOMED CT, IDMP etc. It could also be a national or local formulary code, optionally with translations to other code systems.",
    )
    status: Optional[Literal["active", "inactive", "entered-in-error"]] = Field(
        default=None,
        description="A code to indicate if the medication is in active use. The status refers to the validity about the information of the medication and not to its medicinal properties.",
    )
    manufacturer: Optional[Reference] = Field(
        default=None,
        description="Describes the details of the manufacturer of the medication product. This is not intended to represent the distributor of a medication product.",
    )
    dose_form: Optional[CodeableConcept] = Field(
        default=None,
        alias="doseForm",
        description="Describes the form of the item. Powder; tablets; capsule.",
    )
    amount: Optional[Quantity] = Field(
        default=None,
        description="Specific amount of the drug in the packaged product. For example, when specifying a product that has the same strength (For example, Insulin glargine 100 unit per mL solution for injection), this attribute provides additional clarification of the package amount (For example, 3 mL, 10mL, etc.).",
    )
    synonym: Optional[List[str]] = Field(
        default=None,
        description="Additional names for a medication, for example, the name(s) given to a medication in different countries. For example, acetaminophen and paracetamol or salbutamol and albuterol.",
    )
    related_medication_knowledge: Optional[
        List[MedicationKnowledgeRelatedMedicationKnowledge]
    ] = Field(
        default=None,
        alias="relatedMedicationKnowledge",
        description="Associated or related knowledge about a medication.",
    )
    associated_medication: Optional[List[Reference]] = Field(
        default=None,
        alias="associatedMedication",
        description="Associated or related medications. For example, if the medication is a branded product (e.g. Crestor), this is the Therapeutic Moeity (e.g. Rosuvastatin) or if this is a generic medication (e.g. Rosuvastatin), this would link to a branded product (e.g. Crestor).",
    )
    product_type: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="productType",
        description="Category of the medication or product (e.g. branded product, therapeutic moeity, generic product, innovator product, etc.).",
    )
    monograph: Optional[List[MedicationKnowledgeMonograph]] = Field(
        default=None, description="Associated documentation about the medication."
    )
    ingredient: Optional[List[MedicationKnowledgeIngredient]] = Field(
        default=None,
        description="Identifies a particular constituent of interest in the product.",
    )
    preparation_instruction: Optional[str] = Field(
        default=None,
        alias="preparationInstruction",
        description="The instructions for preparing the medication.",
    )
    intended_route: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="intendedRoute",
        description="The intended or approved route of administration.",
    )
    cost: Optional[List[MedicationKnowledgeCost]] = Field(
        default=None, description="The price of the medication."
    )
    monitoring_program: Optional[List[MedicationKnowledgeMonitoringProgram]] = Field(
        default=None,
        alias="monitoringProgram",
        description="The program under which the medication is reviewed.",
    )
    administration_guidelines: Optional[
        List[MedicationKnowledgeAdministrationGuidelines]
    ] = Field(
        default=None,
        alias="administrationGuidelines",
        description="Guidelines for the administration of the medication.",
    )
    medicine_classification: Optional[
        List[MedicationKnowledgeMedicineClassification]
    ] = Field(
        default=None,
        alias="medicineClassification",
        description="Categorization of the medication within a formulary or classification system.",
    )
    packaging: Optional[MedicationKnowledgePackaging] = Field(
        default=None,
        description="Information that only applies to packages (not products).",
    )
    drug_characteristic: Optional[List[MedicationKnowledgeDrugCharacteristic]] = Field(
        default=None,
        alias="drugCharacteristic",
        description="Specifies descriptive properties of the medicine, such as color, shape, imprints, etc.",
    )
    contraindication: Optional[List[Reference]] = Field(
        default=None,
        description="Potential clinical issue with or between medication(s) (for example, drug-drug interaction, drug-disease contraindication, drug-allergy interaction, etc.).",
    )
    regulatory: Optional[List[MedicationKnowledgeRegulatory]] = Field(
        default=None, description="Regulatory information about a medication."
    )
    kinetics: Optional[List[MedicationKnowledgeKinetics]] = Field(
        default=None,
        description="The time course of drug absorption, distribution, metabolism and excretion of a medication from the body.",
    )


class MedicationKnowledgeAdministrationGuidelines(MedplumFHIRBase):
    """Guidelines for the administration of the medication."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    dosage: Optional[List[MedicationKnowledgeAdministrationGuidelinesDosage]] = Field(
        default=None,
        description="Dosage for the medication for the specific guidelines.",
    )
    indication_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="indicationCodeableConcept",
        description="Indication for use that apply to the specific administration guidelines.",
    )
    indication_reference: Optional[Reference] = Field(
        default=None,
        alias="indicationReference",
        description="Indication for use that apply to the specific administration guidelines.",
    )
    patient_characteristics: Optional[
        List[MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics]
    ] = Field(
        default=None,
        alias="patientCharacteristics",
        description="Characteristics of the patient that are relevant to the administration guidelines (for example, height, weight, gender, etc.).",
    )


class MedicationKnowledgeAdministrationGuidelinesDosage(MedplumFHIRBase):
    """Dosage for the medication for the specific guidelines."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=...,
        description="The type of dosage (for example, prophylaxis, maintenance, therapeutic, etc.).",
    )
    dosage: List[Dosage] = Field(
        default=...,
        description="Dosage for the medication for the specific guidelines.",
    )


class MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics(
    MedplumFHIRBase
):
    """Characteristics of the patient that are relevant to the administration
    guidelines (for example, height, weight, gender, etc.).
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    characteristic_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="characteristicCodeableConcept",
        description="Specific characteristic that is relevant to the administration guideline (e.g. height, weight, gender).",
    )
    characteristic_quantity: Optional[Quantity] = Field(
        default=None,
        alias="characteristicQuantity",
        description="Specific characteristic that is relevant to the administration guideline (e.g. height, weight, gender).",
    )
    value: Optional[List[str]] = Field(
        default=None,
        description="The specific characteristic (e.g. height, weight, gender, etc.).",
    )


class MedicationKnowledgeCost(MedplumFHIRBase):
    """The price of the medication."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=...,
        description="The category of the cost information. For example, manufacturers' cost, patient cost, claim reimbursement cost, actual acquisition cost.",
    )
    source: Optional[str] = Field(
        default=None,
        description="The source or owner that assigns the price to the medication.",
    )
    cost: Money = Field(default=..., description="The price of the medication.")


class MedicationKnowledgeDrugCharacteristic(MedplumFHIRBase):
    """Specifies descriptive properties of the medicine, such as color, shape,
    imprints, etc.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="A code specifying which characteristic of the medicine is being described (for example, colour, shape, imprint).",
    )
    value_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="valueCodeableConcept",
        description="Description of the characteristic.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="Description of the characteristic.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="Description of the characteristic.",
    )
    value_base64_binary: Optional[str] = Field(
        default=None,
        alias="valueBase64Binary",
        description="Description of the characteristic.",
    )


class MedicationKnowledgeIngredient(MedplumFHIRBase):
    """Identifies a particular constituent of interest in the product."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    item_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="itemCodeableConcept",
        description="The actual ingredient - either a substance (simple ingredient) or another medication.",
    )
    item_reference: Optional[Reference] = Field(
        default=None,
        alias="itemReference",
        description="The actual ingredient - either a substance (simple ingredient) or another medication.",
    )
    is_active: Optional[bool] = Field(
        default=None,
        alias="isActive",
        description="Indication of whether this ingredient affects the therapeutic action of the drug.",
    )
    strength: Optional[Ratio] = Field(
        default=None,
        description="Specifies how many (or how much) of the items there are in this Medication. For example, 250 mg per tablet. This is expressed as a ratio where the numerator is 250mg and the denominator is 1 tablet.",
    )


class MedicationKnowledgeKinetics(MedplumFHIRBase):
    """The time course of drug absorption, distribution, metabolism and
    excretion of a medication from the body.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    area_under_curve: Optional[List[Quantity]] = Field(
        default=None,
        alias="areaUnderCurve",
        description="The drug concentration measured at certain discrete points in time.",
    )
    lethal_dose50: Optional[List[Quantity]] = Field(
        default=None,
        alias="lethalDose50",
        description="The median lethal dose of a drug.",
    )
    half_life_period: Optional[Duration] = Field(
        default=None,
        alias="halfLifePeriod",
        description="The time required for any specified property (e.g., the concentration of a substance in the body) to decrease by half.",
    )


class MedicationKnowledgeMedicineClassification(MedplumFHIRBase):
    """Categorization of the medication within a formulary or classification system."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=...,
        description="The type of category for the medication (for example, therapeutic classification, therapeutic sub-classification).",
    )
    classification: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="Specific category assigned to the medication (e.g. anti-infective, anti-hypertensive, antibiotic, etc.).",
    )


class MedicationKnowledgeMonitoringProgram(MedplumFHIRBase):
    """The program under which the medication is reviewed."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="Type of program under which the medication is monitored.",
    )
    name: Optional[str] = Field(
        default=None, description="Name of the reviewing program."
    )


class MedicationKnowledgeMonograph(MedplumFHIRBase):
    """Associated documentation about the medication."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The category of documentation about the medication. (e.g. professional monograph, patient education monograph).",
    )
    source: Optional[Reference] = Field(
        default=None, description="Associated documentation about the medication."
    )


class MedicationKnowledgePackaging(MedplumFHIRBase):
    """Information that only applies to packages (not products)."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="A code that defines the specific type of packaging that the medication can be found in (e.g. blister sleeve, tube, bottle).",
    )
    quantity: Optional[Quantity] = Field(
        default=None,
        description="The number of product units the package would contain if fully loaded.",
    )


class MedicationKnowledgeRegulatory(MedplumFHIRBase):
    """Regulatory information about a medication."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    regulatory_authority: Reference = Field(
        default=...,
        alias="regulatoryAuthority",
        description="The authority that is specifying the regulations.",
    )
    substitution: Optional[List[MedicationKnowledgeRegulatorySubstitution]] = Field(
        default=None,
        description="Specifies if changes are allowed when dispensing a medication from a regulatory perspective.",
    )
    schedule: Optional[List[MedicationKnowledgeRegulatorySchedule]] = Field(
        default=None,
        description="Specifies the schedule of a medication in jurisdiction.",
    )
    max_dispense: Optional[MedicationKnowledgeRegulatoryMaxDispense] = Field(
        default=None,
        alias="maxDispense",
        description="The maximum number of units of the medication that can be dispensed in a period.",
    )


class MedicationKnowledgeRegulatoryMaxDispense(MedplumFHIRBase):
    """The maximum number of units of the medication that can be dispensed in a period."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    quantity: Quantity = Field(
        default=...,
        description="The maximum number of units of the medication that can be dispensed.",
    )
    period: Optional[Duration] = Field(
        default=None,
        description="The period that applies to the maximum number of units.",
    )


class MedicationKnowledgeRegulatorySchedule(MedplumFHIRBase):
    """Specifies the schedule of a medication in jurisdiction."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
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

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
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

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=...,
        description="The category of the associated medication knowledge reference.",
    )
    reference: List[Reference] = Field(
        default=...,
        description="Associated documentation about the associated medication knowledge.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("MedicationKnowledge", MedicationKnowledge)
    register_model(
        "MedicationKnowledgeAdministrationGuidelines",
        MedicationKnowledgeAdministrationGuidelines,
    )
    register_model(
        "MedicationKnowledgeAdministrationGuidelinesDosage",
        MedicationKnowledgeAdministrationGuidelinesDosage,
    )
    register_model(
        "MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics",
        MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics,
    )
    register_model("MedicationKnowledgeCost", MedicationKnowledgeCost)
    register_model(
        "MedicationKnowledgeDrugCharacteristic", MedicationKnowledgeDrugCharacteristic
    )
    register_model("MedicationKnowledgeIngredient", MedicationKnowledgeIngredient)
    register_model("MedicationKnowledgeKinetics", MedicationKnowledgeKinetics)
    register_model(
        "MedicationKnowledgeMedicineClassification",
        MedicationKnowledgeMedicineClassification,
    )
    register_model(
        "MedicationKnowledgeMonitoringProgram", MedicationKnowledgeMonitoringProgram
    )
    register_model("MedicationKnowledgeMonograph", MedicationKnowledgeMonograph)
    register_model("MedicationKnowledgePackaging", MedicationKnowledgePackaging)
    register_model("MedicationKnowledgeRegulatory", MedicationKnowledgeRegulatory)
    register_model(
        "MedicationKnowledgeRegulatoryMaxDispense",
        MedicationKnowledgeRegulatoryMaxDispense,
    )
    register_model(
        "MedicationKnowledgeRegulatorySchedule", MedicationKnowledgeRegulatorySchedule
    )
    register_model(
        "MedicationKnowledgeRegulatorySubstitution",
        MedicationKnowledgeRegulatorySubstitution,
    )
    register_model(
        "MedicationKnowledgeRelatedMedicationKnowledge",
        MedicationKnowledgeRelatedMedicationKnowledge,
    )
