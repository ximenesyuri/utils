from inspect import signature, Signature, Parameter, getsource
from typed import typed, Function, List

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


