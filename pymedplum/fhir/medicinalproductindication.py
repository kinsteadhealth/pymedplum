# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.population import Population
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class MedicinalProductIndication(MedplumFHIRBase):
    """Indication for the Medicinal Product."""

    resource_type: Literal["MedicinalProductIndication"] = Field(
        default="MedicinalProductIndication", alias="resourceType"
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
    subject: list[Reference] | None = Field(
        default=None, description="The medication for which this is an indication."
    )
    disease_symptom_procedure: CodeableConcept | None = Field(
        default=None,
        alias="diseaseSymptomProcedure",
        description="The disease, symptom or procedure that is the indication for treatment.",
    )
    disease_status: CodeableConcept | None = Field(
        default=None,
        alias="diseaseStatus",
        description="The status of the disease or symptom for which the indication applies.",
    )
    comorbidity: list[CodeableConcept] | None = Field(
        default=None,
        description="Comorbidity (concurrent condition) or co-infection as part of the indication.",
    )
    intended_effect: CodeableConcept | None = Field(
        default=None,
        alias="intendedEffect",
        description="The intended effect, aim or strategy to be achieved by the indication.",
    )
    duration: Quantity | None = Field(
        default=None,
        description="Timing or duration information as part of the indication.",
    )
    other_therapy: list[MedicinalProductIndicationOtherTherapy] | None = Field(
        default=None,
        alias="otherTherapy",
        description="Information about the use of the medicinal product in relation to other therapies described as part of the indication.",
    )
    undesirable_effect: list[Reference] | None = Field(
        default=None,
        alias="undesirableEffect",
        description="Describe the undesirable effects of the medicinal product.",
    )
    population: list[Population] | None = Field(
        default=None, description="The population group to which this applies."
    )


class MedicinalProductIndicationOtherTherapy(MedplumFHIRBase):
    """Information about the use of the medicinal product in relation to other
    therapies described as part of the indication.
    """

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
    therapy_relationship_type: CodeableConcept = Field(
        default=...,
        alias="therapyRelationshipType",
        description="The type of relationship between the medicinal product indication or contraindication and another therapy.",
    )
    medication_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="medicationCodeableConcept",
        description="Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication.",
    )
    medication_reference: Reference | None = Field(
        default=None,
        alias="medicationReference",
        description="Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication.",
    )
