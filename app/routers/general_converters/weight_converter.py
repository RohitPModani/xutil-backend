from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.weight_converter_schema import WeightConvertRequest, WeightConvertResponse
from ...crud.general_converters.weight_converter_crud import convert_weight_logic

router = APIRouter(prefix="/weight", tags=["Weight"])

@router.post("/convert", response_model=WeightConvertResponse)
async def convert_weight(data: WeightConvertRequest) -> WeightConvertResponse:
    """
    Convert weight between different units (mg, g, kg, t, oz, lb, st).
    
    Args:
        data: WeightConvertRequest containing value and unit
        
    Returns:
        WeightConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or weight value)
    """
    try:
        return convert_weight_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")