from fastapi import HTTPException
from app.schemas.converters_formatters.bit_byte_converter_schema import (
    BitByteConvertRequest,
    BitByteConvertResponse,
    UNIT_TO_BITS
)

def convert_bit_byte_logic(data: BitByteConvertRequest) -> BitByteConvertResponse:
    if data.unit not in UNIT_TO_BITS:
        raise HTTPException(status_code=400, detail=f"Invalid unit: {data.unit}. Supported units: {list(UNIT_TO_BITS.keys())}")
    
    input_bits = data.value * UNIT_TO_BITS[data.unit]
    return BitByteConvertResponse(
        **{
            key: round(input_bits / bits, 8)
            for key, bits in UNIT_TO_BITS.items()
        }
    )