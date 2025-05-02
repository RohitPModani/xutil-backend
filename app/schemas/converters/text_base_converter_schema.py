from pydantic import BaseModel, model_validator
import re

class TextInput(BaseModel):
    input_text: str
    target_base: int

    @model_validator(mode='after')
    def validate_number(cls, data):
        text = data.input_text
        target_base = data.target_base

        if not text:
            raise ValueError("Input text cannot be empty")
        if target_base not in {2,8,10,16}:
            raise ValueError("Target base must be a valid base (2, 8, 10, 16)")
        if not re.match(r"^[0-9A-Z]+$", text, re.IGNORECASE):
            raise ValueError("Number must contain only valid digits (0-9, A-Z)")

        return data

class BaseInput(BaseModel):
    base_text: str
    source_base: int

    @model_validator(mode='after')
    def validate_number(cls, data):
        text = data.base_text
        source_base = data.source_base

        if not text:
            raise ValueError("Input text cannot be empty")
        if source_base not in {2,8,10,16}:
            raise ValueError("Target base must be a valid base (2, 8, 10, 16)")
        
        return data

class ConversionResponse(BaseModel):
    result: str