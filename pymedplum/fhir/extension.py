# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Extension(MedplumFHIRBase):
    """Optional Extension Element - found in all resources."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    url: str = Field(
        default=...,
        description="Source of the definition for the extension code - a logical name or a URL.",
    )
    value_base64_binary: Optional[str] = Field(
        default=None,
        alias="valueBase64Binary",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_canonical: Optional[str] = Field(
        default=None,
        alias="valueCanonical",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_code: Optional[str] = Field(
        default=None,
        alias="valueCode",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_date: Optional[str] = Field(
        default=None,
        alias="valueDate",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_date_time: Optional[str] = Field(
        default=None,
        alias="valueDateTime",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_id: Optional[str] = Field(
        default=None,
        alias="valueId",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_instant: Optional[str] = Field(
        default=None,
        alias="valueInstant",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_markdown: Optional[str] = Field(
        default=None,
        alias="valueMarkdown",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_oid: Optional[str] = Field(
        default=None,
        alias="valueOid",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_positive_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="valuePositiveInt",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_time: Optional[str] = Field(
        default=None,
        alias="valueTime",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_unsigned_int: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueUnsignedInt",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_uri: Optional[str] = Field(
        default=None,
        alias="valueUri",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_url: Optional[str] = Field(
        default=None,
        alias="valueUrl",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_uuid: Optional[str] = Field(
        default=None,
        alias="valueUuid",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_address: Optional[Address] = Field(
        default=None,
        alias="valueAddress",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_age: Optional[Age] = Field(
        default=None,
        alias="valueAge",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_annotation: Optional[Annotation] = Field(
        default=None,
        alias="valueAnnotation",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_attachment: Optional[Attachment] = Field(
        default=None,
        alias="valueAttachment",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_codeable_concept: Optional[CodeableConcept] = Field(
        default=None,
        alias="valueCodeableConcept",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_contact_point: Optional[ContactPoint] = Field(
        default=None,
        alias="valueContactPoint",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_count: Optional[Count] = Field(
        default=None,
        alias="valueCount",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_distance: Optional[Distance] = Field(
        default=None,
        alias="valueDistance",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_duration: Optional[Duration] = Field(
        default=None,
        alias="valueDuration",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_human_name: Optional[HumanName] = Field(
        default=None,
        alias="valueHumanName",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_identifier: Optional[Identifier] = Field(
        default=None,
        alias="valueIdentifier",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_money: Optional[Money] = Field(
        default=None,
        alias="valueMoney",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_period: Optional[Period] = Field(
        default=None,
        alias="valuePeriod",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_quantity: Optional[Quantity] = Field(
        default=None,
        alias="valueQuantity",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_range: Optional[Range] = Field(
        default=None,
        alias="valueRange",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_ratio: Optional[Ratio] = Field(
        default=None,
        alias="valueRatio",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_sampled_data: Optional[SampledData] = Field(
        default=None,
        alias="valueSampledData",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_signature: Optional[Signature] = Field(
        default=None,
        alias="valueSignature",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_timing: Optional[Timing] = Field(
        default=None,
        alias="valueTiming",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_contact_detail: Optional[ContactDetail] = Field(
        default=None,
        alias="valueContactDetail",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_contributor: Optional[Contributor] = Field(
        default=None,
        alias="valueContributor",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_data_requirement: Optional[DataRequirement] = Field(
        default=None,
        alias="valueDataRequirement",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_expression: Optional[Expression] = Field(
        default=None,
        alias="valueExpression",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_parameter_definition: Optional[ParameterDefinition] = Field(
        default=None,
        alias="valueParameterDefinition",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_related_artifact: Optional[RelatedArtifact] = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_trigger_definition: Optional[TriggerDefinition] = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_usage_context: Optional[UsageContext] = Field(
        default=None,
        alias="valueUsageContext",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_dosage: Optional[Dosage] = Field(
        default=None,
        alias="valueDosage",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_meta: Optional[Meta] = Field(
        default=None,
        alias="valueMeta",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Extension", Extension)
