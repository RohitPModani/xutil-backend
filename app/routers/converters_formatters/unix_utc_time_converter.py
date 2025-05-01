from fastapi import APIRouter
from fastapi import Body
from ...crud.converters_formatters.unix_utc_time_crud import unix_to_utc_logic, utc_to_unix_logic
from ...schemas.converters_formatters.unix_utc_time_schema import UnixTimeRequest, UnixTimeResponse, UtcTimeRequest, UtcTimeResponse

router = APIRouter(
    prefix="/unix-utc",
    tags=["Unix <-> UTC Converter"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/unix-to-utc",
    response_model=UnixTimeResponse,
    summary="Convert Unix timestamp to UTC datetime",
    description="Convert a Unix timestamp (seconds since epoch) to a UTC datetime string in ISO 8601 format."
)
async def unix_to_utc(request: UnixTimeRequest = Body(...)):
    return unix_to_utc_logic(request.timestamp)

@router.post(
    "/utc-to-unix",
    response_model=UtcTimeResponse,
    summary="Convert UTC datetime to Unix timestamp",
    description="Convert a UTC datetime string ('YYYY-MM-DD HH:MM:SS') to a Unix timestamp (seconds since epoch)."
)
async def utc_to_unix(request: UtcTimeRequest = Body(...)):
    return utc_to_unix_logic(request.datetime_utc)
