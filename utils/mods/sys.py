import os
from typed import typed
from utils.mods.path import Path
from utils.err import SysErr

class sys:
    @typed
    def venv() -> Path:
        try:
            return os.getenv("VIRTUAL_ENV")
        except Exception as e:
            raise SysErr(e)
