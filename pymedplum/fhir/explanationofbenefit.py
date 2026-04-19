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
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class ExplanationOfBenefit(MedplumFHIRBase):
    """This resource provides: the claim details; adjudication details from the
    processing of a Claim; and optionally account balance information, for
    informing the subscriber of the benefits provided.
    """

    resource_type: Literal["ExplanationOfBenefit"] = Field(
        default="ExplanationOfBenefit", alias="resourceType"
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
        description="A unique identifier assigned to this explanation of benefit.",
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    type: CodeableConcept = Field(
        default=...,
        description="The category of claim, e.g. oral, pharmacy, vision, institutional, professional.",
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
        description="The party to whom the professional services and/or products have been supplied or are being considered and for whom actual for forecast reimbursement is sought.",
    )
    billable_period: Period | None = Field(
        default=None,
        alias="billablePeriod",
        description="The period for which charges are being submitted.",
    )
    created: str = Field(default=..., description="The date this resource was created.")
    enterer: Reference | None = Field(
        default=None,
        description="Individual who created the claim, predetermination or preauthorization.",
    )
    insurer: Reference = Field(
        default=...,
        description="The party responsible for authorization, adjudication and reimbursement.",
    )
    provider: Reference = Field(
        default=...,
        description="The provider which is responsible for the claim, predetermination or preauthorization.",
    )
    priority: CodeableConcept | None = Field(
        default=None,
        description="The provider-required urgency of processing the request. Typical values include: stat, routine deferred.",
    )
    funds_reserve_requested: CodeableConcept | None = Field(
        default=None,
        alias="fundsReserveRequested",
        description="A code to indicate whether and for whom funds are to be reserved for future claims.",
    )
    funds_reserve: CodeableConcept | None = Field(
        default=None,
        alias="fundsReserve",
        description="A code, used only on a response to a preauthorization, to indicate whether the benefits payable have been reserved and for whom.",
    )
    related: list[ExplanationOfBenefitRelated] | None = Field(
        default=None,
        description="Other claims which are related to this claim such as prior submissions or claims for related services or for the same event.",
    )
    prescription: Reference | None = Field(
        default=None,
        description="Prescription to support the dispensing of pharmacy, device or vision products.",
    )
    original_prescription: Reference | None = Field(
        default=None,
        alias="originalPrescription",
        description="Original prescription which has been superseded by this prescription to support the dispensing of pharmacy services, medications or products.",
    )
    payee: ExplanationOfBenefitPayee | None = Field(
        default=None,
        description="The party to be reimbursed for cost of the products and services according to the terms of the policy.",
    )
    referral: Reference | None = Field(
        default=None, description="A reference to a referral resource."
    )
    facility: Reference | None = Field(
        default=None, description="Facility where the services were provided."
    )
    claim: Reference | None = Field(
        default=None,
        description="The business identifier for the instance of the adjudication request: claim predetermination or preauthorization.",
    )
    claim_response: Reference | None = Field(
        default=None,
        alias="claimResponse",
        description="The business identifier for the instance of the adjudication response: claim, predetermination or preauthorization response.",
    )
    outcome: Literal["queued", "complete", "error", "partial"] = Field(
        default=...,
        description="The outcome of the claim, predetermination, or preauthorization processing.",
    )
    disposition: str | None = Field(
        default=None,
        description="A human readable description of the status of the adjudication.",
    )
    pre_auth_ref: list[str] | None = Field(
        default=None,
        alias="preAuthRef",
        description="Reference from the Insurer which is used in later communications which refers to this adjudication.",
    )
    pre_auth_ref_period: list[Period] | None = Field(
        default=None,
        alias="preAuthRefPeriod",
        description="The timeframe during which the supplied preauthorization reference may be quoted on claims to obtain the adjudication as provided.",
    )
    care_team: list[ExplanationOfBenefitCareTeam] | None = Field(
        default=None,
        alias="careTeam",
        description="The members of the team who provided the products and services.",
    )
    supporting_info: list[ExplanationOfBenefitSupportingInfo] | None = Field(
        default=None,
        alias="supportingInfo",
        description="Additional information codes regarding exceptions, special considerations, the condition, situation, prior or concurrent issues.",
    )
    diagnosis: list[ExplanationOfBenefitDiagnosis] | None = Field(
        default=None,
        description="Information about diagnoses relevant to the claim items.",
    )
    procedure: list[ExplanationOfBenefitProcedure] | None = Field(
        default=None,
        description="Procedures performed on the patient relevant to the billing items with the claim.",
    )
    precedence: int | float | None = Field(
        default=None,
        description="This indicates the relative order of a series of EOBs related to different coverages for the same suite of services.",
    )
    insurance: list[ExplanationOfBenefitInsurance] = Field(
        default=...,
        description="Financial instruments for reimbursement for the health care products and services specified on the claim.",
    )
    accident: ExplanationOfBenefitAccident | None = Field(
        default=None,
        description="Details of a accident which resulted in injuries which required the products and services listed in the claim.",
    )
    item: list[ExplanationOfBenefitItem] | None = Field(
        default=None,
        description="A claim line. Either a simple (a product or service) or a 'group' of details which can also be a simple items or groups of sub-details.",
    )
    add_item: list[ExplanationOfBenefitAddItem] | None = Field(
        default=None,
        alias="addItem",
        description="The first-tier service adjudications for payor added product or service lines.",
    )
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None,
        description="The adjudication results which are presented at the header level rather than at the line-item or add-item levels.",
    )
    total: list[ExplanationOfBenefitTotal] | None = Field(
        default=None, description="Categorized monetary totals for the adjudication."
    )
    payment: ExplanationOfBenefitPayment | None = Field(
        default=None, description="Payment details for the adjudication of the claim."
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
    process_note: list[ExplanationOfBenefitProcessNote] | None = Field(
        default=None,
        alias="processNote",
        description="A note that describes or explains adjudication results in a human readable form.",
    )
    benefit_period: Period | None = Field(
        default=None,
        alias="benefitPeriod",
        description="The term of the benefits documented in this response.",
    )
    benefit_balance: list[ExplanationOfBenefitBenefitBalance] | None = Field(
        default=None, alias="benefitBalance", description="Balance by Benefit Category."
    )


class ExplanationOfBenefitAccident(MedplumFHIRBase):
    """Details of a accident which resulted in injuries which required the
    products and services listed in the claim.
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
    date: str | None = Field(
        default=None,
        description="Date of an accident event related to the products and services contained in the claim.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="The type or context of the accident event for the purposes of selection of potential insurance coverages and determination of coordination between insurers.",
    )
    location_address: Address | None = Field(
        default=None,
        alias="locationAddress",
        description="The physical location of the accident event.",
    )
    location_reference: Reference | None = Field(
        default=None,
        alias="locationReference",
        description="The physical location of the accident event.",
    )


class ExplanationOfBenefitAddItem(MedplumFHIRBase):
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
    sub_detail_sequence: list[int | float] | None = Field(
        default=None,
        alias="subDetailSequence",
        description="The sequence number of the sub-details woithin the details within the claim item which this line is intended to replace.",
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
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None, description="The adjudication results."
    )
    detail: list[ExplanationOfBenefitAddItemDetail] | None = Field(
        default=None,
        description="The second-tier service adjudications for payor added services.",
    )


class ExplanationOfBenefitAddItemDetail(MedplumFHIRBase):
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
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None, description="The adjudication results."
    )
    sub_detail: list[ExplanationOfBenefitAddItemDetailSubDetail] | None = Field(
        default=None,
        alias="subDetail",
        description="The third-tier service adjudications for payor added services.",
    )


class ExplanationOfBenefitAddItemDetailSubDetail(MedplumFHIRBase):
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
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None, description="The adjudication results."
    )


class ExplanationOfBenefitBenefitBalance(MedplumFHIRBase):
    """Balance by Benefit Category."""

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
        description="Code to identify the general type of benefits under which products and services are provided.",
    )
    excluded: bool | None = Field(
        default=None,
        description="True if the indicated class of service is excluded from the plan, missing or False indicates the product or service is included in the coverage.",
    )
    name: str | None = Field(
        default=None, description="A short name or tag for the benefit."
    )
    description: str | None = Field(
        default=None,
        description="A richer description of the benefit or services covered.",
    )
    network: CodeableConcept | None = Field(
        default=None,
        description="Is a flag to indicate whether the benefits refer to in-network providers or out-of-network providers.",
    )
    unit: CodeableConcept | None = Field(
        default=None,
        description="Indicates if the benefits apply to an individual or to the family.",
    )
    term: CodeableConcept | None = Field(
        default=None,
        description="The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'.",
    )
    financial: list[ExplanationOfBenefitBenefitBalanceFinancial] | None = Field(
        default=None, description="Benefits Used to date."
    )


class ExplanationOfBenefitBenefitBalanceFinancial(MedplumFHIRBase):
    """Benefits Used to date."""

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
        default=..., description="Classification of benefit being provided."
    )
    allowed_unsigned_int: int | None = Field(
        default=None,
        alias="allowedUnsignedInt",
        description="The quantity of the benefit which is permitted under the coverage.",
    )
    allowed_string: str | None = Field(
        default=None,
        alias="allowedString",
        description="The quantity of the benefit which is permitted under the coverage.",
    )
    allowed_money: Money | None = Field(
        default=None,
        alias="allowedMoney",
        description="The quantity of the benefit which is permitted under the coverage.",
    )
    used_unsigned_int: int | None = Field(
        default=None,
        alias="usedUnsignedInt",
        description="The quantity of the benefit which have been consumed to date.",
    )
    used_money: Money | None = Field(
        default=None,
        alias="usedMoney",
        description="The quantity of the benefit which have been consumed to date.",
    )


class ExplanationOfBenefitCareTeam(MedplumFHIRBase):
    """The members of the team who provided the products and services."""

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
        default=..., description="A number to uniquely identify care team entries."
    )
    provider: Reference = Field(
        default=...,
        description="Member of the team who provided the product or service.",
    )
    responsible: bool | None = Field(
        default=None,
        description="The party who is billing and/or responsible for the claimed products or services.",
    )
    role: CodeableConcept | None = Field(
        default=None,
        description="The lead, assisting or supervising practitioner and their discipline if a multidisciplinary team.",
    )
    qualification: CodeableConcept | None = Field(
        default=None,
        description="The qualification of the practitioner which is applicable for this service.",
    )


class ExplanationOfBenefitDiagnosis(MedplumFHIRBase):
    """Information about diagnoses relevant to the claim items."""

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
        default=..., description="A number to uniquely identify diagnosis entries."
    )
    diagnosis_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="diagnosisCodeableConcept",
        description="The nature of illness or problem in a coded form or as a reference to an external defined Condition.",
    )
    diagnosis_reference: Reference | None = Field(
        default=None,
        alias="diagnosisReference",
        description="The nature of illness or problem in a coded form or as a reference to an external defined Condition.",
    )
    type: list[CodeableConcept] | None = Field(
        default=None,
        description="When the condition was observed or the relative ranking.",
    )
    on_admission: CodeableConcept | None = Field(
        default=None,
        alias="onAdmission",
        description="Indication of whether the diagnosis was present on admission to a facility.",
    )
    package_code: CodeableConcept | None = Field(
        default=None,
        alias="packageCode",
        description="A package billing code or bundle code used to group products and services to a particular health condition (such as heart attack) which is based on a predetermined grouping code system.",
    )


class ExplanationOfBenefitInsurance(MedplumFHIRBase):
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
    focal: bool = Field(
        default=...,
        description="A flag to indicate that this Coverage is to be used for adjudication of this claim when set to true.",
    )
    coverage: Reference = Field(
        default=...,
        description="Reference to the insurance card level information contained in the Coverage resource. The coverage issuing insurer will use these details to locate the patient's actual coverage within the insurer's information system.",
    )
    pre_auth_ref: list[str] | None = Field(
        default=None,
        alias="preAuthRef",
        description="Reference numbers previously provided by the insurer to the provider to be quoted on subsequent claims containing services or products related to the prior authorization.",
    )


class ExplanationOfBenefitItem(MedplumFHIRBase):
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
    sequence: int | float = Field(
        default=..., description="A number to uniquely identify item entries."
    )
    care_team_sequence: list[int | float] | None = Field(
        default=None,
        alias="careTeamSequence",
        description="Care team members related to this service or product.",
    )
    diagnosis_sequence: list[int | float] | None = Field(
        default=None,
        alias="diagnosisSequence",
        description="Diagnoses applicable for this service or product.",
    )
    procedure_sequence: list[int | float] | None = Field(
        default=None,
        alias="procedureSequence",
        description="Procedures applicable for this service or product.",
    )
    information_sequence: list[int | float] | None = Field(
        default=None,
        alias="informationSequence",
        description="Exceptions, special conditions and supporting information applicable for this service or product.",
    )
    revenue: CodeableConcept | None = Field(
        default=None,
        description="The type of revenue or cost center providing the product and/or service.",
    )
    category: CodeableConcept | None = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
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
    udi: list[Reference] | None = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
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
    encounter: list[Reference] | None = Field(
        default=None,
        description="A billed item may include goods or services provided in multiple encounters.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None,
        description="If this item is a group then the values here are a summary of the adjudication of the detail items. If this item is a simple product or service then this is the result of the adjudication of this item.",
    )
    detail: list[ExplanationOfBenefitItemDetail] | None = Field(
        default=None, description="Second-tier of goods and services."
    )


class ExplanationOfBenefitItemAdjudication(MedplumFHIRBase):
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
        description="A code to indicate the information type of this adjudication record. Information types may include: the value submitted, maximum values or percentages allowed or payable under the plan, amounts that the patient is responsible for in-aggregate or pertaining to this item, amounts paid by other coverages, and the benefit payable for this item.",
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


class ExplanationOfBenefitItemDetail(MedplumFHIRBase):
    """Second-tier of goods and services."""

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
        description="A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are simple items.",
    )
    revenue: CodeableConcept | None = Field(
        default=None,
        description="The type of revenue or cost center providing the product and/or service.",
    )
    category: CodeableConcept | None = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
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
    udi: list[Reference] | None = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None, description="The adjudication results."
    )
    sub_detail: list[ExplanationOfBenefitItemDetailSubDetail] | None = Field(
        default=None, alias="subDetail", description="Third-tier of goods and services."
    )


class ExplanationOfBenefitItemDetailSubDetail(MedplumFHIRBase):
    """Third-tier of goods and services."""

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
        description="A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are simple items.",
    )
    revenue: CodeableConcept | None = Field(
        default=None,
        description="The type of revenue or cost center providing the product and/or service.",
    )
    category: CodeableConcept | None = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
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
    udi: list[Reference] | None = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )
    note_number: list[int | float] | None = Field(
        default=None,
        alias="noteNumber",
        description="The numbers associated with notes below which apply to the adjudication of this item.",
    )
    adjudication: list[ExplanationOfBenefitItemAdjudication] | None = Field(
        default=None, description="The adjudication results."
    )


class ExplanationOfBenefitPayee(MedplumFHIRBase):
    """The party to be reimbursed for cost of the products and services
    according to the terms of the policy.
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
    type: CodeableConcept | None = Field(
        default=None,
        description="Type of Party to be reimbursed: Subscriber, provider, other.",
    )
    party: Reference | None = Field(
        default=None,
        description="Reference to the individual or organization to whom any payment will be made.",
    )


class ExplanationOfBenefitPayment(MedplumFHIRBase):
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
    type: CodeableConcept | None = Field(
        default=None,
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
    amount: Money | None = Field(
        default=None, description="Benefits payable less any payment adjustment."
    )
    identifier: Identifier | None = Field(
        default=None,
        description="Issuer's unique identifier for the payment instrument.",
    )


class ExplanationOfBenefitProcedure(MedplumFHIRBase):
    """Procedures performed on the patient relevant to the billing items with the claim."""

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
        default=..., description="A number to uniquely identify procedure entries."
    )
    type: list[CodeableConcept] | None = Field(
        default=None,
        description="When the condition was observed or the relative ranking.",
    )
    date: str | None = Field(
        default=None,
        description="Date and optionally time the procedure was performed.",
    )
    procedure_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="procedureCodeableConcept",
        description="The code or reference to a Procedure resource which identifies the clinical intervention performed.",
    )
    procedure_reference: Reference | None = Field(
        default=None,
        alias="procedureReference",
        description="The code or reference to a Procedure resource which identifies the clinical intervention performed.",
    )
    udi: list[Reference] | None = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )


