import re
from typing import (
    Tuple,
    List,
    Dict,
    Set,
    FrozenSet,
    Type,
    Any,
    Optional,
    Union
)
from pydantic import BaseModel as Model
from pathlib import Path

JsonData = Union[Dict[str, Any], Set[Any], List[Any]]

class Json:
    def __init__(self, json_data: JsonData):
        if not isinstance(json_data, (dict, set, list)):
            raise TypeError("Data must be a dictionary, set, or list")
        self._json_data = json_data
