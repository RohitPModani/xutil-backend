from typing import Dict
from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.area_converter_schema import AreaConvertRequest, AreaConvertResponse
from ...crud.general_converters.area_converter_crud import convert_area_logic

router = APIRouter(prefix="/area", tags=["Area"])

@router.post("/convert", response_model=AreaConvertResponse)
async def convert_area(data: AreaConvertRequest) -> AreaConvertResponse:
    """
    Convert area between different units (m², km², ft², yd², acre, hectare).
    
    Args:
        data: AreaConvertRequest containing value and unit
        
    Returns:
        AreaConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or area value)
    """
    try:
        return convert_area_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")