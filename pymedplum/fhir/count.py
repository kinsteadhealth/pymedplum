# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Count(MedplumFHIRBase):
    """A measured amount (or an amount that can potentially be measured). Note
    that measured amounts include amounts that are not precisely quantified,
    including amounts involving arbitrary units and floating currencies.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    value: Optional[Union[int, float]] = Field(default=None, description="The value of the measured amount. The value includes an implicit precision in the presentation of the value.")
    comparator: Optional[Literal['<', '<=', '>=', '>']] = Field(default=None, description="How the value should be understood and represented - whether the actual value is greater or less than the stated value due to measurement issues; e.g. if the comparator is &quot;&lt;&quot; , then the real value is &lt; stated value.")
    unit: Optional[str] = Field(default=None, description="A human-readable form of the unit.")
    system: Optional[str] = Field(default=None, description="The identification of the system that provides the coded form of the unit.")
    code: Optional[str] = Field(default=None, description="A computer processable form of the unit in some unit representation system.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Count", Count)
