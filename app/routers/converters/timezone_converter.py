from fastapi import APIRouter, Body
import pytz
from ...schemas.converters.timezone_converter_schema import TimezoneRequest
from ...crud.converters.timezone_converter_crud import convert_timezone_logic

router = APIRouter(
    prefix="/timezone-converter",
    tags=["Timezone Converter"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/",
    summary="Convert datetime between timezones",
    description="Convert datettime from one timezone to another"
)
async def convert_timezone(request: TimezoneRequest = Body(...)):
    return convert_timezone_logic(request)

@router.get("/all-timezones")
def get_all_timezones():
    return {"timezones": pytz.all_timezones}