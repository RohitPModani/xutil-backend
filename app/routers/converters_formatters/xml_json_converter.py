from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from ...crud.converters_formatters.xml_json_converter_crud import (
    json_xml_file_logic,
    json_xml_logic,
    xml_json_logic,
    xml_json_file_logic
)
from ...schemas.converters_formatters.xml_json_converter_schema import (
    ConversionResponse,
    JSONInput,
    XMLInput
)

router = APIRouter(prefix="/xml-json", tags=["XML - JSON"])

@router.post(
    "/xml-to-json",
    summary="Convert XML to JSON",
    description="Converts the provided XML text into JSON format.",
    response_description="JSON representation of the input XML",
    response_model=ConversionResponse
)
async def xml_to_json(input: XMLInput):
    result = xml_json_logic(input.xml_text)
    return ConversionResponse(result=result)

@router.post(
    "/json-to-xml",
    summary="Convert JSON to XML",
    description="Converts the provided JSON text into XML format.",
    response_description="XML representation of the input JSON",
    response_model=ConversionResponse
)
async def json_to_xml(input: JSONInput):
    result = json_xml_logic(input.json_text)
    return ConversionResponse(result=result)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

@router.post(
    "/xml-to-json-file",
    summary="Convert XML file to JSON",
    description="Uploads an XML file and converts its contents to JSON format.",
    response_description="JSON representation of the input XML file",

)
async def convert_xml_to_json(file: UploadFile = File(...)):
    # Validate file extension
    if not file.filename.lower().endswith(".xml"):
        raise HTTPException(status_code=400, detail="Only XML files (.xml) are supported")

    # Validate content type
    if file.content_type not in ["application/xml", "text/xml"]:
        raise HTTPException(status_code=400, detail="Invalid content type. Must be XML")

    # Check file size
    file_size = 0
    contents = b""

    try:
        contents = await file.read()
        file_size = len(contents)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE / (1024 * 1024)}MB limit")
        return xml_json_file_logic(contents)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post(
    "/json-to-xml-file",
    summary="Convert JSON file to XML",
    description="Uploads a JSON file and converts its contents to XML format.",
    response_description="XML representation of the input JSON file",
    response_model=ConversionResponse
)
async def convert_json_to_xml(file: UploadFile = File(...)):
    # Validate file extension
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files (.json) are supported")

    # Validate content type
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid content type. Must be JSON")

    # Check file size
    file_size = 0
    contents = b""

    try:
        contents = await file.read()
        file_size = len(contents)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE / (1024 * 1024)}MB limit")
        return json_xml_file_logic(contents)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")