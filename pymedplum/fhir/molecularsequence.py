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
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.reference import Reference


class MolecularSequence(MedplumFHIRBase):
    """Raw data describing a biological sequence."""

    resource_type: Literal["MolecularSequence"] = Field(
        default="MolecularSequence", alias="resourceType"
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
        description="A unique identifier for this particular sequence instance. This is a FHIR-defined id.",
    )
    type: Literal["aa", "dna", "rna"] | None = Field(
        default=None, description="Amino Acid Sequence/ DNA Sequence / RNA Sequence."
    )
    coordinate_system: int | float = Field(
        default=...,
        alias="coordinateSystem",
        description="Whether the sequence is numbered starting at 0 (0-based numbering or coordinates, inclusive start, exclusive end) or starting at 1 (1-based numbering, inclusive start and inclusive end).",
    )
    patient: Reference | None = Field(
        default=None,
        description="The patient whose sequencing results are described by this resource.",
    )
    specimen: Reference | None = Field(
        default=None, description="Specimen used for sequencing."
    )
    device: Reference | None = Field(
        default=None,
        description="The method for sequencing, for example, chip information.",
    )
    performer: Reference | None = Field(
        default=None,
        description="The organization or lab that should be responsible for this result.",
    )
    quantity: Quantity | None = Field(
        default=None,
        description="The number of copies of the sequence of interest. (RNASeq).",
    )
    reference_seq: MolecularSequenceReferenceSeq | None = Field(
        default=None,
        alias="referenceSeq",
        description="A sequence that is used as a reference to describe variants that are present in a sequence analyzed.",
    )
    variant: list[MolecularSequenceVariant] | None = Field(
        default=None,
        description="The definition of variant here originates from Sequence ontology ([variant_of](http://www.sequenceontology.org/browser/current_svn/term/variant_of)). This element can represent amino acid or nucleic sequence change(including insertion,deletion,SNP,etc.) It can represent some complex mutation or segment variation with the assist of CIGAR string.",
    )
    observed_seq: str | None = Field(
        default=None,
        alias="observedSeq",
        description="Sequence that was observed. It is the result marked by referenceSeq along with variant records on referenceSeq. This shall start from referenceSeq.windowStart and end by referenceSeq.windowEnd.",
    )
    quality: list[MolecularSequenceQuality] | None = Field(
        default=None,
        description="An experimental feature attribute that defines the quality of the feature in a quantitative way, such as a phred quality score ([SO:0001686](http://www.sequenceontology.org/browser/current_svn/term/SO:0001686)).",
    )
    read_coverage: int | float | None = Field(
        default=None,
        alias="readCoverage",
        description="Coverage (read depth or depth) is the average number of reads representing a given nucleotide in the reconstructed sequence.",
    )
    repository: list[MolecularSequenceRepository] | None = Field(
        default=None,
        description="Configurations of the external repository. The repository shall store target's observedSeq or records related with target's observedSeq.",
    )
    pointer: list[Reference] | None = Field(
        default=None,
        description="Pointer to next atomic sequence which at most contains one variant.",
    )
    structure_variant: list[MolecularSequenceStructureVariant] | None = Field(
        default=None,
        alias="structureVariant",
        description="Information about chromosome structure variation.",
    )


