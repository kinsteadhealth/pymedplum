# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class ClaimResponse(MedplumFHIRBase):
    """This resource provides the adjudication details from the processing of a
    Claim resource.
    """

    resource_type: Literal["ClaimResponse"] = Field(
        default="ClaimResponse", alias="resourceType"
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
        default=None, description="A unique identifier assigned to this claim response."
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    type: CodeableConcept = Field(
        default=...,
        description="A finer grained suite of claim type codes which may convey additional information such as Inpatient vs Outpatient and/or a specialty service.",
    )
    sub_type: CodeableConcept | None = Field(
        default=None,
        alias="subType",
        description="A finer grained suite of claim type codes which may convey additional information such as Inpatient vs Outpatient and/or a specialty service.",
    )
    use: Literal["claim", "preauthorization", "predetermination"] = Field(
        default=...,
        description="A code to indicate whether the nature of the request is: to request adjudication of products and services previously rendered; or requesting authorization and adjudication for provision in the future; or requesting the non-binding adjudication of the listed products and services which could be provided in the future.",
    )
    patient: Reference = Field(
        default=...,
        description="The party to whom the professional services and/or products have been supplied or are being considered and for whom actual for facast reimbursement is sought.",
    )
    created: str = Field(default=..., description="The date this resource was created.")
    insurer: Reference = Field(
        default=...,
        description="The party responsible for authorization, adjudication and reimbursement.",
    )
    requestor: Reference | None = Field(
        default=None,
        description="The provider which is responsible for the claim, predetermination or preauthorization.",
    )
    request: Reference | None = Field(
        default=None, description="Original request resource reference."
    )
    outcome: Literal["queued", "complete", "error", "partial"] = Field(
        default=...,
        description="The outcome of the claim, predetermination, or preauthorization processing.",
    )
    disposition: str | None = Field(
        default=None,
        description="A human readable description of the status of the adjudication.",
    )
    pre_auth_ref: str | None = Field(
        default=None,
        alias="preAuthRef",
        description="Reference from the Insurer which is used in later communications which refers to this adjudication.",
    )
    pre_auth_period: Period | None = Field(
        default=None,
        alias="preAuthPeriod",
        description="The time frame during which this authorization is effective.",
    )
    payee_type: CodeableConcept | None = Field(
        default=None,
        alias="payeeType",
        description="Type of Party to be reimbursed: subscriber, provider, other.",
    )
    item: list[ClaimResponseItem] | None = Field(
        default=None,
        description="A claim line. Either a simple (a product or service) or a 'group' of details which can also be a simple items or groups of sub-details.",
    )
    add_item: list[ClaimResponseAddItem] | None = Field(
        default=None,
        alias="addItem",
        description="The first-tier service adjudications for payor added product or service lines.",
    )
    adjudication: list[ClaimResponseItemAdjudication] | None = Field(
        default=None,
        description="The adjudication results which are presented at the header level rather than at the line-item or add-item levels.",
    )
    total: list[ClaimResponseTotal] | None = Field(
        default=None, description="Categorized monetary totals for the adjudication."
    )
    payment: ClaimResponsePayment | None = Field(
        default=None, description="Payment details for the adjudication of the claim."
    )
    funds_reserve: CodeableConcept | None = Field(
        default=None,
        alias="fundsReserve",
        description="A code, used only on a response to a preauthorization, to indicate whether the benefits payable have been reserved and for whom.",
    )
    form_code: CodeableConcept | None = Field(
        default=None,
        alias="formCode",
        description="A code for the form to be used for printing the content.",
    )
    form: Attachment | None = Field(
        default=None,
        description="The actual form, by reference or inclusion, for printing the content or an EOB.",
    )
    process_note: list[ClaimResponseProcessNote] | None = Field(
        default=None,
        alias="processNote",
        description="A note that describes or explains adjudication results in a human readable form.",
    )
    communication_request: list[Reference] | None = Field(
        default=None,
        alias="communicationRequest",
        description="Request for additional supporting or authorizing information.",
    )
    insurance: list[ClaimResponseInsurance] | None = Field(
        default=None,
        description="Financial instruments for reimbursement for the health care products and services specified on the claim.",
    )
    error: list[ClaimResponseError] | None = Field(
        default=None,
        description="Errors encountered during the processing of the adjudication.",
    )


class ClaimResponseAddItem(MedplumFHIRBase):
    """The first-tier service adjudications for payor added product or service lines."""

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
    item_sequence: list[int | float] | None = Field(
        default=None,
        alias="itemSequence",
        description="Claim items which this service line is intended to replace.",
    )
    detail_sequence: list[int | float] | None = Field(
        default=None,
        alias="detailSequence",
        description="The sequence number of the details within the claim item which this line is intended to replace.",
    )
    subdetail_sequence: list[int | float] | None = Field(
        default=None,
        alias="subdetailSequence",
        description="The sequence number of the sub-details within the details within the claim item which this line is intended to replace.",
    )
    provider: list[Reference] | None = Field(
        default=None,
        description="The providers who are authorized for the services rendered to the patient.",
    )
    product_or_service: CodeableConcept = Field(
        default=...,
        alias="productOrService",
        description="When the value is a group code then this item collects a set of related claim details, otherwise this contains the product, service, drug or other billing code for the item.",
    )
    modifier: list[CodeableConcept] | None = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    program_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="programCode",
        description="Identifies the program under which this may be recovered.",
    )
    serviced_date: str | None = Field(
        default=None,
        alias="servicedDate",
        description="The date or dates when the service or product was supplied, performed or completed.",
    )
    serviced_period: Period | None = Field(
        default=None,
        alias="servicedPeriod",
        description="The date or dates when the service or product was supplied, performed or completed.",
    )
    location_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="locationCodeableConcept",
        description="Where the product or service was provided.",
    )
    location_address: Address | None = Field(
        default=None,
        alias="locationAddress",
        description="Where the product or service was provided.",
    )
    location_reference: Reference | None = Field(
        default=None,
        alias="locationReference",
        description="Where the product or service was provided.",
    )
    quantity: Quantity | None = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Money | None = Field(
        default=None,
        alias="unitPrice",
        description="If the item is not a group then this is the fee for the product or service, otherwise this is the total of the fees for the details of the group.",
    )
    factor: int | float | None = Field(
        default=None,
        description="A real number that represents a multiplier used in determining the overall value of services delivered and/or goods received. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.",
    )
    net: Money | None = Field(
        default=None,
        description="The quantity times the unit price for an additional service or product or charge.",
    )
    body_site: CodeableConcept | None = Field(
        default=None,
        alias="bodySite",
        description="Physical service site on the patient (limb, tooth, etc.).",
    )
    sub_site: list[CodeableConcept] | None = Field(
        default=None,
        alias="subSite",
        description="A region or surface of the bodySite, e.g. limb region or tooth surface(s).",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ClaimResponseItemAdjudication] = Field(
        default=..., description="The adjudication results."
    )
    detail: list[ClaimResponseAddItemDetail] | None = Field(
        default=None,
        description="The second-tier service adjudications for payor added services.",
    )


