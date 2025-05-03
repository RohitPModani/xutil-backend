from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for volume unit conversions to liters
UNIT_TO_LITERS: Dict[str, float] = MappingProxyType({
    "m3": 1000.0,           # Cubic meters
    "cm3": 0.001,           # Cubic centimeters
    "l": 1.0,               # Liters
    "ml": 0.001,            # Milliliters
    "ft3": 28.316846592,    # Cubic feet
    "in3": 0.016387064,     # Cubic inches
    "gal": 3.785411784,     # US Gallons
    "qt": 0.946352946,      # US Quarts
    "pt": 0.473176473,      # US Pints
    "fl_oz": 0.0295735295625  # US Fluid Ounces
})

class VolumeConvertRequest(BaseModel):
    value: float = Field(..., description="Volume value to convert", gt=0)
    unit: str = Field(..., description="Volume unit (m3, cm3, l, ml, ft3, in3, gal, qt, pt, fl_oz)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate volume unit."""
        normalized = value.lower()
        if normalized not in UNIT_TO_LITERS:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_LITERS.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_volume(cls, value: float, info) -> float:
        """Validate volume value is positive."""
        if value <= 0:
            raise ValueError("Volume must be greater than zero")
        return value

class VolumeConvertResponse(BaseModel):
    m3: float = Field(..., description="Volume in cubic meters")
    cm3: float = Field(..., description="Volume in cubic centimeters")
    l: float = Field(..., description="Volume in liters")
    ml: float = Field(..., description="Volume in milliliters")
    ft3: float = Field(..., description="Volume in cubic feet")
    in3: float = Field(..., description="Volume in cubic inches")
    gal: float = Field(..., description="Volume in US gallons")
    qt: float = Field(..., description="Volume in US quarts")
    pt: float = Field(..., description="Volume in US pints")
    fl_oz: float = Field(..., description="Volume in US fluid ounces")