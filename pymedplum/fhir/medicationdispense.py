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
    from pymedplum.fhir.dosage import Dosage
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class MedicationDispense(MedplumFHIRBase):
    """Indicates that a medication product is to be or has been dispensed for a
    named person/patient. This includes a description of the medication
    product (supply) provided and the instructions for administering the
    medication. The medication dispense is the result of a pharmacy system
    responding to a medication order.
    """

    resource_type: Literal["MedicationDispense"] = Field(
        default="MedicationDispense", alias="resourceType"
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
        description="Identifiers associated with this Medication Dispense that are defined by business processes and/or used to refer to it when a direct URL reference to the resource itself is not appropriate. They are business identifiers assigned to this resource by the performer or other systems and remain constant as the resource is updated and propagates from server to server.",
    )
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="The procedure that trigger the dispense.",
    )
    status: Literal[
        "preparation",
        "in-progress",
        "cancelled",
        "on-hold",
        "completed",
        "entered-in-error",
        "stopped",
        "declined",
        "unknown",
    ] = Field(
        default=...,
        description="A code specifying the state of the set of dispense events.",
    )
    status_reason_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="statusReasonCodeableConcept",
        description="Indicates the reason why a dispense was not performed.",
    )
    status_reason_reference: Reference | None = Field(
        default=None,
        alias="statusReasonReference",
        description="Indicates the reason why a dispense was not performed.",
    )
    category: CodeableConcept | None = Field(
        default=None,
        description="Indicates the type of medication dispense (for example, where the medication is expected to be consumed or administered (i.e. inpatient or outpatient)).",
    )
    medication_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="medicationCodeableConcept",
        description="Identifies the medication being administered. This is either a link to a resource representing the details of the medication or a simple attribute carrying a code that identifies the medication from a known list of medications.",
    )
    medication_reference: Reference | None = Field(
        default=None,
        alias="medicationReference",
        description="Identifies the medication being administered. This is either a link to a resource representing the details of the medication or a simple attribute carrying a code that identifies the medication from a known list of medications.",
    )
    subject: Reference | None = Field(
        default=None,
        description="A link to a resource representing the person or the group to whom the medication will be given.",
    )
    context: Reference | None = Field(
        default=None,
        description="The encounter or episode of care that establishes the context for this event.",
    )
    supporting_information: list[Reference] | None = Field(
        default=None,
        alias="supportingInformation",
        description="Additional information that supports the medication being dispensed.",
    )
    performer: list[MedicationDispensePerformer] | None = Field(
        default=None, description="Indicates who or what performed the event."
    )
    location: Reference | None = Field(
        default=None,
        description="The principal physical location where the dispense was performed.",
    )
    authorizing_prescription: list[Reference] | None = Field(
        default=None,
        alias="authorizingPrescription",
        description="Indicates the medication order that is being dispensed against.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Indicates the type of dispensing event that is performed. For example, Trial Fill, Completion of Trial, Partial Fill, Emergency Fill, Samples, etc.",
    )
    quantity: Quantity | None = Field(
        default=None,
        description="The amount of medication that has been dispensed. Includes unit of measure.",
    )
    days_supply: Quantity | None = Field(
        default=None,
        alias="daysSupply",
        description="The amount of medication expressed as a timing amount.",
    )
    when_prepared: str | None = Field(
        default=None,
        alias="whenPrepared",
        description="The time when the dispensed product was packaged and reviewed.",
    )
    when_handed_over: str | None = Field(
        default=None,
        alias="whenHandedOver",
        description="The time the dispensed product was provided to the patient or their representative.",
    )
    destination: Reference | None = Field(
        default=None,
        description="Identification of the facility/location where the medication was shipped to, as part of the dispense event.",
    )
    receiver: list[Reference] | None = Field(
        default=None,
        description="Identifies the person who picked up the medication. This will usually be a patient or their caregiver, but some cases exist where it can be a healthcare professional.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Extra information about the dispense that could not be conveyed in the other attributes.",
    )
    dosage_instruction: list[Dosage] | None = Field(
        default=None,
        alias="dosageInstruction",
        description="Indicates how the medication is to be used by the patient.",
    )
    substitution: MedicationDispenseSubstitution | None = Field(
        default=None,
        description="Indicates whether or not substitution was made as part of the dispense. In some cases, substitution will be expected but does not happen, in other cases substitution is not expected but does happen. This block explains what substitution did or did not happen and why. If nothing is specified, substitution was not done.",
    )
    detected_issue: list[Reference] | None = Field(
        default=None,
        alias="detectedIssue",
        description="Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. drug-drug interaction, duplicate therapy, dosage alert etc.",
    )
    event_history: list[Reference] | None = Field(
        default=None,
        alias="eventHistory",
        description="A summary of the events of interest that have occurred, such as when the dispense was verified.",
    )


class MedicationDispensePerformer(MedplumFHIRBase):
    """Indicates who or what performed the event."""

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
        description="Distinguishes the type of performer in the dispense. For example, date enterer, packager, final checker.",
    )
    actor: Reference = Field(
        default=...,
        description="The device, practitioner, etc. who performed the action. It should be assumed that the actor is the dispenser of the medication.",
    )


class MedicationDispenseSubstitution(MedplumFHIRBase):
    """Indicates whether or not substitution was made as part of the dispense.
    In some cases, substitution will be expected but does not happen, in
    other cases substitution is not expected but does happen. This block
    explains what substitution did or did not happen and why. If nothing is
    specified, substitution was not done.
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
    was_substituted: bool = Field(
        default=...,
        alias="wasSubstituted",
        description="True if the dispenser dispensed a different drug or product from what was prescribed.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="A code signifying whether a different drug was dispensed from what was prescribed.",
    )
    reason: list[CodeableConcept] | None = Field(
        default=None,
        description="Indicates the reason for the substitution (or lack of substitution) from what was prescribed.",
    )
    responsible_party: list[Reference] | None = Field(
        default=None,
        alias="responsibleParty",
        description="The person or organization that has primary responsibility for the substitution.",
    )
