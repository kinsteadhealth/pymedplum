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
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class Account(MedplumFHIRBase):
    """A financial tool for tracking value accrued for a particular purpose. In
    the healthcare field, used to track charges for a patient, cost centers,
    etc.
    """

    resource_type: Literal["Account"] = Field(default="Account", alias="resourceType")

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
        description="Unique identifier used to reference the account. Might or might not be intended for human use (e.g. credit card number).",
    )
    status: Literal["active", "inactive", "entered-in-error", "on-hold", "unknown"] = (
        Field(
            default=...,
            description="Indicates whether the account is presently used/usable or not.",
        )
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Categorizes the account for reporting and searching purposes.",
    )
    name: str | None = Field(
        default=None,
        description="Name used for the account when displaying it to humans in reports, etc.",
    )
    subject: list[Reference] | None = Field(
        default=None,
        description="Identifies the entity which incurs the expenses. While the immediate recipients of services or goods might be entities related to the subject, the expenses were ultimately incurred by the subject of the Account.",
    )
    service_period: Period | None = Field(
        default=None,
        alias="servicePeriod",
        description="The date range of services associated with this account.",
    )
    coverage: list[AccountCoverage] | None = Field(
        default=None,
        description="The party(s) that are responsible for covering the payment of this account, and what order should they be applied to the account.",
    )
    owner: Reference | None = Field(
        default=None,
        description="Indicates the service area, hospital, department, etc. with responsibility for managing the Account.",
    )
    description: str | None = Field(
        default=None,
        description="Provides additional information about what the account tracks and how it is used.",
    )
    guarantor: list[AccountGuarantor] | None = Field(
        default=None,
        description="The parties responsible for balancing the account if other payment options fall short.",
    )
    part_of: Reference | None = Field(
        default=None, alias="partOf", description="Reference to a parent Account."
    )


class AccountCoverage(MedplumFHIRBase):
    """The party(s) that are responsible for covering the payment of this
    account, and what order should they be applied to the account.
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
    coverage: Reference = Field(
        default=...,
        description="The party(s) that contribute to payment (or part of) of the charges applied to this account (including self-pay). A coverage may only be responsible for specific types of charges, and the sequence of the coverages in the account could be important when processing billing.",
    )
    priority: int | float | None = Field(
        default=None,
        description="The priority of the coverage in the context of this account.",
    )


class AccountGuarantor(MedplumFHIRBase):
    """The parties responsible for balancing the account if other payment
    options fall short.
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
    party: Reference = Field(default=..., description="The entity who is responsible.")
    on_hold: bool | None = Field(
        default=None,
        alias="onHold",
        description="A guarantor may be placed on credit hold or otherwise have their role temporarily suspended.",
    )
    period: Period | None = Field(
        default=None,
        description="The timeframe during which the guarantor accepts responsibility for the account.",
    )
