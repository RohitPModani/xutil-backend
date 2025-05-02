from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for temperature units
TEMPERATURE_UNITS: Dict[str, str] = MappingProxyType({
    "celsius": "C",
    "fahrenheit": "F",
    "kelvin": "K"
})

# Physical constants
ABSOLUTE_ZERO_K = 0
ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67

class TemperatureConvertRequest(BaseModel):
    value: float = Field(..., description="Temperature value to convert")
    unit: str = Field(..., description="Temperature unit (celsius, fahrenheit, kelvin)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate temperature unit."""
        normalized = value.lower()
        if normalized not in TEMPERATURE_UNITS:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(TEMPERATURE_UNITS.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_temperature(cls, value: float, info) -> float:
        """Validate temperature value against physical limits."""
        if "unit" not in info.data:
            return value  # Unit validation failed, skip temperature validation
        
        unit = info.data["unit"]
        if unit == "kelvin" and value < ABSOLUTE_ZERO_K:
            raise ValueError(f"Temperature cannot be below absolute zero (0 K)")
        elif unit == "celsius" and value < ABSOLUTE_ZERO_C:
            raise ValueError(f"Temperature cannot be below absolute zero (-273.15°C)")
        elif unit == "fahrenheit" and value < ABSOLUTE_ZERO_F:
            raise ValueError(f"Temperature cannot be below absolute zero (-459.67°F)")
        return value

class TemperatureConvertResponse(BaseModel):
    celsius: float = Field(..., description="Temperature in Celsius")
    fahrenheit: float = Field(..., description="Temperature in Fahrenheit")
    kelvin: float = Field(..., description="Temperature in Kelvin")