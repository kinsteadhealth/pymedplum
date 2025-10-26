# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative


class SubstanceProtein(MedplumFHIRBase):
    """A SubstanceProtein is defined as a single unit of a linear amino acid
    sequence, or a combination of subunits that are either covalently linked
    or have a defined invariant stoichiometric relationship. This includes
    all synthetic, recombinant and purified SubstanceProteins of defined
    sequence, whether the use is therapeutic or prophylactic. This set of
    elements will be used to describe albumins, coagulation factors,
    cytokines, growth factors, peptide/SubstanceProtein hormones, enzymes,
    toxins, toxoids, recombinant vaccines, and immunomodulators.
    """

    resource_type: Literal["SubstanceProtein"] = Field(
        default="SubstanceProtein", alias="resourceType"
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
    sequence_type: Optional[CodeableConcept] = Field(
        default=None,
        alias="sequenceType",
        description="The SubstanceProtein descriptive elements will only be used when a complete or partial amino acid sequence is available or derivable from a nucleic acid sequence.",
    )
    number_of_subunits: Optional[Union[int, float]] = Field(
        default=None,
        alias="numberOfSubunits",
        description="Number of linear sequences of amino acids linked through peptide bonds. The number of subunits constituting the SubstanceProtein shall be described. It is possible that the number of subunits can be variable.",
    )
    disulfide_linkage: Optional[list[str]] = Field(
        default=None,
        alias="disulfideLinkage",
        description="The disulphide bond between two cysteine residues either on the same subunit or on two different subunits shall be described. The position of the disulfide bonds in the SubstanceProtein shall be listed in increasing order of subunit number and position within subunit followed by the abbreviation of the amino acids involved. The disulfide linkage positions shall actually contain the amino acid Cysteine at the respective positions.",
    )
    subunit: Optional[list[SubstanceProteinSubunit]] = Field(
        default=None,
        description="This subclause refers to the description of each subunit constituting the SubstanceProtein. A subunit is a linear sequence of amino acids linked through peptide bonds. The Subunit information shall be provided when the finished SubstanceProtein is a complex of multiple sequences; subunits are not used to delineate domains within a single sequence. Subunits are listed in order of decreasing length; sequences of the same length will be ordered by decreasing molecular weight; subunits that have identical sequences will be repeated multiple times.",
    )


class SubstanceProteinSubunit(MedplumFHIRBase):
    """This subclause refers to the description of each subunit constituting
    the SubstanceProtein. A subunit is a linear sequence of amino acids
    linked through peptide bonds. The Subunit information shall be provided
    when the finished SubstanceProtein is a complex of multiple sequences;
    subunits are not used to delineate domains within a single sequence.
    Subunits are listed in order of decreasing length; sequences of the same
    length will be ordered by decreasing molecular weight; subunits that
    have identical sequences will be repeated multiple times.
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
    subunit: Optional[Union[int, float]] = Field(
        default=None,
        description="Index of primary sequences of amino acids linked through peptide bonds in order of decreasing length. Sequences of the same length will be ordered by molecular weight. Subunits that have identical sequences will be repeated and have sequential subscripts.",
    )
    sequence: Optional[str] = Field(
        default=None,
        description="The sequence information shall be provided enumerating the amino acids from N- to C-terminal end using standard single-letter amino acid codes. Uppercase shall be used for L-amino acids and lowercase for D-amino acids. Transcribed SubstanceProteins will always be described using the translated sequence; for synthetic peptide containing amino acids that are not represented with a single letter code an X should be used within the sequence. The modified amino acids will be distinguished by their position in the sequence.",
    )
    length: Optional[Union[int, float]] = Field(
        default=None,
        description="Length of linear sequences of amino acids contained in the subunit.",
    )
    sequence_attachment: Optional[Attachment] = Field(
        default=None,
        alias="sequenceAttachment",
        description="The sequence information shall be provided enumerating the amino acids from N- to C-terminal end using standard single-letter amino acid codes. Uppercase shall be used for L-amino acids and lowercase for D-amino acids. Transcribed SubstanceProteins will always be described using the translated sequence; for synthetic peptide containing amino acids that are not represented with a single letter code an X should be used within the sequence. The modified amino acids will be distinguished by their position in the sequence.",
    )
    n_terminal_modification_id: Optional[Identifier] = Field(
        default=None,
        alias="nTerminalModificationId",
        description="Unique identifier for molecular fragment modification based on the ISO 11238 Substance ID.",
    )
    n_terminal_modification: Optional[str] = Field(
        default=None,
        alias="nTerminalModification",
        description="The name of the fragment modified at the N-terminal of the SubstanceProtein shall be specified.",
    )
    c_terminal_modification_id: Optional[Identifier] = Field(
        default=None,
        alias="cTerminalModificationId",
        description="Unique identifier for molecular fragment modification based on the ISO 11238 Substance ID.",
    )
    c_terminal_modification: Optional[str] = Field(
        default=None,
        alias="cTerminalModification",
        description="The modification at the C-terminal shall be specified.",
    )
