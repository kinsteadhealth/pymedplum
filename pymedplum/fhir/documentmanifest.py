# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class DocumentManifest(MedplumFHIRBase):
    """A collection of documents compiled for a purpose together with metadata
    that applies to the collection.
    """

    resource_type: Literal["DocumentManifest"] = Field(
        default="DocumentManifest", alias="resourceType"
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
    master_identifier: Identifier | None = Field(
        default=None,
        alias="masterIdentifier",
        description="A single identifier that uniquely identifies this manifest. Principally used to refer to the manifest in non-FHIR contexts.",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Other identifiers associated with the document manifest, including version independent identifiers.",
    )
    status: Literal["current", "superseded", "entered-in-error"] = Field(
        default=..., description="The status of this document manifest."
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="The code specifying the type of clinical activity that resulted in placing the associated content into the DocumentManifest.",
    )
    subject: Reference | None = Field(
        default=None,
        description="Who or what the set of documents is about. The documents can be about a person, (patient or healthcare practitioner), a device (i.e. machine) or even a group of subjects (such as a document about a herd of farm animals, or a set of patients that share a common exposure). If the documents cross more than one subject, then more than one subject is allowed here (unusual use case).",
    )
    created: str | None = Field(
        default=None,
        description="When the document manifest was created for submission to the server (not necessarily the same thing as the actual resource last modified time, since it may be modified, replicated, etc.).",
    )
    author: list[Reference] | None = Field(
        default=None,
        description="Identifies who is the author of the manifest. Manifest author is not necessarly the author of the references included.",
    )
    recipient: list[Reference] | None = Field(
        default=None,
        description="A patient, practitioner, or organization for which this set of documents is intended.",
    )
    source: str | None = Field(
        default=None,
        description="Identifies the source system, application, or software that produced the document manifest.",
    )
    description: str | None = Field(
        default=None,
        description="Human-readable description of the source document. This is sometimes known as the &quot;title&quot;.",
    )
    content: list[Reference] = Field(
        default=...,
        description="The list of Resources that consist of the parts of this manifest.",
    )
    related: list[DocumentManifestRelated] | None = Field(
        default=None,
        description="Related identifiers or resources associated with the DocumentManifest.",
    )


class DocumentManifestRelated(MedplumFHIRBase):
    """Related identifiers or resources associated with the DocumentManifest."""

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
    identifier: Identifier | None = Field(
        default=None,
        description="Related identifier to this DocumentManifest. For example, Order numbers, accession numbers, XDW workflow numbers.",
    )
    ref: Reference | None = Field(
        default=None,
        description="Related Resource to this DocumentManifest. For example, Order, ServiceRequest, Procedure, EligibilityRequest, etc.",
    )
