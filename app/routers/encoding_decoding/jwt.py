from fastapi import APIRouter
from ...crud.encoding_decoding.jwt_crud import decode_jwt_logic, encode_jwt_logic
from ...schemas.encoding_decoding.jwt_schema import JWTDecodeRequest, JWTDecodeResponse, JWTEncodeRequest, JWTEncodeResponse

router = APIRouter(prefix="/jwt", tags=["JWT Encoder/Decoder"])

@router.post(
    "/encode",
    response_model=JWTEncodeResponse,
    summary="Encode a JWT token",
    description="Creates a JWT token with the provided payload, secret, and optional headers"
)
async def encode_jwt(data: JWTEncodeRequest):
    return encode_jwt_logic(data)

@router.post(
    "/decode",
    response_model=JWTDecodeResponse,
    summary="Decode a JWT token",
    description="Decodes a JWT token and returns its payload and headers"
)
async def decode_jwt(data: JWTDecodeRequest):
    return decode_jwt_logic(data)