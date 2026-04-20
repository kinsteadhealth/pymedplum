# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.age import Age
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.dosage import Dosage
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.timing import Timing
    from pymedplum.fhir.usagecontext import UsageContext


class ActivityDefinition(MedplumFHIRBase):
    """This resource allows for the definition of some activity to be
    performed, independent of a particular patient, practitioner, or other
    performance context.
    """

    resource_type: Literal["ActivityDefinition"] = Field(
        default="ActivityDefinition", alias="resourceType"
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
    url: str | None = Field(
        default=None,
        description="An absolute URI that is used to identify this activity definition when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this activity definition is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the activity definition is stored on different servers.",
    )
    identifier: list[Identifier] | None = Field(
        default=None,
        description="A formal identifier that is used to identify this activity definition when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: str | None = Field(
        default=None,
        description="The identifier that is used to identify this version of the activity definition when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the activity definition author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. To provide a version consistent with the Decision Support Service specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more information on versioning knowledge assets, refer to the Decision Support Service specification. Note that a version is required for non-experimental active assets.",
    )
    name: str | None = Field(
        default=None,
        description="A natural language name identifying the activity definition. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: str | None = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the activity definition.",
    )
    subtitle: str | None = Field(
        default=None,
        description="An explanatory or alternate title for the activity definition giving additional information about its content.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this activity definition. Enables tracking the life-cycle of the content.",
    )
    experimental: bool | None = Field(
        default=None,
        description="A Boolean value to indicate that this activity definition is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    subject_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="subjectCodeableConcept",
        description="A code or group definition that describes the intended subject of the activity being defined.",
    )
    subject_reference: Reference | None = Field(
        default=None,
        alias="subjectReference",
        description="A code or group definition that describes the intended subject of the activity being defined.",
    )
    date: str | None = Field(
        default=None,
        description="The date (and optionally time) when the activity definition was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the activity definition changes.",
    )
    publisher: str | None = Field(
        default=None,
        description="The name of the organization or individual that published the activity definition.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: str | None = Field(
        default=None,
        description="A free text natural language description of the activity definition from a consumer's perspective.",
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate activity definition instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None,
        description="A legal or geographic region in which the activity definition is intended to be used.",
    )
    purpose: str | None = Field(
        default=None,
        description="Explanation of why this activity definition is needed and why it has been designed as it has.",
    )
    usage: str | None = Field(
        default=None,
        description="A detailed description of how the activity definition is used from a clinical perspective.",
    )
    copyright: str | None = Field(
        default=None,
        description="A copyright statement relating to the activity definition and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the activity definition.",
    )
    approval_date: str | None = Field(
        default=None,
        alias="approvalDate",
        description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.",
    )
    last_review_date: str | None = Field(
        default=None,
        alias="lastReviewDate",
        description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.",
    )
    effective_period: Period | None = Field(
        default=None,
        alias="effectivePeriod",
        description="The period during which the activity definition content was or is planned to be in active use.",
    )
    topic: list[CodeableConcept] | None = Field(
        default=None,
        description="Descriptive topics related to the content of the activity. Topics provide a high-level categorization of the activity that can be useful for filtering and searching.",
    )
    author: list[ContactDetail] | None = Field(
        default=None,
        description="An individiual or organization primarily involved in the creation and maintenance of the content.",
    )
    editor: list[ContactDetail] | None = Field(
        default=None,
        description="An individual or organization primarily responsible for internal coherence of the content.",
    )
    reviewer: list[ContactDetail] | None = Field(
        default=None,
        description="An individual or organization primarily responsible for review of some aspect of the content.",
    )
    endorser: list[ContactDetail] | None = Field(
        default=None,
        description="An individual or organization responsible for officially endorsing the content for use in some setting.",
    )
    related_artifact: list[RelatedArtifact] | None = Field(
        default=None,
        alias="relatedArtifact",
        description="Related artifacts such as additional documentation, justification, or bibliographic references.",
    )
    library: list[str] | None = Field(
        default=None,
        description="A reference to a Library resource containing any formal logic used by the activity definition.",
    )
    kind: (
        Literal[
            "Appointment",
            "AppointmentResponse",
            "CarePlan",
            "Claim",
            "CommunicationRequest",
            "Contract",
            "DeviceRequest",
            "EnrollmentRequest",
            "ImmunizationRecommendation",
            "MedicationRequest",
            "NutritionOrder",
            "ServiceRequest",
            "SupplyRequest",
            "Task",
            "VisionPrescription",
        ]
        | None
    ) = Field(
        default=None,
        description="A description of the kind of resource the activity definition is representing. For example, a MedicationRequest, a ServiceRequest, or a CommunicationRequest. Typically, but not always, this is a Request resource.",
    )
    profile: str | None = Field(
        default=None,
        description="A profile to which the target of the activity definition is expected to conform.",
    )
    code: CodeableConcept | None = Field(
        default=None,
        description="Detailed description of the type of activity; e.g. What lab test, what procedure, what kind of encounter.",
    )
    intent: (
        Literal[
            "proposal",
            "plan",
            "directive",
            "order",
            "original-order",
            "reflex-order",
            "filler-order",
            "instance-order",
            "option",
        ]
        | None
    ) = Field(
        default=None,
        description="Indicates the level of authority/intentionality associated with the activity and where the request should fit into the workflow chain.",
    )
    priority: Literal["routine", "urgent", "asap", "stat"] | None = Field(
        default=None,
        description="Indicates how quickly the activity should be addressed with respect to other requests.",
    )
    do_not_perform: bool | None = Field(
        default=None,
        alias="doNotPerform",
        description="Set this to true if the definition is to indicate that a particular activity should NOT be performed. If true, this element should be interpreted to reinforce a negative coding. For example NPO as a code with a doNotPerform of true would still indicate to NOT perform the action.",
    )
    timing_timing: Timing | None = Field(
        default=None,
        alias="timingTiming",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    timing_date_time: str | None = Field(
        default=None,
        alias="timingDateTime",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    timing_age: Age | None = Field(
        default=None,
        alias="timingAge",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    timing_period: Period | None = Field(
        default=None,
        alias="timingPeriod",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    timing_range: Range | None = Field(
        default=None,
        alias="timingRange",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    timing_duration: Duration | None = Field(
        default=None,
        alias="timingDuration",
        description="The period, timing or frequency upon which the described activity is to occur.",
    )
    location: Reference | None = Field(
        default=None,
        description="Identifies the facility where the activity will occur; e.g. home, hospital, specific clinic, etc.",
    )
    participant: list[ActivityDefinitionParticipant] | None = Field(
        default=None,
        description="Indicates who should participate in performing the action described.",
    )
    product_reference: Reference | None = Field(
        default=None,
        alias="productReference",
        description="Identifies the food, drug or other product being consumed or supplied in the activity.",
    )
    product_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="productCodeableConcept",
        description="Identifies the food, drug or other product being consumed or supplied in the activity.",
    )
    quantity: Quantity | None = Field(
        default=None,
        description="Identifies the quantity expected to be consumed at once (per dose, per meal, etc.).",
    )
    dosage: list[Dosage] | None = Field(
        default=None,
        description="Provides detailed dosage instructions in the same way that they are described for MedicationRequest resources.",
    )
    body_site: list[CodeableConcept] | None = Field(
        default=None,
        alias="bodySite",
        description="Indicates the sites on the subject's body where the procedure should be performed (I.e. the target sites).",
    )
    specimen_requirement: list[Reference] | None = Field(
        default=None,
        alias="specimenRequirement",
        description="Defines specimen requirements for the action to be performed, such as required specimens for a lab test.",
    )
    observation_requirement: list[Reference] | None = Field(
        default=None,
        alias="observationRequirement",
        description="Defines observation requirements for the action to be performed, such as body weight or surface area.",
    )
    observation_result_requirement: list[Reference] | None = Field(
        default=None,
        alias="observationResultRequirement",
        description="Defines the observations that are expected to be produced by the action.",
    )
    transform: str | None = Field(
        default=None,
        description="A reference to a StructureMap resource that defines a transform that can be executed to produce the intent resource using the ActivityDefinition instance as the input.",
    )
    dynamic_value: list[ActivityDefinitionDynamicValue] | None = Field(
        default=None,
        alias="dynamicValue",
        description="Dynamic values that will be evaluated to produce values for elements of the resulting resource. For example, if the dosage of a medication must be computed based on the patient's weight, a dynamic value would be used to specify an expression that calculated the weight, and the path on the request resource that would contain the result.",
    )


class ActivityDefinitionDynamicValue(MedplumFHIRBase):
    """Dynamic values that will be evaluated to produce values for elements of
    the resulting resource. For example, if the dosage of a medication must
    be computed based on the patient's weight, a dynamic value would be used
    to specify an expression that calculated the weight, and the path on the
    request resource that would contain the result.
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
    path: str = Field(
        default=...,
        description="The path to the element to be customized. This is the path on the resource that will hold the result of the calculation defined by the expression. The specified path SHALL be a FHIRPath resolveable on the specified target type of the ActivityDefinition, and SHALL consist only of identifiers, constant indexers, and a restricted subset of functions. The path is allowed to contain qualifiers (.) to traverse sub-elements, as well as indexers ([x]) to traverse multiple-cardinality sub-elements (see the [Simple FHIRPath Profile](fhirpath.html#simple) for full details).",
    )
    expression: Expression = Field(
        default=...,
        description="An expression specifying the value of the customized element.",
    )


class ActivityDefinitionParticipant(MedplumFHIRBase):
    """Indicates who should participate in performing the action described."""

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
    type: Literal["patient", "practitioner", "related-person", "device"] = Field(
        default=..., description="The type of participant in the action."
    )
    role: CodeableConcept | None = Field(
        default=None,
        description="The role the participant should play in performing the described action.",
    )
