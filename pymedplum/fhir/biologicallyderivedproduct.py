# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class BiologicallyDerivedProduct(MedplumFHIRBase):
    """A material substance originating from a biological entity intended to be
    transplanted or infused into another (possibly the same) biological
    entity.
    """

    resource_type: Literal["BiologicallyDerivedProduct"] = Field(
        default="BiologicallyDerivedProduct",
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
    identifier: Optional[list[Identifier]] = Field(default=None, description="This records identifiers associated with this biologically derived product instance that are defined by business processes and/or used to refer to it when a direct URL reference to the resource itself is not appropriate (e.g. in CDA documents, or in written / printed documentation).")
    product_category: Optional[Literal['organ', 'tissue', 'fluid', 'cells', 'biologicalAgent']] = Field(default=None, alias="productCategory", description="Broad category of this product.")
    product_code: Optional[CodeableConcept] = Field(default=None, alias="productCode", description="A code that identifies the kind of this biologically derived product (SNOMED Ctcode).")
    status: Optional[Literal['available', 'unavailable']] = Field(default=None, description="Whether the product is currently available.")
    request: Optional[list[Reference]] = Field(default=None, description="Procedure request to obtain this biologically derived product.")
    quantity: Optional[Union[int, float]] = Field(default=None, description="Number of discrete units within this product.")
    parent: Optional[list[Reference]] = Field(default=None, description="Parent product (if any).")
    collection: Optional[BiologicallyDerivedProductCollection] = Field(default=None, description="How this product was collected.")
    processing: Optional[list[BiologicallyDerivedProductProcessing]] = Field(default=None, description="Any processing of the product during collection that does not change the fundamental nature of the product. For example adding anti-coagulants during the collection of Peripheral Blood Stem Cells.")
    manipulation: Optional[BiologicallyDerivedProductManipulation] = Field(default=None, description="Any manipulation of product post-collection that is intended to alter the product. For example a buffy-coat enrichment or CD8 reduction of Peripheral Blood Stem Cells to make it more suitable for infusion.")
    storage: Optional[list[BiologicallyDerivedProductStorage]] = Field(default=None, description="Product storage.")


class BiologicallyDerivedProductCollection(MedplumFHIRBase):
    """How this product was collected."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    collector: Optional[Reference] = Field(default=None, description="Healthcare professional who is performing the collection.")
    source: Optional[Reference] = Field(default=None, description="The patient or entity, such as a hospital or vendor in the case of a processed/manipulated/manufactured product, providing the product.")
    collected_date_time: Optional[str] = Field(default=None, alias="collectedDateTime", description="Time of product collection.")
    collected_period: Optional[Period] = Field(default=None, alias="collectedPeriod", description="Time of product collection.")


class BiologicallyDerivedProductManipulation(MedplumFHIRBase):
    """Any manipulation of product post-collection that is intended to alter
    the product. For example a buffy-coat enrichment or CD8 reduction of
    Peripheral Blood Stem Cells to make it more suitable for infusion.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    description: Optional[str] = Field(default=None, description="Description of manipulation.")
    time_date_time: Optional[str] = Field(default=None, alias="timeDateTime", description="Time of manipulation.")
    time_period: Optional[Period] = Field(default=None, alias="timePeriod", description="Time of manipulation.")


class BiologicallyDerivedProductProcessing(MedplumFHIRBase):
    """Any processing of the product during collection that does not change the
    fundamental nature of the product. For example adding anti-coagulants
    during the collection of Peripheral Blood Stem Cells.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    description: Optional[str] = Field(default=None, description="Description of of processing.")
    procedure: Optional[CodeableConcept] = Field(default=None, description="Procesing code.")
    additive: Optional[Reference] = Field(default=None, description="Substance added during processing.")
    time_date_time: Optional[str] = Field(default=None, alias="timeDateTime", description="Time of processing.")
    time_period: Optional[Period] = Field(default=None, alias="timePeriod", description="Time of processing.")


class BiologicallyDerivedProductStorage(MedplumFHIRBase):
    """Product storage."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    description: Optional[str] = Field(default=None, description="Description of storage.")
    temperature: Optional[Union[int, float]] = Field(default=None, description="Storage temperature.")
    scale: Optional[Literal['farenheit', 'celsius', 'kelvin']] = Field(default=None, description="Temperature scale used.")
    duration: Optional[Period] = Field(default=None, description="Storage timeperiod.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("BiologicallyDerivedProduct", BiologicallyDerivedProduct)
    register_model("BiologicallyDerivedProductCollection", BiologicallyDerivedProductCollection)
    register_model("BiologicallyDerivedProductManipulation", BiologicallyDerivedProductManipulation)
    register_model("BiologicallyDerivedProductProcessing", BiologicallyDerivedProductProcessing)
    register_model("BiologicallyDerivedProductStorage", BiologicallyDerivedProductStorage)
