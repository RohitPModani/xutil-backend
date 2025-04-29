from pydantic import BaseModel, Field

class URLEncodeResponse(BaseModel):
    original_text: str = Field(..., description="The original input text")
    encoded_text: str = Field(..., description="The URL-encoded text")

    class Config:
        schema_extra = {
            "example": {
                "original_text": "Hello World! & Special Chars",
                "encoded_text": "Hello%20World%21%20%26%20Special%20Chars"
            }
        }

class URLDecodeResponse(BaseModel):
    encoded_text: str = Field(..., description="The URL-encoded input text")
    decoded_text: str = Field(..., description="The decoded text")

    class Config:
        schema_extra = {
            "example": {
                "encoded_text": "Hello%20World%21%20%26%20Special%20Chars",
                "decoded_text": "Hello World! & Special Chars"
            }
        }