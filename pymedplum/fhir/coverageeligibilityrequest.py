# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CoverageEligibilityRequest(MedplumFHIRBase):
    """The CoverageEligibilityRequest provides patient and insurance coverage
    information to an insurer for them to respond, in the form of an
    CoverageEligibilityResponse, with information regarding whether the
    stated coverage is valid and in-force and optionally to provide the
    insurance details of the policy.
    """

    resource_type: Literal["CoverageEligibilityRequest"] = Field(
        default="CoverageEligibilityRequest", alias="resourceType"
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
        description="A unique identifier assigned to this coverage eligiblity request.",
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    priority: Optional[CodeableConcept] = Field(
        default=None,
        description="When the requestor expects the processor to complete processing.",
    )
    purpose: List[
        Literal["auth-requirements", "benefits", "discovery", "validation"]
    ] = Field(
        default=...,
        description="Code to specify whether requesting: prior authorization requirements for some service categories or billing codes; benefits for coverages specified or discovered; discovery and return of coverages for the patient; and/or validation that the specified coverage is in-force at the date/period specified or 'now' if not specified.",
    )
    patient: Reference = Field(
        default=...,
        description="The party who is the beneficiary of the supplied coverage and for whom eligibility is sought.",
    )
    serviced_date: Optional[str] = Field(
        default=None,
        alias="servicedDate",
        description="The date or dates when the enclosed suite of services were performed or completed.",
    )
    serviced_period: Optional[Period] = Field(
        default=None,
        alias="servicedPeriod",
        description="The date or dates when the enclosed suite of services were performed or completed.",
    )
    created: str = Field(
        default=..., description="The date when this resource was created."
    )
    enterer: Optional[Reference] = Field(
        default=None, description="Person who created the request."
    )
    provider: Optional[Reference] = Field(
        default=None, description="The provider which is responsible for the request."
    )
    insurer: Reference = Field(
        default=...,
        description="The Insurer who issued the coverage in question and is the recipient of the request.",
    )
    facility: Optional[Reference] = Field(
        default=None,
        description="Facility where the services are intended to be provided.",
    )
    supporting_info: Optional[List[CoverageEligibilityRequestSupportingInfo]] = Field(
        default=None,
        alias="supportingInfo",
        description="Additional information codes regarding exceptions, special considerations, the condition, situation, prior or concurrent issues.",
    )
    insurance: Optional[List[CoverageEligibilityRequestInsurance]] = Field(
        default=None,
        description="Financial instruments for reimbursement for the health care products and services.",
    )
    item: Optional[List[CoverageEligibilityRequestItem]] = Field(
        default=None,
        description="Service categories or billable services for which benefit details and/or an authorization prior to service delivery may be required by the payor.",
    )


class CoverageEligibilityRequestInsurance(MedplumFHIRBase):
    """Financial instruments for reimbursement for the health care products and services."""

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
    focal: Optional[bool] = Field(
        default=None,
        description="A flag to indicate that this Coverage is to be used for evaluation of this request when set to true.",
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


class CoverageEligibilityRequestItem(MedplumFHIRBase):
    """Service categories or billable services for which benefit details and/or
    an authorization prior to service delivery may be required by the payor.
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
    supporting_info_sequence: Optional[List[Union[int, float]]] = Field(
        default=None,
        alias="supportingInfoSequence",
        description="Exceptions, special conditions and supporting information applicable for this service or product line.",
    )
    category: Optional[CodeableConcept] = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
    )
    product_or_service: Optional[CodeableConcept] = Field(
        default=None,
        alias="productOrService",
        description="This contains the product, service, drug or other billing code for the item.",
    )
    modifier: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    provider: Optional[Reference] = Field(
        default=None,
        description="The practitioner who is responsible for the product or service to be rendered to the patient.",
    )
    quantity: Optional[Quantity] = Field(
        default=None, description="The number of repetitions of a service or product."
    )
    unit_price: Optional[Money] = Field(
        default=None,
        alias="unitPrice",
        description="The amount charged to the patient by the provider for a single unit.",
    )
    facility: Optional[Reference] = Field(
        default=None, description="Facility where the services will be provided."
    )
    diagnosis: Optional[List[CoverageEligibilityRequestItemDiagnosis]] = Field(
        default=None, description="Patient diagnosis for which care is sought."
    )
    detail: Optional[List[Reference]] = Field(
        default=None,
        description="The plan/proposal/order describing the proposed service in detail.",
    )


class CoverageEligibilityRequestItemDiagnosis(MedplumFHIRBase):
    """Patient diagnosis for which care is sought."""

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


class CoverageEligibilityRequestSupportingInfo(MedplumFHIRBase):
    """Additional information codes regarding exceptions, special
    considerations, the condition, situation, prior or concurrent issues.
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
    sequence: Union[int, float] = Field(
        default=...,
        description="A number to uniquely identify supporting information entries.",
    )
    information: Reference = Field(
        default=...,
        description="Additional data or information such as resources, documents, images etc. including references to the data or the actual inclusion of the data.",
    )
    applies_to_all: Optional[bool] = Field(
        default=None,
        alias="appliesToAll",
        description="The supporting materials are applicable for all detail items, product/servce categories and specific billing codes.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CoverageEligibilityRequest", CoverageEligibilityRequest)
    register_model(
        "CoverageEligibilityRequestInsurance", CoverageEligibilityRequestInsurance
    )
    register_model("CoverageEligibilityRequestItem", CoverageEligibilityRequestItem)
    register_model(
        "CoverageEligibilityRequestItemDiagnosis",
        CoverageEligibilityRequestItemDiagnosis,
    )
    register_model(
        "CoverageEligibilityRequestSupportingInfo",
        CoverageEligibilityRequestSupportingInfo,
    )
