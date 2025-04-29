from enum import Enum
from pydantic import BaseModel, Field

class BaseType(str, Enum):
    base32 = "base32"
    base58 = "base58"
    base64 = "base64"

class BaseEncodeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to be encoded")
    base_type: BaseType = Field(..., description="Base type for encoding (e.g., base64)")

class BaseDecodeRequest(BaseModel):
    encoded_text: str = Field(..., min_length=1, description="Text to be decoded")
    base_type: BaseType = Field(..., description="Base type for decoding (e.g., base64)")

class BaseEncodeResponse(BaseModel):
    input_text: str
    base_type: str
    encoded_text: str

    class Config:
        use_enum_values = True

class BaseDecodeResponse(BaseModel):
    encoded_text: str
    base_type: str
    decoded_text: str

    class Config:
        use_enum_values = True