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
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.marketingstatus import MarketingStatus
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference


class MedicinalProduct(MedplumFHIRBase):
    """Detailed definition of a medicinal product, typically for uses other
    than direct patient care (e.g. regulatory use).
    """

    resource_type: Literal["MedicinalProduct"] = Field(
        default="MedicinalProduct", alias="resourceType"
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
        description="Business identifier for this product. Could be an MPID.",
    )
    type: CodeableConcept | None = Field(
        default=None, description="Regulatory type, e.g. Investigational or Authorized."
    )
    domain: Coding | None = Field(
        default=None,
        description="If this medicine applies to human or veterinary uses.",
    )
    combined_pharmaceutical_dose_form: CodeableConcept | None = Field(
        default=None,
        alias="combinedPharmaceuticalDoseForm",
        description="The dose form for a single part product, or combined form of a multiple part product.",
    )
    legal_status_of_supply: CodeableConcept | None = Field(
        default=None,
        alias="legalStatusOfSupply",
        description="The legal status of supply of the medicinal product as classified by the regulator.",
    )
    additional_monitoring_indicator: CodeableConcept | None = Field(
        default=None,
        alias="additionalMonitoringIndicator",
        description="Whether the Medicinal Product is subject to additional monitoring for regulatory reasons.",
    )
    special_measures: list[str] | None = Field(
        default=None,
        alias="specialMeasures",
        description="Whether the Medicinal Product is subject to special measures for regulatory reasons.",
    )
    paediatric_use_indicator: CodeableConcept | None = Field(
        default=None,
        alias="paediatricUseIndicator",
        description="If authorised for use in children.",
    )
    product_classification: list[CodeableConcept] | None = Field(
        default=None,
        alias="productClassification",
        description="Allows the product to be classified by various systems.",
    )
    marketing_status: list[MarketingStatus] | None = Field(
        default=None,
        alias="marketingStatus",
        description="Marketing status of the medicinal product, in contrast to marketing authorizaton.",
    )
    pharmaceutical_product: list[Reference] | None = Field(
        default=None,
        alias="pharmaceuticalProduct",
        description="Pharmaceutical aspects of product.",
    )
    packaged_medicinal_product: list[Reference] | None = Field(
        default=None,
        alias="packagedMedicinalProduct",
        description="Package representation for the product.",
    )
    attached_document: list[Reference] | None = Field(
        default=None,
        alias="attachedDocument",
        description="Supporting documentation, typically for regulatory submission.",
    )
    master_file: list[Reference] | None = Field(
        default=None,
        alias="masterFile",
        description="A master file for to the medicinal product (e.g. Pharmacovigilance System Master File).",
    )
    contact: list[Reference] | None = Field(
        default=None,
        description="A product specific contact, person (in a role), or an organization.",
    )
    clinical_trial: list[Reference] | None = Field(
        default=None,
        alias="clinicalTrial",
        description="Clinical trials or studies that this product is involved in.",
    )
    name: list[MedicinalProductName] = Field(
        default=...,
        description="The product's name, including full name and possibly coded parts.",
    )
    cross_reference: list[Identifier] | None = Field(
        default=None,
        alias="crossReference",
        description="Reference to another product, e.g. for linking authorised to investigational product.",
    )
    manufacturing_business_operation: (
        list[MedicinalProductManufacturingBusinessOperation] | None
    ) = Field(
        default=None,
        alias="manufacturingBusinessOperation",
        description="An operation applied to the product, for manufacturing or adminsitrative purpose.",
    )
    special_designation: list[MedicinalProductSpecialDesignation] | None = Field(
        default=None,
        alias="specialDesignation",
        description="Indicates if the medicinal product has an orphan designation for the treatment of a rare disease.",
    )


class MedicinalProductManufacturingBusinessOperation(MedplumFHIRBase):
    """An operation applied to the product, for manufacturing or adminsitrative purpose."""

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
    operation_type: CodeableConcept | None = Field(
        default=None,
        alias="operationType",
        description="The type of manufacturing operation.",
    )
    authorisation_reference_number: Identifier | None = Field(
        default=None,
        alias="authorisationReferenceNumber",
        description="Regulatory authorization reference number.",
    )
    effective_date: str | None = Field(
        default=None,
        alias="effectiveDate",
        description="Regulatory authorization date.",
    )
    confidentiality_indicator: CodeableConcept | None = Field(
        default=None,
        alias="confidentialityIndicator",
        description="To indicate if this proces is commercially confidential.",
    )
    manufacturer: list[Reference] | None = Field(
        default=None,
        description="The manufacturer or establishment associated with the process.",
    )
    regulator: Reference | None = Field(
        default=None, description="A regulator which oversees the operation."
    )


class MedicinalProductName(MedplumFHIRBase):
    """The product's name, including full name and possibly coded parts."""

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
    product_name: str = Field(
        default=..., alias="productName", description="The full product name."
    )
    name_part: list[MedicinalProductNameNamePart] | None = Field(
        default=None,
        alias="namePart",
        description="Coding words or phrases of the name.",
    )
    country_language: list[MedicinalProductNameCountryLanguage] | None = Field(
        default=None,
        alias="countryLanguage",
        description="Country where the name applies.",
    )


class MedicinalProductNameCountryLanguage(MedplumFHIRBase):
    """Country where the name applies."""

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
    country: CodeableConcept = Field(
        default=..., description="Country code for where this name applies."
    )
    jurisdiction: CodeableConcept | None = Field(
        default=None, description="Jurisdiction code for where this name applies."
    )
    language: CodeableConcept = Field(
        default=..., description="Language code for this name."
    )


class MedicinalProductNameNamePart(MedplumFHIRBase):
    """Coding words or phrases of the name."""

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
    part: str = Field(default=..., description="A fragment of a product name.")
    type: Coding = Field(
        default=...,
        description="Idenifying type for this part of the name (e.g. strength part).",
    )


class MedicinalProductSpecialDesignation(MedplumFHIRBase):
    """Indicates if the medicinal product has an orphan designation for the
    treatment of a rare disease.
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
    identifier: list[Identifier] | None = Field(
        default=None, description="Identifier for the designation, or procedure number."
    )
    type: CodeableConcept | None = Field(
        default=None,
        description="The type of special designation, e.g. orphan drug, minor use.",
    )
    intended_use: CodeableConcept | None = Field(
        default=None,
        alias="intendedUse",
        description="The intended use of the product, e.g. prevention, treatment.",
    )
    indication_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="indicationCodeableConcept",
        description="Condition for which the medicinal use applies.",
    )
    indication_reference: Reference | None = Field(
        default=None,
        alias="indicationReference",
        description="Condition for which the medicinal use applies.",
    )
    status: CodeableConcept | None = Field(
        default=None, description="For example granted, pending, expired or withdrawn."
    )
    date: str | None = Field(
        default=None, description="Date when the designation was granted."
    )
    species: CodeableConcept | None = Field(
        default=None, description="Animal species for which this applies."
    )
