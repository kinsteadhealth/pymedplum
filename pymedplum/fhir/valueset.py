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
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.usagecontext import UsageContext


class ValueSet(MedplumFHIRBase):
    """A ValueSet resource instance specifies a set of codes drawn from one or
    more code systems, intended for use in a particular context. Value sets
    link between [[[CodeSystem]]] definitions and their use in [coded
    elements](terminologies.html).
    """

    resource_type: Literal["ValueSet"] = Field(default="ValueSet", alias="resourceType")

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
        description="An absolute URI that is used to identify this value set when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this value set is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the value set is stored on different servers.",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="A formal identifier that is used to identify this value set when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: str | None = Field(
        default=None,
        description="The identifier that is used to identify this version of the value set when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the value set author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: str | None = Field(
        default=None,
        description="A natural language name identifying the value set. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: str | None = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the value set.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this value set. Enables tracking the life-cycle of the content. The status of the value set applies to the value set definition (ValueSet.compose) and the associated ValueSet metadata. Expansions do not have a state.",
    )
    experimental: bool | None = Field(
        default=None,
        description="A Boolean value to indicate that this value set is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: str | None = Field(
        default=None,
        description="The date (and optionally time) when the value set was created or revised (e.g. the 'content logical definition').",
    )
    publisher: str | None = Field(
        default=None,
        description="The name of the organization or individual that published the value set.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: str | None = Field(
        default=None,
        description="A free text natural language description of the value set from a consumer's perspective. The textual description specifies the span of meanings for concepts to be included within the Value Set Expansion, and also may specify the intended use and limitations of the Value Set.",
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate value set instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None,
        description="A legal or geographic region in which the value set is intended to be used.",
    )
    immutable: bool | None = Field(
        default=None,
        description="If this is set to 'true', then no new versions of the content logical definition can be created. Note: Other metadata might still change.",
    )
    purpose: str | None = Field(
        default=None,
        description="Explanation of why this value set is needed and why it has been designed as it has.",
    )
    copyright: str | None = Field(
        default=None,
        description="A copyright statement relating to the value set and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the value set.",
    )
    compose: ValueSetCompose | None = Field(
        default=None,
        description="A set of criteria that define the contents of the value set by including or excluding codes selected from the specified code system(s) that the value set draws from. This is also known as the Content Logical Definition (CLD).",
    )
    expansion: ValueSetExpansion | None = Field(
        default=None,
        description="A value set can also be &quot;expanded&quot;, where the value set is turned into a simple collection of enumerated codes. This element holds the expansion, if it has been performed.",
    )


class ValueSetCompose(MedplumFHIRBase):
    """A set of criteria that define the contents of the value set by including
    or excluding codes selected from the specified code system(s) that the
    value set draws from. This is also known as the Content Logical
    Definition (CLD).
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
    locked_date: str | None = Field(
        default=None,
        alias="lockedDate",
        description="The Locked Date is the effective date that is used to determine the version of all referenced Code Systems and Value Set Definitions included in the compose that are not already tied to a specific version.",
    )
    inactive: bool | None = Field(
        default=None,
        description="Whether inactive codes - codes that are not approved for current use - are in the value set. If inactive = true, inactive codes are to be included in the expansion, if inactive = false, the inactive codes will not be included in the expansion. If absent, the behavior is determined by the implementation, or by the applicable $expand parameters (but generally, inactive codes would be expected to be included).",
    )
    include: list[ValueSetComposeInclude] = Field(
        default=...,
        description="Include one or more codes from a code system or other value set(s).",
    )
    exclude: list[ValueSetComposeInclude] | None = Field(
        default=None,
        description="Exclude one or more codes from the value set based on code system filters and/or other value sets.",
    )


class ValueSetComposeInclude(MedplumFHIRBase):
    """Include one or more codes from a code system or other value set(s)."""

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
    system: str | None = Field(
        default=None,
        description="An absolute URI which is the code system from which the selected codes come from.",
    )
    version: str | None = Field(
        default=None,
        description="The version of the code system that the codes are selected from, or the special version '*' for all versions.",
    )
    concept: list[ValueSetComposeIncludeConcept] | None = Field(
        default=None, description="Specifies a concept to be included or excluded."
    )
    filter: list[ValueSetComposeIncludeFilter] | None = Field(
        default=None,
        description="Select concepts by specify a matching criterion based on the properties (including relationships) defined by the system, or on filters defined by the system. If multiple filters are specified, they SHALL all be true.",
    )
    value_set: list[str] | None = Field(
        default=None,
        alias="valueSet",
        description="Selects the concepts found in this value set (based on its value set definition). This is an absolute URI that is a reference to ValueSet.url. If multiple value sets are specified this includes the union of the contents of all of the referenced value sets.",
    )


class ValueSetComposeIncludeConcept(MedplumFHIRBase):
    """Specifies a concept to be included or excluded."""

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
    code: str = Field(
        default=...,
        description="Specifies a code for the concept to be included or excluded.",
    )
    display: str | None = Field(
        default=None,
        description="The text to display to the user for this concept in the context of this valueset. If no display is provided, then applications using the value set use the display specified for the code by the system.",
    )
    designation: list[ValueSetComposeIncludeConceptDesignation] | None = Field(
        default=None,
        description="Additional representations for this concept when used in this value set - other languages, aliases, specialized purposes, used for particular purposes, etc.",
    )


class ValueSetComposeIncludeConceptDesignation(MedplumFHIRBase):
    """Additional representations for this concept when used in this value set
    - other languages, aliases, specialized purposes, used for particular
    purposes, etc.
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
    language: str | None = Field(
        default=None, description="The language this designation is defined for."
    )
    use: Coding | None = Field(
        default=None,
        description="A code that represents types of uses of designations.",
    )
    value: str = Field(default=..., description="The text value for this designation.")


