from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for time unit conversions to seconds
UNIT_TO_SECONDS: Dict[str, float] = MappingProxyType({
    "ns": 0.000000001,      # Nanoseconds
    "μs": 0.000001,         # Microseconds
    "ms": 0.001,            # Milliseconds
    "s": 1.0,               # Seconds
    "min": 60.0,            # Minutes
    "hr": 3600.0,           # Hours
    "day": 86400.0,         # Days
    "week": 604800.0,       # Weeks
    "month": 2629746.0,     # Average month = 30.44 days
    "year": 31556952.0,     # Average year = 365.25 days
    "decade": 315569520.0,  # Decade = 10 years
    "century": 3155695200.0 # Century = 100 years
})

class TimeConvertRequest(BaseModel):
    value: float = Field(1, description="Time value to convert", gt=0)
    unit: str = Field('s', description="Time unit (ns, μs, ms, s, min, hr, day, week, month, year, decade, century)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_SECONDS))
    _validate_value = field_validator("value")(validate_positive_value)

class TimeConvertResponse(BaseModel):
    ns: float = Field(..., description="Time in nanoseconds")
    μs: float = Field(..., description="Time in microseconds")
    ms: float = Field(..., description="Time in milliseconds")
    s: float = Field(..., description="Time in seconds")
    min: float = Field(..., description="Time in minutes")
    hr: float = Field(..., description="Time in hours")
    day: float = Field(..., description="Time in days")
    week: float = Field(..., description="Time in weeks")
    month: float = Field(..., description="Time in average months (30.44 days)")
    year: float = Field(..., description="Time in average years (365.25 days)")
    decade: float = Field(..., description="Time in decades")
    century: float = Field(..., description="Time in centuries")