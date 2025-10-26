# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class MedicationRequest(MedplumFHIRBase):
    """An order or request for both supply of the medication and the
    instructions for administration of the medication to a patient. The
    resource is called &quot;MedicationRequest&quot; rather than
    &quot;MedicationPrescription&quot; or &quot;MedicationOrder&quot; to
    generalize the use across inpatient and outpatient settings, including
    care plans, etc., and to harmonize with workflow patterns.
    """

    resource_type: Literal["MedicationRequest"] = Field(
        default="MedicationRequest", alias="resourceType"
    )

    id: Optional[str] = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Optional[Meta] = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: Optional[str] = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: Optional[str] = Field(
        default=None, description="The base language in which the resource is written."
    )
    text: Optional[Narrative] = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: Optional[List[Resource]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="Identifiers associated with this medication request that are defined by business processes and/or used to refer to it when a direct URL reference to the resource itself is not appropriate. They are business identifiers assigned to this resource by the performer or other systems and remain constant as the resource is updated and propagates from server to server.",
    )
    status: Literal[
        "active",
        "on-hold",
        "cancelled",
        "completed",
        "entered-in-error",
        "stopped",
        "draft",
        "unknown",
    ] = Field(
        default=...,
        description="A code specifying the current state of the order. Generally, this will be active or completed state.",
    )
    status_reason: Optional[CodeableConcept] = Field(
        default=None,
        alias="statusReason",
        description="Captures the reason for the current state of the MedicationRequest.",
    )
    intent: Literal[
        "proposal",
        "plan",
        "order",
        "original-order",
        "reflex-order",
        "filler-order",
        "instance-order",
        "option",
    ] = Field(
        default=...,
        description="Whether the request is a proposal, plan, or an original order.",
    )
    category: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="Indicates the type of medication request (for example, where the medication is expected to be consumed or administered (i.e. inpatient or outpatient)).",
    )
    priority: Optional[Literal["routine", "urgent", "asap", "stat"]] = Field(
        default=None,
        description="Indicates how quickly the Medication Request should be addressed with respect to other requests.",
    )
    do_not_perform: Optional[bool] = Field(
        default=None,
        alias="doNotPerform",
        description="If true indicates that the provider is asking for the medication request not to occur.",
    )
    reported_boolean: Optional[bool] = Field(
        default=None,
        alias="reportedBoolean",
        description="Indicates if this record was captured as a secondary 'reported' record rather than as an original primary source-of-truth record. It may also indicate the source of the report.",
    )
    reported_reference: Optional[Reference] = Field(
        default=None,
        alias="reportedReference",
        description="Indicates if this record was captured as a secondary 'reported' record rather than as an original primary source-of-truth record. It may also indicate the source of the report.",
    )
    medication_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="medicationCodeableConcept",
        description="Identifies the medication being requested. This is a link to a resource that represents the medication which may be the details of the medication or simply an attribute carrying a code that identifies the medication from a known list of medications.",
    )
    medication_reference: Optional[Reference] = Field(
        default=None,
        alias="medicationReference",
        description="Identifies the medication being requested. This is a link to a resource that represents the medication which may be the details of the medication or simply an attribute carrying a code that identifies the medication from a known list of medications.",
    )
    subject: Reference = Field(
        default=...,
        description="A link to a resource representing the person or set of individuals to whom the medication will be given.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The Encounter during which this [x] was created or to which the creation of this record is tightly associated.",
    )
    supporting_information: Optional[List[Reference]] = Field(
        default=None,
        alias="supportingInformation",
        description="Include additional information (for example, patient height and weight) that supports the ordering of the medication.",
    )
    authored_on: Optional[str] = Field(
        default=None,
        alias="authoredOn",
        description="The date (and perhaps time) when the prescription was initially written or authored on.",
    )
    requester: Optional[Reference] = Field(
        default=None,
        description="The individual, organization, or device that initiated the request and has responsibility for its activation.",
    )
    performer: Optional[Reference] = Field(
        default=None,
        description="The specified desired performer of the medication treatment (e.g. the performer of the medication administration).",
    )
    performer_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="performerType",
        description="Indicates the type of performer of the administration of the medication.",
    )
    recorder: Optional[Reference] = Field(
        default=None,
        description="The person who entered the order on behalf of another individual for example in the case of a verbal or a telephone order.",
    )
    reason_code: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="reasonCode",
        description="The reason or the indication for ordering or not ordering the medication.",
    )
    reason_reference: Optional[List[Reference]] = Field(
        default=None,
        alias="reasonReference",
        description="Condition or observation that supports why the medication was ordered.",
    )
    instantiates_canonical: Optional[List[str]] = Field(
        default=None,
        alias="instantiatesCanonical",
        description="The URL pointing to a protocol, guideline, orderset, or other definition that is adhered to in whole or in part by this MedicationRequest.",
    )
    instantiates_uri: Optional[List[str]] = Field(
        default=None,
        alias="instantiatesUri",
        description="The URL pointing to an externally maintained protocol, guideline, orderset or other definition that is adhered to in whole or in part by this MedicationRequest.",
    )
    based_on: Optional[List[Reference]] = Field(
        default=None,
        alias="basedOn",
        description="A plan or request that is fulfilled in whole or in part by this medication request.",
    )
    group_identifier: Optional[Identifier] = Field(
        default=None,
        alias="groupIdentifier",
        description="A shared identifier common to all requests that were authorized more or less simultaneously by a single author, representing the identifier of the requisition or prescription.",
    )
    course_of_therapy_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="courseOfTherapyType",
        description="The description of the overall patte3rn of the administration of the medication to the patient.",
    )
    insurance: Optional[List[Reference]] = Field(
        default=None,
        description="Insurance plans, coverage extensions, pre-authorizations and/or pre-determinations that may be required for delivering the requested service.",
    )
    note: Optional[List[Annotation]] = Field(
        default=None,
        description="Extra information about the prescription that could not be conveyed by the other attributes.",
    )
    dosage_instruction: Optional[List[Dosage]] = Field(
        default=None,
        alias="dosageInstruction",
        description="Indicates how the medication is to be used by the patient.",
    )
    dispense_request: Optional[MedicationRequestDispenseRequest] = Field(
        default=None,
        alias="dispenseRequest",
        description="Indicates the specific details for the dispense or medication supply part of a medication request (also known as a Medication Prescription or Medication Order). Note that this information is not always sent with the order. There may be in some settings (e.g. hospitals) institutional or system support for completing the dispense details in the pharmacy department.",
    )
    substitution: Optional[MedicationRequestSubstitution] = Field(
        default=None,
        description="Indicates whether or not substitution can or should be part of the dispense. In some cases, substitution must happen, in other cases substitution must not happen. This block explains the prescriber's intent. If nothing is specified substitution may be done.",
    )
    prior_prescription: Optional[Reference] = Field(
        default=None,
        alias="priorPrescription",
        description="A link to a resource representing an earlier order related order or prescription.",
    )
    detected_issue: Optional[List[Reference]] = Field(
        default=None,
        alias="detectedIssue",
        description="Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, duplicate therapy, dosage alert etc.",
    )
    event_history: Optional[List[Reference]] = Field(
        default=None,
        alias="eventHistory",
        description="Links to Provenance records for past versions of this resource or fulfilling request or event resources that identify key state transitions or updates that are likely to be relevant to a user looking at the current version of the resource.",
    )


