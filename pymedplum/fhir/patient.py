# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class Patient(MedplumFHIRBase):
    """Demographics and other administrative information about an individual or
    animal receiving care or other health-related services.
    """

    resource_type: Literal["Patient"] = Field(default="Patient", alias="resourceType")

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
        default=None, description="An identifier for this patient."
    )
    active: Optional[bool] = Field(
        default=None,
        description="Whether this patient record is in active use. Many systems use this property to mark as non-current patients, such as those that have not been seen for a period of time based on an organization's business rules. It is often used to filter patient lists to exclude inactive patients Deceased patients may also be marked as inactive for the same reasons, but may be active for some time after death.",
    )
    name: Optional[list[HumanName]] = Field(
        default=None, description="A name associated with the individual."
    )
    telecom: Optional[list[ContactPoint]] = Field(
        default=None,
        description="A contact detail (e.g. a telephone number or an email address) by which the individual may be contacted.",
    )
    gender: Optional[Literal["male", "female", "other", "unknown"]] = Field(
        default=None,
        description="Administrative Gender - the gender that the patient is considered to have for administration and record keeping purposes.",
    )
    birth_date: Optional[str] = Field(
        default=None,
        alias="birthDate",
        description="The date of birth for the individual.",
    )
    deceased_boolean: Optional[bool] = Field(
        default=None,
        alias="deceasedBoolean",
        description="Indicates if the individual is deceased or not.",
    )
    deceased_date_time: Optional[str] = Field(
        default=None,
        alias="deceasedDateTime",
        description="Indicates if the individual is deceased or not.",
    )
    address: Optional[list[Address]] = Field(
        default=None, description="An address for the individual."
    )
    marital_status: Optional[CodeableConcept] = Field(
        default=None,
        alias="maritalStatus",
        description="This field contains a patient's most recent marital (civil) status.",
    )
    multiple_birth_boolean: Optional[bool] = Field(
        default=None,
        alias="multipleBirthBoolean",
        description="Indicates whether the patient is part of a multiple (boolean) or indicates the actual birth order (integer).",
    )
    multiple_birth_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="multipleBirthInteger",
        description="Indicates whether the patient is part of a multiple (boolean) or indicates the actual birth order (integer).",
    )
    photo: Optional[list[Attachment]] = Field(
        default=None, description="Image of the patient."
    )
    contact: Optional[list[PatientContact]] = Field(
        default=None,
        description="A contact party (e.g. guardian, partner, friend) for the patient.",
    )
    communication: Optional[list[PatientCommunication]] = Field(
        default=None,
        description="A language which may be used to communicate with the patient about his or her health.",
    )
    general_practitioner: Optional[list[Reference]] = Field(
        default=None,
        alias="generalPractitioner",
        description="Patient's nominated care provider.",
    )
    managing_organization: Optional[Reference] = Field(
        default=None,
        alias="managingOrganization",
        description="Organization that is the custodian of the patient record.",
    )
    link: Optional[list[PatientLink]] = Field(
        default=None,
        description="Link to another patient resource that concerns the same actual patient.",
    )


class PatientCommunication(MedplumFHIRBase):
    """A language which may be used to communicate with the patient about his
    or her health.
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
    language: CodeableConcept = Field(
        default=...,
        description="The ISO-639-1 alpha 2 code in lower case for the language, optionally followed by a hyphen and the ISO-3166-1 alpha 2 code for the region in upper case; e.g. &quot;en&quot; for English, or &quot;en-US&quot; for American English versus &quot;en-EN&quot; for England English.",
    )
    preferred: Optional[bool] = Field(
        default=None,
        description="Indicates whether or not the patient prefers this language (over other languages he masters up a certain level).",
    )


class PatientContact(MedplumFHIRBase):
    """A contact party (e.g. guardian, partner, friend) for the patient."""

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
    relationship: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="The nature of the relationship between the patient and the contact person.",
    )
    name: Optional[HumanName] = Field(
        default=None, description="A name associated with the contact person."
    )
    telecom: Optional[list[ContactPoint]] = Field(
        default=None,
        description="A contact detail for the person, e.g. a telephone number or an email address.",
    )
    address: Optional[Address] = Field(
        default=None, description="Address for the contact person."
    )
    gender: Optional[Literal["male", "female", "other", "unknown"]] = Field(
        default=None,
        description="Administrative Gender - the gender that the contact person is considered to have for administration and record keeping purposes.",
    )
    organization: Optional[Reference] = Field(
        default=None,
        description="Organization on behalf of which the contact is acting or for which the contact is working.",
    )
    period: Optional[Period] = Field(
        default=None,
        description="The period during which this contact person or organization is valid to be contacted relating to this patient.",
    )


class PatientLink(MedplumFHIRBase):
    """Link to another patient resource that concerns the same actual patient."""

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
    other: Reference = Field(
        default=..., description="The other patient resource that the link refers to."
    )
    type: Literal["replaced-by", "replaces", "refer", "seealso"] = Field(
        default=...,
        description="The type of link between this patient resource and another patient resource.",
    )