class ValueSetComposeIncludeFilter(MedplumFHIRBase):
    """Select concepts by specify a matching criterion based on the properties
    (including relationships) defined by the system, or on filters defined
    by the system. If multiple filters are specified, they SHALL all be
    true.
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
    property: str = Field(
        default=...,
        description="A code that identifies a property or a filter defined in the code system.",
    )
    op: Literal[
        "=",
        "is-a",
        "descendent-of",
        "is-not-a",
        "regex",
        "in",
        "not-in",
        "generalizes",
        "exists",
    ] = Field(
        default=...,
        description="The kind of operation to perform as a part of the filter criteria.",
    )
    value: str = Field(
        default=...,
        description="The match value may be either a code defined by the system, or a string value, which is a regex match on the literal string of the property value (if the filter represents a property defined in CodeSystem) or of the system filter value (if the filter represents a filter defined in CodeSystem) when the operation is 'regex', or one of the values (true and false), when the operation is 'exists'.",
    )


class ValueSetExpansion(MedplumFHIRBase):
    """A value set can also be &quot;expanded&quot;, where the value set is
    turned into a simple collection of enumerated codes. This element holds
    the expansion, if it has been performed.
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
    identifier: str | None = Field(
        default=None,
        description="An identifier that uniquely identifies this expansion of the valueset, based on a unique combination of the provided parameters, the system default parameters, and the underlying system code system versions etc. Systems may re-use the same identifier as long as those factors remain the same, and the expansion is the same, but are not required to do so. This is a business identifier.",
    )
    timestamp: str = Field(
        default=...,
        description="The time at which the expansion was produced by the expanding system.",
    )
    total: int | float | None = Field(
        default=None,
        description="The total number of concepts in the expansion. If the number of concept nodes in this resource is less than the stated number, then the server can return more using the offset parameter.",
    )
    offset: int | float | None = Field(
        default=None,
        description="If paging is being used, the offset at which this resource starts. I.e. this resource is a partial view into the expansion. If paging is not being used, this element SHALL NOT be present.",
    )
    parameter: list[ValueSetExpansionParameter] | None = Field(
        default=None,
        description="A parameter that controlled the expansion process. These parameters may be used by users of expanded value sets to check whether the expansion is suitable for a particular purpose, or to pick the correct expansion.",
    )
    contains: list[ValueSetExpansionContains] | None = Field(
        default=None,
        description="The codes that are contained in the value set expansion.",
    )


class ValueSetExpansionContains(MedplumFHIRBase):
    """The codes that are contained in the value set expansion."""

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
    system: str | None = Field(
        default=None,
        description="An absolute URI which is the code system in which the code for this item in the expansion is defined.",
    )
    abstract: bool | None = Field(
        default=None,
        description="If true, this entry is included in the expansion for navigational purposes, and the user cannot select the code directly as a proper value.",
    )
    inactive: bool | None = Field(
        default=None,
        description="If the concept is inactive in the code system that defines it. Inactive codes are those that are no longer to be used, but are maintained by the code system for understanding legacy data. It might not be known or specified whether an concept is inactive (and it may depend on the context of use).",
    )
    version: str | None = Field(
        default=None,
        description="The version of the code system from this code was taken. Note that a well-maintained code system does not need the version reported, because the meaning of codes is consistent across versions. However this cannot consistently be assured, and when the meaning is not guaranteed to be consistent, the version SHOULD be exchanged.",
    )
    code: str | None = Field(
        default=None,
        description="The code for this item in the expansion hierarchy. If this code is missing the entry in the hierarchy is a place holder (abstract) and does not represent a valid code in the value set.",
    )
    display: str | None = Field(
        default=None,
        description="The recommended display for this item in the expansion.",
    )
    designation: list[ValueSetComposeIncludeConceptDesignation] | None = Field(
        default=None,
        description="Additional representations for this item - other languages, aliases, specialized purposes, used for particular purposes, etc. These are relevant when the conditions of the expansion do not fix to a single correct representation.",
    )
    contains: list[ValueSetExpansionContains] | None = Field(
        default=None,
        description="Other codes and entries contained under this entry in the hierarchy.",
    )


class ValueSetExpansionParameter(MedplumFHIRBase):
    """A parameter that controlled the expansion process. These parameters may
    be used by users of expanded value sets to check whether the expansion
    is suitable for a particular purpose, or to pick the correct expansion.
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
    name: str = Field(
        default=...,
        description="Name of the input parameter to the $expand operation; may be a server-assigned name for additional default or other server-supplied parameters used to control the expansion process.",
    )
    value_string: str | None = Field(
        default=None, alias="valueString", description="The value of the parameter."
    )
    value_boolean: bool | None = Field(
        default=None, alias="valueBoolean", description="The value of the parameter."
    )
    value_integer: int | float | None = Field(
        default=None, alias="valueInteger", description="The value of the parameter."
    )
    value_decimal: int | float | None = Field(
        default=None, alias="valueDecimal", description="The value of the parameter."
    )
    value_uri: str | None = Field(
        default=None, alias="valueUri", description="The value of the parameter."
    )
    value_code: str | None = Field(
        default=None, alias="valueCode", description="The value of the parameter."
    )
    value_date_time: str | None = Field(
        default=None, alias="valueDateTime", description="The value of the parameter."
    )
