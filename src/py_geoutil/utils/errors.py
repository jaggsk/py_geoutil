class PyGeoutilError(Exception):
    """Base exception for the package."""
    pass


class ValidationError(MyPackageError):
    """Raised when input validation fails."""
    pass


class ConfigurationError(MyPackageError):
    """Raised when configuration is invalid."""
    pass


class DataError(MyPackageError):
    """Raised when input data is invalid or incomplete."""
    pass