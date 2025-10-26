# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Parameters(MedplumFHIRBase):
    """This resource is a non-persisted resource used to pass information into
    and back from an [operation](operations.html). It has no other use, and
    there is no RESTful endpoint associated with it.
    """

    resource_type: Literal["Parameters"] = Field(
        default="Parameters",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    parameter: Optional[List[ParametersParameter]] = Field(default=None, description="A parameter passed to or received from the operation.")


class ParametersParameter(MedplumFHIRBase):
    """A parameter passed to or received from the operation."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    name: str = Field(default=..., description="The name of the parameter (reference to the operation definition).")
    value_base64_binary: Optional[str] = Field(default=None, alias="valueBase64Binary", description="If the parameter is a data type.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="If the parameter is a data type.")
    value_canonical: Optional[str] = Field(default=None, alias="valueCanonical", description="If the parameter is a data type.")
    value_code: Optional[str] = Field(default=None, alias="valueCode", description="If the parameter is a data type.")
    value_date: Optional[str] = Field(default=None, alias="valueDate", description="If the parameter is a data type.")
    value_date_time: Optional[str] = Field(default=None, alias="valueDateTime", description="If the parameter is a data type.")
    value_decimal: Optional[Union[int, float]] = Field(default=None, alias="valueDecimal", description="If the parameter is a data type.")
    value_id: Optional[str] = Field(default=None, alias="valueId", description="If the parameter is a data type.")
    value_instant: Optional[str] = Field(default=None, alias="valueInstant", description="If the parameter is a data type.")
    value_integer: Optional[Union[int, float]] = Field(default=None, alias="valueInteger", description="If the parameter is a data type.")
    value_markdown: Optional[str] = Field(default=None, alias="valueMarkdown", description="If the parameter is a data type.")
    value_oid: Optional[str] = Field(default=None, alias="valueOid", description="If the parameter is a data type.")
    value_positive_int: Optional[Union[int, float]] = Field(default=None, alias="valuePositiveInt", description="If the parameter is a data type.")
    value_string: Optional[str] = Field(default=None, alias="valueString", description="If the parameter is a data type.")
    value_time: Optional[str] = Field(default=None, alias="valueTime", description="If the parameter is a data type.")
    value_unsigned_int: Optional[Union[int, float]] = Field(default=None, alias="valueUnsignedInt", description="If the parameter is a data type.")
    value_uri: Optional[str] = Field(default=None, alias="valueUri", description="If the parameter is a data type.")
    value_url: Optional[str] = Field(default=None, alias="valueUrl", description="If the parameter is a data type.")
    value_uuid: Optional[str] = Field(default=None, alias="valueUuid", description="If the parameter is a data type.")
    value_address: Optional[Address] = Field(default=None, alias="valueAddress", description="If the parameter is a data type.")
    value_age: Optional[Age] = Field(default=None, alias="valueAge", description="If the parameter is a data type.")
    value_annotation: Optional[Annotation] = Field(default=None, alias="valueAnnotation", description="If the parameter is a data type.")
    value_attachment: Optional[Attachment] = Field(default=None, alias="valueAttachment", description="If the parameter is a data type.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="If the parameter is a data type.")
    value_coding: Optional[Coding] = Field(default=None, alias="valueCoding", description="If the parameter is a data type.")
    value_contact_point: Optional[ContactPoint] = Field(default=None, alias="valueContactPoint", description="If the parameter is a data type.")
    value_count: Optional[Count] = Field(default=None, alias="valueCount", description="If the parameter is a data type.")
    value_distance: Optional[Distance] = Field(default=None, alias="valueDistance", description="If the parameter is a data type.")
    value_duration: Optional[Duration] = Field(default=None, alias="valueDuration", description="If the parameter is a data type.")
    value_human_name: Optional[HumanName] = Field(default=None, alias="valueHumanName", description="If the parameter is a data type.")
    value_identifier: Optional[Identifier] = Field(default=None, alias="valueIdentifier", description="If the parameter is a data type.")
    value_money: Optional[Money] = Field(default=None, alias="valueMoney", description="If the parameter is a data type.")
    value_period: Optional[Period] = Field(default=None, alias="valuePeriod", description="If the parameter is a data type.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="If the parameter is a data type.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="If the parameter is a data type.")
    value_ratio: Optional[Ratio] = Field(default=None, alias="valueRatio", description="If the parameter is a data type.")
    value_reference: Optional[Reference] = Field(default=None, alias="valueReference", description="If the parameter is a data type.")
    value_sampled_data: Optional[SampledData] = Field(default=None, alias="valueSampledData", description="If the parameter is a data type.")
    value_signature: Optional[Signature] = Field(default=None, alias="valueSignature", description="If the parameter is a data type.")
    value_timing: Optional[Timing] = Field(default=None, alias="valueTiming", description="If the parameter is a data type.")
    value_contact_detail: Optional[ContactDetail] = Field(default=None, alias="valueContactDetail", description="If the parameter is a data type.")
    value_contributor: Optional[Contributor] = Field(default=None, alias="valueContributor", description="If the parameter is a data type.")
    value_data_requirement: Optional[DataRequirement] = Field(default=None, alias="valueDataRequirement", description="If the parameter is a data type.")
    value_expression: Optional[Expression] = Field(default=None, alias="valueExpression", description="If the parameter is a data type.")
    value_parameter_definition: Optional[ParameterDefinition] = Field(default=None, alias="valueParameterDefinition", description="If the parameter is a data type.")
    value_related_artifact: Optional[RelatedArtifact] = Field(default=None, alias="valueRelatedArtifact", description="If the parameter is a data type.")
    value_trigger_definition: Optional[TriggerDefinition] = Field(default=None, alias="valueTriggerDefinition", description="If the parameter is a data type.")
    value_usage_context: Optional[UsageContext] = Field(default=None, alias="valueUsageContext", description="If the parameter is a data type.")
    value_dosage: Optional[Dosage] = Field(default=None, alias="valueDosage", description="If the parameter is a data type.")
    value_meta: Optional[Meta] = Field(default=None, alias="valueMeta", description="If the parameter is a data type.")
    resource: Optional[Resource] = Field(default=None, description="If the parameter is a whole resource.")
    part: Optional[List[ParametersParameter]] = Field(default=None, description="A named part of a multi-part parameter.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Parameters", Parameters)
    register_model("ParametersParameter", ParametersParameter)
