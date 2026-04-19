# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class Slot(MedplumFHIRBase):
    """A slot of time on a schedule that may be available for booking appointments."""

    resource_type: Literal["Slot"] = Field(default="Slot", alias="resourceType")

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
        default=None, description="External Ids for this item."
    )
    service_category: list[CodeableConcept] | None = Field(
        default=None,
        alias="serviceCategory",
        description="A broad categorization of the service that is to be performed during this appointment.",
    )
    service_type: list[CodeableConcept] | None = Field(
        default=None,
        alias="serviceType",
        description="The type of appointments that can be booked into this slot (ideally this would be an identifiable service - which is at a location, rather than the location itself). If provided then this overrides the value provided on the availability resource.",
    )
    specialty: list[CodeableConcept] | None = Field(
        default=None,
        description="The specialty of a practitioner that would be required to perform the service requested in this appointment.",
    )
    appointment_type: CodeableConcept | None = Field(
        default=None,
        alias="appointmentType",
        description="The style of appointment or patient that may be booked in the slot (not service type).",
    )
    schedule: Reference = Field(
        default=...,
        description="The schedule resource that this slot defines an interval of status information.",
    )
    status: Literal[
        "busy", "free", "busy-unavailable", "busy-tentative", "entered-in-error"
    ] = Field(
        default=...,
        description="busy | free | busy-unavailable | busy-tentative | entered-in-error.",
    )
    start: str = Field(default=..., description="Date/Time that the slot is to begin.")
    end: str = Field(default=..., description="Date/Time that the slot is to conclude.")
    overbooked: bool | None = Field(
        default=None,
        description="This slot has already been overbooked, appointments are unlikely to be accepted for this time.",
    )
    comment: str | None = Field(
        default=None,
        description="Comments on the slot to describe any extended information. Such as custom constraints on the slot.",
    )
