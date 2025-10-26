# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Contract(MedplumFHIRBase):
    """Legally enforceable, formally recorded unilateral or bilateral directive
    i.e., a policy or agreement.
    """

    resource_type: Literal["Contract"] = Field(
        default="Contract",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Unique identifier for this Contract or a derivative that references a Source Contract.")
    url: Optional[str] = Field(default=None, description="Canonical identifier for this contract, represented as a URI (globally unique).")
    version: Optional[str] = Field(default=None, description="An edition identifier used for business purposes to label business significant variants.")
    status: Optional[Literal['amended', 'appended', 'cancelled', 'disputed', 'entered-in-error', 'executable', 'executed', 'negotiable', 'offered', 'policy', 'rejected', 'renewed', 'revoked', 'resolved', 'terminated']] = Field(default=None, description="The status of the resource instance.")
    legal_state: Optional[CodeableConcept] = Field(default=None, alias="legalState", description="Legal states of the formation of a legal instrument, which is a formally executed written document that can be formally attributed to its author, records and formally expresses a legally enforceable act, process, or contractual duty, obligation, or right, and therefore evidences that act, process, or agreement.")
    instantiates_canonical: Optional[Reference] = Field(default=None, alias="instantiatesCanonical", description="The URL pointing to a FHIR-defined Contract Definition that is adhered to in whole or part by this Contract.")
    instantiates_uri: Optional[str] = Field(default=None, alias="instantiatesUri", description="The URL pointing to an externally maintained definition that is adhered to in whole or in part by this Contract.")
    content_derivative: Optional[CodeableConcept] = Field(default=None, alias="contentDerivative", description="The minimal content derived from the basal information source at a specific stage in its lifecycle.")
    issued: Optional[str] = Field(default=None, description="When this Contract was issued.")
    applies: Optional[Period] = Field(default=None, description="Relevant time or time-period when this Contract is applicable.")
    expiration_type: Optional[CodeableConcept] = Field(default=None, alias="expirationType", description="Event resulting in discontinuation or termination of this Contract instance by one or more parties to the contract.")
    subject: Optional[list[Reference]] = Field(default=None, description="The target entity impacted by or of interest to parties to the agreement.")
    authority: Optional[list[Reference]] = Field(default=None, description="A formally or informally recognized grouping of people, principals, organizations, or jurisdictions formed for the purpose of achieving some form of collective action such as the promulgation, administration and enforcement of contracts and policies.")
    domain: Optional[list[Reference]] = Field(default=None, description="Recognized governance framework or system operating with a circumscribed scope in accordance with specified principles, policies, processes or procedures for managing rights, actions, or behaviors of parties or principals relative to resources.")
    site: Optional[list[Reference]] = Field(default=None, description="Sites in which the contract is complied with, exercised, or in force.")
    name: Optional[str] = Field(default=None, description="A natural language name identifying this Contract definition, derivative, or instance in any legal state. Provides additional information about its content. This name should be usable as an identifier for the module by machine processing applications such as code generation.")
    title: Optional[str] = Field(default=None, description="A short, descriptive, user-friendly title for this Contract definition, derivative, or instance in any legal state.t giving additional information about its content.")
    subtitle: Optional[str] = Field(default=None, description="An explanatory or alternate user-friendly title for this Contract definition, derivative, or instance in any legal state.t giving additional information about its content.")
    alias: Optional[list[str]] = Field(default=None, description="Alternative representation of the title for this Contract definition, derivative, or instance in any legal state., e.g., a domain specific contract number related to legislation.")
    author: Optional[Reference] = Field(default=None, description="The individual or organization that authored the Contract definition, derivative, or instance in any legal state.")
    scope: Optional[CodeableConcept] = Field(default=None, description="A selector of legal concerns for this Contract definition, derivative, or instance in any legal state.")
    topic_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="topicCodeableConcept", description="Narrows the range of legal concerns to focus on the achievement of specific contractual objectives.")
    topic_reference: Optional[Reference] = Field(default=None, alias="topicReference", description="Narrows the range of legal concerns to focus on the achievement of specific contractual objectives.")
    type: Optional[CodeableConcept] = Field(default=None, description="A high-level category for the legal instrument, whether constructed as a Contract definition, derivative, or instance in any legal state. Provides additional information about its content within the context of the Contract's scope to distinguish the kinds of systems that would be interested in the contract.")
    sub_type: Optional[list[CodeableConcept]] = Field(default=None, alias="subType", description="Sub-category for the Contract that distinguishes the kinds of systems that would be interested in the Contract within the context of the Contract's scope.")
    content_definition: Optional[ContractContentDefinition] = Field(default=None, alias="contentDefinition", description="Precusory content developed with a focus and intent of supporting the formation a Contract instance, which may be associated with and transformable into a Contract.")
    term: Optional[list[ContractTerm]] = Field(default=None, description="One or more Contract Provisions, which may be related and conveyed as a group, and may contain nested groups.")
    supporting_info: Optional[list[Reference]] = Field(default=None, alias="supportingInfo", description="Information that may be needed by/relevant to the performer in their execution of this term action.")
    relevant_history: Optional[list[Reference]] = Field(default=None, alias="relevantHistory", description="Links to Provenance records for past versions of this Contract definition, derivative, or instance, which identify key state transitions or updates that are likely to be relevant to a user looking at the current version of the Contract. The Provence.entity indicates the target that was changed in the update. http://build.fhir.org/provenance-definitions.html#Provenance.entity.")
    signer: Optional[list[ContractSigner]] = Field(default=None, description="Parties with legal standing in the Contract, including the principal parties, the grantor(s) and grantee(s), which are any person or organization bound by the contract, and any ancillary parties, which facilitate the execution of the contract such as a notary or witness.")
    friendly: Optional[list[ContractFriendly]] = Field(default=None, description="The &quot;patient friendly language&quot; versionof the Contract in whole or in parts. &quot;Patient friendly language&quot; means the representation of the Contract and Contract Provisions in a manner that is readily accessible and understandable by a layperson in accordance with best practices for communication styles that ensure that those agreeing to or signing the Contract understand the roles, actions, obligations, responsibilities, and implication of the agreement.")
    legal: Optional[list[ContractLegal]] = Field(default=None, description="List of Legal expressions or representations of this Contract.")
    rule: Optional[list[ContractRule]] = Field(default=None, description="List of Computable Policy Rule Language Representations of this Contract.")
    legally_binding_attachment: Optional[Attachment] = Field(default=None, alias="legallyBindingAttachment", description="Legally binding Contract: This is the signed and legally recognized representation of the Contract, which is considered the &quot;source of truth&quot; and which would be the basis for legal action related to enforcement of this Contract.")
    legally_binding_reference: Optional[Reference] = Field(default=None, alias="legallyBindingReference", description="Legally binding Contract: This is the signed and legally recognized representation of the Contract, which is considered the &quot;source of truth&quot; and which would be the basis for legal action related to enforcement of this Contract.")


