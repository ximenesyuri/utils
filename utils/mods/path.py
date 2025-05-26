import os
from utils.mods.types import Path, Tuple, Union
from utils.err import PathErr

class path:
    def exists(*paths: Tuple[Path]) -> bool:
        try:
            return all(Path(path_).exists() for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    def abs(*paths: Tuple[Path]) -> Tuple[Path]:
        return (Path(path_).absolute() for path_ in paths)

    def is_file(*paths: Tuple[Path]) -> bool:
        try:
            return all(Path(path_).is_file() for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    def is_dir(*paths: Tuple[Path]) -> bool:
        try:
            return all(Path(path_).is_dir() for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    def is_abs(*paths: Tuple[Path]) -> bool:
        try:
            return all(Path(path_).is_absolute() for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    def is_rel(*paths: Tuple[Path]) -> bool:
        try:
            return not any(Path(path_).is_absolute() for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    def is_link(*paths: Tuple[Path]) -> bool:
        try:
            return not any(Path(path_).is_symlink() for path_ in paths)
        except Exception as e:
            raise PathErr(e)

    def join(*paths: Tuple[Path]) -> Path:
        try:
            return Path(*paths)
        except Exception as e:
            raise PathErr(e)

    def basename(*paths: Tuple[Path]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return os.path.basename(Path(paths[0]))
        else:
            return (os.path.basename(Path(path_)) for path_ in paths)

    def dirname(*paths: Tuple[Path]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return os.path.dirname(Path(paths[0]))
        else:
            return (os.path.dirname(Path(path_)) for path_ in paths)

    def filename(*paths: Tuple[Path]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return path.basename(Path(paths[0])).split('.')[0]
        else:
            return (path.basename(Path(path_)).split('.')[0] for path_ in paths)

    def extension(*paths: Tuple[Path]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return path.basename(Path(paths[0])).split('.')[1]
        else:
            return (path.basename(Path(path_)).split('.')[1] for path_ in paths)
    ext = extension
