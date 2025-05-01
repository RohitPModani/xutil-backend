from typing import Dict
from pydantic import BaseModel
from types import MappingProxyType

# Immutable dictionary for bit/byte unit conversions (relative to bits, using binary prefixes)
UNIT_TO_BITS: Dict[str, float] = MappingProxyType({
    "bit": 1,                       # Bits
    "byte": 8,                      # Bytes (8 bits)
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
    value: float
    unit: str

class BitByteConvertResponse(BaseModel):
    bit: float
    byte: float
    Kb: float
    KB: float
    Mb: float
    MB: float
    Gb: float
    GB: float
    Tb: float
    TB: float
    Pb: float
    PB: float