from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...schemas.encoding_decoding.cipher_schema import (
    ROT13Request,
    ROT13Response,
    CaesarRequest, 
    CaesarResponse
)
from ...crud.encoding_decoding.cipher_crud import (
    rot13_cipher_logic,
    caesar_cipher_logic,
    validate_text_has_alnum,
)

router = APIRouter(prefix="/cipher", tags=["Cipher"])

@router.post(
    "/rot13",
    summary="Apply ROT13 Cipher",
    description="Encodes or decodes a message using the ROT13 cipher, shifting letters (a-z, A-Z) by 13 and digits (0-9) by 3.",
    response_description="Returns the input text and the transformed (encoded/decoded) text.",
    response_model=ROT13Response,
)
async def apply_rot13(request: ROT13Request):
    try:
        # Validate text has alphanumeric content if required
        validate_text_has_alnum(request.text)
        output = rot13_cipher_logic(request.text)
        return ROT13Response(input_text=request.text, output_text=output)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/caesar",
    summary="Apply Caesar Cipher",
    description="Encodes or decodes a message using the Caesar cipher, shifting letters (a-z, A-Z) and digits (0-9) by the specified value.",
    response_description="Returns the input text, shift value, and the transformed (encoded/decoded) text.",
    response_model=CaesarResponse,
)
async def apply_caesar(request: CaesarRequest):
    try:
        # Validate text has alphanumeric content if required
        validate_text_has_alnum(request.text)
        output = caesar_cipher_logic(request.text, request.shift)
        return CaesarResponse(
            input_text=request.text,
            shift=request.shift,
            output_text=output,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))