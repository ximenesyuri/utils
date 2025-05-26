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
from pathlib import Path
from utils.err import JsonErr

Path = Path
Json = Union[Dict[str, Any], Set[Any], List[Any]]
