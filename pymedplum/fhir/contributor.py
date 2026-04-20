# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.extension import Extension


class Contributor(MedplumFHIRBase):
    """A contributor to the content of a knowledge asset, including authors,
    editors, reviewers, and endorsers.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    type: Literal["author", "editor", "reviewer", "endorser"] = Field(
        default=..., description="The type of contributor."
    )
    name: str = Field(
        default=...,
        description="The name of the individual or organization responsible for the contribution.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the contributor.",
    )
