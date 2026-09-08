from .errors import ValidationError, MyPackageError


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
        raise TypeError(
            f"{name} must be a number between 0 and 1, "
            f"got {type(value).__name__}"
        )

    if not 0 <= value <= 1:
        raise ValueError(
            f"{name} must be > 0 and <= 1, got {value}"
        )