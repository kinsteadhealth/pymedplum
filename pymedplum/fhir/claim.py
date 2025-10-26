# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Claim(MedplumFHIRBase):
    """A provider issued list of professional services and products which have
    been provided, or are to be provided, to a patient which is sent to an
    insurer for reimbursement.
    """

    resource_type: Literal["Claim"] = Field(default="Claim", alias="resourceType")

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
    contained: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None, description="A unique identifier assigned to this claim."
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    type: CodeableConcept = Field(
        default=...,
        description="The category of claim, e.g. oral, pharmacy, vision, institutional, professional.",
    )
    sub_type: Optional[CodeableConcept] = Field(
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
        description="The party to whom the professional services and/or products have been supplied or are being considered and for whom actual or forecast reimbursement is sought.",
    )
    billable_period: Optional[Period] = Field(
        default=None,
        alias="billablePeriod",
        description="The period for which charges are being submitted.",
    )
    created: str = Field(default=..., description="The date this resource was created.")
    enterer: Optional[Reference] = Field(
        default=None,
        description="Individual who created the claim, predetermination or preauthorization.",
    )
    insurer: Optional[Reference] = Field(
        default=None, description="The Insurer who is target of the request."
    )
    provider: Reference = Field(
        default=...,
        description="The provider which is responsible for the claim, predetermination or preauthorization.",
    )
    priority: CodeableConcept = Field(
        default=...,
        description="The provider-required urgency of processing the request. Typical values include: stat, routine deferred.",
    )
    funds_reserve: Optional[CodeableConcept] = Field(
        default=None,
        alias="fundsReserve",
        description="A code to indicate whether and for whom funds are to be reserved for future claims.",
    )
    related: Optional[list[ClaimRelated]] = Field(
        default=None,
        description="Other claims which are related to this claim such as prior submissions or claims for related services or for the same event.",
    )
    prescription: Optional[Reference] = Field(
        default=None,
        description="Prescription to support the dispensing of pharmacy, device or vision products.",
    )
    original_prescription: Optional[Reference] = Field(
        default=None,
        alias="originalPrescription",
        description="Original prescription which has been superseded by this prescription to support the dispensing of pharmacy services, medications or products.",
    )
    payee: Optional[ClaimPayee] = Field(
        default=None,
        description="The party to be reimbursed for cost of the products and services according to the terms of the policy.",
    )
    referral: Optional[Reference] = Field(
        default=None, description="A reference to a referral resource."
    )
    facility: Optional[Reference] = Field(
        default=None, description="Facility where the services were provided."
    )
    care_team: Optional[list[ClaimCareTeam]] = Field(
        default=None,
        alias="careTeam",
        description="The members of the team who provided the products and services.",
    )
    supporting_info: Optional[list[ClaimSupportingInfo]] = Field(
        default=None,
        alias="supportingInfo",
        description="Additional information codes regarding exceptions, special considerations, the condition, situation, prior or concurrent issues.",
    )
    diagnosis: Optional[list[ClaimDiagnosis]] = Field(
        default=None,
        description="Information about diagnoses relevant to the claim items.",
    )
    procedure: Optional[list[ClaimProcedure]] = Field(
        default=None,
        description="Procedures performed on the patient relevant to the billing items with the claim.",
    )
    insurance: list[ClaimInsurance] = Field(
        default=...,
        description="Financial instruments for reimbursement for the health care products and services specified on the claim.",
    )
    accident: Optional[ClaimAccident] = Field(
        default=None,
        description="Details of an accident which resulted in injuries which required the products and services listed in the claim.",
    )
    item: Optional[list[ClaimItem]] = Field(
        default=None,
        description="A claim line. Either a simple product or service or a 'group' of details which can each be a simple items or groups of sub-details.",
    )
    total: Optional[Money] = Field(
        default=None, description="The total value of the all the items in the claim."
    )


