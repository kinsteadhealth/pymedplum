# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class DeviceUseStatement(MedplumFHIRBase):
    """A record of a device being used by a patient where the record is the
    result of a report from the patient or another clinician.
    """

    resource_type: Literal["DeviceUseStatement"] = Field(
        default="DeviceUseStatement",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="An external identifier for this statement such as an IRI.")
    based_on: Optional[list[Reference]] = Field(default=None, alias="basedOn", description="A plan, proposal or order that is fulfilled in whole or in part by this DeviceUseStatement.")
    status: Literal['active', 'completed', 'entered-in-error', 'intended', 'stopped', 'on-hold'] = Field(default=..., description="A code representing the patient or other source's judgment about the state of the device used that this statement is about. Generally this will be active or completed.")
    subject: Reference = Field(default=..., description="The patient who used the device.")
    derived_from: Optional[list[Reference]] = Field(default=None, alias="derivedFrom", description="Allows linking the DeviceUseStatement to the underlying Request, or to other information that supports or is used to derive the DeviceUseStatement.")
    timing_timing: Optional[Timing] = Field(default=None, alias="timingTiming", description="How often the device was used.")
    timing_period: Optional[Period] = Field(default=None, alias="timingPeriod", description="How often the device was used.")
    timing_date_time: Optional[str] = Field(default=None, alias="timingDateTime", description="How often the device was used.")
    recorded_on: Optional[str] = Field(default=None, alias="recordedOn", description="The time at which the statement was made/recorded.")
    source: Optional[Reference] = Field(default=None, description="Who reported the device was being used by the patient.")
    device: Reference = Field(default=..., description="The details of the device used.")
    reason_code: Optional[list[CodeableConcept]] = Field(default=None, alias="reasonCode", description="Reason or justification for the use of the device.")
    reason_reference: Optional[list[Reference]] = Field(default=None, alias="reasonReference", description="Indicates another resource whose existence justifies this DeviceUseStatement.")
    body_site: Optional[CodeableConcept] = Field(default=None, alias="bodySite", description="Indicates the anotomic location on the subject's body where the device was used ( i.e. the target).")
    note: Optional[list[Annotation]] = Field(default=None, description="Details about the device statement that were not represented at all or sufficiently in one of the attributes provided in a class. These may include for example a comment, an instruction, or a note associated with the statement.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("DeviceUseStatement", DeviceUseStatement)
