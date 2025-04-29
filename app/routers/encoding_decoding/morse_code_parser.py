from fastapi import APIRouter, Query
from ...schemas.encoding_decoding.morse_code_parser_schema import MorseInput
from ...crud.encoding_decoding.morse_code_parser_crud import (
    char_to_morse_logic,
    morse_to_char_logic,
    char_to_morse_file_logic,
    morse_to_char_file_logic,
)

router = APIRouter(prefix="/morse", tags=["Morse Code"])

@router.post(
    "/char-to-morse",
    summary="Convert text to Morse code",
    description="Converts a text string to Morse code, Make sure that the words are separated by a single space",
    response_description="Morse code string, In the output each letter will be separated by a space and each word by '/'",
)
async def char_to_morse(payload: MorseInput):
    return {"morse_code": char_to_morse_logic(payload.text)}

@router.post(
    "/morse-to-char",
    summary="Convert Morse code to text",
    description="Converts a Morse code string to text, Make sure that each letter is separated by a space and each word by '/'",
    response_description="Decoded text string",
)
async def morse_to_char(payload: MorseInput):
    return {"decoded_text": morse_to_char_logic(payload.text)}

@router.post(
    "/char-to-morse-file",
    summary="Convert text file to Morse code",
    description="Converts a .txt file's content to Morse code and saves to a new file",
    response_description="Path to the generated Morse code file",
)
async def char_to_morse_file(
    file_path: str
):
    return {"file_path": char_to_morse_file_logic(file_path)}

@router.post(
    "/morse-to-char-file",
    summary="Convert Morse code file to text",
    description="Converts a Morse code .txt file to text and saves to a new file",
    response_description="Path to the generated text file",
)
async def morse_to_char_file(
    file_path: str
):
    return {"file_path": morse_to_char_file_logic(file_path)}