class ContractContentDefinition(MedplumFHIRBase):
    """Precusory content developed with a focus and intent of supporting the
    formation a Contract instance, which may be associated with and
    transformable into a Contract.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: CodeableConcept = Field(default=..., description="Precusory content structure and use, i.e., a boilerplate, template, application for a contract such as an insurance policy or benefits under a program, e.g., workers compensation.")
    sub_type: Optional[CodeableConcept] = Field(default=None, alias="subType", description="Detailed Precusory content type.")
    publisher: Optional[Reference] = Field(default=None, description="The individual or organization that published the Contract precursor content.")
    publication_date: Optional[str] = Field(default=None, alias="publicationDate", description="The date (and optionally time) when the contract was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the contract changes.")
    publication_status: Literal['amended', 'appended', 'cancelled', 'disputed', 'entered-in-error', 'executable', 'executed', 'negotiable', 'offered', 'policy', 'rejected', 'renewed', 'revoked', 'resolved', 'terminated'] = Field(default=..., alias="publicationStatus", description="amended | appended | cancelled | disputed | entered-in-error | executable | executed | negotiable | offered | policy | rejected | renewed | revoked | resolved | terminated.")
    copyright: Optional[str] = Field(default=None, description="A copyright statement relating to Contract precursor content. Copyright statements are generally legal restrictions on the use and publishing of the Contract precursor content.")


class ContractFriendly(MedplumFHIRBase):
    """The &quot;patient friendly language&quot; versionof the Contract in
    whole or in parts. &quot;Patient friendly language&quot; means the
    representation of the Contract and Contract Provisions in a manner that
    is readily accessible and understandable by a layperson in accordance
    with best practices for communication styles that ensure that those
    agreeing to or signing the Contract understand the roles, actions,
    obligations, responsibilities, and implication of the agreement.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    content_attachment: Optional[Attachment] = Field(default=None, alias="contentAttachment", description="Human readable rendering of this Contract in a format and representation intended to enhance comprehension and ensure understandability.")
    content_reference: Optional[Reference] = Field(default=None, alias="contentReference", description="Human readable rendering of this Contract in a format and representation intended to enhance comprehension and ensure understandability.")


