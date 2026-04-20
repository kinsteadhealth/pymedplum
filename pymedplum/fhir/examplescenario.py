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
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.usagecontext import UsageContext


class ExampleScenario(MedplumFHIRBase):
    """Example of workflow instance."""

    resource_type: Literal["ExampleScenario"] = Field(
        default="ExampleScenario", alias="resourceType"
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
    url: str | None = Field(
        default=None,
        description="An absolute URI that is used to identify this example scenario when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this example scenario is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the example scenario is stored on different servers.",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="A formal identifier that is used to identify this example scenario when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: str | None = Field(
        default=None,
        description="The identifier that is used to identify this version of the example scenario when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the example scenario author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: str | None = Field(
        default=None,
        description="A natural language name identifying the example scenario. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this example scenario. Enables tracking the life-cycle of the content.",
    )
    experimental: bool | None = Field(
        default=None,
        description="A Boolean value to indicate that this example scenario is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: str | None = Field(
        default=None,
        description="The date (and optionally time) when the example scenario was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the example scenario changes. (e.g. the 'content logical definition').",
    )
    publisher: str | None = Field(
        default=None,
        description="The name of the organization or individual that published the example scenario.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate example scenario instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None,
        description="A legal or geographic region in which the example scenario is intended to be used.",
    )
    copyright: str | None = Field(
        default=None,
        description="A copyright statement relating to the example scenario and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the example scenario.",
    )
    purpose: str | None = Field(
        default=None,
        description="What the example scenario resource is created for. This should not be used to show the business purpose of the scenario itself, but the purpose of documenting a scenario.",
    )
    actor: list[ExampleScenarioActor] | None = Field(
        default=None, description="Actor participating in the resource."
    )
    instance: list[ExampleScenarioInstance] | None = Field(
        default=None,
        description="Each resource and each version that is present in the workflow.",
    )
    process: list[ExampleScenarioProcess] | None = Field(
        default=None, description="Each major process - a group of operations."
    )
    workflow: list[str] | None = Field(
        default=None, description="Another nested workflow."
    )


class ExampleScenarioActor(MedplumFHIRBase):
    """Actor participating in the resource."""

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
    actor_id: str = Field(
        default=..., alias="actorId", description="ID or acronym of actor."
    )
    type: Literal["person", "entity"] = Field(
        default=..., description="The type of actor - person or system."
    )
    name: str | None = Field(
        default=None, description="The name of the actor as shown in the page."
    )
    description: str | None = Field(
        default=None, description="The description of the actor."
    )


class ExampleScenarioInstance(MedplumFHIRBase):
    """Each resource and each version that is present in the workflow."""

    resource_type: Literal["ExampleScenarioInstance"] = Field(
        default="ExampleScenarioInstance", alias="resourceType"
    )

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
    resource_id: str = Field(
        default=...,
        alias="resourceId",
        description="The id of the resource for referencing.",
    )
    name: str | None = Field(
        default=None, description="A short name for the resource instance."
    )
    description: str | None = Field(
        default=None, description="Human-friendly description of the resource instance."
    )
    version: list[ExampleScenarioInstanceVersion] | None = Field(
        default=None, description="A specific version of the resource."
    )
    contained_instance: list[ExampleScenarioInstanceContainedInstance] | None = Field(
        default=None,
        alias="containedInstance",
        description="Resources contained in the instance (e.g. the observations contained in a bundle).",
    )


class ExampleScenarioInstanceContainedInstance(MedplumFHIRBase):
    """Resources contained in the instance (e.g. the observations contained in a bundle)."""

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
    resource_id: str = Field(
        default=...,
        alias="resourceId",
        description="Each resource contained in the instance.",
    )
    version_id: str | None = Field(
        default=None,
        alias="versionId",
        description="A specific version of a resource contained in the instance.",
    )


class ExampleScenarioInstanceVersion(MedplumFHIRBase):
    """A specific version of the resource."""

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
    version_id: str = Field(
        default=...,
        alias="versionId",
        description="The identifier of a specific version of a resource.",
    )
    description: str = Field(
        default=..., description="The description of the resource version."
    )


class ExampleScenarioProcess(MedplumFHIRBase):
    """Each major process - a group of operations."""

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
    title: str = Field(
        default=..., description="The diagram title of the group of operations."
    )
    description: str | None = Field(
        default=None, description="A longer description of the group of operations."
    )
    pre_conditions: str | None = Field(
        default=None,
        alias="preConditions",
        description="Description of initial status before the process starts.",
    )
    post_conditions: str | None = Field(
        default=None,
        alias="postConditions",
        description="Description of final status after the process ends.",
    )
    step: list[ExampleScenarioProcessStep] | None = Field(
        default=None, description="Each step of the process."
    )


class ExampleScenarioProcessStep(MedplumFHIRBase):
    """Each step of the process."""

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
    process: list[ExampleScenarioProcess] | None = Field(
        default=None, description="Nested process."
    )
    pause: bool | None = Field(
        default=None, description="If there is a pause in the flow."
    )
    operation: ExampleScenarioProcessStepOperation | None = Field(
        default=None, description="Each interaction or action."
    )
    alternative: list[ExampleScenarioProcessStepAlternative] | None = Field(
        default=None,
        description="Indicates an alternative step that can be taken instead of the operations on the base step in exceptional/atypical circumstances.",
    )


class ExampleScenarioProcessStepAlternative(MedplumFHIRBase):
    """Indicates an alternative step that can be taken instead of the
    operations on the base step in exceptional/atypical circumstances.
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
    title: str = Field(
        default=...,
        description="The label to display for the alternative that gives a sense of the circumstance in which the alternative should be invoked.",
    )
    description: str | None = Field(
        default=None,
        description="A human-readable description of the alternative explaining when the alternative should occur rather than the base step.",
    )
    step: list[ExampleScenarioProcessStep] | None = Field(
        default=None, description="What happens in each alternative option."
    )


class ExampleScenarioProcessStepOperation(MedplumFHIRBase):
    """Each interaction or action."""

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
    number: str = Field(
        default=..., description="The sequential number of the interaction, e.g. 1.2.5."
    )
    type: str | None = Field(default=None, description="The type of operation - CRUD.")
    name: str | None = Field(
        default=None, description="The human-friendly name of the interaction."
    )
    initiator: str | None = Field(
        default=None, description="Who starts the transaction."
    )
    receiver: str | None = Field(
        default=None, description="Who receives the transaction."
    )
    description: str | None = Field(
        default=None, description="A comment to be inserted in the diagram."
    )
    initiator_active: bool | None = Field(
        default=None,
        alias="initiatorActive",
        description="Whether the initiator is deactivated right after the transaction.",
    )
    receiver_active: bool | None = Field(
        default=None,
        alias="receiverActive",
        description="Whether the receiver is deactivated right after the transaction.",
    )
    request: ExampleScenarioInstanceContainedInstance | None = Field(
        default=None, description="Each resource instance used by the initiator."
    )
    response: ExampleScenarioInstanceContainedInstance | None = Field(
        default=None, description="Each resource instance used by the responder."
    )
