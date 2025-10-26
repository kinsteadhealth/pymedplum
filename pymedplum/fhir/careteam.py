# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class CareTeam(MedplumFHIRBase):
    """The Care Team includes all the people and organizations who plan to
    participate in the coordination and delivery of care for a patient.
    """

    resource_type: Literal["CareTeam"] = Field(default="CareTeam", alias="resourceType")

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
    contained: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="Business identifiers assigned to this care team by the performer or other systems which remain constant as the resource is updated and propagates from server to server.",
    )
    status: Optional[
        Literal["proposed", "active", "suspended", "inactive", "entered-in-error"]
    ] = Field(default=None, description="Indicates the current state of the care team.")
    category: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Identifies what kind of team. This is to support differentiation between multiple co-existing teams, such as care plan team, episode of care team, longitudinal care team.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A label for human use intended to distinguish like teams. E.g. the &quot;red&quot; vs. &quot;green&quot; trauma teams.",
    )
    subject: Optional[Reference] = Field(
        default=None,
        description="Identifies the patient or group whose intended care is handled by the team.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The Encounter during which this CareTeam was created or to which the creation of this record is tightly associated.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="Indicates when the team did (or is intended to) come into effect and end.",
    )
    participant: Optional[list[CareTeamParticipant]] = Field(
        default=None,
        description="Identifies all people and organizations who are expected to be involved in the care team.",
    )
    reason_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="reasonCode",
        description="Describes why the care team exists.",
    )
    reason_reference: Optional[list[Reference]] = Field(
        default=None,
        alias="reasonReference",
        description="Condition(s) that this care team addresses.",
    )
    managing_organization: Optional[list[Reference]] = Field(
        default=None,
        alias="managingOrganization",
        description="The organization responsible for the care team.",
    )
    telecom: Optional[list[ContactPoint]] = Field(
        default=None,
        description="A central contact detail for the care team (that applies to all members).",
    )
    note: Optional[list[Annotation]] = Field(
        default=None, description="Comments made about the CareTeam."
    )


class CareTeamParticipant(MedplumFHIRBase):
    """Identifies all people and organizations who are expected to be involved
    in the care team.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    role: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="Indicates specific responsibility of an individual within the care team, such as &quot;Primary care physician&quot;, &quot;Trained social worker counselor&quot;, &quot;Caregiver&quot;, etc.",
    )
    member: Optional[Reference] = Field(
        default=None,
        description="The specific person or organization who is participating/expected to participate in the care team.",
    )
    on_behalf_of: Optional[Reference] = Field(
        default=None,
        alias="onBehalfOf",
        description="The organization of the practitioner.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="Indicates when the specific member or organization did (or is intended to) come into effect and end.",
    )
