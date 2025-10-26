# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Literal, TypeVar

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

T = TypeVar("T")

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.operationoutcome import OperationOutcome
    from pymedplum.fhir.signature import Signature


class Bundle(MedplumFHIRBase):
    """A container for a collection of resources."""

    resource_type: Literal["Bundle"] = Field(default="Bundle", alias="resourceType")

    id: str | None = Field(
        default=None,
        description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
    )
    meta: Meta | None = Field(
        default=None,
        description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
    )
    implicit_rules: str | None = Field(
        default=None,
        alias="implicitRules",
        description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
    )
    language: str | None = Field(
        default=None, description="The base language in which the resource is written."
    )
    identifier: Identifier | None = Field(
        default=None,
        description="A persistent identifier for the bundle that won't change as a bundle is copied from server to server.",
    )
    type: Literal[
        "document",
        "message",
        "transaction",
        "transaction-response",
        "batch",
        "batch-response",
        "history",
        "searchset",
        "collection",
    ] = Field(
        default=...,
        description="Indicates the purpose of this bundle - how it is intended to be used.",
    )
    timestamp: str | None = Field(
        default=None,
        description="The date/time that the bundle was assembled - i.e. when the resources were placed in the bundle.",
    )
    total: int | float | None = Field(
        default=None,
        description="If a set of search matches, this is the total number of entries of type 'match' across all pages in the search. It does not include search.mode = 'include' or 'outcome' entries and it does not provide a count of the number of entries in the Bundle.",
    )
    link: list[BundleLink] | None = Field(
        default=None,
        description="A series of links that provide context to this bundle.",
    )
    entry: list[BundleEntry] | None = Field(
        default=None,
        description="An entry in a bundle resource - will either contain a resource or information about a resource (transactions and history only).",
    )
    signature: Signature | None = Field(
        default=None,
        description="Digital Signature - base64 encoded. XML-DSig or a JWT.",
    )


class BundleEntry(MedplumFHIRBase, Generic[T]):
    """An entry in a bundle resource - will either contain a resource or
    information about a resource (transactions and history only).
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    link: list[BundleLink] | None = Field(
        default=None,
        description="A series of links that provide context to this entry.",
    )
    full_url: str | None = Field(
        default=None,
        alias="fullUrl",
        description="The Absolute URL for the resource. The fullUrl SHALL NOT disagree with the id in the resource - i.e. if the fullUrl is not a urn:uuid, the URL shall be version-independent URL consistent with the Resource.id. The fullUrl is a version independent reference to the resource. The fullUrl element SHALL have a value except that: * fullUrl can be empty on a POST (although it does not need to when specifying a temporary id for reference in the bundle) * Results from operations might involve resources that are not identified.",
    )
    resource: T | None = Field(
        default=None,
        description="The Resource for the entry. The purpose/meaning of the resource is determined by the Bundle.type.",
    )
    search: BundleEntrySearch | None = Field(
        default=None,
        description="Information about the search process that lead to the creation of this entry.",
    )
    request: BundleEntryRequest | None = Field(
        default=None,
        description="Additional information about how this entry should be processed as part of a transaction or batch. For history, it shows how the entry was processed to create the version contained in the entry.",
    )
    response: BundleEntryResponse | None = Field(
        default=None,
        description="Indicates the results of processing the corresponding 'request' entry in the batch or transaction being responded to or what the results of an operation where when returning history.",
    )


class BundleEntryRequest(MedplumFHIRBase):
    """Additional information about how this entry should be processed as part
    of a transaction or batch. For history, it shows how the entry was
    processed to create the version contained in the entry.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    method: Literal["GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"] = Field(
        default=...,
        description="In a transaction or batch, this is the HTTP action to be executed for this entry. In a history bundle, this indicates the HTTP action that occurred.",
    )
    url: str = Field(
        default=...,
        description="The URL for this entry, relative to the root (the address to which the request is posted).",
    )
    if_none_match: str | None = Field(
        default=None,
        alias="ifNoneMatch",
        description="If the ETag values match, return a 304 Not Modified status. See the API documentation for [&quot;Conditional Read&quot;](http.html#cread).",
    )
    if_modified_since: str | None = Field(
        default=None,
        alias="ifModifiedSince",
        description="Only perform the operation if the last updated date matches. See the API documentation for [&quot;Conditional Read&quot;](http.html#cread).",
    )
    if_match: str | None = Field(
        default=None,
        alias="ifMatch",
        description="Only perform the operation if the Etag value matches. For more information, see the API section [&quot;Managing Resource Contention&quot;](http.html#concurrency).",
    )
    if_none_exist: str | None = Field(
        default=None,
        alias="ifNoneExist",
        description="Instruct the server not to perform the create if a specified resource already exists. For further information, see the API documentation for [&quot;Conditional Create&quot;](http.html#ccreate). This is just the query portion of the URL - what follows the &quot;?&quot; (not including the &quot;?&quot;).",
    )


class BundleEntryResponse(MedplumFHIRBase):
    """Indicates the results of processing the corresponding 'request' entry in
    the batch or transaction being responded to or what the results of an
    operation where when returning history.
    """

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    status: str = Field(
        default=...,
        description="The status code returned by processing this entry. The status SHALL start with a 3 digit HTTP code (e.g. 404) and may contain the standard HTTP description associated with the status code.",
    )
    location: str | None = Field(
        default=None,
        description="The location header created by processing this operation, populated if the operation returns a location.",
    )
    etag: str | None = Field(
        default=None,
        description="The Etag for the resource, if the operation for the entry produced a versioned resource (see [Resource Metadata and Versioning](http.html#versioning) and [Managing Resource Contention](http.html#concurrency)).",
    )
    last_modified: str | None = Field(
        default=None,
        alias="lastModified",
        description="The date/time that the resource was modified on the server.",
    )
    outcome: OperationOutcome | None = Field(
        default=None,
        description="An OperationOutcome containing hints and warnings produced as part of processing this entry in a batch or transaction.",
    )


class BundleEntrySearch(MedplumFHIRBase):
    """Information about the search process that lead to the creation of this entry."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    mode: Literal["match", "include", "outcome"] | None = Field(
        default=None,
        description="Why this entry is in the result set - whether it's included as a match or because of an _include requirement, or to convey information or warning information about the search process.",
    )
    score: int | float | None = Field(
        default=None,
        description="When searching, the server's search ranking score for the entry.",
    )


class BundleLink(MedplumFHIRBase):
    """A series of links that provide context to this bundle."""

    id: str | None = Field(
        default=None,
        description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    relation: str = Field(
        default=...,
        description="A name which details the functional use for this link - see [http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1](http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1).",
    )
    url: str = Field(default=..., description="The reference details for the link.")
