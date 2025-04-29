from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from typing import Dict, Any, List
from ...crud.converters_formatters.base_converter_crud import base_convert_logic
from ...schemas.converters_formatters.base_converter_schema import (
    NumberInput,
    ConversionResponse
)


router = APIRouter(
    prefix="/base-converter",
    tags=["Base Converter"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/base-convert",
    summary="Convert number between bases",
    description="Converts a number from a source base to a target base. Supports bases 2 to 36 (e.g., binary, decimal, hexadecimal).",
    response_description="Converted number in the target base",
    response_model=ConversionResponse
)
async def base_convert(input: NumberInput):
    try:
        result = base_convert_logic(input.number, input.source_base, input.target_base)
        return ConversionResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")