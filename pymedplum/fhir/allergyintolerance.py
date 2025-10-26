# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class AllergyIntolerance(MedplumFHIRBase):
    """Risk of harmful or undesirable, physiological response which is unique
    to an individual and associated with exposure to a substance.
    """

    resource_type: Literal["AllergyIntolerance"] = Field(
        default="AllergyIntolerance",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Business identifiers assigned to this AllergyIntolerance by the performer or other systems which remain constant as the resource is updated and propagates from server to server.")
    clinical_status: Optional[CodeableConcept] = Field(default=None, alias="clinicalStatus", description="The clinical status of the allergy or intolerance.")
    verification_status: Optional[CodeableConcept] = Field(default=None, alias="verificationStatus", description="Assertion about certainty associated with the propensity, or potential risk, of a reaction to the identified substance (including pharmaceutical product).")
    type: Optional[Literal['allergy', 'intolerance']] = Field(default=None, description="Identification of the underlying physiological mechanism for the reaction risk.")
    category: Optional[list[Literal['food', 'medication', 'environment', 'biologic']]] = Field(default=None, description="Category of the identified substance.")
    criticality: Optional[Literal['low', 'high', 'unable-to-assess']] = Field(default=None, description="Estimate of the potential clinical harm, or seriousness, of the reaction to the identified substance.")
    code: Optional[CodeableConcept] = Field(default=None, description="Code for an allergy or intolerance statement (either a positive or a negated/excluded statement). This may be a code for a substance or pharmaceutical product that is considered to be responsible for the adverse reaction risk (e.g., &quot;Latex&quot;), an allergy or intolerance condition (e.g., &quot;Latex allergy&quot;), or a negated/excluded code for a specific substance or class (e.g., &quot;No latex allergy&quot;) or a general or categorical negated statement (e.g., &quot;No known allergy&quot;, &quot;No known drug allergies&quot;). Note: the substance for a specific reaction may be different from the substance identified as the cause of the risk, but it must be consistent with it. For instance, it may be a more specific substance (e.g. a brand medication) or a composite product that includes the identified substance. It must be clinically safe to only process the 'code' and ignore the 'reaction.substance'. If a receiving system is unable to confirm that AllergyIntolerance.reaction.substance falls within the semantic scope of AllergyIntolerance.code, then the receiving system should ignore AllergyIntolerance.reaction.substance.")
    patient: Reference = Field(default=..., description="The patient who has the allergy or intolerance.")
    encounter: Optional[Reference] = Field(default=None, description="The encounter when the allergy or intolerance was asserted.")
    onset_date_time: Optional[str] = Field(default=None, alias="onsetDateTime", description="Estimated or actual date, date-time, or age when allergy or intolerance was identified.")
    onset_age: Optional[Age] = Field(default=None, alias="onsetAge", description="Estimated or actual date, date-time, or age when allergy or intolerance was identified.")
    onset_period: Optional[Period] = Field(default=None, alias="onsetPeriod", description="Estimated or actual date, date-time, or age when allergy or intolerance was identified.")
    onset_range: Optional[Range] = Field(default=None, alias="onsetRange", description="Estimated or actual date, date-time, or age when allergy or intolerance was identified.")
    onset_string: Optional[str] = Field(default=None, alias="onsetString", description="Estimated or actual date, date-time, or age when allergy or intolerance was identified.")
    recorded_date: Optional[str] = Field(default=None, alias="recordedDate", description="The recordedDate represents when this particular AllergyIntolerance record was created in the system, which is often a system-generated date.")
    recorder: Optional[Reference] = Field(default=None, description="Individual who recorded the record and takes responsibility for its content.")
    asserter: Optional[Reference] = Field(default=None, description="The source of the information about the allergy that is recorded.")
    last_occurrence: Optional[str] = Field(default=None, alias="lastOccurrence", description="Represents the date and/or time of the last known occurrence of a reaction event.")
    note: Optional[list[Annotation]] = Field(default=None, description="Additional narrative about the propensity for the Adverse Reaction, not captured in other fields.")
    reaction: Optional[list[AllergyIntoleranceReaction]] = Field(default=None, description="Details about each adverse reaction event linked to exposure to the identified substance.")


class AllergyIntoleranceReaction(MedplumFHIRBase):
    """Details about each adverse reaction event linked to exposure to the
    identified substance.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    substance: Optional[CodeableConcept] = Field(default=None, description="Identification of the specific substance (or pharmaceutical product) considered to be responsible for the Adverse Reaction event. Note: the substance for a specific reaction may be different from the substance identified as the cause of the risk, but it must be consistent with it. For instance, it may be a more specific substance (e.g. a brand medication) or a composite product that includes the identified substance. It must be clinically safe to only process the 'code' and ignore the 'reaction.substance'. If a receiving system is unable to confirm that AllergyIntolerance.reaction.substance falls within the semantic scope of AllergyIntolerance.code, then the receiving system should ignore AllergyIntolerance.reaction.substance.")
    manifestation: list[CodeableConcept] = Field(default=..., description="Clinical symptoms and/or signs that are observed or associated with the adverse reaction event.")
    description: Optional[str] = Field(default=None, description="Text description about the reaction as a whole, including details of the manifestation if required.")
    onset: Optional[str] = Field(default=None, description="Record of the date and/or time of the onset of the Reaction.")
    severity: Optional[Literal['mild', 'moderate', 'severe']] = Field(default=None, description="Clinical assessment of the severity of the reaction event as a whole, potentially considering multiple different manifestations.")
    exposure_route: Optional[CodeableConcept] = Field(default=None, alias="exposureRoute", description="Identification of the route by which the subject was exposed to the substance.")
    note: Optional[list[Annotation]] = Field(default=None, description="Additional text about the adverse reaction event not captured in other fields.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("AllergyIntolerance", AllergyIntolerance)
    register_model("AllergyIntoleranceReaction", AllergyIntoleranceReaction)
