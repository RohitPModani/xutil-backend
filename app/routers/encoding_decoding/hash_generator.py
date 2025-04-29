from fastapi import APIRouter
from ...crud.encoding_decoding.hash_generator_crud import generate_hash_logic
from ...schemas.encoding_decoding.hash_generator_schema import HashRequest, HashResponse

router = APIRouter(prefix="/hash", tags=["Hash"])

@router.post(
    "/generate",
    response_model=HashResponse,
    summary="Generate a hash",
    description="Generates a cryptographic hash of the input text using the specified algorithm",
    response_description="Hashed text with metadata",
)
async def generate_hash(data: HashRequest):
    return generate_hash_logic(data.text, data.algorithm)