class MolecularSequenceQuality(MedplumFHIRBase):
    """An experimental feature attribute that defines the quality of the
    feature in a quantitative way, such as a phred quality score
    ([SO:0001686](http://www.sequenceontology.org/browser/current_svn/term/SO:0001686)).
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
    type: Literal["indel", "snp", "unknown"] = Field(
        default=..., description="INDEL / SNP / Undefined variant."
    )
    standard_sequence: CodeableConcept | None = Field(
        default=None,
        alias="standardSequence",
        description="Gold standard sequence used for comparing against.",
    )
    start: int | float | None = Field(
        default=None,
        description="Start position of the sequence. If the coordinate system is either 0-based or 1-based, then start position is inclusive.",
    )
    end: int | float | None = Field(
        default=None,
        description="End position of the sequence. If the coordinate system is 0-based then end is exclusive and does not include the last position. If the coordinate system is 1-base, then end is inclusive and includes the last position.",
    )
    score: Quantity | None = Field(
        default=None,
        description="The score of an experimentally derived feature such as a p-value ([SO:0001685](http://www.sequenceontology.org/browser/current_svn/term/SO:0001685)).",
    )
    method: CodeableConcept | None = Field(
        default=None, description="Which method is used to get sequence quality."
    )
    truth_t_p: int | float | None = Field(
        default=None,
        alias="truthTP",
        description="True positives, from the perspective of the truth data, i.e. the number of sites in the Truth Call Set for which there are paths through the Query Call Set that are consistent with all of the alleles at this site, and for which there is an accurate genotype call for the event.",
    )
    query_t_p: int | float | None = Field(
        default=None,
        alias="queryTP",
        description="True positives, from the perspective of the query data, i.e. the number of sites in the Query Call Set for which there are paths through the Truth Call Set that are consistent with all of the alleles at this site, and for which there is an accurate genotype call for the event.",
    )
    truth_f_n: int | float | None = Field(
        default=None,
        alias="truthFN",
        description="False negatives, i.e. the number of sites in the Truth Call Set for which there is no path through the Query Call Set that is consistent with all of the alleles at this site, or sites for which there is an inaccurate genotype call for the event. Sites with correct variant but incorrect genotype are counted here.",
    )
    query_f_p: int | float | None = Field(
        default=None,
        alias="queryFP",
        description="False positives, i.e. the number of sites in the Query Call Set for which there is no path through the Truth Call Set that is consistent with this site. Sites with correct variant but incorrect genotype are counted here.",
    )
    gt_f_p: int | float | None = Field(
        default=None,
        alias="gtFP",
        description="The number of false positives where the non-REF alleles in the Truth and Query Call Sets match (i.e. cases where the truth is 1/1 and the query is 0/1 or similar).",
    )
    precision: int | float | None = Field(
        default=None, description="QUERY.TP / (QUERY.TP + QUERY.FP)."
    )
    recall: int | float | None = Field(
        default=None, description="TRUTH.TP / (TRUTH.TP + TRUTH.FN)."
    )
    f_score: int | float | None = Field(
        default=None,
        alias="fScore",
        description="Harmonic mean of Recall and Precision, computed as: 2 * precision * recall / (precision + recall).",
    )
    roc: MolecularSequenceQualityRoc | None = Field(
        default=None,
        description="Receiver Operator Characteristic (ROC) Curve to give sensitivity/specificity tradeoff.",
    )


class MolecularSequenceQualityRoc(MedplumFHIRBase):
    """Receiver Operator Characteristic (ROC) Curve to give
    sensitivity/specificity tradeoff.
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
    score: list[int | float] | None = Field(
        default=None,
        description="Invidual data point representing the GQ (genotype quality) score threshold.",
    )
    num_t_p: list[int | float] | None = Field(
        default=None,
        alias="numTP",
        description="The number of true positives if the GQ score threshold was set to &quot;score&quot; field value.",
    )
    num_f_p: list[int | float] | None = Field(
        default=None,
        alias="numFP",
        description="The number of false positives if the GQ score threshold was set to &quot;score&quot; field value.",
    )
    num_f_n: list[int | float] | None = Field(
        default=None,
        alias="numFN",
        description="The number of false negatives if the GQ score threshold was set to &quot;score&quot; field value.",
    )
    precision: list[int | float] | None = Field(
        default=None,
        description="Calculated precision if the GQ score threshold was set to &quot;score&quot; field value.",
    )
    sensitivity: list[int | float] | None = Field(
        default=None,
        description="Calculated sensitivity if the GQ score threshold was set to &quot;score&quot; field value.",
    )
    f_measure: list[int | float] | None = Field(
        default=None,
        alias="fMeasure",
        description="Calculated fScore if the GQ score threshold was set to &quot;score&quot; field value.",
    )


