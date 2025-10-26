# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference


class SubstanceSpecification(MedplumFHIRBase):
    """The detailed description of a substance, typically at a level beyond
    what is used for prescribing.
    """

    resource_type: Literal["SubstanceSpecification"] = Field(
        default="SubstanceSpecification", alias="resourceType"
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
        default=None, description="Identifier by which this substance is known."
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="High level categorization, e.g. polymer or nucleic acid.",
    )
    status: CodeableConcept | None = Field(
        default=None,
        description="Status of substance within the catalogue e.g. approved.",
    )
    domain: CodeableConcept | None = Field(
        default=None,
        description="If the substance applies to only human or veterinary use.",
    )
    description: str | None = Field(
        default=None, description="Textual description of the substance."
    )
    source: list[Reference] | None = Field(
        default=None, description="Supporting literature."
    )
    comment: str | None = Field(
        default=None, description="Textual comment about this record of a substance."
    )
    moiety: list[SubstanceSpecificationMoiety] | None = Field(
        default=None, description="Moiety, for structural modifications."
    )
    property: list[SubstanceSpecificationProperty] | None = Field(
        default=None,
        description="General specifications for this substance, including how it is related to other substances.",
    )
    reference_information: Reference | None = Field(
        default=None,
        alias="referenceInformation",
        description="General information detailing this substance.",
    )
    structure: SubstanceSpecificationStructure | None = Field(
        default=None, description="Structural information."
    )
    code: list[SubstanceSpecificationCode] | None = Field(
        default=None, description="Codes associated with the substance."
    )
    name: list[SubstanceSpecificationName] | None = Field(
        default=None, description="Names applicable to this substance."
    )
    molecular_weight: (
        list[SubstanceSpecificationStructureIsotopeMolecularWeight] | None
    ) = Field(
        default=None,
        alias="molecularWeight",
        description="The molecular weight or weight range (for proteins, polymers or nucleic acids).",
    )
    relationship: list[SubstanceSpecificationRelationship] | None = Field(
        default=None,
        description="A link between this substance and another, with details of the relationship.",
    )
    nucleic_acid: Reference | None = Field(
        default=None,
        alias="nucleicAcid",
        description="Data items specific to nucleic acids.",
    )
    polymer: Reference | None = Field(
        default=None, description="Data items specific to polymers."
    )
    protein: Reference | None = Field(
        default=None, description="Data items specific to proteins."
    )
    source_material: Reference | None = Field(
        default=None,
        alias="sourceMaterial",
        description="Material or taxonomic/anatomical source for the substance.",
    )


class SubstanceSpecificationCode(MedplumFHIRBase):
    """Codes associated with the substance."""

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
    code: CodeableConcept | None = Field(default=None, description="The specific code.")
    status: CodeableConcept | None = Field(
        default=None, description="Status of the code assignment."
    )
    status_date: str | None = Field(
        default=None,
        alias="statusDate",
        description="The date at which the code status is changed as part of the terminology maintenance.",
    )
    comment: str | None = Field(
        default=None,
        description="Any comment can be provided in this field, if necessary.",
    )
    source: list[Reference] | None = Field(
        default=None, description="Supporting literature."
    )


class SubstanceSpecificationMoiety(MedplumFHIRBase):
    """Moiety, for structural modifications."""

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
    role: CodeableConcept | None = Field(
        default=None, description="Role that the moiety is playing."
    )
    identifier: Identifier | None = Field(
        default=None, description="Identifier by which this moiety substance is known."
    )
    name: str | None = Field(
        default=None, description="Textual name for this moiety substance."
    )
    stereochemistry: CodeableConcept | None = Field(
        default=None, description="Stereochemistry type."
    )
    optical_activity: CodeableConcept | None = Field(
        default=None, alias="opticalActivity", description="Optical activity type."
    )
    molecular_formula: str | None = Field(
        default=None, alias="molecularFormula", description="Molecular formula."
    )
    amount_quantity: Quantity | None = Field(
        default=None,
        alias="amountQuantity",
        description="Quantitative value for this moiety.",
    )
    amount_string: str | None = Field(
        default=None,
        alias="amountString",
        description="Quantitative value for this moiety.",
    )


