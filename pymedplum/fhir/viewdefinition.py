# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.resourcetype import ResourceType
    from pymedplum.fhir.usagecontext import UsageContext


class ViewDefinition(MedplumFHIRBase):
    """View definitions represent a tabular projection of a FHIR resource,
    where the columns and inclusion criteria are defined by FHIRPath
    expressions.
    """

    url: str | None = Field(
        default=None,
        description="Canonical identifier for this view definition, represented as a URI (globally unique)",
    )
    identifier: Identifier | None = Field(
        default=None, description="Additional identifier for the view definition"
    )
    name: str | None = Field(
        default=None,
        description="Name of the view definition, must be in a database-friendly format.",
    )
    title: str | None = Field(
        default=None, description="A optional human-readable description of the view."
    )
    meta: Meta | None = Field(
        default=None, description="Metadata about the view definition"
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=..., description="draft | active | retired | unknown"
    )
    experimental: bool | None = Field(
        default=None, description="For testing purposes, not real usage"
    )
    publisher: str | None = Field(
        default=None,
        description="Name of the publisher/steward (organization or individual)",
    )
    contact: list[ContactDetail] | None = Field(
        default=None, description="Contact details for the publisher"
    )
    description: str | None = Field(
        default=None, description="Natural language description of the view definition"
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The context that the content is intended to support",
    )
    copyright: str | None = Field(
        default=None, description="Use and/or publishing restrictions"
    )
    resource: ResourceType = Field(
        default=...,
        description="The FHIR resource that the view is based upon, e.g. 'Patient' or 'Observation'.",
    )
    fhir_version: (
        list[
            Literal[
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
            ]
        ]
        | None
    ) = Field(
        default=None,
        alias="fhirVersion",
        description="The FHIR version(s) for the FHIR resource. The value of this element is the formal version of the specification, without the revision number, e.g. [publication].[major].[minor].",
    )
    constant: list[ViewDefinitionConstant] | None = Field(
        default=None,
        description="A constant is a value that is injected into a FHIRPath expression through the use of a FHIRPath external constant with the same name.",
    )
    select: list[ViewDefinitionSelect] = Field(
        default=...,
        description="The select structure defines the columns to be used in the resulting view. These are expressed in the `column` structure below, or in nested `select`s for nested resources.",
    )
    where: list[ViewDefinitionWhere] | None = Field(
        default=None,
        description="A series of zero or more FHIRPath constraints to filter resources for the view. Every constraint must evaluate to true for the resource to be included in the view.",
    )


class ViewDefinitionConstant(MedplumFHIRBase):
    """A constant is a value that is injected into a FHIRPath expression
    through the use of a FHIRPath external constant with the same name.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    name: str = Field(
        default=..., description="Name of constant (referred to in FHIRPath as %[name])"
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_canonical: str | None = Field(
        default=None,
        alias="valueCanonical",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_code: str | None = Field(
        default=None,
        alias="valueCode",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_date: str | None = Field(
        default=None,
        alias="valueDate",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_date_time: str | None = Field(
        default=None,
        alias="valueDateTime",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_decimal: int | float | None = Field(
        default=None,
        alias="valueDecimal",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_id: str | None = Field(
        default=None,
        alias="valueId",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_instant: str | None = Field(
        default=None,
        alias="valueInstant",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_integer: int | float | None = Field(
        default=None,
        alias="valueInteger",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_integer64: str | None = Field(
        default=None,
        alias="valueInteger64",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_oid: str | None = Field(
        default=None,
        alias="valueOid",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_positive_int: int | float | None = Field(
        default=None,
        alias="valuePositiveInt",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_time: str | None = Field(
        default=None,
        alias="valueTime",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_unsigned_int: int | float | None = Field(
        default=None,
        alias="valueUnsignedInt",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_uri: str | None = Field(
        default=None,
        alias="valueUri",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_url: str | None = Field(
        default=None,
        alias="valueUrl",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )
    value_uuid: str | None = Field(
        default=None,
        alias="valueUuid",
        description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.",
    )


class ViewDefinitionSelect(MedplumFHIRBase):
    """The select structure defines the columns to be used in the resulting
    view. These are expressed in the `column` structure below, or in nested
    `select`s for nested resources.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    column: list[ViewDefinitionSelectColumn] | None = Field(
        default=None,
        description="A column to be produced in the resulting table. The column is relative to the select structure that contains it.",
    )
    select: list[ViewDefinitionSelect] | None = Field(
        default=None,
        description="Nested select relative to a parent expression. If the parent `select` has a `forEach` or `forEachOrNull`, this child select will apply for each item in that expression.",
    )
    for_each: str | None = Field(
        default=None,
        alias="forEach",
        description="A FHIRPath expression to retrieve the parent element(s) used in the containing select, relative to the root resource or parent `select`, if applicable. `forEach` will produce a row for each element selected in the expression. For example, using forEach on `address` in Patient will generate a new row for each address, with columns defined in the corresponding `column` structure.",
    )
    for_each_or_null: str | None = Field(
        default=None,
        alias="forEachOrNull",
        description="Same as forEach, but produces a single row with null values in the nested expression if the collection is empty. For example, with a Patient resource, a `forEachOrNull` on address will produce a row for each patient even if there are no addresses; it will simply set the address columns to `null`.",
    )
    union_all: list[ViewDefinitionSelect] | None = Field(
        default=None,
        alias="unionAll",
        description="A `unionAll` combines the results of multiple selection structures. Each structure under the `unionAll` must produce the same column names and types. The results from each nested selection will then have their own row.",
    )


