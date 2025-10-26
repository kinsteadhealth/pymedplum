# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

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


class Medication(MedplumFHIRBase):
    """This resource is primarily used for the identification and definition of
    a medication for the purposes of prescribing, dispensing, and
    administering a medication as well as for making statements about
    medication use.
    """

    resource_type: Literal["Medication"] = Field(
        default="Medication", alias="resourceType"
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
        default=None, description="Business identifier for this medication."
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="A code (or set of codes) that specify this medication, or a textual description if no code is available. Usage note: This could be a standard medication code such as a code from RxNorm, SNOMED CT, IDMP etc. It could also be a national or local formulary code, optionally with translations to other code systems.",
    )
    status: Optional[Literal["active", "inactive", "entered-in-error"]] = Field(
        default=None,
        description="A code to indicate if the medication is in active use.",
    )
    manufacturer: Optional[Reference] = Field(
        default=None,
        description="Describes the details of the manufacturer of the medication product. This is not intended to represent the distributor of a medication product.",
    )
    form: Optional[CodeableConcept] = Field(
        default=None,
        description="Describes the form of the item. Powder; tablets; capsule.",
    )
    amount: Optional[Ratio] = Field(
        default=None,
        description="Specific amount of the drug in the packaged product. For example, when specifying a product that has the same strength (For example, Insulin glargine 100 unit per mL solution for injection), this attribute provides additional clarification of the package amount (For example, 3 mL, 10mL, etc.).",
    )
    ingredient: Optional[list[MedicationIngredient]] = Field(
        default=None,
        description="Identifies a particular constituent of interest in the product.",
    )
    batch: Optional[MedicationBatch] = Field(
        default=None,
        description="Information that only applies to packages (not products).",
    )


class MedicationBatch(MedplumFHIRBase):
    """Information that only applies to packages (not products)."""

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
    lot_number: Optional[str] = Field(
        default=None,
        alias="lotNumber",
        description="The assigned lot number of a batch of the specified product.",
    )
    expiration_date: Optional[str] = Field(
        default=None,
        alias="expirationDate",
        description="When this specific batch of product will expire.",
    )


class MedicationIngredient(MedplumFHIRBase):
    """Identifies a particular constituent of interest in the product."""

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
    item_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="itemCodeableConcept",
        description="The actual ingredient - either a substance (simple ingredient) or another medication of a medication.",
    )
    item_reference: Optional[Reference] = Field(
        default=None,
        alias="itemReference",
        description="The actual ingredient - either a substance (simple ingredient) or another medication of a medication.",
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