class ClaimResponseAddItemDetail(MedplumFHIRBase):
    """The second-tier service adjudications for payor added services."""

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
    product_or_service: CodeableConcept = Field(
        default=...,
        alias="productOrService",
        description="When the value is a group code then this item collects a set of related claim details, otherwise this contains the product, service, drug or other billing code for the item.",
    )
    modifier: list[CodeableConcept] | None = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    quantity: Quantity | None = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Money | None = Field(
        default=None,
        alias="unitPrice",
        description="If the item is not a group then this is the fee for the product or service, otherwise this is the total of the fees for the details of the group.",
    )
    factor: int | float | None = Field(
        default=None,
        description="A real number that represents a multiplier used in determining the overall value of services delivered and/or goods received. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.",
    )
    net: Money | None = Field(
        default=None,
        description="The quantity times the unit price for an additional service or product or charge.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ClaimResponseItemAdjudication] = Field(
        default=..., description="The adjudication results."
    )
    sub_detail: list[ClaimResponseAddItemDetailSubDetail] | None = Field(
        default=None,
        alias="subDetail",
        description="The third-tier service adjudications for payor added services.",
    )


class ClaimResponseAddItemDetailSubDetail(MedplumFHIRBase):
    """The third-tier service adjudications for payor added services."""

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
    product_or_service: CodeableConcept = Field(
        default=...,
        alias="productOrService",
        description="When the value is a group code then this item collects a set of related claim details, otherwise this contains the product, service, drug or other billing code for the item.",
    )
    modifier: list[CodeableConcept] | None = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    quantity: Quantity | None = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Money | None = Field(
        default=None,
        alias="unitPrice",
        description="If the item is not a group then this is the fee for the product or service, otherwise this is the total of the fees for the details of the group.",
    )
    factor: int | float | None = Field(
        default=None,
        description="A real number that represents a multiplier used in determining the overall value of services delivered and/or goods received. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.",
    )
    net: Money | None = Field(
        default=None,
        description="The quantity times the unit price for an additional service or product or charge.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ClaimResponseItemAdjudication] = Field(
        default=..., description="The adjudication results."
    )


