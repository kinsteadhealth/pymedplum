# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class Endpoint(MedplumFHIRBase):
    """The technical details of an endpoint that can be used for electronic
    services, such as for web services providing XDS.b or a REST endpoint
    for another FHIR server. This may include any security context
    information.
    """

    resource_type: Literal["Endpoint"] = Field(default="Endpoint", alias="resourceType")

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
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="Identifier for the organization that is used to identify the endpoint across multiple disparate systems.",
    )
    status: Literal[
        "active", "suspended", "error", "off", "entered-in-error", "test"
    ] = Field(default=..., description="active | suspended | error | off | test.")
    connection_type: Coding = Field(
        default=...,
        alias="connectionType",
        description="A coded value that represents the technical details of the usage of this endpoint, such as what WSDLs should be used in what way. (e.g. XDS.b/DICOM/cds-hook).",
    )
    name: Optional[str] = Field(
        default=None,
        description="A friendly name that this endpoint can be referred to with.",
    )
    managing_organization: Optional[Reference] = Field(
        default=None,
        alias="managingOrganization",
        description="The organization that manages this endpoint (even if technically another organization is hosting this in the cloud, it is the organization associated with the data).",
    )
    contact: Optional[list[ContactPoint]] = Field(
        default=None,
        description="Contact details for a human to contact about the subscription. The primary use of this for system administrator troubleshooting.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="The interval during which the endpoint is expected to be operational.",
    )
    payload_type: list[CodeableConcept] = Field(
        default=...,
        alias="payloadType",
        description="The payload type describes the acceptable content that can be communicated on the endpoint.",
    )
    payload_mime_type: Optional[list[str]] = Field(
        default=None,
        alias="payloadMimeType",
        description="The mime type to send the payload in - e.g. application/fhir+xml, application/fhir+json. If the mime type is not specified, then the sender could send any content (including no content depending on the connectionType).",
    )
    address: str = Field(
        default=...,
        description="The uri that describes the actual end-point to connect to.",
    )
    header: Optional[list[str]] = Field(
        default=None,
        description="Additional headers / information to send as part of the notification.",
    )
