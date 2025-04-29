import pandas as pd
import json
from typing import Any, Dict, List, Union
from io import StringIO, BytesIO
from ...schemas.converters_formatters.csv_json_schema import ConversionResponse

def flatten_json(data: Union[Dict, List], parent_key: str = '', sep: str = '_') -> List[Dict[str, Any]]:
    """
    Generic JSON flattener: supports nested dicts and lists.
    Expands lists properly into multiple records (rows).
    """
    if isinstance(data, dict):
        records = [{}]
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            sub_records = flatten_json(v, new_key, sep)
            new_records = []
            for record in records:
                for sub in sub_records:
                    combined = {**record, **sub}
                    new_records.append(combined)
            records = new_records
        return records

    elif isinstance(data, list):
        records = []
        for item in data:
            sub_records = flatten_json(item, parent_key, sep)
            records.extend(sub_records)
        return records

    else:
        return [{parent_key: data}]


def json_to_csv_logic(json_data: str, separator: str = '_') -> ConversionResponse:
    """Convert ANY nested JSON string into flat CSV."""
    try:
        if not json_data.strip():
            raise ValueError("JSON data cannot be empty")

        data = json.loads(json_data)
        if isinstance(data, dict):
            data = [data]  # Make it list-like always

        all_records = []
        for record in data:
            flattened = flatten_json(record, sep=separator)
            all_records.extend(flattened)

        df = pd.DataFrame(all_records)
        with StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=False, encoding="utf-8")
            return ConversionResponse(result=csv_buffer.getvalue())

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise ValueError(f"JSON to CSV conversion failed: {str(e)}")


def csv_to_json_logic(file_content: bytes, separator: str = '_') -> ConversionResponse:
    """Convert CSV file to nested JSON string."""
    try:
        df = pd.read_csv(BytesIO(file_content), encoding="utf-8", encoding_errors="ignore")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        nested_records = [unflatten_dict(r, sep=separator) for r in records]
        return ConversionResponse(result=json.dumps(nested_records, indent=2, ensure_ascii=False))
    except Exception as e:
        raise ValueError(f"CSV to JSON conversion failed: {str(e)}")


def unflatten_dict(d: Dict[str, Any], sep: str = '_') -> Dict[str, Any]:
    """Unflatten dictionary keys with separator into nested dictionaries."""
    result: Dict[str, Any] = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value
    return result
