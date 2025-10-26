# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class SpecimenDefinition(MedplumFHIRBase):
    """A kind of specimen with associated set of requirements."""

    resource_type: Literal["SpecimenDefinition"] = Field(
        default="SpecimenDefinition",
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
    identifier: Optional[Identifier] = Field(default=None, description="A business identifier associated with the kind of specimen.")
    type_collected: Optional[CodeableConcept] = Field(default=None, alias="typeCollected", description="The kind of material to be collected.")
    patient_preparation: Optional[list[CodeableConcept]] = Field(default=None, alias="patientPreparation", description="Preparation of the patient for specimen collection.")
    time_aspect: Optional[str] = Field(default=None, alias="timeAspect", description="Time aspect of specimen collection (duration or offset).")
    collection: Optional[list[CodeableConcept]] = Field(default=None, description="The action to be performed for collecting the specimen.")
    type_tested: Optional[list[SpecimenDefinitionTypeTested]] = Field(default=None, alias="typeTested", description="Specimen conditioned in a container as expected by the testing laboratory.")


class SpecimenDefinitionTypeTested(MedplumFHIRBase):
    """Specimen conditioned in a container as expected by the testing laboratory."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    is_derived: Optional[bool] = Field(default=None, alias="isDerived", description="Primary of secondary specimen.")
    type: Optional[CodeableConcept] = Field(default=None, description="The kind of specimen conditioned for testing expected by lab.")
    preference: Literal['preferred', 'alternate'] = Field(default=..., description="The preference for this type of conditioned specimen.")
    container: Optional[SpecimenDefinitionTypeTestedContainer] = Field(default=None, description="The specimen's container.")
    requirement: Optional[str] = Field(default=None, description="Requirements for delivery and special handling of this kind of conditioned specimen.")
    retention_time: Optional[Duration] = Field(default=None, alias="retentionTime", description="The usual time that a specimen of this kind is retained after the ordered tests are completed, for the purpose of additional testing.")
    rejection_criterion: Optional[list[CodeableConcept]] = Field(default=None, alias="rejectionCriterion", description="Criterion for rejection of the specimen in its container by the laboratory.")
    handling: Optional[list[SpecimenDefinitionTypeTestedHandling]] = Field(default=None, description="Set of instructions for preservation/transport of the specimen at a defined temperature interval, prior the testing process.")


class SpecimenDefinitionTypeTestedContainer(MedplumFHIRBase):
    """The specimen's container."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    material: Optional[CodeableConcept] = Field(default=None, description="The type of material of the container.")
    type: Optional[CodeableConcept] = Field(default=None, description="The type of container used to contain this kind of specimen.")
    cap: Optional[CodeableConcept] = Field(default=None, description="Color of container cap.")
    description: Optional[str] = Field(default=None, description="The textual description of the kind of container.")
    capacity: Optional[Quantity] = Field(default=None, description="The capacity (volume or other measure) of this kind of container.")
    minimum_volume_quantity: Optional[Quantity] = Field(default=None, alias="minimumVolumeQuantity", description="The minimum volume to be conditioned in the container.")
    minimum_volume_string: Optional[str] = Field(default=None, alias="minimumVolumeString", description="The minimum volume to be conditioned in the container.")
    additive: Optional[list[SpecimenDefinitionTypeTestedContainerAdditive]] = Field(default=None, description="Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.")
    preparation: Optional[str] = Field(default=None, description="Special processing that should be applied to the container for this kind of specimen.")


class SpecimenDefinitionTypeTestedContainerAdditive(MedplumFHIRBase):
    """Substance introduced in the kind of container to preserve, maintain or
    enhance the specimen. Examples: Formalin, Citrate, EDTA.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    additive_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="additiveCodeableConcept", description="Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.")
    additive_reference: Optional[Reference] = Field(default=None, alias="additiveReference", description="Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.")


class SpecimenDefinitionTypeTestedHandling(MedplumFHIRBase):
    """Set of instructions for preservation/transport of the specimen at a
    defined temperature interval, prior the testing process.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    temperature_qualifier: Optional[CodeableConcept] = Field(default=None, alias="temperatureQualifier", description="It qualifies the interval of temperature, which characterizes an occurrence of handling. Conditions that are not related to temperature may be handled in the instruction element.")
    temperature_range: Optional[Range] = Field(default=None, alias="temperatureRange", description="The temperature interval for this set of handling instructions.")
    max_duration: Optional[Duration] = Field(default=None, alias="maxDuration", description="The maximum time interval of preservation of the specimen with these conditions.")
    instruction: Optional[str] = Field(default=None, description="Additional textual instructions for the preservation or transport of the specimen. For instance, 'Protect from light exposure'.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SpecimenDefinition", SpecimenDefinition)
    register_model("SpecimenDefinitionTypeTested", SpecimenDefinitionTypeTested)
    register_model("SpecimenDefinitionTypeTestedContainer", SpecimenDefinitionTypeTestedContainer)
    register_model("SpecimenDefinitionTypeTestedContainerAdditive", SpecimenDefinitionTypeTestedContainerAdditive)
    register_model("SpecimenDefinitionTypeTestedHandling", SpecimenDefinitionTypeTestedHandling)
