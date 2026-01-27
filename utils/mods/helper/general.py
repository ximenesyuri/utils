from typed import typed, TYPE, model, Maybe, Str, Dict, Any, Bool
from typed.types import Callable
from utils.mods.json_ import Json

@model
class _Result:
    message: Maybe(Str)=None
    data:    Maybe(Json)=None
    success: Bool=True

_Result.__display__ = "Result"
_Result.__name__ = "Result"

@typed
def Message(message: Str="", handler: Maybe(Callable)=None, **kwargs: Dict(Str)) -> Any:
    if not kwargs:
        full_message = message
    else:
        full_message = message.rstrip(":") + ":"
        parts = [f"{k}={v!r}" for k, v in kwargs.items()]
        full_message += " " + ", ".join(parts)
        full_message += "."

    if handler is None:
        return full_message

    if isinstance(handler, type) and issubclass(handler, BaseException):
        raise handler(full_message)

    handler(full_message)
    return None

class RESULT(TYPE(_Result)):
    def __instancecheck__(cls, instance):
        return instance in _Result

    def __call__(
        cls,
        message:  Maybe(Str)=None,
        data:     Maybe(Json)=None,
        success:  Bool=True,
        **kwargs: Dict(Str)
    ):
        return _Result(
            message=Message(message=message, **kwargs) if message or kwargs else None,
            data=data,
            success=success
        )
