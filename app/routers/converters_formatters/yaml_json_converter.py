from fastapi import APIRouter, File, HTTPException, UploadFile
from ...schemas.converters_formatters.yaml_json_converter_schema import (
    YAMLInput,
    JSONInput,
    ConversionResponse,
)
from ...crud.converters_formatters.yaml_json_converter_crud import (
    yaml_to_json_logic,
    json_to_yaml_logic,
    yaml_json_file_logic,
    json_yaml_file_logic,
)

router = APIRouter(prefix="/yaml-json", tags=["YAML - JSON"])
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post(
    "/yaml-to-json",
    summary="Convert YAML to JSON",
    description="Converts the provided YAML text into JSON format.",
    response_description="JSON representation of the input YAML",
    response_model=ConversionResponse
)
async def yaml_to_json(input: YAMLInput):
    return yaml_to_json_logic(input.yaml_text)

@router.post(
    "/json-to-yaml",
    summary="Convert JSON to YAML",
    description="Converts the provided JSON text into YAML format.",
    response_description="YAML representation of the input JSON",
    response_model=ConversionResponse
)
async def json_to_yaml(input: JSONInput):
    return json_to_yaml_logic(input.json_text)

@router.post(
    "/yaml-to-json-file",
    summary="Convert YAML file to JSON",
    description="Uploads a YAML file and converts its contents to JSON format.",
    response_description="JSON representation of the input YAML file",
    response_model=ConversionResponse
)
async def convert_yaml_to_json(file: UploadFile = File(...)):
    # Validate file extension first
    if not file.filename.lower().endswith((".yaml", ".yml")):
        raise HTTPException(status_code=400, detail="Only .yaml or .yml files are supported")
    
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        return yaml_json_file_logic(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post(
    "/json-to-yaml-file",
    summary="Convert JSON file to YAML",
    description="Uploads a JSON file and converts its contents to YAML format.",
    response_description="YAML representation of the input JSON file",
    response_model=ConversionResponse
)
async def convert_json_to_yaml(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported")
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid content type. Expected JSON")
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        return json_yaml_file_logic(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")