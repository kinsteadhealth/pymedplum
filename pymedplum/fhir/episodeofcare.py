# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class EpisodeOfCare(MedplumFHIRBase):
    """An association between a patient and an organization / healthcare
    provider(s) during which time encounters may occur. The managing
    organization assumes a level of responsibility for the patient during
    this time.
    """

    resource_type: Literal["EpisodeOfCare"] = Field(
        default="EpisodeOfCare",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[List[Identifier]] = Field(default=None, description="The EpisodeOfCare may be known by different identifiers for different contexts of use, such as when an external agency is tracking the Episode for funding purposes.")
    status: Literal['planned', 'waitlist', 'active', 'onhold', 'finished', 'cancelled', 'entered-in-error'] = Field(default=..., description="planned | waitlist | active | onhold | finished | cancelled.")
    status_history: Optional[List[EpisodeOfCareStatusHistory]] = Field(default=None, alias="statusHistory", description="The history of statuses that the EpisodeOfCare has been through (without requiring processing the history of the resource).")
    type: Optional[List[CodeableConcept]] = Field(default=None, description="A classification of the type of episode of care; e.g. specialist referral, disease management, type of funded care.")
    diagnosis: Optional[List[EpisodeOfCareDiagnosis]] = Field(default=None, description="The list of diagnosis relevant to this episode of care.")
    patient: Reference = Field(default=..., description="The patient who is the focus of this episode of care.")
    managing_organization: Optional[Reference] = Field(default=None, alias="managingOrganization", description="The organization that has assumed the specific responsibilities for the specified duration.")
    period: Optional[Period] = Field(default=None, description="The interval during which the managing organization assumes the defined responsibility.")
    referral_request: Optional[List[Reference]] = Field(default=None, alias="referralRequest", description="Referral Request(s) that are fulfilled by this EpisodeOfCare, incoming referrals.")
    care_manager: Optional[Reference] = Field(default=None, alias="careManager", description="The practitioner that is the care manager/care coordinator for this patient.")
    team: Optional[List[Reference]] = Field(default=None, description="The list of practitioners that may be facilitating this episode of care for specific purposes.")
    account: Optional[List[Reference]] = Field(default=None, description="The set of accounts that may be used for billing for this EpisodeOfCare.")


class EpisodeOfCareDiagnosis(MedplumFHIRBase):
    """The list of diagnosis relevant to this episode of care."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    condition: Reference = Field(default=..., description="A list of conditions/problems/diagnoses that this episode of care is intended to be providing care for.")
    role: Optional[CodeableConcept] = Field(default=None, description="Role that this diagnosis has within the episode of care (e.g. admission, billing, discharge &hellip;).")
    rank: Optional[Union[int, float]] = Field(default=None, description="Ranking of the diagnosis (for each role type).")


class EpisodeOfCareStatusHistory(MedplumFHIRBase):
    """The history of statuses that the EpisodeOfCare has been through (without
    requiring processing the history of the resource).
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    status: Literal['planned', 'waitlist', 'active', 'onhold', 'finished', 'cancelled', 'entered-in-error'] = Field(default=..., description="planned | waitlist | active | onhold | finished | cancelled.")
    period: Period = Field(default=..., description="The period during this EpisodeOfCare that the specific status applied.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("EpisodeOfCare", EpisodeOfCare)
    register_model("EpisodeOfCareDiagnosis", EpisodeOfCareDiagnosis)
    register_model("EpisodeOfCareStatusHistory", EpisodeOfCareStatusHistory)
