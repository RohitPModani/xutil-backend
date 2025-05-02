from fastapi import HTTPException
from app.schemas.general_converters.temperature_converter_schema import (
    TemperatureConvertRequest,
    TemperatureConvertResponse,
    TEMPERATURE_UNITS,
    ABSOLUTE_ZERO_K
)

def convert_temperature_logic(data: TemperatureConvertRequest) -> TemperatureConvertResponse:
    """
    Convert temperature between units.
    
    Args:
        data: TemperatureConvertRequest with validated value and unit
        
    Returns:
        TemperatureConvertResponse with converted values
        
    Raises:
        ValueError: If conversion fails due to invalid input
    """
    try:
        unit = data.unit  # Already validated and normalized
        value = data.value

        # Convert to Kelvin as intermediate unit (O(1) operation)
        if unit == "celsius":
            kelvin = value + 273.15
        elif unit == "fahrenheit":
            kelvin = (value - 32) * 5/9 + 273.15
        else:  # kelvin
            kelvin = value

        # Validate Kelvin result
        if kelvin < ABSOLUTE_ZERO_K:
            raise ValueError("Converted temperature below absolute zero")

        # Convert from Kelvin to all units (O(1) operation)
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9/5 + 32

        return TemperatureConvertResponse(
            celsius=round(celsius, 4),
            fahrenheit=round(fahrenheit, 4),
            kelvin=round(kelvin, 4)
        )
    except ValueError as e:
        raise ValueError(f"Conversion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during conversion: {str(e)}")