"""
Medplum-specific exceptions for better error handling.

These exceptions map to HTTP status codes and common error scenarios,
enabling targeted exception handling and clearer debugging.
"""

from typing import Any, Optional


class MedplumError(Exception):
    """
    Base exception for all Medplum errors.

    All Medplum-specific exceptions inherit from this,
    allowing catching all Medplum errors with one except block.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[dict] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class OperationOutcomeError(MedplumError):
    """FHIR OperationOutcome error with full context"""

    def __init__(self, status: int, outcome: Optional[dict[str, Any]], text: str):
        self.status = status
        self.outcome = outcome
        self.text = text
        super().__init__(
            f"{status}: {outcome or text[:200]}",
            status_code=status,
            response_data=outcome,
        )


class AuthenticationError(MedplumError):
    """
    Authentication failed or token expired.

    Raised when:
    - Client credentials are invalid
    - Access token has expired
    - Server returns 401 Unauthorized

    Recovery:
    - Check client_id and client_secret
    - Re-authenticate
    - Refresh token
    """

    pass


class AuthorizationError(MedplumError):
    """
    User lacks permission for requested resource.

    Raised when:
    - User doesn't have access to resource
    - Server returns 403 Forbidden
    - on_behalf_of membership has insufficient permissions

    Recovery:
    - Verify user permissions in Medplum
    - Check ProjectMembership access rules
    - Use different on_behalf_of membership
    """

    pass


class NotFoundError(MedplumError):
    """
    Requested FHIR resource not found.

    Raised when:
    - Resource ID doesn't exist
    - Resource was deleted
    - Server returns 404 Not Found

    Recovery:
    - Verify resource ID is correct
    - Check if resource was deleted
    - Search instead of direct read
    """

    pass


class ResourceNotFoundError(NotFoundError):
    """Alias for NotFoundError for consistency with plan"""

    pass


class BadRequestError(MedplumError):
    """Error for 400 Bad Request responses"""

    pass


class ValidationError(MedplumError):
    """
    Resource data failed FHIR validation.

    Raised when:
    - Creating resource with invalid data
    - Updating resource with invalid data
    - Server returns 400 Bad Request with validation errors

    Recovery:
    - Review FHIR spec for resource type
    - Check required fields are present
    - Verify field values match allowed patterns
    """

    pass


class RateLimitError(MedplumError):
    """
    Rate limit exceeded.

    Raised when:
    - Too many requests in time window
    - Server returns 429 Too Many Requests

    Recovery:
    - Implement exponential backoff
    - Reduce request frequency
    - Check rate limit headers
    """

    pass


class ServerError(MedplumError):
    """
    Medplum server error.

    Raised when:
    - Server returns 500+ status codes
    - Server is temporarily unavailable
    - Internal server errors

    Recovery:
    - Retry with exponential backoff
    - Check Medplum status page
    - Report to Medplum support if persistent
    """

    pass


class NetworkError(MedplumError):
    """
    Network communication error.

    Raised when:
    - Connection timeout
    - DNS resolution failure
    - Network unreachable

    Recovery:
    - Check internet connection
    - Verify Medplum base URL
    - Check firewall/proxy settings
    """

    pass
