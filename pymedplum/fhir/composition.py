# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Composition(MedplumFHIRBase):
    """A set of healthcare-related information that is assembled together into
    a single logical package that provides a single coherent statement of
    meaning, establishes its own context and that has clinical attestation
    with regard to who is making the statement. A Composition defines the
    structure and narrative content necessary for a document. However, a
    Composition alone does not constitute a document. Rather, the
    Composition must be the first entry in a Bundle where
    Bundle.type=document, and any other resources referenced from
    Composition must be included as subsequent entries in the Bundle (for
    example Patient, Practitioner, Encounter, etc.).
    """

    resource_type: Literal["Composition"] = Field(
        default="Composition", alias="resourceType"
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
    identifier: Optional[Identifier] = Field(
        default=None,
        description="A version-independent identifier for the Composition. This identifier stays constant as the composition is changed over time.",
    )
    status: Literal["preliminary", "final", "amended", "entered-in-error"] = Field(
        default=...,
        description="The workflow/clinical status of this composition. The status is a marker for the clinical standing of the document.",
    )
    type: CodeableConcept = Field(
        default=...,
        description="Specifies the particular kind of composition (e.g. History and Physical, Discharge Summary, Progress Note). This usually equates to the purpose of making the composition.",
    )
    category: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A categorization for the type of the composition - helps for indexing and searching. This may be implied by or derived from the code specified in the Composition Type.",
    )
    subject: Optional[Reference] = Field(
        default=None,
        description="Who or what the composition is about. The composition can be about a person, (patient or healthcare practitioner), a device (e.g. a machine) or even a group of subjects (such as a document about a herd of livestock, or a set of patients that share a common exposure).",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="Describes the clinical encounter or type of care this documentation is associated with.",
    )
    date: str = Field(
        default=...,
        description="The composition editing time, when the composition was last logically changed by the author.",
    )
    author: List[Reference] = Field(
        default=...,
        description="Identifies who is responsible for the information in the composition, not necessarily who typed it in.",
    )
    title: str = Field(
        default=..., description="Official human-readable label for the composition."
    )
    confidentiality: Optional[Literal["U", "L", "M", "N", "R", "V"]] = Field(
        default=None,
        description="The code specifying the level of confidentiality of the Composition.",
    )
    attester: Optional[List[CompositionAttester]] = Field(
        default=None,
        description="A participant who has attested to the accuracy of the composition/document.",
    )
    custodian: Optional[Reference] = Field(
        default=None,
        description="Identifies the organization or group who is responsible for ongoing maintenance of and access to the composition/document information.",
    )
    relates_to: Optional[List[CompositionRelatesTo]] = Field(
        default=None,
        alias="relatesTo",
        description="Relationships that this composition has with other compositions or documents that already exist.",
    )
    event: Optional[List[CompositionEvent]] = Field(
        default=None,
        description="The clinical service, such as a colonoscopy or an appendectomy, being documented.",
    )
    section: Optional[List[CompositionSection]] = Field(
        default=None,
        description="The root of the sections that make up the composition.",
    )


class CompositionAttester(MedplumFHIRBase):
    """A participant who has attested to the accuracy of the composition/document."""

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
    mode: Literal["personal", "professional", "legal", "official"] = Field(
        default=..., description="The type of attestation the authenticator offers."
    )
    time: Optional[str] = Field(
        default=None, description="When the composition was attested by the party."
    )
    party: Optional[Reference] = Field(
        default=None, description="Who attested the composition in the specified way."
    )


class CompositionEvent(MedplumFHIRBase):
    """The clinical service, such as a colonoscopy or an appendectomy, being documented."""

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
    code: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="This list of codes represents the main clinical acts, such as a colonoscopy or an appendectomy, being documented. In some cases, the event is inherent in the typeCode, such as a &quot;History and Physical Report&quot; in which the procedure being documented is necessarily a &quot;History and Physical&quot; act.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="The period of time covered by the documentation. There is no assertion that the documentation is a complete representation for this period, only that it documents events during this time.",
    )
    detail: Optional[List[Reference]] = Field(
        default=None,
        description="The description and/or reference of the event(s) being documented. For example, this could be used to document such a colonoscopy or an appendectomy.",
    )


class CompositionRelatesTo(MedplumFHIRBase):
    """Relationships that this composition has with other compositions or
    documents that already exist.
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
        description="The type of relationship that this composition has with anther composition or document.",
    )
    target_identifier: Optional[Identifier] = Field(
        default=None,
        alias="targetIdentifier",
        description="The target composition/document of this relationship.",
    )
    target_reference: Optional[Reference] = Field(
        default=None,
        alias="targetReference",
        description="The target composition/document of this relationship.",
    )


class CompositionSection(MedplumFHIRBase):
    """The root of the sections that make up the composition."""

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
    title: Optional[str] = Field(
        default=None,
        description="The label for this particular section. This will be part of the rendered content for the document, and is often used to build a table of contents.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="A code identifying the kind of content contained within the section. This must be consistent with the section title.",
    )
    author: Optional[List[Reference]] = Field(
        default=None,
        description="Identifies who is responsible for the information in this section, not necessarily who typed it in.",
    )
    focus: Optional[Reference] = Field(
        default=None,
        description="The actual focus of the section when it is not the subject of the composition, but instead represents something or someone associated with the subject such as (for a patient subject) a spouse, parent, fetus, or donor. If not focus is specified, the focus is assumed to be focus of the parent section, or, for a section in the Composition itself, the subject of the composition. Sections with a focus SHALL only include resources where the logical subject (patient, subject, focus, etc.) matches the section focus, or the resources have no logical subject (few resources).",
    )
    text: Optional[Narrative] = Field(
        default=None,
        description="A human-readable narrative that contains the attested content of the section, used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative.",
    )
    mode: Optional[Literal["working", "snapshot", "changes"]] = Field(
        default=None,
        description="How the entry list was prepared - whether it is a working list that is suitable for being maintained on an ongoing basis, or if it represents a snapshot of a list of items from another source, or whether it is a prepared list where items may be marked as added, modified or deleted.",
    )
    ordered_by: Optional[CodeableConcept] = Field(
        default=None,
        alias="orderedBy",
        description="Specifies the order applied to the items in the section entries.",
    )
    entry: Optional[List[Reference]] = Field(
        default=None,
        description="A reference to the actual resource from which the narrative in the section is derived.",
    )
    empty_reason: Optional[CodeableConcept] = Field(
        default=None,
        alias="emptyReason",
        description="If the section is empty, why the list is empty. An empty section typically has some text explaining the empty reason.",
    )
    section: Optional[List[CompositionSection]] = Field(
        default=None, description="A nested sub-section within this section."
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Composition", Composition)
    register_model("CompositionAttester", CompositionAttester)
    register_model("CompositionEvent", CompositionEvent)
    register_model("CompositionRelatesTo", CompositionRelatesTo)
    register_model("CompositionSection", CompositionSection)
