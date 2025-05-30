import os
from typed import typed, Tuple, Union, Bool, Str, Path
from utils.err import PathErr

class path:
    @typed
    def exists(*paths: Tuple(Path)) -> Bool:
        try:
            return all(os.path.exists(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def abs(*paths: Tuple(Path)) -> Union(Path, Tuple(Path)):
        if len(paths) == 1:
            return os.path.abspath(paths[0])
        return (os.path.abspath(path_) for path_ in paths)

    @typed
    def is_file(*paths: Tuple(Path)) -> Bool:
        try:
            return all(os.path.isfile(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def is_dir(*paths: Tuple(Path)) -> Bool:
        try:
            return all(os.path.isdir(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def is_abs(*paths: Tuple(Path)) -> Bool:
        try:
            return all(os.path.isabs(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def is_rel(*paths: Tuple(Path)) -> Bool:
        try:
            return not any(os.path.isabs(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def is_link(*paths: Tuple(Path)) -> Bool:
        try:
            return not any(os.path.islink(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def join(*paths: Tuple(Path)) -> Path:
        try:
            return os.path.join(*paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def basename(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        if len(paths) == 1:
            return os.path.basename(paths[0])
        else:
            return (os.path.basename(path_) for path_ in paths)

    @typed
    def dirname(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        if len(paths) == 1:
            return os.path.dirname(paths[0])
        else:
            return (os.path.dirname(path_) for path_ in paths)

    @typed
    def filename(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        if len(paths) == 1:
            return path.basename(paths[0]).split('.')[0]
        else:
            return (path.basename(path_).split('.')[0] for path_ in paths)

    @typed
    def extension(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        if len(paths) == 1:
            return path.basename(paths[0]).split('.')[1]
        else:
            return (path.basename(path_).split('.')[1] for path_ in paths)
    ext = extension
