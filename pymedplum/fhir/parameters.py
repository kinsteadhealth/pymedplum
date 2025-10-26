# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

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
    from pymedplum.fhir.parameterdefinition import ParameterDefinition
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.resource import Resource
    from pymedplum.fhir.sampleddata import SampledData
    from pymedplum.fhir.signature import Signature
    from pymedplum.fhir.timing import Timing
    from pymedplum.fhir.triggerdefinition import TriggerDefinition
    from pymedplum.fhir.usagecontext import UsageContext


class Parameters(MedplumFHIRBase):
    """This resource is a non-persisted resource used to pass information into
    and back from an [operation](operations.html). It has no other use, and
    there is no RESTful endpoint associated with it.
    """

    resource_type: Literal["Parameters"] = Field(
        default="Parameters", alias="resourceType"
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
    parameter: list[ParametersParameter] | None = Field(
        default=None,
        description="A parameter passed to or received from the operation.",
    )


class ParametersParameter(MedplumFHIRBase):
    """A parameter passed to or received from the operation."""

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
        description="The name of the parameter (reference to the operation definition).",
    )
    value_base64_binary: str | None = Field(
        default=None,
        alias="valueBase64Binary",
        description="If the parameter is a data type.",
    )
    value_boolean: bool | None = Field(
        default=None,
        alias="valueBoolean",
        description="If the parameter is a data type.",
    )
    value_canonical: str | None = Field(
        default=None,
        alias="valueCanonical",
        description="If the parameter is a data type.",
    )
    value_code: str | None = Field(
        default=None, alias="valueCode", description="If the parameter is a data type."
    )
    value_date: str | None = Field(
        default=None, alias="valueDate", description="If the parameter is a data type."
    )
    value_date_time: str | None = Field(
        default=None,
        alias="valueDateTime",
        description="If the parameter is a data type.",
    )
    value_decimal: int | float | None = Field(
        default=None,
        alias="valueDecimal",
        description="If the parameter is a data type.",
    )
    value_id: str | None = Field(
        default=None, alias="valueId", description="If the parameter is a data type."
    )
    value_instant: str | None = Field(
        default=None,
        alias="valueInstant",
        description="If the parameter is a data type.",
    )
    value_integer: int | float | None = Field(
        default=None,
        alias="valueInteger",
        description="If the parameter is a data type.",
    )
    value_markdown: str | None = Field(
        default=None,
        alias="valueMarkdown",
        description="If the parameter is a data type.",
    )
    value_oid: str | None = Field(
        default=None, alias="valueOid", description="If the parameter is a data type."
    )
    value_positive_int: int | float | None = Field(
        default=None,
        alias="valuePositiveInt",
        description="If the parameter is a data type.",
    )
    value_string: str | None = Field(
        default=None,
        alias="valueString",
        description="If the parameter is a data type.",
    )
    value_time: str | None = Field(
        default=None, alias="valueTime", description="If the parameter is a data type."
    )
    value_unsigned_int: int | float | None = Field(
        default=None,
        alias="valueUnsignedInt",
        description="If the parameter is a data type.",
    )
    value_uri: str | None = Field(
        default=None, alias="valueUri", description="If the parameter is a data type."
    )
    value_url: str | None = Field(
        default=None, alias="valueUrl", description="If the parameter is a data type."
    )
    value_uuid: str | None = Field(
        default=None, alias="valueUuid", description="If the parameter is a data type."
    )
    value_address: Address | None = Field(
        default=None,
        alias="valueAddress",
        description="If the parameter is a data type.",
    )
    value_age: Age | None = Field(
        default=None, alias="valueAge", description="If the parameter is a data type."
    )
    value_annotation: Annotation | None = Field(
        default=None,
        alias="valueAnnotation",
        description="If the parameter is a data type.",
    )
    value_attachment: Attachment | None = Field(
        default=None,
        alias="valueAttachment",
        description="If the parameter is a data type.",
    )
    value_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="valueCodeableConcept",
        description="If the parameter is a data type.",
    )
    value_coding: Coding | None = Field(
        default=None,
        alias="valueCoding",
        description="If the parameter is a data type.",
    )
    value_contact_point: ContactPoint | None = Field(
        default=None,
        alias="valueContactPoint",
        description="If the parameter is a data type.",
    )
    value_count: Count | None = Field(
        default=None, alias="valueCount", description="If the parameter is a data type."
    )
    value_distance: Distance | None = Field(
        default=None,
        alias="valueDistance",
        description="If the parameter is a data type.",
    )
    value_duration: Duration | None = Field(
        default=None,
        alias="valueDuration",
        description="If the parameter is a data type.",
    )
    value_human_name: HumanName | None = Field(
        default=None,
        alias="valueHumanName",
        description="If the parameter is a data type.",
    )
    value_identifier: Identifier | None = Field(
        default=None,
        alias="valueIdentifier",
        description="If the parameter is a data type.",
    )
    value_money: Money | None = Field(
        default=None, alias="valueMoney", description="If the parameter is a data type."
    )
    value_period: Period | None = Field(
        default=None,
        alias="valuePeriod",
        description="If the parameter is a data type.",
    )
    value_quantity: Quantity | None = Field(
        default=None,
        alias="valueQuantity",
        description="If the parameter is a data type.",
    )
    value_range: Range | None = Field(
        default=None, alias="valueRange", description="If the parameter is a data type."
    )
    value_ratio: Ratio | None = Field(
        default=None, alias="valueRatio", description="If the parameter is a data type."
    )
    value_reference: Reference | None = Field(
        default=None,
        alias="valueReference",
        description="If the parameter is a data type.",
    )
    value_sampled_data: SampledData | None = Field(
        default=None,
        alias="valueSampledData",
        description="If the parameter is a data type.",
    )
    value_signature: Signature | None = Field(
        default=None,
        alias="valueSignature",
        description="If the parameter is a data type.",
    )
    value_timing: Timing | None = Field(
        default=None,
        alias="valueTiming",
        description="If the parameter is a data type.",
    )
    value_contact_detail: ContactDetail | None = Field(
        default=None,
        alias="valueContactDetail",
        description="If the parameter is a data type.",
    )
    value_contributor: Contributor | None = Field(
        default=None,
        alias="valueContributor",
        description="If the parameter is a data type.",
    )
    value_data_requirement: DataRequirement | None = Field(
        default=None,
        alias="valueDataRequirement",
        description="If the parameter is a data type.",
    )
    value_expression: Expression | None = Field(
        default=None,
        alias="valueExpression",
        description="If the parameter is a data type.",
    )
    value_parameter_definition: ParameterDefinition | None = Field(
        default=None,
        alias="valueParameterDefinition",
        description="If the parameter is a data type.",
    )
    value_related_artifact: RelatedArtifact | None = Field(
        default=None,
        alias="valueRelatedArtifact",
        description="If the parameter is a data type.",
    )
    value_trigger_definition: TriggerDefinition | None = Field(
        default=None,
        alias="valueTriggerDefinition",
        description="If the parameter is a data type.",
    )
    value_usage_context: UsageContext | None = Field(
        default=None,
        alias="valueUsageContext",
        description="If the parameter is a data type.",
    )
    value_dosage: Dosage | None = Field(
        default=None,
        alias="valueDosage",
        description="If the parameter is a data type.",
    )
    value_meta: Meta | None = Field(
        default=None, alias="valueMeta", description="If the parameter is a data type."
    )
    resource: Resource | None = Field(
        default=None, description="If the parameter is a whole resource."
    )
    part: list[ParametersParameter] | None = Field(
        default=None, description="A named part of a multi-part parameter."
    )
