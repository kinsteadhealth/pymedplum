# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class Location(MedplumFHIRBase):
    """Details and position information for a physical place where services are
    provided and resources and participants may be stored, found, contained,
    or accommodated.
    """

    resource_type: Literal["Location"] = Field(default="Location", alias="resourceType")

    id: str | None = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Meta | None = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: str | None = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: str | None = Field(
        default=None, description="The base language in which the resource is written."
    )
    text: Narrative | None = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: list[dict[str, Any]] | None = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Unique code or number identifying the location to its users.",
    )
    status: Literal["active", "suspended", "inactive"] | None = Field(
        default=None,
        description="The status property covers the general availability of the resource, not the current value which may be covered by the operationStatus, or by a schedule/slots if they are configured for the location.",
    )
    operational_status: Coding | None = Field(
        default=None,
        alias="operationalStatus",
        description="The operational status covers operation values most relevant to beds (but can also apply to rooms/units/chairs/etc. such as an isolation unit/dialysis chair). This typically covers concepts such as contamination, housekeeping, and other activities like maintenance.",
    )
    name: str | None = Field(
        default=None,
        description="Name of the location as used by humans. Does not need to be unique.",
    )
    alias: list[str] | None = Field(
        default=None,
        description="A list of alternate names that the location is known as, or was known as, in the past.",
    )
    description: str | None = Field(
        default=None,
        description="Description of the Location, which helps in finding or referencing the place.",
    )
    mode: Literal["instance", "kind"] | None = Field(
        default=None,
        description="Indicates whether a resource instance represents a specific location or a class of locations.",
    )
    type: list[CodeableConcept] | None = Field(
        default=None,
        description="Indicates the type of function performed at the location.",
    )
    telecom: list[ContactPoint] | None = Field(
        default=None,
        description="The contact details of communication devices available at the location. This can include phone numbers, fax numbers, mobile numbers, email addresses and web sites.",
    )
    address: Address | None = Field(default=None, description="Physical location.")
    physical_type: CodeableConcept | None = Field(
        default=None,
        alias="physicalType",
        description="Physical form of the location, e.g. building, room, vehicle, road.",
    )
    position: LocationPosition | None = Field(
        default=None,
        description="The absolute geographic location of the Location, expressed using the WGS84 datum (This is the same co-ordinate system used in KML).",
    )
    managing_organization: Reference | None = Field(
        default=None,
        alias="managingOrganization",
        description="The organization responsible for the provisioning and upkeep of the location.",
    )
    part_of: Reference | None = Field(
        default=None,
        alias="partOf",
        description="Another Location of which this Location is physically a part of.",
    )
    hours_of_operation: list[LocationHoursOfOperation] | None = Field(
        default=None,
        alias="hoursOfOperation",
        description="What days/times during a week is this location usually open.",
    )
    availability_exceptions: str | None = Field(
        default=None,
        alias="availabilityExceptions",
        description="A description of when the locations opening ours are different to normal, e.g. public holiday availability. Succinctly describing all possible exceptions to normal site availability as detailed in the opening hours Times.",
    )
    endpoint: list[Reference] | None = Field(
        default=None,
        description="Technical endpoints providing access to services operated for the location.",
    )


class LocationHoursOfOperation(MedplumFHIRBase):
    """What days/times during a week is this location usually open."""

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
    days_of_week: (
        list[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]] | None
    ) = Field(
        default=None,
        alias="daysOfWeek",
        description="Indicates which days of the week are available between the start and end Times.",
    )
    all_day: bool | None = Field(
        default=None, alias="allDay", description="The Location is open all day."
    )
    opening_time: str | None = Field(
        default=None, alias="openingTime", description="Time that the Location opens."
    )
    closing_time: str | None = Field(
        default=None, alias="closingTime", description="Time that the Location closes."
    )


class LocationPosition(MedplumFHIRBase):
    """The absolute geographic location of the Location, expressed using the
    WGS84 datum (This is the same co-ordinate system used in KML).
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
    longitude: int | float = Field(
        default=...,
        description="Longitude. The value domain and the interpretation are the same as for the text of the longitude element in KML (see notes below).",
    )
    latitude: int | float = Field(
        default=...,
        description="Latitude. The value domain and the interpretation are the same as for the text of the latitude element in KML (see notes below).",
    )
    altitude: int | float | None = Field(
        default=None,
        description="Altitude. The value domain and the interpretation are the same as for the text of the altitude element in KML (see notes below).",
    )
