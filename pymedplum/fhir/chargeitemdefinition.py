# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ChargeItemDefinition(MedplumFHIRBase):
    """The ChargeItemDefinition resource provides the properties that apply to
    the (billing) codes necessary to calculate costs and prices. The
    properties may differ largely depending on type and realm, therefore
    this resource gives only a rough structure and requires profiling for
    each type of billing code system.
    """

    resource_type: Literal["ChargeItemDefinition"] = Field(
        default="ChargeItemDefinition", alias="resourceType"
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
    contained: Optional[List[Resource]] = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    url: str = Field(
        default=...,
        description="An absolute URI that is used to identify this charge item definition when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this charge item definition is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the charge item definition is stored on different servers.",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        description="A formal identifier that is used to identify this charge item definition when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: Optional[str] = Field(
        default=None,
        description="The identifier that is used to identify this version of the charge item definition when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the charge item definition author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence. To provide a version consistent with the Decision Support Service specification, use the format Major.Minor.Revision (e.g. 1.0.0). For more information on versioning knowledge assets, refer to the Decision Support Service specification. Note that a version is required for non-experimental active assets.",
    )
    title: Optional[str] = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the charge item definition.",
    )
    derived_from_uri: Optional[List[str]] = Field(
        default=None,
        alias="derivedFromUri",
        description="The URL pointing to an externally-defined charge item definition that is adhered to in whole or in part by this definition.",
    )
    part_of: Optional[List[str]] = Field(
        default=None,
        alias="partOf",
        description="A larger definition of which this particular definition is a component or step.",
    )
    replaces: Optional[List[str]] = Field(
        default=None,
        description="As new versions of a protocol or guideline are defined, allows identification of what versions are replaced by a new instance.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=..., description="The current state of the ChargeItemDefinition."
    )
    experimental: Optional[bool] = Field(
        default=None,
        description="A Boolean value to indicate that this charge item definition is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: Optional[str] = Field(
        default=None,
        description="The date (and optionally time) when the charge item definition was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the charge item definition changes.",
    )
    publisher: Optional[str] = Field(
        default=None,
        description="The name of the organization or individual that published the charge item definition.",
    )
    contact: Optional[List[ContactDetail]] = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: Optional[str] = Field(
        default=None,
        description="A free text natural language description of the charge item definition from a consumer's perspective.",
    )
    use_context: Optional[List[UsageContext]] = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate charge item definition instances.",
    )
    jurisdiction: Optional[List[CodeableConcept]] = Field(
        default=None,
        description="A legal or geographic region in which the charge item definition is intended to be used.",
    )
    copyright: Optional[str] = Field(
        default=None,
        description="A copyright statement relating to the charge item definition and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the charge item definition.",
    )
    approval_date: Optional[str] = Field(
        default=None,
        alias="approvalDate",
        description="The date on which the resource content was approved by the publisher. Approval happens once when the content is officially approved for usage.",
    )
    last_review_date: Optional[str] = Field(
        default=None,
        alias="lastReviewDate",
        description="The date on which the resource content was last reviewed. Review happens periodically after approval but does not change the original approval date.",
    )
    effective_period: Optional[Period] = Field(
        default=None,
        alias="effectivePeriod",
        description="The period during which the charge item definition content was or is planned to be in active use.",
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="The defined billing details in this resource pertain to the given billing code.",
    )
    instance: Optional[List[Reference]] = Field(
        default=None,
        description="The defined billing details in this resource pertain to the given product instance(s).",
    )
    applicability: Optional[List[ChargeItemDefinitionApplicability]] = Field(
        default=None,
        description="Expressions that describe applicability criteria for the billing code.",
    )
    property_group: Optional[List[ChargeItemDefinitionPropertyGroup]] = Field(
        default=None,
        alias="propertyGroup",
        description="Group of properties which are applicable under the same conditions. If no applicability rules are established for the group, then all properties always apply.",
    )


class ChargeItemDefinitionApplicability(MedplumFHIRBase):
    """Expressions that describe applicability criteria for the billing code."""

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    description: Optional[str] = Field(
        default=None,
        description="A brief, natural language description of the condition that effectively communicates the intended semantics.",
    )
    language: Optional[str] = Field(
        default=None,
        description="The media type of the language for the expression, e.g. &quot;text/cql&quot; for Clinical Query Language expressions or &quot;text/fhirpath&quot; for FHIRPath expressions.",
    )
    expression: Optional[str] = Field(
        default=None,
        description="An expression that returns true or false, indicating whether the condition is satisfied. When using FHIRPath expressions, the %context environment variable must be replaced at runtime with the ChargeItem resource to which this definition is applied.",
    )


class ChargeItemDefinitionPropertyGroup(MedplumFHIRBase):
    """Group of properties which are applicable under the same conditions. If
    no applicability rules are established for the group, then all
    properties always apply.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    applicability: Optional[List[ChargeItemDefinitionApplicability]] = Field(
        default=None,
        description="Expressions that describe applicability criteria for the priceComponent.",
    )
    price_component: Optional[List[ChargeItemDefinitionPropertyGroupPriceComponent]] = (
        Field(
            default=None,
            alias="priceComponent",
            description="The price for a ChargeItem may be calculated as a base price with surcharges/deductions that apply in certain conditions. A ChargeItemDefinition resource that defines the prices, factors and conditions that apply to a billing code is currently under development. The priceComponent element can be used to offer transparency to the recipient of the Invoice of how the prices have been calculated.",
        )
    )


class ChargeItemDefinitionPropertyGroupPriceComponent(MedplumFHIRBase):
    """The price for a ChargeItem may be calculated as a base price with
    surcharges/deductions that apply in certain conditions. A
    ChargeItemDefinition resource that defines the prices, factors and
    conditions that apply to a billing code is currently under development.
    The priceComponent element can be used to offer transparency to the
    recipient of the Invoice of how the prices have been calculated.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: Optional[List[Extension]] = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: Optional[List[Extension]] = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    type: Literal[
        "base", "surcharge", "deduction", "discount", "tax", "informational"
    ] = Field(
        default=..., description="This code identifies the type of the component."
    )
    code: Optional[CodeableConcept] = Field(
        default=None,
        description="A code that identifies the component. Codes may be used to differentiate between kinds of taxes, surcharges, discounts etc.",
    )
    factor: Optional[Union[int, float]] = Field(
        default=None,
        description="The factor that has been applied on the base price for calculating this component.",
    )
    amount: Optional[Money] = Field(
        default=None, description="The amount calculated for this component."
    )


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ChargeItemDefinition", ChargeItemDefinition)
    register_model(
        "ChargeItemDefinitionApplicability", ChargeItemDefinitionApplicability
    )
    register_model(
        "ChargeItemDefinitionPropertyGroup", ChargeItemDefinitionPropertyGroup
    )
    register_model(
        "ChargeItemDefinitionPropertyGroupPriceComponent",
        ChargeItemDefinitionPropertyGroupPriceComponent,
    )
