from dataclasses import dataclass
from typing import Callable, Dict, Type

@dataclass
class FunctionParams:
    name: str                         # Function name
    doc: str                          # Docstring
    param_types: Dict[str, Type]      # Map of param name to type
    return_type: Type                 # Return type
    callback: Callable[..., str]      # Function that receives named args and returns str
