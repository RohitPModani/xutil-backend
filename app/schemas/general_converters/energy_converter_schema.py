from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for energy unit conversions to joules
UNIT_TO_JOULES: Dict[str, float] = MappingProxyType({
    "j": 1.0,                  # Joules
    "kj": 1000.0,              # Kilojoules
    "cal": 4.184,              # Calories
    "kcal": 4184.0,            # Kilocalories
    "wh": 3600.0,              # Watt-hours
    "kwh": 3600000.0,          # Kilowatt-hours
    "ev": 1.602176634e-19,     # Electronvolts
    "btu": 1055.05585262       # British Thermal Units
})

class EnergyConvertRequest(BaseModel):
    value: float = Field(..., description="Energy value to convert", gt=0)
    unit: str = Field(..., description="Energy unit (j, kj, cal, kcal, wh, kwh, ev, btu)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate energy unit."""
        normalized = value.lower()
        if normalized not in UNIT_TO_JOULES:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_JOULES.keys())}")
        return normalized

    @field_validator("value")
    @classmethod
    def validate_energy(cls, value: float, info) -> float:
        """Validate energy value is positive."""
        if value <= 0:
            raise ValueError("Energy must be greater than zero")
        return value

class EnergyConvertResponse(BaseModel):
    j: float = Field(..., description="Energy in joules")
    kj: float = Field(..., description="Energy in kilojoules")
    cal: float = Field(..., description="Energy in calories")
    kcal: float = Field(..., description="Energy in kilocalories")
    wh: float = Field(..., description="Energy in watt-hours")
    kwh: float = Field(..., description="Energy in kilowatt-hours")
    ev: float = Field(..., description="Energy in electronvolts")
    btu: float = Field(..., description="Energy in British Thermal Units")