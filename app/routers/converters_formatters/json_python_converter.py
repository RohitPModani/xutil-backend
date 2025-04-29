import json
import re
import logging
import tempfile
import ijson
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from typing import Dict, Any

from ...crud.converters_formatters.json_python_crud import json_to_python_logic
from ...schemas.converters_formatters.json_python_schema import (
    JSONInput,
    ConversionResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/json-python",
    tags=["JSON - Python"],
    responses={404: {"description": "Not found"}}
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for reading

@router.post(
    "/json-to-python",
    summary="Convert JSON to Python dataclass",
    description="Converts the provided JSON text into Python dataclass definitions. Supports nested objects, arrays, and primitive types (string, number, boolean, null).",
    response_description="Python dataclass definitions of the input JSON",
    response_model=ConversionResponse,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "result": (
                            "from typing import List, Any\n"
                            "from dataclasses import dataclass\n"
                            "import json\n\n"
                            "@dataclass\n"
                            "class Root:\n"
                            "    name: str\n"
                            "    age: int\n"
                            "    isActive: bool\n"
                            "    # ... rest of the class"
                        )
                    }
                }
            }
        },
        400: {
            "description": "Invalid input",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JSON format"}
                }
            }
        }
    }
)
async def json_to_python(input: JSONInput):
    logger.info(f"Processing JSON to Python dataclass with class name: {input.class_name}")
    try:
        return json_to_python_logic(input.json_data, input.class_name)
    except ValueError as e:
        logger.error(f"ValueError in JSON conversion: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in JSON conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post(
    "/json-to-python-file",
    summary="Convert JSON file to Python dataclass",
    description="Uploads a JSON file and converts its contents to Python dataclass definitions. Supports nested objects, arrays, and primitive types. Maximum file size is 10MB.",
    response_description="Python dataclass definitions of the input JSON file",
    response_model=ConversionResponse,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "result": (
                            "from typing import List, Any\n"
                            "from dataclasses import dataclass\n"
                            "import json\n\n"
                            "@dataclass\n"
                            "class Root:\n"
                            "    name: str\n"
                            "    age: int\n"
                            "    isActive: bool\n"
                            "    # ... rest of the class"
                        )
                    }
                }
            }
        },
        400: {
            "description": "Invalid input",
            "content": {
                "application/json": {
                    "example": {"detail": "Only .json files are supported"}
                }
            }
        }
    }
)
async def convert_json_to_python_file(file: UploadFile = File(...), class_name: str = Form(default="Root")):
    logger.info(f"Processing JSON file upload with class name: {class_name}")
    
    if not file.filename.lower().endswith(".json"):
        logger.error("Invalid file extension")
        raise HTTPException(status_code=400, detail="Only .json files are supported")
    if file.content_type != "application/json":
        logger.error("Invalid content type")
        raise HTTPException(status_code=400, detail="Invalid content type. Expected JSON")
    if not re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', class_name):
        logger.error("Invalid class name")
        raise HTTPException(status_code=400, detail="Invalid class name. Must be a valid Python identifier")

    try:
        # Use tempfile for safe temporary file management
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            size = 0
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    await file.close()
                    logger.error("File size exceeds limit")
                    raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
                temp_file.write(chunk)
            
            # Reset file position for parsing
            temp_file.seek(0)
            # Parse JSON incrementally with ijson
            json_data = next(ijson.items(temp_file, ""), None)
        
        # Clean up temporary file
        import os
        os.unlink(temp_file.name)
        
        if json_data is None:
            await file.close()
            logger.error("Invalid JSON format")
            raise HTTPException(status_code=400, detail="Invalid JSON format")

        result = json_to_python_logic(json.dumps(json_data), class_name)
        await file.close()
        return result
    
    except json.JSONDecodeError:
        await file.close()
        logger.error("Invalid JSON format")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError as e:
        await file.close()
        logger.error(f"ValueError in JSON file conversion: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await file.close()
        logger.error(f"Unexpected error in JSON file conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")