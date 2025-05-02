from fastapi import HTTPException
import math
from app.schemas.general_converters.bit_byte_converter_schema import (
    BitByteConvertRequest,
    BitByteConvertResponse,
    UNIT_TO_BITS
)

def convert_bit_byte_logic(data: BitByteConvertRequest) -> BitByteConvertResponse:
    """
    Convert data storage values between bit/byte units with O(1) time complexity.
    
    Args:
        data: BitByteConvertRequest with validated value and unit (Bit, Byte, Kb, KB, etc.)
        
    Returns:
        BitByteConvertResponse with converted values in all supported units
        
    Raises:
        HTTPException: 
            - 400: If unit is invalid or value causes numerical errors
            - 500: If unexpected errors occur during conversion
    """
    try:
        # Defense-in-depth: Re-validate unit (already validated by Pydantic)
        if data.unit not in UNIT_TO_BITS:
            raise ValueError(f"Invalid unit: {data.unit}. Supported units: {list(UNIT_TO_BITS.keys())}")

        # Validate value for numerical stability
        if not math.isfinite(data.value):
            raise ValueError("Value must be a finite number (not NaN or infinity)")

        # Convert to bits as intermediate unit (O(1) operation)
        input_bits = data.value * UNIT_TO_BITS[data.unit]

        # Check for numerical overflow or invalid results
        if not math.isfinite(input_bits):
            raise ValueError("Conversion resulted in non-finite value (possible overflow)")

        # Convert from bits to all units and round to 8 decimal places (O(1) per unit)
        converted_values = {
            key: round(input_bits / factor, 8)
            for key, factor in UNIT_TO_BITS.items()
        }

        return BitByteConvertResponse(**converted_values)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Conversion error: {str(e)}")
    except OverflowError:
        raise HTTPException(status_code=400, detail="Value too large for conversion")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during conversion: {str(e)}")