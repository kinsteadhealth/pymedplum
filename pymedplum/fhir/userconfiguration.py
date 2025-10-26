# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative


class UserConfiguration(MedplumFHIRBase):
    """User specific configuration for the Medplum application."""

    resource_type: Literal["UserConfiguration"] = Field(
        default="UserConfiguration", alias="resourceType"
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
    name: Optional[str] = Field(
        default=None, description="A name associated with the UserConfiguration."
    )
    menu: Optional[list[UserConfigurationMenu]] = Field(
        default=None, description="Optional menu of shortcuts to URLs."
    )
    search: Optional[list[UserConfigurationSearch]] = Field(
        default=None, description="Shortcut links to URLs."
    )
    option: Optional[list[UserConfigurationOption]] = Field(
        default=None,
        description="User options that control the display of the application.",
    )


class UserConfigurationMenu(MedplumFHIRBase):
    """Optional menu of shortcuts to URLs."""

    title: str = Field(default=..., description="Title of the menu.")
    link: Optional[list[UserConfigurationMenuLink]] = Field(
        default=None, description="Shortcut links to URLs."
    )


class UserConfigurationMenuLink(MedplumFHIRBase):
    """Shortcut links to URLs."""

    name: str = Field(default=..., description="The human friendly name of the link.")
    target: str = Field(default=..., description="The URL target of the link.")


class UserConfigurationOption(MedplumFHIRBase):
    """User options that control the display of the application."""

    id: str = Field(default=..., description="The unique identifier of the option.")
    value_boolean: Optional[bool] = Field(
        default=None,
        alias="valueBoolean",
        description="Value of option - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_code: Optional[str] = Field(
        default=None,
        alias="valueCode",
        description="Value of option - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_decimal: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueDecimal",
        description="Value of option - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_integer: Optional[Union[int, float]] = Field(
        default=None,
        alias="valueInteger",
        description="Value of option - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )
    value_string: Optional[str] = Field(
        default=None,
        alias="valueString",
        description="Value of option - must be one of a constrained set of the data types (see [Extensibility](extensibility.html) for a list).",
    )


class UserConfigurationSearch(MedplumFHIRBase):
    """Shortcut links to URLs."""

    name: str = Field(default=..., description="The human friendly name of the link.")
    criteria: str = Field(
        default=...,
        description="The rules that the server should use to determine which resources to return.",
    )
