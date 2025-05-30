from typed import typed, Path, Str, Nill, List
from utils.mods.path  import path
from utils.err import FileErr

class file:
    @typed
    def read(file: Path='') -> Str:
        try:
            if path.is_file(file):
                with open(file, 'r') as f:
                    return f.read()
        except Exception as e:
            raise FileErr(e)

    @typed
    def write(file: Path='', content: Str='') -> Nill:
        try:
            with open(file, 'w') as f:
                return f.write()
        except Exception as e:
            raise FileErr(e)

    @typed
    def append(file: Path='', content: Str='') -> Nill:
        try:
            if path.is_file(file):
                with open(file, 'a') as f:
                    return f.write()
        except Exception as e:
            raise FileErr(e)

    @typed
    def lines(file: Path='') -> List(Str):
        try:
            with open(file, 'r') as f:
                return f.readlines()
        except Exception as e:
            raise FileErr(e)

    @typed
    def stripped_lines(file: Path='') -> List(Str):
        try:
            with open(file, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            raise FileErr(e)
