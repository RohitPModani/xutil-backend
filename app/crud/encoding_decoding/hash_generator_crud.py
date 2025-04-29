import hashlib
from fastapi import HTTPException
from ...schemas.encoding_decoding.hash_generator_schema import HashAlgorithm, HashResponse
from typing import Dict, Any

def generate_hash_logic(text: str, algorithm: HashAlgorithm) -> HashResponse:
    """
    Generate a cryptographic hash for the input text using the specified algorithm.

    Args:
        text: Input text to hash
        algorithm: Hashing algorithm to use (md5, sha1, sha256, sha512)

    Returns:
        HashResponse: Pydantic model with original text, algorithm, and hashed text

    Raises:
        HTTPException: If input is invalid or algorithm is unsupported
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    # Dictionary mapping enum values to hashlib functions
    hash_algorithms: Dict[HashAlgorithm, Any] = {
        HashAlgorithm.md5: hashlib.md5,
        HashAlgorithm.sha1: hashlib.sha1,
        HashAlgorithm.sha256: hashlib.sha256,
        HashAlgorithm.sha512: hashlib.sha512,
    }

    # Validate algorithm
    if algorithm not in hash_algorithms:
        raise HTTPException(status_code=400, detail=f"Unsupported algorithm: {algorithm.value}")

    # Generate hash
    try:
        hash_func = hash_algorithms[algorithm]()
        hash_func.update(text.encode('utf-8'))
        hashed_text = hash_func.hexdigest()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate hash: {str(e)}")

    return HashResponse(
        text=text,
        algorithm=algorithm.value,
        hashed_text=hashed_text
    )