from exception import InvalidDataException


class InvalidCredentialsException(InvalidDataException):
    """Exception raised when the provided credentials are invalid."""


class UserNotFoundException(InvalidDataException):
    """Exception raised when the user is not found."""


class InvalidPassword(InvalidDataException):
    """Exception raised when the password is invalid."""


class NotAuthorized(InvalidDataException):
    """Exception raised when user is not authorized."""

# Add more specific exceptions as needed...
