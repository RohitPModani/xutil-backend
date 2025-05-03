from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for weight unit conversions to grams
UNIT_TO_GRAMS: Dict[str, float] = MappingProxyType({
    "mg": 0.001,          # Milligrams
    "g": 1.0,             # Grams
    "kg": 1000.0,         # Kilograms
    "t": 1000000.0,       # Metric Tons
    "oz": 28.349523125,   # Ounces
    "lb": 453.59237,      # Pounds
    "st": 6350.29318      # Stones
})

class WeightConvertRequest(BaseModel):
    value: float = Field(1, description="Weight value to convert", gt=0)
    unit: str = Field('g', description="Weight unit (mg, g, kg, t, oz, lb, st)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_GRAMS))
    _validate_value = field_validator("value")(validate_positive_value)

class WeightConvertResponse(BaseModel):
    mg: float = Field(..., description="Weight in milligrams")
    g: float = Field(..., description="Weight in grams")
    kg: float = Field(..., description="Weight in kilograms")
    t: float = Field(..., description="Weight in metric tons")
    oz: float = Field(..., description="Weight in ounces")
    lb: float = Field(..., description="Weight in pounds")
    st: float = Field(..., description="Weight in stones")