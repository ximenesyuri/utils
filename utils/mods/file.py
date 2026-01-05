from typed import typed, Str, Nill, List
from utils.mods.path import Path, File

class FileErr(Exception): pass

class file:
    @typed
    def read(filepath: File='') -> Str:
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            raise FileErr(e)

    @typed
    def write(filepath: Path='', content: Str='') -> Nill:
        try:
            with open(filepath, 'w') as f:
                f.write(content)
        except Exception as e:
            raise FileErr(e)

    @typed
    def append(filepath: File='', content: Str='') -> Nill:
        try:
            with open(filepath, 'a') as f:
                f.write(content)
        except Exception as e:
            raise FileErr(e)

    @typed
    def get_lines(filepath: File='') -> List(Str):
        try:
            with open(filepath, 'r') as f:
                return f.readlines()
        except Exception as e:
            raise FileErr(e)

    @typed
    def get_stripped_lines(filepath: File='') -> List(Str):
        try:
            with open(filepath, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            raise FileErr(e)
