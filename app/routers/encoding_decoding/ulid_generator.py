from fastapi import APIRouter, Query
from ...crud.encoding_decoding.ulid_generator_crud import get_ulid_logic, get_bulk_ulids_logic, get_ulid_timestamp_logic

router = APIRouter(prefix="/ulid", tags=["ULID"])

@router.get(
    "/",
    summary="Generate a single ULID",
    description="Generates a single ULID",
    response_description="A single ULID as a string",
)
async def get_ulid():
    return get_ulid_logic()

@router.get(
    "/bulk",
    summary="Generate multiple ULIDs",
    description="Generates multiple ULIDs",
    response_description="A list of generated ULIDs",
)
async def get_bulk_guids(
    count: int = Query(5, ge=1, le=1000, description="Number of ULIDs to generate (1-1000)")
):
    return get_bulk_ulids_logic(count)

@router.get(
    "/timestamp",
    summary="Get timestamp",
    description="Gets the timestamp from ULID",
    response_description="The timestamp from ULID",
)
async def get_ulid_timestamp(
    ULID_str: str = Query(..., description="ULID for which timestamp is to be fetched")
):
    return get_ulid_timestamp_logic(ULID_str)