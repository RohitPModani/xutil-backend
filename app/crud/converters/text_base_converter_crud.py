import re

def text_to_base_logic(text: str, target_base: int) -> str:
    """Convert text to a numeric base (binary, octal, decimal, hexadecimal).
    
    Args:
        text: Input text to convert (ASCII/UTF-8).
        target_base: Target base (2 for binary, 8 for octal, 10 for decimal, 16 for hexadecimal).
    
    Returns:
        Space-separated string of code points in the target base.
    
    Raises:
        ValueError: If text is empty or target_base is invalid.
    """
    if not text:
        raise ValueError("Input text cannot be empty")
    if target_base not in {2, 8, 10, 16}:
        raise ValueError("Target base must be 2 (binary), 8 (octal), 10 (decimal), or 16 (hexadecimal)")
    
    result = []
    for char in text:
        code_point = ord(char)
        if target_base == 2:
            # Binary: 8-bit padded
            binary = bin(code_point)[2:].zfill(8)
            result.append(binary)
        elif target_base == 8:
            # Octal: 3-digit padded
            octal = oct(code_point)[2:].zfill(3)
            result.append(octal)
        elif target_base == 10:
            # Decimal: Direct code point
            result.append(str(code_point))
        elif target_base == 16:
            # Hexadecimal: 2-digit padded
            hex_val = hex(code_point)[2:].upper().zfill(2)
            result.append(hex_val)
    
    return ' '.join(result)

def base_to_text_logic(input_str: str, source_base: int) -> str:
    """Convert a numeric base (binary, octal, decimal, hexadecimal) to text.
    
    Args:
        input_str: Space-separated string of numbers in the source base.
        source_base: Source base (2 for binary, 8 for octal, 10 for decimal, 16 for hexadecimal).
    
    Returns:
        Decoded text string.
    
    Raises:
        ValueError: If input is invalid or contains invalid digits/code points.
    """
    if not input_str:
        raise ValueError("Input string cannot be empty")
    if source_base not in {2, 8, 10, 16}:
        raise ValueError("Source base must be 2 (binary), 8 (octal), 10 (decimal), or 16 (hexadecimal)")
    
    # Define valid digits for each base
    valid_digits = {
        2: r'^[0-1]+$',
        8: r'^[0-7]+$',
        10: r'^[0-9]+$',
        16: r'^[0-9A-Fa-f]+$'
    }
    
    chunks = input_str.split()
    if not chunks:
        raise ValueError("Input must contain at least one number")
    
    result = []
    for chunk in chunks:
        # Validate digits
        if not re.match(valid_digits[source_base], chunk):
            raise ValueError(f"Invalid digits in '{chunk}' for base {source_base}")
        
        try:
            # Convert chunk to decimal
            code_point = int(chunk, source_base)
            # Validate code point (UTF-8 range: 0 to 1114111)
            if not (0 <= code_point <= 1114111):
                raise ValueError(f"Code point {code_point} is out of valid UTF-8 range (0-1114111)")
            # Convert to character
            result.append(chr(code_point))
        except ValueError as e:
            if str(e).startswith("invalid literal"):
                raise ValueError(f"Invalid number '{chunk}' for base {source_base}")
            raise
    
    return ''.join(result)