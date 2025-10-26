# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING

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
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.money import Money
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


class Extension(MedplumFHIRBase):
    """Optional Extension Element - found in all resources."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    url: str = Field(
        default=...,
        description="Source of the definition for the extension code - a logical name or a URL.",
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_canonical: str | None = Field(
        default=None,
        alias="valueCanonical",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_code: str | None = Field(
        default=None,
        alias="valueCode",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_date: str | None = Field(
        default=None,
        alias="valueDate",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_date_time: str | None = Field(
        default=None,
        alias="valueDateTime",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_decimal: int | float | None = Field(
        default=None,
        alias="valueDecimal",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_id: str | None = Field(
        default=None,
        alias="valueId",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_instant: str | None = Field(
        default=None,
        alias="valueInstant",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_integer: int | float | None = Field(
        default=None,
        alias="valueInteger",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_markdown: str | None = Field(
        default=None,
        alias="valueMarkdown",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_oid: str | None = Field(
        default=None,
        alias="valueOid",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_positive_int: int | float | None = Field(
        default=None,
        alias="valuePositiveInt",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_time: str | None = Field(
        default=None,
        alias="valueTime",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_unsigned_int: int | float | None = Field(
        default=None,
        alias="valueUnsignedInt",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_uri: str | None = Field(
        default=None,
        alias="valueUri",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_url: str | None = Field(
        default=None,
        alias="valueUrl",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_uuid: str | None = Field(
        default=None,
        alias="valueUuid",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_address: Address | None = Field(
        default=None,
        alias="valueAddress",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_age: Age | None = Field(
        default=None,
        alias="valueAge",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_annotation: Annotation | None = Field(
        default=None,
        alias="valueAnnotation",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_attachment: Attachment | None = Field(
        default=None,
        alias="valueAttachment",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_coding: Coding | None = Field(
        default=None,
        alias="valueCoding",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_contact_point: ContactPoint | None = Field(
        default=None,
        alias="valueContactPoint",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_count: Count | None = Field(
        default=None,
        alias="valueCount",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_distance: Distance | None = Field(
        default=None,
        alias="valueDistance",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_duration: Duration | None = Field(
        default=None,
        alias="valueDuration",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_human_name: HumanName | None = Field(
        default=None,
        alias="valueHumanName",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_identifier: Identifier | None = Field(
        default=None,
        alias="valueIdentifier",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_money: Money | None = Field(
        default=None,
        alias="valueMoney",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_period: Period | None = Field(
        default=None,
        alias="valuePeriod",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_range: Range | None = Field(
        default=None,
        alias="valueRange",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_ratio: Ratio | None = Field(
        default=None,
        alias="valueRatio",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_sampled_data: SampledData | None = Field(
        default=None,
        alias="valueSampledData",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_signature: Signature | None = Field(
        default=None,
        alias="valueSignature",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_timing: Timing | None = Field(
        default=None,
        alias="valueTiming",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_contact_detail: ContactDetail | None = Field(
        default=None,
        alias="valueContactDetail",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_contributor: Contributor | None = Field(
        default=None,
        alias="valueContributor",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_data_requirement: DataRequirement | None = Field(
        default=None,
        alias="valueDataRequirement",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_expression: Expression | None = Field(
        default=None,
        alias="valueExpression",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_parameter_definition: ParameterDefinition | None = Field(
        default=None,
        alias="valueParameterDefinition",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_related_artifact: RelatedArtifact | None = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_trigger_definition: TriggerDefinition | None = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_usage_context: UsageContext | None = Field(
        default=None,
        alias="valueUsageContext",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_dosage: Dosage | None = Field(
        default=None,
        alias="valueDosage",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_meta: Meta | None = Field(
        default=None,
        alias="valueMeta",
        description="Value of extension - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
