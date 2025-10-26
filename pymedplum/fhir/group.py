# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

class Group(MedplumFHIRBase):
    """Represents a defined collection of entities that may be discussed or
    acted upon collectively but which are not expected to act collectively,
    and are not formally or legally recognized; i.e. a collection of
    entities that isn't an Organization.
    """

    resource_type: Literal["Group"] = Field(
        default="Group",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    text: Optional[Narrative] = Field(default=None, description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.")
    contained: Optional[List[Resource]] = Field(default=None, description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    identifier: Optional[List[Identifier]] = Field(default=None, description="A unique business identifier for this group.")
    active: Optional[bool] = Field(default=None, description="Indicates whether the record for the group is available for use or is merely being retained for historical purposes.")
    type: Literal['person', 'animal', 'practitioner', 'device', 'medication', 'substance'] = Field(default=..., description="Identifies the broad classification of the kind of resources the group includes.")
    actual: bool = Field(default=..., description="If true, indicates that the resource refers to a specific group of real individuals. If false, the group defines a set of intended individuals.")
    code: Optional[CodeableConcept] = Field(default=None, description="Provides a specific type of resource the group includes; e.g. &quot;cow&quot;, &quot;syringe&quot;, etc.")
    name: Optional[str] = Field(default=None, description="A label assigned to the group for human identification and communication.")
    quantity: Optional[Union[int, float]] = Field(default=None, description="A count of the number of resource instances that are part of the group.")
    managing_entity: Optional[Reference] = Field(default=None, alias="managingEntity", description="Entity responsible for defining and maintaining Group characteristics and/or registered members.")
    characteristic: Optional[List[GroupCharacteristic]] = Field(default=None, description="Identifies traits whose presence r absence is shared by members of the group.")
    member: Optional[List[GroupMember]] = Field(default=None, description="Identifies the resource instances that are members of the group.")


class GroupCharacteristic(MedplumFHIRBase):
    """Identifies traits whose presence r absence is shared by members of the group."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    code: CodeableConcept = Field(default=..., description="A code that identifies the kind of trait being asserted.")
    value_codeable_concept: Optional[CodeableConcept] = Field(default=None, alias="valueCodeableConcept", description="The value of the trait that holds (or does not hold - see 'exclude') for members of the group.")
    value_boolean: Optional[bool] = Field(default=None, alias="valueBoolean", description="The value of the trait that holds (or does not hold - see 'exclude') for members of the group.")
    value_quantity: Optional[Quantity] = Field(default=None, alias="valueQuantity", description="The value of the trait that holds (or does not hold - see 'exclude') for members of the group.")
    value_range: Optional[Range] = Field(default=None, alias="valueRange", description="The value of the trait that holds (or does not hold - see 'exclude') for members of the group.")
    value_reference: Optional[Reference] = Field(default=None, alias="valueReference", description="The value of the trait that holds (or does not hold - see 'exclude') for members of the group.")
    exclude: bool = Field(default=..., description="If true, indicates the characteristic is one that is NOT held by members of the group.")
    period: Optional[Period] = Field(default=None, description="The period over which the characteristic is tested; e.g. the patient had an operation during the month of June.")


class GroupMember(MedplumFHIRBase):
    """Identifies the resource instances that are members of the group."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[List[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[List[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    entity: Reference = Field(default=..., description="A reference to the entity that is a member of the group. Must be consistent with Group.type. If the entity is another group, then the type must be the same.")
    period: Optional[Period] = Field(default=None, description="The period that the member was in the group, if known.")
    inactive: Optional[bool] = Field(default=None, description="A flag to indicate that the member is no longer in the group, but previously may have been a member.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model

    register_model("Group", Group)
    register_model("GroupCharacteristic", GroupCharacteristic)
    register_model("GroupMember", GroupMember)
