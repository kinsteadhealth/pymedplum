# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class DetectedIssue(MedplumFHIRBase):
    """Indicates an actual or potential clinical issue with or between one or
    more active or proposed clinical actions for a patient; e.g. Drug-drug
    interaction, Ineffective treatment frequency, Procedure-condition
    conflict, etc.
    """

    resource_type: Literal["DetectedIssue"] = Field(
        default="DetectedIssue",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="Business identifier associated with the detected issue record.")
    status: Literal['preliminary', 'final', 'entered-in-error', 'mitigated'] = Field(default=..., description="Indicates the status of the detected issue.")
    code: Optional[CodeableConcept] = Field(default=None, description="Identifies the general type of issue identified.")
    severity: Optional[Literal['high', 'moderate', 'low']] = Field(default=None, description="Indicates the degree of importance associated with the identified issue based on the potential impact on the patient.")
    patient: Optional[Reference] = Field(default=None, description="Indicates the patient whose record the detected issue is associated with.")
    identified_date_time: Optional[str] = Field(default=None, alias="identifiedDateTime", description="The date or period when the detected issue was initially identified.")
    identified_period: Optional[Period] = Field(default=None, alias="identifiedPeriod", description="The date or period when the detected issue was initially identified.")
    author: Optional[Reference] = Field(default=None, description="Individual or device responsible for the issue being raised. For example, a decision support application or a pharmacist conducting a medication review.")
    implicated: Optional[list[Reference]] = Field(default=None, description="Indicates the resource representing the current activity or proposed activity that is potentially problematic.")
    evidence: Optional[list[DetectedIssueEvidence]] = Field(default=None, description="Supporting evidence or manifestations that provide the basis for identifying the detected issue such as a GuidanceResponse or MeasureReport.")
    detail: Optional[str] = Field(default=None, description="A textual explanation of the detected issue.")
    reference: Optional[str] = Field(default=None, description="The literature, knowledge-base or similar reference that describes the propensity for the detected issue identified.")
    mitigation: Optional[list[DetectedIssueMitigation]] = Field(default=None, description="Indicates an action that has been taken or is committed to reduce or eliminate the likelihood of the risk identified by the detected issue from manifesting. Can also reflect an observation of known mitigating factors that may reduce/eliminate the need for any action.")


class DetectedIssueEvidence(MedplumFHIRBase):
    """Supporting evidence or manifestations that provide the basis for
    identifying the detected issue such as a GuidanceResponse or
    MeasureReport.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: Optional[list[CodeableConcept]] = Field(default=None, description="A manifestation that led to the recording of this detected issue.")
    detail: Optional[list[Reference]] = Field(default=None, description="Links to resources that constitute evidence for the detected issue such as a GuidanceResponse or MeasureReport.")


class DetectedIssueMitigation(MedplumFHIRBase):
    """Indicates an action that has been taken or is committed to reduce or
    eliminate the likelihood of the risk identified by the detected issue
    from manifesting. Can also reflect an observation of known mitigating
    factors that may reduce/eliminate the need for any action.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    action: CodeableConcept = Field(default=..., description="Describes the action that was taken or the observation that was made that reduces/eliminates the risk associated with the identified issue.")
    date: Optional[str] = Field(default=None, description="Indicates when the mitigating action was documented.")
    author: Optional[Reference] = Field(default=None, description="Identifies the practitioner who determined the mitigation and takes responsibility for the mitigation step occurring.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("DetectedIssue", DetectedIssue)
    register_model("DetectedIssueEvidence", DetectedIssueEvidence)
    register_model("DetectedIssueMitigation", DetectedIssueMitigation)
