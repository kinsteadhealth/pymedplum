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
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class MedicationStatement(MedplumFHIRBase):
    """A record of a medication that is being consumed by a patient. A
    MedicationStatement may indicate that the patient may be taking the
    medication now or has taken the medication in the past or will be taking
    the medication in the future. The source of this information can be the
    patient, significant other (such as a family member or spouse), or a
    clinician. A common scenario where this information is captured is
    during the history taking process during a patient visit or stay. The
    medication information may come from sources such as the patient's
    memory, from a prescription bottle, or from a list of medications the
    patient, clinician or other party maintains. The primary difference
    between a medication statement and a medication administration is that
    the medication administration has complete administration information
    and is based on actual administration information from the person who
    administered the medication. A medication statement is often, if not
    always, less specific. There is no required date/time when the
    medication was administered, in fact we only know that a source has
    reported the patient is taking this medication, where details such as
    time, quantity, or rate or even medication product may be incomplete or
    missing or less precise. As stated earlier, the medication statement
    information may come from the patient's memory, from a prescription
    bottle or from a list of medications the patient, clinician or other
    party maintains. Medication administration is more formal and is not
    missing detailed information.
    """

    resource_type: Literal["MedicationStatement"] = Field(
        default="MedicationStatement", alias="resourceType"
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
        description="Identifiers associated with this Medication Statement that are defined by business processes and/or used to refer to it when a direct URL reference to the resource itself is not appropriate. They are business identifiers assigned to this resource by the performer or other systems and remain constant as the resource is updated and propagates from server to server.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="A plan, proposal or order that is fulfilled in whole or in part by this event.",
    )
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="A larger event of which this particular event is a component or step.",
    )
    status: Literal[
        "active",
        "completed",
        "entered-in-error",
        "intended",
        "stopped",
        "on-hold",
        "unknown",
        "not-taken",
    ] = Field(
        default=...,
        description="A code representing the patient or other source's judgment about the state of the medication used that this statement is about. Generally, this will be active or completed.",
    )
    status_reason: list[CodeableConcept] | None = Field(
        default=None,
        alias="statusReason",
        description="Captures the reason for the current state of the MedicationStatement.",
    )
    category: CodeableConcept | None = Field(
        default=None,
        description="Indicates where the medication is expected to be consumed or administered.",
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
    subject: Reference = Field(
        default=...,
        description="The person, animal or group who is/was taking the medication.",
    )
    context: Reference | None = Field(
        default=None,
        description="The encounter or episode of care that establishes the context for this MedicationStatement.",
    )
    effective_date_time: str | None = Field(
        default=None,
        alias="effectiveDateTime",
        description="The interval of time during which it is being asserted that the patient is/was/will be taking the medication (or was not taking, when the MedicationStatement.taken element is No).",
    )
    effective_period: Period | None = Field(
        default=None,
        alias="effectivePeriod",
        description="The interval of time during which it is being asserted that the patient is/was/will be taking the medication (or was not taking, when the MedicationStatement.taken element is No).",
    )
    date_asserted: str | None = Field(
        default=None,
        alias="dateAsserted",
        description="The date when the medication statement was asserted by the information source.",
    )
    information_source: Reference | None = Field(
        default=None,
        alias="informationSource",
        description="The person or organization that provided the information about the taking of this medication. Note: Use derivedFrom when a MedicationStatement is derived from other resources, e.g. Claim or MedicationRequest.",
    )
    derived_from: list[Reference] | None = Field(
        default=None,
        alias="derivedFrom",
        description="Allows linking the MedicationStatement to the underlying MedicationRequest, or to other information that supports or is used to derive the MedicationStatement.",
    )
    reason_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="reasonCode",
        description="A reason for why the medication is being/was taken.",
    )
    reason_reference: list[Reference] | None = Field(
        default=None,
        alias="reasonReference",
        description="Condition or observation that supports why the medication is being/was taken.",
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Provides extra information about the medication statement that is not conveyed by the other attributes.",
    )
    dosage: list[Dosage] | None = Field(
        default=None,
        description="Indicates how the medication is/was or should be taken by the patient.",
    )
