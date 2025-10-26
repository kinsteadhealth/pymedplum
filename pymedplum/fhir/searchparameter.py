# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class SearchParameter(MedplumFHIRBase):
    """A search parameter that defines a named search item that can be used to
    search/filter on a resource.
    """

    resource_type: Literal["SearchParameter"] = Field(
        default="SearchParameter",
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
    url: str = Field(default=..., description="An absolute URI that is used to identify this search parameter when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this search parameter is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the search parameter is stored on different servers.")
    version: Optional[str] = Field(default=None, description="The identifier that is used to identify this version of the search parameter when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the search parameter author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.")
    name: str = Field(default=..., description="A natural language name identifying the search parameter. This name should be usable as an identifier for the module by machine processing applications such as code generation.")
    derived_from: Optional[str] = Field(default=None, alias="derivedFrom", description="Where this search parameter is originally defined. If a derivedFrom is provided, then the details in the search parameter must be consistent with the definition from which it is defined. i.e. the parameter should have the same meaning, and (usually) the functionality should be a proper subset of the underlying search parameter.")
    status: Literal['draft', 'active', 'retired', 'unknown'] = Field(default=..., description="The status of this search parameter. Enables tracking the life-cycle of the content.")
    experimental: Optional[bool] = Field(default=None, description="A Boolean value to indicate that this search parameter is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.")
    date: Optional[str] = Field(default=None, description="The date (and optionally time) when the search parameter was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the search parameter changes.")
    publisher: Optional[str] = Field(default=None, description="The name of the organization or individual that published the search parameter.")
    contact: Optional[List[ContactDetail]] = Field(default=None, description="Contact details to assist a user in finding and communicating with the publisher.")
    description: str = Field(default=..., description="And how it used.")
    use_context: Optional[List[UsageContext]] = Field(default=None, alias="useContext", description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate search parameter instances.")
    jurisdiction: Optional[List[CodeableConcept]] = Field(default=None, description="A legal or geographic region in which the search parameter is intended to be used.")
    purpose: Optional[str] = Field(default=None, description="Explanation of why this search parameter is needed and why it has been designed as it has.")
    code: str = Field(default=..., description="The code used in the URL or the parameter name in a parameters resource for this search parameter.")
    base: List[ResourceType] = Field(default=..., description="The base resource type(s) that this search parameter can be used against.")
    type: Literal['number', 'date', 'string', 'token', 'reference', 'composite', 'quantity', 'uri', 'special'] = Field(default=..., description="The type of value that a search parameter may contain, and how the content is interpreted.")
    expression: Optional[str] = Field(default=None, description="A FHIRPath expression that returns a set of elements for the search parameter.")
    xpath: Optional[str] = Field(default=None, description="An XPath expression that returns a set of elements for the search parameter.")
    xpath_usage: Optional[Literal['normal', 'phonetic', 'nearby', 'distance', 'other']] = Field(default=None, alias="xpathUsage", description="How the search parameter relates to the set of elements returned by evaluating the xpath query.")
    target: Optional[List[ResourceType]] = Field(default=None, description="Types of resource (if a resource is referenced).")
    multiple_or: Optional[bool] = Field(default=None, alias="multipleOr", description="Whether multiple values are allowed for each time the parameter exists. Values are separated by commas, and the parameter matches if any of the values match.")
    multiple_and: Optional[bool] = Field(default=None, alias="multipleAnd", description="Whether multiple parameters are allowed - e.g. more than one parameter with the same name. The search matches if all the parameters match.")
    comparator: Optional[List[Literal['eq', 'ne', 'gt', 'lt', 'ge', 'le', 'sa', 'eb', 'ap']]] = Field(default=None, description="Comparators supported for the search parameter.")
    modifier: Optional[List[Literal['missing', 'exact', 'contains', 'not', 'text', 'in', 'not-in', 'below', 'above', 'type', 'identifier', 'ofType']]] = Field(default=None, description="A modifier supported for the search parameter.")
    chain: Optional[List[str]] = Field(default=None, description="Contains the names of any search parameters which may be chained to the containing search parameter. Chained parameters may be added to search parameters of type reference and specify that resources will only be returned if they contain a reference to a resource which matches the chained parameter value. Values for this field should be drawn from SearchParameter.code for a parameter on the target resource type.")
    component: Optional[List[SearchParameterComponent]] = Field(default=None, description="Used to define the parts of a composite search parameter.")


class SearchParameterComponent(MedplumFHIRBase):
    """Used to define the parts of a composite search parameter."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    definition: str = Field(default=..., description="The definition of the search parameter that describes this part.")
    expression: str = Field(default=..., description="A sub-expression that defines how to extract values for this component from the output of the main SearchParameter.expression.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SearchParameter", SearchParameter)
    register_model("SearchParameterComponent", SearchParameterComponent)
