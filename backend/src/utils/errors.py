"""Custom exceptions and error handling utilities."""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to JSON-serializable dict."""
        return {
            "error": self.message,
            "code": self.code,
            "status": self.status_code,
            **self.details,
        }


class UnauthorizedError(AppException):
    """401 Unauthorized - Invalid or missing authentication."""

    def __init__(
        self,
        message: str = "Please log in to continue",
        code: str = "UNAUTHORIZED",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=401,
            details=details,
        )


class ForbiddenError(AppException):
    """403 Forbidden - User lacks permission to access resource."""

    def __init__(
        self,
        message: str = "You don't have permission to access this resource",
        code: str = "FORBIDDEN",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=403,
            details=details,
        )


class NotFoundError(AppException):
    """404 Not Found - Resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=404,
            details=details,
        )


class ValidationError(AppException):
    """400 Bad Request - Invalid input data."""

    def __init__(
        self,
        message: str = "Invalid input",
        code: str = "INVALID_INPUT",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=400,
            details=details,
        )


class ConflictError(AppException):
    """409 Conflict - Resource already exists or state conflict."""

    def __init__(
        self,
        message: str = "Resource already exists",
        code: str = "CONFLICT",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=409,
            details=details,
        )


# Common error messages
ERROR_MESSAGES = {
    "UNAUTHORIZED": "Please log in to continue",
    "FORBIDDEN": "You don't have permission to access this resource",
    "NOT_FOUND": "Resource not found",
    "TASK_NOT_FOUND": "Task not found",
    "USER_NOT_FOUND": "User not found",
    "INVALID_INPUT": "Invalid input",
    "INVALID_CREDENTIALS": "Invalid email or password",
    "EMAIL_EXISTS": "An account with this email already exists",
    "CONFLICT": "Resource already exists",
}


def get_error_message(code: str) -> str:
    """Get user-friendly error message by error code.

    Args:
        code: Error code

    Returns:
        str: User-friendly error message

    Example:
        message = get_error_message("TASK_NOT_FOUND")  # "Task not found"
    """
    return ERROR_MESSAGES.get(code, "An error occurred")
