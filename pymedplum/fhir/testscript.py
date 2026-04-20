# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.usagecontext import UsageContext


class TestScript(MedplumFHIRBase):
    """A structured set of tests against a FHIR server or client implementation
    to determine compliance against the FHIR specification.
    """

    resource_type: Literal["TestScript"] = Field(
        default="TestScript", alias="resourceType"
    )

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
    text: Narrative | None = Field(
        default=None,
        description="A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it &quot;clinically safe&quot; for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.",
    )
    contained: list[dict[str, Any]] | None = Field(
        default=None,
        description="These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, and nor can they have their own independent transaction scope.",
    )
    extension: list[Extension] | None = Field(
        default=None,
        description="May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
    )
    modifier_extension: list[Extension] | None = Field(
        default=None,
        alias="modifierExtension",
        description="May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and manageable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions. Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
    )
    url: str = Field(
        default=...,
        description="An absolute URI that is used to identify this test script when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which at which an authoritative instance of this test script is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the test script is stored on different servers.",
    )
    identifier: Identifier | None = Field(
        default=None,
        description="A formal identifier that is used to identify this test script when it is represented in other formats, or referenced in a specification, model, design or an instance.",
    )
    version: str | None = Field(
        default=None,
        description="The identifier that is used to identify this version of the test script when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the test script author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
    )
    name: str = Field(
        default=...,
        description="A natural language name identifying the test script. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
    )
    title: str | None = Field(
        default=None,
        description="A short, descriptive, user-friendly title for the test script.",
    )
    status: Literal["draft", "active", "retired", "unknown"] = Field(
        default=...,
        description="The status of this test script. Enables tracking the life-cycle of the content.",
    )
    experimental: bool | None = Field(
        default=None,
        description="A Boolean value to indicate that this test script is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
    )
    date: str | None = Field(
        default=None,
        description="The date (and optionally time) when the test script was published. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the test script changes.",
    )
    publisher: str | None = Field(
        default=None,
        description="The name of the organization or individual that published the test script.",
    )
    contact: list[ContactDetail] | None = Field(
        default=None,
        description="Contact details to assist a user in finding and communicating with the publisher.",
    )
    description: str | None = Field(
        default=None,
        description="A free text natural language description of the test script from a consumer's perspective.",
    )
    use_context: list[UsageContext] | None = Field(
        default=None,
        alias="useContext",
        description="The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate test script instances.",
    )
    jurisdiction: list[CodeableConcept] | None = Field(
        default=None,
        description="A legal or geographic region in which the test script is intended to be used.",
    )
    purpose: str | None = Field(
        default=None,
        description="Explanation of why this test script is needed and why it has been designed as it has.",
    )
    copyright: str | None = Field(
        default=None,
        description="A copyright statement relating to the test script and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the test script.",
    )
    origin: list[TestScriptOrigin] | None = Field(
        default=None,
        description="An abstract server used in operations within this test script in the origin element.",
    )
    destination: list[TestScriptDestination] | None = Field(
        default=None,
        description="An abstract server used in operations within this test script in the destination element.",
    )
    metadata: TestScriptMetadata | None = Field(
        default=None,
        description="The required capability must exist and are assumed to function correctly on the FHIR server being tested.",
    )
    fixture: list[TestScriptFixture] | None = Field(
        default=None,
        description="Fixture in the test script - by reference (uri). All fixtures are required for the test script to execute.",
    )
    profile: list[Reference] | None = Field(
        default=None, description="Reference to the profile to be used for validation."
    )
    variable: list[TestScriptVariable] | None = Field(
        default=None,
        description="Variable is set based either on element value in response body or on header field value in the response headers.",
    )
    setup: TestScriptSetup | None = Field(
        default=None,
        description="A series of required setup operations before tests are executed.",
    )
    test: list[TestScriptTest] | None = Field(
        default=None, description="A test in this script."
    )
    teardown: TestScriptTeardown | None = Field(
        default=None,
        description="A series of operations required to clean up after all the tests are executed (successfully or otherwise).",
    )


