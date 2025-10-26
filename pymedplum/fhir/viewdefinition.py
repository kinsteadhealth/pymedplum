# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class ViewDefinition(MedplumFHIRBase):
    """View definitions represent a tabular projection of a FHIR resource,
    where the columns and inclusion criteria are defined by FHIRPath
    expressions.
    """

    url: Optional[str] = Field(default=None, description="Canonical identifier for this view definition, represented as a URI (globally unique)")
    identifier: Optional[Identifier] = Field(default=None, description="Additional identifier for the view definition")
    name: Optional[str] = Field(default=None, description="Name of the view definition, must be in a database-friendly format.")
    title: Optional[str] = Field(default=None, description="A optional human-readable description of the view.")
    meta: Optional[Meta] = Field(default=None, description="Metadata about the view definition")
    status: Literal['draft', 'active', 'retired', 'unknown'] = Field(default=..., description="draft | active | retired | unknown")
    experimental: Optional[bool] = Field(default=None, description="For testing purposes, not real usage")
    publisher: Optional[str] = Field(default=None, description="Name of the publisher/steward (organization or individual)")
    contact: Optional[list[ContactDetail]] = Field(default=None, description="Contact details for the publisher")
    description: Optional[str] = Field(default=None, description="Natural language description of the view definition")
    use_context: Optional[list[UsageContext]] = Field(default=None, alias="useContext", description="The context that the content is intended to support")
    copyright: Optional[str] = Field(default=None, description="Use and/or publishing restrictions")
    resource: ResourceType = Field(default=..., description="The FHIR resource that the view is based upon, e.g. 'Patient' or 'Observation'.")
    fhir_version: Optional[list[Literal['0.01', '0.05', '0.06', '0.11', '0.0.80', '0.0.81', '0.0.82', '0.4.0', '0.5.0', '1.0.0', '1.0.1', '1.0.2', '1.1.0', '1.4.0', '1.6.0', '1.8.0', '3.0.0', '3.0.1', '3.3.0', '3.5.0', '4.0.0', '4.0.1']]] = Field(default=None, alias="fhirVersion", description="The FHIR version(s) for the FHIR resource. The value of this element is the formal version of the specification, without the revision number, e.g. [publication].[major].[minor].")
    constant: Optional[list[ViewDefinitionConstant]] = Field(default=None, description="A constant is a value that is injected into a FHIRPath expression through the use of a FHIRPath external constant with the same name.")
    select: list[ViewDefinitionSelect] = Field(default=..., description="The select structure defines the columns to be used in the resulting view. These are expressed in the `column` structure below, or in nested `select`s for nested resources.")
    where: Optional[list[ViewDefinitionWhere]] = Field(default=None, description="A series of zero or more FHIRPath constraints to filter resources for the view. Every constraint must evaluate to true for the resource to be included in the view.")


class ViewDefinitionConstant(MedplumFHIRBase):
    """A constant is a value that is injected into a FHIRPath expression
    through the use of a FHIRPath external constant with the same name.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="Name of constant (referred to in FHIRPath as %[name])")
    value_base64_binary: Optional[str] = Field(default=None, alias="valueBase64Binary", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_canonical: Optional[str] = Field(default=None, alias="valueCanonical", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_code: Optional[str] = Field(default=None, alias="valueCode", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_date: Optional[str] = Field(default=None, alias="valueDate", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_date_time: Optional[str] = Field(default=None, alias="valueDateTime", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_decimal: Optional[Union[int, float]] = Field(default=None, alias="valueDecimal", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_id: Optional[str] = Field(default=None, alias="valueId", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_instant: Optional[str] = Field(default=None, alias="valueInstant", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_integer: Optional[Union[int, float]] = Field(default=None, alias="valueInteger", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_integer64: Optional[str] = Field(default=None, alias="valueInteger64", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_oid: Optional[str] = Field(default=None, alias="valueOid", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_string: Optional[str] = Field(default=None, alias="valueString", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_positive_int: Optional[Union[int, float]] = Field(default=None, alias="valuePositiveInt", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_time: Optional[str] = Field(default=None, alias="valueTime", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_unsigned_int: Optional[Union[int, float]] = Field(default=None, alias="valueUnsignedInt", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_uri: Optional[str] = Field(default=None, alias="valueUri", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_url: Optional[str] = Field(default=None, alias="valueUrl", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")
    value_uuid: Optional[str] = Field(default=None, alias="valueUuid", description="The value that will be substituted in place of the constant reference. This is done by including `%your_constant_name` in a FHIRPath expression, which effectively converts the FHIR literal defined here to a FHIRPath literal used in the path expression. Support for additional types may be added in the future.")


class ViewDefinitionSelect(MedplumFHIRBase):
    """The select structure defines the columns to be used in the resulting
    view. These are expressed in the `column` structure below, or in nested
    `select`s for nested resources.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    column: Optional[list[ViewDefinitionSelectColumn]] = Field(default=None, description="A column to be produced in the resulting table. The column is relative to the select structure that contains it.")
    select: Optional[list[ViewDefinitionSelect]] = Field(default=None, description="Nested select relative to a parent expression. If the parent `select` has a `forEach` or `forEachOrNull`, this child select will apply for each item in that expression.")
    for_each: Optional[str] = Field(default=None, alias="forEach", description="A FHIRPath expression to retrieve the parent element(s) used in the containing select, relative to the root resource or parent `select`, if applicable. `forEach` will produce a row for each element selected in the expression. For example, using forEach on `address` in Patient will generate a new row for each address, with columns defined in the corresponding `column` structure.")
    for_each_or_null: Optional[str] = Field(default=None, alias="forEachOrNull", description="Same as forEach, but produces a single row with null values in the nested expression if the collection is empty. For example, with a Patient resource, a `forEachOrNull` on address will produce a row for each patient even if there are no addresses; it will simply set the address columns to `null`.")
    union_all: Optional[list[ViewDefinitionSelect]] = Field(default=None, alias="unionAll", description="A `unionAll` combines the results of multiple selection structures. Each structure under the `unionAll` must produce the same column names and types. The results from each nested selection will then have their own row.")


