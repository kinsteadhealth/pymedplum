# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class TriggerDefinition(MedplumFHIRBase):
    """A description of a triggering event. Triggering events can be named
    events, data events, or periodic, as determined by the type element.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    type: Literal['named-event', 'periodic', 'data-changed', 'data-added', 'data-modified', 'data-removed', 'data-accessed', 'data-access-ended'] = Field(default=..., description="The type of triggering event.")
    name: Optional[str] = Field(default=None, description="A formal name for the event. This may be an absolute URI that identifies the event formally (e.g. from a trigger registry), or a simple relative URI that identifies the event in a local context.")
    timing_timing: Optional[Timing] = Field(default=None, alias="timingTiming", description="The timing of the event (if this is a periodic trigger).")
    timing_reference: Optional[Reference] = Field(default=None, alias="timingReference", description="The timing of the event (if this is a periodic trigger).")
    timing_date: Optional[str] = Field(default=None, alias="timingDate", description="The timing of the event (if this is a periodic trigger).")
    timing_date_time: Optional[str] = Field(default=None, alias="timingDateTime", description="The timing of the event (if this is a periodic trigger).")
    data: Optional[list[DataRequirement]] = Field(default=None, description="The triggering data of the event (if this is a data trigger). If more than one data is requirement is specified, then all the data requirements must be true.")
    condition: Optional[Expression] = Field(default=None, description="A boolean-valued expression that is evaluated in the context of the container of the trigger definition and returns whether or not the trigger fires.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("TriggerDefinition", TriggerDefinition)
