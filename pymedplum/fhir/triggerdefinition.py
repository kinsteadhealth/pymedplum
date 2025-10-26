# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.datarequirement import DataRequirement
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.timing import Timing


class TriggerDefinition(MedplumFHIRBase):
    """A description of a triggering event. Triggering events can be named
    events, data events, or periodic, as determined by the type element.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    type: Literal[
        "named-event",
        "periodic",
        "data-changed",
        "data-added",
        "data-modified",
        "data-removed",
        "data-accessed",
        "data-access-ended",
    ] = Field(default=..., description="The type of triggering event.")
    name: str | None = Field(
        default=None,
        description="A formal name for the event. This may be an absolute URI that identifies the event formally (e.g. from a trigger registry), or a simple relative URI that identifies the event in a local context.",
    )
    timing_timing: Timing | None = Field(
        default=None,
        alias="timingTiming",
        description="The timing of the event (if this is a periodic trigger).",
    )
    timing_reference: Reference | None = Field(
        default=None,
        alias="timingReference",
        description="The timing of the event (if this is a periodic trigger).",
    )
    timing_date: str | None = Field(
        default=None,
        alias="timingDate",
        description="The timing of the event (if this is a periodic trigger).",
    )
    timing_date_time: str | None = Field(
        default=None,
        alias="timingDateTime",
        description="The timing of the event (if this is a periodic trigger).",
    )
    data: list[DataRequirement] | None = Field(
        default=None,
        description="The triggering data of the event (if this is a data trigger). If more than one data is requirement is specified, then all the data requirements must be true.",
    )
    condition: Expression | None = Field(
        default=None,
        description="A boolean-valued expression that is evaluated in the context of the container of the trigger definition and returns whether or not the trigger fires.",
    )
