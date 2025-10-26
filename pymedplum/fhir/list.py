# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class List(MedplumFHIRBase):
    """A list is a curated collection of resources."""

    resource_type: Literal["List"] = Field(default="List", alias="resourceType")

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
        description="Identifier for the List assigned for business purposes outside the context of FHIR.",
    )
    status: Literal["current", "retired", "entered-in-error"] = Field(
        default=..., description="Indicates the current state of this list."
    )
    mode: Literal["working", "snapshot", "changes"] = Field(
        default=...,
        description="How this list was prepared - whether it is a working list that is suitable for being maintained on an ongoing basis, or if it represents a snapshot of a list of items from another source, or whether it is a prepared list where items may be marked as added, modified or deleted.",
    )
    title: Optional[str] = Field(
        default=None, description="A label for the list assigned by the author."
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="This code defines the purpose of the list - why it was created.",
    )
    subject: Optional[Reference] = Field(
        default=None,
        description="The common subject (or patient) of the resources that are in the list if there is one.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The encounter that is the context in which this list was created.",
    )
    date: Optional[str] = Field(
        default=None, description="The date that the list was prepared."
    )
    source: Optional[Reference] = Field(
        default=None,
        description="The entity responsible for deciding what the contents of the list were. Where the list was created by a human, this is the same as the author of the list.",
    )
    ordered_by: Optional[CodeableConcept] = Field(
        default=None,
        alias="orderedBy",
        description="What order applies to the items in the list.",
    )
    note: Optional[list[Annotation]] = Field(
        default=None, description="Comments that apply to the overall list."
    )
    entry: Optional[list[ListEntry]] = Field(
        default=None, description="Entries in this list."
    )
    empty_reason: Optional[CodeableConcept] = Field(
        default=None,
        alias="emptyReason",
        description="If the list is empty, why the list is empty.",
    )


class ListEntry(MedplumFHIRBase):
    """Entries in this list."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    flag: Optional[CodeableConcept] = Field(
        default=None,
        description="The flag allows the system constructing the list to indicate the role and significance of the item in the list.",
    )
    deleted: Optional[bool] = Field(
        default=None, description="True if this item is marked as deleted in the list."
    )
    date: Optional[str] = Field(
        default=None, description="When this item was added to the list."
    )
    item: Reference = Field(
        default=...,
        description="A reference to the actual resource from which data was derived.",
    )
