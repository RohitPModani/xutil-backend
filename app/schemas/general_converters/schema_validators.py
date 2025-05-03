import math
from typing import Dict

def validate_unit(unit_dict: Dict[str, float]):
    def inner(cls, value: str) -> str:
        key = value.lower()
        if key not in unit_dict:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(unit_dict.keys())}")
        return key
    return inner

def validate_positive_value(cls, value: float, info=None) -> float:
    if value <= 0:
        raise ValueError("Value must be greater than zero")
    return value

def validate_non_negative_value(cls, value: float) -> float:
    if value < 0:
        raise ValueError("Value cannot be negative")
    return value

def validate_finite_value(cls, value: float) -> float:
    if not math.isfinite(value):
        raise ValueError("Value must be a finite number (not NaN or infinity)")
    if value < 0:
        raise ValueError("Value cannot be negative")
    return value
