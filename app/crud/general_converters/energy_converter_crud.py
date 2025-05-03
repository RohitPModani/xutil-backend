from fastapi import HTTPException
from app.schemas.general_converters.energy_converter_schema import (
    EnergyConvertRequest,
    EnergyConvertResponse,
    UNIT_TO_JOULES
)

def convert_energy_logic(data: EnergyConvertRequest) -> EnergyConvertResponse:
    """
    Convert energy between units with O(1) time complexity.
    
    Args:
        data: EnergyConvertRequest with validated value and unit
        
    Returns:
        EnergyConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to joules as intermediate unit (O(1) operation)
        joules = value * UNIT_TO_JOULES[unit]

        # Map UNIT_TO_JOULES keys to EnergyConvertResponse field names
        response_data = {
            key: round(joules / UNIT_TO_JOULES[key], 8)
            for key in UNIT_TO_JOULES
        }

        return EnergyConvertResponse(**response_data)
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")