class ClaimResponseError(MedplumFHIRBase):
    """Errors encountered during the processing of the adjudication."""

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
    item_sequence: int | float | None = Field(
        default=None,
        alias="itemSequence",
        description="The sequence number of the line item submitted which contains the error. This value is omitted when the error occurs outside of the item structure.",
    )
    detail_sequence: int | float | None = Field(
        default=None,
        alias="detailSequence",
        description="The sequence number of the detail within the line item submitted which contains the error. This value is omitted when the error occurs outside of the item structure.",
    )
    sub_detail_sequence: int | float | None = Field(
        default=None,
        alias="subDetailSequence",
        description="The sequence number of the sub-detail within the detail within the line item submitted which contains the error. This value is omitted when the error occurs outside of the item structure.",
    )
    code: CodeableConcept = Field(
        default=...,
        description="An error code, from a specified code system, which details why the claim could not be adjudicated.",
    )


class ClaimResponseInsurance(MedplumFHIRBase):
    """Financial instruments for reimbursement for the health care products and
    services specified on the claim.
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
    sequence: int | float = Field(
        default=...,
        description="A number to uniquely identify insurance entries and provide a sequence of coverages to convey coordination of benefit order.",
    )
    focal: bool = Field(
        default=...,
        description="A flag to indicate that this Coverage is to be used for adjudication of this claim when set to true.",
    )
    coverage: Reference = Field(
        default=...,
        description="Reference to the insurance card level information contained in the Coverage resource. The coverage issuing insurer will use these details to locate the patient's actual coverage within the insurer's information system.",
    )
    business_arrangement: str | None = Field(
        default=None,
        alias="businessArrangement",
        description="A business agreement number established between the provider and the insurer for special business processing purposes.",
    )
    claim_response: Reference | None = Field(
        default=None,
        alias="claimResponse",
        description="The result of the adjudication of the line items for the Coverage specified in this insurance.",
    )


class ClaimResponseItem(MedplumFHIRBase):
    """A claim line. Either a simple (a product or service) or a 'group' of
    details which can also be a simple items or groups of sub-details.
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
    item_sequence: int | float = Field(
        default=...,
        alias="itemSequence",
        description="A number to uniquely reference the claim item entries.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ClaimResponseItemAdjudication] = Field(
        default=...,
        description="If this item is a group then the values here are a summary of the adjudication of the detail items. If this item is a simple product or service then this is the result of the adjudication of this item.",
    )
    detail: list[ClaimResponseItemDetail] | None = Field(
        default=None,
        description="A claim detail. Either a simple (a product or service) or a 'group' of sub-details which are simple items.",
    )


