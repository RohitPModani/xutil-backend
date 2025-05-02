from pydantic import BaseModel, model_validator
import re

class NumberInput(BaseModel):
    number: str
    source_base: int
    target_base: int

    @model_validator(mode='after')
    def validate_number(cls, data):
        number = data.number
        source_base = data.source_base
        target_base = data.target_base

        if not number:
            raise ValueError("Number cannot be empty")
        if source_base < 2 or source_base > 36:
            raise ValueError("Source base must be a valid base (2-36)")
        if target_base < 2 or target_base > 36:
            raise ValueError("Target base must be a valid base (2-36)")
        if not re.match(r"^[0-9A-Z]+$", number, re.IGNORECASE):
            raise ValueError("Number must contain only valid digits (0-9, A-Z)")
        try:
            int(number, source_base)
        except ValueError:
            raise ValueError(f"Invalid number '{number}' for base {source_base}")
        return data

    class Config:
        validate_assignment = True
        use_enum_values = True

class ConversionResponse(BaseModel):
    result: str