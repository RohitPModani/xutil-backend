from pydantic import BaseModel, Field

class JSONInput(BaseModel):
    json_data: str = Field(..., min_length=1, description="JSON data to convert to CSV (expected as a list of objects)")
    separator: str = Field('_', description="Separator used for nested fields during conversion")

class ConversionResponse(BaseModel):
    result: str = Field(..., description="Converted data (JSON, XML or CSV)")
