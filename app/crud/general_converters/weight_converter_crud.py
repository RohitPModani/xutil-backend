from fastapi import HTTPException
from ...schemas.general_converters.weight_converter_schema import (
    WeightConvertRequest,
    WeightConvertResponse,
    UNIT_TO_GRAMS
)

def convert_weight_logic(data: WeightConvertRequest) -> WeightConvertResponse:
    """
    Convert weight between units with O(1) time complexity.
    
    Args:
        data: WeightConvertRequest with validated value and unit
        
    Returns:
        WeightConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to grams as intermediate unit (O(1) operation)
        grams = value * UNIT_TO_GRAMS[unit]

        # Map UNIT_TO_GRAMS keys to WeightConvertResponse field names
        response_data = {
            key: round(grams / UNIT_TO_GRAMS[key], 8)
            for key in UNIT_TO_GRAMS
        }

        return WeightConvertResponse(**response_data)
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")