# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class PaymentReconciliation(MedplumFHIRBase):
    """This resource provides the details including amount of a payment and
    allocates the payment items being paid.
    """

    resource_type: Literal["PaymentReconciliation"] = Field(
        default="PaymentReconciliation", alias="resourceType"
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
        description="A unique identifier assigned to this payment reconciliation.",
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    period: Period | None = Field(
        default=None,
        description="The period of time for which payments have been gathered into this bulk payment for settlement.",
    )
    created: str = Field(
        default=..., description="The date when the resource was created."
    )
    payment_issuer: Reference | None = Field(
        default=None,
        alias="paymentIssuer",
        description="The party who generated the payment.",
    )
    request: Reference | None = Field(
        default=None, description="Original request resource reference."
    )
    requestor: Reference | None = Field(
        default=None,
        description="The practitioner who is responsible for the services rendered to the patient.",
    )
    outcome: Literal["queued", "complete", "error", "partial"] | None = Field(
        default=None, description="The outcome of a request for a reconciliation."
    )
    disposition: str | None = Field(
        default=None,
        description="A human readable description of the status of the request for the reconciliation.",
    )
    payment_date: str = Field(
        default=...,
        alias="paymentDate",
        description="The date of payment as indicated on the financial instrument.",
    )
    payment_amount: Money = Field(
        default=...,
        alias="paymentAmount",
        description="Total payment amount as indicated on the financial instrument.",
    )
    payment_identifier: Identifier | None = Field(
        default=None,
        alias="paymentIdentifier",
        description="Issuer's unique identifier for the payment instrument.",
    )
    detail: list[PaymentReconciliationDetail] | None = Field(
        default=None,
        description="Distribution of the payment amount for a previously acknowledged payable.",
    )
    form_code: CodeableConcept | None = Field(
        default=None,
        alias="formCode",
        description="A code for the form to be used for printing the content.",
    )
    process_note: list[PaymentReconciliationProcessNote] | None = Field(
        default=None,
        alias="processNote",
        description="A note that describes or explains the processing in a human readable form.",
    )


class PaymentReconciliationDetail(MedplumFHIRBase):
    """Distribution of the payment amount for a previously acknowledged payable."""

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
    identifier: Identifier | None = Field(
        default=None,
        description="Unique identifier for the current payment item for the referenced payable.",
    )
    predecessor: Identifier | None = Field(
        default=None,
        description="Unique identifier for the prior payment item for the referenced payable.",
    )
    type: CodeableConcept = Field(
        default=..., description="Code to indicate the nature of the payment."
    )
    request: Reference | None = Field(
        default=None,
        description="A resource, such as a Claim, the evaluation of which could lead to payment.",
    )
    submitter: Reference | None = Field(
        default=None,
        description="The party which submitted the claim or financial transaction.",
    )
    response: Reference | None = Field(
        default=None,
        description="A resource, such as a ClaimResponse, which contains a commitment to payment.",
    )
    date: str | None = Field(
        default=None,
        description="The date from the response resource containing a commitment to pay.",
    )
    responsible: Reference | None = Field(
        default=None,
        description="A reference to the individual who is responsible for inquiries regarding the response and its payment.",
    )
    payee: Reference | None = Field(
        default=None, description="The party which is receiving the payment."
    )
    amount: Money | None = Field(
        default=None,
        description="The monetary amount allocated from the total payment to the payable.",
    )


class PaymentReconciliationProcessNote(MedplumFHIRBase):
    """A note that describes or explains the processing in a human readable form."""

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
    type: Literal["display", "print", "printoper"] | None = Field(
        default=None, description="The business purpose of the note text."
    )
    text: str | None = Field(
        default=None,
        description="The explanation or description associated with the processing.",
    )
