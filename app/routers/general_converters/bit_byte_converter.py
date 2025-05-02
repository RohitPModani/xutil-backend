from typing import Dict
from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.bit_byte_converter_schema import BitByteConvertRequest, BitByteConvertResponse, UNIT_TO_BITS
from ...crud.general_converters.bit_byte_converter_crud import convert_bit_byte_logic

router = APIRouter(prefix="/bit-byte", tags=["Bit-Byte"])

@router.post("/convert", response_model=BitByteConvertResponse)
async def convert_bit_byte(data: BitByteConvertRequest) -> BitByteConvertResponse:
    """
    Convert between bit/byte units (Bit, Byte, Kb, KB, Mb, MB, Gb, GB, Tb, TB, Pb, PB).
    
    Args:
        data: BitByteConvertRequest containing value and unit
        
    Returns:
        BitByteConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If the input unit is invalid
    """
    return convert_bit_byte_logic(data)