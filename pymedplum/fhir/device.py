# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Device(MedplumFHIRBase):
    """A type of a manufactured item that is used in the provision of
    healthcare without being substantially changed through that activity.
    The device may be a medical or non-medical device.
    """

    resource_type: Literal["Device"] = Field(
        default="Device",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[List[Identifier]] = Field(default=None, description="Unique instance identifiers assigned to a device by manufacturers other organizations or owners.")
    definition: Optional[Reference] = Field(default=None, description="The reference to the definition for the device.")
    udi_carrier: Optional[List[DeviceUdiCarrier]] = Field(default=None, alias="udiCarrier", description="Unique device identifier (UDI) assigned to device label or package. Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.")
    status: Optional[Literal['active', 'inactive', 'entered-in-error', 'unknown']] = Field(default=None, description="Status of the Device availability.")
    status_reason: Optional[List[CodeableConcept]] = Field(default=None, alias="statusReason", description="Reason for the dtatus of the Device availability.")
    distinct_identifier: Optional[str] = Field(default=None, alias="distinctIdentifier", description="The distinct identification string as required by regulation for a human cell, tissue, or cellular and tissue-based product.")
    manufacturer: Optional[str] = Field(default=None, description="A name of the manufacturer.")
    manufacture_date: Optional[str] = Field(default=None, alias="manufactureDate", description="The date and time when the device was manufactured.")
    expiration_date: Optional[str] = Field(default=None, alias="expirationDate", description="The date and time beyond which this device is no longer valid or should not be used (if applicable).")
    lot_number: Optional[str] = Field(default=None, alias="lotNumber", description="Lot number assigned by the manufacturer.")
    serial_number: Optional[str] = Field(default=None, alias="serialNumber", description="The serial number assigned by the organization when the device was manufactured.")
    device_name: Optional[List[DeviceDeviceName]] = Field(default=None, alias="deviceName", description="This represents the manufacturer's name of the device as provided by the device, from a UDI label, or by a person describing the Device. This typically would be used when a person provides the name(s) or when the device represents one of the names available from DeviceDefinition.")
    model_number: Optional[str] = Field(default=None, alias="modelNumber", description="The model number for the device.")
    part_number: Optional[str] = Field(default=None, alias="partNumber", description="The part number of the device.")
    type: Optional[CodeableConcept] = Field(default=None, description="The kind or type of device.")
    specialization: Optional[List[DeviceSpecialization]] = Field(default=None, description="The capabilities supported on a device, the standards to which the device conforms for a particular purpose, and used for the communication.")
    version: Optional[List[DeviceVersion]] = Field(default=None, description="The actual design of the device or software version running on the device.")
    property: Optional[List[DeviceProperty]] = Field(default=None, description="The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.")
    patient: Optional[Reference] = Field(default=None, description="Patient information, If the device is affixed to a person.")
    owner: Optional[Reference] = Field(default=None, description="An organization that is responsible for the provision and ongoing maintenance of the device.")
    contact: Optional[List[ContactPoint]] = Field(default=None, description="Contact details for an organization or a particular human that is responsible for the device.")
    location: Optional[Reference] = Field(default=None, description="The place where the device can be found.")
    url: Optional[str] = Field(default=None, description="A network address on which the device may be contacted directly.")
    note: Optional[List[Annotation]] = Field(default=None, description="Descriptive information, usage information or implantation information that is not captured in an existing element.")
    safety: Optional[List[CodeableConcept]] = Field(default=None, description="Provides additional safety characteristics about a medical device. For example devices containing latex.")
    parent: Optional[Reference] = Field(default=None, description="The parent device.")


class DeviceDeviceName(MedplumFHIRBase):
    """This represents the manufacturer's name of the device as provided by the
    device, from a UDI label, or by a person describing the Device. This
    typically would be used when a person provides the name(s) or when the
    device represents one of the names available from DeviceDefinition.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="The name of the device.")
    type: Literal['udi-label-name', 'user-friendly-name', 'patient-reported-name', 'manufacturer-name', 'model-name', 'other'] = Field(default=..., description="The type of deviceName. UDILabelName | UserFriendlyName | PatientReportedName | ManufactureDeviceName | ModelName.")


class DeviceProperty(MedplumFHIRBase):
    """The actual configuration settings of a device as it actually operates,
    e.g., regulation status, time properties.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: CodeableConcept = Field(default=..., description="Code that specifies the property DeviceDefinitionPropetyCode (Extensible).")
    value_quantity: Optional[List[Quantity]] = Field(default=None, alias="valueQuantity", description="Property value as a quantity.")
    value_code: Optional[List[CodeableConcept]] = Field(default=None, alias="valueCode", description="Property value as a code, e.g., NTP4 (synced to NTP).")


class DeviceSpecialization(MedplumFHIRBase):
    """The capabilities supported on a device, the standards to which the
    device conforms for a particular purpose, and used for the
    communication.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    system_type: CodeableConcept = Field(default=..., alias="systemType", description="The standard that is used to operate and communicate.")
    version: Optional[str] = Field(default=None, description="The version of the standard that is used to operate and communicate.")


class DeviceUdiCarrier(MedplumFHIRBase):
    """Unique device identifier (UDI) assigned to device label or package. Note
    that the Device may include multiple udiCarriers as it either may
    include just the udiCarrier for the jurisdiction it is sold, or for
    multiple jurisdictions it could have been sold.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    device_identifier: Optional[str] = Field(default=None, alias="deviceIdentifier", description="The device identifier (DI) is a mandatory, fixed portion of a UDI that identifies the labeler and the specific version or model of a device.")
    issuer: Optional[str] = Field(default=None, description="Organization that is charged with issuing UDIs for devices. For example, the US FDA issuers include : 1) GS1: http://hl7.org/fhir/NamingSystem/gs1-di, 2) HIBCC: http://hl7.org/fhir/NamingSystem/hibcc-dI, 3) ICCBBA for blood containers: http://hl7.org/fhir/NamingSystem/iccbba-blood-di, 4) ICCBA for other devices: http://hl7.org/fhir/NamingSystem/iccbba-other-di.")
    jurisdiction: Optional[str] = Field(default=None, description="The identity of the authoritative source for UDI generation within a jurisdiction. All UDIs are globally unique within a single namespace with the appropriate repository uri as the system. For example, UDIs of devices managed in the U.S. by the FDA, the value is http://hl7.org/fhir/NamingSystem/fda-udi.")
    carrier_a_i_d_c: Optional[str] = Field(default=None, alias="carrierAIDC", description="The full UDI carrier of the Automatic Identification and Data Capture (AIDC) technology representation of the barcode string as printed on the packaging of the device - e.g., a barcode or RFID. Because of limitations on character sets in XML and the need to round-trip JSON data through XML, AIDC Formats *SHALL* be base64 encoded.")
    carrier_h_r_f: Optional[str] = Field(default=None, alias="carrierHRF", description="The full UDI carrier as the human readable form (HRF) representation of the barcode string as printed on the packaging of the device.")
    entry_type: Optional[Literal['barcode', 'rfid', 'manual', 'card', 'self-reported', 'unknown']] = Field(default=None, alias="entryType", description="A coded entry to indicate how the data was entered.")


class DeviceVersion(MedplumFHIRBase):
    """The actual design of the device or software version running on the device."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: Optional[CodeableConcept] = Field(default=None, description="The type of the device version.")
    component: Optional[Identifier] = Field(default=None, description="A single component of the device version.")
    value: str = Field(default=..., description="The version text.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Device", Device)
    register_model("DeviceDeviceName", DeviceDeviceName)
    register_model("DeviceProperty", DeviceProperty)
    register_model("DeviceSpecialization", DeviceSpecialization)
    register_model("DeviceUdiCarrier", DeviceUdiCarrier)
    register_model("DeviceVersion", DeviceVersion)
