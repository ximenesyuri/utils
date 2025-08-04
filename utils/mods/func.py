from inspect import signature, Signature, Parameter, getsource
from typed import typed, Function, List, Tuple, Str, Dict, Any
from utils.mods.helper import _get_globals

class func:
    @typed
    def signature(f: Function) -> Signature:
        return signature(f)
    sig = signature

    @typed
    def params(f: Function) -> Tuple(Parameter):
        return (param for param in signature(f).parameters.values())
    args = params

    @typed
    def code(f: Function) -> Str:
        return getsource(f)

    @typed
    def globals(f: Function) -> Dict(Any):
        return  _get_globals(f)
