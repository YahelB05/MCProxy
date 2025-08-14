from typing import Dict


def map_str_to_type(type_str: str) -> type:
    mapping = {
        "string": str,
        "boolean": bool,
        "integer": int,
        "float": float
    }
    return mapping.get(type_str, str)  # default to str if unknown


def extract_param_types(endpoint) -> Dict[str, type]:
    param_types = {}

    for param in (endpoint.path_params or []):
        param_types[param.field] = map_str_to_type(param.type)

    for param in (endpoint.query_params or []):
        param_types[param.field] = map_str_to_type(param.type)

    return param_types
