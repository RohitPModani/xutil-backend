from pydantic import BaseModel, Field

class YAMLInput(BaseModel):
    yaml_text: str = Field(..., min_length=1, description="YAML text to convert to JSON")

class JSONInput(BaseModel):
    json_text: str = Field(..., min_length=1, description="JSON text to convert to YAML")

class ConversionResponse(BaseModel):
    result: str = Field(..., description="Converted data")