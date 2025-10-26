# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class ImagingStudy(MedplumFHIRBase):
    """Representation of the content produced in a DICOM imaging study. A study
    comprises a set of series, each of which includes a set of
    Service-Object Pair Instances (SOP Instances - images or other data)
    acquired or produced in a common context. A series is of only one
    modality (e.g. X-ray, CT, MR, ultrasound), but a study may have multiple
    series of different modalities.
    """

    resource_type: Literal["ImagingStudy"] = Field(
        default="ImagingStudy", alias="resourceType"
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
        default=None,
        description="Identifiers for the ImagingStudy such as DICOM Study Instance UID, and Accession Number.",
    )
    status: Literal[
        "registered", "available", "cancelled", "entered-in-error", "unknown"
    ] = Field(default=..., description="The current state of the ImagingStudy.")
    modality: list[Coding] | None = Field(
        default=None,
        description="A list of all the series.modality values that are actual acquisition modalities, i.e. those in the DICOM Context Group 29 (value set OID 1.2.840.10008.6.1.19).",
    )
    subject: Reference = Field(
        default=...,
        description="The subject, typically a patient, of the imaging study.",
    )
    encounter: Reference | None = Field(
        default=None,
        description="The healthcare event (e.g. a patient and healthcare provider interaction) during which this ImagingStudy is made.",
    )
    started: str | None = Field(
        default=None, description="Date and time the study started."
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="A list of the diagnostic requests that resulted in this imaging study being performed.",
    )
    referrer: Reference | None = Field(
        default=None, description="The requesting/referring physician."
    )
    interpreter: list[Reference] | None = Field(
        default=None,
        description="Who read the study and interpreted the images or other content.",
    )
    endpoint: list[Reference] | None = Field(
        default=None,
        description="The network service providing access (e.g., query, view, or retrieval) for the study. See implementation notes for information about using DICOM endpoints. A study-level endpoint applies to each series in the study, unless overridden by a series-level endpoint with the same Endpoint.connectionType.",
    )
    number_of_series: int | float | None = Field(
        default=None,
        alias="numberOfSeries",
        description="Number of Series in the Study. This value given may be larger than the number of series elements this Resource contains due to resource availability, security, or other factors. This element should be present if any series elements are present.",
    )
    number_of_instances: int | float | None = Field(
        default=None,
        alias="numberOfInstances",
        description="Number of SOP Instances in Study. This value given may be larger than the number of instance elements this resource contains due to resource availability, security, or other factors. This element should be present if any instance elements are present.",
    )
    procedure_reference: Reference | None = Field(
        default=None,
        alias="procedureReference",
        description="The procedure which this ImagingStudy was part of.",
    )
    procedure_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="procedureCode",
        description="The code for the performed procedure type.",
    )
    location: Reference | None = Field(
        default=None,
        description="The principal physical location where the ImagingStudy was performed.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="Description of clinical condition indicating why the ImagingStudy was requested.",
    )
    reason_reference: list[Reference] | None = Field(
        default=None,
        alias="reasonReference",
        description="Indicates another resource whose existence justifies this Study.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Per the recommended DICOM mapping, this element is derived from the Study Description attribute (0008,1030). Observations or findings about the imaging study should be recorded in another resource, e.g. Observation, and not in this element.",
    )
    description: str | None = Field(
        default=None,
        description="The Imaging Manager description of the study. Institution-generated description or classification of the Study (component) performed.",
    )
    series: list[ImagingStudySeries] | None = Field(
        default=None,
        description="Each study has one or more series of images or other content.",
    )


class ImagingStudySeries(MedplumFHIRBase):
    """Each study has one or more series of images or other content."""

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
    uid: str = Field(
        default=..., description="The DICOM Series Instance UID for the series."
    )
    number: int | float | None = Field(
        default=None, description="The numeric identifier of this series in the study."
    )
    modality: Coding = Field(
        default=..., description="The modality of this series sequence."
    )
    description: str | None = Field(
        default=None, description="A description of the series."
    )
    number_of_instances: int | float | None = Field(
        default=None,
        alias="numberOfInstances",
        description="Number of SOP Instances in the Study. The value given may be larger than the number of instance elements this resource contains due to resource availability, security, or other factors. This element should be present if any instance elements are present.",
    )
    endpoint: list[Reference] | None = Field(
        default=None,
        description="The network service providing access (e.g., query, view, or retrieval) for this series. See implementation notes for information about using DICOM endpoints. A series-level endpoint, if present, has precedence over a study-level endpoint with the same Endpoint.connectionType.",
    )
    body_site: Coding | None = Field(
        default=None,
        alias="bodySite",
        description="The anatomic structures examined. See DICOM Part 16 Annex L (http://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_L.html) for DICOM to SNOMED-CT mappings. The bodySite may indicate the laterality of body part imaged; if so, it shall be consistent with any content of ImagingStudy.series.laterality.",
    )
    laterality: Coding | None = Field(
        default=None,
        description="The laterality of the (possibly paired) anatomic structures examined. E.g., the left knee, both lungs, or unpaired abdomen. If present, shall be consistent with any laterality information indicated in ImagingStudy.series.bodySite.",
    )
    specimen: list[Reference] | None = Field(
        default=None,
        description="The specimen imaged, e.g., for whole slide imaging of a biopsy.",
    )
    started: str | None = Field(
        default=None, description="The date and time the series was started."
    )
    performer: list[ImagingStudySeriesPerformer] | None = Field(
        default=None,
        description="Indicates who or what performed the series and how they were involved.",
    )
    instance: list[ImagingStudySeriesInstance] | None = Field(
        default=None,
        description="A single SOP instance within the series, e.g. an image, or presentation state.",
    )


class ImagingStudySeriesInstance(MedplumFHIRBase):
    """A single SOP instance within the series, e.g. an image, or presentation state."""

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
    uid: str = Field(
        default=...,
        description="The DICOM SOP Instance UID for this image or other DICOM content.",
    )
    sop_class: Coding = Field(
        default=..., alias="sopClass", description="DICOM instance type."
    )
    number: int | float | None = Field(
        default=None, description="The number of instance in the series."
    )
    title: str | None = Field(
        default=None, description="The description of the instance."
    )


class ImagingStudySeriesPerformer(MedplumFHIRBase):
    """Indicates who or what performed the series and how they were involved."""

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
    function: CodeableConcept | None = Field(
        default=None,
        description="Distinguishes the type of involvement of the performer in the series.",
    )
    actor: Reference = Field(
        default=..., description="Indicates who or what performed the series."
    )
