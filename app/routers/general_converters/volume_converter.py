from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.volume_converter_schema import VolumeConvertRequest, VolumeConvertResponse
from ...crud.general_converters.volume_converter_crud import convert_volume_logic

router = APIRouter(prefix="/volume", tags=["Volume"])

@router.post("/convert", response_model=VolumeConvertResponse)
async def convert_volume(data: VolumeConvertRequest) -> VolumeConvertResponse:
    """
    Convert volume between different units (m3, cm3, l, ml, ft3, in3, gal, qt, pt, fl_oz).
    
    Args:
        data: VolumeConvertRequest containing value and unit
        
    Returns:
        VolumeConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or volume value)
    """
    try:
        return convert_volume_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")