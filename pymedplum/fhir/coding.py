# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Coding(MedplumFHIRBase):
    """A reference to a code defined by a terminology system."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    system: Optional[str] = Field(default=None, description="The identification of the code system that defines the meaning of the symbol in the code.")
    version: Optional[str] = Field(default=None, description="The version of the code system which was used when choosing this code. Note that a well-maintained code system does not need the version reported, because the meaning of codes is consistent across versions. However this cannot consistently be assured, and when the meaning is not guaranteed to be consistent, the version SHOULD be exchanged.")
    code: Optional[str] = Field(default=None, description="A symbol in syntax defined by the system. The symbol may be a predefined code or an expression in a syntax defined by the coding system (e.g. post-coordination).")
    display: Optional[str] = Field(default=None, description="A representation of the meaning of the code in the system, following the rules of the system.")
    user_selected: Optional[bool] = Field(default=None, alias="userSelected", description="Indicates that this coding was chosen by a user directly - e.g. off a pick list of available items (codes or displays).")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Coding", Coding)
