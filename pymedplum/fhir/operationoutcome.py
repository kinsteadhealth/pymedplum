# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class OperationOutcome(MedplumFHIRBase):
    """A collection of error, warning, or information messages that result from
    a system action.
    """

    resource_type: Literal["OperationOutcome"] = Field(
        default="OperationOutcome",
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
    issue: List[OperationOutcomeIssue] = Field(default=..., description="An error, warning, or information message that results from a system action.")


class OperationOutcomeIssue(MedplumFHIRBase):
    """An error, warning, or information message that results from a system action."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    severity: Literal['fatal', 'error', 'warning', 'information'] = Field(default=..., description="Indicates whether the issue indicates a variation from successful processing.")
    code: Literal['invalid', 'structure', 'required', 'value', 'invariant', 'security', 'login', 'unknown', 'expired', 'forbidden', 'suppressed', 'processing', 'not-supported', 'duplicate', 'multiple-matches', 'not-found', 'deleted', 'too-long', 'code-invalid', 'extension', 'too-costly', 'business-rule', 'conflict', 'transient', 'lock-error', 'no-store', 'exception', 'timeout', 'incomplete', 'throttled', 'informational'] = Field(default=..., description="Describes the type of the issue. The system that creates an OperationOutcome SHALL choose the most applicable code from the IssueType value set, and may additional provide its own code for the error in the details element.")
    details: Optional[CodeableConcept] = Field(default=None, description="Additional details about the error. This may be a text description of the error or a system code that identifies the error.")
    diagnostics: Optional[str] = Field(default=None, description="Additional diagnostic information about the issue.")
    location: Optional[List[str]] = Field(default=None, description="This element is deprecated because it is XML specific. It is replaced by issue.expression, which is format independent, and simpler to parse. For resource issues, this will be a simple XPath limited to element names, repetition indicators and the default child accessor that identifies one of the elements in the resource that caused this issue to be raised. For HTTP errors, will be &quot;http.&quot; + the parameter name.")
    expression: Optional[List[str]] = Field(default=None, description="A [simple subset of FHIRPath](fhirpath.html#simple) limited to element names, repetition indicators and the default child accessor that identifies one of the elements in the resource that caused this issue to be raised.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("OperationOutcome", OperationOutcome)
    register_model("OperationOutcomeIssue", OperationOutcomeIssue)
