from pydantic import BaseModel

class TimezoneRequest(BaseModel):
    datetime_str: str
    from_timezone: str
    to_timezone: str