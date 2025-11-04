import os
from typed import typed, Path

class sys:
    @typed
    def venv() -> Path:
        try:
            return os.getenv("VIRTUAL_ENV")
        except Exception as e:
            raise SysErr(e)
