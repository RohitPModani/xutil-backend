from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for speed unit conversions to meters per second
UNIT_TO_METERS_PER_SECOND: Dict[str, float] = MappingProxyType({
    "m_s": 1.0,              # Meters per second
    "km_h": 0.27777777778,   # Kilometers per hour
    "mph": 0.44704,          # Miles per hour
    "ft_s": 0.3048,          # Feet per second
    "kn": 0.51444444444      # Knots
})

class SpeedConvertRequest(BaseModel):
    value: float = Field(..., description="Speed value to convert", gt=0)
    unit: str = Field(..., description="Speed unit (m_s, km_h, mph, ft_s, kn)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate speed unit."""
        normalized = value.lower()
        if normalized not in UNIT_TO_METERS_PER_SECOND:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_METERS_PER_SECOND.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_speed(cls, value: float, info) -> float:
        """Validate speed value is positive."""
        if value <= 0:
            raise ValueError("Speed must be greater than zero")
        return value

class SpeedConvertResponse(BaseModel):
    m_s: float = Field(..., description="Speed in meters per second")
    km_h: float = Field(..., description="Speed in kilometers per hour")
    mph: float = Field(..., description="Speed in miles per hour")
    ft_s: float = Field(..., description="Speed in feet per second")
    kn: float = Field(..., description="Speed in knots")