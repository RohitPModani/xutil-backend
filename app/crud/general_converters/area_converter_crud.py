from fastapi import HTTPException
from app.schemas.general_converters.area_converter_schema import (
    AreaConvertRequest,
    AreaConvertResponse,
    UNIT_TO_SQUARE_METERS
)

def convert_area_logic(data: AreaConvertRequest) -> AreaConvertResponse:
    """
    Convert area between units with O(1) time complexity.
    
    Args:
        data: AreaConvertRequest with validated value and unit
        
    Returns:
        AreaConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to square meters as intermediate unit (O(1) operation)
        square_meters = value * UNIT_TO_SQUARE_METERS[unit]

        # Convert from square meters to all units (O(1) operation)
        return AreaConvertResponse(
            **{
                key: round(square_meters / factor, 8)
                for key, factor in UNIT_TO_SQUARE_METERS.items()
            }
        )
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")