class TestScriptDestination(MedplumFHIRBase):
    """An abstract server used in operations within this test script in the
    destination element.
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
    index: int | float = Field(
        default=...,
        description="Abstract name given to a destination server in this test script. The name is provided as a number starting at 1.",
    )
    profile: Coding = Field(
        default=...,
        description="The type of destination profile the test system supports.",
    )


class TestScriptFixture(MedplumFHIRBase):
    """Fixture in the test script - by reference (uri). All fixtures are
    required for the test script to execute.
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
    autocreate: bool = Field(
        default=...,
        description="Whether or not to implicitly create the fixture during setup. If true, the fixture is automatically created on each server being tested during setup, therefore no create operation is required for this fixture in the TestScript.setup section.",
    )
    autodelete: bool = Field(
        default=...,
        description="Whether or not to implicitly delete the fixture during teardown. If true, the fixture is automatically deleted on each server being tested during teardown, therefore no delete operation is required for this fixture in the TestScript.teardown section.",
    )
    resource: Reference | None = Field(
        default=None,
        description="Reference to the resource (containing the contents of the resource needed for operations).",
    )


class TestScriptMetadata(MedplumFHIRBase):
    """The required capability must exist and are assumed to function correctly
    on the FHIR server being tested.
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
    link: list[TestScriptMetadataLink] | None = Field(
        default=None,
        description="A link to the FHIR specification that this test is covering.",
    )
    capability: list[TestScriptMetadataCapability] = Field(
        default=...,
        description="Capabilities that must exist and are assumed to function correctly on the FHIR server being tested.",
    )


class TestScriptMetadataCapability(MedplumFHIRBase):
    """Capabilities that must exist and are assumed to function correctly on
    the FHIR server being tested.
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
    required: bool = Field(
        default=...,
        description="Whether or not the test execution will require the given capabilities of the server in order for this test script to execute.",
    )
    validated: bool = Field(
        default=...,
        description="Whether or not the test execution will validate the given capabilities of the server in order for this test script to execute.",
    )
    description: str | None = Field(
        default=None,
        description="Description of the capabilities that this test script is requiring the server to support.",
    )
    origin: list[int | float] | None = Field(
        default=None, description="Which origin server these requirements apply to."
    )
    destination: int | float | None = Field(
        default=None, description="Which server these requirements apply to."
    )
    link: list[str] | None = Field(
        default=None,
        description="Links to the FHIR specification that describes this interaction and the resources involved in more detail.",
    )
    capabilities: str = Field(
        default=...,
        description="Minimum capabilities required of server for test script to execute successfully. If server does not meet at a minimum the referenced capability statement, then all tests in this script are skipped.",
    )


class TestScriptMetadataLink(MedplumFHIRBase):
    """A link to the FHIR specification that this test is covering."""

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
    url: str = Field(
        default=...,
        description="URL to a particular requirement or feature within the FHIR specification.",
    )
    description: str | None = Field(
        default=None, description="Short description of the link."
    )


class TestScriptOrigin(MedplumFHIRBase):
    """An abstract server used in operations within this test script in the origin element."""

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
    index: int | float = Field(
        default=...,
        description="Abstract name given to an origin server in this test script. The name is provided as a number starting at 1.",
    )
    profile: Coding = Field(
        default=..., description="The type of origin profile the test system supports."
    )


class TestScriptSetup(MedplumFHIRBase):
    """A series of required setup operations before tests are executed."""

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
    action: list[TestScriptSetupAction] = Field(
        default=...,
        description="Action would contain either an operation or an assertion.",
    )


class TestScriptSetupAction(MedplumFHIRBase):
    """Action would contain either an operation or an assertion."""

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
    operation: TestScriptSetupActionOperation | None = Field(
        default=None, description="The operation to perform."
    )
    assert_: TestScriptSetupActionAssert | None = Field(
        default=None,
        alias="assert",
        description="Evaluates the results of previous operations to determine if the server under test behaves appropriately.",
    )


