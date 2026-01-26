import importlib
import sys
from typing import TYPE_CHECKING as __lsp__
from utils.mods.helper.general import Message, RESULT, _Result

def lazy(imports):
    caller_globals = sys._getframe(1).f_globals
    caller_name = caller_globals.get("__name__", "<unknown>")

    all_names = list(imports.keys())
    caller_globals["__all__"] = all_names

    lazy_map = {}
    for name, module_path in imports.items():
        if name == "dt" and "datetime" in imports and imports["datetime"] == module_path:
            lazy_map[name] = (imports["datetime"], "datetime")
        else:
            lazy_map[name] = (module_path, name)

    caller_globals["__lazy__"] = lazy_map

    def __getattr__(name):
        try:
            module_name, attr_name = caller_globals["__lazy__"][name]
        except KeyError:
            raise AttributeError(
                f"module {caller_name!r} has no attribute {name!r}"
            ) from None

        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name)
        caller_globals[name] = attr
        return attr

    def __dir__():
        return sorted(set(caller_globals.keys()) | set(caller_globals["__all__"]))

    caller_globals["__getattr__"] = __getattr__
    caller_globals["__dir__"] = __dir__

    return __lsp__

Result = RESULT("Result", (_Result,), {"__display__": "Result"})
