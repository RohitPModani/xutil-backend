from fastapi import HTTPException
from app.schemas.general_converters.speed_converter_schema import (
    SpeedConvertRequest,
    SpeedConvertResponse,
    UNIT_TO_METERS_PER_SECOND
)

def convert_speed_logic(data: SpeedConvertRequest) -> SpeedConvertResponse:
    """
    Convert speed between units with O(1) time complexity.
    
    Args:
        data: SpeedConvertRequest with validated value and unit
        
    Returns:
        SpeedConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to meters per second as intermediate unit (O(1) operation)
        meters_per_second = value * UNIT_TO_METERS_PER_SECOND[unit]

        # Map UNIT_TO_METERS_PER_SECOND keys to SpeedConvertResponse field names
        response_data = {
            key: round(meters_per_second / UNIT_TO_METERS_PER_SECOND[key], 8)
            for key in UNIT_TO_METERS_PER_SECOND
        }

        return SpeedConvertResponse(**response_data)
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")