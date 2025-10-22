from typing import Any, Optional


class MedplumError(Exception):
    """Base exception for Medplum SDK"""

    pass


class OperationOutcomeError(MedplumError):
    """FHIR OperationOutcome error with full context"""

    def __init__(self, status: int, outcome: Optional[dict[str, Any]], text: str):
        self.status = status
        self.outcome = outcome
        self.text = text
        super().__init__(f"{status}: {outcome or text[:200]}")


class AuthenticationError(MedplumError):
    """Error for 401 Unauthorized responses"""

    pass


class AuthorizationError(MedplumError):
    """Error for 403 Forbidden responses"""

    pass


class NotFoundError(MedplumError):
    """Error for 404 Not Found responses"""

    pass


class BadRequestError(MedplumError):
    """Error for 400 Bad Request responses"""

    pass
