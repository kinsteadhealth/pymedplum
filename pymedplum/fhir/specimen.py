# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Specimen(MedplumFHIRBase):
    """A sample to be used for analysis."""

    resource_type: Literal["Specimen"] = Field(
        default="Specimen",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Id for specimen.")
    accession_identifier: Optional[Identifier] = Field(default=None, alias="accessionIdentifier", description="The identifier assigned by the lab when accessioning specimen(s). This is not necessarily the same as the specimen identifier, depending on local lab procedures.")
    status: Optional[Literal['available', 'unavailable', 'unsatisfactory', 'entered-in-error']] = Field(default=None, description="The availability of the specimen.")
    type: Optional[CodeableConcept] = Field(default=None, description="The kind of material that forms the specimen.")
    subject: Optional[Reference] = Field(default=None, description="Where the specimen came from. This may be from patient(s), from a location (e.g., the source of an environmental sample), or a sampling of a substance or a device.")
    received_time: Optional[str] = Field(default=None, alias="receivedTime", description="Time when specimen was received for processing or testing.")
    parent: Optional[list[Reference]] = Field(default=None, description="Reference to the parent (source) specimen which is used when the specimen was either derived from or a component of another specimen.")
    request: Optional[list[Reference]] = Field(default=None, description="Details concerning a service request that required a specimen to be collected.")
    collection: Optional[SpecimenCollection] = Field(default=None, description="Details concerning the specimen collection.")
    processing: Optional[list[SpecimenProcessing]] = Field(default=None, description="Details concerning processing and processing steps for the specimen.")
    container: Optional[list[SpecimenContainer]] = Field(default=None, description="The container holding the specimen. The recursive nature of containers; i.e. blood in tube in tray in rack is not addressed here.")
    condition: Optional[list[CodeableConcept]] = Field(default=None, description="A mode or state of being that describes the nature of the specimen.")
    note: Optional[list[Annotation]] = Field(default=None, description="To communicate any details or issues about the specimen or during the specimen collection. (for example: broken vial, sent with patient, frozen).")


class SpecimenCollection(MedplumFHIRBase):
    """Details concerning the specimen collection."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    collector: Optional[Reference] = Field(default=None, description="Person who collected the specimen.")
    collected_date_time: Optional[str] = Field(default=None, alias="collectedDateTime", description="Time when specimen was collected from subject - the physiologically relevant time.")
    collected_period: Optional[Period] = Field(default=None, alias="collectedPeriod", description="Time when specimen was collected from subject - the physiologically relevant time.")
    duration: Optional[Duration] = Field(default=None, description="The span of time over which the collection of a specimen occurred.")
    quantity: Optional[Quantity] = Field(default=None, description="The quantity of specimen collected; for instance the volume of a blood sample, or the physical measurement of an anatomic pathology sample.")
    method: Optional[CodeableConcept] = Field(default=None, description="A coded value specifying the technique that is used to perform the procedure.")
    body_site: Optional[CodeableConcept] = Field(default=None, alias="bodySite", description="Anatomical location from which the specimen was collected (if subject is a patient). This is the target site. This element is not used for environmental specimens.")
    fasting_status_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="fastingStatusCodeableConcept", description="Abstinence or reduction from some or all food, drink, or both, for a period of time prior to sample collection.")
    fasting_status_duration: Optional[Duration] = Field(default=None, alias="fastingStatusDuration", description="Abstinence or reduction from some or all food, drink, or both, for a period of time prior to sample collection.")


class SpecimenContainer(MedplumFHIRBase):
    """The container holding the specimen. The recursive nature of containers;
    i.e. blood in tube in tray in rack is not addressed here.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[list[Identifier]] = Field(default=None, description="Id for container. There may be multiple; a manufacturer's bar code, lab assigned identifier, etc. The container ID may differ from the specimen id in some circumstances.")
    description: Optional[str] = Field(default=None, description="Textual description of the container.")
    type: Optional[CodeableConcept] = Field(default=None, description="The type of container associated with the specimen (e.g. slide, aliquot, etc.).")
    capacity: Optional[Quantity] = Field(default=None, description="The capacity (volume or other measure) the container may contain.")
    specimen_quantity: Optional[Quantity] = Field(default=None, alias="specimenQuantity", description="The quantity of specimen in the container; may be volume, dimensions, or other appropriate measurements, depending on the specimen type.")
    additive_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="additiveCodeableConcept", description="Introduced substance to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.")
    additive_reference: Optional[Reference] = Field(default=None, alias="additiveReference", description="Introduced substance to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.")


class SpecimenProcessing(MedplumFHIRBase):
    """Details concerning processing and processing steps for the specimen."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    description: Optional[str] = Field(default=None, description="Textual description of procedure.")
    procedure: Optional[CodeableConcept] = Field(default=None, description="A coded value specifying the procedure used to process the specimen.")
    additive: Optional[list[Reference]] = Field(default=None, description="Material used in the processing step.")
    time_date_time: Optional[str] = Field(default=None, alias="timeDateTime", description="A record of the time or period when the specimen processing occurred. For example the time of sample fixation or the period of time the sample was in formalin.")
    time_period: Optional[Period] = Field(default=None, alias="timePeriod", description="A record of the time or period when the specimen processing occurred. For example the time of sample fixation or the period of time the sample was in formalin.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("Specimen", Specimen)
    register_model("SpecimenCollection", SpecimenCollection)
    register_model("SpecimenContainer", SpecimenContainer)
    register_model("SpecimenProcessing", SpecimenProcessing)
