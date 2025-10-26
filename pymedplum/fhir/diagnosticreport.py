# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class DiagnosticReport(MedplumFHIRBase):
    """The findings and interpretation of diagnostic tests performed on
    patients, groups of patients, devices, and locations, and/or specimens
    derived from these. The report includes clinical context such as
    requesting and provider information, and some mix of atomic results,
    images, textual and coded interpretations, and formatted representation
    of diagnostic reports.
    """

    resource_type: Literal["DiagnosticReport"] = Field(
        default="DiagnosticReport", alias="resourceType"
    )

    id: Optional[str] = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Optional[Meta] = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: Optional[str] = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: Optional[str] = Field(
        default=None, description="The base language in which the resource is written."
    )
    text: Optional[Narrative] = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    identifier: Optional[list[Identifier]] = Field(
        default=None,
        description="Identifiers assigned to this report by the performer or other systems.",
    )
    based_on: Optional[list[Reference]] = Field(
        default=None,
        alias="basedOn",
        description="Details concerning a service requested.",
    )
    status: Literal[
        "registered",
        "partial",
        "preliminary",
        "final",
        "amended",
        "corrected",
        "appended",
        "cancelled",
        "entered-in-error",
        "unknown",
    ] = Field(default=..., description="The status of the diagnostic report.")
    category: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A code that classifies the clinical discipline, department or diagnostic service that created the report (e.g. cardiology, biochemistry, hematology, MRI). This is used for searching, sorting and display purposes.",
    )
    code: CodeableConcept = Field(
        default=..., description="A code or name that describes this diagnostic report."
    )
    subject: Optional[Reference] = Field(
        default=None,
        description="The subject of the report. Usually, but not always, this is a patient. However, diagnostic services also perform analyses on specimens collected from a variety of other sources.",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        description="The healthcare event (e.g. a patient and healthcare provider interaction) which this DiagnosticReport is about.",
    )
    effective_date_time: Optional[str] = Field(
        default=None,
        alias="effectiveDateTime",
        description="The time or time-period the observed values are related to. When the subject of the report is a patient, this is usually either the time of the procedure or of specimen collection(s), but very often the source of the date/time is not known, only the date/time itself.",
    )
    effective_period: Optional[Period] = Field(
        default=None,
        alias="effectivePeriod",
        description="The time or time-period the observed values are related to. When the subject of the report is a patient, this is usually either the time of the procedure or of specimen collection(s), but very often the source of the date/time is not known, only the date/time itself.",
    )
    issued: Optional[str] = Field(
        default=None,
        description="The date and time that this version of the report was made available to providers, typically after the report was reviewed and verified.",
    )
    performer: Optional[list[Reference]] = Field(
        default=None,
        description="The diagnostic service that is responsible for issuing the report.",
    )
    results_interpreter: Optional[list[Reference]] = Field(
        default=None,
        alias="resultsInterpreter",
        description="The practitioner or organization that is responsible for the report's conclusions and interpretations.",
    )
    specimen: Optional[list[Reference]] = Field(
        default=None,
        description="Details about the specimens on which this diagnostic report is based.",
    )
    result: Optional[list[Reference]] = Field(
        default=None,
        description="[Observations](observation.html) that are part of this diagnostic report.",
    )
    imaging_study: Optional[list[Reference]] = Field(
        default=None,
        alias="imagingStudy",
        description="One or more links to full details of any imaging performed during the diagnostic investigation. Typically, this is imaging performed by DICOM enabled modalities, but this is not required. A fully enabled PACS viewer can use this information to provide views of the source images.",
    )
    media: Optional[list[DiagnosticReportMedia]] = Field(
        default=None,
        description="A list of key images associated with this report. The images are generally created during the diagnostic process, and may be directly of the patient, or of treated specimens (i.e. slides of interest).",
    )
    conclusion: Optional[str] = Field(
        default=None,
        description="Concise and clinically contextualized summary conclusion (interpretation/impression) of the diagnostic report.",
    )
    conclusion_code: Optional[list[CodeableConcept]] = Field(
        default=None,
        alias="conclusionCode",
        description="One or more codes that represent the summary conclusion (interpretation/impression) of the diagnostic report.",
    )
    presented_form: Optional[list[Attachment]] = Field(
        default=None,
        alias="presentedForm",
        description="Rich text representation of the entire result as issued by the diagnostic service. Multiple formats are allowed but they SHALL be semantically equivalent.",
    )


class DiagnosticReportMedia(MedplumFHIRBase):
    """A list of key images associated with this report. The images are
    generally created during the diagnostic process, and may be directly of
    the patient, or of treated specimens (i.e. slides of interest).
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[list[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[list[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    comment: Optional[str] = Field(
        default=None,
        description="A comment about the image. Typically, this is used to provide an explanation for why the image is included, or to draw the viewer's attention to important features.",
    )
    link: Reference = Field(default=..., description="Reference to the image source.")
