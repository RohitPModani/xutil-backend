from pydantic import BaseModel, Field

class XMLInput(BaseModel):
    xml_text: str = Field(..., min_length=1, description="XML text to convert to JSON")

class JSONInput(BaseModel):
    json_text: str = Field(..., min_length=1, description="JSON text to convert to XML")

class ConversionResponse(BaseModel):
    result: str = Field(..., description="Converted data")