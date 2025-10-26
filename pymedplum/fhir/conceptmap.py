# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ConceptMap(MedplumFHIRBase):
    """A statement of relationships from one set of concepts to one or more
    other concepts - either concepts in code systems, or data element/data
    element concepts, or classes in class models.
    """

    resource_type: Literal["ConceptMap"] = Field(
        default="ConceptMap", alias="resourceType"
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
    url: Optional[str] = Field(
        default=None,
        description="An absolute URI that is used to identify this concept map when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this concept map is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the concept map is stored on different servers.",
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        description="A formal identifier that is used to identify this concept map when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the concept map when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the concept map author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: Optional[str] = Field(
        default=None,
        description="A natural language name identifying the concept map. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the concept map.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this concept map. Enables tracking the life-cycle of the content.",
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this concept map is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the concept map was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the concept map changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the concept map.",
    )
    contact: Optional[list[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the concept map from a consumer's perspective.",
    )
    use_context: Optional[list[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate concept map instances.",
    )
    jurisdiction: Optional[list[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the concept map is intended to be used.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Explanation of why this concept map is needed and why it has been designed as it has.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the concept map and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the concept map.",
    )
    source_uri: Optional[str] = Field(
        default=None,
        alias="sourceUri",
        description="Identifier for the source value set that contains the concepts that are being mapped and provides context for the mappings.",
    )
    source_canonical: Optional[str] = Field(
        default=None,
        alias="sourceCanonical",
        description="Identifier for the source value set that contains the concepts that are being mapped and provides context for the mappings.",
    )
    target_uri: Optional[str] = Field(
        default=None,
        alias="targetUri",
        description="The target value set provides context for the mappings. Note that the mapping is made between concepts, not between value sets, but the value set provides important context about how the concept mapping choices are made.",
    )
    target_canonical: Optional[str] = Field(
        default=None,
        alias="targetCanonical",
        description="The target value set provides context for the mappings. Note that the mapping is made between concepts, not between value sets, but the value set provides important context about how the concept mapping choices are made.",
    )
    group: Optional[list[ConceptMapGroup]] = Field(
        default=None,
        description="A group of mappings that all have the same source and target system.",
    )


class ConceptMapGroup(MedplumFHIRBase):
    """A group of mappings that all have the same source and target system."""

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
    source: Optional[str] = Field(
        default=None,
        description="An absolute URI that identifies the source system where the concepts to be mapped are defined.",
    )
    source_version: Optional[str] = Field(
        default=None,
        alias="sourceVersion",
        description="The specific version of the code system, as determined by the code system authority.",
    )
    target: Optional[str] = Field(
        default=None,
        description="An absolute URI that identifies the target system that the concepts will be mapped to.",
    )
    target_version: Optional[str] = Field(
        default=None,
        alias="targetVersion",
        description="The specific version of the code system, as determined by the code system authority.",
    )
    element: list[ConceptMapGroupElement] = Field(
        default=...,
        description="Mappings for an individual concept in the source to one or more concepts in the target.",
    )
    unmapped: Optional[ConceptMapGroupUnmapped] = Field(
        default=None,
        description="What to do when there is no mapping for the source concept. &quot;Unmapped&quot; does not include codes that are unmatched, and the unmapped element is ignored in a code is specified to have equivalence = unmatched.",
    )


class ConceptMapGroupElement(MedplumFHIRBase):
    """Mappings for an individual concept in the source to one or more concepts
    in the target.
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
    code: Optional[str] = Field(
        default=None,
        description="Identity (code or path) or the element/item being mapped.",
    )
    display: Optional[str] = Field(
        default=None,
        description="The display for the code. The display is only provided to help editors when editing the concept map.",
    )
    target: Optional[list[ConceptMapGroupElementTarget]] = Field(
        default=None,
        description="A concept from the target value set that this concept maps to.",
    )


class ConceptMapGroupElementTarget(MedplumFHIRBase):
    """A concept from the target value set that this concept maps to."""

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
    code: Optional[str] = Field(
        default=None,
        description="Identity (code or path) or the element/item that the map refers to.",
    )
    display: Optional[str] = Field(
        default=None,
        description="The display for the code. The display is only provided to help editors when editing the concept map.",
    )
    equivalence: Literal[
        "relatedto",
        "equivalent",
        "equal",
        "wider",
        "subsumes",
        "narrower",
        "specializes",
        "inexact",
        "unmatched",
        "disjoint",
    ] = Field(
        default=...,
        description="The equivalence between the source and target concepts (counting for the dependencies and products). The equivalence is read from target to source (e.g. the target is 'wider' than the source).",
    )
    comment: Optional[str] = Field(
        default=None,
        description="A description of status/issues in mapping that conveys additional information not represented in the structured data.",
    )
    depends_on: Optional[list[ConceptMapGroupElementTargetDependsOn]] = Field(
        default=None,
        alias="dependsOn",
        description="A set of additional dependencies for this mapping to hold. This mapping is only applicable if the specified element can be resolved, and it has the specified value.",
    )
    product: Optional[list[ConceptMapGroupElementTargetDependsOn]] = Field(
        default=None,
        description="A set of additional outcomes from this mapping to other elements. To properly execute this mapping, the specified element must be mapped to some data element or source that is in context. The mapping may still be useful without a place for the additional data elements, but the equivalence cannot be relied on.",
    )


class ConceptMapGroupElementTargetDependsOn(MedplumFHIRBase):
    """A set of additional dependencies for this mapping to hold. This mapping
    is only applicable if the specified element can be resolved, and it has
    the specified value.
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
    property: str = Field(
        default=...,
        description="A reference to an element that holds a coded value that corresponds to a code system property. The idea is that the information model carries an element somewhere that is labeled to correspond with a code system property.",
    )
    system: Optional[str] = Field(
        default=None,
        description="An absolute URI that identifies the code system of the dependency code (if the source/dependency is a value set that crosses code systems).",
    )
    value: str = Field(
        default=...,
        description="Identity (code or path) or the element/item/ValueSet/text that the map depends on / refers to.",
    )
    display: Optional[str] = Field(
        default=None,
        description="The display for the code. The display is only provided to help editors when editing the concept map.",
    )


class ConceptMapGroupUnmapped(MedplumFHIRBase):
    """What to do when there is no mapping for the source concept.
    &quot;Unmapped&quot; does not include codes that are unmatched, and the
    unmapped element is ignored in a code is specified to have equivalence =
    unmatched.
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
    mode: Literal["provided", "fixed", "other-map"] = Field(
        default=...,
        description="Defines which action to take if there is no match for the source concept in the target system designated for the group. One of 3 actions are possible: use the unmapped code (this is useful when doing a mapping between versions, and only a few codes have changed), use a fixed code (a default code), or alternatively, a reference to a different concept map can be provided (by canonical URL).",
    )
    code: Optional[str] = Field(
        default=None,
        description="The fixed code to use when the mode = 'fixed' - all unmapped codes are mapped to a single fixed code.",
    )
    display: Optional[str] = Field(
        default=None,
        description="The display for the code. The display is only provided to help editors when editing the concept map.",
    )
    url: Optional[str] = Field(
        default=None,
        description="The canonical reference to an additional ConceptMap resource instance to use for mapping if this ConceptMap resource contains no matching mapping for the source concept.",
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ConceptMap", ConceptMap)
    register_model("ConceptMapGroup", ConceptMapGroup)
    register_model("ConceptMapGroupElement", ConceptMapGroupElement)
    register_model("ConceptMapGroupElementTarget", ConceptMapGroupElementTarget)
    register_model(
        "ConceptMapGroupElementTargetDependsOn", ConceptMapGroupElementTargetDependsOn
    )
    register_model("ConceptMapGroupUnmapped", ConceptMapGroupUnmapped)
