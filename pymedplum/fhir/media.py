# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class Media(MedplumFHIRBase):
    """A photo, video, or audio recording acquired or used in healthcare. The
    actual content may be inline or provided by direct reference.
    """

    resource_type: Literal["Media"] = Field(default="Media", alias="resourceType")

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
        description="Identifiers associated with the image - these may include identifiers for the image itself, identifiers for the context of its collection (e.g. series ids) and context ids such as accession numbers or other workflow identifiers.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="A procedure that is fulfilled in whole or in part by the creation of this media.",
    )
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="A larger event of which this particular event is a component or step.",
    )
    status: Literal[
        "preparation",
        "in-progress",
        "not-done",
        "on-hold",
        "stopped",
        "completed",
        "entered-in-error",
        "unknown",
    ] = Field(default=..., description="The current state of the {{title}}.")
    type: CodeableConcept | None = Field(
        default=None,
        description="A code that classifies whether the media is an image, video or audio recording or some other media category.",
    )
    modality: CodeableConcept | None = Field(
        default=None,
        description="Details of the type of the media - usually, how it was acquired (what type of device). If images sourced from a DICOM system, are wrapped in a Media resource, then this is the modality.",
    )
    view: CodeableConcept | None = Field(
        default=None,
        description="The name of the imaging view e.g. Lateral or Antero-posterior (AP).",
    )
    subject: Reference | None = Field(
        default=None, description="Who/What this Media is a record of."
    )
    encounter: Reference | None = Field(
        default=None,
        description="The encounter that establishes the context for this media.",
    )
    created_date_time: str | None = Field(
        default=None,
        alias="createdDateTime",
        description="The date and time(s) at which the media was collected.",
    )
    created_period: Period | None = Field(
        default=None,
        alias="createdPeriod",
        description="The date and time(s) at which the media was collected.",
    )
    issued: str | None = Field(
        default=None,
        description="The date and time this version of the media was made available to providers, typically after having been reviewed.",
    )
    operator: Reference | None = Field(
        default=None,
        description="The person who administered the collection of the image.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="Describes why the event occurred in coded or textual form.",
    )
    body_site: CodeableConcept | None = Field(
        default=None,
        alias="bodySite",
        description="Indicates the site on the subject's body where the observation was made (i.e. the target site).",
    )
    device_name: str | None = Field(
        default=None,
        alias="deviceName",
        description="The name of the device / manufacturer of the device that was used to make the recording.",
    )
    device: Reference | None = Field(
        default=None, description="The device used to collect the media."
    )
    height: int | float | None = Field(
        default=None, description="Height of the image in pixels (photo/video)."
    )
    width: int | float | None = Field(
        default=None, description="Width of the image in pixels (photo/video)."
    )
    frames: int | float | None = Field(
        default=None,
        description="The number of frames in a photo. This is used with a multi-page fax, or an imaging acquisition context that takes multiple slices in a single image, or an animated gif. If there is more than one frame, this SHALL have a value in order to alert interface software that a multi-frame capable rendering widget is required.",
    )
    duration: int | float | None = Field(
        default=None,
        description="The duration of the recording in seconds - for audio and video.",
    )
    content: Attachment = Field(
        default=...,
        description="The actual content of the media - inline or by direct reference to the media source file.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Comments made about the media by the performer, subject or other participants.",
    )
