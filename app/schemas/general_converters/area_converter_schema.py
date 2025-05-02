from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for area unit conversions (to square meters)
UNIT_TO_SQUARE_METERS: Dict[str, float] = MappingProxyType({
    "m2": 1,                    # Square meters
    "km2": 1_000_000,          # Square kilometers
    "ft2": 0.09290304,         # Square feet
    "yd2": 0.83612736,         # Square yards
    "acre": 4046.8564224,      # Acres
    "hectare": 10_000          # Hectares
})

class AreaConvertRequest(BaseModel):
    value: float = Field(..., description="Area value to convert")
    unit: str = Field(..., description="Area unit (m2, km2, ft2, yd2, acre, hectare)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate area unit."""
        normalized = value.lower()
        if normalized not in UNIT_TO_SQUARE_METERS:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_SQUARE_METERS.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_area(cls, value: float) -> float:
        """Validate area value is non-negative."""
        if value < 0:
            raise ValueError("Area cannot be negative")
        return value

class AreaConvertResponse(BaseModel):
    m2: float = Field(..., description="Area in square meters")
    km2: float = Field(..., description="Area in square kilometers")
    ft2: float = Field(..., description="Area in square feet")
    yd2: float = Field(..., description="Area in square yards")
    acre: float = Field(..., description="Area in acres")
    hectare: float = Field(..., description="Area in hectares")