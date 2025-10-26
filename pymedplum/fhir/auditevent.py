# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class AuditEvent(MedplumFHIRBase):
    """A record of an event made for purposes of maintaining a security log.
    Typical uses include detection of intrusion attempts and monitoring for
    inappropriate usage.
    """

    resource_type: Literal["AuditEvent"] = Field(
        default="AuditEvent", alias="resourceType"
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
    type: Coding = Field(
        default=...,
        description="Identifier for a family of the event. For example, a menu item, program, rule, policy, function code, application name or URL. It identifies the performed function.",
    )
    subtype: list[Coding] | None = Field(
        default=None, description="Identifier for the category of event."
    )
    action: Literal["C", "R", "U", "D", "E"] | None = Field(
        default=None,
        description="Indicator for type of action performed during the event that generated the audit.",
    )
    period: Period | None = Field(
        default=None, description="The period during which the activity occurred."
    )
    recorded: str = Field(
        default=..., description="The time when the event was recorded."
    )
    outcome: Literal["0", "4", "8", "12"] | None = Field(
        default=None, description="Indicates whether the event succeeded or failed."
    )
    outcome_desc: str | None = Field(
        default=None,
        alias="outcomeDesc",
        description="A free text description of the outcome of the event.",
    )
    purpose_of_event: list[CodeableConcept] | None = Field(
        default=None,
        alias="purposeOfEvent",
        description="The purposeOfUse (reason) that was used during the event being recorded.",
    )
    agent: list[AuditEventAgent] = Field(
        default=...,
        description="An actor taking an active role in the event or activity that is logged.",
    )
    source: AuditEventSource = Field(
        default=..., description="The system that is reporting the event."
    )
    entity: list[AuditEventEntity] | None = Field(
        default=None,
        description="Specific instances of data or objects that have been accessed.",
    )


class AuditEventAgent(MedplumFHIRBase):
    """An actor taking an active role in the event or activity that is logged."""

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
    type: CodeableConcept | None = Field(
        default=None,
        description="Specification of the participation type the user plays when performing the event.",
    )
    role: list[CodeableConcept] | None = Field(
        default=None,
        description="The security role that the user was acting under, that come from local codes defined by the access control security system (e.g. RBAC, ABAC) used in the local context.",
    )
    who: Reference | None = Field(
        default=None,
        description="Reference to who this agent is that was involved in the event.",
    )
    alt_id: str | None = Field(
        default=None,
        alias="altId",
        description="Alternative agent Identifier. For a human, this should be a user identifier text string from authentication system. This identifier would be one known to a common authentication system (e.g. single sign-on), if available.",
    )
    name: str | None = Field(
        default=None, description="Human-meaningful name for the agent."
    )
    requestor: bool = Field(
        default=...,
        description="Indicator that the user is or is not the requestor, or initiator, for the event being audited.",
    )
    location: Reference | None = Field(
        default=None, description="Where the event occurred."
    )
    policy: list[str] | None = Field(
        default=None,
        description="The policy or plan that authorized the activity being recorded. Typically, a single activity may have multiple applicable policies, such as patient consent, guarantor funding, etc. The policy would also indicate the security token used.",
    )
    media: Coding | None = Field(
        default=None,
        description="Type of media involved. Used when the event is about exporting/importing onto media.",
    )
    network: AuditEventAgentNetwork | None = Field(
        default=None,
        description="Logical network location for application activity, if the activity has a network location.",
    )
    purpose_of_use: list[CodeableConcept] | None = Field(
        default=None,
        alias="purposeOfUse",
        description="The reason (purpose of use), specific to this agent, that was used during the event being recorded.",
    )


class AuditEventAgentNetwork(MedplumFHIRBase):
    """Logical network location for application activity, if the activity has a
    network location.
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
    address: str | None = Field(
        default=None,
        description="An identifier for the network access point of the user device for the audit event.",
    )
    type: Literal["1", "2", "3", "4", "5"] | None = Field(
        default=None,
        description="An identifier for the type of network access point that originated the audit event.",
    )


class AuditEventEntity(MedplumFHIRBase):
    """Specific instances of data or objects that have been accessed."""

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
    what: Reference | None = Field(
        default=None,
        description="Identifies a specific instance of the entity. The reference should be version specific.",
    )
    type: Coding | None = Field(
        default=None,
        description="The type of the object that was involved in this audit event.",
    )
    role: Coding | None = Field(
        default=None,
        description="Code representing the role the entity played in the event being audited.",
    )
    lifecycle: Coding | None = Field(
        default=None,
        description="Identifier for the data life-cycle stage for the entity.",
    )
    security_label: list[Coding] | None = Field(
        default=None,
        alias="securityLabel",
        description="Security labels for the identified entity.",
    )
    name: str | None = Field(
        default=None, description="A name of the entity in the audit event."
    )
    description: str | None = Field(
        default=None, description="Text that describes the entity in more detail."
    )
    query: str | None = Field(
        default=None, description="The query parameters for a query-type entities."
    )
    detail: list[AuditEventEntityDetail] | None = Field(
        default=None,
        description="Tagged value pairs for conveying additional information about the entity.",
    )


class AuditEventEntityDetail(MedplumFHIRBase):
    """Tagged value pairs for conveying additional information about the entity."""

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
    type: str = Field(
        default=..., description="The type of extra detail provided in the value."
    )
    value_string: str | None = Field(
        default=None, alias="valueString", description="The value of the extra detail."
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="The value of the extra detail.",
    )


class AuditEventSource(MedplumFHIRBase):
    """The system that is reporting the event."""

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
    site: str | None = Field(
        default=None,
        description="Logical source location within the healthcare enterprise network. For example, a hospital or other provider location within a multi-entity provider group.",
    )
    observer: Reference = Field(
        default=...,
        description="Identifier of the source where the event was detected.",
    )
    type: list[Coding] | None = Field(
        default=None,
        description="Code specifying the type of source where event originated.",
    )
