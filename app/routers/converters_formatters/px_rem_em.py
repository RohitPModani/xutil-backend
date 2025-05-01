from enum import Enum
from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.crud.converters_formatters.px_rem_em_crud import convert_units
from ...schemas.converters_formatters.px_rem_em_schema import (
    ConversionType,
    ConversionRequest,
    ConversionResponse
)

router = APIRouter(prefix="/px-rem-em", tags=["PX-REM-EM Converter"])

# Constants
DEFAULT_FONT_SIZE = 16
ROUNDING_PRECISION = 4

# Dependency for query parameters
def get_conversion_params(
    value: float = Query(..., gt=0, description="Value to convert"),
    root_font_size: float = Query(
        DEFAULT_FONT_SIZE, gt=0, description="Root font size in pixels (for REM)"
    ),
    parent_font_size: float = Query(
        DEFAULT_FONT_SIZE, gt=0, description="Parent font size in pixels (for EM)"
    )
) -> ConversionRequest:
    return ConversionRequest(
        value=value,
        root_font_size=root_font_size,
        parent_font_size=parent_font_size
    )

@router.get(
    "/",
    response_model=ConversionResponse,
    summary="Convert between PX, REM, and EM units",
    description="Converts a value between PX, REM, and EM units based on root and parent font sizes."
)
async def convert(
    conversion_type: ConversionType = Query(..., description="Type of conversion"),
    params: ConversionRequest = Depends(get_conversion_params)
):
    result = convert_units(
        conversion_type,
        params.value,
        params.root_font_size,
        params.parent_font_size
    )
    return JSONResponse(content=result.model_dump(exclude_none=True))