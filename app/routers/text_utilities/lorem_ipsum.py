from fastapi import APIRouter, HTTPException
from ...schemas.text_utilities.lorem_ipsum_schema import LoremIpsumRequest, LoremIpsumResponse
from ...crud.text_utilities.lorem_ipsum_crud import generate_lorem_ipsum_logic

router = APIRouter(prefix="/lorem-ipsum", tags=["Lorem Ipsum Generator"])

@router.post("/generate", response_model=LoremIpsumResponse)
async def generate_lorem_ipsum(data: LoremIpsumRequest) -> LoremIpsumResponse:
    """
    Generate Lorem Ipsum text based on specified type and count, starting with 'Lorem ipsum dolor sit amet'.
    
    Args:
        data: LoremIpsumRequest containing type, count, and format
        
    Returns:
        LoremIpsumResponse with generated text or HTML
    """
    try:
        return generate_lorem_ipsum_logic(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Lorem Ipsum: {str(e)}")
