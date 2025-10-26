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
    from pymedplum.fhir.reference import Reference


class Communication(MedplumFHIRBase):
    """An occurrence of information being transmitted; e.g. an alert that was
    sent to a responsible provider, a public health agency that was notified
    about a reportable condition.
    """

    resource_type: Literal["Communication"] = Field(
        default="Communication", alias="resourceType"
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
        description="Business identifiers assigned to this communication by the performer or other systems which remain constant as the resource is updated and propagates from server to server.",
    )
    instantiates_canonical: list[str] | None = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this Communication.",
    )
    instantiates_uri: list[str] | None = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this Communication.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="An order, proposal or plan fulfilled in whole or in part by this Communication.",
    )
    part_of: list[Reference] | None = Field(
        default=None, alias="partOf", description="Part of this action."
    )
    in_response_to: list[Reference] | None = Field(
        default=None,
        alias="inResponseTo",
        description="Prior communication that this communication is in response to.",
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
    ] = Field(default=..., description="The status of the transmission.")
    status_reason: CodeableConcept | None = Field(
        default=None,
        alias="statusReason",
        description="Captures the reason for the current state of the Communication.",
    )
    category: list[CodeableConcept] | None = Field(
        default=None,
        description="The type of message conveyed such as alert, notification, reminder, instruction, etc.",
    )
    priority: Literal["routine", "urgent", "asap", "stat"] | None = Field(
        default=None,
        description="Characterizes how quickly the planned or in progress communication must be addressed. Includes concepts such as stat, urgent, routine.",
    )
    medium: list[CodeableConcept] | None = Field(
        default=None,
        description="A channel that was used for this communication (e.g. email, fax).",
    )
    subject: Reference | None = Field(
        default=None,
        description="The patient or group that was the focus of this communication.",
    )
    topic: CodeableConcept | None = Field(
        default=None,
        description="Description of the purpose/content, similar to a subject line in an email.",
    )
    about: list[Reference] | None = Field(
        default=None,
        description="Other resources that pertain to this communication and to which this communication should be associated.",
    )
    encounter: Reference | None = Field(
        default=None,
        description="The Encounter during which this Communication was created or to which the creation of this record is tightly associated.",
    )
    sent: str | None = Field(
        default=None, description="The time when this communication was sent."
    )
    received: str | None = Field(
        default=None,
        description="The time when this communication arrived at the destination.",
    )
    recipient: list[Reference] | None = Field(
        default=None,
        description="The entity (e.g. person, organization, clinical information system, care team or device) which was the target of the communication. If receipts need to be tracked by an individual, a separate resource instance will need to be created for each recipient. Multiple recipient communications are intended where either receipts are not tracked (e.g. a mass mail-out) or a receipt is captured in aggregate (all emails confirmed received by a particular time).",
    )
    sender: Reference | None = Field(
        default=None,
        description="The entity (e.g. person, organization, clinical information system, or device) which was the source of the communication.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="The reason or justification for the communication.",
    )
    reason_reference: list[Reference] | None = Field(
        default=None,
        alias="reasonReference",
        description="Indicates another resource whose existence justifies this communication.",
    )
    payload: list[CommunicationPayload] | None = Field(
        default=None,
        description="Text, attachment(s), or resource(s) that was communicated to the recipient.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Additional notes or commentary about the communication by the sender, receiver or other interested parties.",
    )


class CommunicationPayload(MedplumFHIRBase):
    """Text, attachment(s), or resource(s) that was communicated to the recipient."""

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
    content_string: str | None = Field(
        default=None,
        alias="contentString",
        description="A communicated content (or for multi-part communications, one portion of the communication).",
    )
    content_attachment: Attachment | None = Field(
        default=None,
        alias="contentAttachment",
        description="A communicated content (or for multi-part communications, one portion of the communication).",
    )
    content_reference: Reference | None = Field(
        default=None,
        alias="contentReference",
        description="A communicated content (or for multi-part communications, one portion of the communication).",
    )
