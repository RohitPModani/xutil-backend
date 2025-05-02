from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for length unit conversions to meters
UNIT_TO_METERS: Dict[str, float] = MappingProxyType({
    "mm": 0.001,           # Millimeters
    "cm": 0.01,            # Centimeters
    "m": 1.0,              # Meters
    "km": 1000.0,          # Kilometers
    "inch": 0.0254,          # Inches
    "ft": 0.3048,          # Feet
    "yd": 0.9144,          # Yards
    "mi": 1609.344,        # Miles
    "nm": 1852.0           # Nautical Miles
})

class LengthConvertRequest(BaseModel):
    value: float = Field(..., description="Length value to convert", gt=0)
    unit: str = Field(..., description="Length unit (mm, cm, m, km, inch, ft, yd, mi, nm)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate length unit."""
        normalized = value.lower()
        if normalized not in UNIT_TO_METERS:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_METERS.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_length(cls, value: float, info) -> float:
        """Validate length value is positive."""
        if value <= 0:
            raise ValueError("Length must be greater than zero")
        return value

class LengthConvertResponse(BaseModel):
    mm: float = Field(..., description="Length in millimeters")
    cm: float = Field(..., description="Length in centimeters")
    m: float = Field(..., description="Length in meters")
    km: float = Field(..., description="Length in kilometers")
    inch: float = Field(..., description="Length in inches")
    ft: float = Field(..., description="Length in feet")
    yd: float = Field(..., description="Length in yards")
    mi: float = Field(..., description="Length in miles")
    nm: float = Field(..., description="Length in nautical miles")