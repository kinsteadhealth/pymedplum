# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CatalogEntry(MedplumFHIRBase):
    """Catalog entries are wrappers that contextualize items included in a catalog."""

    resource_type: Literal["CatalogEntry"] = Field(
        default="CatalogEntry", alias="resourceType"
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
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="Used in supporting different identifiers for the same product, e.g. manufacturer code and retailer code.",
    )
    type: Optional[CodeableConcept] = Field(
        default=None,
        description="The type of item - medication, device, service, protocol or other.",
    )
    orderable: bool = Field(
        default=..., description="Whether the entry represents an orderable item."
    )
    referenced_item: Union[Reference] = Field(
        default=...,
        alias="referencedItem",
        description="The item in a catalog or definition.",
    )
    additional_identifier: Optional[List[Identifier]] = Field(
        default=None,
        alias="additionalIdentifier",
        description="Used in supporting related concepts, e.g. NDC to RxNorm.",
    )
    classification: Optional[List[CodeableConcept]] = Field(
        default=None, description="Classes of devices, or ATC for medication."
    )
    status: Optional[Literal["draft", "active", "retired", "unknown"]] = Field(
        default=None,
        description="Used to support catalog exchange even for unsupported products, e.g. getting list of medications even if not prescribable.",
    )
    validity_period: Optional[Period] = Field(
        default=None,
        alias="validityPeriod",
        description="The time period in which this catalog entry is expected to be active.",
    )
    valid_to: Optional[str] = Field(
        default=None,
        alias="validTo",
        description="The date until which this catalog entry is expected to be active.",
    )
    last_updated: Optional[str] = Field(
        default=None,
        alias="lastUpdated",
        description="Typically date of issue is different from the beginning of the validity. This can be used to see when an item was last updated.",
    )
    additional_characteristic: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="additionalCharacteristic",
        description="Used for examplefor Out of Formulary, or any specifics.",
    )
    additional_classification: Optional[List[CodeableConcept]] = Field(
        default=None,
        alias="additionalClassification",
        description="User for example for ATC classification, or.",
    )
    related_entry: Optional[List[CatalogEntryRelatedEntry]] = Field(
        default=None,
        alias="relatedEntry",
        description="Used for example, to point to a substance, or to a device used to administer a medication.",
    )


class CatalogEntryRelatedEntry(MedplumFHIRBase):
    """Used for example, to point to a substance, or to a device used to
    administer a medication.
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
    relationtype: Literal["triggers", "is-replaced-by"] = Field(
        default=...,
        description="The type of relation to the related item: child, parent, packageContent, containerPackage, usedIn, uses, requires, etc.",
    )
    item: Reference = Field(
        default=..., description="The reference to the related item."
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CatalogEntry", CatalogEntry)
    register_model("CatalogEntryRelatedEntry", CatalogEntryRelatedEntry)
