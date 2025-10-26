# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Person(MedplumFHIRBase):
    """Demographics and administrative information about a person independent
    of a specific health-related context.
    """

    resource_type: Literal["Person"] = Field(default="Person", alias="resourceType")

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
        default=None, description="Identifier for a person within a particular scope."
    )
    name: Optional[List[HumanName]] = Field(
        default=None, description="A name associated with the person."
    )
    telecom: Optional[List[ContactPoint]] = Field(
        default=None,
        description="A contact detail for the person, e.g. a telephone number or an email address.",
    )
    gender: Optional[Literal["male", "female", "other", "unknown"]] = Field(
        default=None, description="Administrative Gender."
    )
    birth_date: Optional[str] = Field(
        default=None, alias="birthDate", description="The birth date for the person."
    )
    address: Optional[List[Address]] = Field(
        default=None, description="One or more addresses for the person."
    )
    photo: Optional[Attachment] = Field(
        default=None,
        description="An image that can be displayed as a thumbnail of the person to enhance the identification of the individual.",
    )
    managing_organization: Optional[Reference] = Field(
        default=None,
        alias="managingOrganization",
        description="The organization that is the custodian of the person record.",
    )
    active: Optional[bool] = Field(
        default=None, description="Whether this person's record is in active use."
    )
    link: Optional[List[PersonLink]] = Field(
        default=None,
        description="Link to a resource that concerns the same actual person.",
    )


class PersonLink(MedplumFHIRBase):
    """Link to a resource that concerns the same actual person."""

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
    target: Reference = Field(
        default=...,
        description="The resource to which this actual person is associated.",
    )
    assurance: Optional[Literal["level1", "level2", "level3", "level4"]] = Field(
        default=None,
        description="Level of assurance that this link is associated with the target resource.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Person", Person)
    register_model("PersonLink", PersonLink)
