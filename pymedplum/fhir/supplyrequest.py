# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class SupplyRequest(MedplumFHIRBase):
    """A record of a request for a medication, substance or device used in the
    healthcare setting.
    """

    resource_type: Literal["SupplyRequest"] = Field(
        default="SupplyRequest",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[list[dict[str, Any]]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[list[Identifier]] = Field(default=None, description="Business identifiers assigned to this SupplyRequest by the author and/or other systems. These identifiers remain constant as the resource is updated and propagates from server to server.")
    status: Optional[Literal['draft', 'active', 'suspended', 'cancelled', 'completed', 'entered-in-error', 'unknown']] = Field(default=None, description="Status of the supply request.")
    category: Optional[CodeableConcept] = Field(default=None, description="Category of supply, e.g. central, non-stock, etc. This is used to support work flows associated with the supply process.")
    priority: Optional[Literal['routine', 'urgent', 'asap', 'stat']] = Field(default=None, description="Indicates how quickly this SupplyRequest should be addressed with respect to other requests.")
    item_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="itemCodeableConcept", description="The item that is requested to be supplied. This is either a link to a resource representing the details of the item or a code that identifies the item from a known list.")
    item_reference: Optional[Reference] = Field(default=None, alias="itemReference", description="The item that is requested to be supplied. This is either a link to a resource representing the details of the item or a code that identifies the item from a known list.")
    quantity: Quantity = Field(default=..., description="The amount that is being ordered of the indicated item.")
    parameter: Optional[list[SupplyRequestParameter]] = Field(default=None, description="Specific parameters for the ordered item. For example, the size of the indicated item.")
    occurrence_date_time: Optional[str] = Field(default=None, alias="occurrenceDateTime", description="When the request should be fulfilled.")
    occurrence_period: Optional[Period] = Field(default=None, alias="occurrencePeriod", description="When the request should be fulfilled.")
    occurrence_timing: Optional[Timing] = Field(default=None, alias="occurrenceTiming", description="When the request should be fulfilled.")
    authored_on: Optional[str] = Field(default=None, alias="authoredOn", description="When the request was made.")
    requester: Optional[Reference] = Field(default=None, description="The device, practitioner, etc. who initiated the request.")
    supplier: Optional[list[Reference]] = Field(default=None, description="Who is intended to fulfill the request.")
    reason_code: Optional[list[CodeableConcept]] = Field(default=None, alias="reasonCode", description="The reason why the supply item was requested.")
    reason_reference: Optional[list[Reference]] = Field(default=None, alias="reasonReference", description="The reason why the supply item was requested.")
    deliver_from: Optional[Reference] = Field(default=None, alias="deliverFrom", description="Where the supply is expected to come from.")
    deliver_to: Optional[Reference] = Field(default=None, alias="deliverTo", description="Where the supply is destined to go.")


class SupplyRequestParameter(MedplumFHIRBase):
    """Specific parameters for the ordered item. For example, the size of the
    indicated item.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[CodeableConcept] = Field(default=None, description="A code or string that identifies the device detail being asserted.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="The value of the device detail.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="The value of the device detail.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="The value of the device detail.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="The value of the device detail.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SupplyRequest", SupplyRequest)
    register_model("SupplyRequestParameter", SupplyRequestParameter)
