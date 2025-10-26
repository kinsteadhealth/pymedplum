# This is a generated file
# Do not edit manually.
# Generated from Medplum TypeScript definitions
# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()

from __future__ import annotations

from typing import Literal, Optional, TypeVar, Union

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

T = TypeVar("T")

class Bundle(MedplumFHIRBase):
    """A container for a collection of resources."""

    resource_type: Literal["Bundle"] = Field(
        default="Bundle",
        alias="resourceType"
    )

    id: Optional[str] = Field(default=None, description="The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.")
    meta: Optional[Meta] = Field(default=None, description="The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.")
    implicit_rules: Optional[str] = Field(default=None, alias="implicitRules", description="A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.")
    language: Optional[str] = Field(default=None, description="The base language in which the resource is written.")
    identifier: Optional[Identifier] = Field(default=None, description="A persistent identifier for the bundle that won't change as a bundle is copied from server to server.")
    type: Literal['document', 'message', 'transaction', 'transaction-response', 'batch', 'batch-response', 'history', 'searchset', 'collection'] = Field(default=..., description="Indicates the purpose of this bundle - how it is intended to be used.")
    timestamp: Optional[str] = Field(default=None, description="The date/time that the bundle was assembled - i.e. when the resources were placed in the bundle.")
    total: Optional[Union[int, float]] = Field(default=None, description="If a set of search matches, this is the total number of entries of type 'match' across all pages in the search. It does not include search.mode = 'include' or 'outcome' entries and it does not provide a count of the number of entries in the Bundle.")
    link: Optional[list[BundleLink]] = Field(default=None, description="A series of links that provide context to this bundle.")
    entry: Optional[list[BundleEntry]] = Field(default=None, description="An entry in a bundle resource - will either contain a resource or information about a resource (transactions and history only).")
    signature: Optional[Signature] = Field(default=None, description="Digital Signature - base64 encoded. XML-DSig or a JWT.")


class BundleEntry(MedplumFHIRBase):
    """An entry in a bundle resource - will either contain a resource or
    information about a resource (transactions and history only).
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    link: Optional[list[BundleLink]] = Field(default=None, description="A series of links that provide context to this entry.")
    full_url: Optional[str] = Field(default=None, alias="fullUrl", description="The Absolute URL for the resource. The fullUrl SHALL NOT disagree with the id in the resource - i.e. if the fullUrl is not a urn:uuid, the URL shall be version-independent URL consistent with the Resource.id. The fullUrl is a version independent reference to the resource. The fullUrl element SHALL have a value except that: * fullUrl can be empty on a POST (although it does not need to when specifying a temporary id for reference in the bundle) * Results from operations might involve resources that are not identified.")
    resource: Optional[T] = Field(default=None, description="The Resource for the entry. The purpose/meaning of the resource is determined by the Bundle.type.")
    search: Optional[BundleEntrySearch] = Field(default=None, description="Information about the search process that lead to the creation of this entry.")
    request: Optional[BundleEntryRequest] = Field(default=None, description="Additional information about how this entry should be processed as part of a transaction or batch. For history, it shows how the entry was processed to create the version contained in the entry.")
    response: Optional[BundleEntryResponse] = Field(default=None, description="Indicates the results of processing the corresponding 'request' entry in the batch or transaction being responded to or what the results of an operation where when returning history.")


class BundleEntryRequest(MedplumFHIRBase):
    """Additional information about how this entry should be processed as part
    of a transaction or batch. For history, it shows how the entry was
    processed to create the version contained in the entry.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    method: Literal['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'] = Field(default=..., description="In a transaction or batch, this is the HTTP action to be executed for this entry. In a history bundle, this indicates the HTTP action that occurred.")
    url: str = Field(default=..., description="The URL for this entry, relative to the root (the address to which the request is posted).")
    if_none_match: Optional[str] = Field(default=None, alias="ifNoneMatch", description="If the ETag values match, return a 304 Not Modified status. See the API documentation for [&quot;Conditional Read&quot;](http.html#cread).")
    if_modified_since: Optional[str] = Field(default=None, alias="ifModifiedSince", description="Only perform the operation if the last updated date matches. See the API documentation for [&quot;Conditional Read&quot;](http.html#cread).")
    if_match: Optional[str] = Field(default=None, alias="ifMatch", description="Only perform the operation if the Etag value matches. For more information, see the API section [&quot;Managing Resource Contention&quot;](http.html#concurrency).")
    if_none_exist: Optional[str] = Field(default=None, alias="ifNoneExist", description="Instruct the server not to perform the create if a specified resource already exists. For further information, see the API documentation for [&quot;Conditional Create&quot;](http.html#ccreate). This is just the query portion of the URL - what follows the &quot;?&quot; (not including the &quot;?&quot;).")


class BundleEntryResponse(MedplumFHIRBase):
    """Indicates the results of processing the corresponding 'request' entry in
    the batch or transaction being responded to or what the results of an
    operation where when returning history.
    """

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    status: str = Field(default=..., description="The status code returned by processing this entry. The status SHALL start with a 3 digit HTTP code (e.g. 404) and may contain the standard HTTP description associated with the status code.")
    location: Optional[str] = Field(default=None, description="The location header created by processing this operation, populated if the operation returns a location.")
    etag: Optional[str] = Field(default=None, description="The Etag for the resource, if the operation for the entry produced a versioned resource (see [Resource Metadata and Versioning](http.html#versioning) and [Managing Resource Contention](http.html#concurrency)).")
    last_modified: Optional[str] = Field(default=None, alias="lastModified", description="The date/time that the resource was modified on the server.")
    outcome: Optional[OperationOutcome] = Field(default=None, description="An OperationOutcome containing hints and warnings produced as part of processing this entry in a batch or transaction.")


class BundleEntrySearch(MedplumFHIRBase):
    """Information about the search process that lead to the creation of this entry."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    mode: Optional[Literal['match', 'include', 'outcome']] = Field(default=None, description="Why this entry is in the result set - whether it's included as a match or because of an _include requirement, or to convey information or warning information about the search process.")
    score: Optional[Union[int, float]] = Field(default=None, description="When searching, the server's search ranking score for the entry.")


class BundleLink(MedplumFHIRBase):
    """A series of links that provide context to this bundle."""

    id: Optional[str] = Field(default=None, description="Unique id for the element within a resource (for internal references). This may be any string value that does not contain spaces.")
    extension: Optional[list[Extension]] = Field(default=None, description="May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.")
    modifier_extension: Optional[list[Extension]] = Field(default=None, alias="modifierExtension", description="May be used to represent additional information that is not part of the basic definition of the element and that modifies the understanding of the element in which it is contained and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).")
    relation: str = Field(default=..., description="A name which details the functional use for this link - see [http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1](http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1).")
    url: str = Field(default=..., description="The reference details for the link.")


# Register models for forward reference resolution
from typing import TYPE_CHECKING  # noqa: E402

if not TYPE_CHECKING:
    from pymedplum.fhir._rebuild import register_model  # noqa: E402

    register_model("Bundle", Bundle)
    register_model("BundleEntry", BundleEntry)
    register_model("BundleEntryRequest", BundleEntryRequest)
    register_model("BundleEntryResponse", BundleEntryResponse)
    register_model("BundleEntrySearch", BundleEntrySearch)
    register_model("BundleLink", BundleLink)
