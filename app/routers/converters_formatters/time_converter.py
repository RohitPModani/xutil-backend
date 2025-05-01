from typing import Dict
from fastapi import APIRouter, HTTPException
from ...schemas.converters_formatters.time_converter_scehma import TimeConvertRequest, TimeConvertResponse, UNIT_TO_SECONDS
from ...crud.converters_formatters.time_converter_crud import convert_time_logic

router = APIRouter(prefix="/time", tags=["time"])

@router.post("/convert", response_model=TimeConvertResponse)
async def convert_time(data: TimeConvertRequest) -> TimeConvertResponse:
    """
    Convert time between different units (ns, μs, ms, s, min, hr, day, week, month, year, decade, century).
    
    Args:
        data: TimeConvertRequest containing value and unit
        
    Returns:
        TimeConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If the input unit is invalid
    """
    return convert_time_logic(data)