# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Invoice(MedplumFHIRBase):
    """Invoice containing collected ChargeItems from an Account with calculated
    individual and total price for Billing purpose.
    """

    resource_type: Literal["Invoice"] = Field(
        default="Invoice",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Identifier of this Invoice, often used for reference in correspondence about this invoice or for tracking of payments.")
    status: Literal['draft', 'issued', 'balanced', 'cancelled', 'entered-in-error'] = Field(default=..., description="The current state of the Invoice.")
    cancelled_reason: Optional[str] = Field(default=None, alias="cancelledReason", description="In case of Invoice cancellation a reason must be given (entered in error, superseded by corrected invoice etc.).")
    type: Optional[CodeableConcept] = Field(default=None, description="Type of Invoice depending on domain, realm an usage (e.g. internal/external, dental, preliminary).")
    subject: Optional[Reference] = Field(default=None, description="The individual or set of individuals receiving the goods and services billed in this invoice.")
    recipient: Optional[Reference] = Field(default=None, description="The individual or Organization responsible for balancing of this invoice.")
    date: Optional[str] = Field(default=None, description="Date/time(s) of when this Invoice was posted.")
    participant: Optional[list[InvoiceParticipant]] = Field(default=None, description="Indicates who or what performed or participated in the charged service.")
    issuer: Optional[Reference] = Field(default=None, description="The organizationissuing the Invoice.")
    account: Optional[Reference] = Field(default=None, description="Account which is supposed to be balanced with this Invoice.")
    line_item: Optional[list[InvoiceLineItem]] = Field(default=None, alias="lineItem", description="Each line item represents one charge for goods and services rendered. Details such as date, code and amount are found in the referenced ChargeItem resource.")
    total_price_component: Optional[list[InvoiceLineItemPriceComponent]] = Field(default=None, alias="totalPriceComponent", description="The total amount for the Invoice may be calculated as the sum of the line items with surcharges/deductions that apply in certain conditions. The priceComponent element can be used to offer transparency to the recipient of the Invoice of how the total price was calculated.")
    total_net: Optional[Money] = Field(default=None, alias="totalNet", description="Invoice total , taxes excluded.")
    total_gross: Optional[Money] = Field(default=None, alias="totalGross", description="Invoice total, tax included.")
    payment_terms: Optional[str] = Field(default=None, alias="paymentTerms", description="Payment details such as banking details, period of payment, deductibles, methods of payment.")
    note: Optional[list[Annotation]] = Field(default=None, description="Comments made about the invoice by the issuer, subject, or other participants.")


class InvoiceLineItem(MedplumFHIRBase):
    """Each line item represents one charge for goods and services rendered.
    Details such as date, code and amount are found in the referenced
    ChargeItem resource.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    sequence: Optional[Union[int, float]] = Field(default=None, description="Sequence in which the items appear on the invoice.")
    charge_item_reference: Optional[Reference] = Field(default=None, alias="chargeItemReference", description="The ChargeItem contains information such as the billing code, date, amount etc. If no further details are required for the lineItem, inline billing codes can be added using the CodeableConcept data type instead of the Reference.")
    charge_item_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="chargeItemCodeableConcept", description="The ChargeItem contains information such as the billing code, date, amount etc. If no further details are required for the lineItem, inline billing codes can be added using the CodeableConcept data type instead of the Reference.")
    price_component: Optional[list[InvoiceLineItemPriceComponent]] = Field(default=None, alias="priceComponent", description="The price for a ChargeItem may be calculated as a base price with surcharges/deductions that apply in certain conditions. A ChargeItemDefinition resource that defines the prices, factors and conditions that apply to a billing code is currently under development. The priceComponent element can be used to offer transparency to the recipient of the Invoice as to how the prices have been calculated.")


class InvoiceLineItemPriceComponent(MedplumFHIRBase):
    """The price for a ChargeItem may be calculated as a base price with
    surcharges/deductions that apply in certain conditions. A
    ChargeItemDefinition resource that defines the prices, factors and
    conditions that apply to a billing code is currently under development.
    The priceComponent element can be used to offer transparency to the
    recipient of the Invoice as to how the prices have been calculated.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: Literal['base', 'surcharge', 'deduction', 'discount', 'tax', 'informational'] = Field(default=..., description="This code identifies the type of the component.")
    code: Optional[CodeableConcept] = Field(default=None, description="A code that identifies the component. Codes may be used to differentiate between kinds of taxes, surcharges, discounts etc.")
    factor: Optional[Union[int, float]] = Field(default=None, description="The factor that has been applied on the base price for calculating this component.")
    amount: Optional[Money] = Field(default=None, description="The amount calculated for this component.")


class InvoiceParticipant(MedplumFHIRBase):
    """Indicates who or what performed or participated in the charged service."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    role: Optional[CodeableConcept] = Field(default=None, description="Describes the type of involvement (e.g. transcriptionist, creator etc.). If the invoice has been created automatically, the Participant may be a billing engine or another kind of device.")
    actor: Reference = Field(default=..., description="The device, practitioner, etc. who performed or participated in the service.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Invoice", Invoice)
    register_model("InvoiceLineItem", InvoiceLineItem)
    register_model("InvoiceLineItemPriceComponent", InvoiceLineItemPriceComponent)
    register_model("InvoiceParticipant", InvoiceParticipant)
