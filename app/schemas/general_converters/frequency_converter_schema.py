from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for frequency unit conversions to hertz
UNIT_TO_HERTZ: Dict[str, float] = MappingProxyType({
    "hz": 1.0,             # Hertz
    "khz": 1000.0,         # Kilohertz
    "mhz": 1000000.0,      # Megahertz
    "ghz": 1000000000.0,   # Gigahertz
    "rpm": 1.0 / 60.0      # Revolutions per minute (1 RPM = 1/60 Hz)
})

class FrequencyConvertRequest(BaseModel):
    value: float = Field(1, description="Frequency value to convert", gt=0)
    unit: str = Field('hz', description="Frequency unit (hz, khz, mhz, ghz, rpm)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_HERTZ))
    _validate_value = field_validator("value")(validate_positive_value)

class FrequencyConvertResponse(BaseModel):
    hz: float = Field(..., description="Frequency in hertz")
    khz: float = Field(..., description="Frequency in kilohertz")
    mhz: float = Field(..., description="Frequency in megahertz")
    ghz: float = Field(..., description="Frequency in gigahertz")
    rpm: float = Field(..., description="Frequency in revolutions per minute")