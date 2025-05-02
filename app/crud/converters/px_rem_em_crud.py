from ...schemas.converters.px_rem_em_schema import (             
    ConversionType,
    ConversionRequest,
    ConversionResponse
)

# Constants
DEFAULT_FONT_SIZE = 16
ROUNDING_PRECISION = 4

# Conversion logic
def convert_units(
    conversion_type: ConversionType,
    value: float,
    root_font_size: float,
    parent_font_size: float
) -> ConversionResponse:
    if conversion_type == ConversionType.PX_TO_REM_EM:
        return ConversionResponse(
            px=value,
            rem=round(value / root_font_size, ROUNDING_PRECISION),
            em=round(value / parent_font_size, ROUNDING_PRECISION)
        )
    elif conversion_type == ConversionType.REM_TO_PX_EM:
        px = value * root_font_size
        return ConversionResponse(
            px=round(px, ROUNDING_PRECISION),
            rem=value,
            em=round(px / parent_font_size, ROUNDING_PRECISION)
        )
    else:  # EM_TO_PX_REM
        px = value * parent_font_size
        return ConversionResponse(
            px=round(px, ROUNDING_PRECISION),
            em=value,
            rem=round(px / root_font_size, ROUNDING_PRECISION)
        )