class SubstanceSpecificationName(MedplumFHIRBase):
    """Names applicable to this substance."""

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
    name: str = Field(default=..., description="The actual name.")
    type: CodeableConcept | None = Field(default=None, description="Name type.")
    status: CodeableConcept | None = Field(
        default=None, description="The status of the name."
    )
    preferred: bool | None = Field(
        default=None, description="If this is the preferred name for this substance."
    )
    language: list[CodeableConcept] | None = Field(
        default=None, description="Language of the name."
    )
    domain: list[CodeableConcept] | None = Field(
        default=None,
        description="The use context of this name for example if there is a different name a drug active ingredient as opposed to a food colour additive.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None, description="The jurisdiction where this name applies."
    )
    synonym: list[SubstanceSpecificationName] | None = Field(
        default=None, description="A synonym of this name."
    )
    translation: list[SubstanceSpecificationName] | None = Field(
        default=None, description="A translation for this name."
    )
    official: list[SubstanceSpecificationNameOfficial] | None = Field(
        default=None, description="Details of the official nature of this name."
    )
    source: list[Reference] | None = Field(
        default=None, description="Supporting literature."
    )


class SubstanceSpecificationNameOfficial(MedplumFHIRBase):
    """Details of the official nature of this name."""

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
    authority: CodeableConcept | None = Field(
        default=None, description="Which authority uses this official name."
    )
    status: CodeableConcept | None = Field(
        default=None, description="The status of the official name."
    )
    date: str | None = Field(default=None, description="Date of official name change.")