class TestScriptSetupActionAssert(MedplumFHIRBase):
    """Evaluates the results of previous operations to determine if the server
    under test behaves appropriately.
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
    label: str | None = Field(
        default=None,
        description="The label would be used for tracking/logging purposes by test engines.",
    )
    description: str | None = Field(
        default=None,
        description="The description would be used by test engines for tracking and reporting purposes.",
    )
    direction: Literal["response", "request"] | None = Field(
        default=None, description="The direction to use for the assertion."
    )
    compare_to_source_id: str | None = Field(
        default=None,
        alias="compareToSourceId",
        description="Id of the source fixture used as the contents to be evaluated by either the &quot;source/expression&quot; or &quot;sourceId/path&quot; definition.",
    )
    compare_to_source_expression: str | None = Field(
        default=None,
        alias="compareToSourceExpression",
        description="The FHIRPath expression to evaluate against the source fixture. When compareToSourceId is defined, either compareToSourceExpression or compareToSourcePath must be defined, but not both.",
    )
    compare_to_source_path: str | None = Field(
        default=None,
        alias="compareToSourcePath",
        description="XPath or JSONPath expression to evaluate against the source fixture. When compareToSourceId is defined, either compareToSourceExpression or compareToSourcePath must be defined, but not both.",
    )
    content_type: str | None = Field(
        default=None,
        alias="contentType",
        description="The mime-type contents to compare against the request or response message 'Content-Type' header.",
    )
    expression: str | None = Field(
        default=None,
        description="The FHIRPath expression to be evaluated against the request or response message contents - HTTP headers and payload.",
    )
    header_field: str | None = Field(
        default=None,
        alias="headerField",
        description="The HTTP header field name e.g. 'Location'.",
    )
    minimum_id: str | None = Field(
        default=None,
        alias="minimumId",
        description="The ID of a fixture. Asserts that the response contains at a minimum the fixture specified by minimumId.",
    )
    navigation_links: bool | None = Field(
        default=None,
        alias="navigationLinks",
        description="Whether or not the test execution performs validation on the bundle navigation links.",
    )
    operator: (
        Literal[
            "equals",
            "notEquals",
            "in",
            "notIn",
            "greaterThan",
            "lessThan",
            "empty",
            "notEmpty",
            "contains",
            "notContains",
            "eval",
        ]
        | None
    ) = Field(
        default=None,
        description="The operator type defines the conditional behavior of the assert. If not defined, the default is equals.",
    )
    path: str | None = Field(
        default=None,
        description="The XPath or JSONPath expression to be evaluated against the fixture representing the response received from server.",
    )
    request_method: (
        Literal["delete", "get", "options", "patch", "post", "put", "head"] | None
    ) = Field(
        default=None,
        alias="requestMethod",
        description="The request method or HTTP operation code to compare against that used by the client system under test.",
    )
    request_u_r_l: str | None = Field(
        default=None,
        alias="requestURL",
        description="The value to use in a comparison against the request URL path string.",
    )
    resource: str | None = Field(
        default=None,
        description="The type of the resource. See http://build.fhir.org/resourcelist.html.",
    )
    response: (
        Literal[
            "okay",
            "created",
            "noContent",
            "notModified",
            "bad",
            "forbidden",
            "notFound",
            "methodNotAllowed",
            "conflict",
            "gone",
            "preconditionFailed",
            "unprocessable",
        ]
        | None
    ) = Field(
        default=None,
        description="okay | created | noContent | notModified | bad | forbidden | notFound | methodNotAllowed | conflict | gone | preconditionFailed | unprocessable.",
    )
    response_code: str | None = Field(
        default=None,
        alias="responseCode",
        description="The value of the HTTP response code to be tested.",
    )
    source_id: str | None = Field(
        default=None,
        alias="sourceId",
        description="Fixture to evaluate the XPath/JSONPath expression or the headerField against.",
    )
    validate_profile_id: str | None = Field(
        default=None,
        alias="validateProfileId",
        description="The ID of the Profile to validate against.",
    )
    value: str | None = Field(default=None, description="The value to compare to.")
    warning_only: bool = Field(
        default=...,
        alias="warningOnly",
        description="Whether or not the test execution will produce a warning only on error for this assert.",
    )


class TestScriptSetupActionOperation(MedplumFHIRBase):
    """The operation to perform."""

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
    type: Coding | None = Field(
        default=None, description="Server interaction or operation type."
    )
    resource: str | None = Field(
        default=None,
        description="The type of the resource. See http://build.fhir.org/resourcelist.html.",
    )
    label: str | None = Field(
        default=None,
        description="The label would be used for tracking/logging purposes by test engines.",
    )
    description: str | None = Field(
        default=None,
        description="The description would be used by test engines for tracking and reporting purposes.",
    )
    accept: str | None = Field(
        default=None,
        description="The mime-type to use for RESTful operation in the 'Accept' header.",
    )
    content_type: str | None = Field(
        default=None,
        alias="contentType",
        description="The mime-type to use for RESTful operation in the 'Content-Type' header.",
    )
    destination: int | float | None = Field(
        default=None,
        description="The server where the request message is destined for. Must be one of the server numbers listed in TestScript.destination section.",
    )
    encode_request_url: bool = Field(
        default=...,
        alias="encodeRequestUrl",
        description="Whether or not to implicitly send the request url in encoded format. The default is true to match the standard RESTful client behavior. Set to false when communicating with a server that does not support encoded url paths.",
    )
    method: (
        Literal["delete", "get", "options", "patch", "post", "put", "head"] | None
    ) = Field(
        default=None,
        description="The HTTP method the test engine MUST use for this operation regardless of any other operation details.",
    )
    origin: int | float | None = Field(
        default=None,
        description="The server where the request message originates from. Must be one of the server numbers listed in TestScript.origin section.",
    )
    params: str | None = Field(
        default=None,
        description="Path plus parameters after [type]. Used to set parts of the request URL explicitly.",
    )
    request_header: list[TestScriptSetupActionOperationRequestHeader] | None = Field(
        default=None,
        alias="requestHeader",
        description="Header elements would be used to set HTTP headers.",
    )
    request_id: str | None = Field(
        default=None,
        alias="requestId",
        description="The fixture id (maybe new) to map to the request.",
    )
    response_id: str | None = Field(
        default=None,
        alias="responseId",
        description="The fixture id (maybe new) to map to the response.",
    )
    source_id: str | None = Field(
        default=None,
        alias="sourceId",
        description="The id of the fixture used as the body of a PUT or POST request.",
    )
    target_id: str | None = Field(
        default=None,
        alias="targetId",
        description="Id of fixture used for extracting the [id], [type], and [vid] for GET requests.",
    )
    url: str | None = Field(default=None, description="Complete request URL.")


class TestScriptSetupActionOperationRequestHeader(MedplumFHIRBase):
    """Header elements would be used to set HTTP headers."""

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
    field: str = Field(
        default=..., description="The HTTP header field e.g. &quot;Accept&quot;."
    )
    value: str = Field(
        default=...,
        description="The value of the header e.g. &quot;application/fhir+xml&quot;.",
    )


class TestScriptTeardown(MedplumFHIRBase):
    """A series of operations required to clean up after all the tests are
    executed (successfully or otherwise).
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
    action: list[TestScriptTeardownAction] = Field(
        default=..., description="The teardown action will only contain an operation."
    )


