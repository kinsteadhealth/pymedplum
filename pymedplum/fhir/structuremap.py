# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.age import Age
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.contributor import Contributor
    from pymedplum.fhir.count import Count
    from pymedplum.fhir.datarequirement import DataRequirement
    from pymedplum.fhir.distance import Distance
    from pymedplum.fhir.dosage import Dosage
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.parameterdefinition import ParameterDefinition
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.sampleddata import SampledData
    from pymedplum.fhir.signature import Signature
    from pymedplum.fhir.timing import Timing
    from pymedplum.fhir.triggerdefinition import TriggerDefinition
    from pymedplum.fhir.usagecontext import UsageContext


class StructureMap(MedplumFHIRBase):
    """A Map of relationships between 2 structures that can be used to transform data."""

    resource_type: Literal["StructureMap"] = Field(
        default="StructureMap", alias="resourceType"
    )

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
    url: str = Field(
        default=...,
        description="An absolute URI that is used to identify this structure map when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this structure map is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the structure map is stored on different servers.",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="A formal identifier that is used to identify this structure map when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: str | None = Field(
        default=None,
        description="The identifier that is used to identify this version of the structure map when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the structure map author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: str = Field(
        default=...,
        description="A natural language name identifying the structure map. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: str | None = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the structure map.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this structure map. Enables tracking the life-cycle of the content.",
    )
    experimental: bool | None = Field(
        default=None,
        description="A Boolean value to indicate that this structure map is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: str | None = Field(
        default=None,
        description="The date (and optionally time) when the structure map was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the structure map changes.",
    )
    publisher: str | None = Field(
        default=None,
        description="The name of the organization or individual that published the structure map.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: str | None = Field(
        default=None,
        description="A free text natural language description of the structure map from a consumer's perspective.",
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate structure map instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None,
        description="A legal or geographic region in which the structure map is intended to be used.",
    )
    purpose: str | None = Field(
        default=None,
        description="Explanation of why this structure map is needed and why it has been designed as it has.",
    )
    copyright: str | None = Field(
        default=None,
        description="A copyright statement relating to the structure map and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the structure map.",
    )
    structure: list[StructureMapStructure] | None = Field(
        default=None,
        description="A structure definition used by this map. The structure definition may describe instances that are converted, or the instances that are produced.",
    )
    import_: list[str] | None = Field(
        default=None,
        alias="import",
        description="Other maps used by this map (canonical URLs).",
    )
    group: list[StructureMapGroup] = Field(
        default=...,
        description="Organizes the mapping into manageable chunks for human review/ease of maintenance.",
    )


class StructureMapGroup(MedplumFHIRBase):
    """Organizes the mapping into manageable chunks for human review/ease of maintenance."""

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
        description="A unique name for the group for the convenience of human readers.",
    )
    extends: str | None = Field(
        default=None, description="Another group that this group adds rules to."
    )
    type_mode: Literal["none", "types", "type-and-types"] = Field(
        default=...,
        alias="typeMode",
        description="If this is the default rule set to apply for the source type or this combination of types.",
    )
    documentation: str | None = Field(
        default=None,
        description="Additional supporting documentation that explains the purpose of the group and the types of mappings within it.",
    )
    input: list[StructureMapGroupInput] = Field(
        default=...,
        description="A name assigned to an instance of data. The instance must be provided when the mapping is invoked.",
    )
    rule: list[StructureMapGroupRule] = Field(
        default=..., description="Transform Rule from source to target."
    )


