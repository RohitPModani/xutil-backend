import uuid
from fastapi import HTTPException
from typing import Dict, List

def get_guid_logic() -> Dict[str, str]:
    """
    Generate a single UUID version 4 (random) GUID.

    Returns:
        dict: A dictionary containing the generated GUID
    """
    return {"guid": str(uuid.uuid4())}

def get_bulk_guids_logic(count: int) -> Dict[str, List[str]]:
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

    return {"guids": [str(uuid.uuid4()) for _ in range(count)]}