class ClaimAccident(MedplumFHIRBase):
    """Details of an accident which resulted in injuries which required the
    products and services listed in the claim.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    date: str = Field(
        default=...,
        description="Date of an accident event related to the products and services contained in the claim.",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The type or context of the accident event for the purposes of selection of potential insurance coverages and determination of coordination between insurers.",
    )
    location_address: Optional[Address] = Field(
        default=None,
        alias="locationAddress",
        description="The physical location of the accident event.",
    )
    location_reference: Optional[Reference] = Field(
        default=None,
        alias="locationReference",
        description="The physical location of the accident event.",
    )


class ClaimCareTeam(MedplumFHIRBase):
    """The members of the team who provided the products and services."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=..., description="A number to uniquely identify care team entries."
    )
    provider: Reference = Field(
        default=...,
        description="Member of the team who provided the product or service.",
    )
    responsible: Optional[bool] = Field(
        default=None,
        description="The party who is billing and/or responsible for the claimed products or services.",
    )
    role: Optional[CodeableConcept] = Field(
        default=None,
        description="The lead, assisting or supervising practitioner and their discipline if a multidisciplinary team.",
    )
    qualification: Optional[CodeableConcept] = Field(
        default=None,
        description="The qualification of the practitioner which is applicable for this service.",
    )


class ClaimDiagnosis(MedplumFHIRBase):
    """Information about diagnoses relevant to the claim items."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=..., description="A number to uniquely identify diagnosis entries."
    )
    diagnosis_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="diagnosisCodeableConcept",
        description="The nature of illness or problem in a coded form or as a reference to an external defined Condition.",
    )
    diagnosis_reference: Optional[Reference] = Field(
        default=None,
        alias="diagnosisReference",
        description="The nature of illness or problem in a coded form or as a reference to an external defined Condition.",
    )
    type: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="When the condition was observed or the relative ranking.",
    )
    on_admission: Optional[CodeableConcept] = Field(
        default=None,
        alias="onAdmission",
        description="Indication of whether the diagnosis was present on admission to a facility.",
    )
    package_code: Optional[CodeableConcept] = Field(
        default=None,
        alias="packageCode",
        description="A package billing code or bundle code used to group products and services to a particular health condition (such as heart attack) which is based on a predetermined grouping code system.",
    )


class ClaimInsurance(MedplumFHIRBase):
    """Financial instruments for reimbursement for the health care products and
    services specified on the claim.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=...,
        description="A number to uniquely identify insurance entries and provide a sequence of coverages to convey coordination of benefit order.",
    )
    focal: bool = Field(
        default=...,
        description="A flag to indicate that this Coverage is to be used for adjudication of this claim when set to true.",
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        description="The business identifier to be used when the claim is sent for adjudication against this insurance policy.",
    )
    coverage: Reference = Field(
        default=...,
        description="Reference to the insurance card level information contained in the Coverage resource. The coverage issuing insurer will use these details to locate the patient's actual coverage within the insurer's information system.",
    )
    business_arrangement: Optional[str] = Field(
        default=None,
        alias="businessArrangement",
        description="A business agreement number established between the provider and the insurer for special business processing purposes.",
    )
    pre_auth_ref: Optional[list[str]] = Field(
        default=None,
        alias="preAuthRef",
        description="Reference numbers previously provided by the insurer to the provider to be quoted on subsequent claims containing services or products related to the prior authorization.",
    )
    claim_response: Optional[Reference] = Field(
        default=None,
        alias="claimResponse",
        description="The result of the adjudication of the line items for the Coverage specified in this insurance.",
    )


