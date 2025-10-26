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
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.signature import Signature
    from pymedplum.fhir.timing import Timing


class VerificationResult(MedplumFHIRBase):
    """Describes validation requirements, source(s), status and dates for one
    or more elements.
    """

    resource_type: Literal["VerificationResult"] = Field(
        default="VerificationResult", alias="resourceType"
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
    target: list[Reference] | None = Field(
        default=None, description="A resource that was validated."
    )
    target_location: list[str] | None = Field(
        default=None,
        alias="targetLocation",
        description="The fhirpath location(s) within the resource that was validated.",
    )
    need: CodeableConcept | None = Field(
        default=None,
        description="The frequency with which the target must be validated (none; initial; periodic).",
    )
    status: Literal[
        "attested", "validated", "in-process", "req-revalid", "val-fail", "reval-fail"
    ] = Field(
        default=...,
        description="The validation status of the target (attested; validated; in process; requires revalidation; validation failed; revalidation failed).",
    )
    status_date: str | None = Field(
        default=None,
        alias="statusDate",
        description="When the validation status was updated.",
    )
    validation_type: CodeableConcept | None = Field(
        default=None,
        alias="validationType",
        description="What the target is validated against (nothing; primary source; multiple sources).",
    )
    validation_process: list[CodeableConcept] | None = Field(
        default=None,
        alias="validationProcess",
        description="The primary process by which the target is validated (edit check; value set; primary source; multiple sources; standalone; in context).",
    )
    frequency: Timing | None = Field(
        default=None, description="Frequency of revalidation."
    )
    last_performed: str | None = Field(
        default=None,
        alias="lastPerformed",
        description="The date/time validation was last completed (including failed validations).",
    )
    next_scheduled: str | None = Field(
        default=None,
        alias="nextScheduled",
        description="The date when target is next validated, if appropriate.",
    )
    failure_action: CodeableConcept | None = Field(
        default=None,
        alias="failureAction",
        description="The result if validation fails (fatal; warning; record only; none).",
    )
    primary_source: list[VerificationResultPrimarySource] | None = Field(
        default=None,
        alias="primarySource",
        description="Information about the primary source(s) involved in validation.",
    )
    attestation: VerificationResultAttestation | None = Field(
        default=None,
        description="Information about the entity attesting to information.",
    )
    validator: list[VerificationResultValidator] | None = Field(
        default=None, description="Information about the entity validating information."
    )


class VerificationResultAttestation(MedplumFHIRBase):
    """Information about the entity attesting to information."""

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
    who: Reference | None = Field(
        default=None,
        description="The individual or organization attesting to information.",
    )
    on_behalf_of: Reference | None = Field(
        default=None,
        alias="onBehalfOf",
        description="When the who is asserting on behalf of another (organization or individual).",
    )
    communication_method: CodeableConcept | None = Field(
        default=None,
        alias="communicationMethod",
        description="The method by which attested information was submitted/retrieved (manual; API; Push).",
    )
    date: str | None = Field(
        default=None, description="The date the information was attested to."
    )
    source_identity_certificate: str | None = Field(
        default=None,
        alias="sourceIdentityCertificate",
        description="A digital identity certificate associated with the attestation source.",
    )
    proxy_identity_certificate: str | None = Field(
        default=None,
        alias="proxyIdentityCertificate",
        description="A digital identity certificate associated with the proxy entity submitting attested information on behalf of the attestation source.",
    )
    proxy_signature: Signature | None = Field(
        default=None,
        alias="proxySignature",
        description="Signed assertion by the proxy entity indicating that they have the right to submit attested information on behalf of the attestation source.",
    )
    source_signature: Signature | None = Field(
        default=None,
        alias="sourceSignature",
        description="Signed assertion by the attestation source that they have attested to the information.",
    )


class VerificationResultPrimarySource(MedplumFHIRBase):
    """Information about the primary source(s) involved in validation."""

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
    who: Reference | None = Field(
        default=None, description="Reference to the primary source."
    )
    type: list[CodeableConcept] | None = Field(
        default=None,
        description="Type of primary source (License Board; Primary Education; Continuing Education; Postal Service; Relationship owner; Registration Authority; legal source; issuing source; authoritative source).",
    )
    communication_method: list[CodeableConcept] | None = Field(
        default=None,
        alias="communicationMethod",
        description="Method for communicating with the primary source (manual; API; Push).",
    )
    validation_status: CodeableConcept | None = Field(
        default=None,
        alias="validationStatus",
        description="Status of the validation of the target against the primary source (successful; failed; unknown).",
    )
    validation_date: str | None = Field(
        default=None,
        alias="validationDate",
        description="When the target was validated against the primary source.",
    )
    can_push_updates: CodeableConcept | None = Field(
        default=None,
        alias="canPushUpdates",
        description="Ability of the primary source to push updates/alerts (yes; no; undetermined).",
    )
    push_type_available: list[CodeableConcept] | None = Field(
        default=None,
        alias="pushTypeAvailable",
        description="Type of alerts/updates the primary source can send (specific requested changes; any changes; as defined by source).",
    )


class VerificationResultValidator(MedplumFHIRBase):
    """Information about the entity validating information."""

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
    organization: Reference = Field(
        default=..., description="Reference to the organization validating information."
    )
    identity_certificate: str | None = Field(
        default=None,
        alias="identityCertificate",
        description="A digital identity certificate associated with the validator.",
    )
    attestation_signature: Signature | None = Field(
        default=None,
        alias="attestationSignature",
        description="Signed assertion by the validator that they have validated the information.",
    )
