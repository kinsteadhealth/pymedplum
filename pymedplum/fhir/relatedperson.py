# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class RelatedPerson(MedplumFHIRBase):
    """Information about a person that is involved in the care for a patient,
    but who is not the target of healthcare, nor has a formal responsibility
    in the care process.
    """

    resource_type: Literal["RelatedPerson"] = Field(
        default="RelatedPerson",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Identifier for a person within a particular scope.")
    active: Optional[bool] = Field(default=None, description="Whether this related person record is in active use.")
    patient: Reference = Field(default=..., description="The patient this person is related to.")
    relationship: Optional[list[CodeableConcept]] = Field(default=None, description="The nature of the relationship between a patient and the related person.")
    name: Optional[list[HumanName]] = Field(default=None, description="A name associated with the person.")
    telecom: Optional[list[ContactPoint]] = Field(default=None, description="A contact detail for the person, e.g. a telephone number or an email address.")
    gender: Optional[Literal['male', 'female', 'other', 'unknown']] = Field(default=None, description="Administrative Gender - the gender that the person is considered to have for administration and record keeping purposes.")
    birth_date: Optional[str] = Field(default=None, alias="birthDate", description="The date on which the related person was born.")
    address: Optional[list[Address]] = Field(default=None, description="Address where the related person can be contacted or visited.")
    photo: Optional[list[Attachment]] = Field(default=None, description="Image of the person.")
    period: Optional[Period] = Field(default=None, description="The period of time during which this relationship is or was active. If there are no dates defined, then the interval is unknown.")
    communication: Optional[list[RelatedPersonCommunication]] = Field(default=None, description="A language which may be used to communicate with about the patient's health.")


class RelatedPersonCommunication(MedplumFHIRBase):
    """A language which may be used to communicate with about the patient's health."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    language: CodeableConcept = Field(default=..., description="The ISO-639-1 alpha 2 code in lower case for the language, optionally followed by a hyphen and the ISO-3166-1 alpha 2 code for the region in upper case; e.g. &quot;en&quot; for English, or &quot;en-US&quot; for American English versus &quot;en-EN&quot; for England English.")
    preferred: Optional[bool] = Field(default=None, description="Indicates whether or not the patient prefers this language (over other languages he masters up a certain level).")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("RelatedPerson", RelatedPerson)
    register_model("RelatedPersonCommunication", RelatedPersonCommunication)