class ViewDefinitionSelectColumn(MedplumFHIRBase):
    """A column to be produced in the resulting table. The column is relative
    to the select structure that contains it.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    path: str = Field(
        default=...,
        description="A FHIRPath expression that evaluates to the value that will be output in the column for each resource. The input context is the collection of resources of the type specified in the resource element. Constants defined in Reference({constant}) can be referenced as %[name].",
    )
    name: str = Field(
        default=...,
        description="Name of the column produced in the output, must be in a database-friendly format. The column names in the output must not have any duplicates.",
    )
    description: str | None = Field(
        default=None, description="A human-readable description of the column."
    )
    collection: bool | None = Field(
        default=None,
        description="Indicates whether the column may have multiple values. Defaults to `false` if unset. ViewDefinitions must have this set to `true` if multiple values may be returned. Implementations SHALL report an error if multiple values are produced when that is not the case.",
    )
    type: str | None = Field(
        default=None,
        description="A FHIR StructureDefinition URI for the column's type. Relative URIs are implicitly given the 'http://hl7.org/fhir/StructureDefinition/' prefix. The URI may also use FHIR element ID notation to indicate a backbone element within a structure. For instance, `Observation.referenceRange` may be specified to indicate the returned type is that backbone element. This field *must* be provided if a ViewDefinition returns a non-primitive type. Implementations should report an error if the returned type does not match the type set here, or if a non-primitive type is returned but this field is unset.",
    )
    tag: list[ViewDefinitionSelectColumnTag] | None = Field(
        default=None,
        description="Tags can be used to attach additional metadata to columns, such as implementation-specific directives or database-specific type hints.",
    )


class ViewDefinitionSelectColumnTag(MedplumFHIRBase):
    """Tags can be used to attach additional metadata to columns, such as
    implementation-specific directives or database-specific type hints.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    name: str = Field(
        default=...,
        description="A name that identifies the meaning of the tag. A namespace should be used to scope the tag to a particular context. For example, 'ansi/type' could be used to indicate the type that should be used to represent the value within an ANSI SQL database.",
    )
    value: str = Field(default=..., description="Value of tag")


class ViewDefinitionWhere(MedplumFHIRBase):
    """A series of zero or more FHIRPath constraints to filter resources for
    the view. Every constraint must evaluate to true for the resource to be
    included in the view.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    path: str = Field(
        default=...,
        description="A FHIRPath expression that defines a filter that must evaluate to true for a resource to be included in the output. The input context is the collection of resources of the type specified in the resource element. Constants defined in Reference({constant}) can be referenced as %[name].",
    )
    description: str | None = Field(
        default=None,
        description="A human-readable description of the above where constraint.",
    )
