import os
import sys
import inspect
from typed import Bool, Path, Union, Tuple, Int, Str, typed, Nill
from utils.err import PathErr

class path:
    @typed
    def cwd(*paths: Tuple(Path)) -> Path:
        try:
            if len(paths) == 0:
                return os.getcwd()
            return path.join(os.getcwd(), *paths)
        except Exception as e:
            raise PathErr(e)
    pwd = cwd

    @typed
    def here(*paths: Tuple(Path)) -> Path:
        try:
            caller_frame = inspect.stack()[2]
            caller_filepath = caller_frame.filename
            here_ = os.path.dirname(os.path.abspath(caller_filepath))
            if len(paths) == 0:
                return here_
            return path.join(here_, *paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def exists(*paths: Tuple(Path)) -> Bool:
        try:
            return all(os.path.exists(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def abs(*paths: Tuple(Path)) -> Union(Path, Tuple(Path)):
        try:
            if len(paths) == 1:
                return os.path.abspath(paths[0])
            return (os.path.abspath(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def insert(*paths: Tuple(Path)) -> Nill:
        try:
            for p in paths:
                sys.path.insert(0, path.abs(p))
        except Exception as e:
            raise PathErr(e)

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
        try:
            if len(paths) == 1:
                return os.path.basename(paths[0])
            else:
                return (os.path.basename(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def dirname(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        try:
            if len(paths) == 1:
                return os.path.dirname(paths[0])
            else:
                return (os.path.dirname(path_) for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def filename(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        try:
            if len(paths) == 1:
                return path.basename(paths[0]).split('.')[0]
            else:
                return (path.basename(path_).split('.')[0] for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    @typed
    def extension(*paths: Tuple(Path)) -> Union(Str, Tuple(Str)):
        try:
            if len(paths) == 1:
                return path.basename(paths[0]).split('.')[1]
            else:
                return (path.basename(path_).split('.')[1] for path_ in paths)
        except Exception as e:
            raise PathErr(e)
    ext = extension

    @typed
    def parent(path: Path="", level: Int=1) -> Path:
        parts = path.split('/')
        if len(parts) < level:
            level = len(parts)
        last_part = -level
        if not parts[0:last_part] or parts[0:last_part] == ['']:
            return '/'
        return '/'.join(parts[0:last_part])