class ContractLegal(MedplumFHIRBase):
    """List of Legal expressions or representations of this Contract."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    content_attachment: Optional[Attachment] = Field(default=None, alias="contentAttachment", description="Contract legal text in human renderable form.")
    content_reference: Optional[Reference] = Field(default=None, alias="contentReference", description="Contract legal text in human renderable form.")


class ContractRule(MedplumFHIRBase):
    """List of Computable Policy Rule Language Representations of this Contract."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    content_attachment: Optional[Attachment] = Field(default=None, alias="contentAttachment", description="Computable Contract conveyed using a policy rule language (e.g. XACML, DKAL, SecPal).")
    content_reference: Optional[Reference] = Field(default=None, alias="contentReference", description="Computable Contract conveyed using a policy rule language (e.g. XACML, DKAL, SecPal).")


class ContractSigner(MedplumFHIRBase):
    """Parties with legal standing in the Contract, including the principal
    parties, the grantor(s) and grantee(s), which are any person or
    organization bound by the contract, and any ancillary parties, which
    facilitate the execution of the contract such as a notary or witness.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    type: Coding = Field(default=..., description="Role of this Contract signer, e.g. notary, grantee.")
    party: Reference = Field(default=..., description="Party which is a signator to this Contract.")
    signature: list[Signature] = Field(default=..., description="Legally binding Contract DSIG signature contents in Base64.")


class ContractTerm(MedplumFHIRBase):
    """One or more Contract Provisions, which may be related and conveyed as a
    group, and may contain nested groups.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[Identifier] = Field(default=None, description="Unique identifier for this particular Contract Provision.")
    issued: Optional[str] = Field(default=None, description="When this Contract Provision was issued.")
    applies: Optional[Period] = Field(default=None, description="Relevant time or time-period when this Contract Provision is applicable.")
    topic_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="topicCodeableConcept", description="The entity that the term applies to.")
    topic_reference: Optional[Reference] = Field(default=None, alias="topicReference", description="The entity that the term applies to.")
    type: Optional[CodeableConcept] = Field(default=None, description="A legal clause or condition contained within a contract that requires one or both parties to perform a particular requirement by some specified time or prevents one or both parties from performing a particular requirement by some specified time.")
    sub_type: Optional[CodeableConcept] = Field(default=None, alias="subType", description="A specialized legal clause or condition based on overarching contract type.")
    text: Optional[str] = Field(default=None, description="Statement of a provision in a policy or a contract.")
    security_label: Optional[list[ContractTermSecurityLabel]] = Field(default=None, alias="securityLabel", description="Security labels that protect the handling of information about the term and its elements, which may be specifically identified..")
    offer: ContractTermOffer = Field(default=..., description="The matter of concern in the context of this provision of the agrement.")
    asset: Optional[list[ContractTermAsset]] = Field(default=None, description="Contract Term Asset List.")
    action: Optional[list[ContractTermAction]] = Field(default=None, description="An actor taking a role in an activity for which it can be assigned some degree of responsibility for the activity taking place.")
    group: Optional[list[ContractTerm]] = Field(default=None, description="Nested group of Contract Provisions.")


