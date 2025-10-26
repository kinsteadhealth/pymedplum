# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Provenance(MedplumFHIRBase):
    """Provenance of a resource is a record that describes entities and
    processes involved in producing and delivering or otherwise influencing
    that resource. Provenance provides a critical foundation for assessing
    authenticity, enabling trust, and allowing reproducibility. Provenance
    assertions are a form of contextual metadata and can themselves become
    important records with their own provenance. Provenance statement
    indicates clinical significance in terms of confidence in authenticity,
    reliability, and trustworthiness, integrity, and stage in lifecycle
    (e.g. Document Completion - has the artifact been legally
    authenticated), all of which may impact security, privacy, and trust
    policies.
    """

    resource_type: Literal["Provenance"] = Field(
        default="Provenance",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[list[dict[str, Any]]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    target: list[Reference] = Field(default=..., description="The Reference(s) that were generated or updated by the activity described in this resource. A provenance can point to more than one target if multiple resources were created/updated by the same activity.")
    occurred_period: Optional[Period] = Field(default=None, alias="occurredPeriod", description="The period during which the activity occurred.")
    occurred_date_time: Optional[str] = Field(default=None, alias="occurredDateTime", description="The period during which the activity occurred.")
    recorded: str = Field(default=..., description="The instant of time at which the activity was recorded.")
    policy: Optional[list[str]] = Field(default=None, description="Policy or plan the activity was defined by. Typically, a single activity may have multiple applicable policy documents, such as patient consent, guarantor funding, etc.")
    location: Optional[Reference] = Field(default=None, description="Where the activity occurred, if relevant.")
    reason: Optional[list[CodeableConcept]] = Field(default=None, description="The reason that the activity was taking place.")
    activity: Optional[CodeableConcept] = Field(default=None, description="An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.")
    agent: list[ProvenanceAgent] = Field(default=..., description="An actor taking a role in an activity for which it can be assigned some degree of responsibility for the activity taking place.")
    entity: Optional[list[ProvenanceEntity]] = Field(default=None, description="An entity used in this activity.")
    signature: Optional[list[Signature]] = Field(default=None, description="A digital signature on the target Reference(s). The signer should match a Provenance.agent. The purpose of the signature is indicated.")


class ProvenanceAgent(MedplumFHIRBase):
    """An actor taking a role in an activity for which it can be assigned some
    degree of responsibility for the activity taking place.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: Optional[CodeableConcept] = Field(default=None, description="The participation the agent had with respect to the activity.")
    role: Optional[list[CodeableConcept]] = Field(default=None, description="The function of the agent with respect to the activity. The security role enabling the agent with respect to the activity.")
    who: Reference = Field(default=..., description="The individual, device or organization that participated in the event.")
    on_behalf_of: Optional[Reference] = Field(default=None, alias="onBehalfOf", description="The individual, device, or organization for whom the change was made.")


class ProvenanceEntity(MedplumFHIRBase):
    """An entity used in this activity."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    role: Literal['derivation', 'revision', 'quotation', 'source', 'removal'] = Field(default=..., description="How the entity was used during the activity.")
    what: Reference = Field(default=..., description="Identity of the Entity used. May be a logical or physical uri and maybe absolute or relative.")
    agent: Optional[list[ProvenanceAgent]] = Field(default=None, description="The entity is attributed to an agent to express the agent's responsibility for that entity, possibly along with other agents. This description can be understood as shorthand for saying that the agent was responsible for the activity which generated the entity.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Provenance", Provenance)
    register_model("ProvenanceAgent", ProvenanceAgent)
    register_model("ProvenanceEntity", ProvenanceEntity)
