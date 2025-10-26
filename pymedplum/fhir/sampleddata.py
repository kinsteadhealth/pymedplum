# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class SampledData(MedplumFHIRBase):
    """A series of measurements taken by a device, with upper and lower limits.
    There may be more than one dimension in the data.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    origin: Quantity = Field(default=..., description="The base quantity that a measured value of zero represents. In addition, this provides the units of the entire measurement series.")
    period: Union[int, float] = Field(default=..., description="The length of time between sampling times, measured in milliseconds.")
    factor: Optional[Union[int, float]] = Field(default=None, description="A correction factor that is applied to the sampled data points before they are added to the origin.")
    lower_limit: Optional[Union[int, float]] = Field(default=None, alias="lowerLimit", description="The lower limit of detection of the measured points. This is needed if any of the data points have the value &quot;L&quot; (lower than detection limit).")
    upper_limit: Optional[Union[int, float]] = Field(default=None, alias="upperLimit", description="The upper limit of detection of the measured points. This is needed if any of the data points have the value &quot;U&quot; (higher than detection limit).")
    dimensions: Union[int, float] = Field(default=..., description="The number of sample points at each time point. If this value is greater than one, then the dimensions will be interlaced - all the sample points for a point in time will be recorded at once.")
    data: Optional[str] = Field(default=None, description="A series of data points which are decimal values separated by a single space (character u20). The special values &quot;E&quot; (error), &quot;L&quot; (below detection limit) and &quot;U&quot; (above detection limit) can also be used in place of a decimal value.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SampledData", SampledData)
