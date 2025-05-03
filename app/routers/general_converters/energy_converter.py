from fastapi import APIRouter, HTTPException
from ...schemas.general_converters.energy_converter_schema import EnergyConvertRequest, EnergyConvertResponse
from ...crud.general_converters.energy_converter_crud import convert_energy_logic

router = APIRouter(prefix="/energy", tags=["Energy"])

@router.post("/convert", response_model=EnergyConvertResponse)
async def convert_energy(data: EnergyConvertRequest) -> EnergyConvertResponse:
    """
    Convert energy between different units (j, kj, cal, kcal, wh, kwh, ev, btu).
    
    Args:
        data: EnergyConvertRequest containing value and unit
        
    Returns:
        EnergyConvertResponse with converted values in all units
        
    Raises:
        HTTPException: If input validation fails (invalid unit or energy value)
    """
    try:
        return convert_energy_logic(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")