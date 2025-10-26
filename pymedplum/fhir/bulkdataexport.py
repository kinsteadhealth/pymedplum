# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.resourcetype import ResourceType


class BulkDataExport(MedplumFHIRBase):
    """User specific configuration for the Medplum application."""

    resource_type: Literal["BulkDataExport"] = Field(
        default="BulkDataExport", alias="resourceType"
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
    contained: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    status: Literal["accepted", "active", "completed", "error", "cancelled"] = Field(
        default=..., description="The status of the request."
    )
    request_time: str = Field(
        default=...,
        alias="requestTime",
        description="Indicates the server's time when the query is requested.",
    )
    transaction_time: Optional[str] = Field(
        default=None,
        alias="transactionTime",
        description="Indicates the server's time when the query is run. The response SHOULD NOT include any resources modified after this instant, and SHALL include any matching resources modified up to and including this instant.",
    )
    request: str = Field(
        default=...,
        description="The full URL of the original Bulk Data kick-off request. In the case of a POST request, this URL will not include the request parameters.",
    )
    requires_access_token: Optional[bool] = Field(
        default=None,
        alias="requiresAccessToken",
        description="Indicates whether downloading the generated files requires the same authorization mechanism as the $export operation itself.",
    )
    output: Optional[list[BulkDataExportOutput]] = Field(
        default=None,
        description="An array of file items with one entry for each generated file. If no resources are returned from the kick-off request, the server SHOULD return an empty array.",
    )
    deleted: Optional[list[BulkDataExportDeleted]] = Field(
        default=None,
        description="An array of deleted file items following the same structure as the output array.",
    )
    error: Optional[list[BulkDataExportError]] = Field(
        default=None,
        description="Array of message file items following the same structure as the output array.",
    )


class BulkDataExportDeleted(MedplumFHIRBase):
    """An array of deleted file items following the same structure as the output array."""

    type: ResourceType = Field(
        default=..., description="The FHIR resource type that is contained in the file."
    )
    url: str = Field(
        default=...,
        description="The absolute path to the file. The format of the file SHOULD reflect that requested in the _outputFormat parameter of the initial kick-off request.",
    )


class BulkDataExportError(MedplumFHIRBase):
    """Array of message file items following the same structure as the output array."""

    type: ResourceType = Field(
        default=..., description="The FHIR resource type that is contained in the file."
    )
    url: str = Field(
        default=...,
        description="The absolute path to the file. The format of the file SHOULD reflect that requested in the _outputFormat parameter of the initial kick-off request.",
    )


class BulkDataExportOutput(MedplumFHIRBase):
    """An array of file items with one entry for each generated file. If no
    resources are returned from the kick-off request, the server SHOULD
    return an empty array.
    """

    type: ResourceType = Field(
        default=..., description="The FHIR resource type that is contained in the file."
    )
    url: str = Field(
        default=...,
        description="The absolute path to the file. The format of the file SHOULD reflect that requested in the _outputFormat parameter of the initial kick-off request.",
    )
