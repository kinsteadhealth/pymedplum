# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class Consent(MedplumFHIRBase):
    """A record of a healthcare consumer&rsquo;s choices, which permits or
    denies identified recipient(s) or recipient role(s) to perform one or
    more actions within a given policy context, for specific purposes and
    periods of time.
    """

    resource_type: Literal["Consent"] = Field(default="Consent", alias="resourceType")

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
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Unique identifier for this copy of the Consent Statement.",
    )
    status: Literal[
        "draft", "proposed", "active", "rejected", "inactive", "entered-in-error"
    ] = Field(default=..., description="Indicates the current state of this consent.")
    scope: CodeableConcept = Field(
        default=...,
        description="A selector of the type of consent being presented: ADR, Privacy, Treatment, Research. This list is now extensible.",
    )
    category: list[CodeableConcept] = Field(
        default=...,
        description="A classification of the type of consents found in the statement. This element supports indexing and retrieval of consent statements.",
    )
    patient: Reference | None = Field(
        default=None,
        description="The patient/healthcare consumer to whom this consent applies.",
    )
    date_time: str | None = Field(
        default=None,
        alias="dateTime",
        description="When this Consent was issued / created / indexed.",
    )
    performer: list[Reference] | None = Field(
        default=None,
        description="Either the Grantor, which is the entity responsible for granting the rights listed in a Consent Directive or the Grantee, which is the entity responsible for complying with the Consent Directive, including any obligations or limitations on authorizations and enforcement of prohibitions.",
    )
    organization: list[Reference] | None = Field(
        default=None,
        description="The organization that manages the consent, and the framework within which it is executed.",
    )
    source_attachment: Attachment | None = Field(
        default=None,
        alias="sourceAttachment",
        description="The source on which this consent statement is based. The source might be a scanned original paper form, or a reference to a consent that links back to such a source, a reference to a document repository (e.g. XDS) that stores the original consent document.",
    )
    source_reference: Reference | None = Field(
        default=None,
        alias="sourceReference",
        description="The source on which this consent statement is based. The source might be a scanned original paper form, or a reference to a consent that links back to such a source, a reference to a document repository (e.g. XDS) that stores the original consent document.",
    )
    policy: list[ConsentPolicy] | None = Field(
        default=None,
        description="The references to the policies that are included in this consent scope. Policies may be organizational, but are often defined jurisdictionally, or in law.",
    )
    policy_rule: CodeableConcept | None = Field(
        default=None,
        alias="policyRule",
        description="A reference to the specific base computable regulation or policy.",
    )
    verification: list[ConsentVerification] | None = Field(
        default=None,
        description="Whether a treatment instruction (e.g. artificial respiration yes or no) was verified with the patient, his/her family or another authorized person.",
    )
    provision: ConsentProvision | None = Field(
        default=None,
        description="An exception to the base policy of this consent. An exception can be an addition or removal of access permissions.",
    )


class ConsentPolicy(MedplumFHIRBase):
    """The references to the policies that are included in this consent scope.
    Policies may be organizational, but are often defined jurisdictionally,
    or in law.
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
    authority: str | None = Field(
        default=None,
        description="Entity or Organization having regulatory jurisdiction or accountability for enforcing policies pertaining to Consent Directives.",
    )
    uri: str | None = Field(
        default=None,
        description="The references to the policies that are included in this consent scope. Policies may be organizational, but are often defined jurisdictionally, or in law.",
    )


class ConsentProvision(MedplumFHIRBase):
    """An exception to the base policy of this consent. An exception can be an
    addition or removal of access permissions.
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
    type: Literal["deny", "permit"] | None = Field(
        default=None,
        description="Action to take - permit or deny - when the rule conditions are met. Not permitted in root rule, required in all nested rules.",
    )
    period: Period | None = Field(
        default=None, description="The timeframe in this rule is valid."
    )
    actor: list[ConsentProvisionActor] | None = Field(
        default=None,
        description="Who or what is controlled by this rule. Use group to identify a set of actors by some property they share (e.g. 'admitting officers').",
    )
    action: list[CodeableConcept] | None = Field(
        default=None, description="Actions controlled by this Rule."
    )
    security_label: list[Coding] | None = Field(
        default=None,
        alias="securityLabel",
        description="A security label, comprised of 0..* security label fields (Privacy tags), which define which resources are controlled by this exception.",
    )
    purpose: list[Coding] | None = Field(
        default=None,
        description="The context of the activities a user is taking - why the user is accessing the data - that are controlled by this rule.",
    )
    class_: list[Coding] | None = Field(
        default=None,
        alias="class",
        description="The class of information covered by this rule. The type can be a FHIR resource type, a profile on a type, or a CDA document, or some other type that indicates what sort of information the consent relates to.",
    )
    code: list[CodeableConcept] | None = Field(
        default=None,
        description="If this code is found in an instance, then the rule applies.",
    )
    data_period: Period | None = Field(
        default=None,
        alias="dataPeriod",
        description="Clinical or Operational Relevant period of time that bounds the data controlled by this rule.",
    )
    data: list[ConsentProvisionData] | None = Field(
        default=None,
        description="The resources controlled by this rule if specific resources are referenced.",
    )
    provision: list[ConsentProvision] | None = Field(
        default=None,
        description="Rules which provide exceptions to the base rule or subrules.",
    )


class ConsentProvisionActor(MedplumFHIRBase):
    """Who or what is controlled by this rule. Use group to identify a set of
    actors by some property they share (e.g. 'admitting officers').
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
    role: CodeableConcept = Field(
        default=...,
        description="How the individual is involved in the resources content that is described in the exception.",
    )
    reference: Reference = Field(
        default=...,
        description="The resource that identifies the actor. To identify actors by type, use group to identify a set of actors by some property they share (e.g. 'admitting officers').",
    )


class ConsentProvisionData(MedplumFHIRBase):
    """The resources controlled by this rule if specific resources are referenced."""

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
    meaning: Literal["instance", "related", "dependents", "authoredby"] = Field(
        default=...,
        description="How the resource reference is interpreted when testing consent restrictions.",
    )
    reference: Reference = Field(
        default=...,
        description="A reference to a specific resource that defines which resources are covered by this consent.",
    )


class ConsentVerification(MedplumFHIRBase):
    """Whether a treatment instruction (e.g. artificial respiration yes or no)
    was verified with the patient, his/her family or another authorized
    person.
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
    verified: bool = Field(
        default=..., description="Has the instruction been verified."
    )
    verified_with: Reference | None = Field(
        default=None,
        alias="verifiedWith",
        description="Who verified the instruction (Patient, Relative or other Authorized Person).",
    )
    verification_date: str | None = Field(
        default=None,
        alias="verificationDate",
        description="Date verification was collected.",
    )
