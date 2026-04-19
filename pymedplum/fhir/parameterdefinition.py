# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension


class ParameterDefinition(MedplumFHIRBase):
    """The parameters to the module. This collection specifies both the input
    and output parameters. Input parameters are provided by the caller as
    part of the $evaluate operation. Output parameters are included in the
    GuidanceResponse.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    name: str | None = Field(
        default=None,
        description="The name of the parameter used to allow access to the value of the parameter in evaluation contexts.",
    )
    use: Literal["in", "out"] = Field(
        default=...,
        description="Whether the parameter is input or output for the module.",
    )
    min: int | float | None = Field(
        default=None,
        description="The minimum number of times this parameter SHALL appear in the request or response.",
    )
    max: str | None = Field(
        default=None,
        description="The maximum number of times this element is permitted to appear in the request or response.",
    )
    documentation: str | None = Field(
        default=None,
        description="A brief discussion of what the parameter is for and how it is used by the module.",
    )
    type: str = Field(default=..., description="The type of the parameter.")
    profile: str | None = Field(
        default=None,
        description="If specified, this indicates a profile that the input data must conform to, or that the output data will conform to.",
    )