class MolecularSequenceReferenceSeq(MedplumFHIRBase):
    """A sequence that is used as a reference to describe variants that are
    present in a sequence analyzed.
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
    chromosome: CodeableConcept | None = Field(
        default=None,
        description="Structural unit composed of a nucleic acid molecule which controls its own replication through the interaction of specific proteins at one or more origins of replication ([SO:0000340](http://www.sequenceontology.org/browser/current_svn/term/SO:0000340)).",
    )
    genome_build: str | None = Field(
        default=None,
        alias="genomeBuild",
        description="The Genome Build used for reference, following GRCh build versions e.g. 'GRCh 37'. Version number must be included if a versioned release of a primary build was used.",
    )
    orientation: Literal["sense", "antisense"] | None = Field(
        default=None,
        description="A relative reference to a DNA strand based on gene orientation. The strand that contains the open reading frame of the gene is the &quot;sense&quot; strand, and the opposite complementary strand is the &quot;antisense&quot; strand.",
    )
    reference_seq_id: CodeableConcept | None = Field(
        default=None,
        alias="referenceSeqId",
        description="Reference identifier of reference sequence submitted to NCBI. It must match the type in the MolecularSequence.type field. For example, the prefix, &ldquo;NG_&rdquo; identifies reference sequence for genes, &ldquo;NM_&rdquo; for messenger RNA transcripts, and &ldquo;NP_&rdquo; for amino acid sequences.",
    )
    reference_seq_pointer: Reference | None = Field(
        default=None,
        alias="referenceSeqPointer",
        description="A pointer to another MolecularSequence entity as reference sequence.",
    )
    reference_seq_string: str | None = Field(
        default=None,
        alias="referenceSeqString",
        description="A string like &quot;ACGT&quot;.",
    )
    strand: Literal["watson", "crick"] | None = Field(
        default=None,
        description="An absolute reference to a strand. The Watson strand is the strand whose 5'-end is on the short arm of the chromosome, and the Crick strand as the one whose 5'-end is on the long arm.",
    )
    window_start: int | float | None = Field(
        default=None,
        alias="windowStart",
        description="Start position of the window on the reference sequence. If the coordinate system is either 0-based or 1-based, then start position is inclusive.",
    )
    window_end: int | float | None = Field(
        default=None,
        alias="windowEnd",
        description="End position of the window on the reference sequence. If the coordinate system is 0-based then end is exclusive and does not include the last position. If the coordinate system is 1-base, then end is inclusive and includes the last position.",
    )


class MolecularSequenceRepository(MedplumFHIRBase):
    """Configurations of the external repository. The repository shall store
    target's observedSeq or records related with target's observedSeq.
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
    type: Literal["directlink", "openapi", "login", "oauth", "other"] = Field(
        default=...,
        description="Click and see / RESTful API / Need login to see / RESTful API with authentication / Other ways to see resource.",
    )
    url: str | None = Field(
        default=None,
        description="URI of an external repository which contains further details about the genetics data.",
    )
    name: str | None = Field(
        default=None,
        description="URI of an external repository which contains further details about the genetics data.",
    )
    dataset_id: str | None = Field(
        default=None,
        alias="datasetId",
        description="Id of the variant in this external repository. The server will understand how to use this id to call for more info about datasets in external repository.",
    )
    variantset_id: str | None = Field(
        default=None,
        alias="variantsetId",
        description="Id of the variantset in this external repository. The server will understand how to use this id to call for more info about variantsets in external repository.",
    )
    readset_id: str | None = Field(
        default=None,
        alias="readsetId",
        description="Id of the read in this external repository.",
    )