class ClaimItem(MedplumFHIRBase):
    """A claim line. Either a simple product or service or a 'group' of details
    which can each be a simple items or groups of sub-details.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=..., description="A number to uniquely identify item entries."
    )
    care_team_sequence: Optional[list[Union[int, float]]] = Field(
        default=None,
        alias="careTeamSequence",
        description="CareTeam members related to this service or product.",
    )
    diagnosis_sequence: Optional[list[Union[int, float]]] = Field(
        default=None,
        alias="diagnosisSequence",
        description="Diagnosis applicable for this service or product.",
    )
    procedure_sequence: Optional[list[Union[int, float]]] = Field(
        default=None,
        alias="procedureSequence",
        description="Procedures applicable for this service or product.",
    )
    information_sequence: Optional[list[Union[int, float]]] = Field(
        default=None,
        alias="informationSequence",
        description="Exceptions, special conditions and supporting information applicable for this service or product.",
    )
    revenue: Optional[CodeableConcept] = Field(
        default=None,
        description="The type of revenue or cost center providing the product and/or service.",
    )
    category: Optional[CodeableConcept] = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
    )
    product_or_service: CodeableConcept = Field(
        default=...,
        alias="productOrService",
        description="When the value is a group code then this item collects a set of related claim details, otherwise this contains the product, service, drug or other billing code for the item.",
    )
    modifier: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    program_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="programCode",
        description="Identifies the program under which this may be recovered.",
    )
    serviced_date: Optional[str] = Field(
        default=None,
        alias="servicedDate",
        description="The date or dates when the service or product was supplied, performed or completed.",
    )
    serviced_period: Optional[Period] = Field(
        default=None,
        alias="servicedPeriod",
        description="The date or dates when the service or product was supplied, performed or completed.",
    )
    location_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="locationCodeableConcept",
        description="Where the product or service was provided.",
    )
    location_address: Optional[Address] = Field(
        default=None,
        alias="locationAddress",
        description="Where the product or service was provided.",
    )
    location_reference: Optional[Reference] = Field(
        default=None,
        alias="locationReference",
        description="Where the product or service was provided.",
    )
    quantity: Optional[Quantity] = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Optional[Money] = Field(
        default=None,
        alias="unitPrice",
        description="If the item is not a group then this is the fee for the product or service, otherwise this is the total of the fees for the details of the group.",
    )
    factor: Optional[Union[int, float]] = Field(
        default=None,
        description="A real number that represents a multiplier used in determining the overall value of services delivered and/or goods received. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.",
    )
    net: Optional[Money] = Field(
        default=None,
        description="The quantity times the unit price for an additional service or product or charge.",
    )
    udi: Optional[list[Reference]] = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )
    body_site: Optional[CodeableConcept] = Field(
        default=None,
        alias="bodySite",
        description="Physical service site on the patient (limb, tooth, etc.).",
    )
    sub_site: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="subSite",
        description="A region or surface of the bodySite, e.g. limb region or tooth surface(s).",
    )
    encounter: Optional[list[Reference]] = Field(
        default=None,
        description="The Encounters during which this Claim was created or to which the creation of this record is tightly associated.",
    )
    detail: Optional[list[ClaimItemDetail]] = Field(
        default=None,
        description="A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are simple items.",
    )


class ClaimItemDetail(MedplumFHIRBase):
    """A claim detail line. Either a simple (a product or service) or a 'group'
    of sub-details which are simple items.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=..., description="A number to uniquely identify item entries."
    )
    revenue: Optional[CodeableConcept] = Field(
        default=None,
        description="The type of revenue or cost center providing the product and/or service.",
    )
    category: Optional[CodeableConcept] = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
    )
    product_or_service: CodeableConcept = Field(
        default=...,
        alias="productOrService",
        description="When the value is a group code then this item collects a set of related claim details, otherwise this contains the product, service, drug or other billing code for the item.",
    )
    modifier: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    program_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="programCode",
        description="Identifies the program under which this may be recovered.",
    )
    quantity: Optional[Quantity] = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Optional[Money] = Field(
        default=None,
        alias="unitPrice",
        description="If the item is not a group then this is the fee for the product or service, otherwise this is the total of the fees for the details of the group.",
    )
    factor: Optional[Union[int, float]] = Field(
        default=None,
        description="A real number that represents a multiplier used in determining the overall value of services delivered and/or goods received. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.",
    )
    net: Optional[Money] = Field(
        default=None,
        description="The quantity times the unit price for an additional service or product or charge.",
    )
    udi: Optional[list[Reference]] = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )
    sub_detail: Optional[list[ClaimItemDetailSubDetail]] = Field(
        default=None,
        alias="subDetail",
        description="A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are simple items.",
    )


