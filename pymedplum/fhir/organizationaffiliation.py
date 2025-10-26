# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class OrganizationAffiliation(MedplumFHIRBase):
    """Defines an affiliation/assotiation/relationship between 2 distinct
    oganizations, that is not a part-of relationship/sub-division
    relationship.
    """

    resource_type: Literal["OrganizationAffiliation"] = Field(
        default="OrganizationAffiliation",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[list[dict[str, Any]]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[list[Identifier]] = Field(default=None, description="Business identifiers that are specific to this role.")
    active: Optional[bool] = Field(default=None, description="Whether this organization affiliation record is in active use.")
    period: Optional[Period] = Field(default=None, description="The period during which the participatingOrganization is affiliated with the primary organization.")
    organization: Optional[Reference] = Field(default=None, description="Organization where the role is available (primary organization/has members).")
    participating_organization: Optional[Reference] = Field(default=None, alias="participatingOrganization", description="The Participating Organization provides/performs the role(s) defined by the code to the Primary Organization (e.g. providing services or is a member of).")
    network: Optional[list[Reference]] = Field(default=None, description="Health insurance provider network in which the participatingOrganization provides the role's services (if defined) at the indicated locations (if defined).")
    code: Optional[list[CodeableConcept]] = Field(default=None, description="Definition of the role the participatingOrganization plays in the association.")
    specialty: Optional[list[CodeableConcept]] = Field(default=None, description="Specific specialty of the participatingOrganization in the context of the role.")
    location: Optional[list[Reference]] = Field(default=None, description="The location(s) at which the role occurs.")
    healthcare_service: Optional[list[Reference]] = Field(default=None, alias="healthcareService", description="Healthcare services provided through the role.")
    telecom: Optional[list[ContactPoint]] = Field(default=None, description="Contact details at the participatingOrganization relevant to this Affiliation.")
    endpoint: Optional[list[Reference]] = Field(default=None, description="Technical endpoints providing access to services operated for this role.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("OrganizationAffiliation", OrganizationAffiliation)
