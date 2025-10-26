# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class MedicinalProductPackaged(MedplumFHIRBase):
    """A medicinal product in a container or package."""

    resource_type: Literal["MedicinalProductPackaged"] = Field(
        default="MedicinalProductPackaged",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[list[dict[str, Any]]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[list[Identifier]] = Field(default=None, description="Unique identifier.")
    subject: Optional[list[Reference]] = Field(default=None, description="The product with this is a pack for.")
    description: Optional[str] = Field(default=None, description="Textual description.")
    legal_status_of_supply: Optional[CodeableConcept] = Field(default=None, alias="legalStatusOfSupply", description="The legal status of supply of the medicinal product as classified by the regulator.")
    marketing_status: Optional[list[MarketingStatus]] = Field(default=None, alias="marketingStatus", description="Marketing information.")
    marketing_authorization: Optional[Reference] = Field(default=None, alias="marketingAuthorization", description="Manufacturer of this Package Item.")
    manufacturer: Optional[list[Reference]] = Field(default=None, description="Manufacturer of this Package Item.")
    batch_identifier: Optional[list[MedicinalProductPackagedBatchIdentifier]] = Field(default=None, alias="batchIdentifier", description="Batch numbering.")
    package_item: list[MedicinalProductPackagedPackageItem] = Field(default=..., alias="packageItem", description="A packaging item, as a contained for medicine, possibly with other packaging items within.")


class MedicinalProductPackagedBatchIdentifier(MedplumFHIRBase):
    """Batch numbering."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    outer_packaging: Identifier = Field(default=..., alias="outerPackaging", description="A number appearing on the outer packaging of a specific batch.")
    immediate_packaging: Optional[Identifier] = Field(default=None, alias="immediatePackaging", description="A number appearing on the immediate packaging (and not the outer packaging).")


class MedicinalProductPackagedPackageItem(MedplumFHIRBase):
    """A packaging item, as a contained for medicine, possibly with other
    packaging items within.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[list[Identifier]] = Field(default=None, description="Including possibly Data Carrier Identifier.")
    type: CodeableConcept = Field(default=..., description="The physical type of the container of the medicine.")
    quantity: Quantity = Field(default=..., description="The quantity of this package in the medicinal product, at the current level of packaging. The outermost is always 1.")
    material: Optional[list[CodeableConcept]] = Field(default=None, description="Material type of the package item.")
    alternate_material: Optional[list[CodeableConcept]] = Field(default=None, alias="alternateMaterial", description="A possible alternate material for the packaging.")
    device: Optional[list[Reference]] = Field(default=None, description="A device accompanying a medicinal product.")
    manufactured_item: Optional[list[Reference]] = Field(default=None, alias="manufacturedItem", description="The manufactured item as contained in the packaged medicinal product.")
    package_item: Optional[list[MedicinalProductPackagedPackageItem]] = Field(default=None, alias="packageItem", description="Allows containers within containers.")
    physical_characteristics: Optional[ProdCharacteristic] = Field(default=None, alias="physicalCharacteristics", description="Dimensions, color etc.")
    other_characteristics: Optional[list[CodeableConcept]] = Field(default=None, alias="otherCharacteristics", description="Other codeable characteristics.")
    shelf_life_storage: Optional[list[ProductShelfLife]] = Field(default=None, alias="shelfLifeStorage", description="Shelf Life and storage information.")
    manufacturer: Optional[list[Reference]] = Field(default=None, description="Manufacturer of this Package Item.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("MedicinalProductPackaged", MedicinalProductPackaged)
    register_model("MedicinalProductPackagedBatchIdentifier", MedicinalProductPackagedBatchIdentifier)
    register_model("MedicinalProductPackagedPackageItem", MedicinalProductPackagedPackageItem)