class ClaimItemDetailSubDetail(MedplumFHIRBase):
    """A claim detail line. Either a simple (a product or service) or a 'group'
    of sub-details which are simple items.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=..., description="A number to uniquely identify item entries."
    )
    revenue: Optional[CodeableConcept] = Field(
        default=None,
        description="The type of revenue or cost center providing the product and/or service.",
    )
    category: Optional[CodeableConcept] = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
    )
    product_or_service: CodeableConcept = Field(
        default=...,
        alias="productOrService",
        description="When the value is a group code then this item collects a set of related claim details, otherwise this contains the product, service, drug or other billing code for the item.",
    )
    modifier: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    program_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="programCode",
        description="Identifies the program under which this may be recovered.",
    )
    quantity: Optional[Quantity] = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Optional[Money] = Field(
        default=None,
        alias="unitPrice",
        description="If the item is not a group then this is the fee for the product or service, otherwise this is the total of the fees for the details of the group.",
    )
    factor: Optional[Union[int, float]] = Field(
        default=None,
        description="A real number that represents a multiplier used in determining the overall value of services delivered and/or goods received. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.",
    )
    net: Optional[Money] = Field(
        default=None,
        description="The quantity times the unit price for an additional service or product or charge.",
    )
    udi: Optional[list[Reference]] = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )


class ClaimPayee(MedplumFHIRBase):
    """The party to be reimbursed for cost of the products and services
    according to the terms of the policy.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: CodeableConcept = Field(
        default=...,
        description="Type of Party to be reimbursed: subscriber, provider, other.",
    )
    party: Optional[Reference] = Field(
        default=None,
        description="Reference to the individual or organization to whom any payment will be made.",
    )


class ClaimProcedure(MedplumFHIRBase):
    """Procedures performed on the patient relevant to the billing items with the claim."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=..., description="A number to uniquely identify procedure entries."
    )
    type: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="When the condition was observed or the relative ranking.",
    )
    date: Optional[str] = Field(
        default=None,
        description="Date and optionally time the procedure was performed.",
    )
    procedure_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="procedureCodeableConcept",
        description="The code or reference to a Procedure resource which identifies the clinical intervention performed.",
    )
    procedure_reference: Optional[Reference] = Field(
        default=None,
        alias="procedureReference",
        description="The code or reference to a Procedure resource which identifies the clinical intervention performed.",
    )
    udi: Optional[list[Reference]] = Field(
        default=None,
        description="Unique Device Identifiers associated with this line item.",
    )


class ClaimRelated(MedplumFHIRBase):
    """Other claims which are related to this claim such as prior submissions
    or claims for related services or for the same event.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    claim: Optional[Reference] = Field(
        default=None, description="Reference to a related claim."
    )
    relationship: Optional[CodeableConcept] = Field(
        default=None, description="A code to convey how the claims are related."
    )
    reference: Optional[Identifier] = Field(
        default=None,
        description="An alternate organizational reference to the case or file to which this particular claim pertains.",
    )


class ClaimSupportingInfo(MedplumFHIRBase):
    """Additional information codes regarding exceptions, special
    considerations, the condition, situation, prior or concurrent issues.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    sequence: Union[int, float] = Field(
        default=...,
        description="A number to uniquely identify supporting information entries.",
    )
    category: CodeableConcept = Field(
        default=...,
        description="The general class of the information supplied: information; exception; accident, employment; onset, etc.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="System and code pertaining to the specific information regarding special conditions relating to the setting, treatment or patient for which care is sought.",
    )
    timing_date: Optional[str] = Field(
        default=None,
        alias="timingDate",
        description="The date when or period to which this information refers.",
    )
    timing_period: Optional[Period] = Field(
        default=None,
        alias="timingPeriod",
        description="The date when or period to which this information refers.",
    )
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="valueAttachment",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    reason: Optional[CodeableConcept] = Field(
        default=None,
        description="Provides the reason in the situation where a reason code is required in addition to the content.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Claim", Claim)
    register_model("ClaimAccident", ClaimAccident)
    register_model("ClaimCareTeam", ClaimCareTeam)
    register_model("ClaimDiagnosis", ClaimDiagnosis)
    register_model("ClaimInsurance", ClaimInsurance)
    register_model("ClaimItem", ClaimItem)
    register_model("ClaimItemDetail", ClaimItemDetail)
    register_model("ClaimItemDetailSubDetail", ClaimItemDetailSubDetail)
    register_model("ClaimPayee", ClaimPayee)
    register_model("ClaimProcedure", ClaimProcedure)
    register_model("ClaimRelated", ClaimRelated)
    register_model("ClaimSupportingInfo", ClaimSupportingInfo)
