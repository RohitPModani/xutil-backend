from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from typing import Optional

# Constants
DEFAULT_FONT_SIZE = 16

# Conversion type enum
class ConversionType(str, Enum):
    PX_TO_REM_EM = "px-to-rem-em"
    REM_TO_PX_EM = "rem-to-px-em"
    EM_TO_PX_REM = "em-to-px-rem"

# Request model for query parameters
class ConversionRequest(BaseModel):
    value: float = Field(..., gt=0, description="Value to convert")
    root_font_size: float = Field(
        DEFAULT_FONT_SIZE, gt=0, description="Root font size in pixels (for REM)"
    )
    parent_font_size: float = Field(
        DEFAULT_FONT_SIZE, gt=0, description="Parent font size in pixels (for EM)"
    )

# Response model
class ConversionResponse(BaseModel):
    px: Optional[float] = Field(None, description="PX value")
    rem: Optional[float] = Field(None, description="REM value")
    em: Optional[float] = Field(None, description="EM value")