from .errors import ValidationError, DataError, FileNotFoundError, PyGeoutilError
from numbers import Real, Integral
from pathlib import Path
import re


'''
ConfigurationError	The program/setup is incorrectly configured	Invalid grid configuration
ValidationError	A supplied value/argument is invalid	nx = -10
DataError	The input data is bad, missing, or inconsistent	IRAP file contains malformed data
FileNotFoundError	A required file doesn't exist	Input grid path doesn't exist
ValueError	A generic Python value is inappropriate	float("abc")
TypeError	Wrong Python type	nx="100" instead of nx=100

A particularly useful rule

Think:
ConfigurationError = "The software doesn't know how it is supposed to operate."

Whereas:
ValidationError = "You gave me a value I don't accept."

and:
DataError = "The data I was given is bad."
'''

def validate_number(value, name="value"):
    if not isinstance(value, (float, int)):
        raise ValidationError(
            f"{name} must be a float or int, got {type(value).__name__}: {value}"
        )
    
def validate_string(value, valid_values, name="value"):
    if value not in valid_values:
        raise ValidationError(
            f"Invalid {name}: '{value}'. "
            f"Expected one of: {valid_values}"
        )

def validate_fraction(value, name="value"):
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"{name} must be a number between 0 and 1, "
            f"got {type(value).__name__}"
        )

    if not 0 <= value <= 1:
        raise ValueError(
            f"{name} must be > 0 and <= 1, got {value}"
        )

def validate_equal(value_one, value_two,name="value"):
    """Check that two numeric values are the same."""

    if value_one != value_two:
        raise ValidationError(
            f"{name} must be equal: {value_one} , {value_two}"
        )

def validate_pattern(value, pattern, name="value"):
    match = re.match(pattern, value)

    if match is None:
        raise ConfigurationError(
            f"Invalid {name}: '{value}'. "
            f"Expected pattern: {pattern}"
        )

    return match

def validate_positive(value, name="value", allow_zero=False):
    """Check that a numeric value is positive."""

    if allow_zero:
        valid = value >= 0
        requirement = ">= 0"
    else:
        valid = value > 0
        requirement = "> 0"

    if not valid:
        raise ValidationError(
            f"{name} must be {requirement}; got {value}"
        )

def validate_type(value, expected_type, name="value"):
    """Check that a value has the expected type."""

    if not isinstance(value, expected_type):
        raise ValidationError(  
            f"{name} must be of type {expected_type.__name__}; "
            f"got {type(value).__name__}"
        )

def validate_required(**kwargs ):
    """Check that required arguments have been supplied."""

    for name, value in kwargs.items():
        if value is None:
            raise ValidationError(f"{name} is required")

def validate_file_path(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"File does not exist: {path}"
        )

    return path

def validate_file_path_format(infile, path):

    if not isinstance(infile, path):
        raise ValidationError(
            f"{infile} & {path} must be a pathlib.Path.")

def validate_boolean(value, name="value"):
    """Check that a value is a boolean."""
    
    if not isinstance(value, bool):
        raise ValidationError(
            f"{name} must be a boolean; got {type(value).__name__}"
        )