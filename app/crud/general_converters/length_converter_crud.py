from fastapi import HTTPException
from app.schemas.general_converters.length_converter_schema import (
    LengthConvertRequest,
    LengthConvertResponse,
    UNIT_TO_METERS
)

def convert_length_logic(data: LengthConvertRequest) -> LengthConvertResponse:
    """
    Convert length between units with O(1) time complexity.
    
    Args:
        data: LengthConvertRequest with validated value and unit
        
    Returns:
        LengthConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to meters as intermediate unit (O(1) operation)
        meters = value * UNIT_TO_METERS[unit]

        # Map UNIT_TO_METERS keys to LengthConvertResponse field names
        response_data = {
            key : round(meters / UNIT_TO_METERS[key], 8)
            for key in UNIT_TO_METERS
        }

        return LengthConvertResponse(**response_data)
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")