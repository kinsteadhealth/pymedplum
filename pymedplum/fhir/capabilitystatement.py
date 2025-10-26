# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CapabilityStatement(MedplumFHIRBase):
    """A Capability Statement documents a set of capabilities (behaviors) of a
    FHIR Server for a particular version of FHIR that may be used as a
    statement of actual server functionality or a statement of required or
    desired server implementation.
    """

    resource_type: Literal["CapabilityStatement"] = Field(
        default="CapabilityStatement", alias="resourceType"
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
    url: Optional[str] = Field(
        default=None,
        description="An absolute URI that is used to identify this capability statement when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this capability statement is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the capability statement is stored on different servers.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the capability statement when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the capability statement author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A natural language name identifying the capability statement. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the capability statement.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this capability statement. Enables tracking the life-cycle of the content.",
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this capability statement is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: str = Field(
        default=...,
        description="The date (and optionally time) when the capability statement was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the capability statement changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the capability statement.",
    )
    contact: Optional[List[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the capability statement from a consumer's perspective. Typically, this is used when the capability statement describes a desired rather than an actual solution, for example as a formal expression of requirements as part of an RFP.",
    )
    use_context: Optional[List[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate capability statement instances.",
    )
    jurisdiction: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the capability statement is intended to be used.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Explanation of why this capability statement is needed and why it has been designed as it has.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the capability statement and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the capability statement.",
    )
    kind: Literal["instance", "capability", "requirements"] = Field(
        default=...,
        description="The way that this statement is intended to be used, to describe an actual running instance of software, a particular product (kind, not instance of software) or a class of implementation (e.g. a desired purchase).",
    )
    instantiates: Optional[List[str]] = Field(
        default=None,
        description="Reference to a canonical URL of another CapabilityStatement that this software implements. This capability statement is a published API description that corresponds to a business service. The server may actually implement a subset of the capability statement it claims to implement, so the capability statement must specify the full capability details.",
    )
    imports: Optional[List[str]] = Field(
        default=None,
        description="Reference to a canonical URL of another CapabilityStatement that this software adds to. The capability statement automatically includes everything in the other statement, and it is not duplicated, though the server may repeat the same resources, interactions and operations to add additional details to them.",
    )
    software: Optional[CapabilityStatementSoftware] = Field(
        default=None,
        description="Software that is covered by this capability statement. It is used when the capability statement describes the capabilities of a particular software version, independent of an installation.",
    )
    implementation: Optional[CapabilityStatementImplementation] = Field(
        default=None,
        description="Identifies a specific implementation instance that is described by the capability statement - i.e. a particular installation, rather than the capabilities of a software program.",
    )
    fhir_version: Literal[
        "0.01",
        "0.05",
        "0.06",
        "0.11",
        "0.0.80",
        "0.0.81",
        "0.0.82",
        "0.4.0",
        "0.5.0",
        "1.0.0",
        "1.0.1",
        "1.0.2",
        "1.1.0",
        "1.4.0",
        "1.6.0",
        "1.8.0",
        "3.0.0",
        "3.0.1",
        "3.3.0",
        "3.5.0",
        "4.0.0",
        "4.0.1",
    ] = Field(
        default=...,
        alias="fhirVersion",
        description="The version of the FHIR specification that this CapabilityStatement describes (which SHALL be the same as the FHIR version of the CapabilityStatement itself). There is no default value.",
    )
    format: List[str] = Field(
        default=...,
        description="A list of the formats supported by this implementation using their content types.",
    )
    patch_format: Optional[List[str]] = Field(
        default=None,
        alias="patchFormat",
        description="A list of the patch formats supported by this implementation using their content types.",
    )
    implementation_guide: Optional[List[str]] = Field(
        default=None,
        alias="implementationGuide",
        description="A list of implementation guides that the server does (or should) support in their entirety.",
    )
    rest: Optional[List[CapabilityStatementRest]] = Field(
        default=None,
        description="A definition of the restful capabilities of the solution, if any.",
    )
    messaging: Optional[List[CapabilityStatementMessaging]] = Field(
        default=None,
        description="A description of the messaging capabilities of the solution.",
    )
    document: Optional[List[CapabilityStatementDocument]] = Field(
        default=None, description="A document definition."
    )


class CapabilityStatementDocument(MedplumFHIRBase):
    """A document definition."""

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
    mode: Literal["producer", "consumer"] = Field(
        default=...,
        description="Mode of this document declaration - whether an application is a producer or consumer.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="A description of how the application supports or uses the specified document profile. For example, when documents are created, what action is taken with consumed documents, etc.",
    )
    profile: str = Field(
        default=...,
        description="A profile on the document Bundle that constrains which resources are present, and their contents.",
    )


class CapabilityStatementImplementation(MedplumFHIRBase):
    """Identifies a specific implementation instance that is described by the
    capability statement - i.e. a particular installation, rather than the
    capabilities of a software program.
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
        description="Information about the specific installation that this capability statement relates to.",
    )
    url: Optional[str] = Field(
        default=None,
        description="An absolute base URL for the implementation. This forms the base for REST interfaces as well as the mailbox and document interfaces.",
    )
    custodian: Optional[Reference] = Field(
        default=None,
        description="The organization responsible for the management of the instance and oversight of the data on the server at the specified URL.",
    )


class CapabilityStatementMessaging(MedplumFHIRBase):
    """A description of the messaging capabilities of the solution."""

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
    endpoint: Optional[List[CapabilityStatementMessagingEndpoint]] = Field(
        default=None,
        description="An endpoint (network accessible address) to which messages and/or replies are to be sent.",
    )
    reliable_cache: Optional[Union[int, float]] = Field(
        default=None,
        alias="reliableCache",
        description="Length if the receiver's reliable messaging cache in minutes (if a receiver) or how long the cache length on the receiver should be (if a sender).",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Documentation about the system's messaging capabilities for this endpoint not otherwise documented by the capability statement. For example, the process for becoming an authorized messaging exchange partner.",
    )
    supported_message: Optional[List[CapabilityStatementMessagingSupportedMessage]] = (
        Field(
            default=None,
            alias="supportedMessage",
            description="References to message definitions for messages this system can send or receive.",
        )
    )


class CapabilityStatementMessagingEndpoint(MedplumFHIRBase):
    """An endpoint (network accessible address) to which messages and/or
    replies are to be sent.
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
    protocol: Coding = Field(
        default=...,
        description="A list of the messaging transport protocol(s) identifiers, supported by this endpoint.",
    )
    address: str = Field(
        default=...,
        description="The network address of the endpoint. For solutions that do not use network addresses for routing, it can be just an identifier.",
    )


class CapabilityStatementMessagingSupportedMessage(MedplumFHIRBase):
    """References to message definitions for messages this system can send or receive."""

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
    mode: Literal["sender", "receiver"] = Field(
        default=...,
        description="The mode of this event declaration - whether application is sender or receiver.",
    )
    definition: str = Field(
        default=...,
        description="Points to a message definition that identifies the messaging event, message structure, allowed responses, etc.",
    )


class CapabilityStatementRest(MedplumFHIRBase):
    """A definition of the restful capabilities of the solution, if any."""

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
    mode: Literal["client", "server"] = Field(
        default=...,
        description="Identifies whether this portion of the statement is describing the ability to initiate or receive restful operations.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Information about the system's restful capabilities that apply across all applications, such as security.",
    )
    security: Optional[CapabilityStatementRestSecurity] = Field(
        default=None,
        description="Information about security implementation from an interface perspective - what a client needs to know.",
    )
    resource: Optional[List[CapabilityStatementRestResource]] = Field(
        default=None,
        description="A specification of the restful capabilities of the solution for a specific resource type.",
    )
    interaction: Optional[List[CapabilityStatementRestInteraction]] = Field(
        default=None,
        description="A specification of restful operations supported by the system.",
    )
    search_param: Optional[List[CapabilityStatementRestResourceSearchParam]] = Field(
        default=None,
        alias="searchParam",
        description="Search parameters that are supported for searching all resources for implementations to support and/or make use of - either references to ones defined in the specification, or additional ones defined for/by the implementation.",
    )
    operation: Optional[List[CapabilityStatementRestResourceOperation]] = Field(
        default=None,
        description="Definition of an operation or a named query together with its parameters and their meaning and type.",
    )
    compartment: Optional[List[str]] = Field(
        default=None,
        description="An absolute URI which is a reference to the definition of a compartment that the system supports. The reference is to a CompartmentDefinition resource by its canonical URL .",
    )


class CapabilityStatementRestInteraction(MedplumFHIRBase):
    """A specification of restful operations supported by the system."""

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
    code: Literal["transaction", "batch", "search-system", "history-system"] = Field(
        default=...,
        description="A coded identifier of the operation, supported by the system.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Guidance specific to the implementation of this operation, such as limitations on the kind of transactions allowed, or information about system wide search is implemented.",
    )


class CapabilityStatementRestResource(MedplumFHIRBase):
    """A specification of the restful capabilities of the solution for a
    specific resource type.
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
    type: ResourceType = Field(
        default=..., description="A type of resource exposed via the restful interface."
    )
    profile: Optional[str] = Field(
        default=None,
        description="A specification of the profile that describes the solution's overall support for the resource, including any constraints on cardinality, bindings, lengths or other limitations. See further discussion in [Using Profiles](profiling.html#profile-uses).",
    )
    supported_profile: Optional[List[str]] = Field(
        default=None,
        alias="supportedProfile",
        description="A list of profiles that represent different use cases supported by the system. For a server, &quot;supported by the system&quot; means the system hosts/produces a set of resources that are conformant to a particular profile, and allows clients that use its services to search using this profile and to find appropriate data. For a client, it means the system will search by this profile and process data according to the guidance implicit in the profile. See further discussion in [Using Profiles](profiling.html#profile-uses).",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Additional information about the resource type used by the system.",
    )
    interaction: Optional[List[CapabilityStatementRestResourceInteraction]] = Field(
        default=None,
        description="Identifies a restful operation supported by the solution.",
    )
    versioning: Optional[Literal["no-version", "versioned", "versioned-update"]] = (
        Field(
            default=None,
            description="This field is set to no-version to specify that the system does not support (server) or use (client) versioning for this resource type. If this has some other value, the server must at least correctly track and populate the versionId meta-property on resources. If the value is 'versioned-update', then the server supports all the versioning features, including using e-tags for version integrity in the API.",
        )
    )
    read_history: Optional[bool] = Field(
        default=None,
        alias="readHistory",
        description="A flag for whether the server is able to return past versions as part of the vRead operation.",
    )
    update_create: Optional[bool] = Field(
        default=None,
        alias="updateCreate",
        description="A flag to indicate that the server allows or needs to allow the client to create new identities on the server (that is, the client PUTs to a location where there is no existing resource). Allowing this operation means that the server allows the client to create new identities on the server.",
    )
    conditional_create: Optional[bool] = Field(
        default=None,
        alias="conditionalCreate",
        description="A flag that indicates that the server supports conditional create.",
    )
    conditional_read: Optional[
        Literal["not-supported", "modified-since", "not-match", "full-support"]
    ] = Field(
        default=None,
        alias="conditionalRead",
        description="A code that indicates how the server supports conditional read.",
    )
    conditional_update: Optional[bool] = Field(
        default=None,
        alias="conditionalUpdate",
        description="A flag that indicates that the server supports conditional update.",
    )
    conditional_delete: Optional[Literal["not-supported", "single", "multiple"]] = (
        Field(
            default=None,
            alias="conditionalDelete",
            description="A code that indicates how the server supports conditional delete.",
        )
    )
    reference_policy: Optional[
        List[Literal["literal", "logical", "resolves", "enforced", "local"]]
    ] = Field(
        default=None,
        alias="referencePolicy",
        description="A set of flags that defines how references are supported.",
    )
    search_include: Optional[List[str]] = Field(
        default=None,
        alias="searchInclude",
        description="A list of _include values supported by the server.",
    )
    search_rev_include: Optional[List[str]] = Field(
        default=None,
        alias="searchRevInclude",
        description="A list of _revinclude (reverse include) values supported by the server.",
    )
    search_param: Optional[List[CapabilityStatementRestResourceSearchParam]] = Field(
        default=None,
        alias="searchParam",
        description="Search parameters for implementations to support and/or make use of - either references to ones defined in the specification, or additional ones defined for/by the implementation.",
    )
    operation: Optional[List[CapabilityStatementRestResourceOperation]] = Field(
        default=None,
        description="Definition of an operation or a named query together with its parameters and their meaning and type. Consult the definition of the operation for details about how to invoke the operation, and the parameters.",
    )


class CapabilityStatementRestResourceInteraction(MedplumFHIRBase):
    """Identifies a restful operation supported by the solution."""

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
    code: Literal[
        "read",
        "vread",
        "update",
        "patch",
        "delete",
        "history-instance",
        "history-type",
        "create",
        "search-type",
    ] = Field(
        default=...,
        description="Coded identifier of the operation, supported by the system resource.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Guidance specific to the implementation of this operation, such as 'delete is a logical delete' or 'updates are only allowed with version id' or 'creates permitted from pre-authorized certificates only'.",
    )


class CapabilityStatementRestResourceOperation(MedplumFHIRBase):
    """Definition of an operation or a named query together with its parameters
    and their meaning and type. Consult the definition of the operation for
    details about how to invoke the operation, and the parameters.
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
    name: str = Field(
        default=...,
        description="The name of the operation or query. For an operation, this is the name prefixed with $ and used in the URL. For a query, this is the name used in the _query parameter when the query is called.",
    )
    definition: str = Field(
        default=...,
        description="Where the formal definition can be found. If a server references the base definition of an Operation (i.e. from the specification itself such as ```http://hl7.org/fhir/OperationDefinition/ValueSet-expand```), that means it supports the full capabilities of the operation - e.g. both GET and POST invocation. If it only supports a subset, it must define its own custom [OperationDefinition](operationdefinition.html#) with a 'base' of the original OperationDefinition. The custom definition would describe the specific subset of functionality supported.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Documentation that describes anything special about the operation behavior, possibly detailing different behavior for system, type and instance-level invocation of the operation.",
    )


class CapabilityStatementRestResourceSearchParam(MedplumFHIRBase):
    """Search parameters for implementations to support and/or make use of -
    either references to ones defined in the specification, or additional
    ones defined for/by the implementation.
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
    name: str = Field(
        default=...,
        description="The name of the search parameter used in the interface.",
    )
    definition: Optional[str] = Field(
        default=None,
        description="An absolute URI that is a formal reference to where this parameter was first defined, so that a client can be confident of the meaning of the search parameter (a reference to [SearchParameter.url](searchparameter-definitions.html#SearchParameter.url)). This element SHALL be populated if the search parameter refers to a SearchParameter defined by the FHIR core specification or externally defined IGs.",
    )
    type: Literal[
        "number",
        "date",
        "string",
        "token",
        "reference",
        "composite",
        "quantity",
        "uri",
        "special",
    ] = Field(
        default=...,
        description="The type of value a search parameter refers to, and how the content is interpreted.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="This allows documentation of any distinct behaviors about how the search parameter is used. For example, text matching algorithms.",
    )


class CapabilityStatementRestSecurity(MedplumFHIRBase):
    """Information about security implementation from an interface perspective
    - what a client needs to know.
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
    cors: Optional[bool] = Field(
        default=None,
        description="Server adds CORS headers when responding to requests - this enables Javascript applications to use the server.",
    )
    service: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="Types of security services that are supported/required by the system.",
    )
    description: Optional[str] = Field(
        default=None, description="General description of how security works."
    )


class CapabilityStatementSoftware(MedplumFHIRBase):
    """Software that is covered by this capability statement. It is used when
    the capability statement describes the capabilities of a particular
    software version, independent of an installation.
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
    name: str = Field(default=..., description="Name the software is known by.")
    version: Optional[str] = Field(
        default=None,
        description="The version identifier for the software covered by this statement.",
    )
    release_date: Optional[str] = Field(
        default=None,
        alias="releaseDate",
        description="Date this version of the software was released.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CapabilityStatement", CapabilityStatement)
    register_model("CapabilityStatementDocument", CapabilityStatementDocument)
    register_model(
        "CapabilityStatementImplementation", CapabilityStatementImplementation
    )
    register_model("CapabilityStatementMessaging", CapabilityStatementMessaging)
    register_model(
        "CapabilityStatementMessagingEndpoint", CapabilityStatementMessagingEndpoint
    )
    register_model(
        "CapabilityStatementMessagingSupportedMessage",
        CapabilityStatementMessagingSupportedMessage,
    )
    register_model("CapabilityStatementRest", CapabilityStatementRest)
    register_model(
        "CapabilityStatementRestInteraction", CapabilityStatementRestInteraction
    )
    register_model("CapabilityStatementRestResource", CapabilityStatementRestResource)
    register_model(
        "CapabilityStatementRestResourceInteraction",
        CapabilityStatementRestResourceInteraction,
    )
    register_model(
        "CapabilityStatementRestResourceOperation",
        CapabilityStatementRestResourceOperation,
    )
    register_model(
        "CapabilityStatementRestResourceSearchParam",
        CapabilityStatementRestResourceSearchParam,
    )
    register_model("CapabilityStatementRestSecurity", CapabilityStatementRestSecurity)
    register_model("CapabilityStatementSoftware", CapabilityStatementSoftware)
