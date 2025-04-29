from fastapi import APIRouter, Query
from ...crud.encoding_decoding.password_generator_crud import generate_password_logic
from typing import Optional

router = APIRouter(prefix="/password", tags=["Password Generator"])

@router.get(
    "/generate",
    summary="Generate a secure password",
    description="Generates a random password with specified length and character types",
    response_description="Generated password as a string",
)
async def generate_password(
    length: int = Query(..., ge=8, le=128, description="Password length (8-128 characters)"),
    include_numbers: bool = Query(True, description="Include digits (0-9)"),
    include_special: bool = Query(True, description="Include special characters (e.g., !@#$%^)"),
    include_uppercase: bool = Query(True, description="Include uppercase letters (A-Z)"),
    include_lowercase: bool = Query(True, description="Include lowercase letters (a-z)")
) -> str:
    return generate_password_logic(
        length=length,
        include_numbers=include_numbers,
        include_special=include_special,
        include_uppercase=include_uppercase,
        include_lowercase=include_lowercase
    )