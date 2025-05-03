from fastapi import HTTPException
from app.schemas.general_converters.volume_converter_schema import (
    VolumeConvertRequest,
    VolumeConvertResponse,
    UNIT_TO_LITERS
)

def convert_volume_logic(data: VolumeConvertRequest) -> VolumeConvertResponse:
    """
    Convert volume between units with O(1) time complexity.
    
    Args:
        data: VolumeConvertRequest with validated value and unit
        
    Returns:
        VolumeConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to liters as intermediate unit (O(1) operation)
        liters = value * UNIT_TO_LITERS[unit]

        # Map UNIT_TO_LITERS keys to VolumeConvertResponse field names
        response_data = {
            key: round(liters / UNIT_TO_LITERS[key], 8)
            for key in UNIT_TO_LITERS
        }

        return VolumeConvertResponse(**response_data)
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")