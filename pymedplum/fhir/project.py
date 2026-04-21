# This is a generated file — do not edit manually.
# See NOTICE for attribution (HL7 FHIR R4 / @medplum/fhirtypes / PyMedplum)
# and LICENSE for terms.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field

from pymedplum.fhir.base import MedplumFHIRBase

if TYPE_CHECKING:
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.resourcetype import ResourceType


class Project(MedplumFHIRBase):
    """Encapsulation of resources for a specific project or organization."""

    resource_type: Literal["Project"] = Field(default="Project", alias="resourceType")

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
    identifier: list[Identifier] | None = Field(
        default=None, description="An identifier for this project."
    )
    name: str | None = Field(
        default=None, description="A name associated with the Project."
    )
    description: str | None = Field(
        default=None,
        description="A summary, characterization or explanation of the Project.",
    )
    super_admin: bool | None = Field(
        default=None,
        alias="superAdmin",
        description="Whether this project is the super administrator project. A super administrator is a user who has complete access to all resources in all projects.",
    )
    strict_mode: bool | None = Field(
        default=None,
        alias="strictMode",
        description="Whether this project uses strict FHIR validation. This setting has been deprecated, and can only be set by a super admin.",
    )
    check_references_on_write: bool | None = Field(
        default=None,
        alias="checkReferencesOnWrite",
        description="Whether this project uses referential integrity on write operations such as 'create' and 'update'.",
    )
    owner: Reference | None = Field(
        default=None, description="The user who owns the project."
    )
    features: (
        list[
            Literal[
                "ai",
                "aws-comprehend",
                "aws-textract",
                "bots",
                "cron",
                "email",
                "google-auth-required",
                "graphql-introspection",
                "websocket-subscriptions",
                "transaction-bundles",
                "validate-terminology",
            ]
        ]
        | None
    ) = Field(
        default=None,
        description="A list of optional features that are enabled for the project.",
    )
    default_patient_access_policy: Reference | None = Field(
        default=None,
        alias="defaultPatientAccessPolicy",
        description="The default access policy for patients using open registration.",
    )
    setting: list[ProjectSetting] | None = Field(
        default=None,
        description="Option or parameter that can be adjusted within the Medplum Project to customize its behavior.",
    )
    secret: list[ProjectSetting] | None = Field(
        default=None,
        description="Option or parameter that can be adjusted within the Medplum Project to customize its behavior, only visible to project administrators.",
    )
    system_setting: list[ProjectSetting] | None = Field(
        default=None,
        alias="systemSetting",
        description="Option or parameter that can be adjusted within the Medplum Project to customize its behavior, only modifiable by system administrators.",
    )
    system_secret: list[ProjectSetting] | None = Field(
        default=None,
        alias="systemSecret",
        description="Option or parameter that can be adjusted within the Medplum Project to customize its behavior, only visible to system administrators.",
    )
    site: list[ProjectSite] | None = Field(
        default=None,
        description="Web application or web site that is associated with the project.",
    )
    link: list[ProjectLink] | None = Field(
        default=None,
        description="Linked Projects whose contents are made available to this one",
    )
    default_profile: list[ProjectDefaultProfile] | None = Field(
        default=None,
        alias="defaultProfile",
        description="Default profiles to apply to resources in this project that do not individually specify profiles",
    )
    exported_resource_type: list[ResourceType] | None = Field(
        default=None,
        alias="exportedResourceType",
        description="The resource types exported by the project when linked",
    )


class ProjectDefaultProfile(MedplumFHIRBase):
    """Default profiles to apply to resources in this project that do not
    individually specify profiles
    """

    resource_type: ResourceType = Field(
        default=...,
        alias="resourceType",
        description="The resource type onto which to apply the default profiles",
    )
    profile: list[str] = Field(
        default=..., description="The profiles to add by default"
    )


class ProjectLink(MedplumFHIRBase):
    """Linked Projects whose contents are made available to this one"""

    project: Reference = Field(
        default=..., description="A reference to the Project to be linked into this one"
    )


class ProjectSetting(MedplumFHIRBase):
    """Option or parameter that can be adjusted within the Medplum Project to
    customize its behavior.
    """

    name: str = Field(default=..., description="The secret name.")
    value_string: str | None = Field(
        default=None, alias="valueString", description="The secret value."
    )
    value_boolean: bool | None = Field(
        default=None, alias="valueBoolean", description="The secret value."
    )
    value_decimal: float | None = Field(
        default=None, alias="valueDecimal", description="The secret value."
    )
    value_integer: int | None = Field(
        default=None, alias="valueInteger", description="The secret value."
    )


class ProjectSite(MedplumFHIRBase):
    """Web application or web site that is associated with the project."""

    name: str = Field(
        default=...,
        description="Friendly name that will make it easy for you to identify the site in the future.",
    )
    domain: list[str] = Field(
        default=...,
        description="The list of domain names associated with the site. User authentication will be restricted to the domains you enter here, plus any subdomains. In other words, a registration for example.com also registers subdomain.example.com. A valid domain requires a host and must not include any path, port, query or fragment.",
    )
    google_client_id: str | None = Field(
        default=None,
        alias="googleClientId",
        description="The publicly visible Google Client ID for the site. This is used to authenticate users with Google. This value is available in the Google Developer Console.",
    )
    google_client_secret: str | None = Field(
        default=None,
        alias="googleClientSecret",
        description="The private Google Client Secret for the site. This value is available in the Google Developer Console.",
    )
    recaptcha_site_key: str | None = Field(
        default=None,
        alias="recaptchaSiteKey",
        description="The publicly visible reCAPTCHA site key. This value is generated when you create a new reCAPTCHA site in the reCAPTCHA admin console. Use this site key in the HTML code your site serves to users.",
    )
    recaptcha_secret_key: str | None = Field(
        default=None,
        alias="recaptchaSecretKey",
        description="The private reCAPTCHA secret key. This value is generated when you create a new reCAPTCHA site in the reCAPTCHA admin console. Use this secret key for communication between your site and reCAPTCHA.",
    )
