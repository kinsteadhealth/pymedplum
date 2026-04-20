# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class MedicinalProductAuthorization(MedplumFHIRBase):
    """The regulatory authorization of a medicinal product."""

    resource_type: Literal["MedicinalProductAuthorization"] = Field(
        default="MedicinalProductAuthorization", alias="resourceType"
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
    identifier: list[Identifier] | None = Field(
        default=None,
        description="Business identifier for the marketing authorization, as assigned by a regulator.",
    )
    subject: Reference | None = Field(
        default=None, description="The medicinal product that is being authorized."
    )
    country: list[CodeableConcept] | None = Field(
        default=None,
        description="The country in which the marketing authorization has been granted.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None, description="Jurisdiction within a country."
    )
    status: CodeableConcept | None = Field(
        default=None, description="The status of the marketing authorization."
    )
    status_date: str | None = Field(
        default=None,
        alias="statusDate",
        description="The date at which the given status has become applicable.",
    )
    restore_date: str | None = Field(
        default=None,
        alias="restoreDate",
        description="The date when a suspended the marketing or the marketing authorization of the product is anticipated to be restored.",
    )
    validity_period: Period | None = Field(
        default=None,
        alias="validityPeriod",
        description="The beginning of the time period in which the marketing authorization is in the specific status shall be specified A complete date consisting of day, month and year shall be specified using the ISO 8601 date format.",
    )
    data_exclusivity_period: Period | None = Field(
        default=None,
        alias="dataExclusivityPeriod",
        description="A period of time after authorization before generic product applicatiosn can be submitted.",
    )
    date_of_first_authorization: str | None = Field(
        default=None,
        alias="dateOfFirstAuthorization",
        description="The date when the first authorization was granted by a Medicines Regulatory Agency.",
    )
    international_birth_date: str | None = Field(
        default=None,
        alias="internationalBirthDate",
        description="Date of first marketing authorization for a company's new medicinal product in any country in the World.",
    )
    legal_basis: CodeableConcept | None = Field(
        default=None,
        alias="legalBasis",
        description="The legal framework against which this authorization is granted.",
    )
    jurisdictional_authorization: (
        list[MedicinalProductAuthorizationJurisdictionalAuthorization] | None
    ) = Field(
        default=None,
        alias="jurisdictionalAuthorization",
        description="Authorization in areas within a country.",
    )
    holder: Reference | None = Field(
        default=None, description="Marketing Authorization Holder."
    )
    regulator: Reference | None = Field(
        default=None, description="Medicines Regulatory Agency."
    )
    procedure: MedicinalProductAuthorizationProcedure | None = Field(
        default=None,
        description="The regulatory procedure for granting or amending a marketing authorization.",
    )


class MedicinalProductAuthorizationJurisdictionalAuthorization(MedplumFHIRBase):
    """Authorization in areas within a country."""

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
    identifier: list[Identifier] | None = Field(
        default=None, description="The assigned number for the marketing authorization."
    )
    country: CodeableConcept | None = Field(
        default=None, description="Country of authorization."
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None, description="Jurisdiction within a country."
    )
    legal_status_of_supply: CodeableConcept | None = Field(
        default=None,
        alias="legalStatusOfSupply",
        description="The legal status of supply in a jurisdiction or region.",
    )
    validity_period: Period | None = Field(
        default=None,
        alias="validityPeriod",
        description="The start and expected end date of the authorization.",
    )


class MedicinalProductAuthorizationProcedure(MedplumFHIRBase):
    """The regulatory procedure for granting or amending a marketing authorization."""

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
    identifier: Identifier | None = Field(
        default=None, description="Identifier for this procedure."
    )
    type: CodeableConcept = Field(default=..., description="Type of procedure.")
    date_period: Period | None = Field(
        default=None, alias="datePeriod", description="Date of procedure."
    )
    date_date_time: str | None = Field(
        default=None, alias="dateDateTime", description="Date of procedure."
    )
    application: list[MedicinalProductAuthorizationProcedure] | None = Field(
        default=None,
        description="Applcations submitted to obtain a marketing authorization.",
    )
