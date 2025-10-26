# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class OperationDefinition(MedplumFHIRBase):
    """A formal computable definition of an operation (on the RESTful
    interface) or a named query (using the search interaction).
    """

    resource_type: Literal["OperationDefinition"] = Field(
        default="OperationDefinition",
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
    url: Optional[str] = Field(default=None, description="An absolute URI that is used to identify this operation definition when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this operation definition is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the operation definition is stored on different servers.")
    version: Optional[str] = Field(default=None, description="The identifier that is used to identify this version of the operation definition when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the operation definition author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.")
    name: str = Field(default=..., description="A natural language name identifying the operation definition. This name should be usable as an identifier for the module by machine processing applications such as code generation.")
    title: Optional[str] = Field(default=None, description="A short, descriptive, user-friendly title for the operation definition.")
    status: Literal['draft', 'active', 'retired', 'unknown'] = Field(default=..., description="The status of this operation definition. Enables tracking the life-cycle of the content.")
    kind: Literal['operation', 'query'] = Field(default=..., description="Whether this is an operation or a named query.")
    experimental: Optional[bool] = Field(default=None, description="A Boolean value to indicate that this operation definition is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.")
    date: Optional[str] = Field(default=None, description="The date (and optionally time) when the operation definition was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the operation definition changes.")
    publisher: Optional[str] = Field(default=None, description="The name of the organization or individual that published the operation definition.")
    contact: Optional[List[ContactDetail]] = Field(default=None, description="Contact details to assist a user in finding and communicating with the publisher.")
    description: Optional[str] = Field(default=None, description="A free text natural language description of the operation definition from a consumer's perspective.")
    use_context: Optional[List[UsageContext]] = Field(default=None, alias="useContext", description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate operation definition instances.")
    jurisdiction: Optional[List[CodeableConcept]] = Field(default=None, description="A legal or geographic region in which the operation definition is intended to be used.")
    purpose: Optional[str] = Field(default=None, description="Explanation of why this operation definition is needed and why it has been designed as it has.")
    affects_state: Optional[bool] = Field(default=None, alias="affectsState", description="Whether the operation affects state. Side effects such as producing audit trail entries do not count as 'affecting state'.")
    code: str = Field(default=..., description="The name used to invoke the operation.")
    comment: Optional[str] = Field(default=None, description="Additional information about how to use this operation or named query.")
    base: Optional[str] = Field(default=None, description="Indicates that this operation definition is a constraining profile on the base.")
    resource: Optional[List[ResourceType]] = Field(default=None, description="The types on which this operation can be executed.")
    system: bool = Field(default=..., description="Indicates whether this operation or named query can be invoked at the system level (e.g. without needing to choose a resource type for the context).")
    type: bool = Field(default=..., description="Indicates whether this operation or named query can be invoked at the resource type level for any given resource type level (e.g. without needing to choose a specific resource id for the context).")
    instance: bool = Field(default=..., description="Indicates whether this operation can be invoked on a particular instance of one of the given types.")
    input_profile: Optional[str] = Field(default=None, alias="inputProfile", description="Additional validation information for the in parameters - a single profile that covers all the parameters. The profile is a constraint on the parameters resource as a whole.")
    output_profile: Optional[str] = Field(default=None, alias="outputProfile", description="Additional validation information for the out parameters - a single profile that covers all the parameters. The profile is a constraint on the parameters resource.")
    parameter: Optional[List[OperationDefinitionParameter]] = Field(default=None, description="The parameters for the operation/query.")
    overload: Optional[List[OperationDefinitionOverload]] = Field(default=None, description="Defines an appropriate combination of parameters to use when invoking this operation, to help code generators when generating overloaded parameter sets for this operation.")


class OperationDefinitionOverload(MedplumFHIRBase):
    """Defines an appropriate combination of parameters to use when invoking
    this operation, to help code generators when generating overloaded
    parameter sets for this operation.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    parameter_name: Optional[List[str]] = Field(default=None, alias="parameterName", description="Name of parameter to include in overload.")
    comment: Optional[str] = Field(default=None, description="Comments to go on overload.")


class OperationDefinitionParameter(MedplumFHIRBase):
    """The parameters for the operation/query."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="The name of used to identify the parameter.")
    use: Literal['in', 'out'] = Field(default=..., description="Whether this is an input or an output parameter.")
    min: Union[int, float] = Field(default=..., description="The minimum number of times this parameter SHALL appear in the request or response.")
    max: str = Field(default=..., description="The maximum number of times this element is permitted to appear in the request or response.")
    documentation: Optional[str] = Field(default=None, description="Describes the meaning or use of this parameter.")
    type: Optional[str] = Field(default=None, description="The type for this parameter.")
    target_profile: Optional[List[str]] = Field(default=None, alias="targetProfile", description="Used when the type is &quot;Reference&quot; or &quot;canonical&quot;, and identifies a profile structure or implementation Guide that applies to the target of the reference this parameter refers to. If any profiles are specified, then the content must conform to at least one of them. The URL can be a local reference - to a contained StructureDefinition, or a reference to another StructureDefinition or Implementation Guide by a canonical URL. When an implementation guide is specified, the target resource SHALL conform to at least one profile defined in the implementation guide.")
    search_type: Optional[Literal['number', 'date', 'string', 'token', 'reference', 'composite', 'quantity', 'uri', 'special']] = Field(default=None, alias="searchType", description="How the parameter is understood as a search parameter. This is only used if the parameter type is 'string'.")
    binding: Optional[OperationDefinitionParameterBinding] = Field(default=None, description="Binds to a value set if this parameter is coded (code, Coding, CodeableConcept).")
    referenced_from: Optional[List[OperationDefinitionParameterReferencedFrom]] = Field(default=None, alias="referencedFrom", description="Identifies other resource parameters within the operation invocation that are expected to resolve to this resource.")
    part: Optional[List[OperationDefinitionParameter]] = Field(default=None, description="The parts of a nested Parameter.")


class OperationDefinitionParameterBinding(MedplumFHIRBase):
    """Binds to a value set if this parameter is coded (code, Coding, CodeableConcept)."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    strength: Literal['required', 'extensible', 'preferred', 'example'] = Field(default=..., description="Indicates the degree of conformance expectations associated with this binding - that is, the degree to which the provided value set must be adhered to in the instances.")
    value_set: str = Field(default=..., alias="valueSet", description="Points to the value set or external definition (e.g. implicit value set) that identifies the set of codes to be used.")


class OperationDefinitionParameterReferencedFrom(MedplumFHIRBase):
    """Identifies other resource parameters within the operation invocation
    that are expected to resolve to this resource.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    source: str = Field(default=..., description="The name of the parameter or dot-separated path of parameter names pointing to the resource parameter that is expected to contain a reference to this resource.")
    source_id: Optional[str] = Field(default=None, alias="sourceId", description="The id of the element in the referencing resource that is expected to resolve to this resource.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("OperationDefinition", OperationDefinition)
    register_model("OperationDefinitionOverload", OperationDefinitionOverload)
    register_model("OperationDefinitionParameter", OperationDefinitionParameter)
    register_model("OperationDefinitionParameterBinding", OperationDefinitionParameterBinding)
    register_model("OperationDefinitionParameterReferencedFrom", OperationDefinitionParameterReferencedFrom)