class ContractTermAction(MedplumFHIRBase):
    """An actor taking a role in an activity for which it can be assigned some
    degree of responsibility for the activity taking place.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    do_not_perform: Optional[bool] = Field(default=None, alias="doNotPerform", description="True if the term prohibits the action.")
    type: CodeableConcept = Field(default=..., description="Activity or service obligation to be done or not done, performed or not performed, effectuated or not by this Contract term.")
    subject: Optional[list[ContractTermActionSubject]] = Field(default=None, description="Entity of the action.")
    intent: CodeableConcept = Field(default=..., description="Reason or purpose for the action stipulated by this Contract Provision.")
    link_id: Optional[list[str]] = Field(default=None, alias="linkId", description="Id [identifier??] of the clause or question text related to this action in the referenced form or QuestionnaireResponse.")
    status: CodeableConcept = Field(default=..., description="Current state of the term action.")
    context: Optional[Reference] = Field(default=None, description="Encounter or Episode with primary association to specified term activity.")
    context_link_id: Optional[list[str]] = Field(default=None, alias="contextLinkId", description="Id [identifier??] of the clause or question text related to the requester of this action in the referenced form or QuestionnaireResponse.")
    occurrence_date_time: Optional[str] = Field(default=None, alias="occurrenceDateTime", description="When action happens.")
    occurrence_period: Optional[Period] = Field(default=None, alias="occurrencePeriod", description="When action happens.")
    occurrence_timing: Optional[Timing] = Field(default=None, alias="occurrenceTiming", description="When action happens.")
    requester: Optional[list[Reference]] = Field(default=None, description="Who or what initiated the action and has responsibility for its activation.")
    requester_link_id: Optional[list[str]] = Field(default=None, alias="requesterLinkId", description="Id [identifier??] of the clause or question text related to the requester of this action in the referenced form or QuestionnaireResponse.")
    performer_type: Optional[list[CodeableConcept]] = Field(default=None, alias="performerType", description="The type of individual that is desired or required to perform or not perform the action.")
    performer_role: Optional[CodeableConcept] = Field(default=None, alias="performerRole", description="The type of role or competency of an individual desired or required to perform or not perform the action.")
    performer: Optional[Reference] = Field(default=None, description="Indicates who or what is being asked to perform (or not perform) the ction.")
    performer_link_id: Optional[list[str]] = Field(default=None, alias="performerLinkId", description="Id [identifier??] of the clause or question text related to the reason type or reference of this action in the referenced form or QuestionnaireResponse.")
    reason_code: Optional[list[CodeableConcept]] = Field(default=None, alias="reasonCode", description="Rationale for the action to be performed or not performed. Describes why the action is permitted or prohibited.")
    reason_reference: Optional[list[Reference]] = Field(default=None, alias="reasonReference", description="Indicates another resource whose existence justifies permitting or not permitting this action.")
    reason: Optional[list[str]] = Field(default=None, description="Describes why the action is to be performed or not performed in textual form.")
    reason_link_id: Optional[list[str]] = Field(default=None, alias="reasonLinkId", description="Id [identifier??] of the clause or question text related to the reason type or reference of this action in the referenced form or QuestionnaireResponse.")
    note: Optional[list[Annotation]] = Field(default=None, description="Comments made about the term action made by the requester, performer, subject or other participants.")
    security_label_number: Optional[list[Union[int, float]]] = Field(default=None, alias="securityLabelNumber", description="Security labels that protects the action.")


class ContractTermActionSubject(MedplumFHIRBase):
    """Entity of the action."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    reference: list[Reference] = Field(default=..., description="The entity the action is performed or not performed on or for.")
    role: Optional[CodeableConcept] = Field(default=None, description="Role type of agent assigned roles in this Contract.")