class StructureMapGroupInput(MedplumFHIRBase):
    """A name assigned to an instance of data. The instance must be provided
    when the mapping is invoked.
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
    name: str = Field(default=..., description="Name for this instance of data.")
    type: str | None = Field(
        default=None, description="Type for this instance of data."
    )
    mode: Literal["source", "target"] = Field(
        default=..., description="Mode for this instance of data."
    )
    documentation: str | None = Field(
        default=None, description="Documentation for this instance of data."
    )


class StructureMapGroupRule(MedplumFHIRBase):
    """Transform Rule from source to target."""

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
        default=..., description="Name of the rule for internal references."
    )
    source: list[StructureMapGroupRuleSource] = Field(
        default=..., description="Source inputs to the mapping."
    )
    target: list[StructureMapGroupRuleTarget] | None = Field(
        default=None, description="Content to create because of this mapping rule."
    )
    rule: list[StructureMapGroupRule] | None = Field(
        default=None, description="Rules contained in this rule."
    )
    dependent: list[StructureMapGroupRuleDependent] | None = Field(
        default=None,
        description="Which other rules to apply in the context of this rule.",
    )
    documentation: str | None = Field(
        default=None, description="Documentation for this instance of data."
    )


class StructureMapGroupRuleDependent(MedplumFHIRBase):
    """Which other rules to apply in the context of this rule."""

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
    name: str = Field(default=..., description="Name of a rule or group to apply.")
    variable: list[str] = Field(
        default=..., description="Variable to pass to the rule or group."
    )


class StructureMapGroupRuleSource(MedplumFHIRBase):
    """Source inputs to the mapping."""

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
    context: str = Field(
        default=..., description="Type or variable this rule applies to."
    )
    min: int | float | None = Field(
        default=None,
        description="Specified minimum cardinality for the element. This is optional; if present, it acts an implicit check on the input content.",
    )
    max: str | None = Field(
        default=None,
        description="Specified maximum cardinality for the element - a number or a &quot;*&quot;. This is optional; if present, it acts an implicit check on the input content (* just serves as documentation; it's the default value).",
    )
    type: str | None = Field(
        default=None,
        description="Specified type for the element. This works as a condition on the mapping - use for polymorphic elements.",
    )
    default_value_base64_binary: str | None = Field(
        default=None,
        alias="defaultValueBase64Binary",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_boolean: bool | None = Field(
        default=None,
        alias="defaultValueBoolean",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_canonical: str | None = Field(
        default=None,
        alias="defaultValueCanonical",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_code: str | None = Field(
        default=None,
        alias="defaultValueCode",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_date: str | None = Field(
        default=None,
        alias="defaultValueDate",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_date_time: str | None = Field(
        default=None,
        alias="defaultValueDateTime",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_decimal: float | None = Field(
        default=None,
        alias="defaultValueDecimal",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_id: str | None = Field(
        default=None,
        alias="defaultValueId",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_instant: str | None = Field(
        default=None,
        alias="defaultValueInstant",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_integer: int | None = Field(
        default=None,
        alias="defaultValueInteger",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_markdown: str | None = Field(
        default=None,
        alias="defaultValueMarkdown",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_oid: str | None = Field(
        default=None,
        alias="defaultValueOid",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_positive_int: int | None = Field(
        default=None,
        alias="defaultValuePositiveInt",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_string: str | None = Field(
        default=None,
        alias="defaultValueString",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_time: str | None = Field(
        default=None,
        alias="defaultValueTime",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_unsigned_int: int | None = Field(
        default=None,
        alias="defaultValueUnsignedInt",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_uri: str | None = Field(
        default=None,
        alias="defaultValueUri",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_url: str | None = Field(
        default=None,
        alias="defaultValueUrl",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_uuid: str | None = Field(
        default=None,
        alias="defaultValueUuid",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_address: Address | None = Field(
        default=None,
        alias="defaultValueAddress",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_age: Age | None = Field(
        default=None,
        alias="defaultValueAge",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_annotation: Annotation | None = Field(
        default=None,
        alias="defaultValueAnnotation",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_attachment: Attachment | None = Field(
        default=None,
        alias="defaultValueAttachment",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="defaultValueCodeableConcept",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_coding: Coding | None = Field(
        default=None,
        alias="defaultValueCoding",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_contact_point: ContactPoint | None = Field(
        default=None,
        alias="defaultValueContactPoint",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_count: Count | None = Field(
        default=None,
        alias="defaultValueCount",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_distance: Distance | None = Field(
        default=None,
        alias="defaultValueDistance",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_duration: Duration | None = Field(
        default=None,
        alias="defaultValueDuration",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_human_name: HumanName | None = Field(
        default=None,
        alias="defaultValueHumanName",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_identifier: Identifier | None = Field(
        default=None,
        alias="defaultValueIdentifier",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_money: Money | None = Field(
        default=None,
        alias="defaultValueMoney",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_period: Period | None = Field(
        default=None,
        alias="defaultValuePeriod",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_quantity: Quantity | None = Field(
        default=None,
        alias="defaultValueQuantity",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_range: Range | None = Field(
        default=None,
        alias="defaultValueRange",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_ratio: Ratio | None = Field(
        default=None,
        alias="defaultValueRatio",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_reference: Reference | None = Field(
        default=None,
        alias="defaultValueReference",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_sampled_data: SampledData | None = Field(
        default=None,
        alias="defaultValueSampledData",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_signature: Signature | None = Field(
        default=None,
        alias="defaultValueSignature",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_timing: Timing | None = Field(
        default=None,
        alias="defaultValueTiming",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_contact_detail: ContactDetail | None = Field(
        default=None,
        alias="defaultValueContactDetail",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_contributor: Contributor | None = Field(
        default=None,
        alias="defaultValueContributor",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_data_requirement: DataRequirement | None = Field(
        default=None,
        alias="defaultValueDataRequirement",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_expression: Expression | None = Field(
        default=None,
        alias="defaultValueExpression",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_parameter_definition: ParameterDefinition | None = Field(
        default=None,
        alias="defaultValueParameterDefinition",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_related_artifact: RelatedArtifact | None = Field(
        default=None,
        alias="defaultValueRelatedArtifact",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_trigger_definition: TriggerDefinition | None = Field(
        default=None,
        alias="defaultValueTriggerDefinition",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_usage_context: UsageContext | None = Field(
        default=None,
        alias="defaultValueUsageContext",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_dosage: Dosage | None = Field(
        default=None,
        alias="defaultValueDosage",
        description="A value to use if there is no existing value in the source object.",
    )
    default_value_meta: Meta | None = Field(
        default=None,
        alias="defaultValueMeta",
        description="A value to use if there is no existing value in the source object.",
    )
    element: str | None = Field(
        default=None, description="Optional field for this source."
    )
    list_mode: Literal["first", "not_first", "last", "not_last", "only_one"] | None = (
        Field(
            default=None,
            alias="listMode",
            description="How to handle the list mode for this element.",
        )
    )
    variable: str | None = Field(
        default=None, description="Named context for field, if a field is specified."
    )
    condition: str | None = Field(
        default=None,
        description="FHIRPath expression - must be true or the rule does not apply.",
    )
    check: str | None = Field(
        default=None,
        description="FHIRPath expression - must be true or the mapping engine throws an error instead of completing.",
    )
    log_message: str | None = Field(
        default=None,
        alias="logMessage",
        description="A FHIRPath expression which specifies a message to put in the transform log when content matching the source rule is found.",
    )


class StructureMapGroupRuleTarget(MedplumFHIRBase):
    """Content to create because of this mapping rule."""

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
    context: str | None = Field(
        default=None, description="Type or variable this rule applies to."
    )
    context_type: Literal["type", "variable"] | None = Field(
        default=None, alias="contextType", description="How to interpret the context."
    )
    element: str | None = Field(
        default=None, description="Field to create in the context."
    )
    variable: str | None = Field(
        default=None,
        description="Named context for field, if desired, and a field is specified.",
    )
    list_mode: list[Literal["first", "share", "last", "collate"]] | None = Field(
        default=None,
        alias="listMode",
        description="If field is a list, how to manage the list.",
    )
    list_rule_id: str | None = Field(
        default=None,
        alias="listRuleId",
        description="Internal rule reference for shared list items.",
    )
    transform: (
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
        | None
    ) = Field(default=None, description="How the data is copied / created.")
    parameter: list[StructureMapGroupRuleTargetParameter] | None = Field(
        default=None, description="Parameters to the transform."
    )


class StructureMapGroupRuleTargetParameter(MedplumFHIRBase):
    """Parameters to the transform."""

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
    value_id: str | None = Field(
        default=None,
        alias="valueId",
        description="Parameter value - variable or literal.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="Parameter value - variable or literal.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="Parameter value - variable or literal.",
    )
    value_integer: int | None = Field(
        default=None,
        alias="valueInteger",
        description="Parameter value - variable or literal.",
    )
    value_decimal: float | None = Field(
        default=None,
        alias="valueDecimal",
        description="Parameter value - variable or literal.",
    )


class StructureMapStructure(MedplumFHIRBase):
    """A structure definition used by this map. The structure definition may
    describe instances that are converted, or the instances that are
    produced.
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
    url: str = Field(
        default=..., description="The canonical reference to the structure."
    )
    mode: Literal["source", "queried", "target", "produced"] = Field(
        default=..., description="How the referenced structure is used in this mapping."
    )
    alias: str | None = Field(
        default=None, description="The name used for this type in the map."
    )
    documentation: str | None = Field(
        default=None,
        description="Documentation that describes how the structure is used in the mapping.",
    )
