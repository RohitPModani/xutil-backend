from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for power unit conversions to watts
UNIT_TO_WATTS: Dict[str, float] = MappingProxyType({
    "w": 1.0,              # Watts
    "kw": 1000.0,          # Kilowatts
    "hp_metric": 735.49875,    # Metric horsepower (PS)
    "hp_imperial": 745.69987158227022,  # Imperial horsepower
    "mw": 1000000.0,       # Megawatts
    "ft_lb_s": 1.3558179483314004  # Foot-pounds per second
})

class PowerConvertRequest(BaseModel):
    value: float = Field(1, description="Power value to convert", gt=0)
    unit: str = Field('w', description="Power unit (w, kw, hp_metric, hp_imperial, mw, ft_lb_s)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_WATTS))
    _validate_value = field_validator("value")(validate_positive_value)

class PowerConvertResponse(BaseModel):
    w: float = Field(..., description="Power in watts")
    kw: float = Field(..., description="Power in kilowatts")
    hp_metric: float = Field(..., description="Power in metric horsepower")
    hp_imperial: float = Field(..., description="Power in imperial horsepower")
    mw: float = Field(..., description="Power in megawatts")
    ft_lb_s: float = Field(..., description="Power in foot-pounds per second")