import html
from typing import Dict

def encode_html_entities_logic(text: str) -> Dict[str, str]:
    """
    Encode special characters in text to HTML entities.
    
    Args:
        text: Input text to encode.
    
    Returns:
        Dictionary containing original and encoded text.
    
    Raises:
        ValueError: If input text is invalid.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    return {
        "original_text": text,
        "encoded_text": html.escape(text, quote=True)
    }

def decode_html_entities_logic(text: str) -> Dict[str, str]:
    """
    Decode HTML entities to their original characters.
    
    Args:
        text: Input text containing HTML entities.
    
    Returns:
        Dictionary containing encoded and decoded text.
    
    Raises:
        ValueError: If input text is invalid.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    return {
        "encoded_text": text,
        "decoded_text": html.unescape(text)
    }