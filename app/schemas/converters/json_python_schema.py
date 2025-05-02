import json
from pydantic import BaseModel, field_validator
import re

class JSONInput(BaseModel):
    json_data: str
    class_name: str = "Root"

    @field_validator("json_data")
    def validate_json(cls, v):
        try:
            json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        return v
    
    @field_validator("class_name")
    def validate_class_name(cls, v):
        if not re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', v):
            raise ValueError("Invalid class name. Must be a valid Python identifier")
        return v

class ConversionResponse(BaseModel):
    result: str