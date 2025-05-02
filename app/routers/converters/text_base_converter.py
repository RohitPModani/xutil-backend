from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile
from typing import Any
from ...crud.converters.text_base_converter_crud import text_to_base_logic, base_to_text_logic
from ...schemas.converters.text_base_converter_schema import (
    TextInput,
    BaseInput,
    ConversionResponse
)

router = APIRouter(
    prefix="/text-base",
    tags=["Text - Base Converter"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/text-to-base",
    summary="Convert text to base numbers",
    description="Converts a text to a target base. Supports bases binary, octal, decimal, hexadecimal",
    response_description="Converted text in the target base",
    response_model=ConversionResponse
)
async def text_to_base_convert(input: TextInput = Body(...)):
    try:
        result = text_to_base_logic(input.input_text, input.target_base)
        return ConversionResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post(
    "/base-to-text",
    summary="Convert base numbers to text",
    description="Converts a base input to text. Supports bases binary, octal, decimal, hexadecimal",
    response_description="Converted base input in text",
    response_model=ConversionResponse
)
async def base_to_text_convert(input: BaseInput = Body(...)):
    try:
        result = base_to_text_logic(input.base_text, input.source_base)
        return ConversionResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")