class ContractTermAsset(MedplumFHIRBase):
    """Contract Term Asset List."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    scope: Optional[CodeableConcept] = Field(default=None, description="Differentiates the kind of the asset .")
    type: Optional[list[CodeableConcept]] = Field(default=None, description="Target entity type about which the term may be concerned.")
    type_reference: Optional[list[Reference]] = Field(default=None, alias="typeReference", description="Associated entities.")
    subtype: Optional[list[CodeableConcept]] = Field(default=None, description="May be a subtype or part of an offered asset.")
    relationship: Optional[Coding] = Field(default=None, description="Specifies the applicability of the term to an asset resource instance, and instances it refers to orinstances that refer to it, and/or are owned by the offeree.")
    context: Optional[list[ContractTermAssetContext]] = Field(default=None, description="Circumstance of the asset.")
    condition: Optional[str] = Field(default=None, description="Description of the quality and completeness of the asset that imay be a factor in its valuation.")
    period_type: Optional[list[CodeableConcept]] = Field(default=None, alias="periodType", description="Type of Asset availability for use or ownership.")
    period: Optional[list[Period]] = Field(default=None, description="Asset relevant contractual time period.")
    use_period: Optional[list[Period]] = Field(default=None, alias="usePeriod", description="Time period of asset use.")
    text: Optional[str] = Field(default=None, description="Clause or question text (Prose Object) concerning the asset in a linked form, such as a QuestionnaireResponse used in the formation of the contract.")
    link_id: Optional[list[str]] = Field(default=None, alias="linkId", description="Id [identifier??] of the clause or question text about the asset in the referenced form or QuestionnaireResponse.")
    answer: Optional[list[ContractTermOfferAnswer]] = Field(default=None, description="Response to assets.")
    security_label_number: Optional[list[Union[int, float]]] = Field(default=None, alias="securityLabelNumber", description="Security labels that protects the asset.")
    valued_item: Optional[list[ContractTermAssetValuedItem]] = Field(default=None, alias="valuedItem", description="Contract Valued Item List.")


class ContractTermAssetContext(MedplumFHIRBase):
    """Circumstance of the asset."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    reference: Optional[Reference] = Field(default=None, description="Asset context reference may include the creator, custodian, or owning Person or Organization (e.g., bank, repository), location held, e.g., building, jurisdiction.")
    code: Optional[list[CodeableConcept]] = Field(default=None, description="Coded representation of the context generally or of the Referenced entity, such as the asset holder type or location.")
    text: Optional[str] = Field(default=None, description="Context description.")


class ContractTermAssetValuedItem(MedplumFHIRBase):
    """Contract Valued Item List."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    entity_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="entityCodeableConcept", description="Specific type of Contract Valued Item that may be priced.")
    entity_reference: Optional[Reference] = Field(default=None, alias="entityReference", description="Specific type of Contract Valued Item that may be priced.")
    identifier: Optional[Identifier] = Field(default=None, description="Identifies a Contract Valued Item instance.")
    effective_time: Optional[str] = Field(default=None, alias="effectiveTime", description="Indicates the time during which this Contract ValuedItem information is effective.")
    quantity: Optional[Quantity] = Field(default=None, description="Specifies the units by which the Contract Valued Item is measured or counted, and quantifies the countable or measurable Contract Valued Item instances.")
    unit_price: Optional[Money] = Field(default=None, alias="unitPrice", description="A Contract Valued Item unit valuation measure.")
    factor: Optional[Union[int, float]] = Field(default=None, description="A real number that represents a multiplier used in determining the overall value of the Contract Valued Item delivered. The concept of a Factor allows for a discount or surcharge multiplier to be applied to a monetary amount.")
    points: Optional[Union[int, float]] = Field(default=None, description="An amount that expresses the weighting (based on difficulty, cost and/or resource intensiveness) associated with the Contract Valued Item delivered. The concept of Points allows for assignment of point values for a Contract Valued Item, such that a monetary amount can be assigned to each point.")
    net: Optional[Money] = Field(default=None, description="Expresses the product of the Contract Valued Item unitQuantity and the unitPriceAmt. For example, the formula: unit Quantity * unit Price (Cost per Point) * factor Number * points = net Amount. Quantity, factor and points are assumed to be 1 if not supplied.")
    payment: Optional[str] = Field(default=None, description="Terms of valuation.")
    payment_date: Optional[str] = Field(default=None, alias="paymentDate", description="When payment is due.")
    responsible: Optional[Reference] = Field(default=None, description="Who will make payment.")
    recipient: Optional[Reference] = Field(default=None, description="Who will receive payment.")
    link_id: Optional[list[str]] = Field(default=None, alias="linkId", description="Id of the clause or question text related to the context of this valuedItem in the referenced form or QuestionnaireResponse.")
    security_label_number: Optional[list[Union[int, float]]] = Field(default=None, alias="securityLabelNumber", description="A set of security labels that define which terms are controlled by this condition.")


class ContractTermOffer(MedplumFHIRBase):
    """The matter of concern in the context of this provision of the agrement."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[list[Identifier]] = Field(default=None, description="Unique identifier for this particular Contract Provision.")
    party: Optional[list[ContractTermOfferParty]] = Field(default=None, description="Offer Recipient.")
    topic: Optional[Reference] = Field(default=None, description="The owner of an asset has the residual control rights over the asset: the right to decide all usages of the asset in any way not inconsistent with a prior contract, custom, or law (Hart, 1995, p. 30).")
    type: Optional[CodeableConcept] = Field(default=None, description="Type of Contract Provision such as specific requirements, purposes for actions, obligations, prohibitions, e.g. life time maximum benefit.")
    decision: Optional[CodeableConcept] = Field(default=None, description="Type of choice made by accepting party with respect to an offer made by an offeror/ grantee.")
    decision_mode: Optional[list[CodeableConcept]] = Field(default=None, alias="decisionMode", description="How the decision about a Contract was conveyed.")
    answer: Optional[list[ContractTermOfferAnswer]] = Field(default=None, description="Response to offer text.")
    text: Optional[str] = Field(default=None, description="Human readable form of this Contract Offer.")
    link_id: Optional[list[str]] = Field(default=None, alias="linkId", description="The id of the clause or question text of the offer in the referenced questionnaire/response.")
    security_label_number: Optional[list[Union[int, float]]] = Field(default=None, alias="securityLabelNumber", description="Security labels that protects the offer.")


