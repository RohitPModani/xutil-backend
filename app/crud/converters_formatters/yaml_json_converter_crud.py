import yaml
import json
import datetime
from fastapi import HTTPException
from ...schemas.converters_formatters.yaml_json_converter_schema import ConversionResponse

def register_fallback_tag_constructor():
    """
    Registers a fallback constructor to ignore unknown YAML tags like !secret, !vault, etc.
    Treats them as normal string values.
    """
    def fallback_constructor(loader, tag_suffix, node):
        return loader.construct_scalar(node)
    yaml.SafeLoader.add_multi_constructor("!", fallback_constructor)

# Register once when this module is imported
register_fallback_tag_constructor()


# --- Utility to handle datetime ---

def convert_datetime(obj):
    """
    Recursively convert datetime or date objects into ISO formatted strings.
    """
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime(i) for i in obj]
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    else:
        return obj

def yaml_to_json_logic(yaml_text: str) -> ConversionResponse:
    """
    Convert a YAML string to JSON, handling datetime fields properly.
    """
    try:
        yaml_data = yaml.safe_load(yaml_text)
        if yaml_data is None:
            raise HTTPException(status_code=400, detail="Invalid YAML: Empty or invalid content")
        
        processed_data = convert_datetime(yaml_data)
        json_data = json.dumps(processed_data, indent=2, ensure_ascii=False)
        return ConversionResponse(result=json_data)
    
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Error parsing YAML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting YAML to JSON: {str(e)}")


def json_to_yaml_logic(json_text: str) -> ConversionResponse:
    """
    Convert a JSON string to YAML.
    """
    try:
        json_data = json.loads(json_text)
        
        yaml_data = yaml.dump(
            json_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
        )
        return ConversionResponse(result=yaml_data)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Error parsing JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting JSON to YAML: {str(e)}")


def yaml_json_file_logic(file_content: bytes) -> ConversionResponse:
    """
    Convert the content of a YAML file to JSON, handling datetime fields properly.
    """
    try:
        yaml_text = file_content.decode('utf-8')
        yaml_data = yaml.safe_load(yaml_text)
        if yaml_data is None:
            raise HTTPException(status_code=400, detail="Invalid YAML: Empty or invalid content")
        
        processed_data = convert_datetime(yaml_data)
        json_data = json.dumps(processed_data, indent=2, ensure_ascii=False)
        return ConversionResponse(result=json_data)
    
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Error parsing YAML: {str(e)}")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding must be UTF-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting YAML file to JSON: {str(e)}")


def json_yaml_file_logic(file_content: bytes) -> ConversionResponse:
    """
    Convert the content of a JSON file to YAML.
    """
    try:
        json_text = file_content.decode('utf-8')
        json_data = json.loads(json_text)
        
        yaml_data = yaml.dump(
            json_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
        )
        return ConversionResponse(result=yaml_data)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Error parsing JSON: {str(e)}")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding must be UTF-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting JSON file to YAML: {str(e)}")