# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class PractitionerRole(MedplumFHIRBase):
    """A specific set of Roles/Locations/specialties/services that a
    practitioner may perform at an organization for a period of time.
    """

    resource_type: Literal["PractitionerRole"] = Field(
        default="PractitionerRole", alias="resourceType"
    )

    id: Optional[str] = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Optional[Meta] = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: Optional[str] = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: Optional[str] = Field(
        default=None, description="The base language in which the resource is written."
    )
    text: Optional[Narrative] = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: Optional[List[Resource]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="Business Identifiers that are specific to a role/location.",
    )
    active: Optional[bool] = Field(
        default=None,
        description="Whether this practitioner role record is in active use.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="The period during which the person is authorized to act as a practitioner in these role(s) for the organization.",
    )
    practitioner: Optional[Reference] = Field(
        default=None,
        description="Practitioner that is able to provide the defined services for the organization.",
    )
    organization: Optional[Reference] = Field(
        default=None,
        description="The organization where the Practitioner performs the roles associated.",
    )
    code: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="Roles which this practitioner is authorized to perform for the organization.",
    )
    specialty: Optional[List[CodeableConcept]] = Field(
        default=None, description="Specific specialty of the practitioner."
    )
    location: Optional[List[Reference]] = Field(
        default=None,
        description="The location(s) at which this practitioner provides care.",
    )
    healthcare_service: Optional[List[Reference]] = Field(
        default=None,
        alias="healthcareService",
        description="The list of healthcare services that this worker provides for this role's Organization/Location(s).",
    )
    telecom: Optional[List[ContactPoint]] = Field(
        default=None,
        description="Contact details that are specific to the role/location/service.",
    )
    available_time: Optional[List[PractitionerRoleAvailableTime]] = Field(
        default=None,
        alias="availableTime",
        description="A collection of times the practitioner is available or performing this role at the location and/or healthcareservice.",
    )
    not_available: Optional[List[PractitionerRoleNotAvailable]] = Field(
        default=None,
        alias="notAvailable",
        description="The practitioner is not available or performing this role during this period of time due to the provided reason.",
    )
    availability_exceptions: Optional[str] = Field(
        default=None,
        alias="availabilityExceptions",
        description="A description of site availability exceptions, e.g. public holiday availability. Succinctly describing all possible exceptions to normal site availability as details in the available Times and not available Times.",
    )
    endpoint: Optional[List[Reference]] = Field(
        default=None,
        description="Technical endpoints providing access to services operated for the practitioner with this role.",
    )


class PractitionerRoleAvailableTime(MedplumFHIRBase):
    """A collection of times the practitioner is available or performing this
    role at the location and/or healthcareservice.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    days_of_week: Optional[
        List[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]
    ] = Field(
        default=None,
        alias="daysOfWeek",
        description="Indicates which days of the week are available between the start and end Times.",
    )
    all_day: Optional[bool] = Field(
        default=None,
        alias="allDay",
        description="Is this always available? (hence times are irrelevant) e.g. 24 hour service.",
    )
    available_start_time: Optional[str] = Field(
        default=None,
        alias="availableStartTime",
        description="The opening time of day. Note: If the AllDay flag is set, then this time is ignored.",
    )
    available_end_time: Optional[str] = Field(
        default=None,
        alias="availableEndTime",
        description="The closing time of day. Note: If the AllDay flag is set, then this time is ignored.",
    )


class PractitionerRoleNotAvailable(MedplumFHIRBase):
    """The practitioner is not available or performing this role during this
    period of time due to the provided reason.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    description: str = Field(
        default=...,
        description="The reason that can be presented to the user as to why this time is not available.",
    )
    during: Optional[Period] = Field(
        default=None,
        description="Service is not available (seasonally or for a public holiday) from this date.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("PractitionerRole", PractitionerRole)
    register_model("PractitionerRoleAvailableTime", PractitionerRoleAvailableTime)
    register_model("PractitionerRoleNotAvailable", PractitionerRoleNotAvailable)
