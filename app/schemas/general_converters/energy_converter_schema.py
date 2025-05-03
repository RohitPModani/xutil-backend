from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

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
    value: float = Field(1, description="Energy value to convert", gt=0)
    unit: str = Field('j', description="Energy unit (j, kj, cal, kcal, wh, kwh, ev, btu)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_JOULES))
    _validate_value = field_validator("value")(validate_positive_value)

class EnergyConvertResponse(BaseModel):
    j: float = Field(..., description="Energy in joules")
    kj: float = Field(..., description="Energy in kilojoules")
    cal: float = Field(..., description="Energy in calories")
    kcal: float = Field(..., description="Energy in kilocalories")
    wh: float = Field(..., description="Energy in watt-hours")
    kwh: float = Field(..., description="Energy in kilowatt-hours")
    ev: float = Field(..., description="Energy in electronvolts")
    btu: float = Field(..., description="Energy in British Thermal Units")