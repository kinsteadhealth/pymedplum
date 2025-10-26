# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class ImagingStudy(MedplumFHIRBase):
    """Representation of the content produced in a DICOM imaging study. A study
    comprises a set of series, each of which includes a set of
    Service-Object Pair Instances (SOP Instances - images or other data)
    acquired or produced in a common context. A series is of only one
    modality (e.g. X-ray, CT, MR, ultrasound), but a study may have multiple
    series of different modalities.
    """

    resource_type: Literal["ImagingStudy"] = Field(
        default="ImagingStudy",
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
    identifier: Optional[List[Identifier]] = Field(default=None, description="Identifiers for the ImagingStudy such as DICOM Study Instance UID, and Accession Number.")
    status: Literal['registered', 'available', 'cancelled', 'entered-in-error', 'unknown'] = Field(default=..., description="The current state of the ImagingStudy.")
    modality: Optional[List[Coding]] = Field(default=None, description="A list of all the series.modality values that are actual acquisition modalities, i.e. those in the DICOM Context Group 29 (value set OID 1.2.840.10008.6.1.19).")
    subject: Reference = Field(default=..., description="The subject, typically a patient, of the imaging study.")
    encounter: Optional[Reference] = Field(default=None, description="The healthcare event (e.g. a patient and healthcare provider interaction) during which this ImagingStudy is made.")
    started: Optional[str] = Field(default=None, description="Date and time the study started.")
    based_on: Optional[List[Reference]] = Field(default=None, alias="basedOn", description="A list of the diagnostic requests that resulted in this imaging study being performed.")
    referrer: Optional[Reference] = Field(default=None, description="The requesting/referring physician.")
    interpreter: Optional[List[Reference]] = Field(default=None, description="Who read the study and interpreted the images or other content.")
    endpoint: Optional[List[Reference]] = Field(default=None, description="The network service providing access (e.g., query, view, or retrieval) for the study. See implementation notes for information about using DICOM endpoints. A study-level endpoint applies to each series in the study, unless overridden by a series-level endpoint with the same Endpoint.connectionType.")
    number_of_series: Optional[Union[int, float]] = Field(default=None, alias="numberOfSeries", description="Number of Series in the Study. This value given may be larger than the number of series elements this Resource contains due to resource availability, security, or other factors. This element should be present if any series elements are present.")
    number_of_instances: Optional[Union[int, float]] = Field(default=None, alias="numberOfInstances", description="Number of SOP Instances in Study. This value given may be larger than the number of instance elements this resource contains due to resource availability, security, or other factors. This element should be present if any instance elements are present.")
    procedure_reference: Optional[Reference] = Field(default=None, alias="procedureReference", description="The procedure which this ImagingStudy was part of.")
    procedure_code: Optional[List[CodeableConcept]] = Field(default=None, alias="procedureCode", description="The code for the performed procedure type.")
    location: Optional[Reference] = Field(default=None, description="The principal physical location where the ImagingStudy was performed.")
    reason_code: Optional[List[CodeableConcept]] = Field(default=None, alias="reasonCode", description="Description of clinical condition indicating why the ImagingStudy was requested.")
    reason_reference: Optional[List[Reference]] = Field(default=None, alias="reasonReference", description="Indicates another resource whose existence justifies this Study.")
    note: Optional[List[Annotation]] = Field(default=None, description="Per the recommended DICOM mapping, this element is derived from the Study Description attribute (0008,1030). Observations or findings about the imaging study should be recorded in another resource, e.g. Observation, and not in this element.")
    description: Optional[str] = Field(default=None, description="The Imaging Manager description of the study. Institution-generated description or classification of the Study (component) performed.")
    series: Optional[List[ImagingStudySeries]] = Field(default=None, description="Each study has one or more series of images or other content.")


class ImagingStudySeries(MedplumFHIRBase):
    """Each study has one or more series of images or other content."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    uid: str = Field(default=..., description="The DICOM Series Instance UID for the series.")
    number: Optional[Union[int, float]] = Field(default=None, description="The numeric identifier of this series in the study.")
    modality: Coding = Field(default=..., description="The modality of this series sequence.")
    description: Optional[str] = Field(default=None, description="A description of the series.")
    number_of_instances: Optional[Union[int, float]] = Field(default=None, alias="numberOfInstances", description="Number of SOP Instances in the Study. The value given may be larger than the number of instance elements this resource contains due to resource availability, security, or other factors. This element should be present if any instance elements are present.")
    endpoint: Optional[List[Reference]] = Field(default=None, description="The network service providing access (e.g., query, view, or retrieval) for this series. See implementation notes for information about using DICOM endpoints. A series-level endpoint, if present, has precedence over a study-level endpoint with the same Endpoint.connectionType.")
    body_site: Optional[Coding] = Field(default=None, alias="bodySite", description="The anatomic structures examined. See DICOM Part 16 Annex L (http://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_L.html) for DICOM to SNOMED-CT mappings. The bodySite may indicate the laterality of body part imaged; if so, it shall be consistent with any content of ImagingStudy.series.laterality.")
    laterality: Optional[Coding] = Field(default=None, description="The laterality of the (possibly paired) anatomic structures examined. E.g., the left knee, both lungs, or unpaired abdomen. If present, shall be consistent with any laterality information indicated in ImagingStudy.series.bodySite.")
    specimen: Optional[List[Reference]] = Field(default=None, description="The specimen imaged, e.g., for whole slide imaging of a biopsy.")
    started: Optional[str] = Field(default=None, description="The date and time the series was started.")
    performer: Optional[List[ImagingStudySeriesPerformer]] = Field(default=None, description="Indicates who or what performed the series and how they were involved.")
    instance: Optional[List[ImagingStudySeriesInstance]] = Field(default=None, description="A single SOP instance within the series, e.g. an image, or presentation state.")


class ImagingStudySeriesInstance(MedplumFHIRBase):
    """A single SOP instance within the series, e.g. an image, or presentation state."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    uid: str = Field(default=..., description="The DICOM SOP Instance UID for this image or other DICOM content.")
    sop_class: Coding = Field(default=..., alias="sopClass", description="DICOM instance type.")
    number: Optional[Union[int, float]] = Field(default=None, description="The number of instance in the series.")
    title: Optional[str] = Field(default=None, description="The description of the instance.")


class ImagingStudySeriesPerformer(MedplumFHIRBase):
    """Indicates who or what performed the series and how they were involved."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    function: Optional[CodeableConcept] = Field(default=None, description="Distinguishes the type of involvement of the performer in the series.")
    actor: Reference = Field(default=..., description="Indicates who or what performed the series.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ImagingStudy", ImagingStudy)
    register_model("ImagingStudySeries", ImagingStudySeries)
    register_model("ImagingStudySeriesInstance", ImagingStudySeriesInstance)
    register_model("ImagingStudySeriesPerformer", ImagingStudySeriesPerformer)
