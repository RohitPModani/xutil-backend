from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from ...crud.encoding_decoding.html_entities_crud import encode_html_entities_logic, decode_html_entities_logic

router = APIRouter(prefix="/html-entities", tags=["HTML Entities"])

# Pydantic models for response structure
class EncodeResponse(BaseModel):
    original_text: str
    encoded_text: str

class DecodeResponse(BaseModel):
    encoded_text: str
    decoded_text: str

# Pydantic model for POST request body
class TextInput(BaseModel):
    text: str

@router.get("/encode", response_model=EncodeResponse, summary="Encode text into HTML entities")
async def encode_html_entities(
    text: str = Query(
        ...,
        description="Raw text to encode into HTML entities",
        min_length=1,
        max_length=10000
    )
):
    """
    Encode special characters in text to HTML entities (e.g., < to <).
    """
    try:
        return encode_html_entities_logic(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/encode", response_model=EncodeResponse, summary="Encode text into HTML entities (POST)")
async def encode_html_entities_post(input: TextInput):
    """
    Encode special characters in text to HTML entities using a POST request.
    Suitable for larger inputs.
    """
    try:
        return encode_html_entities_logic(input.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/decode", response_model=DecodeResponse, summary="Decode HTML entities to original text")
async def decode_html_entities(
    text: str = Query(
        ...,
        description="Text with HTML entities to decode",
        min_length=1,
        max_length=10000
    )
):
    """
    Decode HTML entities to their original characters (e.g., < to <).
    """
    try:
        return decode_html_entities_logic(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/decode", response_model=DecodeResponse, summary="Decode HTML entities to original text (POST)")
async def decode_html_entities_post(input: TextInput):
    """
    Decode HTML entities to their original characters using a POST request.
    Suitable for larger inputs.
    """
    try:
        return decode_html_entities_logic(input.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")