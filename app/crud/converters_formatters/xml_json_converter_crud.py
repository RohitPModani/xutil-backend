from xml.etree.ElementTree import ParseError
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse
import xmltodict
import json
from ...schemas.converters_formatters.xml_json_converter_schema import ConversionResponse

def xml_json_logic(xml_text: str) -> str:
    try:
        xml_dict = xmltodict.parse(xml_text)
        json_text = json.dumps(xml_dict, indent=2)
        return json_text
    except ParseError:
        raise HTTPException(status_code=400, detail="Invalid XML format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

def json_xml_logic(json_text: str) -> str:
    try:
        json_dict = json.loads(json_text)
        xml_text = xmltodict.unparse(json_dict, pretty=True)
        return xml_text
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
    
def xml_json_file_logic(contents: bytes) -> ConversionResponse:
    try:
        # Decode bytes to string
        xml_data = contents.decode("utf-8")

        # Parse XML to dictionary
        parsed_dict = xmltodict.parse(xml_data)

        # Convert to JSON with indentation
        json_data = json.dumps(parsed_dict, indent=4)

        return ConversionResponse(result = json_data)

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    except xmltodict.ParsingInterrupted:
        raise HTTPException(status_code=400, detail="Invalid XML format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    
def json_xml_file_logic(contents: bytes) -> ConversionResponse:
    try:
        # Decode bytes to string
        json_data = contents.decode("utf-8")

        # Parse JSON to dictionary
        parsed_dict = json.loads(json_data)

        # Convert to XML with pretty printing
        xml_data = xmltodict.unparse(parsed_dict, pretty=True)

        return ConversionResponse(result = xml_data)

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")