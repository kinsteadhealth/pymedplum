# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class InsurancePlan(MedplumFHIRBase):
    """Details of a Health Insurance product/plan provided by an organization."""

    resource_type: Literal["InsurancePlan"] = Field(
        default="InsurancePlan", alias="resourceType"
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
        description="Business identifiers assigned to this health insurance product which remain constant as the resource is updated and propagates from server to server.",
    )
    status: Literal["draft", "active", "retired", "unknown"] | None = Field(
        default=None, description="The current state of the health insurance product."
    )
    type: list[CodeableConcept] | None = Field(
        default=None, description="The kind of health insurance product."
    )
    name: str | None = Field(
        default=None,
        description="Official name of the health insurance product as designated by the owner.",
    )
    alias: list[str] | None = Field(
        default=None,
        description="A list of alternate names that the product is known as, or was known as in the past.",
    )
    period: Period | None = Field(
        default=None,
        description="The period of time that the health insurance product is available.",
    )
    owned_by: Reference | None = Field(
        default=None,
        alias="ownedBy",
        description="The entity that is providing the health insurance product and underwriting the risk. This is typically an insurance carriers, other third-party payers, or health plan sponsors comonly referred to as 'payers'.",
    )
    administered_by: Reference | None = Field(
        default=None,
        alias="administeredBy",
        description="An organization which administer other services such as underwriting, customer service and/or claims processing on behalf of the health insurance product owner.",
    )
    coverage_area: list[Reference] | None = Field(
        default=None,
        alias="coverageArea",
        description="The geographic region in which a health insurance product's benefits apply.",
    )
    contact: list[InsurancePlanContact] | None = Field(
        default=None,
        description="The contact for the health insurance product for a certain purpose.",
    )
    endpoint: list[Reference] | None = Field(
        default=None,
        description="The technical endpoints providing access to services operated for the health insurance product.",
    )
    network: list[Reference] | None = Field(
        default=None,
        description="Reference to the network included in the health insurance product.",
    )
    coverage: list[InsurancePlanCoverage] | None = Field(
        default=None,
        description="Details about the coverage offered by the insurance product.",
    )
    plan: list[InsurancePlanPlan] | None = Field(
        default=None, description="Details about an insurance plan."
    )


class InsurancePlanContact(MedplumFHIRBase):
    """The contact for the health insurance product for a certain purpose."""

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
    purpose: CodeableConcept | None = Field(
        default=None,
        description="Indicates a purpose for which the contact can be reached.",
    )
    name: HumanName | None = Field(
        default=None, description="A name associated with the contact."
    )
    telecom: list[ContactPoint] | None = Field(
        default=None,
        description="A contact detail (e.g. a telephone number or an email address) by which the party may be contacted.",
    )
    address: Address | None = Field(
        default=None, description="Visiting or postal addresses for the contact."
    )


class InsurancePlanCoverage(MedplumFHIRBase):
    """Details about the coverage offered by the insurance product."""

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
        description="Type of coverage (Medical; Dental; Mental Health; Substance Abuse; Vision; Drug; Short Term; Long Term Care; Hospice; Home Health).",
    )
    network: list[Reference] | None = Field(
        default=None,
        description="Reference to the network that providing the type of coverage.",
    )
    benefit: list[InsurancePlanCoverageBenefit] = Field(
        default=..., description="Specific benefits under this type of coverage."
    )


class InsurancePlanCoverageBenefit(MedplumFHIRBase):
    """Specific benefits under this type of coverage."""

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
        description="Type of benefit (primary care; speciality care; inpatient; outpatient).",
    )
    requirement: str | None = Field(
        default=None,
        description="The referral requirements to have access/coverage for this benefit.",
    )
    limit: list[InsurancePlanCoverageBenefitLimit] | None = Field(
        default=None, description="The specific limits on the benefit."
    )


class InsurancePlanCoverageBenefitLimit(MedplumFHIRBase):
    """The specific limits on the benefit."""

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
    value: Quantity | None = Field(
        default=None,
        description="The maximum amount of a service item a plan will pay for a covered benefit. For examples. wellness visits, or eyeglasses.",
    )
    code: CodeableConcept | None = Field(
        default=None, description="The specific limit on the benefit."
    )


class InsurancePlanPlan(MedplumFHIRBase):
    """Details about an insurance plan."""

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
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Business identifiers assigned to this health insurance plan which remain constant as the resource is updated and propagates from server to server.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Type of plan. For example, &quot;Platinum&quot; or &quot;High Deductable&quot;.",
    )
    coverage_area: list[Reference] | None = Field(
        default=None,
        alias="coverageArea",
        description="The geographic region in which a health insurance plan's benefits apply.",
    )
    network: list[Reference] | None = Field(
        default=None,
        description="Reference to the network that providing the type of coverage.",
    )
    general_cost: list[InsurancePlanPlanGeneralCost] | None = Field(
        default=None,
        alias="generalCost",
        description="Overall costs associated with the plan.",
    )
    specific_cost: list[InsurancePlanPlanSpecificCost] | None = Field(
        default=None,
        alias="specificCost",
        description="Costs associated with the coverage provided by the product.",
    )


class InsurancePlanPlanGeneralCost(MedplumFHIRBase):
    """Overall costs associated with the plan."""

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
    type: CodeableConcept | None = Field(default=None, description="Type of cost.")
    group_size: int | float | None = Field(
        default=None,
        alias="groupSize",
        description="Number of participants enrolled in the plan.",
    )
    cost: Money | None = Field(default=None, description="Value of the cost.")
    comment: str | None = Field(
        default=None,
        description="Additional information about the general costs associated with this plan.",
    )


class InsurancePlanPlanSpecificCost(MedplumFHIRBase):
    """Costs associated with the coverage provided by the product."""

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
        description="General category of benefit (Medical; Dental; Vision; Drug; Mental Health; Substance Abuse; Hospice, Home Health).",
    )
    benefit: list[InsurancePlanPlanSpecificCostBenefit] | None = Field(
        default=None,
        description="List of the specific benefits under this category of benefit.",
    )


class InsurancePlanPlanSpecificCostBenefit(MedplumFHIRBase):
    """List of the specific benefits under this category of benefit."""

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
        description="Type of specific benefit (preventative; primary care office visit; speciality office visit; hospitalization; emergency room; urgent care).",
    )
    cost: list[InsurancePlanPlanSpecificCostBenefitCost] | None = Field(
        default=None,
        description="List of the costs associated with a specific benefit.",
    )


class InsurancePlanPlanSpecificCostBenefitCost(MedplumFHIRBase):
    """List of the costs associated with a specific benefit."""

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
        description="Type of cost (copay; individual cap; family cap; coinsurance; deductible).",
    )
    applicability: CodeableConcept | None = Field(
        default=None,
        description="Whether the cost applies to in-network or out-of-network providers (in-network; out-of-network; other).",
    )
    qualifiers: list[CodeableConcept] | None = Field(
        default=None,
        description="Additional information about the cost, such as information about funding sources (e.g. HSA, HRA, FSA, RRA).",
    )
    value: Quantity | None = Field(
        default=None,
        description="The actual cost value. (some of the costs may be represented as percentages rather than currency, e.g. 10% coinsurance).",
    )
