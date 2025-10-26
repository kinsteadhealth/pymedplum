# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CoverageEligibilityResponse(MedplumFHIRBase):
    """This resource provides eligibility and plan details from the processing
    of an CoverageEligibilityRequest resource.
    """

    resource_type: Literal["CoverageEligibilityResponse"] = Field(
        default="CoverageEligibilityResponse", alias="resourceType"
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
        default=None,
        description="A unique identifier assigned to this coverage eligiblity request.",
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    purpose: list[
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
    created: str = Field(default=..., description="The date this resource was created.")
    requestor: Optional[Reference] = Field(
        default=None, description="The provider which is responsible for the request."
    )
    request: Reference = Field(
        default=..., description="Reference to the original request resource."
    )
    outcome: Literal["queued", "complete", "error", "partial"] = Field(
        default=..., description="The outcome of the request processing."
    )
    disposition: Optional[str] = Field(
        default=None,
        description="A human readable description of the status of the adjudication.",
    )
    insurer: Reference = Field(
        default=...,
        description="The Insurer who issued the coverage in question and is the author of the response.",
    )
    insurance: Optional[list[CoverageEligibilityResponseInsurance]] = Field(
        default=None,
        description="Financial instruments for reimbursement for the health care products and services.",
    )
    pre_auth_ref: Optional[str] = Field(
        default=None,
        alias="preAuthRef",
        description="A reference from the Insurer to which these services pertain to be used on further communication and as proof that the request occurred.",
    )
    form: Optional[CodeableConcept] = Field(
        default=None,
        description="A code for the form to be used for printing the content.",
    )
    error: Optional[list[CoverageEligibilityResponseError]] = Field(
        default=None,
        description="Errors encountered during the processing of the request.",
    )


class CoverageEligibilityResponseError(MedplumFHIRBase):
    """Errors encountered during the processing of the request."""

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
    code: CodeableConcept = Field(
        default=...,
        description="An error code,from a specified code system, which details why the eligibility check could not be performed.",
    )


class CoverageEligibilityResponseInsurance(MedplumFHIRBase):
    """Financial instruments for reimbursement for the health care products and services."""

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
    coverage: Reference = Field(
        default=...,
        description="Reference to the insurance card level information contained in the Coverage resource. The coverage issuing insurer will use these details to locate the patient's actual coverage within the insurer's information system.",
    )
    inforce: Optional[bool] = Field(
        default=None,
        description="Flag indicating if the coverage provided is inforce currently if no service date(s) specified or for the whole duration of the service dates.",
    )
    benefit_period: Optional[Period] = Field(
        default=None,
        alias="benefitPeriod",
        description="The term of the benefits documented in this response.",
    )
    item: Optional[list[CoverageEligibilityResponseInsuranceItem]] = Field(
        default=None,
        description="Benefits and optionally current balances, and authorization details by category or service.",
    )


class CoverageEligibilityResponseInsuranceItem(MedplumFHIRBase):
    """Benefits and optionally current balances, and authorization details by
    category or service.
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
    category: Optional[CodeableConcept] = Field(
        default=None,
        description="Code to identify the general type of benefits under which products and services are provided.",
    )
    product_or_service: Optional[CodeableConcept] = Field(
        default=None,
        alias="productOrService",
        description="This contains the product, service, drug or other billing code for the item.",
    )
    modifier: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Item typification or modifiers codes to convey additional context for the product or service.",
    )
    provider: Optional[Reference] = Field(
        default=None,
        description="The practitioner who is eligible for the provision of the product or service.",
    )
    excluded: Optional[bool] = Field(
        default=None,
        description="True if the indicated class of service is excluded from the plan, missing or False indicates the product or service is included in the coverage.",
    )
    name: Optional[str] = Field(
        default=None, description="A short name or tag for the benefit."
    )
    description: Optional[str] = Field(
        default=None,
        description="A richer description of the benefit or services covered.",
    )
    network: Optional[CodeableConcept] = Field(
        default=None,
        description="Is a flag to indicate whether the benefits refer to in-network providers or out-of-network providers.",
    )
    unit: Optional[CodeableConcept] = Field(
        default=None,
        description="Indicates if the benefits apply to an individual or to the family.",
    )
    term: Optional[CodeableConcept] = Field(
        default=None,
        description="The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'.",
    )
    benefit: Optional[list[CoverageEligibilityResponseInsuranceItemBenefit]] = Field(
        default=None, description="Benefits used to date."
    )
    authorization_required: Optional[bool] = Field(
        default=None,
        alias="authorizationRequired",
        description="A boolean flag indicating whether a preauthorization is required prior to actual service delivery.",
    )
    authorization_supporting: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="authorizationSupporting",
        description="Codes or comments regarding information or actions associated with the preauthorization.",
    )
    authorization_url: Optional[str] = Field(
        default=None,
        alias="authorizationUrl",
        description="A web location for obtaining requirements or descriptive information regarding the preauthorization.",
    )


class CoverageEligibilityResponseInsuranceItemBenefit(MedplumFHIRBase):
    """Benefits used to date."""

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
        default=..., description="Classification of benefit being provided."
    )
    allowed_unsigned_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="allowedUnsignedInt",
        description="The quantity of the benefit which is permitted under the coverage.",
    )
    allowed_string: Optional[str] = Field(
        default=None,
        alias="allowedString",
        description="The quantity of the benefit which is permitted under the coverage.",
    )
    allowed_money: Optional[Money] = Field(
        default=None,
        alias="allowedMoney",
        description="The quantity of the benefit which is permitted under the coverage.",
    )
    used_unsigned_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="usedUnsignedInt",
        description="The quantity of the benefit which have been consumed to date.",
    )
    used_string: Optional[str] = Field(
        default=None,
        alias="usedString",
        description="The quantity of the benefit which have been consumed to date.",
    )
    used_money: Optional[Money] = Field(
        default=None,
        alias="usedMoney",
        description="The quantity of the benefit which have been consumed to date.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CoverageEligibilityResponse", CoverageEligibilityResponse)
    register_model("CoverageEligibilityResponseError", CoverageEligibilityResponseError)
    register_model(
        "CoverageEligibilityResponseInsurance", CoverageEligibilityResponseInsurance
    )
    register_model(
        "CoverageEligibilityResponseInsuranceItem",
        CoverageEligibilityResponseInsuranceItem,
    )
    register_model(
        "CoverageEligibilityResponseInsuranceItemBenefit",
        CoverageEligibilityResponseInsuranceItemBenefit,
    )
