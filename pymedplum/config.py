"""Configuration dataclass for Medplum clients.

This module provides a structured way to configure Medplum client instances,
encapsulating all initialization options in a type-safe dataclass.
"""

from dataclasses import dataclass
from typing import Optional

from .types import DEFAULT_ORG_EXTENSION_URL, BeforeRequestCallback, OrgMode


@dataclass
class MedplumClientConfig:
    """Configuration for Medplum client initialization.

    This dataclass encapsulates all configuration options for both
    MedplumClient and AsyncMedplumClient, providing a clean, type-safe
    way to configure client instances.

    Args:
        base_url: Medplum server base URL (default: https://api.medplum.com/)
        client_id: OAuth2 client ID for authentication
        client_secret: OAuth2 client secret for authentication
        access_token: Pre-existing access token (optional)
        fhir_url_path: FHIR API path relative to base_url (default: fhir/R4/)
        project_id: Medplum project ID (optional)
        org_mode: Multi-organization mode ("accounts" or "extension")
        org_ref: Organization reference for multi-org mode
        org_extension_url: Custom extension URL for org mode
        before_request: Callback executed before each HTTP request
        default_on_behalf_of: Default ProjectMembership for on-behalf-of operations

    Example:
        >>> config = MedplumClientConfig(
        ...     base_url="https://api.medplum.com/",
        ...     client_id="my-client-id",
        ...     client_secret="my-secret",
        ...     org_mode="accounts",
        ...     org_ref="Organization/123"
        ... )
        >>> client = MedplumClient(config=config)
    """

    base_url: str = "https://api.medplum.com/"
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    access_token: Optional[str] = None
    fhir_url_path: str = "fhir/R4/"
    project_id: Optional[str] = None
    org_mode: Optional[OrgMode] = None
    org_ref: Optional[str] = None
    org_extension_url: str = DEFAULT_ORG_EXTENSION_URL
    before_request: Optional[BeforeRequestCallback] = None
    default_on_behalf_of: Optional[str] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Ensure base_url ends with /
        if not self.base_url.endswith("/"):
            self.base_url = self.base_url + "/"

        # Validate org_mode if set
        if self.org_mode and self.org_mode not in ("accounts", "extension"):
            raise ValueError(
                f"Invalid org_mode: {self.org_mode}. Must be 'accounts' or 'extension'"
            )

        # Validate org configuration
        if self.org_mode and not self.org_ref:
            raise ValueError("org_ref is required when org_mode is set")

    def to_dict(self) -> dict:
        """Convert config to dictionary for client initialization.

        Returns:
            Dict of configuration parameters
        """
        return {
            "base_url": self.base_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "access_token": self.access_token,
            "fhir_url_path": self.fhir_url_path,
            "project_id": self.project_id,
            "org_mode": self.org_mode,
            "org_ref": self.org_ref,
            "org_extension_url": self.org_extension_url,
            "before_request": self.before_request,
            "default_on_behalf_of": self.default_on_behalf_of,
        }
