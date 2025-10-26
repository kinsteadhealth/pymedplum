# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class DeviceDefinition(MedplumFHIRBase):
    """The characteristics, operational status and capabilities of a
    medical-related component of a medical device.
    """

    resource_type: Literal["DeviceDefinition"] = Field(
        default="DeviceDefinition",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Unique instance identifiers assigned to a device by the software, manufacturers, other organizations or owners. For example: handle ID.")
    udi_device_identifier: Optional[list[DeviceDefinitionUdiDeviceIdentifier]] = Field(default=None, alias="udiDeviceIdentifier", description="Unique device identifier (UDI) assigned to device label or package. Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.")
    manufacturer_string: Optional[str] = Field(default=None, alias="manufacturerString", description="A name of the manufacturer.")
    manufacturer_reference: Optional[Reference] = Field(default=None, alias="manufacturerReference", description="A name of the manufacturer.")
    device_name: Optional[list[DeviceDefinitionDeviceName]] = Field(default=None, alias="deviceName", description="A name given to the device to identify it.")
    model_number: Optional[str] = Field(default=None, alias="modelNumber", description="The model number for the device.")
    type: Optional[CodeableConcept] = Field(default=None, description="What kind of device or device system this is.")
    specialization: Optional[list[DeviceDefinitionSpecialization]] = Field(default=None, description="The capabilities supported on a device, the standards to which the device conforms for a particular purpose, and used for the communication.")
    version: Optional[list[str]] = Field(default=None, description="The available versions of the device, e.g., software versions.")
    safety: Optional[list[CodeableConcept]] = Field(default=None, description="Safety characteristics of the device.")
    shelf_life_storage: Optional[list[ProductShelfLife]] = Field(default=None, alias="shelfLifeStorage", description="Shelf Life and storage information.")
    physical_characteristics: Optional[ProdCharacteristic] = Field(default=None, alias="physicalCharacteristics", description="Dimensions, color etc.")
    language_code: Optional[list[CodeableConcept]] = Field(default=None, alias="languageCode", description="Language code for the human-readable text strings produced by the device (all supported).")
    capability: Optional[list[DeviceDefinitionCapability]] = Field(default=None, description="Device capabilities.")
    property: Optional[list[DeviceDefinitionProperty]] = Field(default=None, description="The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.")
    owner: Optional[Reference] = Field(default=None, description="An organization that is responsible for the provision and ongoing maintenance of the device.")
    contact: Optional[list[ContactPoint]] = Field(default=None, description="Contact details for an organization or a particular human that is responsible for the device.")
    url: Optional[str] = Field(default=None, description="A network address on which the device may be contacted directly.")
    online_information: Optional[str] = Field(default=None, alias="onlineInformation", description="Access to on-line information about the device.")
    note: Optional[list[Annotation]] = Field(default=None, description="Descriptive information, usage information or implantation information that is not captured in an existing element.")
    quantity: Optional[Quantity] = Field(default=None, description="The quantity of the device present in the packaging (e.g. the number of devices present in a pack, or the number of devices in the same package of the medicinal product).")
    parent_device: Optional[Reference] = Field(default=None, alias="parentDevice", description="The parent device it can be part of.")
    material: Optional[list[DeviceDefinitionMaterial]] = Field(default=None, description="A substance used to create the material(s) of which the device is made.")
    classification: Optional[list[DeviceDefinitionClassification]] = Field(default=None, description="What kind of device or device system this is.")
    body_site: Optional[CodeableConcept] = Field(default=None, alias="bodySite", description="Indicates the anotomic location on the subject's body where the device was used ( i.e. the target).")


class DeviceDefinitionCapability(MedplumFHIRBase):
    """Device capabilities."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: CodeableConcept = Field(default=..., description="Type of capability.")
    description: Optional[list[CodeableConcept]] = Field(default=None, description="Description of capability.")


class DeviceDefinitionClassification(MedplumFHIRBase):
    """What kind of device or device system this is."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: CodeableConcept = Field(default=..., description="A classification or risk class of the device model.")
    justification: Optional[list[RelatedArtifact]] = Field(default=None, description="Further information qualifying this classification of the device model.")


class DeviceDefinitionDeviceName(MedplumFHIRBase):
    """A name given to the device to identify it."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="The name of the device.")
    type: Literal['udi-label-name', 'user-friendly-name', 'patient-reported-name', 'manufacturer-name', 'model-name', 'other'] = Field(default=..., description="The type of deviceName. UDILabelName | UserFriendlyName | PatientReportedName | ManufactureDeviceName | ModelName.")


class DeviceDefinitionMaterial(MedplumFHIRBase):
    """A substance used to create the material(s) of which the device is made."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    substance: CodeableConcept = Field(default=..., description="The substance.")
    alternate: Optional[bool] = Field(default=None, description="Indicates an alternative material of the device.")
    allergenic_indicator: Optional[bool] = Field(default=None, alias="allergenicIndicator", description="Whether the substance is a known or suspected allergen.")


class DeviceDefinitionProperty(MedplumFHIRBase):
    """The actual configuration settings of a device as it actually operates,
    e.g., regulation status, time properties.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: CodeableConcept = Field(default=..., description="Code that specifies the property DeviceDefinitionPropetyCode (Extensible).")
    value_quantity: Optional[list[Quantity]] = Field(default=None, alias="valueQuantity", description="Property value as a quantity.")
    value_code: Optional[list[CodeableConcept]] = Field(default=None, alias="valueCode", description="Property value as a code, e.g., NTP4 (synced to NTP).")


class DeviceDefinitionSpecialization(MedplumFHIRBase):
    """The capabilities supported on a device, the standards to which the
    device conforms for a particular purpose, and used for the
    communication.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    system_type: str = Field(default=..., alias="systemType", description="The standard that is used to operate and communicate.")
    version: Optional[str] = Field(default=None, description="The version of the standard that is used to operate and communicate.")


class DeviceDefinitionUdiDeviceIdentifier(MedplumFHIRBase):
    """Unique device identifier (UDI) assigned to device label or package. Note
    that the Device may include multiple udiCarriers as it either may
    include just the udiCarrier for the jurisdiction it is sold, or for
    multiple jurisdictions it could have been sold.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    device_identifier: str = Field(default=..., alias="deviceIdentifier", description="The identifier that is to be associated with every Device that references this DeviceDefintiion for the issuer and jurisdication porvided in the DeviceDefinition.udiDeviceIdentifier.")
    issuer: str = Field(default=..., description="The organization that assigns the identifier algorithm.")
    jurisdiction: str = Field(default=..., description="The jurisdiction to which the deviceIdentifier applies.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("DeviceDefinition", DeviceDefinition)
    register_model("DeviceDefinitionCapability", DeviceDefinitionCapability)
    register_model("DeviceDefinitionClassification", DeviceDefinitionClassification)
    register_model("DeviceDefinitionDeviceName", DeviceDefinitionDeviceName)
    register_model("DeviceDefinitionMaterial", DeviceDefinitionMaterial)
    register_model("DeviceDefinitionProperty", DeviceDefinitionProperty)
    register_model("DeviceDefinitionSpecialization", DeviceDefinitionSpecialization)
    register_model("DeviceDefinitionUdiDeviceIdentifier", DeviceDefinitionUdiDeviceIdentifier)
