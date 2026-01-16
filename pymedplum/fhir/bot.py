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
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.timing import Timing


class Bot(MedplumFHIRBase):
    """Bot account for automated actions."""

    resource_type: Literal["Bot"] = Field(default="Bot", alias="resourceType")

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
        default=None, description="An identifier for this bot."
    )
    name: str | None = Field(
        default=None, description="A name associated with the Bot."
    )
    description: str | None = Field(
        default=None,
        description="A summary, characterization or explanation of the Bot.",
    )
    runtime_version: Literal["awslambda", "vmcontext", "fission"] | None = Field(
        default=None,
        alias="runtimeVersion",
        description="The identifier of the bot runtime environment (i.e., vmcontext, awslambda, etc).",
    )
    timeout: int | float | None = Field(
        default=None,
        description="The maximum allowed execution time of the bot in seconds.",
    )
    photo: Attachment | None = Field(default=None, description="Image of the bot.")
    cron_timing: Timing | None = Field(
        default=None,
        alias="cronTiming",
        description="A schedule for the bot to be executed.",
    )
    cron_string: str | None = Field(
        default=None,
        alias="cronString",
        description="A schedule for the bot to be executed.",
    )
    category: list[CodeableConcept] | None = Field(
        default=None,
        description="A code that classifies the service for searching, sorting and display purposes (e.g. &quot;Surgical Procedure&quot;).",
    )
    system: bool | None = Field(
        default=None,
        description="Optional flag to indicate that the bot is a system bot and therefore has access to system secrets.",
    )
    run_as_user: bool | None = Field(
        default=None,
        alias="runAsUser",
        description="Optional flag to indicate that the bot should be run as the user.",
    )
    public_webhook: bool | None = Field(
        default=None,
        alias="publicWebhook",
        description="Optional flag to indicate that the bot can be used as an unauthenticated public webhook. Note that this is a security risk and should only be used for public bots that do not require authentication.",
    )
    audit_event_trigger: Literal["always", "never", "on-error", "on-output"] | None = (
        Field(
            default=None,
            alias="auditEventTrigger",
            description="Criteria for creating an AuditEvent as a result of the bot invocation. Possible values are 'always', 'never', 'on-error', or 'on-output'. Default value is 'always'.",
        )
    )
    audit_event_destination: list[Literal["log", "resource"]] | None = Field(
        default=None,
        alias="auditEventDestination",
        description="The destination system in which the AuditEvent is to be sent. Possible values are 'log' or 'resource'. Default value is 'resource'.",
    )
    source_code: Attachment | None = Field(
        default=None,
        alias="sourceCode",
        description="Bot logic in original source code form written by developers.",
    )
    executable_code: Attachment | None = Field(
        default=None,
        alias="executableCode",
        description="Bot logic in executable form as a result of compiling and bundling source code.",
    )
    cds_service: BotCdsService | None = Field(
        default=None,
        alias="cdsService",
        description="CDS service definition if the bot is used as a CDS Hooks service. See https://cds-hooks.hl7.org/ for more details.",
    )
    code: str | None = Field(default=None)


class BotCdsService(MedplumFHIRBase):
    """CDS service definition if the bot is used as a CDS Hooks service. See
    https://cds-hooks.hl7.org/ for more details.
    """

    hook: str = Field(
        default=...,
        description="The hook this service should be invoked on. See https://cds-hooks.hl7.org/#hooks for possible values.",
    )
    title: str = Field(
        default=..., description="The human-friendly name of this CDS service."
    )
    description: str = Field(
        default=..., description="The description of this CDS service."
    )
    usage_requirements: str | None = Field(
        default=None,
        alias="usageRequirements",
        description="Optional human-friendly description of any preconditions for the use of this CDS Service.",
    )
    prefetch: list[BotCdsServicePrefetch] | None = Field(
        default=None,
        description="An object containing key/value pairs of FHIR queries that this service is requesting the CDS Client to perform and provide on each service call.",
    )


class BotCdsServicePrefetch(MedplumFHIRBase):
    """An object containing key/value pairs of FHIR queries that this service
    is requesting the CDS Client to perform and provide on each service
    call.
    """

    key: str = Field(
        default=...,
        description="The type of data being requested. See https://cds-hooks.hl7.org/#prefetch-template",
    )
    query: str = Field(
        default=...,
        description="The FHIR query used to retrieve the requested data. See https://cds-hooks.hl7.org/#prefetch-template",
    )
