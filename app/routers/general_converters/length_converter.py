from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.length_converter_schema import LengthConvertRequest, LengthConvertResponse
from ...crud.general_converters.length_converter_crud import convert_length_logic

router = APIRouter(prefix="/length", tags=["Length"])

@router.post("/convert", response_model=LengthConvertResponse)
async def convert_length(data: LengthConvertRequest) -> LengthConvertResponse:
    """
    Convert length between different units (mm, cm, m, km, in, ft, yd, mi, nm).
    
    Args:
        data: LengthConvertRequest containing value and unit
        
    Returns:
        LengthConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or length value)
    """
    try:
        return convert_length_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")