# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class SubstanceAmount(MedplumFHIRBase):
    """Chemical substances are a single substance type whose primary defining
    element is the molecular structure. Chemical substances shall be defined
    on the basis of their complete covalent molecular structure; the
    presence of a salt (counter-ion) and/or solvates (water, alcohols) is
    also captured. Purity, grade, physical form or particle size are not
    taken into account in the definition of a chemical substance or in the
    assignment of a Substance ID.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    amount_quantity: Optional[Quantity] = Field(default=None, alias="amountQuantity", description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.")
    amount_range: Optional[Range] = Field(default=None, alias="amountRange", description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.")
    amount_string: Optional[str] = Field(default=None, alias="amountString", description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.")
    amount_type: Optional[CodeableConcept] = Field(default=None, alias="amountType", description="Most elements that require a quantitative value will also have a field called amount type. Amount type should always be specified because the actual value of the amount is often dependent on it. EXAMPLE: In capturing the actual relative amounts of substances or molecular fragments it is essential to indicate whether the amount refers to a mole ratio or weight ratio. For any given element an effort should be made to use same the amount type for all related definitional elements.")
    amount_text: Optional[str] = Field(default=None, alias="amountText", description="A textual comment on a numeric value.")
    reference_range: Optional[SubstanceAmountReferenceRange] = Field(default=None, alias="referenceRange", description="Reference range of possible or expected values.")


class SubstanceAmountReferenceRange(MedplumFHIRBase):
    """Reference range of possible or expected values."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    low_limit: Optional[Quantity] = Field(default=None, alias="lowLimit", description="Lower limit possible or expected.")
    high_limit: Optional[Quantity] = Field(default=None, alias="highLimit", description="Upper limit possible or expected.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SubstanceAmount", SubstanceAmount)
    register_model("SubstanceAmountReferenceRange", SubstanceAmountReferenceRange)
