import string
import secrets
from fastapi import HTTPException
from typing import List

def generate_password_logic(
    length: int,
    include_numbers: bool,
    include_special: bool,
    include_uppercase: bool,
    include_lowercase: bool
) -> str:
    """
    Generate a secure random password based on specified criteria.

    Args:
        length: Desired password length
        include_numbers: Include digits (0-9)
        include_special: Include special characters (e.g., !@#$%^)
        include_uppercase: Include uppercase letters (A-Z)
        include_lowercase: Include lowercase letters (a-z)

    Returns:
        str: Generated password

    Raises:
        HTTPException: If inputs are invalid or no character types are selected
    """
    if length < 8 or length > 128:
        raise HTTPException(status_code=400, detail="Password length must be between 8 and 128 characters")

    # Build character pool
    char_pool = ""
    if include_numbers:
        char_pool += string.digits
    if include_special:
        char_pool += string.punctuation
    if include_lowercase:
        char_pool += string.ascii_lowercase
    if include_uppercase:
        char_pool += string.ascii_uppercase

    if not char_pool:
        raise HTTPException(status_code=400, detail="At least one character type must be selected")

    # Ensure at least one character of each selected type
    required_chars: List[str] = []
    if include_numbers:
        required_chars.append(secrets.choice(string.digits))
    if include_special:
        required_chars.append(secrets.choice(string.punctuation))
    if include_lowercase:
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if include_uppercase:
        required_chars.append(secrets.choice(string.ascii_uppercase))

    remaining_length = length - len(required_chars)
    if remaining_length < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Password length ({length}) too short to include all required character types"
        )

    # Generate remaining characters
    password_chars = required_chars + [
        secrets.choice(char_pool) for _ in range(remaining_length)
    ]

    # Shuffle the password to ensure randomness
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)