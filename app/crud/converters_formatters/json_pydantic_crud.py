import json
from typing import Any, Dict, List, Tuple
from ...schemas.converters_formatters.json_python_schema import ConversionResponse

def infer_type(value: Any) -> str:
    """Infer Python type from JSON value for Pydantic models."""
    if value is None:
        return "Any"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, str):
        return "str"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, list):
        if not value:
            return "List[Any]"
        # Check all elements for mixed types
        types = {infer_type(item) for item in value if item is not None}
        if len(types) > 1 or None in value:
            return "List[Any]"
        if value and isinstance(value[0], dict):
            return f"List[{value[0].get('_class_name', 'Any')}]"
        return f"List[{infer_type(value[0])}]"
    elif isinstance(value, dict):
        return value.get('_class_name', 'Any')
    return "Any"

def singularize(key: str) -> str:
    """Convert plural key to singular form."""
    if key.endswith('ches'):  # Handle 'branches' → 'branch'
        return key[:-2]
    elif key.endswith('s'):
        return key[:-1]
    return key

def to_camel_case(name: str) -> str:
    """Convert underscore-separated name to camelCase (PascalCase for classes)."""
    return ''.join(word.capitalize() for word in name.split('_'))

def generate_class_definitions(json_data: Dict, class_name: str = "Root", depth: int = 0, max_depth: int = 50, path: str = "") -> Tuple[str, List[str]]:
    """Generate Pydantic class definitions from JSON data, with nesting depth limit and camelCase class names."""
    if depth > max_depth:
        raise ValueError("Maximum nesting depth of 50 levels exceeded")
    
    classes = []
    imports = ["from pydantic import BaseModel", "from typing import List, Any"]
    
    def process_dict(data: Dict, name: str, current_path: str) -> str:
        fields = []
        for key, value in data.items():
            if key == "_class_name":  # Skip internal metadata
                continue
            new_path = f"{current_path}_{key}" if current_path else key
            if isinstance(value, dict):
                nested_class_name = to_camel_case(new_path)
                value['_class_name'] = nested_class_name
                nested_class, nested_imports = generate_class_definitions(value, nested_class_name, depth + 1, max_depth, new_path)
                classes.append(nested_class)
                fields.append((key, nested_class_name))
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                nested_class_name = to_camel_case(singularize(new_path))
                value[0]['_class_name'] = nested_class_name
                nested_class, nested_imports = generate_class_definitions(value[0], nested_class_name, depth + 1, max_depth, new_path)
                classes.append(nested_class)
                fields.append((key, f"List[{nested_class_name}]"))
            else:
                field_type = infer_type(value)
                # Handle fields that may have null values across list items
                if isinstance(value, list) and any(isinstance(item, dict) and item.get('_class_name') for item in value):
                    field_type = f"List[{value[0].get('_class_name', 'Any')}]"
                elif key in data and data[key] is None:
                    field_type = "Any"
                fields.append((key, field_type))

        # Generate class definition
        class_def = [f"class {name}(BaseModel):"]
        for field_name, field_type in fields:
            class_def.append(f"    {field_name}: {field_type}")
        if not fields:  # Handle empty objects
            class_def.append("    pass")
        
        return "\n".join(class_def)

    class_def = process_dict(json_data, class_name, path)
    classes.append(class_def)
    return "\n\n".join(reversed(classes)), imports

def json_to_pydantic_logic(json_data: str, class_name: str = "Root") -> ConversionResponse:
    """Convert JSON string to Pydantic class definitions."""
    try:
        parsed_data = json.loads(json_data)
        if not parsed_data:
            raise ValueError("Empty JSON data")
        class_definitions, imports = generate_class_definitions(parsed_data, class_name)
        output = "\n".join(imports) + "\n\n" + class_definitions
        return ConversionResponse(result=output)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")