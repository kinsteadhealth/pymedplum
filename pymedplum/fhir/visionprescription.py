# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

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
    from pymedplum.fhir.reference import Reference


class VisionPrescription(MedplumFHIRBase):
    """An authorization for the provision of glasses and/or contact lenses to a patient."""

    resource_type: Literal["VisionPrescription"] = Field(
        default="VisionPrescription", alias="resourceType"
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
        description="A unique identifier assigned to this vision prescription.",
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    created: str = Field(default=..., description="The date this resource was created.")
    patient: Reference = Field(
        default=...,
        description="A resource reference to the person to whom the vision prescription applies.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="A reference to a resource that identifies the particular occurrence of contact between patient and health care provider during which the prescription was issued.",
    )
    date_written: str = Field(
        default=...,
        alias="dateWritten",
        description="The date (and perhaps time) when the prescription was written.",
    )
    prescriber: Reference = Field(
        default=...,
        description="The healthcare professional responsible for authorizing the prescription.",
    )
    lens_specification: list[VisionPrescriptionLensSpecification] = Field(
        default=...,
        alias="lensSpecification",
        description="Contain the details of the individual lens specifications and serves as the authorization for the fullfillment by certified professionals.",
    )


class VisionPrescriptionLensSpecification(MedplumFHIRBase):
    """Contain the details of the individual lens specifications and serves as
    the authorization for the fullfillment by certified professionals.
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
    product: CodeableConcept = Field(
        default=...,
        description="Identifies the type of vision correction product which is required for the patient.",
    )
    eye: Literal["right", "left"] = Field(
        default=..., description="The eye for which the lens specification applies."
    )
    sphere: Optional[Union[int, float]] = Field(
        default=None, description="Lens power measured in dioptres (0.25 units)."
    )
    cylinder: Optional[Union[int, float]] = Field(
        default=None,
        description="Power adjustment for astigmatism measured in dioptres (0.25 units).",
    )
    axis: Optional[Union[int, float]] = Field(
        default=None,
        description="Adjustment for astigmatism measured in integer degrees.",
    )
    prism: Optional[list[VisionPrescriptionLensSpecificationPrism]] = Field(
        default=None, description="Allows for adjustment on two axis."
    )
    add: Optional[Union[int, float]] = Field(
        default=None,
        description="Power adjustment for multifocal lenses measured in dioptres (0.25 units).",
    )
    power: Optional[Union[int, float]] = Field(
        default=None,
        description="Contact lens power measured in dioptres (0.25 units).",
    )
    back_curve: Optional[Union[int, float]] = Field(
        default=None,
        alias="backCurve",
        description="Back curvature measured in millimetres.",
    )
    diameter: Optional[Union[int, float]] = Field(
        default=None, description="Contact lens diameter measured in millimetres."
    )
    duration: Optional[Quantity] = Field(
        default=None, description="The recommended maximum wear period for the lens."
    )
    color: Optional[str] = Field(default=None, description="Special color or pattern.")
    brand: Optional[str] = Field(
        default=None, description="Brand recommendations or restrictions."
    )
    note: Optional[list[Annotation]] = Field(
        default=None,
        description="Notes for special requirements such as coatings and lens materials.",
    )


class VisionPrescriptionLensSpecificationPrism(MedplumFHIRBase):
    """Allows for adjustment on two axis."""

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
    amount: Union[int, float] = Field(
        default=...,
        description="Amount of prism to compensate for eye alignment in fractional units.",
    )
    base: Literal["up", "down", "in", "out"] = Field(
        default=...,
        description="The relative base, or reference lens edge, for the prism.",
    )
