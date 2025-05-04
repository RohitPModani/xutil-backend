from typing import Literal
from pydantic import BaseModel, Field
from pydantic import field_validator
from enum import Enum

class Separator(str, Enum):
    HYPHEN = "-"
    UNDERSCORE = "_"
    DOT = "."

class Case(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"

class SlugGenerateRequest(BaseModel):
    text: str = Field(..., description="Text to convert into a slug", min_length=1)
    separator: Separator = Field(Separator.HYPHEN, description="Separator for the slug (-, _, .)")
    case: Case = Field(Case.LOWERCASE, description="Case for the slug (lowercase, uppercase)")

    @field_validator("text")
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v.strip()

class SlugGenerateResponse(BaseModel):
    slug: str = Field(..., description="Generated URL-friendly slug")