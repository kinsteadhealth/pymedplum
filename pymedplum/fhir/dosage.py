# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.timing import Timing


class Dosage(MedplumFHIRBase):
    """Indicates how the medication is/was taken or should be taken by the patient."""

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
    sequence: int | float | None = Field(
        default=None,
        description="Indicates the order in which the dosage instructions should be applied or interpreted.",
    )
    text: str | None = Field(
        default=None, description="Free text dosage instructions e.g. SIG."
    )
    additional_instruction: list[CodeableConcept] | None = Field(
        default=None,
        alias="additionalInstruction",
        description="Supplemental instructions to the patient on how to take the medication (e.g. &quot;with meals&quot; or&quot;take half to one hour before food&quot;) or warnings for the patient about the medication (e.g. &quot;may cause drowsiness&quot; or &quot;avoid exposure of skin to direct sunlight or sunlamps&quot;).",
    )
    patient_instruction: str | None = Field(
        default=None,
        alias="patientInstruction",
        description="Instructions in terms that are understood by the patient or consumer.",
    )
    timing: Timing | None = Field(
        default=None, description="When medication should be administered."
    )
    as_needed_boolean: bool | None = Field(
        default=None,
        alias="asNeededBoolean",
        description="Indicates whether the Medication is only taken when needed within a specific dosing schedule (Boolean option), or it indicates the precondition for taking the Medication (CodeableConcept).",
    )
    as_needed_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="asNeededCodeableConcept",
        description="Indicates whether the Medication is only taken when needed within a specific dosing schedule (Boolean option), or it indicates the precondition for taking the Medication (CodeableConcept).",
    )
    site: CodeableConcept | None = Field(
        default=None, description="Body site to administer to."
    )
    route: CodeableConcept | None = Field(
        default=None, description="How drug should enter body."
    )
    method: CodeableConcept | None = Field(
        default=None, description="Technique for administering medication."
    )
    dose_and_rate: list[DosageDoseAndRate] | None = Field(
        default=None,
        alias="doseAndRate",
        description="The amount of medication administered.",
    )
    max_dose_per_period: Ratio | None = Field(
        default=None,
        alias="maxDosePerPeriod",
        description="Upper limit on medication per unit of time.",
    )
    max_dose_per_administration: Quantity | None = Field(
        default=None,
        alias="maxDosePerAdministration",
        description="Upper limit on medication per administration.",
    )
    max_dose_per_lifetime: Quantity | None = Field(
        default=None,
        alias="maxDosePerLifetime",
        description="Upper limit on medication per lifetime of the patient.",
    )


class DosageDoseAndRate(MedplumFHIRBase):
    """The amount of medication administered."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="The kind of dose or rate specified, for example, ordered or calculated.",
    )
    dose_range: Range | None = Field(
        default=None, alias="doseRange", description="Amount of medication per dose."
    )
    dose_quantity: Quantity | None = Field(
        default=None, alias="doseQuantity", description="Amount of medication per dose."
    )
    rate_ratio: Ratio | None = Field(
        default=None,
        alias="rateRatio",
        description="Amount of medication per unit of time.",
    )
    rate_range: Range | None = Field(
        default=None,
        alias="rateRange",
        description="Amount of medication per unit of time.",
    )
    rate_quantity: Quantity | None = Field(
        default=None,
        alias="rateQuantity",
        description="Amount of medication per unit of time.",
    )
