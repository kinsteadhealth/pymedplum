# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase


class ProdCharacteristic(MedplumFHIRBase):
    """The marketing status describes the date when a medicinal product is
    actually put on the market or the date as of which it is no longer
    available.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    height: Optional[Quantity] = Field(default=None, description="Where applicable, the height can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used.")
    width: Optional[Quantity] = Field(default=None, description="Where applicable, the width can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used.")
    depth: Optional[Quantity] = Field(default=None, description="Where applicable, the depth can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used.")
    weight: Optional[Quantity] = Field(default=None, description="Where applicable, the weight can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used.")
    nominal_volume: Optional[Quantity] = Field(default=None, alias="nominalVolume", description="Where applicable, the nominal volume can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used.")
    external_diameter: Optional[Quantity] = Field(default=None, alias="externalDiameter", description="Where applicable, the external diameter can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used.")
    shape: Optional[str] = Field(default=None, description="Where applicable, the shape can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used.")
    color: Optional[list[str]] = Field(default=None, description="Where applicable, the color can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used.")
    imprint: Optional[list[str]] = Field(default=None, description="Where applicable, the imprint can be specified as text.")
    image: Optional[list[Attachment]] = Field(default=None, description="Where applicable, the image can be provided The format of the image attachment shall be specified by regional implementations.")
    scoring: Optional[CodeableConcept] = Field(default=None, description="Where applicable, the scoring can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("ProdCharacteristic", ProdCharacteristic)
