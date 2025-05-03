from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

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
    value: float = Field(1, description="Volume value to convert", gt=0)
    unit: str = Field('l', description="Volume unit (m3, cm3, l, ml, ft3, in3, gal, qt, pt, fl_oz)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_LITERS))
    _validate_value = field_validator("value")(validate_positive_value)

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