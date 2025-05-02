from typing import Dict
from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.temperature_converter_schema import TemperatureConvertRequest, TemperatureConvertResponse
from ...crud.general_converters.temperature_converter_crud import convert_temperature_logic

router = APIRouter(prefix="/temperature", tags=["Temperature"])

@router.post("/convert", response_model=TemperatureConvertResponse)
async def convert_temperature(data: TemperatureConvertRequest) -> TemperatureConvertResponse:
    """
    Convert temperature between different units (Celsius, Fahrenheit, Kelvin).
    
    Args:
        data: TemperatureConvertRequest containing value and unit
        
    Returns:
        TemperatureConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or temperature value)
    """
    try:
        return convert_temperature_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")