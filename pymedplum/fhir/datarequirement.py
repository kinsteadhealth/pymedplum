# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.reference import Reference


class DataRequirement(MedplumFHIRBase):
    """Describes a required data item for evaluation in terms of the type of
    data, and optional code or date-based filters of the data.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    type: str = Field(
        default=...,
        description="The type of the required data, specified as the type name of a resource. For profiles, this value is set to the type of the base resource of the profile.",
    )
    profile: list[str] | None = Field(
        default=None,
        description="The profile of the required data, specified as the uri of the profile definition.",
    )
    subject_codeable_concept: CodeableConcept | None = Field(
        default=None,
        alias="subjectCodeableConcept",
        description="The intended subjects of the data requirement. If this element is not provided, a Patient subject is assumed.",
    )
    subject_reference: Reference | None = Field(
        default=None,
        alias="subjectReference",
        description="The intended subjects of the data requirement. If this element is not provided, a Patient subject is assumed.",
    )
    must_support: list[str] | None = Field(
        default=None,
        alias="mustSupport",
        description="Indicates that specific elements of the type are referenced by the knowledge module and must be supported by the consumer in order to obtain an effective evaluation. This does not mean that a value is required for this element, only that the consuming system must understand the element and be able to provide values for it if they are available. The value of mustSupport SHALL be a FHIRPath resolveable on the type of the DataRequirement. The path SHALL consist only of identifiers, constant indexers, and .resolve() (see the [Simple FHIRPath Profile](fhirpath.html#simple) for full details).",
    )
    code_filter: list[DataRequirementCodeFilter] | None = Field(
        default=None,
        alias="codeFilter",
        description="Code filters specify additional constraints on the data, specifying the value set of interest for a particular element of the data. Each code filter defines an additional constraint on the data, i.e. code filters are AND'ed, not OR'ed.",
    )
    date_filter: list[DataRequirementDateFilter] | None = Field(
        default=None,
        alias="dateFilter",
        description="Date filters specify additional constraints on the data in terms of the applicable date range for specific elements. Each date filter specifies an additional constraint on the data, i.e. date filters are AND'ed, not OR'ed.",
    )
    limit: int | float | None = Field(
        default=None,
        description="Specifies a maximum number of results that are required (uses the _count search parameter).",
    )
    sort: list[DataRequirementSort] | None = Field(
        default=None, description="Specifies the order of the results to be returned."
    )


class DataRequirementCodeFilter(MedplumFHIRBase):
    """Code filters specify additional constraints on the data, specifying the
    value set of interest for a particular element of the data. Each code
    filter defines an additional constraint on the data, i.e. code filters
    are AND'ed, not OR'ed.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    path: str | None = Field(
        default=None,
        description="The code-valued attribute of the filter. The specified path SHALL be a FHIRPath resolveable on the specified type of the DataRequirement, and SHALL consist only of identifiers, constant indexers, and .resolve(). The path is allowed to contain qualifiers (.) to traverse sub-elements, as well as indexers ([x]) to traverse multiple-cardinality sub-elements (see the [Simple FHIRPath Profile](fhirpath.html#simple) for full details). Note that the index must be an integer constant. The path must resolve to an element of type code, Coding, or CodeableConcept.",
    )
    search_param: str | None = Field(
        default=None,
        alias="searchParam",
        description="A token parameter that refers to a search parameter defined on the specified type of the DataRequirement, and which searches on elements of type code, Coding, or CodeableConcept.",
    )
    value_set: str | None = Field(
        default=None,
        alias="valueSet",
        description="The valueset for the code filter. The valueSet and code elements are additive. If valueSet is specified, the filter will return only those data items for which the value of the code-valued element specified in the path is a member of the specified valueset.",
    )
    code: list[Coding] | None = Field(
        default=None,
        description="The codes for the code filter. If values are given, the filter will return only those data items for which the code-valued attribute specified by the path has a value that is one of the specified codes. If codes are specified in addition to a value set, the filter returns items matching a code in the value set or one of the specified codes.",
    )


class DataRequirementDateFilter(MedplumFHIRBase):
    """Date filters specify additional constraints on the data in terms of the
    applicable date range for specific elements. Each date filter specifies
    an additional constraint on the data, i.e. date filters are AND'ed, not
    OR'ed.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    path: str | None = Field(
        default=None,
        description="The date-valued attribute of the filter. The specified path SHALL be a FHIRPath resolveable on the specified type of the DataRequirement, and SHALL consist only of identifiers, constant indexers, and .resolve(). The path is allowed to contain qualifiers (.) to traverse sub-elements, as well as indexers ([x]) to traverse multiple-cardinality sub-elements (see the [Simple FHIRPath Profile](fhirpath.html#simple) for full details). Note that the index must be an integer constant. The path must resolve to an element of type date, dateTime, Period, Schedule, or Timing.",
    )
    search_param: str | None = Field(
        default=None,
        alias="searchParam",
        description="A date parameter that refers to a search parameter defined on the specified type of the DataRequirement, and which searches on elements of type date, dateTime, Period, Schedule, or Timing.",
    )
    value_date_time: str | None = Field(
        default=None,
        alias="valueDateTime",
        description="The value of the filter. If period is specified, the filter will return only those data items that fall within the bounds determined by the Period, inclusive of the period boundaries. If dateTime is specified, the filter will return only those data items that are equal to the specified dateTime. If a Duration is specified, the filter will return only those data items that fall within Duration before now.",
    )
    value_period: Period | None = Field(
        default=None,
        alias="valuePeriod",
        description="The value of the filter. If period is specified, the filter will return only those data items that fall within the bounds determined by the Period, inclusive of the period boundaries. If dateTime is specified, the filter will return only those data items that are equal to the specified dateTime. If a Duration is specified, the filter will return only those data items that fall within Duration before now.",
    )
    value_duration: Duration | None = Field(
        default=None,
        alias="valueDuration",
        description="The value of the filter. If period is specified, the filter will return only those data items that fall within the bounds determined by the Period, inclusive of the period boundaries. If dateTime is specified, the filter will return only those data items that are equal to the specified dateTime. If a Duration is specified, the filter will return only those data items that fall within Duration before now.",
    )


class DataRequirementSort(MedplumFHIRBase):
    """Specifies the order of the results to be returned."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    path: str = Field(
        default=...,
        description="The attribute of the sort. The specified path must be resolvable from the type of the required data. The path is allowed to contain qualifiers (.) to traverse sub-elements, as well as indexers ([x]) to traverse multiple-cardinality sub-elements. Note that the index must be an integer constant.",
    )
    direction: Literal["ascending", "descending"] = Field(
        default=..., description="The direction of the sort, ascending or descending."
    )
