from datetime import datetime
import ulid
from fastapi import HTTPException
from typing import Dict, List

def get_ulid_logic() -> Dict[str, str]:
    """
    Generate a single UUID version 4 (random) GUID.

    Returns:
        dict: A dictionary containing the generated GUID
    """
    return {"ulid": str(ulid.new())}

def get_bulk_ulids_logic(count: int) -> Dict[str, List[str]]:
    """
    Generate multiple UUID version 4 (random) GUIDs.

    Args:
        count: Number of GUIDs to generate

    Returns:
        dict: A dictionary containing a list of generated GUIDs

    Raises:
        HTTPException: If count is invalid
    """
    if count < 1 or count > 1000:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 1000")

    return {"ulids": [str(ulid.new()) for _ in range(count)]}

def get_ulid_timestamp_logic(ulid_str: str) -> Dict[str, str]:
    """
    Gets timestamp from the given ULID.

    Args:
        ULID: ULID to be parsed

    Returns:
        dict: A dictionary containing the parsed timestamp.

    Raises:
        HTTPException: If ULID is invalid
    """
    try:
        parsed_ulid = ulid.from_str(ulid_str)
        timestamp_ms = parsed_ulid.timestamp().int
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000.0)
        return {"Timestamp": timestamp}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ULID string")