from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for weight unit conversions to grams
UNIT_TO_GRAMS: Dict[str, float] = MappingProxyType({
    "mg": 0.001,          # Milligrams
    "g": 1.0,             # Grams
    "kg": 1000.0,         # Kilograms
    "t": 1000000.0,       # Metric Tons
    "oz": 28.349523125,   # Ounces
    "lb": 453.59237,      # Pounds
    "st": 6350.29318      # Stones
})

class WeightConvertRequest(BaseModel):
    value: float = Field(..., description="Weight value to convert", gt=0)
    unit: str = Field(..., description="Weight unit (mg, g, kg, t, oz, lb, st)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate weight unit."""
        normalized = value.lower()
        if normalized not in UNIT_TO_GRAMS:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_GRAMS.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_weight(cls, value: float, info) -> float:
        """Validate weight value is positive."""
        if value <= 0:
            raise ValueError("Weight must be greater than zero")
        return value

class WeightConvertResponse(BaseModel):
    mg: float = Field(..., description="Weight in milligrams")
    g: float = Field(..., description="Weight in grams")
    kg: float = Field(..., description="Weight in kilograms")
    t: float = Field(..., description="Weight in metric tons")
    oz: float = Field(..., description="Weight in ounces")
    lb: float = Field(..., description="Weight in pounds")
    st: float = Field(..., description="Weight in stones")