from fastapi import HTTPException
from typing import TypeVar, Type, Dict, Any
import math

from app.schemas.general_converters.temperature_converter_schema import TemperatureConvertRequest, TemperatureConvertResponse

# Generic type variables for request and response schemas
RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")

def convert_unit_logic(
    data: RequestT,
    conversion_dict: Dict[str, float],
    response_class: Type[ResponseT],
    unit_field: str = "unit",
    value_field: str = "value"
) -> ResponseT:
    """
    Generic unit conversion with O(1) time complexity.

    Args:
        data: Validated request object with unit and value
        conversion_dict: Dictionary mapping units to conversion factors for intermediate unit
        response_class: Response class to instantiate with converted values
        unit_field: Name of the unit field in the request object (default: 'unit')
        value_field: Name of the value field in the request object (default: 'value')

    Returns:
        ResponseT: Response object with converted values in all supported units

    Raises:
        HTTPException:
            - 400: If unit is invalid, value causes numerical errors, or conversion fails
            - 500: If unexpected errors occur during conversion
    """
    try:
        # Extract unit and value dynamically
        unit = getattr(data, unit_field)
        value = getattr(data, value_field)

        # Validate unit
        if unit not in conversion_dict:
            raise ValueError(f"Invalid unit: {unit}. Supported units: {list(conversion_dict.keys())}")

        # Validate value for numerical stability
        if not math.isfinite(value):
            raise ValueError("Value must be a finite number (not NaN or infinity)")

        # Convert to intermediate unit (O(1) operation)
        intermediate_value = value * conversion_dict[unit]

        # Check for numerical overflow or invalid results
        if not math.isfinite(intermediate_value):
            raise ValueError("Conversion resulted in non-finite value (possible overflow)")

        # Convert from intermediate unit to all units and round to 8 decimal places
        converted_values = {
            key: round(intermediate_value / factor, 8)
            for key, factor in conversion_dict.items()
        }

        return response_class(**converted_values)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Conversion error: {str(e)}")
    except OverflowError:
        raise HTTPException(status_code=400, detail="Value too large for conversion")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during conversion: {str(e)}")
    
def convert_temperature_logic(data: TemperatureConvertRequest) -> TemperatureConvertResponse:
    """
    Convert temperature between Celsius, Fahrenheit, and Kelvin.

    Args:
        data: Validated request object with unit and value

    Returns:
        TemperatureConvertResponse with converted values in all units

    Raises:
        HTTPException:
            - 400: If value causes numerical errors or conversion fails
            - 500: If unexpected errors occur during conversion
    """
    try:
        unit = data.unit
        value = data.value

        # Validate value for numerical stability
        if not math.isfinite(value):
            raise ValueError("Value must be a finite number (not NaN or infinity)")

        # Convert to Celsius as an intermediate step, then to other units
        if unit == "celsius":
            celsius = value
        elif unit == "fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif unit == "kelvin":
            celsius = value - 273.15
        else:
            raise ValueError(f"Invalid unit: {unit}")

        # Check for numerical stability of intermediate value
        if not math.isfinite(celsius):
            raise ValueError("Conversion resulted in non-finite value (possible overflow)")

        # Convert to other units
        fahrenheit = celsius * 9 / 5 + 32
        kelvin = celsius + 273.15

        # Round to 8 decimal places
        celsius = round(celsius, 8)
        fahrenheit = round(fahrenheit, 8)
        kelvin = round(kelvin, 8)

        return TemperatureConvertResponse(
            celsius=celsius,
            fahrenheit=fahrenheit,
            kelvin=kelvin
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Conversion error: {str(e)}")
    except OverflowError:
        raise HTTPException(status_code=400, detail="Value too large for conversion")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during conversion: {str(e)}")