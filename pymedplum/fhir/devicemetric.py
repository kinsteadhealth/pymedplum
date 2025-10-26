# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class DeviceMetric(MedplumFHIRBase):
    """Describes a measurement, calculation or setting capability of a medical device."""

    resource_type: Literal["DeviceMetric"] = Field(
        default="DeviceMetric",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Unique instance identifiers assigned to a device by the device or gateway software, manufacturers, other organizations or owners. For example: handle ID.")
    type: CodeableConcept = Field(default=..., description="Describes the type of the metric. For example: Heart Rate, PEEP Setting, etc.")
    unit: Optional[CodeableConcept] = Field(default=None, description="Describes the unit that an observed value determined for this metric will have. For example: Percent, Seconds, etc.")
    source: Optional[Reference] = Field(default=None, description="Describes the link to the Device that this DeviceMetric belongs to and that contains administrative device information such as manufacturer, serial number, etc.")
    parent: Optional[Reference] = Field(default=None, description="Describes the link to the Device that this DeviceMetric belongs to and that provide information about the location of this DeviceMetric in the containment structure of the parent Device. An example would be a Device that represents a Channel. This reference can be used by a client application to distinguish DeviceMetrics that have the same type, but should be interpreted based on their containment location.")
    operational_status: Optional[Literal['on', 'off', 'standby', 'entered-in-error']] = Field(default=None, alias="operationalStatus", description="Indicates current operational state of the device. For example: On, Off, Standby, etc.")
    color: Optional[Literal['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']] = Field(default=None, description="Describes the color representation for the metric. This is often used to aid clinicians to track and identify parameter types by color. In practice, consider a Patient Monitor that has ECG/HR and Pleth for example; the parameters are displayed in different characteristic colors, such as HR-blue, BP-green, and PR and SpO2- magenta.")
    category: Literal['measurement', 'setting', 'calculation', 'unspecified'] = Field(default=..., description="Indicates the category of the observation generation process. A DeviceMetric can be for example a setting, measurement, or calculation.")
    measurement_period: Optional[Timing] = Field(default=None, alias="measurementPeriod", description="Describes the measurement repetition time. This is not necessarily the same as the update period. The measurement repetition time can range from milliseconds up to hours. An example for a measurement repetition time in the range of milliseconds is the sampling rate of an ECG. An example for a measurement repetition time in the range of hours is a NIBP that is triggered automatically every hour. The update period may be different than the measurement repetition time, if the device does not update the published observed value with the same frequency as it was measured.")
    calibration: Optional[list[DeviceMetricCalibration]] = Field(default=None, description="Describes the calibrations that have been performed or that are required to be performed.")


class DeviceMetricCalibration(MedplumFHIRBase):
    """Describes the calibrations that have been performed or that are required
    to be performed.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: Optional[Literal['unspecified', 'offset', 'gain', 'two-point']] = Field(default=None, description="Describes the type of the calibration method.")
    state: Optional[Literal['not-calibrated', 'calibration-required', 'calibrated', 'unspecified']] = Field(default=None, description="Describes the state of the calibration.")
    time: Optional[str] = Field(default=None, description="Describes the time last calibration has been performed.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("DeviceMetric", DeviceMetric)
    register_model("DeviceMetricCalibration", DeviceMetricCalibration)
