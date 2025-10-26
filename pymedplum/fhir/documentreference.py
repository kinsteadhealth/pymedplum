# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class DocumentReference(MedplumFHIRBase):
    """A reference to a document of any kind for any purpose. Provides metadata
    about the document so that the document can be discovered and managed.
    The scope of a document is any seralized object with a mime-type, so
    includes formal patient centric documents (CDA), cliical notes, scanned
    paper, and non-patient specific documents like policy text.
    """

    resource_type: Literal["DocumentReference"] = Field(
        default="DocumentReference", alias="resourceType"
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
    master_identifier: Optional[Identifier] = Field(
        default=None,
        alias="masterIdentifier",
        description="Document identifier as assigned by the source of the document. This identifier is specific to this version of the document. This unique identifier may be used elsewhere to identify this version of the document.",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="Other identifiers associated with the document, including version independent identifiers.",
    )
    status: Literal["current", "superseded", "entered-in-error"] = Field(
        default=..., description="The status of this document reference."
    )
    doc_status: Optional[
        Literal["preliminary", "final", "amended", "entered-in-error"]
    ] = Field(
        default=None,
        alias="docStatus",
        description="The status of the underlying document.",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="Specifies the particular kind of document referenced (e.g. History and Physical, Discharge Summary, Progress Note). This usually equates to the purpose of making the document referenced.",
    )
    category: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A categorization for the type of document referenced - helps for indexing and searching. This may be implied by or derived from the code specified in the DocumentReference.type.",
    )
    subject: Optional[Reference] = Field(
        default=None,
        description="Who or what the document is about. The document can be about a person, (patient or healthcare practitioner), a device (e.g. a machine) or even a group of subjects (such as a document about a herd of farm animals, or a set of patients that share a common exposure).",
    )
    date: Optional[str] = Field(
        default=None, description="When the document reference was created."
    )
    author: Optional[List[Reference]] = Field(
        default=None,
        description="Identifies who is responsible for adding the information to the document.",
    )
    authenticator: Optional[Reference] = Field(
        default=None,
        description="Which person or organization authenticates that this document is valid.",
    )
    custodian: Optional[Reference] = Field(
        default=None,
        description="Identifies the organization or group who is responsible for ongoing maintenance of and access to the document.",
    )
    relates_to: Optional[List[DocumentReferenceRelatesTo]] = Field(
        default=None,
        alias="relatesTo",
        description="Relationships that this document has with other document references that already exist.",
    )
    description: Optional[str] = Field(
        default=None, description="Human-readable description of the source document."
    )
    security_label: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="securityLabel",
        description="A set of Security-Tag codes specifying the level of privacy/security of the Document. Note that DocumentReference.meta.security contains the security labels of the &quot;reference&quot; to the document, while DocumentReference.securityLabel contains a snapshot of the security labels on the document the reference refers to.",
    )
    content: List[DocumentReferenceContent] = Field(
        default=...,
        description="The document and format referenced. There may be multiple content element repetitions, each with a different format.",
    )
    context: Optional[DocumentReferenceContext] = Field(
        default=None,
        description="The clinical context in which the document was prepared.",
    )


class DocumentReferenceContent(MedplumFHIRBase):
    """The document and format referenced. There may be multiple content
    element repetitions, each with a different format.
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
    attachment: Attachment = Field(
        default=...,
        description="The document or URL of the document along with critical metadata to prove content has integrity.",
    )
    format: Optional[Coding] = Field(
        default=None,
        description="An identifier of the document encoding, structure, and template that the document conforms to beyond the base format indicated in the mimeType.",
    )


class DocumentReferenceContext(MedplumFHIRBase):
    """The clinical context in which the document was prepared."""

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
    encounter: Optional[List[Reference]] = Field(
        default=None,
        description="Describes the clinical encounter or type of care that the document content is associated with.",
    )
    event: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="This list of codes represents the main clinical acts, such as a colonoscopy or an appendectomy, being documented. In some cases, the event is inherent in the type Code, such as a &quot;History and Physical Report&quot; in which the procedure being documented is necessarily a &quot;History and Physical&quot; act.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="The time period over which the service that is described by the document was provided.",
    )
    facility_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="facilityType",
        description="The kind of facility where the patient was seen.",
    )
    practice_setting: Optional[CodeableConcept] = Field(
        default=None,
        alias="practiceSetting",
        description="This property may convey specifics about the practice setting where the content was created, often reflecting the clinical specialty.",
    )
    source_patient_info: Optional[Reference] = Field(
        default=None,
        alias="sourcePatientInfo",
        description="The Patient Information as known when the document was published. May be a reference to a version specific, or contained.",
    )
    related: Optional[List[Reference]] = Field(
        default=None,
        description="Related identifiers or resources associated with the DocumentReference.",
    )


class DocumentReferenceRelatesTo(MedplumFHIRBase):
    """Relationships that this document has with other document references that
    already exist.
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
    code: Literal["replaces", "transforms", "signs", "appends"] = Field(
        default=...,
        description="The type of relationship that this document has with anther document.",
    )
    target: Reference = Field(
        default=..., description="The target document of this relationship."
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("DocumentReference", DocumentReference)
    register_model("DocumentReferenceContent", DocumentReferenceContent)
    register_model("DocumentReferenceContext", DocumentReferenceContext)
    register_model("DocumentReferenceRelatesTo", DocumentReferenceRelatesTo)
