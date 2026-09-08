class PyGeoutilError(Exception):
    """Base exception for the package."""
    pass


class ValidationError(PyGeoutilError):
    """Raised when input validation fails."""
    pass


class ConfigurationError(PyGeoutilError):
    """Raised when configuration is invalid."""
    pass


class DataError(PyGeoutilError):
    """Raised when input data is invalid or incomplete."""
    pass