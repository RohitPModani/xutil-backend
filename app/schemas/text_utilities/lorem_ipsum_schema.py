from typing import Literal
from pydantic import BaseModel, Field
from pydantic import field_validator
from enum import Enum

class LoremType(str, Enum):
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"
    WORD = "word"

class OutputFormat(str, Enum):
    TEXT = "text"
    HTML = "html"

class LoremIpsumRequest(BaseModel):
    type: LoremType = Field(LoremType.PARAGRAPH, description="Type of Lorem Ipsum to generate (paragraph, sentence, word)")
    count: int = Field(..., description="Number of paragraphs (1-20), sentences (1-50), or words (1-100)", ge=1)
    format: OutputFormat = Field(OutputFormat.TEXT, description="Output format (text or html)")

    @field_validator("count")
    def validate_count(cls, v, info):
        type_value = info.data.get("type")
        if type_value == LoremType.PARAGRAPH and not 1 <= v <= 20:
            raise ValueError("Paragraph count must be between 1 and 20")
        elif type_value == LoremType.SENTENCE and not 1 <= v <= 50:
            raise ValueError("Sentence count must be between 1 and 50")
        elif type_value == LoremType.WORD and not 1 <= v <= 100:
            raise ValueError("Word count must be between 1 and 100")
        return v

class LoremIpsumResponse(BaseModel):
    content: str = Field(..., description="Generated Lorem Ipsum text or HTML")