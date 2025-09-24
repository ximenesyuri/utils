from functools import wraps
from inspect import signature, Signature, Parameter, getsource
from typed import typed, TYPE, Function, List, Tuple, Str, Dict, Callable, convert
from utils.mods.helper.func import _get_globals, _copy_func, _eval_func
from utils.err import FuncErr

class func:
    Signature = convert(Signature, TYPE)
    Parameter = convert(Signature, TYPE)
    @typed
    def signature(f: Function) -> Signature:
        try:
            return signature(f)
        except Exception as e:
            raise FuncErr(e)
    sig = signature

    @typed
    def params(f: Function) -> Tuple(Parameter):
        try:
            return (param for param in signature(f).parameters.values())
        except Exception as e:
            raise FuncErr(e)
    args = params

    @typed
    def code(f: Function) -> Str:
        try:
            return getsource(f)
        except Exception as e:
            raise FuncErr(e)

    @typed
    def globals(f: Function) -> Dict:
        try:
            return  _get_globals(f)
        except Exception as e:
            raise FuncErr(e)

    @typed
    def wrap(f: Function) -> Function:
        try:
            return wraps(f)
        except Exception as e:
            raise FuncErr(e)

    @typed
    def unwrap(f: Function) -> Function:
        try:
            while hasattr(f, '__wrapped__'):
                f = f.__wrapped__
            return f
        except Exception as e:
            raise FuncErr(e)

    @typed
    def copy(f: Function, **renamed_vars: Dict(Str)) -> Function:
        try:
            return _copy_func(f, **renamed_vars)
        except Exception as e:
            raise FuncErr(e)

    @typed
    def eval(f: Function, **fixed_vars: Dict) -> Function:
        try:
            return _eval_func(f, **fixed_vars)
        except Exception as e:
            raise FuncErr(e)
