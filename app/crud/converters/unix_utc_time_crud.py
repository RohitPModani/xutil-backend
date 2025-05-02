from datetime import datetime, timezone
from fastapi import HTTPException
from ...schemas.converters.unix_utc_time_schema import UnixTimeResponse, UtcTimeResponse

def unix_to_utc_logic(timestamp: int) -> UnixTimeResponse:
    try:
        dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return UnixTimeResponse(
            datetime_utc=dt_utc.isoformat(),
            timestamp=timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid timestamp: {e}")

def utc_to_unix_logic(datetime_utc_str: str) -> UtcTimeResponse:
    try:
        dt = datetime.strptime(datetime_utc_str, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
        timestamp = int(dt.timestamp())
        return UtcTimeResponse(
            datetime_utc=dt.isoformat(),
            timestamp=timestamp
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use 'YYYY-MM-DD HH:MM:SS'")
