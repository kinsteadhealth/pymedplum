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
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class CommunicationRequest(MedplumFHIRBase):
    """A request to convey information; e.g. the CDS system proposes that an
    alert be sent to a responsible provider, the CDS system proposes that
    the public health agency be notified about a reportable condition.
    """

    resource_type: Literal["CommunicationRequest"] = Field(
        default="CommunicationRequest", alias="resourceType"
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
        description="Business identifiers assigned to this communication request by the performer or other systems which remain constant as the resource is updated and propagates from server to server.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="A plan or proposal that is fulfilled in whole or in part by this request.",
    )
    replaces: list[Reference] | None = Field(
        default=None,
        description="Completed or terminated request(s) whose function is taken by this new request.",
    )
    group_identifier: Identifier | None = Field(
        default=None,
        alias="groupIdentifier",
        description="A shared identifier common to all requests that were authorized more or less simultaneously by a single author, representing the identifier of the requisition, prescription or similar form.",
    )
    status: Literal[
        "draft",
        "active",
        "on-hold",
        "revoked",
        "completed",
        "entered-in-error",
        "unknown",
    ] = Field(default=..., description="The status of the proposal or order.")
    status_reason: CodeableConcept | None = Field(
        default=None,
        alias="statusReason",
        description="Captures the reason for the current state of the CommunicationRequest.",
    )
    category: list[CodeableConcept] | None = Field(
        default=None,
        description="The type of message to be sent such as alert, notification, reminder, instruction, etc.",
    )
    priority: Literal["routine", "urgent", "asap", "stat"] | None = Field(
        default=None,
        description="Characterizes how quickly the proposed act must be initiated. Includes concepts such as stat, urgent, routine.",
    )
    do_not_perform: bool | None = Field(
        default=None,
        alias="doNotPerform",
        description="If true indicates that the CommunicationRequest is asking for the specified action to *not* occur.",
    )
    medium: list[CodeableConcept] | None = Field(
        default=None,
        description="A channel that was used for this communication (e.g. email, fax).",
    )
    subject: Reference | None = Field(
        default=None,
        description="The patient or group that is the focus of this communication request.",
    )
    about: list[Reference] | None = Field(
        default=None,
        description="Other resources that pertain to this communication request and to which this communication request should be associated.",
    )
    encounter: Reference | None = Field(
        default=None,
        description="The Encounter during which this CommunicationRequest was created or to which the creation of this record is tightly associated.",
    )
    payload: list[CommunicationRequestPayload] | None = Field(
        default=None,
        description="Text, attachment(s), or resource(s) to be communicated to the recipient.",
    )
    occurrence_date_time: str | None = Field(
        default=None,
        alias="occurrenceDateTime",
        description="The time when this communication is to occur.",
    )
    occurrence_period: Period | None = Field(
        default=None,
        alias="occurrencePeriod",
        description="The time when this communication is to occur.",
    )
    authored_on: str | None = Field(
        default=None,
        alias="authoredOn",
        description="For draft requests, indicates the date of initial creation. For requests with other statuses, indicates the date of activation.",
    )
    requester: Reference | None = Field(
        default=None,
        description="The device, individual, or organization who initiated the request and has responsibility for its activation.",
    )
    recipient: list[Reference] | None = Field(
        default=None,
        description="The entity (e.g. person, organization, clinical information system, device, group, or care team) which is the intended target of the communication.",
    )
    sender: Reference | None = Field(
        default=None,
        description="The entity (e.g. person, organization, clinical information system, or device) which is to be the source of the communication.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="Describes why the request is being made in coded or textual form.",
    )
    reason_reference: list[Reference] | None = Field(
        default=None,
        alias="reasonReference",
        description="Indicates another resource whose existence justifies this request.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Comments made about the request by the requester, sender, recipient, subject or other participants.",
    )


class CommunicationRequestPayload(MedplumFHIRBase):
    """Text, attachment(s), or resource(s) to be communicated to the recipient."""

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
        description="The communicated content (or for multi-part communications, one portion of the communication).",
    )
    content_attachment: Attachment | None = Field(
        default=None,
        alias="contentAttachment",
        description="The communicated content (or for multi-part communications, one portion of the communication).",
    )
    content_reference: Reference | None = Field(
        default=None,
        alias="contentReference",
        description="The communicated content (or for multi-part communications, one portion of the communication).",
    )