class MolecularSequenceStructureVariant(MedplumFHIRBase):
    """Information about chromosome structure variation."""

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
    variant_type: CodeableConcept | None = Field(
        default=None,
        alias="variantType",
        description="Information about chromosome structure variation DNA change type.",
    )
    exact: bool | None = Field(
        default=None,
        description="Used to indicate if the outer and inner start-end values have the same meaning.",
    )
    length: int | float | None = Field(
        default=None, description="Length of the variant chromosome."
    )
    outer: MolecularSequenceStructureVariantOuter | None = Field(
        default=None, description="Structural variant outer."
    )
    inner: MolecularSequenceStructureVariantInner | None = Field(
        default=None, description="Structural variant inner."
    )


class MolecularSequenceStructureVariantInner(MedplumFHIRBase):
    """Structural variant inner."""

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
    start: int | float | None = Field(
        default=None,
        description="Structural variant inner start. If the coordinate system is either 0-based or 1-based, then start position is inclusive.",
    )
    end: int | float | None = Field(
        default=None,
        description="Structural variant inner end. If the coordinate system is 0-based then end is exclusive and does not include the last position. If the coordinate system is 1-base, then end is inclusive and includes the last position.",
    )


class MolecularSequenceStructureVariantOuter(MedplumFHIRBase):
    """Structural variant outer."""

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
    start: int | float | None = Field(
        default=None,
        description="Structural variant outer start. If the coordinate system is either 0-based or 1-based, then start position is inclusive.",
    )
    end: int | float | None = Field(
        default=None,
        description="Structural variant outer end. If the coordinate system is 0-based then end is exclusive and does not include the last position. If the coordinate system is 1-base, then end is inclusive and includes the last position.",
    )


class MolecularSequenceVariant(MedplumFHIRBase):
    """The definition of variant here originates from Sequence ontology
    ([variant_of](http://www.sequenceontology.org/browser/current_svn/term/variant_of)).
    This element can represent amino acid or nucleic sequence
    change(including insertion,deletion,SNP,etc.) It can represent some
    complex mutation or segment variation with the assist of CIGAR string.
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
    start: int | float | None = Field(
        default=None,
        description="Start position of the variant on the reference sequence. If the coordinate system is either 0-based or 1-based, then start position is inclusive.",
    )
    end: int | float | None = Field(
        default=None,
        description="End position of the variant on the reference sequence. If the coordinate system is 0-based then end is exclusive and does not include the last position. If the coordinate system is 1-base, then end is inclusive and includes the last position.",
    )
    observed_allele: str | None = Field(
        default=None,
        alias="observedAllele",
        description="An allele is one of a set of coexisting sequence variants of a gene ([SO:0001023](http://www.sequenceontology.org/browser/current_svn/term/SO:0001023)). Nucleotide(s)/amino acids from start position of sequence to stop position of sequence on the positive (+) strand of the observed sequence. When the sequence type is DNA, it should be the sequence on the positive (+) strand. This will lay in the range between variant.start and variant.end.",
    )
    reference_allele: str | None = Field(
        default=None,
        alias="referenceAllele",
        description="An allele is one of a set of coexisting sequence variants of a gene ([SO:0001023](http://www.sequenceontology.org/browser/current_svn/term/SO:0001023)). Nucleotide(s)/amino acids from start position of sequence to stop position of sequence on the positive (+) strand of the reference sequence. When the sequence type is DNA, it should be the sequence on the positive (+) strand. This will lay in the range between variant.start and variant.end.",
    )
    cigar: str | None = Field(
        default=None,
        description="Extended CIGAR string for aligning the sequence with reference bases. See detailed documentation [here](http://support.illumina.com/help/SequencingAnalysisWorkflow/Content/Vault/Informatics/Sequencing_Analysis/CASAVA/swSEQ_mCA_ExtendedCIGARFormat.htm).",
    )
    variant_pointer: Reference | None = Field(
        default=None,
        alias="variantPointer",
        description="A pointer to an Observation containing variant information.",
    )