class TestScriptTeardownAction(MedplumFHIRBase):
    """The teardown action will only contain an operation."""

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
    operation: TestScriptSetupActionOperation = Field(
        default=...,
        description="An operation would involve a REST request to a server.",
    )


class TestScriptTest(MedplumFHIRBase):
    """A test in this script."""

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
    name: str | None = Field(
        default=None,
        description="The name of this test used for tracking/logging purposes by test engines.",
    )
    description: str | None = Field(
        default=None,
        description="A short description of the test used by test engines for tracking and reporting purposes.",
    )
    action: list[TestScriptTestAction] = Field(
        default=...,
        description="Action would contain either an operation or an assertion.",
    )


class TestScriptTestAction(MedplumFHIRBase):
    """Action would contain either an operation or an assertion."""

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
    operation: TestScriptSetupActionOperation | None = Field(
        default=None,
        description="An operation would involve a REST request to a server.",
    )
    assert_: TestScriptSetupActionAssert | None = Field(
        default=None,
        alias="assert",
        description="Evaluates the results of previous operations to determine if the server under test behaves appropriately.",
    )


class TestScriptVariable(MedplumFHIRBase):
    """Variable is set based either on element value in response body or on
    header field value in the response headers.
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
    name: str = Field(default=..., description="Descriptive name for this variable.")
    default_value: str | None = Field(
        default=None,
        alias="defaultValue",
        description="A default, hard-coded, or user-defined value for this variable.",
    )
    description: str | None = Field(
        default=None,
        description="A free text natural language description of the variable and its purpose.",
    )
    expression: str | None = Field(
        default=None,
        description="The FHIRPath expression to evaluate against the fixture body. When variables are defined, only one of either expression, headerField or path must be specified.",
    )
    header_field: str | None = Field(
        default=None,
        alias="headerField",
        description="Will be used to grab the HTTP header field value from the headers that sourceId is pointing to.",
    )
    hint: str | None = Field(
        default=None,
        description="Displayable text string with hint help information to the user when entering a default value.",
    )
    path: str | None = Field(
        default=None,
        description="XPath or JSONPath to evaluate against the fixture body. When variables are defined, only one of either expression, headerField or path must be specified.",
    )
    source_id: str | None = Field(
        default=None,
        alias="sourceId",
        description="Fixture to evaluate the XPath/JSONPath expression or the headerField against within this variable.",
    )
