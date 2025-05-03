from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for pressure unit conversions to pascals
UNIT_TO_PASCALS: Dict[str, float] = MappingProxyType({
    "pa": 1.0,             # Pascals
    "kpa": 1000.0,         # Kilopascals
    "atm": 101325.0,       # Atmospheres
    "bar": 100000.0,       # Bars
    "mbar": 100.0,         # Millibars
    "psi": 6894.757293168, # Pounds per square inch
    "mmhg": 133.322387415, # Millimeters of mercury
    "torr": 133.322387415  # Torr (equivalent to mmHg)
})

class PressureConvertRequest(BaseModel):
    value: float = Field(1, description="Pressure value to convert", gt=0)
    unit: str = Field('pa', description="Pressure unit (pa, kpa, atm, bar, mbar, psi, mmhg, torr)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_PASCALS))
    _validate_value = field_validator("value")(validate_positive_value)

class PressureConvertResponse(BaseModel):
    pa: float = Field(..., description="Pressure in pascals")
    kpa: float = Field(..., description="Pressure in kilopascals")
    atm: float = Field(..., description="Pressure in atmospheres")
    bar: float = Field(..., description="Pressure in bars")
    mbar: float = Field(..., description="Pressure in millibars")
    psi: float = Field(..., description="Pressure in pounds per square inch")
    mmhg: float = Field(..., description="Pressure in millimeters of mercury")
    torr: float = Field(..., description="Pressure in torr")