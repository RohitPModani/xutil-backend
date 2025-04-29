from pydantic import BaseModel, Field, field_validator

class ROT13Request(BaseModel):
    text: str = Field(..., min_length=1, description="Text to encode/decode using ROT13")

class ROT13Response(BaseModel):
    input_text: str = Field(..., min_length=1, description="The original input text")
    output_text: str = Field(..., description="The text after applying ROT13 transformation")

class CaesarRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to encode/decode")
    shift: int = Field(..., ge=-100, le=100, description="Shift value for the Caesar cipher")

class CaesarResponse(BaseModel):
    input_text: str = Field(..., min_length=1, description="The original input text")
    shift: int = Field(..., description="The shift value used for encoding")
    output_text: str = Field(..., description="The text after applying the Caesar cipher encoding")