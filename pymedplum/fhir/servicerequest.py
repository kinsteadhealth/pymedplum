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
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.timing import Timing


class ServiceRequest(MedplumFHIRBase):
    """A record of a request for service such as diagnostic investigations,
    treatments, or operations to be performed.
    """

    resource_type: Literal["ServiceRequest"] = Field(
        default="ServiceRequest", alias="resourceType"
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
        description="Identifiers assigned to this order instance by the orderer and/or the receiver and/or order fulfiller.",
    )
    instantiates_canonical: list[str] | None = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a FHIR-defined protocol, guideline, orderset or other definition that is adhered to in whole or in part by this ServiceRequest.",
    )
    instantiates_uri: list[str] | None = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this ServiceRequest.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="Plan/proposal/order fulfilled by this request.",
    )
    replaces: list[Reference] | None = Field(
        default=None,
        description="The request takes the place of the referenced completed or terminated request(s).",
    )
    requisition: Identifier | None = Field(
        default=None,
        description="A shared identifier common to all service requests that were authorized more or less simultaneously by a single author, representing the composite or group identifier.",
    )
    status: Literal[
        "draft",
        "active",
        "on-hold",
        "revoked",
        "completed",
        "entered-in-error",
        "unknown",
    ] = Field(default=..., description="The status of the order.")
    intent: Literal[
        "proposal",
        "plan",
        "directive",
        "order",
        "original-order",
        "reflex-order",
        "filler-order",
        "instance-order",
        "option",
    ] = Field(
        default=...,
        description="Whether the request is a proposal, plan, an original order or a reflex order.",
    )
    category: list[CodeableConcept] | None = Field(
        default=None,
        description="A code that classifies the service for searching, sorting and display purposes (e.g. &quot;Surgical Procedure&quot;).",
    )
    priority: Literal["routine", "urgent", "asap", "stat"] | None = Field(
        default=None,
        description="Indicates how quickly the ServiceRequest should be addressed with respect to other requests.",
    )
    do_not_perform: bool | None = Field(
        default=None,
        alias="doNotPerform",
        description="Set this to true if the record is saying that the service/procedure should NOT be performed.",
    )
    code: CodeableConcept | None = Field(
        default=None,
        description="A code that identifies a particular service (i.e., procedure, diagnostic investigation, or panel of investigations) that have been requested.",
    )
    order_detail: list[CodeableConcept] | None = Field(
        default=None,
        alias="orderDetail",
        description="Additional details and instructions about the how the services are to be delivered. For example, and order for a urinary catheter may have an order detail for an external or indwelling catheter, or an order for a bandage may require additional instructions specifying how the bandage should be applied.",
    )
    quantity_quantity: Quantity | None = Field(
        default=None,
        alias="quantityQuantity",
        description="An amount of service being requested which can be a quantity ( for example $1,500 home modification), a ratio ( for example, 20 half day visits per month), or a range (2.0 to 1.8 Gy per fraction).",
    )
    quantity_ratio: Ratio | None = Field(
        default=None,
        alias="quantityRatio",
        description="An amount of service being requested which can be a quantity ( for example $1,500 home modification), a ratio ( for example, 20 half day visits per month), or a range (2.0 to 1.8 Gy per fraction).",
    )
    quantity_range: Range | None = Field(
        default=None,
        alias="quantityRange",
        description="An amount of service being requested which can be a quantity ( for example $1,500 home modification), a ratio ( for example, 20 half day visits per month), or a range (2.0 to 1.8 Gy per fraction).",
    )
    subject: Reference = Field(
        default=...,
        description="On whom or what the service is to be performed. This is usually a human patient, but can also be requested on animals, groups of humans or animals, devices such as dialysis machines, or even locations (typically for environmental scans).",
    )
    encounter: Reference | None = Field(
        default=None,
        description="An encounter that provides additional information about the healthcare context in which this request is made.",
    )
    occurrence_date_time: str | None = Field(
        default=None,
        alias="occurrenceDateTime",
        description="The date/time at which the requested service should occur.",
    )
    occurrence_period: Period | None = Field(
        default=None,
        alias="occurrencePeriod",
        description="The date/time at which the requested service should occur.",
    )
    occurrence_timing: Timing | None = Field(
        default=None,
        alias="occurrenceTiming",
        description="The date/time at which the requested service should occur.",
    )
    as_needed_boolean: bool | None = Field(
        default=None,
        alias="asNeededBoolean",
        description="If a CodeableConcept is present, it indicates the pre-condition for performing the service. For example &quot;pain&quot;, &quot;on flare-up&quot;, etc.",
    )
    as_needed_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="asNeededCodeableConcept",
        description="If a CodeableConcept is present, it indicates the pre-condition for performing the service. For example &quot;pain&quot;, &quot;on flare-up&quot;, etc.",
    )
    authored_on: str | None = Field(
        default=None,
        alias="authoredOn",
        description="When the request transitioned to being actionable.",
    )
    requester: Reference | None = Field(
        default=None,
        description="The individual who initiated the request and has responsibility for its activation.",
    )
    performer_type: CodeableConcept | None = Field(
        default=None,
        alias="performerType",
        description="Desired type of performer for doing the requested service.",
    )
    performer: list[Reference] | None = Field(
        default=None,
        description="The desired performer for doing the requested service. For example, the surgeon, dermatopathologist, endoscopist, etc.",
    )
    location_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="locationCode",
        description="The preferred location(s) where the procedure should actually happen in coded or free text form. E.g. at home or nursing day care center.",
    )
    location_reference: list[Reference] | None = Field(
        default=None,
        alias="locationReference",
        description="A reference to the the preferred location(s) where the procedure should actually happen. E.g. at home or nursing day care center.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="An explanation or justification for why this service is being requested in coded or textual form. This is often for billing purposes. May relate to the resources referred to in `supportingInfo`.",
    )
    reason_reference: list[Reference] | None = Field(
        default=None,
        alias="reasonReference",
        description="Indicates another resource that provides a justification for why this service is being requested. May relate to the resources referred to in `supportingInfo`.",
    )
    insurance: list[Reference] | None = Field(
        default=None,
        description="Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be needed for delivering the requested service.",
    )
    supporting_info: list[Reference] | None = Field(
        default=None,
        alias="supportingInfo",
        description="Additional clinical information about the patient or specimen that may influence the services or their interpretations. This information includes diagnosis, clinical findings and other observations. In laboratory ordering these are typically referred to as &quot;ask at order entry questions (AOEs)&quot;. This includes observations explicitly requested by the producer (filler) to provide context or supporting information needed to complete the order. For example, reporting the amount of inspired oxygen for blood gas measurements.",
    )
    specimen: list[Reference] | None = Field(
        default=None,
        description="One or more specimens that the laboratory procedure will use.",
    )
    body_site: list[CodeableConcept] | None = Field(
        default=None,
        alias="bodySite",
        description="Anatomic location where the procedure should be performed. This is the target site.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Any other notes and comments made about the service request. For example, internal billing notes.",
    )
    patient_instruction: str | None = Field(
        default=None,
        alias="patientInstruction",
        description="Instructions in terms that are understood by the patient or consumer.",
    )
    relevant_history: list[Reference] | None = Field(
        default=None,
        alias="relevantHistory",
        description="Key events in the history of the request.",
    )
