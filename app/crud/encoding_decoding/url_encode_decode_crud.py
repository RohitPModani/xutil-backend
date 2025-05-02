from urllib.parse import quote, unquote
from fastapi import HTTPException

def encode_url_logic(text: str) -> dict:
    """
    Encode a URL string with customizable safe characters.
    
    Args:
        text: Input text to encode
        safe: Characters to exclude from encoding (default: "/")
        
    Returns:
        Dictionary containing original and encoded text
        
    Raises:
        HTTPException: If input is empty or invalid
    """
    if not text or text.isspace():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    try:
        encoded = quote(text, '')
        return {"original_text": text, "encoded_text": encoded}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encoding failed: {str(e)}")

def decode_url_logic(encoded_text: str) -> dict:
    """
    Decode an encoded URL string.
    
    Args:
        encoded_text: Encoded text to decode
        
    Returns:
        Dictionary containing encoded and decoded text
        
    Raises:
        HTTPException: If input is empty or invalid
    """
    if not encoded_text or encoded_text.isspace():
        raise HTTPException(status_code=400, detail="Encoded text cannot be empty")
    
    try:
        decoded = unquote(encoded_text)
        return {"encoded_text": encoded_text, "decoded_text": decoded}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decoding failed: {str(e)}")