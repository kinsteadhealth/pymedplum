# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class Device(MedplumFHIRBase):
    """A type of a manufactured item that is used in the provision of
    healthcare without being substantially changed through that activity.
    The device may be a medical or non-medical device.
    """

    resource_type: Literal["Device"] = Field(default="Device", alias="resourceType")

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
        default=None,
        description="Unique instance identifiers assigned to a device by manufacturers other organizations or owners.",
    )
    definition: Reference | None = Field(
        default=None, description="The reference to the definition for the device."
    )
    udi_carrier: list[DeviceUdiCarrier] | None = Field(
        default=None,
        alias="udiCarrier",
        description="Unique device identifier (UDI) assigned to device label or package. Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.",
    )
    status: Literal["active", "inactive", "entered-in-error", "unknown"] | None = Field(
        default=None, description="Status of the Device availability."
    )
    status_reason: list[CodeableConcept] | None = Field(
        default=None,
        alias="statusReason",
        description="Reason for the dtatus of the Device availability.",
    )
    distinct_identifier: str | None = Field(
        default=None,
        alias="distinctIdentifier",
        description="The distinct identification string as required by regulation for a human cell, tissue, or cellular and tissue-based product.",
    )
    manufacturer: str | None = Field(
        default=None, description="A name of the manufacturer."
    )
    manufacture_date: str | None = Field(
        default=None,
        alias="manufactureDate",
        description="The date and time when the device was manufactured.",
    )
    expiration_date: str | None = Field(
        default=None,
        alias="expirationDate",
        description="The date and time beyond which this device is no longer valid or should not be used (if applicable).",
    )
    lot_number: str | None = Field(
        default=None,
        alias="lotNumber",
        description="Lot number assigned by the manufacturer.",
    )
    serial_number: str | None = Field(
        default=None,
        alias="serialNumber",
        description="The serial number assigned by the organization when the device was manufactured.",
    )
    device_name: list[DeviceDeviceName] | None = Field(
        default=None,
        alias="deviceName",
        description="This represents the manufacturer's name of the device as provided by the device, from a UDI label, or by a person describing the Device. This typically would be used when a person provides the name(s) or when the device represents one of the names available from DeviceDefinition.",
    )
    model_number: str | None = Field(
        default=None,
        alias="modelNumber",
        description="The model number for the device.",
    )
    part_number: str | None = Field(
        default=None, alias="partNumber", description="The part number of the device."
    )
    type: CodeableConcept | None = Field(
        default=None, description="The kind or type of device."
    )
    specialization: list[DeviceSpecialization] | None = Field(
        default=None,
        description="The capabilities supported on a device, the standards to which the device conforms for a particular purpose, and used for the communication.",
    )
    version: list[DeviceVersion] | None = Field(
        default=None,
        description="The actual design of the device or software version running on the device.",
    )
    property: list[DeviceProperty] | None = Field(
        default=None,
        description="The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.",
    )
    patient: Reference | None = Field(
        default=None,
        description="Patient information, If the device is affixed to a person.",
    )
    owner: Reference | None = Field(
        default=None,
        description="An organization that is responsible for the provision and ongoing maintenance of the device.",
    )
    contact: list[ContactPoint] | None = Field(
        default=None,
        description="Contact details for an organization or a particular human that is responsible for the device.",
    )
    location: Reference | None = Field(
        default=None, description="The place where the device can be found."
    )
    url: str | None = Field(
        default=None,
        description="A network address on which the device may be contacted directly.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Descriptive information, usage information or implantation information that is not captured in an existing element.",
    )
    safety: list[CodeableConcept] | None = Field(
        default=None,
        description="Provides additional safety characteristics about a medical device. For example devices containing latex.",
    )
    parent: Reference | None = Field(default=None, description="The parent device.")


