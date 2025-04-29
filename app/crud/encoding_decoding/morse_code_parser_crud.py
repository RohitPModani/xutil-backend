import os
from fastapi import HTTPException
from ...schemas.encoding_decoding.morse_code_parser_schema import CHAR_TO_MORSE, MORSE_TO_CHAR
from typing import List

def char_to_morse_logic(text: str) -> str:
    """
    Convert text to Morse code.

    Args:
        text: Input text to convert

    Returns:
        str: Morse code string with spaces between codes and '/' for word breaks

    Raises:
        HTTPException: If input is empty
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    text = text.upper()
    morse_code: List[str] = []
    for char in text:
        morse_code.append(CHAR_TO_MORSE.get(char, '?'))

    return ' '.join(morse_code)

def morse_to_char_logic(text: str) -> str:
    """
    Convert Morse code to text.

    Args:
        text: Input Morse code string

    Returns:
        str: Decoded text string

    Raises:
        HTTPException: If input is empty or invalid
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input Morse code cannot be empty")

    words = text.strip().split(" / ")
    if not words or not any(word.strip() for word in words):
        raise HTTPException(status_code=400, detail="Invalid Morse code format")

    final_text: List[str] = []
    for word in words:
        letters = word.strip().split()
        if not letters:
            continue
        decoded_word = ''
        for symbol in letters:
            if not symbol:
                continue
            decoded_word += MORSE_TO_CHAR.get(symbol, '?')
        final_text.append(decoded_word)

    return ' '.join(final_text) if final_text else ''

def char_to_morse_file_logic(file_path: str) -> str:
    """
    Convert a text file to Morse code and save to a new file.

    Args:
        file_path: Path to the input .txt file

    Returns:
        str: Path to the generated Morse code file

    Raises:
        HTTPException: If file is invalid or inaccessible
    """
    if not file_path.strip():
        raise HTTPException(status_code=400, detail="File path cannot be empty")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    if not file_path.lower().endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    if not os.access(os.path.dirname(file_path), os.W_OK):
        raise HTTPException(status_code=400, detail="No write permission for output directory")

    file_name = os.path.basename(file_path)
    name, _ = os.path.splitext(file_name)
    output_file_path = os.path.join(os.path.dirname(file_path), f"{name}_morse.txt")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if not content.strip():
            raise HTTPException(status_code=400, detail="Input file is empty")

        morse_code = char_to_morse_logic(content)
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(morse_code)

        return output_file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

def morse_to_char_file_logic(file_path: str) -> str:
    """
    Convert a Morse code file to text and save to a new file.

    Args:
        file_path: Path to the input Morse code .txt file

    Returns:
        str: Path to the generated text file

    Raises:
        HTTPException: If file is invalid or inaccessible
    """
    if not file_path.strip():
        raise HTTPException(status_code=400, detail="File path cannot be empty")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    if not file_path.lower().endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    if not os.access(os.path.dirname(file_path), os.W_OK):
        raise HTTPException(status_code=400, detail="No write permission for output directory")

    file_name = os.path.basename(file_path)
    name, _ = os.path.splitext(file_name)
    output_file_path = os.path.join(os.path.dirname(file_path), f"{name}_char.txt")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if not content.strip():
            raise HTTPException(status_code=400, detail="Input file is empty")

        decoded_text = morse_to_char_logic(content)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(decoded_text)

        return output_file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")