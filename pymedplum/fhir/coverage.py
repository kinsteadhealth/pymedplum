# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

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
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class Coverage(MedplumFHIRBase):
    """Financial instrument which may be used to reimburse or pay for health
    care products and services. Includes both insurance and self-payment.
    """

    resource_type: Literal["Coverage"] = Field(default="Coverage", alias="resourceType")

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
        default=None, description="A unique identifier assigned to this coverage."
    )
    status: Literal["active", "cancelled", "draft", "entered-in-error"] = Field(
        default=..., description="The status of the resource instance."
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The type of coverage: social program, medical plan, accident coverage (workers compensation, auto), group health or payment by an individual or organization.",
    )
    policy_holder: Optional[Reference] = Field(
        default=None,
        alias="policyHolder",
        description="The party who 'owns' the insurance policy.",
    )
    subscriber: Optional[Reference] = Field(
        default=None,
        description="The party who has signed-up for or 'owns' the contractual relationship to the policy or to whom the benefit of the policy for services rendered to them or their family is due.",
    )
    subscriber_id: Optional[str] = Field(
        default=None,
        alias="subscriberId",
        description="The insurer assigned ID for the Subscriber.",
    )
    beneficiary: Reference = Field(
        default=...,
        description="The party who benefits from the insurance coverage; the patient when products and/or services are provided.",
    )
    dependent: Optional[str] = Field(
        default=None,
        description="A unique identifier for a dependent under the coverage.",
    )
    relationship: Optional[CodeableConcept] = Field(
        default=None,
        description="The relationship of beneficiary (patient) to the subscriber.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="Time period during which the coverage is in force. A missing start date indicates the start date isn't known, a missing end date means the coverage is continuing to be in force.",
    )
    payor: list[Reference] = Field(
        default=...,
        description="The program or plan underwriter or payor including both insurance and non-insurance agreements, such as patient-pay agreements.",
    )
    class_: Optional[list[CoverageClass]] = Field(
        default=None,
        alias="class",
        description="A suite of underwriter specific classifiers.",
    )
    order: Optional[Union[int, float]] = Field(
        default=None,
        description="The order of applicability of this coverage relative to other coverages which are currently in force. Note, there may be gaps in the numbering and this does not imply primary, secondary etc. as the specific positioning of coverages depends upon the episode of care.",
    )
    network: Optional[str] = Field(
        default=None,
        description="The insurer-specific identifier for the insurer-defined network of providers to which the beneficiary may seek treatment which will be covered at the 'in-network' rate, otherwise 'out of network' terms and conditions apply.",
    )
    cost_to_beneficiary: Optional[list[CoverageCostToBeneficiary]] = Field(
        default=None,
        alias="costToBeneficiary",
        description="A suite of codes indicating the cost category and associated amount which have been detailed in the policy and may have been included on the health card.",
    )
    subrogation: Optional[bool] = Field(
        default=None,
        description="When 'subrogation=true' this insurance instance has been included not for adjudication but to provide insurers with the details to recover costs.",
    )
    contract: Optional[list[Reference]] = Field(
        default=None,
        description="The policy(s) which constitute this insurance coverage.",
    )


class CoverageClass(MedplumFHIRBase):
    """A suite of underwriter specific classifiers."""

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
        description="The type of classification for which an insurer-specific class label or number and optional name is provided, for example may be used to identify a class of coverage or employer group, Policy, Plan.",
    )
    value: str = Field(
        default=...,
        description="The alphanumeric string value associated with the insurer issued label.",
    )
    name: Optional[str] = Field(
        default=None, description="A short description for the class."
    )


class CoverageCostToBeneficiary(MedplumFHIRBase):
    """A suite of codes indicating the cost category and associated amount
    which have been detailed in the policy and may have been included on the
    health card.
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
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The category of patient centric costs associated with treatment.",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="The amount due from the patient for the cost category.",
    )
    value_money: Optional[Money] = Field(
        default=None,
        alias="valueMoney",
        description="The amount due from the patient for the cost category.",
    )
    exception: Optional[list[CoverageCostToBeneficiaryException]] = Field(
        default=None,
        description="A suite of codes indicating exceptions or reductions to patient costs and their effective periods.",
    )


class CoverageCostToBeneficiaryException(MedplumFHIRBase):
    """A suite of codes indicating exceptions or reductions to patient costs
    and their effective periods.
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
        default=..., description="The code for the specific exception."
    )
    period: Optional[Period] = Field(
        default=None, description="The timeframe during when the exception is in force."
    )
