from pydantic import BaseModel, Field

class UnixTimeRequest(BaseModel):
    timestamp: int = Field(..., description="Unix timestamp in seconds")

class UnixTimeResponse(BaseModel):
    datetime_utc: str = Field(..., description="UTC datetime string in ISO 8601 format")
    timestamp: int = Field(..., description="Unix timestamp in seconds")

class UtcTimeRequest(BaseModel):
    datetime_utc: str = Field(..., description="UTC datetime string in 'YYYY-MM-DD HH:MM:SS' format")

class UtcTimeResponse(BaseModel):
    datetime_utc: str = Field(..., description="UTC datetime string in ISO 8601 format")
    timestamp: int = Field(..., description="Unix timestamp in seconds")
