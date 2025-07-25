from typed import typed, Any, Str, Int, List, Tuple, Set
from utils.err import ToErr

class to:
    @typed
    def str(x: Any) -> Str:
        try:
           return str(x)
        except Exception as e:
            raise ToErr(e)

    @typed
    def int(x: Any) -> Int:
        try:
           return int(x)
        except Exception as e:
            raise ToErr(e)

    @typed
    def tuple(x: Any) -> Tuple(Any):
        try:
           return tuple(x)
        except Exception as e:
            raise ToErr(e)

    @typed
    def list(x: Any) -> List(Any):
        try:
           return list(x)
        except Exception as e:
            raise ToErr(e)

    @typed
    def set(x: Any) -> Set(Any):
        try:
           return set(x)
        except Exception as e:
            raise ToErr(e)
