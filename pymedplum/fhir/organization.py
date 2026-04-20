# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class Organization(MedplumFHIRBase):
    """A formally or informally recognized grouping of people or organizations
    formed for the purpose of achieving some form of collective action.
    Includes companies, institutions, corporations, departments, community
    groups, healthcare practice groups, payer/insurer, etc.
    """

    resource_type: Literal["Organization"] = Field(
        default="Organization", alias="resourceType"
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
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Identifier for the organization that is used to identify the organization across multiple disparate systems.",
    )
    active: bool | None = Field(
        default=None,
        description="Whether the organization's record is still in active use.",
    )
    type: list[CodeableConcept] | None = Field(
        default=None, description="The kind(s) of organization that this is."
    )
    name: str | None = Field(
        default=None, description="A name associated with the organization."
    )
    alias: list[str] | None = Field(
        default=None,
        description="A list of alternate names that the organization is known as, or was known as in the past.",
    )
    telecom: list[ContactPoint] | None = Field(
        default=None, description="A contact detail for the organization."
    )
    address: list[Address] | None = Field(
        default=None, description="An address for the organization."
    )
    part_of: Reference | None = Field(
        default=None,
        alias="partOf",
        description="The organization of which this organization forms a part.",
    )
    contact: list[OrganizationContact] | None = Field(
        default=None, description="Contact for the organization for a certain purpose."
    )
    endpoint: list[Reference] | None = Field(
        default=None,
        description="Technical endpoints providing access to services operated for the organization.",
    )


class OrganizationContact(MedplumFHIRBase):
    """Contact for the organization for a certain purpose."""

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
    purpose: CodeableConcept | None = Field(
        default=None,
        description="Indicates a purpose for which the contact can be reached.",
    )
    name: HumanName | None = Field(
        default=None, description="A name associated with the contact."
    )
    telecom: list[ContactPoint] | None = Field(
        default=None,
        description="A contact detail (e.g. a telephone number or an email address) by which the party may be contacted.",
    )
    address: Address | None = Field(
        default=None, description="Visiting or postal addresses for the contact."
    )
