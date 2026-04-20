# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.range import Range


class Timing(MedplumFHIRBase):
    """Specifies an event that may occur multiple times. Timing schedules are
    used to record when things are planned, expected or requested to occur.
    The most common usage is in dosage instructions for medications. They
    are also used when planning care of various kinds, and may be used for
    reporting the schedule to which past regular activities were carried
    out.
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
    event: list[str] | None = Field(
        default=None, description="Identifies specific times when the event occurs."
    )
    repeat: TimingRepeat | None = Field(
        default=None,
        description="A set of rules that describe when the event is scheduled.",
    )
    code: CodeableConcept | None = Field(
        default=None,
        description="A code for the timing schedule (or just text in code.text). Some codes such as BID are ubiquitous, but many institutions define their own additional codes. If a code is provided, the code is understood to be a complete statement of whatever is specified in the structured timing data, and either the code or the data may be used to interpret the Timing, with the exception that .repeat.bounds still applies over the code (and is not contained in the code).",
    )


class TimingRepeat(MedplumFHIRBase):
    """A set of rules that describe when the event is scheduled."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    bounds_duration: Duration | None = Field(
        default=None,
        alias="boundsDuration",
        description="Either a duration for the length of the timing schedule, a range of possible length, or outer bounds for start and/or end limits of the timing schedule.",
    )
    bounds_range: Range | None = Field(
        default=None,
        alias="boundsRange",
        description="Either a duration for the length of the timing schedule, a range of possible length, or outer bounds for start and/or end limits of the timing schedule.",
    )
    bounds_period: Period | None = Field(
        default=None,
        alias="boundsPeriod",
        description="Either a duration for the length of the timing schedule, a range of possible length, or outer bounds for start and/or end limits of the timing schedule.",
    )
    count: int | float | None = Field(
        default=None,
        description="A total count of the desired number of repetitions across the duration of the entire timing specification. If countMax is present, this element indicates the lower bound of the allowed range of count values.",
    )
    count_max: int | float | None = Field(
        default=None,
        alias="countMax",
        description="If present, indicates that the count is a range - so to perform the action between [count] and [countMax] times.",
    )
    duration: int | float | None = Field(
        default=None,
        description="How long this thing happens for when it happens. If durationMax is present, this element indicates the lower bound of the allowed range of the duration.",
    )
    duration_max: int | float | None = Field(
        default=None,
        alias="durationMax",
        description="If present, indicates that the duration is a range - so to perform the action between [duration] and [durationMax] time length.",
    )
    duration_unit: Literal["s", "min", "h", "d", "wk", "mo", "a"] | None = Field(
        default=None,
        alias="durationUnit",
        description="The units of time for the duration, in UCUM units.",
    )
    frequency: int | float | None = Field(
        default=None,
        description="The number of times to repeat the action within the specified period. If frequencyMax is present, this element indicates the lower bound of the allowed range of the frequency.",
    )
    frequency_max: int | float | None = Field(
        default=None,
        alias="frequencyMax",
        description="If present, indicates that the frequency is a range - so to repeat between [frequency] and [frequencyMax] times within the period or period range.",
    )
    period: int | float | None = Field(
        default=None,
        description="Indicates the duration of time over which repetitions are to occur; e.g. to express &quot;3 times per day&quot;, 3 would be the frequency and &quot;1 day&quot; would be the period. If periodMax is present, this element indicates the lower bound of the allowed range of the period length.",
    )
    period_max: int | float | None = Field(
        default=None,
        alias="periodMax",
        description="If present, indicates that the period is a range from [period] to [periodMax], allowing expressing concepts such as &quot;do this once every 3-5 days.",
    )
    period_unit: Literal["s", "min", "h", "d", "wk", "mo", "a"] | None = Field(
        default=None,
        alias="periodUnit",
        description="The units of time for the period in UCUM units.",
    )
    day_of_week: (
        list[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]] | None
    ) = Field(
        default=None,
        alias="dayOfWeek",
        description="If one or more days of week is provided, then the action happens only on the specified day(s).",
    )
    time_of_day: list[str] | None = Field(
        default=None,
        alias="timeOfDay",
        description="Specified time of day for action to take place.",
    )
    when: (
        list[
            Literal[
                "MORN",
                "MORN.early",
                "MORN.late",
                "NOON",
                "AFT",
                "AFT.early",
                "AFT.late",
                "EVE",
                "EVE.early",
                "EVE.late",
                "NIGHT",
                "PHS",
                "HS",
                "WAKE",
                "C",
                "CM",
                "CD",
                "CV",
                "AC",
                "ACM",
                "ACD",
                "ACV",
                "PC",
                "PCM",
                "PCD",
                "PCV",
            ]
        ]
        | None
    ) = Field(
        default=None,
        description="An approximate time period during the day, potentially linked to an event of daily living that indicates when the action should occur.",
    )
    offset: int | float | None = Field(
        default=None,
        description="The number of minutes from the event. If the event code does not indicate whether the minutes is before or after the event, then the offset is assumed to be after the event.",
    )
