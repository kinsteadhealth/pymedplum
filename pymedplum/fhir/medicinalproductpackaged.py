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
    from pymedplum.fhir.marketingstatus import MarketingStatus
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.prodcharacteristic import ProdCharacteristic
    from pymedplum.fhir.productshelflife import ProductShelfLife
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class MedicinalProductPackaged(MedplumFHIRBase):
    """A medicinal product in a container or package."""

    resource_type: Literal["MedicinalProductPackaged"] = Field(
        default="MedicinalProductPackaged", alias="resourceType"
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
        default=None, description="Unique identifier."
    )
    subject: list[Reference] | None = Field(
        default=None, description="The product with this is a pack for."
    )
    description: str | None = Field(default=None, description="Textual description.")
    legal_status_of_supply: CodeableConcept | None = Field(
        default=None,
        alias="legalStatusOfSupply",
        description="The legal status of supply of the medicinal product as classified by the regulator.",
    )
    marketing_status: list[MarketingStatus] | None = Field(
        default=None, alias="marketingStatus", description="Marketing information."
    )
    marketing_authorization: Reference | None = Field(
        default=None,
        alias="marketingAuthorization",
        description="Manufacturer of this Package Item.",
    )
    manufacturer: list[Reference] | None = Field(
        default=None, description="Manufacturer of this Package Item."
    )
    batch_identifier: list[MedicinalProductPackagedBatchIdentifier] | None = Field(
        default=None, alias="batchIdentifier", description="Batch numbering."
    )
    package_item: list[MedicinalProductPackagedPackageItem] = Field(
        default=...,
        alias="packageItem",
        description="A packaging item, as a contained for medicine, possibly with other packaging items within.",
    )


class MedicinalProductPackagedBatchIdentifier(MedplumFHIRBase):
    """Batch numbering."""

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
    outer_packaging: Identifier = Field(
        default=...,
        alias="outerPackaging",
        description="A number appearing on the outer packaging of a specific batch.",
    )
    immediate_packaging: Identifier | None = Field(
        default=None,
        alias="immediatePackaging",
        description="A number appearing on the immediate packaging (and not the outer packaging).",
    )


class MedicinalProductPackagedPackageItem(MedplumFHIRBase):
    """A packaging item, as a contained for medicine, possibly with other
    packaging items within.
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
    identifier: list[Identifier] | None = Field(
        default=None, description="Including possibly Data Carrier Identifier."
    )
    type: CodeableConcept = Field(
        default=..., description="The physical type of the container of the medicine."
    )
    quantity: Quantity = Field(
        default=...,
        description="The quantity of this package in the medicinal product, at the current level of packaging. The outermost is always 1.",
    )
    material: list[CodeableConcept] | None = Field(
        default=None, description="Material type of the package item."
    )
    alternate_material: list[CodeableConcept] | None = Field(
        default=None,
        alias="alternateMaterial",
        description="A possible alternate material for the packaging.",
    )
    device: list[Reference] | None = Field(
        default=None, description="A device accompanying a medicinal product."
    )
    manufactured_item: list[Reference] | None = Field(
        default=None,
        alias="manufacturedItem",
        description="The manufactured item as contained in the packaged medicinal product.",
    )
    package_item: list[MedicinalProductPackagedPackageItem] | None = Field(
        default=None,
        alias="packageItem",
        description="Allows containers within containers.",
    )
    physical_characteristics: ProdCharacteristic | None = Field(
        default=None,
        alias="physicalCharacteristics",
        description="Dimensions, color etc.",
    )
    other_characteristics: list[CodeableConcept] | None = Field(
        default=None,
        alias="otherCharacteristics",
        description="Other codeable characteristics.",
    )
    shelf_life_storage: list[ProductShelfLife] | None = Field(
        default=None,
        alias="shelfLifeStorage",
        description="Shelf Life and storage information.",
    )
    manufacturer: list[Reference] | None = Field(
        default=None, description="Manufacturer of this Package Item."
    )
