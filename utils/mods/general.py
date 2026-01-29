import importlib
import sys
import functools
from typing import TYPE_CHECKING as __lsp__
from typed import typed, model, Dict, Union, Maybe, Str, Bool, Bytes, Int, name, Any
from utils.mods.json_ import Json
from utils.mods.helper.general import Message
from utils.mods.helper.types import Client
from utils.mods.func import func

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

ResultData = Union(Json, Str, Int, Bytes)

@model
class Result:
    message: Maybe(Str)=None
    data:    Maybe(ResultData)=None
    success: Bool=True

Result.__display__ = "Result"

class result:
    @typed
    def success(message: Maybe(Str)=None, data: Maybe(ResultData)=None, **kwargs: Dict(Str)) -> Result:
        return Result(
            message=Message(message=message, **kwargs) if message or kwargs else None,
            data=data,
            success=True
        )

    @typed
    def failure(message: Maybe(Str)=None, data: Maybe(ResultData)=None, **kwargs: Dict(Str)) -> Result:
        return Result(
            message=Message(message=message, **kwargs) if message or kwargs else None,
            data=data,
            success=False
        )

    @typed
    def data(action: Any, propagate: Bool=True, **kwargs: Dict(Str)):
        res = action(**kwargs)
        if propagate:
            globals()['propagate'].failure(res)
        return res.data

class _Propagate(Exception):
    def __init__(self, result):
        self.result = result

class propagate:
    @typed
    def failure(res: Result) -> Result:
        if not res.success:
            raise _Propagate(res)
        return res

    @typed
    def success(res: Result) -> Result:
        if res.success:
            raise _Propagate(res)
        return res


def Action(Error=None, message=None):
    if Error is None:
        typed_ = typed
    if isinstance(Error, type) and issubclass(Error, BaseException):
        if message:
            typed_ = func.eval(typed, enclose=Error, message=message)
        else:
            typed_ = func.eval(typed, enclose=Error)
    elif Error in Str:
        if message:
            typed_ = func.eval(typed, enclose=type(Error, (Exception,), {}), message=message)
        else:
            typed_ = func.eval(typed, enclose=type(Error, (Exception,), {}))
    else:
        raise TypeError("Error must be an exception class or a string")

    def decorator(func=None, **kwargs):
        def apply(f):
            typed_func = typed_(f, **kwargs)
            cod = getattr(typed_func, "cod", None)
            if cod is not Result and not (isinstance(cod, type) and issubclass(cod, Client)):
                raise TypeError(
                    f"Codomain mismatch in function '{name(f)}':\n"
                    "    [expected_type] 'Result'\n"
                    f"    [received_type] '{name(cod)}'"
                )
            if cod is Result:
                @functools.wraps(f)
                def wrapper(*args, **kw):
                    try:
                        return typed_func(*args, **kw)
                    except _Propagate as exc:
                        return exc.result

                wrapper.cod = cod
                if hasattr(typed_func, "dom"):
                    wrapper.dom = typed_func.dom
                return wrapper
            return typed_func
        if func is None:
            return apply
        else:
            return apply(func)

    decorator.success = result.success
    decorator.failure = result.failure
    decorator.data = result.data
    decorator.propagate = propagate

    return decorator
