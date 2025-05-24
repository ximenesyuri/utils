from typing import Tuple, Union
import os

class path:
    def exists(*paths: Tuple[str]) -> bool:
        return all(os.path.exists(path_) for path_ in paths)

    def is_file(*paths: Tuple[str]) -> bool:
        return all(os.path.isfile(path_) for path_ in paths)

    def is_dir(*paths: Tuple[str]) -> bool:
        return all(os.path.isdir(path_) for path_ in paths)

    def is_abs(*paths: Tuple[str]) -> bool:
        return all(os.path.isabs(path_) for path_ in paths)

    def is_rel(*paths: Tuple[str]) -> bool:
        return not any(os.path.isabs(path_) for path_ in paths)

    def is_link(*paths: Tuple[str]) -> bool:
        return not any(os.path.islink(path_) for path_ in paths)

    def join(*paths: Tuple[str]) -> Union[str, Tuple[str]]:
        return os.path.join(*paths)

    def basename(*paths: Tuple[str]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return os.path.basename(paths[0])
        else:
            return (os.path.basename(path_) for path_ in paths)

    def dirname(*paths: Tuple[str]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return os.path.dirname(paths[0])
        else:
            return (os.path.dirname(path_) for path_ in paths)

    def filename(*paths: Tuple[str]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return path.basename(paths[0]).split('.')[0]
        else:
            return (path.basename(path_).split('.')[0] for path_ in paths)

    def extension(*paths: Tuple[str]) -> Union[str, Tuple[str]]:
        if len(paths) == 1:
            return path.basename(paths[0]).split('.')[1]
        else:
            return (path.basename(path_).split('.')[1] for path_ in paths)

