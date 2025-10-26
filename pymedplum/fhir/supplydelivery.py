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
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.timing import Timing


class SupplyDelivery(MedplumFHIRBase):
    """Record of delivery of what is supplied."""

    resource_type: Literal["SupplyDelivery"] = Field(
        default="SupplyDelivery", alias="resourceType"
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
        description="Identifier for the supply delivery event that is used to identify it across multiple disparate systems.",
    )
    based_on: list[Reference] | None = Field(
        default=None,
        alias="basedOn",
        description="A plan, proposal or order that is fulfilled in whole or in part by this event.",
    )
    part_of: list[Reference] | None = Field(
        default=None,
        alias="partOf",
        description="A larger event of which this particular event is a component or step.",
    )
    status: (
        Literal["in-progress", "completed", "abandoned", "entered-in-error"] | None
    ) = Field(
        default=None, description="A code specifying the state of the dispense event."
    )
    patient: Reference | None = Field(
        default=None,
        description="A link to a resource representing the person whom the delivered item is for.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="Indicates the type of dispensing event that is performed. Examples include: Trial Fill, Completion of Trial, Partial Fill, Emergency Fill, Samples, etc.",
    )
    supplied_item: SupplyDeliverySuppliedItem | None = Field(
        default=None,
        alias="suppliedItem",
        description="The item that is being delivered or has been supplied.",
    )
    occurrence_date_time: str | None = Field(
        default=None,
        alias="occurrenceDateTime",
        description="The date or time(s) the activity occurred.",
    )
    occurrence_period: Period | None = Field(
        default=None,
        alias="occurrencePeriod",
        description="The date or time(s) the activity occurred.",
    )
    occurrence_timing: Timing | None = Field(
        default=None,
        alias="occurrenceTiming",
        description="The date or time(s) the activity occurred.",
    )
    supplier: Reference | None = Field(
        default=None,
        description="The individual responsible for dispensing the medication, supplier or device.",
    )
    destination: Reference | None = Field(
        default=None,
        description="Identification of the facility/location where the Supply was shipped to, as part of the dispense event.",
    )
    receiver: list[Reference] | None = Field(
        default=None, description="Identifies the person who picked up the Supply."
    )


class SupplyDeliverySuppliedItem(MedplumFHIRBase):
    """The item that is being delivered or has been supplied."""

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
    quantity: Quantity | None = Field(
        default=None,
        description="The amount of supply that has been dispensed. Includes unit of measure.",
    )
    item_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="itemCodeableConcept",
        description="Identifies the medication, substance or device being dispensed. This is either a link to a resource representing the details of the item or a code that identifies the item from a known list.",
    )
    item_reference: Reference | None = Field(
        default=None,
        alias="itemReference",
        description="Identifies the medication, substance or device being dispensed. This is either a link to a resource representing the details of the item or a code that identifies the item from a known list.",
    )
