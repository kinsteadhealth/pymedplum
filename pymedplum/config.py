"""Configuration dataclass for Medplum clients.

This module provides a structured way to configure Medplum client instances,
encapsulating all initialization options in a type-safe dataclass.
"""

from dataclasses import dataclass

from .types import BeforeRequestCallback


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
        before_request: Callback executed before each HTTP request
        default_on_behalf_of: Default ProjectMembership for on-behalf-of operations

    Example:
        >>> config = MedplumClientConfig(
        ...     base_url="https://api.medplum.com/",
        ...     client_id="my-client-id",
        ...     client_secret="my-secret",
        ... )
        >>> client = MedplumClient(config=config)
    """

    base_url: str = "https://api.medplum.com/"
    client_id: str | None = None
    client_secret: str | None = None
    access_token: str | None = None
    fhir_url_path: str = "fhir/R4/"
    project_id: str | None = None
    before_request: BeforeRequestCallback | None = None
    default_on_behalf_of: str | None = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.base_url.endswith("/"):
            self.base_url = self.base_url + "/"

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
            "before_request": self.before_request,
            "default_on_behalf_of": self.default_on_behalf_of,
        }