class SubstanceSpecificationProperty(MedplumFHIRBase):
    """General specifications for this substance, including how it is related
    to other substances.
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
    category: CodeableConcept | None = Field(
        default=None,
        description="A category for this property, e.g. Physical, Chemical, Enzymatic.",
    )
    code: CodeableConcept | None = Field(
        default=None, description="Property type e.g. viscosity, pH, isoelectric point."
    )
    parameters: str | None = Field(
        default=None,
        description="Parameters that were used in the measurement of a property (e.g. for viscosity: measured at 20C with a pH of 7.1).",
    )
    defining_substance_reference: Reference | None = Field(
        default=None,
        alias="definingSubstanceReference",
        description="A substance upon which a defining property depends (e.g. for solubility: in water, in alcohol).",
    )
    defining_substance_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="definingSubstanceCodeableConcept",
        description="A substance upon which a defining property depends (e.g. for solubility: in water, in alcohol).",
    )
    amount_quantity: Quantity | None = Field(
        default=None,
        alias="amountQuantity",
        description="Quantitative value for this property.",
    )
    amount_string: str | None = Field(
        default=None,
        alias="amountString",
        description="Quantitative value for this property.",
    )


class SubstanceSpecificationRelationship(MedplumFHIRBase):
    """A link between this substance and another, with details of the relationship."""

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
    substance_reference: Reference | None = Field(
        default=None,
        alias="substanceReference",
        description="A pointer to another substance, as a resource or just a representational code.",
    )
    substance_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="substanceCodeableConcept",
        description="A pointer to another substance, as a resource or just a representational code.",
    )
    relationship: CodeableConcept | None = Field(
        default=None,
        description="For example &quot;salt to parent&quot;, &quot;active moiety&quot;, &quot;starting material&quot;.",
    )
    is_defining: bool | None = Field(
        default=None,
        alias="isDefining",
        description="For example where an enzyme strongly bonds with a particular substance, this is a defining relationship for that enzyme, out of several possible substance relationships.",
    )
    amount_quantity: Quantity | None = Field(
        default=None,
        alias="amountQuantity",
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other.",
    )
    amount_range: Range | None = Field(
        default=None,
        alias="amountRange",
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other.",
    )
    amount_ratio: Ratio | None = Field(
        default=None,
        alias="amountRatio",
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other.",
    )
    amount_string: str | None = Field(
        default=None,
        alias="amountString",
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other.",
    )
    amount_ratio_low_limit: Ratio | None = Field(
        default=None,
        alias="amountRatioLowLimit",
        description="For use when the numeric.",
    )
    amount_type: CodeableConcept | None = Field(
        default=None,
        alias="amountType",
        description="An operator for the amount, for example &quot;average&quot;, &quot;approximately&quot;, &quot;less than&quot;.",
    )
    source: list[Reference] | None = Field(
        default=None, description="Supporting literature."
    )


class SubstanceSpecificationStructure(MedplumFHIRBase):
    """Structural information."""

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
    stereochemistry: CodeableConcept | None = Field(
        default=None, description="Stereochemistry type."
    )
    optical_activity: CodeableConcept | None = Field(
        default=None, alias="opticalActivity", description="Optical activity type."
    )
    molecular_formula: str | None = Field(
        default=None, alias="molecularFormula", description="Molecular formula."
    )
    molecular_formula_by_moiety: str | None = Field(
        default=None,
        alias="molecularFormulaByMoiety",
        description="Specified per moiety according to the Hill system, i.e. first C, then H, then alphabetical, each moiety separated by a dot.",
    )
    isotope: list[SubstanceSpecificationStructureIsotope] | None = Field(
        default=None,
        description="Applicable for single substances that contain a radionuclide or a non-natural isotopic ratio.",
    )
    molecular_weight: SubstanceSpecificationStructureIsotopeMolecularWeight | None = (
        Field(
            default=None,
            alias="molecularWeight",
            description="The molecular weight or weight range (for proteins, polymers or nucleic acids).",
        )
    )
    source: list[Reference] | None = Field(
        default=None, description="Supporting literature."
    )
    representation: list[SubstanceSpecificationStructureRepresentation] | None = Field(
        default=None, description="Molecular structural representation."
    )


class SubstanceSpecificationStructureIsotope(MedplumFHIRBase):
    """Applicable for single substances that contain a radionuclide or a
    non-natural isotopic ratio.
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
    identifier: Identifier | None = Field(
        default=None,
        description="Substance identifier for each non-natural or radioisotope.",
    )
    name: CodeableConcept | None = Field(
        default=None, description="Substance name for each non-natural or radioisotope."
    )
    substitution: CodeableConcept | None = Field(
        default=None,
        description="The type of isotopic substitution present in a single substance.",
    )
    half_life: Quantity | None = Field(
        default=None,
        alias="halfLife",
        description="Half life - for a non-natural nuclide.",
    )
    molecular_weight: SubstanceSpecificationStructureIsotopeMolecularWeight | None = (
        Field(
            default=None,
            alias="molecularWeight",
            description="The molecular weight or weight range (for proteins, polymers or nucleic acids).",
        )
    )


class SubstanceSpecificationStructureIsotopeMolecularWeight(MedplumFHIRBase):
    """The molecular weight or weight range (for proteins, polymers or nucleic acids)."""

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
    method: CodeableConcept | None = Field(
        default=None,
        description="The method by which the molecular weight was determined.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Type of molecular weight such as exact, average (also known as. number average), weight average.",
    )
    amount: Quantity | None = Field(
        default=None,
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.",
    )


class SubstanceSpecificationStructureRepresentation(MedplumFHIRBase):
    """Molecular structural representation."""

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
        description="The type of structure (e.g. Full, Partial, Representative).",
    )
    representation: str | None = Field(
        default=None,
        description="The structural representation as text string in a format e.g. InChI, SMILES, MOLFILE, CDX.",
    )
    attachment: Attachment | None = Field(
        default=None, description="An attached file with the structural representation."
    )
