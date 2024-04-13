class AuthException(Exception):
    """Base exception class for authentication errors."""


class InvalidCredentialsException(AuthException):
    """Exception raised when the provided credentials are invalid."""


class UserNotFoundException(AuthException):
    """Exception raised when the user is not found."""


class AccountLockedException(AuthException):
    """Exception raised when the user's account is locked."""


# Add more specific exceptions as needed...