class MedicationRequestDispenseRequest(MedplumFHIRBase):
    """Indicates the specific details for the dispense or medication supply
    part of a medication request (also known as a Medication Prescription or
    Medication Order). Note that this information is not always sent with
    the order. There may be in some settings (e.g. hospitals) institutional
    or system support for completing the dispense details in the pharmacy
    department.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    initial_fill: Optional[MedicationRequestDispenseRequestInitialFill] = Field(
        default=None,
        alias="initialFill",
        description="Indicates the quantity or duration for the first dispense of the medication.",
    )
    dispense_interval: Optional[Duration] = Field(
        default=None,
        alias="dispenseInterval",
        description="The minimum period of time that must occur between dispenses of the medication.",
    )
    validity_period: Optional[Period] = Field(
        default=None,
        alias="validityPeriod",
        description="This indicates the validity period of a prescription (stale dating the Prescription).",
    )
    number_of_repeats_allowed: Optional[Union[int, float]] = Field(
        default=None,
        alias="numberOfRepeatsAllowed",
        description="An integer indicating the number of times, in addition to the original dispense, (aka refills or repeats) that the patient can receive the prescribed medication. Usage Notes: This integer does not include the original order dispense. This means that if an order indicates dispense 30 tablets plus &quot;3 repeats&quot;, then the order can be dispensed a total of 4 times and the patient can receive a total of 120 tablets. A prescriber may explicitly say that zero refills are permitted after the initial dispense.",
    )
    quantity: Optional[Quantity] = Field(
        default=None, description="The amount that is to be dispensed for one fill."
    )
    expected_supply_duration: Optional[Duration] = Field(
        default=None,
        alias="expectedSupplyDuration",
        description="Identifies the period time over which the supplied product is expected to be used, or the length of time the dispense is expected to last.",
    )
    performer: Optional[Reference] = Field(
        default=None,
        description="Indicates the intended dispensing Organization specified by the prescriber.",
    )


class MedicationRequestDispenseRequestInitialFill(MedplumFHIRBase):
    """Indicates the quantity or duration for the first dispense of the medication."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    quantity: Optional[Quantity] = Field(
        default=None,
        description="The amount or quantity to provide as part of the first dispense.",
    )
    duration: Optional[Duration] = Field(
        default=None,
        description="The length of time that the first dispense is expected to last.",
    )


class MedicationRequestSubstitution(MedplumFHIRBase):
    """Indicates whether or not substitution can or should be part of the
    dispense. In some cases, substitution must happen, in other cases
    substitution must not happen. This block explains the prescriber's
    intent. If nothing is specified substitution may be done.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    allowed_boolean: Optional[bool] = Field(
        default=None,
        alias="allowedBoolean",
        description="True if the prescriber allows a different drug to be dispensed from what was prescribed.",
    )
    allowed_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="allowedCodeableConcept",
        description="True if the prescriber allows a different drug to be dispensed from what was prescribed.",
    )
    reason: Optional[CodeableConcept] = Field(
        default=None,
        description="Indicates the reason for the substitution, or why substitution must or must not be performed.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("MedicationRequest", MedicationRequest)
    register_model("MedicationRequestDispenseRequest", MedicationRequestDispenseRequest)
    register_model(
        "MedicationRequestDispenseRequestInitialFill",
        MedicationRequestDispenseRequestInitialFill,
    )
    register_model("MedicationRequestSubstitution", MedicationRequestSubstitution)
