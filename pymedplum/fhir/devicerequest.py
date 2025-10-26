# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class DeviceRequest(MedplumFHIRBase):
    """Represents a request for a patient to employ a medical device. The
    device may be an implantable device, or an external assistive device,
    such as a walker.
    """

    resource_type: Literal["DeviceRequest"] = Field(
        default="DeviceRequest",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Identifiers assigned to this order by the orderer or by the receiver.")
    instantiates_canonical: Optional[list[str]] = Field(default=None, alias="instantiatesCanonical", description="The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this DeviceRequest.")
    instantiates_uri: Optional[list[str]] = Field(default=None, alias="instantiatesUri", description="The URL pointing to an externally maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this DeviceRequest.")
    based_on: Optional[list[Reference]] = Field(default=None, alias="basedOn", description="Plan/proposal/order fulfilled by this request.")
    prior_request: Optional[list[Reference]] = Field(default=None, alias="priorRequest", description="The request takes the place of the referenced completed or terminated request(s).")
    group_identifier: Optional[Identifier] = Field(default=None, alias="groupIdentifier", description="Composite request this is part of.")
    status: Optional[Literal['draft', 'active', 'on-hold', 'revoked', 'completed', 'entered-in-error', 'unknown']] = Field(default=None, description="The status of the request.")
    intent: Literal['proposal', 'plan', 'directive', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'] = Field(default=..., description="Whether the request is a proposal, plan, an original order or a reflex order.")
    priority: Optional[Literal['routine', 'urgent', 'asap', 'stat']] = Field(default=None, description="Indicates how quickly the {{title}} should be addressed with respect to other requests.")
    code_reference: Optional[Reference] = Field(default=None, alias="codeReference", description="The details of the device to be used.")
    code_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="codeCodeableConcept", description="The details of the device to be used.")
    parameter: Optional[list[DeviceRequestParameter]] = Field(default=None, description="Specific parameters for the ordered item. For example, the prism value for lenses.")
    subject: Reference = Field(default=..., description="The patient who will use the device.")
    encounter: Optional[Reference] = Field(default=None, description="An encounter that provides additional context in which this request is made.")
    occurrence_date_time: Optional[str] = Field(default=None, alias="occurrenceDateTime", description="The timing schedule for the use of the device. The Schedule data type allows many different expressions, for example. &quot;Every 8 hours&quot;; &quot;Three times a day&quot;; &quot;1/2 an hour before breakfast for 10 days from 23-Dec 2011:&quot;; &quot;15 Oct 2013, 17 Oct 2013 and 1 Nov 2013&quot;.")
    occurrence_period: Optional[Period] = Field(default=None, alias="occurrencePeriod", description="The timing schedule for the use of the device. The Schedule data type allows many different expressions, for example. &quot;Every 8 hours&quot;; &quot;Three times a day&quot;; &quot;1/2 an hour before breakfast for 10 days from 23-Dec 2011:&quot;; &quot;15 Oct 2013, 17 Oct 2013 and 1 Nov 2013&quot;.")
    occurrence_timing: Optional[Timing] = Field(default=None, alias="occurrenceTiming", description="The timing schedule for the use of the device. The Schedule data type allows many different expressions, for example. &quot;Every 8 hours&quot;; &quot;Three times a day&quot;; &quot;1/2 an hour before breakfast for 10 days from 23-Dec 2011:&quot;; &quot;15 Oct 2013, 17 Oct 2013 and 1 Nov 2013&quot;.")
    authored_on: Optional[str] = Field(default=None, alias="authoredOn", description="When the request transitioned to being actionable.")
    requester: Optional[Reference] = Field(default=None, description="The individual who initiated the request and has responsibility for its activation.")
    performer_type: Optional[CodeableConcept] = Field(default=None, alias="performerType", description="Desired type of performer for doing the diagnostic testing.")
    performer: Optional[Reference] = Field(default=None, description="The desired performer for doing the diagnostic testing.")
    reason_code: Optional[list[CodeableConcept]] = Field(default=None, alias="reasonCode", description="Reason or justification for the use of this device.")
    reason_reference: Optional[list[Reference]] = Field(default=None, alias="reasonReference", description="Reason or justification for the use of this device.")
    insurance: Optional[list[Reference]] = Field(default=None, description="Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be required for delivering the requested service.")
    supporting_info: Optional[list[Reference]] = Field(default=None, alias="supportingInfo", description="Additional clinical information about the patient that may influence the request fulfilment. For example, this may include where on the subject's body the device will be used (i.e. the target site).")
    note: Optional[list[Annotation]] = Field(default=None, description="Details about this request that were not represented at all or sufficiently in one of the attributes provided in a class. These may include for example a comment, an instruction, or a note associated with the statement.")
    relevant_history: Optional[list[Reference]] = Field(default=None, alias="relevantHistory", description="Key events in the history of the request.")


class DeviceRequestParameter(MedplumFHIRBase):
    """Specific parameters for the ordered item. For example, the prism value for lenses."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="A code or string that identifies the device detail being asserted.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="The value of the device detail.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="The value of the device detail.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="The value of the device detail.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="The value of the device detail.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("DeviceRequest", DeviceRequest)
    register_model("DeviceRequestParameter", DeviceRequestParameter)
