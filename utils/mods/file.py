from utils.mods.types import Path
from utils.mods.path  import path
from utils.err import FileErr

class file:
    def read(file: Path='') -> str:
        try:
            if path.is_file(file):
                with open(file, 'r') as f:
                    return f.read()
        except Exception as e:
            raise FileErr(e)

    def write(file: Path='', content: str='') -> None:
        try:
            with open(file, 'w') as f:
                return f.write()
        except Exception as e:
            raise FileErr(e)

    def append(file: Path='', content: str='') -> None:
        try:
            if path.is_file(file):
                with open(file, 'a') as f:
                    return f.write()
        except Exception as e:
            raise FileErr(e)

    def lines(file: Path='') -> list:
        try:
            with open(file, 'r') as f:
                return f.readlines()
        except Exception as e:
            raise FileErr(e)

    def stripped_lines(file: Path='') -> list:
        try:
            with open(file, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            raise FileErr(e)
