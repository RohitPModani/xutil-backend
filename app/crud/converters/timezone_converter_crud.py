from datetime import datetime
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from ...schemas.converters.timezone_converter_schema import TimezoneRequest

def convert_timezone_logic(request: TimezoneRequest) -> dict:
    try:
        naive_dt = datetime.strptime(request.datetime_str, "%Y-%m-%d %H:%M:%S")
        from_tz = pytz.timezone(request.from_timezone)
        to_tz = pytz.timezone(request.to_timezone)
        try:
            localized_dt = from_tz.localize(naive_dt, is_dst=None)
        except AmbiguousTimeError:
            return {"error": "Ambiguous time (DST transition). Please specify a non-ambiguous time."}
        except NonExistentTimeError:
            return {"error": "Non-existent time (DST transition). Please specify a valid time."}
        target_dt = localized_dt.astimezone(to_tz)
        return {
            "result": target_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
        }
    except Exception as e:
        return {"error": str(e)}
