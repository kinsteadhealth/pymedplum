# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Meta(MedplumFHIRBase):
    """The metadata about a resource. This is content in the resource that is
    maintained by the infrastructure. Changes to the content might not
    always be associated with version changes to the resource.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    version_id: Optional[str] = Field(default=None, alias="versionId", description="The version specific identifier, as it appears in the version portion of the URL. This value changes when the resource is created, updated, or deleted.")
    last_updated: Optional[str] = Field(default=None, alias="lastUpdated", description="When the resource last changed - e.g. when the version changed.")
    source: Optional[str] = Field(default=None, description="A uri that identifies the source system of the resource. This provides a minimal amount of [Provenance](provenance.html#) information that can be used to track or differentiate the source of information in the resource. The source may identify another FHIR server, document, message, database, etc.")
    profile: Optional[list[str]] = Field(default=None, description="A list of profiles (references to [StructureDefinition](structuredefinition.html#) resources) that this resource claims to conform to. The URL is a reference to [StructureDefinition.url](structuredefinition-definitions.html#StructureDefinition.url).")
    security: Optional[list[Coding]] = Field(default=None, description="Security labels applied to this resource. These tags connect specific resources to the overall security policy and infrastructure.")
    tag: Optional[list[Coding]] = Field(default=None, description="Tags applied to this resource. Tags are intended to be used to identify and relate resources to process and workflow, and applications are not required to consider the tags when interpreting the meaning of a resource.")
    project: Optional[str] = Field(default=None, description="The project that contains this resource.")
    author: Optional[Reference] = Field(default=None, description="The individual, device or organization who initiated the last change.")
    on_behalf_of: Optional[Reference] = Field(default=None, alias="onBehalfOf", description="Optional individual, device, or organization for whom the change was made.")
    account: Optional[Reference] = Field(default=None)
    accounts: Optional[list[Reference]] = Field(default=None, description="Optional account references that can be used for sub-project compartments.")
    compartment: Optional[list[Reference]] = Field(default=None, description="The list of compartments containing this resource")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Meta", Meta)
