"""Custom exceptions for the application."""


class AppException(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AppException):
    """Validation error."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)


class BusinessLogicError(AppException):
    """Business logic error."""
    def __init__(self, message: str = "Business logic error"):
        super().__init__(message, status_code=400)
