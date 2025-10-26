# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class TerminologyCapabilities(MedplumFHIRBase):
    """A TerminologyCapabilities resource documents a set of capabilities
    (behaviors) of a FHIR Terminology Server that may be used as a statement
    of actual server functionality or a statement of required or desired
    server implementation.
    """

    resource_type: Literal["TerminologyCapabilities"] = Field(
        default="TerminologyCapabilities",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    url: Optional[str] = Field(default=None, description="An absolute URI that is used to identify this terminology capabilities when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this terminology capabilities is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the terminology capabilities is stored on different servers.")
    version: Optional[str] = Field(default=None, description="The identifier that is used to identify this version of the terminology capabilities when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the terminology capabilities author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.")
    name: Optional[str] = Field(default=None, description="A natural language name identifying the terminology capabilities. This name should be usable as an identifier for the module by machine processing applications such as code generation.")
    title: Optional[str] = Field(default=None, description="A short, descriptive, user-friendly title for the terminology capabilities.")
    status: Literal['draft', 'active', 'retired', 'unknown'] = Field(default=..., description="The status of this terminology capabilities. Enables tracking the life-cycle of the content.")
    experimental: Optional[bool] = Field(default=None, description="A Boolean value to indicate that this terminology capabilities is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.")
    date: str = Field(default=..., description="The date (and optionally time) when the terminology capabilities was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the terminology capabilities changes.")
    publisher: Optional[str] = Field(default=None, description="The name of the organization or individual that published the terminology capabilities.")
    contact: Optional[List[ContactDetail]] = Field(default=None, description="Contact details to assist a user in finding and communicating with the publisher.")
    description: Optional[str] = Field(default=None, description="A free text natural language description of the terminology capabilities from a consumer's perspective. Typically, this is used when the capability statement describes a desired rather than an actual solution, for example as a formal expression of requirements as part of an RFP.")
    use_context: Optional[List[UsageContext]] = Field(default=None, alias="useContext", description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate terminology capabilities instances.")
    jurisdiction: Optional[List[CodeableConcept]] = Field(default=None, description="A legal or geographic region in which the terminology capabilities is intended to be used.")
    purpose: Optional[str] = Field(default=None, description="Explanation of why this terminology capabilities is needed and why it has been designed as it has.")
    copyright: Optional[str] = Field(default=None, description="A copyright statement relating to the terminology capabilities and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the terminology capabilities.")
    kind: Literal['instance', 'capability', 'requirements'] = Field(default=..., description="The way that this statement is intended to be used, to describe an actual running instance of software, a particular product (kind, not instance of software) or a class of implementation (e.g. a desired purchase).")
    software: Optional[TerminologyCapabilitiesSoftware] = Field(default=None, description="Software that is covered by this terminology capability statement. It is used when the statement describes the capabilities of a particular software version, independent of an installation.")
    implementation: Optional[TerminologyCapabilitiesImplementation] = Field(default=None, description="Identifies a specific implementation instance that is described by the terminology capability statement - i.e. a particular installation, rather than the capabilities of a software program.")
    locked_date: Optional[bool] = Field(default=None, alias="lockedDate", description="Whether the server supports lockedDate.")
    code_system: Optional[List[TerminologyCapabilitiesCodeSystem]] = Field(default=None, alias="codeSystem", description="Identifies a code system that is supported by the server. If there is a no code system URL, then this declares the general assumptions a client can make about support for any CodeSystem resource.")
    expansion: Optional[TerminologyCapabilitiesExpansion] = Field(default=None, description="Information about the [ValueSet/$expand](valueset-operation-expand.html) operation.")
    code_search: Optional[Literal['explicit', 'all']] = Field(default=None, alias="codeSearch", description="The degree to which the server supports the code search parameter on ValueSet, if it is supported.")
    validate_code: Optional[TerminologyCapabilitiesValidateCode] = Field(default=None, alias="validateCode", description="Information about the [ValueSet/$validate-code](valueset-operation-validate-code.html) operation.")
    translation: Optional[TerminologyCapabilitiesTranslation] = Field(default=None, description="Information about the [ConceptMap/$translate](conceptmap-operation-translate.html) operation.")
    closure: Optional[TerminologyCapabilitiesClosure] = Field(default=None, description="Whether the $closure operation is supported.")


class TerminologyCapabilitiesClosure(MedplumFHIRBase):
    """Whether the $closure operation is supported."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    translation: Optional[bool] = Field(default=None, description="If cross-system closure is supported.")


class TerminologyCapabilitiesCodeSystem(MedplumFHIRBase):
    """Identifies a code system that is supported by the server. If there is a
    no code system URL, then this declares the general assumptions a client
    can make about support for any CodeSystem resource.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    uri: Optional[str] = Field(default=None, description="URI for the Code System.")
    version: Optional[List[TerminologyCapabilitiesCodeSystemVersion]] = Field(default=None, description="For the code system, a list of versions that are supported by the server.")
    subsumption: Optional[bool] = Field(default=None, description="True if subsumption is supported for this version of the code system.")


class TerminologyCapabilitiesCodeSystemVersion(MedplumFHIRBase):
    """For the code system, a list of versions that are supported by the server."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[str] = Field(default=None, description="For version-less code systems, there should be a single version with no identifier.")
    is_default: Optional[bool] = Field(default=None, alias="isDefault", description="If this is the default version for this code system.")
    compositional: Optional[bool] = Field(default=None, description="If the compositional grammar defined by the code system is supported.")
    language: Optional[List[str]] = Field(default=None, description="Language Displays supported.")
    filter: Optional[List[TerminologyCapabilitiesCodeSystemVersionFilter]] = Field(default=None, description="Filter Properties supported.")
    property: Optional[List[str]] = Field(default=None, description="Properties supported for $lookup.")


class TerminologyCapabilitiesCodeSystemVersionFilter(MedplumFHIRBase):
    """Filter Properties supported."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: str = Field(default=..., description="Code of the property supported.")
    op: List[str] = Field(default=..., description="Operations supported for the property.")


class TerminologyCapabilitiesExpansion(MedplumFHIRBase):
    """Information about the [ValueSet/$expand](valueset-operation-expand.html) operation."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    hierarchical: Optional[bool] = Field(default=None, description="Whether the server can return nested value sets.")
    paging: Optional[bool] = Field(default=None, description="Whether the server supports paging on expansion.")
    incomplete: Optional[bool] = Field(default=None, description="Allow request for incomplete expansions?")
    parameter: Optional[List[TerminologyCapabilitiesExpansionParameter]] = Field(default=None, description="Supported expansion parameter.")
    text_filter: Optional[str] = Field(default=None, alias="textFilter", description="Documentation about text searching works.")


class TerminologyCapabilitiesExpansionParameter(MedplumFHIRBase):
    """Supported expansion parameter."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="Expansion Parameter name.")
    documentation: Optional[str] = Field(default=None, description="Description of support for parameter.")


class TerminologyCapabilitiesImplementation(MedplumFHIRBase):
    """Identifies a specific implementation instance that is described by the
    terminology capability statement - i.e. a particular installation,
    rather than the capabilities of a software program.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    description: str = Field(default=..., description="Information about the specific installation that this terminology capability statement relates to.")
    url: Optional[str] = Field(default=None, description="An absolute base URL for the implementation.")


class TerminologyCapabilitiesSoftware(MedplumFHIRBase):
    """Software that is covered by this terminology capability statement. It is
    used when the statement describes the capabilities of a particular
    software version, independent of an installation.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="Name the software is known by.")
    version: Optional[str] = Field(default=None, description="The version identifier for the software covered by this statement.")


class TerminologyCapabilitiesTranslation(MedplumFHIRBase):
    """Information about the
    [ConceptMap/$translate](conceptmap-operation-translate.html) operation.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    needs_map: bool = Field(default=..., alias="needsMap", description="Whether the client must identify the map.")


class TerminologyCapabilitiesValidateCode(MedplumFHIRBase):
    """Information about the
    [ValueSet/$validate-code](valueset-operation-validate-code.html)
    operation.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    translations: bool = Field(default=..., description="Whether translations are validated.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("TerminologyCapabilities", TerminologyCapabilities)
    register_model("TerminologyCapabilitiesClosure", TerminologyCapabilitiesClosure)
    register_model("TerminologyCapabilitiesCodeSystem", TerminologyCapabilitiesCodeSystem)
    register_model("TerminologyCapabilitiesCodeSystemVersion", TerminologyCapabilitiesCodeSystemVersion)
    register_model("TerminologyCapabilitiesCodeSystemVersionFilter", TerminologyCapabilitiesCodeSystemVersionFilter)
    register_model("TerminologyCapabilitiesExpansion", TerminologyCapabilitiesExpansion)
    register_model("TerminologyCapabilitiesExpansionParameter", TerminologyCapabilitiesExpansionParameter)
    register_model("TerminologyCapabilitiesImplementation", TerminologyCapabilitiesImplementation)
    register_model("TerminologyCapabilitiesSoftware", TerminologyCapabilitiesSoftware)
    register_model("TerminologyCapabilitiesTranslation", TerminologyCapabilitiesTranslation)
    register_model("TerminologyCapabilitiesValidateCode", TerminologyCapabilitiesValidateCode)