class ExplanationOfBenefitProcessNote(MedplumFHIRBase):
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
    text: str | None = Field(
        default=None,
        description="The explanation or description associated with the processing.",
    )
    language: CodeableConcept | None = Field(
        default=None,
        description="A code to define the language used in the text of the note.",
    )


class ExplanationOfBenefitRelated(MedplumFHIRBase):
    """Other claims which are related to this claim such as prior submissions
    or claims for related services or for the same event.
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
    claim: Reference | None = Field(
        default=None, description="Reference to a related claim."
    )
    relationship: CodeableConcept | None = Field(
        default=None, description="A code to convey how the claims are related."
    )
    reference: Identifier | None = Field(
        default=None,
        description="An alternate organizational reference to the case or file to which this particular claim pertains.",
    )


class ExplanationOfBenefitSupportingInfo(MedplumFHIRBase):
    """Additional information codes regarding exceptions, special
    considerations, the condition, situation, prior or concurrent issues.
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
        description="A number to uniquely identify supporting information entries.",
    )
    category: CodeableConcept = Field(
        default=...,
        description="The general class of the information supplied: information; exception; accident, employment; onset, etc.",
    )
    code: CodeableConcept | None = Field(
        default=None,
        description="System and code pertaining to the specific information regarding special conditions relating to the setting, treatment or patient for which care is sought.",
    )
    timing_date: str | None = Field(
        default=None,
        alias="timingDate",
        description="The date when or period to which this information refers.",
    )
    timing_period: Period | None = Field(
        default=None,
        alias="timingPeriod",
        description="The date when or period to which this information refers.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_attachment: Attachment | None = Field(
        default=None,
        alias="valueAttachment",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    reason: Coding | None = Field(
        default=None,
        description="Provides the reason in the situation where a reason code is required in addition to the content.",
    )


class ExplanationOfBenefitTotal(MedplumFHIRBase):
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
