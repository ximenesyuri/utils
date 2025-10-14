from functools import wraps
from inspect import signature, Signature, Parameter, getsource
from typed import typed, TYPE, Function, Tuple, Str, Dict, convert
from utils.mods.helper.func import _get_globals, _copy_func, _eval_func, _find_in_stack
from utils.err import FuncErr

class func:
    Signature = convert(Signature, TYPE)
    Parameter = convert(Parameter, TYPE)
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
            return tuple(param for param in signature(f).parameters.values())
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

    def unwrap(f: Function) -> Function:
        seen = set()
        candidate = f
        possible_attrs = ['__wrapped__', '__func__', 'func', 'f', '__func', 'function']

        try:
            while True:
                if id(candidate) in seen:
                    break
                seen.add(id(candidate))
                for attr in possible_attrs:
                    if hasattr(candidate, attr):
                        candidate = getattr(candidate, attr)
                        break
                else:
                    break
            if isinstance(candidate, Function):
                return candidate
            found = _find_in_stack(candidate)
            if isinstance(found, Function):
                return found
            raise FuncErr("Could not unwrap to a function object.")
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
