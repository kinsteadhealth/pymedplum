# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class SubstanceNucleicAcid(MedplumFHIRBase):
    """Nucleic acids are defined by three distinct elements: the base, sugar
    and linkage. Individual substance/moiety IDs will be created for each of
    these elements. The nucleotide sequence will be always entered in the
    5&rsquo;-3&rsquo; direction.
    """

    resource_type: Literal["SubstanceNucleicAcid"] = Field(
        default="SubstanceNucleicAcid",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    sequence_type: Optional[CodeableConcept] = Field(default=None, alias="sequenceType", description="The type of the sequence shall be specified based on a controlled vocabulary.")
    number_of_subunits: Optional[Union[int, float]] = Field(default=None, alias="numberOfSubunits", description="The number of linear sequences of nucleotides linked through phosphodiester bonds shall be described. Subunits would be strands of nucleic acids that are tightly associated typically through Watson-Crick base pairing. NOTE: If not specified in the reference source, the assumption is that there is 1 subunit.")
    area_of_hybridisation: Optional[str] = Field(default=None, alias="areaOfHybridisation", description="The area of hybridisation shall be described if applicable for double stranded RNA or DNA. The number associated with the subunit followed by the number associated to the residue shall be specified in increasing order. The underscore &ldquo;&rdquo; shall be used as separator as follows: &ldquo;Subunitnumber Residue&rdquo;.")
    oligo_nucleotide_type: Optional[CodeableConcept] = Field(default=None, alias="oligoNucleotideType", description="(TBC).")
    subunit: Optional[List[SubstanceNucleicAcidSubunit]] = Field(default=None, description="Subunits are listed in order of decreasing length; sequences of the same length will be ordered by molecular weight; subunits that have identical sequences will be repeated multiple times.")


class SubstanceNucleicAcidSubunit(MedplumFHIRBase):
    """Subunits are listed in order of decreasing length; sequences of the same
    length will be ordered by molecular weight; subunits that have identical
    sequences will be repeated multiple times.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    subunit: Optional[Union[int, float]] = Field(default=None, description="Index of linear sequences of nucleic acids in order of decreasing length. Sequences of the same length will be ordered by molecular weight. Subunits that have identical sequences will be repeated and have sequential subscripts.")
    sequence: Optional[str] = Field(default=None, description="Actual nucleotide sequence notation from 5' to 3' end using standard single letter codes. In addition to the base sequence, sugar and type of phosphate or non-phosphate linkage should also be captured.")
    length: Optional[Union[int, float]] = Field(default=None, description="The length of the sequence shall be captured.")
    sequence_attachment: Optional[Attachment] = Field(default=None, alias="sequenceAttachment", description="(TBC).")
    five_prime: Optional[CodeableConcept] = Field(default=None, alias="fivePrime", description="The nucleotide present at the 5&rsquo; terminal shall be specified based on a controlled vocabulary. Since the sequence is represented from the 5' to the 3' end, the 5&rsquo; prime nucleotide is the letter at the first position in the sequence. A separate representation would be redundant.")
    three_prime: Optional[CodeableConcept] = Field(default=None, alias="threePrime", description="The nucleotide present at the 3&rsquo; terminal shall be specified based on a controlled vocabulary. Since the sequence is represented from the 5' to the 3' end, the 5&rsquo; prime nucleotide is the letter at the last position in the sequence. A separate representation would be redundant.")
    linkage: Optional[List[SubstanceNucleicAcidSubunitLinkage]] = Field(default=None, description="The linkages between sugar residues will also be captured.")
    sugar: Optional[List[SubstanceNucleicAcidSubunitSugar]] = Field(default=None, description="5.3.6.8.1 Sugar ID (Mandatory).")


class SubstanceNucleicAcidSubunitLinkage(MedplumFHIRBase):
    """The linkages between sugar residues will also be captured."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    connectivity: Optional[str] = Field(default=None, description="The entity that links the sugar residues together should also be captured for nearly all naturally occurring nucleic acid the linkage is a phosphate group. For many synthetic oligonucleotides phosphorothioate linkages are often seen. Linkage connectivity is assumed to be 3&rsquo;-5&rsquo;. If the linkage is either 3&rsquo;-3&rsquo; or 5&rsquo;-5&rsquo; this should be specified.")
    identifier: Optional[Identifier] = Field(default=None, description="Each linkage will be registered as a fragment and have an ID.")
    name: Optional[str] = Field(default=None, description="Each linkage will be registered as a fragment and have at least one name. A single name shall be assigned to each linkage.")
    residue_site: Optional[str] = Field(default=None, alias="residueSite", description="Residues shall be captured as described in 5.3.6.8.3.")


class SubstanceNucleicAcidSubunitSugar(MedplumFHIRBase):
    """5.3.6.8.1 Sugar ID (Mandatory)."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[Identifier] = Field(default=None, description="The Substance ID of the sugar or sugar-like component that make up the nucleotide.")
    name: Optional[str] = Field(default=None, description="The name of the sugar or sugar-like component that make up the nucleotide.")
    residue_site: Optional[str] = Field(default=None, alias="residueSite", description="The residues that contain a given sugar will be captured. The order of given residues will be captured in the 5&lsquo;-3&lsquo;direction consistent with the base sequences listed above.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("SubstanceNucleicAcid", SubstanceNucleicAcid)
    register_model("SubstanceNucleicAcidSubunit", SubstanceNucleicAcidSubunit)
    register_model("SubstanceNucleicAcidSubunitLinkage", SubstanceNucleicAcidSubunitLinkage)
    register_model("SubstanceNucleicAcidSubunitSugar", SubstanceNucleicAcidSubunitSugar)
