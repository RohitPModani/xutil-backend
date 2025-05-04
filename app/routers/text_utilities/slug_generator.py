from fastapi import APIRouter, HTTPException
from ...schemas.text_utilities.slug_converter_schema import SlugGenerateRequest, SlugGenerateResponse
from ...crud.text_utilities.slug_generator_crud import generate_slug_logic
import re

router = APIRouter(prefix="/slug", tags=["Slug Generator"])
@router.post("/generate", response_model=SlugGenerateResponse)
async def generate_slug(data: SlugGenerateRequest) -> SlugGenerateResponse:
    """
    Generate a URL-friendly slug from input text.
    
    Args:
        data: SlugGenerateRequest containing text, separator, and case
        
    Returns:
        SlugGenerateResponse with the generated slug
        
    Raises:
        HTTPException: If input validation fails or generation fails
    """
    try:
        slug = generate_slug_logic(data.text, data.separator, data.case)
        if not slug:
            raise ValueError("Generated slug is empty")
        return SlugGenerateResponse(slug=slug)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")