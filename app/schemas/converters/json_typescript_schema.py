from pydantic import BaseModel
import re

class JSONInput(BaseModel):
    json_data: str
    interface_name: str = "Data"

class ConversionResponse(BaseModel):
    result: str