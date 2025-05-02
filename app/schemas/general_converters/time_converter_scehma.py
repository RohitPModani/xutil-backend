from typing import Dict
from pydantic import BaseModel
from types import MappingProxyType

# Immutable dictionary for time unit conversions
UNIT_TO_SECONDS: Dict[str, float] = MappingProxyType({
    "ns": 0.000000001,      # Nanoseconds
    "μs": 0.000001,         # Microseconds
    "ms": 0.001,            # Milliseconds
    "s": 1,                 # Seconds
    "min": 60,              # Minutes
    "hr": 3600,             # Hours
    "day": 86400,           # Days
    "week": 604800,         # Weeks
    "month": 2629746,       # Average month = 30.44 days
    "year": 31556952,       # Average year = 365.25 days
    "decade": 315569520,    # Decade = 10 years
    "century": 3155695200   # Century = 100 years
})

class TimeConvertRequest(BaseModel):
    value: float
    unit: str

class TimeConvertResponse(BaseModel):
    ns: float
    μs: float
    ms: float
    s: float
    min: float
    hr: float
    day: float
    week: float
    month: float
    year: float
    decade: float
    century: float