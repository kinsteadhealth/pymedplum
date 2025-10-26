# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class SubstancePolymer(MedplumFHIRBase):
    """Todo."""

    resource_type: Literal["SubstancePolymer"] = Field(
        default="SubstancePolymer", alias="resourceType"
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
    class_: Optional[CodeableConcept] = Field(
        default=None, alias="class", description="Todo."
    )
    geometry: Optional[CodeableConcept] = Field(default=None, description="Todo.")
    copolymer_connectivity: Optional[list[CodeableConcept]] = Field(
        default=None, alias="copolymerConnectivity", description="Todo."
    )
    modification: Optional[list[str]] = Field(default=None, description="Todo.")
    monomer_set: Optional[list[SubstancePolymerMonomerSet]] = Field(
        default=None, alias="monomerSet", description="Todo."
    )
    repeat: Optional[list[SubstancePolymerRepeat]] = Field(
        default=None, description="Todo."
    )


class SubstancePolymerMonomerSet(MedplumFHIRBase):
    """Todo."""

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
    ratio_type: Optional[CodeableConcept] = Field(
        default=None, alias="ratioType", description="Todo."
    )
    starting_material: Optional[list[SubstancePolymerMonomerSetStartingMaterial]] = (
        Field(default=None, alias="startingMaterial", description="Todo.")
    )


class SubstancePolymerMonomerSetStartingMaterial(MedplumFHIRBase):
    """Todo."""

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
    material: Optional[CodeableConcept] = Field(default=None, description="Todo.")
    type: Optional[CodeableConcept] = Field(default=None, description="Todo.")
    is_defining: Optional[bool] = Field(
        default=None, alias="isDefining", description="Todo."
    )
    amount: Optional[SubstanceAmount] = Field(default=None, description="Todo.")


class SubstancePolymerRepeat(MedplumFHIRBase):
    """Todo."""

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
    number_of_units: Optional[Union[int, float]] = Field(
        default=None, alias="numberOfUnits", description="Todo."
    )
    average_molecular_formula: Optional[str] = Field(
        default=None, alias="averageMolecularFormula", description="Todo."
    )
    repeat_unit_amount_type: Optional[CodeableConcept] = Field(
        default=None, alias="repeatUnitAmountType", description="Todo."
    )
    repeat_unit: Optional[list[SubstancePolymerRepeatRepeatUnit]] = Field(
        default=None, alias="repeatUnit", description="Todo."
    )


class SubstancePolymerRepeatRepeatUnit(MedplumFHIRBase):
    """Todo."""

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
    orientation_of_polymerisation: Optional[CodeableConcept] = Field(
        default=None, alias="orientationOfPolymerisation", description="Todo."
    )
    repeat_unit: Optional[str] = Field(
        default=None, alias="repeatUnit", description="Todo."
    )
    amount: Optional[SubstanceAmount] = Field(default=None, description="Todo.")
    degree_of_polymerisation: Optional[
        list[SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation]
    ] = Field(default=None, alias="degreeOfPolymerisation", description="Todo.")
    structural_representation: Optional[
        list[SubstancePolymerRepeatRepeatUnitStructuralRepresentation]
    ] = Field(default=None, alias="structuralRepresentation", description="Todo.")


class SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation(MedplumFHIRBase):
    """Todo."""

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
    degree: Optional[CodeableConcept] = Field(default=None, description="Todo.")
    amount: Optional[SubstanceAmount] = Field(default=None, description="Todo.")


class SubstancePolymerRepeatRepeatUnitStructuralRepresentation(MedplumFHIRBase):
    """Todo."""

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
    type: Optional[CodeableConcept] = Field(default=None, description="Todo.")
    representation: Optional[str] = Field(default=None, description="Todo.")
    attachment: Optional[Attachment] = Field(default=None, description="Todo.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SubstancePolymer", SubstancePolymer)
    register_model("SubstancePolymerMonomerSet", SubstancePolymerMonomerSet)
    register_model(
        "SubstancePolymerMonomerSetStartingMaterial",
        SubstancePolymerMonomerSetStartingMaterial,
    )
    register_model("SubstancePolymerRepeat", SubstancePolymerRepeat)
    register_model("SubstancePolymerRepeatRepeatUnit", SubstancePolymerRepeatRepeatUnit)
    register_model(
        "SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation",
        SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation,
    )
    register_model(
        "SubstancePolymerRepeatRepeatUnitStructuralRepresentation",
        SubstancePolymerRepeatRepeatUnitStructuralRepresentation,
    )
