from fastapi import APIRouter, Query
from ...schemas.encoding_decoding.url_encode_decode_schema import URLEncodeResponse, URLDecodeResponse
from ...crud.encoding_decoding.url_encode_decode_crud import encode_url_logic, decode_url_logic

router = APIRouter(prefix="/url", tags=["URL Encoder/Decoder"])

@router.get("/encode", response_model=URLEncodeResponse)
def encode_url(
    text: str = Query(..., description="The text or URL to encode", min_length=1),
    safe: str = Query("/", description="Characters to exclude from encoding")
):
    return encode_url_logic(text, safe)

@router.get("/decode", response_model=URLDecodeResponse)
def decode_url(
    encoded_text: str = Query(..., description="The encoded URL to decode", min_length=1)
):
    return decode_url_logic(encoded_text)