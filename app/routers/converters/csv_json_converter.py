from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from ...schemas.converters.csv_json_schema import (
    ConversionResponse,
    JSONInput,
)
from ...crud.converters.csv_json_crud import (
    csv_to_json_logic,
    json_to_csv_logic,
)

router = APIRouter(
    prefix="/csv-json",
    tags=["CSV - JSON/XML"],
    responses={404: {"description": "Not found"}}
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post(
    "/csv-to-json",
    summary="Convert CSV File to JSON",
    description="Converts an uploaded CSV file (.csv) to JSON format. Max file size: 10MB.",
    response_description="JSON representation of the CSV file data",
    response_model=ConversionResponse,
    status_code=status.HTTP_200_OK
)
async def csv_to_json(file: UploadFile = File(...), separator: str = Form('_')):
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only .csv files are supported")
        
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE/1024/1024}MB limit")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="File is empty")

        return csv_to_json_logic(contents, separator=separator)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV to JSON conversion failed: {str(e)}")

@router.post(
    "/json-to-csv",
    summary="Convert JSON to CSV",
    description="Converts provided JSON data to CSV format.",
    response_description="CSV representation of the JSON data",
    response_model=ConversionResponse,
    status_code=status.HTTP_200_OK
)
async def json_to_csv(input: JSONInput):
    try:
        return json_to_csv_logic(input.json_data, separator=input.separator)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON to CSV conversion failed: {str(e)}")