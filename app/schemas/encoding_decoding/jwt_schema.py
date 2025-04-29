from datetime import datetime
import re
from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator

class JWTEncodeRequest(BaseModel):
    payload: Dict = Field(..., description="JWT payload data")
    secret: str = Field(..., min_length=8, description="Secret key for signing")
    algorithm: str = Field(default="HS256", description="JWT signing algorithm")
    headers: Optional[Dict] = Field(None, description="Optional JWT headers")
    expiry_minutes: Optional[int] = Field(None, ge=1, description="Token expiry in minutes")

    @field_validator("algorithm")
    def validate_algorithm(cls, value):
        supported_algorithms = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
        if value not in supported_algorithms:
            raise ValueError(f"Algorithm must be one of {supported_algorithms}")
        return value

class JWTEncodeResponse(BaseModel):
    token: str = Field(..., description="Encoded JWT token")
    expires_at: Optional[datetime] = Field(None, description="Token expiry timestamp")

class JWTDecodeRequest(BaseModel):
    token: str = Field(..., description="JWT token to decode")
    secret: str = Field(..., min_length=8, description="Secret key for verification")
    algorithm: str = Field(default="HS256", description="JWT signing algorithm")
    verify_expiry: bool = Field(default=True, description="Verify token expiry")

    @field_validator("token")
    def validate_token_format(cls, value):
        if not re.match(r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$', value):
            raise ValueError("Invalid JWT token format")
        return value

class JWTDecodeResponse(BaseModel):
    payload: Dict = Field(..., description="Decoded JWT payload")
    headers: Dict = Field(..., description="JWT headers")
    issued_at: Optional[datetime] = Field(None, description="Token issuance timestamp")
    expires_at: Optional[datetime] = Field(None, description="Token expiry timestamp")