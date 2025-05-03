from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType
import math
from app.schemas.general_converters.schema_validators import validate_positive_value, validate_unit

# Immutable dictionary for angle unit conversions to radians
UNIT_TO_RADIANS: Dict[str, float] = MappingProxyType({
    "deg": math.pi / 180.0,        # Degrees
    "rad": 1.0,                    # Radians
    "grad": math.pi / 200.0,       # Gradians
    "arcmin": math.pi / 10800.0,   # Arcminutes
    "arcsec": math.pi / 648000.0,  # Arcseconds
    "turn": 2.0 * math.pi          # Turns (full rotations)
})

class AngleConvertRequest(BaseModel):
    value: float = Field(1, description="Angle value to convert", gt=0)
    unit: str = Field('rad', description="Angle unit (deg, rad, grad, arcmin, arcsec, turn)")

    _validate_unit = field_validator("unit")(validate_unit(UNIT_TO_RADIANS))
    _validate_value = field_validator("value")(validate_positive_value)

class AngleConvertResponse(BaseModel):
    deg: float = Field(..., description="Angle in degrees")
    rad: float = Field(..., description="Angle in radians")
    grad: float = Field(..., description="Angle in gradians")
    arcmin: float = Field(..., description="Angle in arcminutes")
    arcsec: float = Field(..., description="Angle in arcseconds")
    turn: float = Field(..., description="Angle in turns")