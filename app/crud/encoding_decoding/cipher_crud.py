from fastapi import HTTPException

def validate_text_has_alnum(text: str) -> None:
    """Raise an HTTPException if the input text contains no alphanumeric characters."""
    if not any(c.isalnum() for c in text):
        raise HTTPException(status_code=422, detail="Input text must contain at least one letter or digit")

def rot13_cipher_logic(text: str) -> str:
    """Apply ROT13 transformation to the input text, shifting letters by 13 and digits by 3."""
    validate_text_has_alnum(text)
    return caesar_cipher_logic(text, shift=13)

def caesar_cipher_logic(text: str, shift: int) -> str:
    """Apply Caesar cipher transformation to the input text, shifting letters and digits."""
    validate_text_has_alnum(text)
    letter_shift = shift % 26
    digit_shift = shift % 10
    return ''.join(
        chr((ord(c) - ord('a') + letter_shift) % 26 + ord('a')) if c.islower() else
        chr((ord(c) - ord('A') + letter_shift) % 26 + ord('A')) if c.isupper() else
        chr((ord(c) - ord('0') + digit_shift) % 10 + ord('0')) if c.isdigit() else c
        for c in text
    )