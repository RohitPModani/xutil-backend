from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...schemas.encoding_decoding.base_encode_decode_schema import (
    BaseDecodeRequest,
    BaseDecodeResponse,
    BaseEncodeRequest,
    BaseEncodeResponse,
)
from ...crud.encoding_decoding.base_encode_decode_crud import (
    base_encode_logic,
    base_decode_logic,
)

router = APIRouter(prefix="/base", tags=["Base-Encoder-Decoder"])

@router.post(
    "/encode",
    summary="Encode text into a base type",
    description="Encodes input text into the selected base type (Base32, Base58, or Base64).",
    response_description="Returns the original text, base type, and encoded text.",
    response_model=BaseEncodeResponse,
)
async def base_encode(request: BaseEncodeRequest):
    try:
        return base_encode_logic(request.text, request.base_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/decode",
    summary="Decode text from a base type",
    description="Decodes text from the selected base type (Base32, Base58, or Base64) back to its original form.",
    response_description="Returns the encoded text, base type, and decoded text.",
    response_model=BaseDecodeResponse,
)
async def base_decode(request: BaseDecodeRequest):
    try:
        return base_decode_logic(request.encoded_text, request.base_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))