from fastapi import APIRouter, Query
from ...crud.encoding_decoding.guid_generator_crud import get_guid_logic, get_bulk_guids_logic

router = APIRouter(prefix="/guid", tags=["GUID"])

@router.get(
    "/",
    summary="Generate a single GUID",
    description="Generates a single UUID version 4 (random) GUID",
    response_description="A single GUID as a string",
)
async def get_guid():
    return get_guid_logic()

@router.get(
    "/bulk",
    summary="Generate multiple GUIDs",
    description="Generates multiple UUID version 4 (random) GUIDs",
    response_description="A list of generated GUIDs",
)
async def get_bulk_guids(
    count: int = Query(5, ge=1, le=1000, description="Number of GUIDs to generate (1-1000)")
):
    return get_bulk_guids_logic(count)