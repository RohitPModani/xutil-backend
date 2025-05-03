from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

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
    value: float = Field(1, description="Area value to convert")
    unit: str = Field('m2', description="Area unit (m2, km2, ft2, yd2, acre, hectare)")
    
    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_SQUARE_METERS))
    _validate_value = field_validator("value")(validate_positive_value)

class AreaConvertResponse(BaseModel):
    m2: float = Field(..., description="Area in square meters")
    km2: float = Field(..., description="Area in square kilometers")
    ft2: float = Field(..., description="Area in square feet")
    yd2: float = Field(..., description="Area in square yards")
    acre: float = Field(..., description="Area in acres")
    hectare: float = Field(..., description="Area in hectares")