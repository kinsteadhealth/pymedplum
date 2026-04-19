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


class SubstanceSourceMaterial(MedplumFHIRBase):
    """Source material shall capture information on the taxonomic and
    anatomical origins as well as the fraction of a material that can result
    in or can be modified to form a substance. This set of data elements
    shall be used to define polymer substances isolated from biological
    matrices. Taxonomic and anatomical origins shall be described using a
    controlled vocabulary as required. This information is captured for
    naturally derived polymers ( . starch) and structurally diverse
    substances. For Organisms belonging to the Kingdom Plantae the Substance
    level defines the fresh material of a single species or infraspecies,
    the Herbal Drug and the Herbal preparation. For Herbal preparations, the
    fraction information will be captured at the Substance information level
    and additional information for herbal extracts will be captured at the
    Specified Substance Group 1 information level. See for further
    explanation the Substance Class: Structurally Diverse and the herbal
    annex.
    """

    resource_type: Literal["SubstanceSourceMaterial"] = Field(
        default="SubstanceSourceMaterial", alias="resourceType"
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
    source_material_class: CodeableConcept | None = Field(
        default=None,
        alias="sourceMaterialClass",
        description="General high level classification of the source material specific to the origin of the material.",
    )
    source_material_type: CodeableConcept | None = Field(
        default=None,
        alias="sourceMaterialType",
        description="The type of the source material shall be specified based on a controlled vocabulary. For vaccines, this subclause refers to the class of infectious agent.",
    )
    source_material_state: CodeableConcept | None = Field(
        default=None,
        alias="sourceMaterialState",
        description="The state of the source material when extracted.",
    )
    organism_id: Identifier | None = Field(
        default=None,
        alias="organismId",
        description="The unique identifier associated with the source material parent organism shall be specified.",
    )
    organism_name: str | None = Field(
        default=None,
        alias="organismName",
        description="The organism accepted Scientific name shall be provided based on the organism taxonomy.",
    )
    parent_substance_id: list[Identifier] | None = Field(
        default=None,
        alias="parentSubstanceId",
        description="The parent of the herbal drug Ginkgo biloba, Leaf is the substance ID of the substance (fresh) of Ginkgo biloba L. or Ginkgo biloba L. (Whole plant).",
    )
    parent_substance_name: list[str] | None = Field(
        default=None,
        alias="parentSubstanceName",
        description="The parent substance of the Herbal Drug, or Herbal preparation.",
    )
    country_of_origin: list[CodeableConcept] | None = Field(
        default=None,
        alias="countryOfOrigin",
        description="The country where the plant material is harvested or the countries where the plasma is sourced from as laid down in accordance with the Plasma Master File. For &ldquo;Plasma-derived substances&rdquo; the attribute country of origin provides information about the countries used for the manufacturing of the Cryopoor plama or Crioprecipitate.",
    )
    geographical_location: list[str] | None = Field(
        default=None,
        alias="geographicalLocation",
        description="The place/region where the plant is harvested or the places/regions where the animal source material has its habitat.",
    )
    development_stage: CodeableConcept | None = Field(
        default=None,
        alias="developmentStage",
        description="Stage of life for animals, plants, insects and microorganisms. This information shall be provided only when the substance is significantly different in these stages (e.g. foetal bovine serum).",
    )
    fraction_description: list[SubstanceSourceMaterialFractionDescription] | None = (
        Field(
            default=None,
            alias="fractionDescription",
            description="Many complex materials are fractions of parts of plants, animals, or minerals. Fraction elements are often necessary to define both Substances and Specified Group 1 Substances. For substances derived from Plants, fraction information will be captured at the Substance information level ( . Oils, Juices and Exudates). Additional information for Extracts, such as extraction solvent composition, will be captured at the Specified Substance Group 1 information level. For plasma-derived products fraction information will be captured at the Substance and the Specified Substance Group 1 levels.",
        )
    )
    organism: SubstanceSourceMaterialOrganism | None = Field(
        default=None,
        description="This subclause describes the organism which the substance is derived from. For vaccines, the parent organism shall be specified based on these subclause elements. As an example, full taxonomy will be described for the Substance Name: ., Leaf.",
    )
    part_description: list[SubstanceSourceMaterialPartDescription] | None = Field(
        default=None, alias="partDescription", description="To do."
    )


class SubstanceSourceMaterialFractionDescription(MedplumFHIRBase):
    """Many complex materials are fractions of parts of plants, animals, or
    minerals. Fraction elements are often necessary to define both
    Substances and Specified Group 1 Substances. For substances derived from
    Plants, fraction information will be captured at the Substance
    information level ( . Oils, Juices and Exudates). Additional information
    for Extracts, such as extraction solvent composition, will be captured
    at the Specified Substance Group 1 information level. For plasma-derived
    products fraction information will be captured at the Substance and the
    Specified Substance Group 1 levels.
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
    fraction: str | None = Field(
        default=None,
        description="This element is capturing information about the fraction of a plant part, or human plasma for fractionation.",
    )
    material_type: CodeableConcept | None = Field(
        default=None,
        alias="materialType",
        description="The specific type of the material constituting the component. For Herbal preparations the particulars of the extracts (liquid/dry) is described in Specified Substance Group 1.",
    )


class SubstanceSourceMaterialOrganism(MedplumFHIRBase):
    """This subclause describes the organism which the substance is derived
    from. For vaccines, the parent organism shall be specified based on
    these subclause elements. As an example, full taxonomy will be described
    for the Substance Name: ., Leaf.
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
    family: CodeableConcept | None = Field(
        default=None, description="The family of an organism shall be specified."
    )
    genus: CodeableConcept | None = Field(
        default=None,
        description="The genus of an organism shall be specified; refers to the Latin epithet of the genus element of the plant/animal scientific name; it is present in names for genera, species and infraspecies.",
    )
    species: CodeableConcept | None = Field(
        default=None,
        description="The species of an organism shall be specified; refers to the Latin epithet of the species of the plant/animal; it is present in names for species and infraspecies.",
    )
    intraspecific_type: CodeableConcept | None = Field(
        default=None,
        alias="intraspecificType",
        description="The Intraspecific type of an organism shall be specified.",
    )
    intraspecific_description: str | None = Field(
        default=None,
        alias="intraspecificDescription",
        description="The intraspecific description of an organism shall be specified based on a controlled vocabulary. For Influenza Vaccine, the intraspecific description shall contain the syntax of the antigen in line with the WHO convention.",
    )
    author: list[SubstanceSourceMaterialOrganismAuthor] | None = Field(
        default=None, description="4.9.13.6.1 Author type (Conditional)."
    )
    hybrid: SubstanceSourceMaterialOrganismHybrid | None = Field(
        default=None,
        description="4.9.13.8.1 Hybrid species maternal organism ID (Optional).",
    )
    organism_general: SubstanceSourceMaterialOrganismOrganismGeneral | None = Field(
        default=None,
        alias="organismGeneral",
        description="4.9.13.7.1 Kingdom (Conditional).",
    )


class SubstanceSourceMaterialOrganismAuthor(MedplumFHIRBase):
    """4.9.13.6.1 Author type (Conditional)."""

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
    author_type: CodeableConcept | None = Field(
        default=None,
        alias="authorType",
        description="The type of author of an organism species shall be specified. The parenthetical author of an organism species refers to the first author who published the plant/animal name (of any rank). The primary author of an organism species refers to the first author(s), who validly published the plant/animal name.",
    )
    author_description: str | None = Field(
        default=None,
        alias="authorDescription",
        description="The author of an organism species shall be specified. The author year of an organism shall also be specified when applicable; refers to the year in which the first author(s) published the infraspecific plant/animal name (of any rank).",
    )


class SubstanceSourceMaterialOrganismHybrid(MedplumFHIRBase):
    """4.9.13.8.1 Hybrid species maternal organism ID (Optional)."""

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
    maternal_organism_id: str | None = Field(
        default=None,
        alias="maternalOrganismId",
        description="The identifier of the maternal species constituting the hybrid organism shall be specified based on a controlled vocabulary. For plants, the parents aren&rsquo;t always known, and it is unlikely that it will be known which is maternal and which is paternal.",
    )
    maternal_organism_name: str | None = Field(
        default=None,
        alias="maternalOrganismName",
        description="The name of the maternal species constituting the hybrid organism shall be specified. For plants, the parents aren&rsquo;t always known, and it is unlikely that it will be known which is maternal and which is paternal.",
    )
    paternal_organism_id: str | None = Field(
        default=None,
        alias="paternalOrganismId",
        description="The identifier of the paternal species constituting the hybrid organism shall be specified based on a controlled vocabulary.",
    )
    paternal_organism_name: str | None = Field(
        default=None,
        alias="paternalOrganismName",
        description="The name of the paternal species constituting the hybrid organism shall be specified.",
    )
    hybrid_type: CodeableConcept | None = Field(
        default=None,
        alias="hybridType",
        description="The hybrid type of an organism shall be specified.",
    )


class SubstanceSourceMaterialOrganismOrganismGeneral(MedplumFHIRBase):
    """4.9.13.7.1 Kingdom (Conditional)."""

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
    kingdom: CodeableConcept | None = Field(
        default=None, description="The kingdom of an organism shall be specified."
    )
    phylum: CodeableConcept | None = Field(
        default=None, description="The phylum of an organism shall be specified."
    )
    class_: CodeableConcept | None = Field(
        default=None,
        alias="class",
        description="The class of an organism shall be specified.",
    )
    order: CodeableConcept | None = Field(
        default=None, description="The order of an organism shall be specified,."
    )


class SubstanceSourceMaterialPartDescription(MedplumFHIRBase):
    """To do."""

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
    part: CodeableConcept | None = Field(
        default=None,
        description="Entity of anatomical origin of source material within an organism.",
    )
    part_location: CodeableConcept | None = Field(
        default=None,
        alias="partLocation",
        description="The detailed anatomic location when the part can be extracted from different anatomical locations of the organism. Multiple alternative locations may apply.",
    )
