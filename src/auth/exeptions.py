from exception import InvalidDataException


class InvalidCredentialsException(InvalidDataException):
    """Exception raised when the provided credentials are invalid."""


class UserNotFoundException(InvalidDataException):
    """Exception raised when the user is not found."""


class UserExists(InvalidDataException):
    """Exception raised when the user exists."""


class AccountLockedException(InvalidDataException):
    """Exception raised when the user's account is locked."""


# Add more specific exceptions as needed...
