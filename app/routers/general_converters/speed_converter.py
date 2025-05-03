from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.speed_converter_schema import SpeedConvertRequest, SpeedConvertResponse
from ...crud.general_converters.speed_converter_crud import convert_speed_logic

router = APIRouter(prefix="/speed", tags=["Speed"])

@router.post("/convert", response_model=SpeedConvertResponse)
async def convert_speed(data: SpeedConvertRequest) -> SpeedConvertResponse:
    """
    Convert speed between different units (m_s, km_h, mph, ft_s, kn).
    
    Args:
        data: SpeedConvertRequest containing value and unit
        
    Returns:
        SpeedConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or speed value)
    """
    try:
        return convert_speed_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")