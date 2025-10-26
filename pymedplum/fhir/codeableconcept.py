# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class CodeableConcept(MedplumFHIRBase):
    """A concept that may be defined by a formal reference to a terminology or
    ontology or may be provided by text.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    coding: Optional[list[Coding]] = Field(default=None, description="A reference to a code defined by a terminology system.")
    text: Optional[str] = Field(default=None, description="A human language representation of the concept as seen/selected/uttered by the user who entered the data and/or which represents the intended meaning of the user.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("CodeableConcept", CodeableConcept)
