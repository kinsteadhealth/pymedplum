# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ParameterDefinition(MedplumFHIRBase):
    """The parameters to the module. This collection specifies both the input
    and output parameters. Input parameters are provided by the caller as
    part of the $evaluate operation. Output parameters are included in the
    GuidanceResponse.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    name: Optional[str] = Field(default=None, description="The name of the parameter used to allow access to the value of the parameter in evaluation contexts.")
    use: Literal['in', 'out'] = Field(default=..., description="Whether the parameter is input or output for the module.")
    min: Optional[Union[int, float]] = Field(default=None, description="The minimum number of times this parameter SHALL appear in the request or response.")
    max: Optional[str] = Field(default=None, description="The maximum number of times this element is permitted to appear in the request or response.")
    documentation: Optional[str] = Field(default=None, description="A brief discussion of what the parameter is for and how it is used by the module.")
    type: str = Field(default=..., description="The type of the parameter.")
    profile: Optional[str] = Field(default=None, description="If specified, this indicates a profile that the input data must conform to, or that the output data will conform to.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ParameterDefinition", ParameterDefinition)