class ClaimResponseItemAdjudication(MedplumFHIRBase):
    """If this item is a group then the values here are a summary of the
    adjudication of the detail items. If this item is a simple product or
    service then this is the result of the adjudication of this item.
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
    category: CodeableConcept = Field(
        default=...,
        description="A code to indicate the information type of this adjudication record. Information types may include the value submitted, maximum values or percentages allowed or payable under the plan, amounts that: the patient is responsible for in aggregate or pertaining to this item; amounts paid by other coverages; and, the benefit payable for this item.",
    )
    reason: CodeableConcept | None = Field(
        default=None,
        description="A code supporting the understanding of the adjudication result and explaining variance from expected amount.",
    )
    amount: Money | None = Field(
        default=None, description="Monetary amount associated with the category."
    )
    value: int | float | None = Field(
        default=None,
        description="A non-monetary value associated with the category. Mutually exclusive to the amount element above.",
    )


class ClaimResponseItemDetail(MedplumFHIRBase):
    """A claim detail. Either a simple (a product or service) or a 'group' of
    sub-details which are simple items.
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
    detail_sequence: int | float = Field(
        default=...,
        alias="detailSequence",
        description="A number to uniquely reference the claim detail entry.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ClaimResponseItemAdjudication] = Field(
        default=..., description="The adjudication results."
    )
    sub_detail: list[ClaimResponseItemDetailSubDetail] | None = Field(
        default=None,
        alias="subDetail",
        description="A sub-detail adjudication of a simple product or service.",
    )


class ClaimResponseItemDetailSubDetail(MedplumFHIRBase):
    """A sub-detail adjudication of a simple product or service."""

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
    sub_detail_sequence: int | float = Field(
        default=...,
        alias="subDetailSequence",
        description="A number to uniquely reference the claim sub-detail entry.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ClaimResponseItemAdjudication] | None = Field(
        default=None, description="The adjudication results."
    )


class ClaimResponsePayment(MedplumFHIRBase):
    """Payment details for the adjudication of the claim."""

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
    type: CodeableConcept = Field(
        default=...,
        description="Whether this represents partial or complete payment of the benefits payable.",
    )
    adjustment: Money | None = Field(
        default=None,
        description="Total amount of all adjustments to this payment included in this transaction which are not related to this claim's adjudication.",
    )
    adjustment_reason: CodeableConcept | None = Field(
        default=None,
        alias="adjustmentReason",
        description="Reason for the payment adjustment.",
    )
    date: str | None = Field(
        default=None,
        description="Estimated date the payment will be issued or the actual issue date of payment.",
    )
    amount: Money = Field(
        default=..., description="Benefits payable less any payment adjustment."
    )
    identifier: Identifier | None = Field(
        default=None,
        description="Issuer's unique identifier for the payment instrument.",
    )


class ClaimResponseProcessNote(MedplumFHIRBase):
    """A note that describes or explains adjudication results in a human readable form."""

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
    number: int | float | None = Field(
        default=None, description="A number to uniquely identify a note entry."
    )
    type: Literal["display", "print", "printoper"] | None = Field(
        default=None, description="The business purpose of the note text."
    )
    text: str = Field(
        default=...,
        description="The explanation or description associated with the processing.",
    )
    language: CodeableConcept | None = Field(
        default=None,
        description="A code to define the language used in the text of the note.",
    )


class ClaimResponseTotal(MedplumFHIRBase):
    """Categorized monetary totals for the adjudication."""

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
    category: CodeableConcept = Field(
        default=...,
        description="A code to indicate the information type of this adjudication record. Information types may include: the value submitted, maximum values or percentages allowed or payable under the plan, amounts that the patient is responsible for in aggregate or pertaining to this item, amounts paid by other coverages, and the benefit payable for this item.",
    )
    amount: Money = Field(
        default=..., description="Monetary total amount associated with the category."
    )
