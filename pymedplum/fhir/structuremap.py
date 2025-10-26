# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class StructureMap(MedplumFHIRBase):
    """A Map of relationships between 2 structures that can be used to transform data."""

    resource_type: Literal["StructureMap"] = Field(
        default="StructureMap", alias="resourceType"
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
    url: str = Field(
        default=...,
        description="An absolute URI that is used to identify this structure map when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this structure map is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the structure map is stored on different servers.",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="A formal identifier that is used to identify this structure map when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the structure map when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the structure map author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: str = Field(
        default=...,
        description="A natural language name identifying the structure map. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the structure map.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this structure map. Enables tracking the life-cycle of the content.",
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this structure map is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the structure map was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the structure map changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the structure map.",
    )
    contact: Optional[List[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the structure map from a consumer's perspective.",
    )
    use_context: Optional[List[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate structure map instances.",
    )
    jurisdiction: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the structure map is intended to be used.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Explanation of why this structure map is needed and why it has been designed as it has.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the structure map and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the structure map.",
    )
    structure: Optional[List[StructureMapStructure]] = Field(
        default=None,
        description="A structure definition used by this map. The structure definition may describe instances that are converted, or the instances that are produced.",
    )
    import_: Optional[List[str]] = Field(
        default=None,
        alias="import",
        description="Other maps used by this map (canonical URLs).",
    )
    group: List[StructureMapGroup] = Field(
        default=...,
        description="Organizes the mapping into manageable chunks for human review/ease of maintenance.",
    )


class StructureMapGroup(MedplumFHIRBase):
    """Organizes the mapping into manageable chunks for human review/ease of maintenance."""

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
        description="A unique name for the group for the convenience of human readers.",
    )
    extends: Optional[str] = Field(
        default=None, description="Another group that this group adds rules to."
    )
    type_mode: Literal["none", "types", "type-and-types"] = Field(
        default=...,
        alias="typeMode",
        description="If this is the default rule set to apply for the source type or this combination of types.",
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Additional supporting documentation that explains the purpose of the group and the types of mappings within it.",
    )
    input: List[StructureMapGroupInput] = Field(
        default=...,
        description="A name assigned to an instance of data. The instance must be provided when the mapping is invoked.",
    )
    rule: List[StructureMapGroupRule] = Field(
        default=..., description="Transform Rule from source to target."
    )


class StructureMapGroupInput(MedplumFHIRBase):
    """A name assigned to an instance of data. The instance must be provided
    when the mapping is invoked.
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
    name: str = Field(default=..., description="Name for this instance of data.")
    type: Optional[str] = Field(
        default=None, description="Type for this instance of data."
    )
    mode: Literal["source", "target"] = Field(
        default=..., description="Mode for this instance of data."
    )
    documentation: Optional[str] = Field(
        default=None, description="Documentation for this instance of data."
    )


class StructureMapGroupRule(MedplumFHIRBase):
    """Transform Rule from source to target."""

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
        default=..., description="Name of the rule for internal references."
    )
    source: List[StructureMapGroupRuleSource] = Field(
        default=..., description="Source inputs to the mapping."
    )
    target: Optional[List[StructureMapGroupRuleTarget]] = Field(
        default=None, description="Content to create because of this mapping rule."
    )
    rule: Optional[List[StructureMapGroupRule]] = Field(
        default=None, description="Rules contained in this rule."
    )
    dependent: Optional[List[StructureMapGroupRuleDependent]] = Field(
        default=None,
        description="Which other rules to apply in the context of this rule.",
    )
    documentation: Optional[str] = Field(
        default=None, description="Documentation for this instance of data."
    )


class StructureMapGroupRuleDependent(MedplumFHIRBase):
    """Which other rules to apply in the context of this rule."""

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
    name: str = Field(default=..., description="Name of a rule or group to apply.")
    variable: List[str] = Field(
        default=..., description="Variable to pass to the rule or group."
    )


class StructureMapGroupRuleSource(MedplumFHIRBase):
    """Source inputs to the mapping."""

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
    context: str = Field(
        default=..., description="Type or variable this rule applies to."
    )
    min: Optional[Union[int, float]] = Field(
        default=None,
        description="Specified minimum cardinality for the element. This is optional; if present, it acts an implicit check on the input content.",
    )
    max: Optional[str] = Field(
        default=None,
        description="Specified maximum cardinality for the element - a number or a &quot;*&quot;. This is optional; if present, it acts an implicit check on the input content (* just serves as documentation; it's the default value).",
    )
    type: Optional[str] = Field(
        default=None,
        description="Specified type for the element. This works as a condition on the mapping - use for polymorphic elements.",
    )
    default_value_base64_binary: Optional[str] = Field(
        default=None,
        alias="defaultValueBase64Binary",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_boolean: Optional[bool] = Field(
        default=None,
        alias="defaultValueBoolean",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_canonical: Optional[str] = Field(
        default=None,
        alias="defaultValueCanonical",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_code: Optional[str] = Field(
        default=None,
        alias="defaultValueCode",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_date: Optional[str] = Field(
        default=None,
        alias="defaultValueDate",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_date_time: Optional[str] = Field(
        default=None,
        alias="defaultValueDateTime",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="defaultValueDecimal",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_id: Optional[str] = Field(
        default=None,
        alias="defaultValueId",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_instant: Optional[str] = Field(
        default=None,
        alias="defaultValueInstant",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="defaultValueInteger",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_markdown: Optional[str] = Field(
        default=None,
        alias="defaultValueMarkdown",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_oid: Optional[str] = Field(
        default=None,
        alias="defaultValueOid",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_positive_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="defaultValuePositiveInt",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_string: Optional[str] = Field(
        default=None,
        alias="defaultValueString",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_time: Optional[str] = Field(
        default=None,
        alias="defaultValueTime",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_unsigned_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="defaultValueUnsignedInt",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_uri: Optional[str] = Field(
        default=None,
        alias="defaultValueUri",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_url: Optional[str] = Field(
        default=None,
        alias="defaultValueUrl",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_uuid: Optional[str] = Field(
        default=None,
        alias="defaultValueUuid",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_address: Optional[Address] = Field(
        default=None,
        alias="defaultValueAddress",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_age: Optional[Age] = Field(
        default=None,
        alias="defaultValueAge",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_annotation: Optional[Annotation] = Field(
        default=None,
        alias="defaultValueAnnotation",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="defaultValueAttachment",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="defaultValueCodeableConcept",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_coding: Optional[Coding] = Field(
        default=None,
        alias="defaultValueCoding",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_contact_point: Optional[ContactPoint] = Field(
        default=None,
        alias="defaultValueContactPoint",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_count: Optional[Count] = Field(
        default=None,
        alias="defaultValueCount",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_distance: Optional[Distance] = Field(
        default=None,
        alias="defaultValueDistance",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_duration: Optional[Duration] = Field(
        default=None,
        alias="defaultValueDuration",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_human_name: Optional[HumanName] = Field(
        default=None,
        alias="defaultValueHumanName",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_identifier: Optional[Identifier] = Field(
        default=None,
        alias="defaultValueIdentifier",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_money: Optional[Money] = Field(
        default=None,
        alias="defaultValueMoney",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_period: Optional[Period] = Field(
        default=None,
        alias="defaultValuePeriod",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="defaultValueQuantity",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_range: Optional[Range] = Field(
        default=None,
        alias="defaultValueRange",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_ratio: Optional[Ratio] = Field(
        default=None,
        alias="defaultValueRatio",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_reference: Optional[Reference] = Field(
        default=None,
        alias="defaultValueReference",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_sampled_data: Optional[SampledData] = Field(
        default=None,
        alias="defaultValueSampledData",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_signature: Optional[Signature] = Field(
        default=None,
        alias="defaultValueSignature",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_timing: Optional[Timing] = Field(
        default=None,
        alias="defaultValueTiming",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_contact_detail: Optional[ContactDetail] = Field(
        default=None,
        alias="defaultValueContactDetail",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_contributor: Optional[Contributor] = Field(
        default=None,
        alias="defaultValueContributor",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_data_requirement: Optional[DataRequirement] = Field(
        default=None,
        alias="defaultValueDataRequirement",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_expression: Optional[Expression] = Field(
        default=None,
        alias="defaultValueExpression",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_parameter_definition: Optional[ParameterDefinition] = Field(
        default=None,
        alias="defaultValueParameterDefinition",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_related_artifact: Optional[RelatedArtifact] = Field(
        default=None,
        alias="defaultValueRelatedArtifact",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_trigger_definition: Optional[TriggerDefinition] = Field(
        default=None,
        alias="defaultValueTriggerDefinition",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_usage_context: Optional[UsageContext] = Field(
        default=None,
        alias="defaultValueUsageContext",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_dosage: Optional[Dosage] = Field(
        default=None,
        alias="defaultValueDosage",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_meta: Optional[Meta] = Field(
        default=None,
        alias="defaultValueMeta",
        description="A value to use if there is no existing value in the source object.",
    )
    element: Optional[str] = Field(
        default=None, description="Optional field for this source."
    )
    list_mode: Optional[
        Literal["first", "not_first", "last", "not_last", "only_one"]
    ] = Field(
        default=None,
        alias="listMode",
        description="How to handle the list mode for this element.",
    )
    variable: Optional[str] = Field(
        default=None, description="Named context for field, if a field is specified."
    )
    condition: Optional[str] = Field(
        default=None,
        description="FHIRPath expression - must be true or the rule does not apply.",
    )
    check: Optional[str] = Field(
        default=None,
        description="FHIRPath expression - must be true or the mapping engine throws an error instead of completing.",
    )
    log_message: Optional[str] = Field(
        default=None,
        alias="logMessage",
        description="A FHIRPath expression which specifies a message to put in the transform log when content matching the source rule is found.",
    )


class StructureMapGroupRuleTarget(MedplumFHIRBase):
    """Content to create because of this mapping rule."""

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
    context: Optional[str] = Field(
        default=None, description="Type or variable this rule applies to."
    )
    context_type: Optional[Literal["type", "variable"]] = Field(
        default=None, alias="contextType", description="How to interpret the context."
    )
    element: Optional[str] = Field(
        default=None, description="Field to create in the context."
    )
    variable: Optional[str] = Field(
        default=None,
        description="Named context for field, if desired, and a field is specified.",
    )
    list_mode: Optional[List[Literal["first", "share", "last", "collate"]]] = Field(
        default=None,
        alias="listMode",
        description="If field is a list, how to manage the list.",
    )
    list_rule_id: Optional[str] = Field(
        default=None,
        alias="listRuleId",
        description="Internal rule reference for shared list items.",
    )
    transform: Optional[
        Literal[
            "create",
            "copy",
            "truncate",
            "escape",
            "cast",
            "append",
            "translate",
            "reference",
            "dateOp",
            "uuid",
            "pointer",
            "evaluate",
            "cc",
            "c",
            "qty",
            "id",
            "cp",
        ]
    ] = Field(default=None, description="How the data is copied / created.")
    parameter: Optional[List[StructureMapGroupRuleTargetParameter]] = Field(
        default=None, description="Parameters to the transform."
    )


class StructureMapGroupRuleTargetParameter(MedplumFHIRBase):
    """Parameters to the transform."""

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
    value_id: Optional[str] = Field(
        default=None,
        alias="valueId",
        description="Parameter value - variable or literal.",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="Parameter value - variable or literal.",
    )
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="Parameter value - variable or literal.",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="Parameter value - variable or literal.",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="Parameter value - variable or literal.",
    )


class StructureMapStructure(MedplumFHIRBase):
    """A structure definition used by this map. The structure definition may
    describe instances that are converted, or the instances that are
    produced.
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
    url: str = Field(
        default=..., description="The canonical reference to the structure."
    )
    mode: Literal["source", "queried", "target", "produced"] = Field(
        default=..., description="How the referenced structure is used in this mapping."
    )
    alias: Optional[str] = Field(
        default=None, description="The name used for this type in the map."
    )
    documentation: Optional[str] = Field(
        default=None,
        description="Documentation that describes how the structure is used in the mapping.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("StructureMap", StructureMap)
    register_model("StructureMapGroup", StructureMapGroup)
    register_model("StructureMapGroupInput", StructureMapGroupInput)
    register_model("StructureMapGroupRule", StructureMapGroupRule)
    register_model("StructureMapGroupRuleDependent", StructureMapGroupRuleDependent)
    register_model("StructureMapGroupRuleSource", StructureMapGroupRuleSource)
    register_model("StructureMapGroupRuleTarget", StructureMapGroupRuleTarget)
    register_model(
        "StructureMapGroupRuleTargetParameter", StructureMapGroupRuleTargetParameter
    )
    register_model("StructureMapStructure", StructureMapStructure)
