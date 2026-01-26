from typed import model, Maybe, Str
from utils.mods.json_ import Json

@model
class _Result:
    message: Maybe(Str)=None
    data: Maybe(Json)=None

_Result.__display__ = "Result"
