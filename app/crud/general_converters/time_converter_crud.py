from fastapi import HTTPException
from app.schemas.general_converters.time_converter_scehma import (
    TimeConvertRequest,
    TimeConvertResponse,
    UNIT_TO_SECONDS
)

def convert_time_logic(data: TimeConvertRequest) -> TimeConvertResponse:
    if data.unit not in UNIT_TO_SECONDS:
        raise HTTPException(status_code=400, detail=f"Invalid unit: {data.unit}. Supported units: {list(UNIT_TO_SECONDS.keys())}")
    
    input_seconds = data.value * UNIT_TO_SECONDS[data.unit]
    return TimeConvertResponse(
        **{
            key: round(input_seconds / seconds, 8)
            for key, seconds in UNIT_TO_SECONDS.items()
        }
    )