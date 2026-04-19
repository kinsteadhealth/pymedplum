# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range


class SubstanceAmount(MedplumFHIRBase):
    """Chemical substances are a single substance type whose primary defining
    element is the molecular structure. Chemical substances shall be defined
    on the basis of their complete covalent molecular structure; the
    presence of a salt (counter-ion) and/or solvates (water, alcohols) is
    also captured. Purity, grade, physical form or particle size are not
    taken into account in the definition of a chemical substance or in the
    assignment of a Substance ID.
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
    amount_quantity: Quantity | None = Field(
        default=None,
        alias="amountQuantity",
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.",
    )
    amount_range: Range | None = Field(
        default=None,
        alias="amountRange",
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.",
    )
    amount_string: str | None = Field(
        default=None,
        alias="amountString",
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field.",
    )
    amount_type: CodeableConcept | None = Field(
        default=None,
        alias="amountType",
        description="Most elements that require a quantitative value will also have a field called amount type. Amount type should always be specified because the actual value of the amount is often dependent on it. EXAMPLE: In capturing the actual relative amounts of substances or molecular fragments it is essential to indicate whether the amount refers to a mole ratio or weight ratio. For any given element an effort should be made to use same the amount type for all related definitional elements.",
    )
    amount_text: str | None = Field(
        default=None,
        alias="amountText",
        description="A textual comment on a numeric value.",
    )
    reference_range: SubstanceAmountReferenceRange | None = Field(
        default=None,
        alias="referenceRange",
        description="Reference range of possible or expected values.",
    )


class SubstanceAmountReferenceRange(MedplumFHIRBase):
    """Reference range of possible or expected values."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    low_limit: Quantity | None = Field(
        default=None, alias="lowLimit", description="Lower limit possible or expected."
    )
    high_limit: Quantity | None = Field(
        default=None, alias="highLimit", description="Upper limit possible or expected."
    )
