import json
from io import StringIO
from ...schemas.converters.json_typescript_schema import ConversionResponse

def json_to_typescript_logic(json_data, interface_name="Data", max_depth=50):
    if max_depth <= 0:
        raise ValueError("Maximum recursion depth exceeded")

    # Precompute indentation strings
    INDENT_CACHE = {i: "  " * i for i in range(10)}  # Cache up to 10 levels

    # Track visited objects and collect interfaces
    visited = set()
    interfaces = []

    def get_type(value) -> str:
        if isinstance(value, str):
            return "string"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, list):
            if not value:
                return "unknown[]"
            if isinstance(value[0], dict):
                array_interface_name = f"{interface_name}Item"
                array_interface = generate_interface(value[0], array_interface_name, max_depth - 1)
                interfaces.append(array_interface)
                return f"{array_interface_name}[]"
            return f"{get_type(value[0])}[]"
        elif isinstance(value, dict):
            value_id = id(value)
            if value_id in visited:
                return "any"
            visited.add(value_id)
            nested_interface_name = f"{interface_name}Nested"
            nested_interface = generate_interface(value, nested_interface_name, max_depth - 1)
            interfaces.append(nested_interface)
            return nested_interface_name
        elif value is None:
            return "null"
        return "any"

    def generate_interface(data: dict, name: str, depth: int, indent: int = 0) -> str:
        if depth <= 0:
            return ""
        output = StringIO()
        indent_str = INDENT_CACHE.get(indent, "  " * indent)
        output.write(f"{indent_str}interface {name} {{\n")
        
        for key, value in data.items():
            ts_type = get_type(value)
            output.write(f"{indent_str}  {key}: {ts_type};\n")
        
        output.write(f"{indent_str}}}\n")
        result = output.getvalue()
        output.close()
        return result

    # Validate and parse input
    if not isinstance(json_data, (str, dict)):
        raise ValueError("Input must be a JSON string or dictionary")
    try:
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON string")

    # Generate main interface
    main_interface = generate_interface(data, interface_name, max_depth)
    interfaces.append(main_interface)

    # Combine interfaces efficiently
    result = "\n".join(filter(None, interfaces))
    return ConversionResponse(result=result)