class ContractTermOfferAnswer(MedplumFHIRBase):
    """Response to offer text."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_decimal: Optional[Union[int, float]] = Field(default=None, alias="valueDecimal", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_integer: Optional[Union[int, float]] = Field(default=None, alias="valueInteger", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_date: Optional[str] = Field(default=None, alias="valueDate", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_date_time: Optional[str] = Field(default=None, alias="valueDateTime", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_time: Optional[str] = Field(default=None, alias="valueTime", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_string: Optional[str] = Field(default=None, alias="valueString", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_uri: Optional[str] = Field(default=None, alias="valueUri", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_attachment: Optional[Attachment] = Field(default=None, alias="valueAttachment", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_coding: Optional[Coding] = Field(default=None, alias="valueCoding", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")
    value_reference: Optional[Reference] = Field(default=None, alias="valueReference", description="Response to an offer clause or question text, which enables selection of values to be agreed to, e.g., the period of participation, the date of occupancy of a rental, warrently duration, or whether biospecimen may be used for further research.")


class ContractTermOfferParty(MedplumFHIRBase):
    """Offer Recipient."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    reference: list[Reference] = Field(default=..., description="Participant in the offer.")
    role: CodeableConcept = Field(default=..., description="How the party participates in the offer.")


class ContractTermSecurityLabel(MedplumFHIRBase):
    """Security labels that protect the handling of information about the term
    and its elements, which may be specifically identified..
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    number: Optional[list[Union[int, float]]] = Field(default=None, description="Number used to link this term or term element to the applicable Security Label.")
    classification: Coding = Field(default=..., description="Security label privacy tag that species the level of confidentiality protection required for this term and/or term elements.")
    category: Optional[list[Coding]] = Field(default=None, description="Security label privacy tag that species the applicable privacy and security policies governing this term and/or term elements.")
    control: Optional[list[Coding]] = Field(default=None, description="Security label privacy tag that species the manner in which term and/or term elements are to be protected.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Contract", Contract)
    register_model("ContractContentDefinition", ContractContentDefinition)
    register_model("ContractFriendly", ContractFriendly)
    register_model("ContractLegal", ContractLegal)
    register_model("ContractRule", ContractRule)
    register_model("ContractSigner", ContractSigner)
    register_model("ContractTerm", ContractTerm)
    register_model("ContractTermAction", ContractTermAction)
    register_model("ContractTermActionSubject", ContractTermActionSubject)
    register_model("ContractTermAsset", ContractTermAsset)
    register_model("ContractTermAssetContext", ContractTermAssetContext)
    register_model("ContractTermAssetValuedItem", ContractTermAssetValuedItem)
    register_model("ContractTermOffer", ContractTermOffer)
    register_model("ContractTermOfferAnswer", ContractTermOfferAnswer)
    register_model("ContractTermOfferParty", ContractTermOfferParty)
    register_model("ContractTermSecurityLabel", ContractTermSecurityLabel)
