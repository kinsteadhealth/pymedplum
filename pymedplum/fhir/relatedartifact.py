# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class RelatedArtifact(MedplumFHIRBase):
    """Related artifacts such as additional documentation, justification, or
    bibliographic references.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    type: Literal['documentation', 'justification', 'citation', 'predecessor', 'successor', 'derived-from', 'depends-on', 'composed-of'] = Field(default=..., description="The type of relationship to the related artifact.")
    label: Optional[str] = Field(default=None, description="A short label that can be used to reference the citation from elsewhere in the containing artifact, such as a footnote index.")
    display: Optional[str] = Field(default=None, description="A brief description of the document or knowledge resource being referenced, suitable for display to a consumer.")
    citation: Optional[str] = Field(default=None, description="A bibliographic citation for the related artifact. This text SHOULD be formatted according to an accepted citation format.")
    url: Optional[str] = Field(default=None, description="A url for the artifact that can be followed to access the actual content.")
    document: Optional[Attachment] = Field(default=None, description="The document being referenced, represented as an attachment. This is exclusive with the resource element.")
    resource: Optional[str] = Field(default=None, description="The related resource, such as a library, value set, profile, or other knowledge resource.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("RelatedArtifact", RelatedArtifact)
