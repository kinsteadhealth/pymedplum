# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.age import Age
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.reference import Reference


class Procedure(MedplumFHIRBase):
    """An action that is or was performed on or for a patient. This can be a
    physical intervention like an operation, or less invasive like long term
    services, counseling, or hypnotherapy.
    """

    resource_type: Literal["Procedure"] = Field(
        default="Procedure", alias="resourceType"
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
        description="Business identifiers assigned to this procedure by the performer or other systems which remain constant as the resource is updated and is propagated from server to server.",
    )
    instantiates_canonical: list[str] | None = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a FHIR-defined protocol, guideline, order set or other definition that is adhered to in whole or in part by this Procedure.",
    )
    instantiates_uri: list[str] | None = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, order set or other definition that is adhered to in whole or in part by this Procedure.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="A reference to a resource that contains details of the request for this procedure.",
    )
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="A larger event of which this particular procedure is a component or step.",
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
    ] = Field(
        default=...,
        description="A code specifying the state of the procedure. Generally, this will be the in-progress or completed state.",
    )
    status_reason: CodeableConcept | None = Field(
        default=None,
        alias="statusReason",
        description="Captures the reason for the current state of the procedure.",
    )
    category: CodeableConcept | None = Field(
        default=None,
        description="A code that classifies the procedure for searching, sorting and display purposes (e.g. &quot;Surgical Procedure&quot;).",
    )
    code: CodeableConcept | None = Field(
        default=None,
        description="The specific procedure that is performed. Use text if the exact nature of the procedure cannot be coded (e.g. &quot;Laparoscopic Appendectomy&quot;).",
    )
    subject: Reference = Field(
        default=...,
        description="The person, animal or group on which the procedure was performed.",
    )
    encounter: Reference | None = Field(
        default=None,
        description="The Encounter during which this Procedure was created or performed or to which the creation of this record is tightly associated.",
    )
    performed_date_time: str | None = Field(
        default=None,
        alias="performedDateTime",
        description="Estimated or actual date, date-time, period, or age when the procedure was performed. Allows a period to support complex procedures that span more than one date, and also allows for the length of the procedure to be captured.",
    )
    performed_period: Period | None = Field(
        default=None,
        alias="performedPeriod",
        description="Estimated or actual date, date-time, period, or age when the procedure was performed. Allows a period to support complex procedures that span more than one date, and also allows for the length of the procedure to be captured.",
    )
    performed_string: str | None = Field(
        default=None,
        alias="performedString",
        description="Estimated or actual date, date-time, period, or age when the procedure was performed. Allows a period to support complex procedures that span more than one date, and also allows for the length of the procedure to be captured.",
    )
    performed_age: Age | None = Field(
        default=None,
        alias="performedAge",
        description="Estimated or actual date, date-time, period, or age when the procedure was performed. Allows a period to support complex procedures that span more than one date, and also allows for the length of the procedure to be captured.",
    )
    performed_range: Range | None = Field(
        default=None,
        alias="performedRange",
        description="Estimated or actual date, date-time, period, or age when the procedure was performed. Allows a period to support complex procedures that span more than one date, and also allows for the length of the procedure to be captured.",
    )
    recorder: Reference | None = Field(
        default=None,
        description="Individual who recorded the record and takes responsibility for its content.",
    )
    asserter: Reference | None = Field(
        default=None, description="Individual who is making the procedure statement."
    )
    performer: list[ProcedurePerformer] | None = Field(
        default=None,
        description="Limited to &quot;real&quot; people rather than equipment.",
    )
    location: Reference | None = Field(
        default=None,
        description="The location where the procedure actually happened. E.g. a newborn at home, a tracheostomy at a restaurant.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="The coded reason why the procedure was performed. This may be a coded entity of some type, or may simply be present as text.",
    )
    reason_reference: list[Reference] | None = Field(
        default=None,
        alias="reasonReference",
        description="The justification of why the procedure was performed.",
    )
    body_site: list[CodeableConcept] | None = Field(
        default=None,
        alias="bodySite",
        description="Detailed and structured anatomical location information. Multiple locations are allowed - e.g. multiple punch biopsies of a lesion.",
    )
    outcome: CodeableConcept | None = Field(
        default=None,
        description="The outcome of the procedure - did it resolve the reasons for the procedure being performed?",
    )
    report: list[Reference] | None = Field(
        default=None,
        description="This could be a histology result, pathology report, surgical report, etc.",
    )
    complication: list[CodeableConcept] | None = Field(
        default=None,
        description="Any complications that occurred during the procedure, or in the immediate post-performance period. These are generally tracked separately from the notes, which will typically describe the procedure itself rather than any 'post procedure' issues.",
    )
    complication_detail: list[Reference] | None = Field(
        default=None,
        alias="complicationDetail",
        description="Any complications that occurred during the procedure, or in the immediate post-performance period.",
    )
    follow_up: list[CodeableConcept] | None = Field(
        default=None,
        alias="followUp",
        description="If the procedure required specific follow up - e.g. removal of sutures. The follow up may be represented as a simple note or could potentially be more complex, in which case the CarePlan resource can be used.",
    )
    note: list[Annotation] | None = Field(
        default=None, description="Any other notes and comments about the procedure."
    )
    focal_device: list[ProcedureFocalDevice] | None = Field(
        default=None,
        alias="focalDevice",
        description="A device that is implanted, removed or otherwise manipulated (calibration, battery replacement, fitting a prosthesis, attaching a wound-vac, etc.) as a focal portion of the Procedure.",
    )
    used_reference: list[Reference] | None = Field(
        default=None,
        alias="usedReference",
        description="Identifies medications, devices and any other substance used as part of the procedure.",
    )
    used_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="usedCode",
        description="Identifies coded items that were used as part of the procedure.",
    )


class ProcedureFocalDevice(MedplumFHIRBase):
    """A device that is implanted, removed or otherwise manipulated
    (calibration, battery replacement, fitting a prosthesis, attaching a
    wound-vac, etc.) as a focal portion of the Procedure.
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
    action: CodeableConcept | None = Field(
        default=None,
        description="The kind of change that happened to the device during the procedure.",
    )
    manipulated: Reference = Field(
        default=...,
        description="The device that was manipulated (changed) during the procedure.",
    )


class ProcedurePerformer(MedplumFHIRBase):
    """Limited to &quot;real&quot; people rather than equipment."""

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
        description="Distinguishes the type of involvement of the performer in the procedure. For example, surgeon, anaesthetist, endoscopist.",
    )
    actor: Reference = Field(
        default=..., description="The practitioner who was involved in the procedure."
    )
    on_behalf_of: Reference | None = Field(
        default=None,
        alias="onBehalfOf",
        description="The organization the device or practitioner was acting on behalf of.",
    )
