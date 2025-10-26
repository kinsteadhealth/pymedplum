# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class UsageContext(MedplumFHIRBase):
    """Specifies clinical/business/etc. metadata that can be used to retrieve,
    index and/or categorize an artifact. This metadata can either be
    specific to the applicable population (e.g., age category, DRG) or the
    specific context of care (e.g., venue, care setting, provider of care).
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    code: Coding = Field(default=..., description="A code that identifies the type of context being specified by this usage context.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.")
    value_reference: Optional[Reference] = Field(default=None, alias="valueReference", description="A value that defines the context specified in this context of use. The interpretation of the value is defined by the code.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("UsageContext", UsageContext)
