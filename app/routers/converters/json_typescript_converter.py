from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
import json
import re
from ...crud.converters.json_typescript_crud import json_to_typescript_logic
from ...schemas.converters.json_typescript_schema import ConversionResponse, JSONInput

router = APIRouter(
    prefix="/json-ts",
    tags=["JSON - TypeScript"],
    responses={404: {"description": "Not found"}}
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for reading

@router.post(
    "/json-to-typescript",
    summary="Convert JSON to TypeScript interface",
    description="Converts the provided JSON text into TypeScript interface. Supports nested objects, arrays, and primitive types (string, number, boolean, null). Maximum nesting depth is 50 levels.",
    response_description="TypeScript interface of the input JSON",
    response_model=ConversionResponse
)
async def json_to_typescript(input: JSONInput):
    try:
        return json_to_typescript_logic(input.json_data, input.interface_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post(
    "/json-to-typescript-file",
    summary="Convert JSON file to TypeScript interface",
    description="Uploads a JSON file and converts its contents to TypeScript interface. Supports nested objects, arrays, and primitive types. Maximum file size is 10MB.",
    response_description="TypeScript interface of the input JSON file",
    response_model=ConversionResponse
)
async def convert_json_to_typescript_file(file: UploadFile = File(...), interface_name: str = Form(default="Data")):
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported")
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid content type. Expected JSON")
    if not re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', interface_name):
        raise HTTPException(status_code=400, detail="Invalid interface name. Must be a valid TypeScript identifier")
    
    size = 0
    contents = b""
    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break
        size += len(chunk)
        if size > MAX_FILE_SIZE:
            await file.close()
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        contents += chunk
    
    await file.close()
    
    try:
        data = json.loads(contents.decode('utf-8'))
        result = json_to_typescript_logic(data, interface_name)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")