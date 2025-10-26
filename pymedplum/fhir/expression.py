# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class Expression(MedplumFHIRBase):
    """A expression that is evaluated in a specified context and returns a
    value. The context of use of the expression must specify the context in
    which the expression is evaluated, and how the result of the expression
    is used.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    description: Optional[str] = Field(default=None, description="A brief, natural language description of the condition that effectively communicates the intended semantics.")
    name: Optional[str] = Field(default=None, description="A short name assigned to the expression to allow for multiple reuse of the expression in the context where it is defined.")
    language: Literal['text/cql', 'text/fhirpath', 'application/x-fhir-query'] = Field(default=..., description="The media type of the language for the expression.")
    expression: Optional[str] = Field(default=None, description="An expression in the specified language that returns a value.")
    reference: Optional[str] = Field(default=None, description="A URI that defines where the expression is found.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Expression", Expression)
