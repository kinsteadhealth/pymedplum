# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class HealthcareService(MedplumFHIRBase):
    """The details of a healthcare service available at a location."""

    resource_type: Literal["HealthcareService"] = Field(
        default="HealthcareService", alias="resourceType"
    )

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
        default=None, description="External identifiers for this item."
    )
    active: bool | None = Field(
        default=None,
        description="This flag is used to mark the record to not be used. This is not used when a center is closed for maintenance, or for holidays, the notAvailable period is to be used for this.",
    )
    provided_by: Reference | None = Field(
        default=None,
        alias="providedBy",
        description="The organization that provides this healthcare service.",
    )
    category: list[CodeableConcept] | None = Field(
        default=None,
        description="Identifies the broad category of service being performed or delivered.",
    )
    type: list[CodeableConcept] | None = Field(
        default=None,
        description="The specific type of service that may be delivered or performed.",
    )
    specialty: list[CodeableConcept] | None = Field(
        default=None,
        description="Collection of specialties handled by the service site. This is more of a medical term.",
    )
    location: list[Reference] | None = Field(
        default=None,
        description="The location(s) where this healthcare service may be provided.",
    )
    name: str | None = Field(
        default=None,
        description="Further description of the service as it would be presented to a consumer while searching.",
    )
    comment: str | None = Field(
        default=None,
        description="Any additional description of the service and/or any specific issues not covered by the other attributes, which can be displayed as further detail under the serviceName.",
    )
    extra_details: str | None = Field(
        default=None,
        alias="extraDetails",
        description="Extra details about the service that can't be placed in the other fields.",
    )
    photo: Attachment | None = Field(
        default=None,
        description="If there is a photo/symbol associated with this HealthcareService, it may be included here to facilitate quick identification of the service in a list.",
    )
    telecom: list[ContactPoint] | None = Field(
        default=None,
        description="List of contacts related to this specific healthcare service.",
    )
    coverage_area: list[Reference] | None = Field(
        default=None,
        alias="coverageArea",
        description="The location(s) that this service is available to (not where the service is provided).",
    )
    service_provision_code: list[CodeableConcept] | None = Field(
        default=None,
        alias="serviceProvisionCode",
        description="The code(s) that detail the conditions under which the healthcare service is available/offered.",
    )
    eligibility: list[HealthcareServiceEligibility] | None = Field(
        default=None,
        description="Does this service have specific eligibility requirements that need to be met in order to use the service?",
    )
    program: list[CodeableConcept] | None = Field(
        default=None, description="Programs that this service is applicable to."
    )
    characteristic: list[CodeableConcept] | None = Field(
        default=None, description="Collection of characteristics (attributes)."
    )
    communication: list[CodeableConcept] | None = Field(
        default=None,
        description="Some services are specifically made available in multiple languages, this property permits a directory to declare the languages this is offered in. Typically this is only provided where a service operates in communities with mixed languages used.",
    )
    referral_method: list[CodeableConcept] | None = Field(
        default=None,
        alias="referralMethod",
        description="Ways that the service accepts referrals, if this is not provided then it is implied that no referral is required.",
    )
    appointment_required: bool | None = Field(
        default=None,
        alias="appointmentRequired",
        description="Indicates whether or not a prospective consumer will require an appointment for a particular service at a site to be provided by the Organization. Indicates if an appointment is required for access to this service.",
    )
    available_time: list[HealthcareServiceAvailableTime] | None = Field(
        default=None,
        alias="availableTime",
        description="A collection of times that the Service Site is available.",
    )
    not_available: list[HealthcareServiceNotAvailable] | None = Field(
        default=None,
        alias="notAvailable",
        description="The HealthcareService is not available during this period of time due to the provided reason.",
    )
    availability_exceptions: str | None = Field(
        default=None,
        alias="availabilityExceptions",
        description="A description of site availability exceptions, e.g. public holiday availability. Succinctly describing all possible exceptions to normal site availability as details in the available Times and not available Times.",
    )
    endpoint: list[Reference] | None = Field(
        default=None,
        description="Technical endpoints providing access to services operated for the specific healthcare services defined at this resource.",
    )


class HealthcareServiceAvailableTime(MedplumFHIRBase):
    """A collection of times that the Service Site is available."""

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
        default=None,
        alias="allDay",
        description="Is this always available? (hence times are irrelevant) e.g. 24 hour service.",
    )
    available_start_time: str | None = Field(
        default=None,
        alias="availableStartTime",
        description="The opening time of day. Note: If the AllDay flag is set, then this time is ignored.",
    )
    available_end_time: str | None = Field(
        default=None,
        alias="availableEndTime",
        description="The closing time of day. Note: If the AllDay flag is set, then this time is ignored.",
    )


class HealthcareServiceEligibility(MedplumFHIRBase):
    """Does this service have specific eligibility requirements that need to be
    met in order to use the service?
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
    code: CodeableConcept | None = Field(
        default=None, description="Coded value for the eligibility."
    )
    comment: str | None = Field(
        default=None,
        description="Describes the eligibility conditions for the service.",
    )


class HealthcareServiceNotAvailable(MedplumFHIRBase):
    """The HealthcareService is not available during this period of time due to
    the provided reason.
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
    description: str = Field(
        default=...,
        description="The reason that can be presented to the user as to why this time is not available.",
    )
    during: Period | None = Field(
        default=None,
        description="Service is not available (seasonally or for a public holiday) from this date.",
    )
