from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for fuel economy conversions to km/L
UNIT_TO_KM_PER_LITER: Dict[str, float] = MappingProxyType({
    "mpg_us": 0.425144,      # Miles per US gallon
    "mpg_uk": 0.354006,      # Miles per UK gallon
    "km_l": 1.0,             # Kilometers per liter
    "l_100km": 100.0         # Liters per 100 kilometers (inverted for conversion)
})

class FuelEconomyConvertRequest(BaseModel):
    value: float = Field(1, description="Fuel economy value to convert", gt=0)
    unit: str = Field('km_l', description="Fuel economy unit (mpg_us, mpg_uk, km_l, l_100km)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_KM_PER_LITER))
    _validate_value = field_validator("value")(validate_positive_value)

class FuelEconomyConvertResponse(BaseModel):
    mpg_us: float = Field(..., description="Fuel economy in miles per US gallon")
    mpg_uk: float = Field(..., description="Fuel economy in miles per UK gallon")
    km_l: float = Field(..., description="Fuel economy in kilometers per liter")
    l_100km: float = Field(..., description="Fuel economy in liters per 100 kilometers")