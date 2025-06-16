from typed import *
from utils.err import ListErr

class list:
    @typed
    def append(x: Any, X: List(Any)) -> List(Any):
        try:
            return X.append(x)
        except Exception as e:
            raise ListErr(e)