class ViewDefinitionSelectColumn(MedplumFHIRBase):
    """A column to be produced in the resulting table. The column is relative
    to the select structure that contains it.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    path: str = Field(default=..., description="A FHIRPath expression that evaluates to the value that will be output in the column for each resource. The input context is the collection of resources of the type specified in the resource element. Constants defined in Reference({constant}) can be referenced as %[name].")
    name: str = Field(default=..., description="Name of the column produced in the output, must be in a database-friendly format. The column names in the output must not have any duplicates.")
    description: Optional[str] = Field(default=None, description="A human-readable description of the column.")
    collection: Optional[bool] = Field(default=None, description="Indicates whether the column may have multiple values. Defaults to `false` if unset. ViewDefinitions must have this set to `true` if multiple values may be returned. Implementations SHALL report an error if multiple values are produced when that is not the case.")
    type: Optional[str] = Field(default=None, description="A FHIR StructureDefinition URI for the column's type. Relative URIs are implicitly given the 'http://hl7.org/fhir/StructureDefinition/' prefix. The URI may also use FHIR element ID notation to indicate a backbone element within a structure. For instance, `Observation.referenceRange` may be specified to indicate the returned type is that backbone element. This field *must* be provided if a ViewDefinition returns a non-primitive type. Implementations should report an error if the returned type does not match the type set here, or if a non-primitive type is returned but this field is unset.")
    tag: Optional[list[ViewDefinitionSelectColumnTag]] = Field(default=None, description="Tags can be used to attach additional metadata to columns, such as implementation-specific directives or database-specific type hints.")


class ViewDefinitionSelectColumnTag(MedplumFHIRBase):
    """Tags can be used to attach additional metadata to columns, such as
    implementation-specific directives or database-specific type hints.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="A name that identifies the meaning of the tag. A namespace should be used to scope the tag to a particular context. For example, 'ansi/type' could be used to indicate the type that should be used to represent the value within an ANSI SQL database.")
    value: str = Field(default=..., description="Value of tag")


class ViewDefinitionWhere(MedplumFHIRBase):
    """A series of zero or more FHIRPath constraints to filter resources for
    the view. Every constraint must evaluate to true for the resource to be
    included in the view.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    path: str = Field(default=..., description="A FHIRPath expression that defines a filter that must evaluate to true for a resource to be included in the output. The input context is the collection of resources of the type specified in the resource element. Constants defined in Reference({constant}) can be referenced as %[name].")
    description: Optional[str] = Field(default=None, description="A human-readable description of the above where constraint.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("ViewDefinition", ViewDefinition)
    register_model("ViewDefinitionConstant", ViewDefinitionConstant)
    register_model("ViewDefinitionSelect", ViewDefinitionSelect)
    register_model("ViewDefinitionSelectColumn", ViewDefinitionSelectColumn)
    register_model("ViewDefinitionSelectColumnTag", ViewDefinitionSelectColumnTag)
    register_model("ViewDefinitionWhere", ViewDefinitionWhere)
