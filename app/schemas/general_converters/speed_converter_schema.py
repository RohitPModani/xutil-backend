from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for speed unit conversions to meters per second
UNIT_TO_METERS_PER_SECOND: Dict[str, float] = MappingProxyType({
    "m_s": 1.0,              # Meters per second
    "km_h": 0.27777777778,   # Kilometers per hour
    "mph": 0.44704,          # Miles per hour
    "ft_s": 0.3048,          # Feet per second
    "kn": 0.51444444444      # Knots
})

class SpeedConvertRequest(BaseModel):
    value: float = Field(1, description="Speed value to convert", gt=0)
    unit: str = Field('m_s', description="Speed unit (m_s, km_h, mph, ft_s, kn)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_METERS_PER_SECOND))
    _validate_value = field_validator("value")(validate_positive_value)

class SpeedConvertResponse(BaseModel):
    m_s: float = Field(..., description="Speed in meters per second")
    km_h: float = Field(..., description="Speed in kilometers per hour")
    mph: float = Field(..., description="Speed in miles per hour")
    ft_s: float = Field(..., description="Speed in feet per second")
    kn: float = Field(..., description="Speed in knots")