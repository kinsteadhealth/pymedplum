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
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.timing import Timing


class ChargeItem(MedplumFHIRBase):
    """The resource ChargeItem describes the provision of healthcare provider
    products for a certain patient, therefore referring not only to the
    product, but containing in addition details of the provision, like date,
    time, amounts and participating organizations and persons. Main Usage of
    the ChargeItem is to enable the billing process and internal cost
    allocation.
    """

    resource_type: Literal["ChargeItem"] = Field(
        default="ChargeItem", alias="resourceType"
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
        description="Identifiers assigned to this event performer or other systems.",
    )
    definition_uri: list[str] | None = Field(
        default=None,
        alias="definitionUri",
        description="References the (external) source of pricing information, rules of application for the code this ChargeItem uses.",
    )
    definition_canonical: list[str] | None = Field(
        default=None,
        alias="definitionCanonical",
        description="References the source of pricing information, rules of application for the code this ChargeItem uses.",
    )
    status: Literal[
        "planned",
        "billable",
        "not-billable",
        "aborted",
        "billed",
        "entered-in-error",
        "unknown",
    ] = Field(default=..., description="The current state of the ChargeItem.")
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="ChargeItems can be grouped to larger ChargeItems covering the whole set.",
    )
    code: CodeableConcept = Field(
        default=...,
        description="A code that identifies the charge, like a billing code.",
    )
    subject: Reference = Field(
        default=...,
        description="The individual or set of individuals the action is being or was performed on.",
    )
    context: Reference | None = Field(
        default=None,
        description="The encounter or episode of care that establishes the context for this event.",
    )
    occurrence_date_time: str | None = Field(
        default=None,
        alias="occurrenceDateTime",
        description="Date/time(s) or duration when the charged service was applied.",
    )
    occurrence_period: Period | None = Field(
        default=None,
        alias="occurrencePeriod",
        description="Date/time(s) or duration when the charged service was applied.",
    )
    occurrence_timing: Timing | None = Field(
        default=None,
        alias="occurrenceTiming",
        description="Date/time(s) or duration when the charged service was applied.",
    )
    performer: list[ChargeItemPerformer] | None = Field(
        default=None,
        description="Indicates who or what performed or participated in the charged service.",
    )
    performing_organization: Reference | None = Field(
        default=None,
        alias="performingOrganization",
        description="The organization requesting the service.",
    )
    requesting_organization: Reference | None = Field(
        default=None,
        alias="requestingOrganization",
        description="The organization performing the service.",
    )
    cost_center: Reference | None = Field(
        default=None,
        alias="costCenter",
        description="The financial cost center permits the tracking of charge attribution.",
    )
    quantity: Quantity | None = Field(
        default=None, description="Quantity of which the charge item has been serviced."
    )
    bodysite: list[CodeableConcept] | None = Field(
        default=None,
        description="The anatomical location where the related service has been applied.",
    )
    factor_override: int | float | None = Field(
        default=None,
        alias="factorOverride",
        description="Factor overriding the factor determined by the rules associated with the code.",
    )
    price_override: Money | None = Field(
        default=None,
        alias="priceOverride",
        description="Total price of the charge overriding the list price associated with the code.",
    )
    override_reason: str | None = Field(
        default=None,
        alias="overrideReason",
        description="If the list price or the rule-based factor associated with the code is overridden, this attribute can capture a text to indicate the reason for this action.",
    )
    enterer: Reference | None = Field(
        default=None,
        description="The device, practitioner, etc. who entered the charge item.",
    )
    entered_date: str | None = Field(
        default=None,
        alias="enteredDate",
        description="Date the charge item was entered.",
    )
    reason: list[CodeableConcept] | None = Field(
        default=None,
        description="Describes why the event occurred in coded or textual form.",
    )
    service: list[Reference] | None = Field(
        default=None,
        description="Indicated the rendered service that caused this charge.",
    )
    product_reference: Reference | None = Field(
        default=None,
        alias="productReference",
        description="Identifies the device, food, drug or other product being charged either by type code or reference to an instance.",
    )
    product_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="productCodeableConcept",
        description="Identifies the device, food, drug or other product being charged either by type code or reference to an instance.",
    )
    account: list[Reference] | None = Field(
        default=None, description="Account into which this ChargeItems belongs."
    )
    note: list[Annotation] | None = Field(
        default=None,
        description="Comments made about the event by the performer, subject or other participants.",
    )
    supporting_information: list[Reference] | None = Field(
        default=None,
        alias="supportingInformation",
        description="Further information supporting this charge.",
    )


class ChargeItemPerformer(MedplumFHIRBase):
    """Indicates who or what performed or participated in the charged service."""

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
    function: CodeableConcept | None = Field(
        default=None,
        description="Describes the type of performance or participation(e.g. primary surgeon, anesthesiologiest, etc.).",
    )
    actor: Reference = Field(
        default=...,
        description="The device, practitioner, etc. who performed or participated in the service.",
    )
