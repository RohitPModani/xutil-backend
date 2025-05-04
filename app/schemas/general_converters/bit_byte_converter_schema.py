from typing import Dict
from pydantic import BaseModel, Field
from pydantic import field_validator
from types import MappingProxyType

# Immutable dictionary for bit/byte unit conversions (relative to bits, using binary prefixes)
UNIT_TO_BITS: Dict[str, float] = MappingProxyType({
    "Bit": 1,                       # Bits
    "Byte": 8,                      # Bytes (8 bits)
    "Kb": 1_024,                    # Kilobits (2¹⁰ bits)
    "KB": 8 * 1_024,                # Kilobytes (2¹⁰ bytes = 8 * 2¹⁰ bits)
    "Mb": 1_048_576,                # Megabits (2²⁰ bits)
    "MB": 8 * 1_048_576,            # Megabytes (2²⁰ bytes = 8 * 2²⁰ bits)
    "Gb": 1_073_741_824,            # Gigabits (2³⁰ bits)
    "GB": 8 * 1_073_741_824,        # Gigabytes (2³⁰ bytes = 8 * 2³⁰ bits)
    "Tb": 1_099_511_627_776,        # Terabits (2⁴⁰ bits)
    "TB": 8 * 1_099_511_627_776,    # Terabytes (2⁴⁰ bytes = 8 * 2⁴⁰ bits)
    "Pb": 1_125_899_906_842_624,    # Petabits (2⁵⁰ bits)
    "PB": 8 * 1_125_899_906_842_624 # Petabytes (2⁵⁰ bytes = 8 * 2⁵⁰ bits)
})

class BitByteConvertRequest(BaseModel):
    value: float = Field(1, description="Data storage value to convert")
    unit: str = Field('Bit', description="Data storage unit (Bit, Byte, Kb, KB, Mb, MB, Gb, GB, Tb, TB, Pb, PB)")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        """Validate data storage unit."""
        if value not in UNIT_TO_BITS:
            raise ValueError(f"Invalid unit: {value}. Supported units: {list(UNIT_TO_BITS.keys())}")
        return value
    
    @field_validator("value")
    @classmethod
    def validate_positive_value(cls, value: float) -> float:
        """Validate that the value is positive."""
        if value <= 0:
            raise ValueError("Value must be greater than 0")
        return value

class BitByteConvertResponse(BaseModel):
    Bit: float = Field(..., description="Value in bits")
    Byte: float = Field(..., description="Value in bytes")
    Kb: float = Field(..., description="Value in kilobits")
    KB: float = Field(..., description="Value in kilobytes")
    Mb: float = Field(..., description="Value in megabits")
    MB: float = Field(..., description="Value in megabytes")
    Gb: float = Field(..., description="Value in gigabits")
    GB: float = Field(..., description="Value in gigabytes")
    Tb: float = Field(..., description="Value in terabits")
    TB: float = Field(..., description="Value in terabytes")
    Pb: float = Field(..., description="Value in petabits")
    PB: float = Field(..., description="Value in petabytes")