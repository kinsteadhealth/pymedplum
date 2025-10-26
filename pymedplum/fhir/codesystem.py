# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CodeSystem(MedplumFHIRBase):
    """The CodeSystem resource is used to declare the existence of and describe
    a code system or code system supplement and its key properties, and
    optionally define a part or all of its content.
    """

    resource_type: Literal["CodeSystem"] = Field(
        default="CodeSystem", alias="resourceType"
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
        description="An absolute URI that is used to identify this code system when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this code system is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the code system is stored on different servers. This is used in [Coding](datatypes.html#Coding).system.",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="A formal identifier that is used to identify this code system when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the code system when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the code system author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. This is used in [Coding](datatypes.html#Coding).version.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A natural language name identifying the code system. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the code system.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The date (and optionally time) when the code system resource was created or revised.",
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this code system is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the code system was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the code system changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the code system.",
    )
    contact: Optional[List[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the code system from a consumer's perspective.",
    )
    use_context: Optional[List[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate code system instances.",
    )
    jurisdiction: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the code system is intended to be used.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Explanation of why this code system is needed and why it has been designed as it has.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the code system and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the code system.",
    )
    case_sensitive: Optional[bool] = Field(
        default=None,
        alias="caseSensitive",
        description="If code comparison is case sensitive when codes within this system are compared to each other.",
    )
    value_set: Optional[str] = Field(
        default=None,
        alias="valueSet",
        description="Canonical reference to the value set that contains the entire code system.",
    )
    hierarchy_meaning: Optional[
        Literal["grouped-by", "is-a", "part-of", "classified-with"]
    ] = Field(
        default=None,
        alias="hierarchyMeaning",
        description="The meaning of the hierarchy of concepts as represented in this resource.",
    )
    compositional: Optional[bool] = Field(
        default=None,
        description="The code system defines a compositional (post-coordination) grammar.",
    )
    version_needed: Optional[bool] = Field(
        default=None,
        alias="versionNeeded",
        description="This flag is used to signify that the code system does not commit to concept permanence across versions. If true, a version must be specified when referencing this code system.",
    )
    content: Literal["not-present", "example", "fragment", "complete", "supplement"] = (
        Field(
            default=...,
            description="The extent of the content of the code system (the concepts and codes it defines) are represented in this resource instance.",
        )
    )
    supplements: Optional[str] = Field(
        default=None,
        description="The canonical URL of the code system that this code system supplement is adding designations and properties to.",
    )
    count: Optional[Union[int, float]] = Field(
        default=None,
        description="The total number of concepts defined by the code system. Where the code system has a compositional grammar, the basis of this count is defined by the system steward.",
    )
    filter: Optional[List[CodeSystemFilter]] = Field(
        default=None,
        description="A filter that can be used in a value set compose statement when selecting concepts using a filter.",
    )
    property: Optional[List[CodeSystemProperty]] = Field(
        default=None,
        description="A property defines an additional slot through which additional information can be provided about a concept.",
    )
    concept: Optional[List[CodeSystemConcept]] = Field(
        default=None,
        description="Concepts that are in the code system. The concept definitions are inherently hierarchical, but the definitions must be consulted to determine what the meanings of the hierarchical relationships are.",
    )


class CodeSystemConcept(MedplumFHIRBase):
    """Concepts that are in the code system. The concept definitions are
    inherently hierarchical, but the definitions must be consulted to
    determine what the meanings of the hierarchical relationships are.
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
    code: str = Field(
        default=...,
        description="A code - a text symbol - that uniquely identifies the concept within the code system.",
    )
    display: Optional[str] = Field(
        default=None,
        description="A human readable string that is the recommended default way to present this concept to a user.",
    )
    definition: Optional[str] = Field(
        default=None,
        description="The formal definition of the concept. The code system resource does not make formal definitions required, because of the prevalence of legacy systems. However, they are highly recommended, as without them there is no formal meaning associated with the concept.",
    )
    designation: Optional[List[CodeSystemConceptDesignation]] = Field(
        default=None,
        description="Additional representations for the concept - other languages, aliases, specialized purposes, used for particular purposes, etc.",
    )
    property: Optional[List[CodeSystemConceptProperty]] = Field(
        default=None, description="A property value for this concept."
    )
    concept: Optional[List[CodeSystemConcept]] = Field(
        default=None,
        description="Defines children of a concept to produce a hierarchy of concepts. The nature of the relationships is variable (is-a/contains/categorizes) - see hierarchyMeaning.",
    )


class CodeSystemConceptDesignation(MedplumFHIRBase):
    """Additional representations for the concept - other languages, aliases,
    specialized purposes, used for particular purposes, etc.
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
    language: Optional[str] = Field(
        default=None, description="The language this designation is defined for."
    )
    use: Optional[Coding] = Field(
        default=None,
        description="A code that details how this designation would be used.",
    )
    value: str = Field(default=..., description="The text value for this designation.")


class CodeSystemConceptProperty(MedplumFHIRBase):
    """A property value for this concept."""

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
    code: str = Field(
        default=...,
        description="A code that is a reference to CodeSystem.property.code.",
    )
    value_code: Optional[str] = Field(
        default=None, alias="valueCode", description="The value of this property."
    )
    value_coding: Optional[Coding] = Field(
        default=None, alias="valueCoding", description="The value of this property."
    )
    value_string: Optional[str] = Field(
        default=None, alias="valueString", description="The value of this property."
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None, alias="valueInteger", description="The value of this property."
    )
    value_boolean: Optional[bool] = Field(
        default=None, alias="valueBoolean", description="The value of this property."
    )
    value_date_time: Optional[str] = Field(
        default=None, alias="valueDateTime", description="The value of this property."
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None, alias="valueDecimal", description="The value of this property."
    )


class CodeSystemFilter(MedplumFHIRBase):
    """A filter that can be used in a value set compose statement when
    selecting concepts using a filter.
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
    code: str = Field(
        default=...,
        description="The code that identifies this filter when it is used as a filter in [ValueSet](valueset.html#).compose.include.filter.",
    )
    description: Optional[str] = Field(
        default=None, description="A description of how or why the filter is used."
    )
    operator: List[
        Literal[
            "=",
            "is-a",
            "descendent-of",
            "is-not-a",
            "regex",
            "in",
            "not-in",
            "generalizes",
            "exists",
        ]
    ] = Field(
        default=..., description="A list of operators that can be used with the filter."
    )
    value: str = Field(
        default=...,
        description="A description of what the value for the filter should be.",
    )


class CodeSystemProperty(MedplumFHIRBase):
    """A property defines an additional slot through which additional
    information can be provided about a concept.
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
    code: str = Field(
        default=...,
        description="A code that is used to identify the property. The code is used internally (in CodeSystem.concept.property.code) and also externally, such as in property filters.",
    )
    uri: Optional[str] = Field(
        default=None,
        description="Reference to the formal meaning of the property. One possible source of meaning is the [Concept Properties](codesystem-concept-properties.html) code system.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A description of the property- why it is defined, and how its value might be used.",
    )
    type: Literal[
        "code", "Coding", "string", "integer", "boolean", "dateTime", "decimal"
    ] = Field(
        default=...,
        description="The type of the property value. Properties of type &quot;code&quot; contain a code defined by the code system (e.g. a reference to another defined concept).",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CodeSystem", CodeSystem)
    register_model("CodeSystemConcept", CodeSystemConcept)
    register_model("CodeSystemConceptDesignation", CodeSystemConceptDesignation)
    register_model("CodeSystemConceptProperty", CodeSystemConceptProperty)
    register_model("CodeSystemFilter", CodeSystemFilter)
    register_model("CodeSystemProperty", CodeSystemProperty)