class DeviceDeviceName(MedplumFHIRBase):
    """This represents the manufacturer's name of the device as provided by the
    device, from a UDI label, or by a person describing the Device. This
    typically would be used when a person provides the name(s) or when the
    device represents one of the names available from DeviceDefinition.
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
    name: str = Field(default=..., description="The name of the device.")
    type: Literal[
        "udi-label-name",
        "user-friendly-name",
        "patient-reported-name",
        "manufacturer-name",
        "model-name",
        "other",
    ] = Field(
        default=...,
        description="The type of deviceName. UDILabelName | UserFriendlyName | PatientReportedName | ManufactureDeviceName | ModelName.",
    )


class DeviceProperty(MedplumFHIRBase):
    """The actual configuration settings of a device as it actually operates,
    e.g., regulation status, time properties.
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
        default=...,
        description="Code that specifies the property DeviceDefinitionPropetyCode (Extensible).",
    )
    value_quantity: list[Quantity] | None = Field(
        default=None, alias="valueQuantity", description="Property value as a quantity."
    )
    value_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="valueCode",
        description="Property value as a code, e.g., NTP4 (synced to NTP).",
    )


class DeviceSpecialization(MedplumFHIRBase):
    """The capabilities supported on a device, the standards to which the
    device conforms for a particular purpose, and used for the
    communication.
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
    system_type: CodeableConcept = Field(
        default=...,
        alias="systemType",
        description="The standard that is used to operate and communicate.",
    )
    version: str | None = Field(
        default=None,
        description="The version of the standard that is used to operate and communicate.",
    )


class DeviceUdiCarrier(MedplumFHIRBase):
    """Unique device identifier (UDI) assigned to device label or package. Note
    that the Device may include multiple udiCarriers as it either may
    include just the udiCarrier for the jurisdiction it is sold, or for
    multiple jurisdictions it could have been sold.
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
    device_identifier: str | None = Field(
        default=None,
        alias="deviceIdentifier",
        description="The device identifier (DI) is a mandatory, fixed portion of a UDI that identifies the labeler and the specific version or model of a device.",
    )
    issuer: str | None = Field(
        default=None,
        description="Organization that is charged with issuing UDIs for devices. For example, the US FDA issuers include : 1) GS1: http://hl7.org/fhir/NamingSystem/gs1-di, 2) HIBCC: http://hl7.org/fhir/NamingSystem/hibcc-dI, 3) ICCBBA for blood containers: http://hl7.org/fhir/NamingSystem/iccbba-blood-di, 4) ICCBA for other devices: http://hl7.org/fhir/NamingSystem/iccbba-other-di.",
    )
    jurisdiction: str | None = Field(
        default=None,
        description="The identity of the authoritative source for UDI generation within a jurisdiction. All UDIs are globally unique within a single namespace with the appropriate repository uri as the system. For example, UDIs of devices managed in the U.S. by the FDA, the value is http://hl7.org/fhir/NamingSystem/fda-udi.",
    )
    carrier_a_i_d_c: str | None = Field(
        default=None,
        alias="carrierAIDC",
        description="The full UDI carrier of the Automatic Identification and Data Capture (AIDC) technology representation of the barcode string as printed on the packaging of the device - e.g., a barcode or RFID. Because of limitations on character sets in XML and the need to round-trip JSON data through XML, AIDC Formats *SHALL* be base64 encoded.",
    )
    carrier_h_r_f: str | None = Field(
        default=None,
        alias="carrierHRF",
        description="The full UDI carrier as the human readable form (HRF) representation of the barcode string as printed on the packaging of the device.",
    )
    entry_type: (
        Literal["barcode", "rfid", "manual", "card", "self-reported", "unknown"] | None
    ) = Field(
        default=None,
        alias="entryType",
        description="A coded entry to indicate how the data was entered.",
    )


class DeviceVersion(MedplumFHIRBase):
    """The actual design of the device or software version running on the device."""

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
        default=None, description="The type of the device version."
    )
    component: Identifier | None = Field(
        default=None, description="A single component of the device version."
    )
    value: str = Field(default=..., description="The version text.")
