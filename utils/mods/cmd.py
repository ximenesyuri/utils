import shutil
import filecmp
import tempfile
import os
import sys
import time
import subprocess
from pathlib import Path as Path_
from typed import (
    typed,
    Str,
    List,
    Bool,
    Path,
    Nill,
    Any,
    Dir,
    Env,
    Pos,
    Nat,
    Exists
)
from utils.err import CmdErr

class cmd:
    @typed
    def run(cmd_str: Str, cwd: Path='', envs: List(Env)=[], terminate: Bool=True, **kargs: Any) -> Nill:
        """
        Execute any system command as a subprocess by passing a command str and environment variables.
        """
        try:
            cmd_list = cmd_str.split()
            env = os.environ.copy()
            if envs:
                env.update(envs)
            if terminate:
                try:
                    process = subprocess.run(
                        cmd_list,
                        cwd=cwd,
                        capture_output=True,
                        text=True,
                        env=env,
                        check=True
                    )
                    return process.stderr, process.stdout
                except subprocess.CalledProcessError as e:
                    return e.stderr, e.stdout
            else:
                try:
                    process = subprocess.Popen(
                        cmd_list,
                        cwd=cwd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        env=env
                    )
                    for line in process.stdout:
                        print(line, end='')
                    return_code = process.wait()
                    return None, None
                except Exception as e:
                    print(f"Error in Popen: {e}", file=sys.stderr)
                    return str(e), None
        except Exception as e:
            raise CmdErr(e)

    @typed
    def sleep(seconds: Pos=1) -> Nill:
        try:
            return time.sleep(seconds)
        except Exception as e:
            raise CmdErr(e)

    @typed
    def exit(code: Nat=0) -> Nill:
        try:
            return sys.exit(code)
        except Exception as e:
            raise CmdErr(e)

    @typed
    def ls(dir: Dir='', exclude: List(Str)=[]) -> List(Path):
        try:
            return [
                d for d in os.listdir(dir)
                and d not in exclude
            ]
        except Exception as e:
            raise CmdErr(e)

    @typed
    def lsf(dir: Dir='', extension: Str='') -> List(Path):
        try:
            if extension:
                return [
                    f for f in os.listdir(dir)
                    if os.path.isfile(os.path.join(dir, f))
                    and f.endswith(extension)
                ]
            return [
                f for f in os.listdir(dir)
                if os.path.isfile(os.path.join(dir, f))
            ]
        except Exception as e:
            raise CmdErr(e)

    @typed
    def lsd(dir: Dir='', exclude: List(Str)=[]) -> List(Path):
        try:
            return [
                d for d in os.listdir(dir)
                if os.path.isdir(os.path.join(dir, d))
                and d not in exclude
            ]
        except Exception as e:
            raise CmdErr(e)

    @typed
    def rm(path: Path='') -> Nill:
        try:
            path_to_remove = Path_(path)
            if path_to_remove.exists():
                if path_to_remove.is_dir():
                    shutil.rmtree(path_to_remove)
                else:
                    os.remove(path_to_remove)
        except Exception as e:
            raise CmdErr(e)

    @typed
    def mkdir(path: Path="") -> Nill:
        try:
            path_to_create = Path_(path)
            path_to_create.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise CmdErr(e)
    mkd = mkdir

    @typed
    def clean(path: Path) -> Nill:
        try:
            path_to_clean = Path_(path)
            if path_to_clean.is_dir():
                cmd.rm(path)
            with open(path, 'w') as file:
                file.write('')
        except Exception as e:
            raise CmdErr(e)

    @typed
    def touch(path: Path="") -> Nill:
        try:
            path_to_create = Path_(path)
            path_to_create.touch(exist_ok=True)
        except Exception as e:
            raise CmdErr(e)
    mkf = touch

    class mktemp:
        @typed
        def dir() -> Path:
            try:
                temp_dir = tempfile.mkdtemp()
                cmd.mkdir(temp_dir)
                return temp_dir
            except Exception as e:
                raise CmdErr(e)

        @typed
        def file(prefix: Str='', extension: Str='') -> Path:
            try:
                temp_file = tempfile.mktemp(prefix=prefix, suffix=f'.{extension}')
                cmd.touch(temp_file)
                return temp_file
            except Exception as e:
                raise CmdErr(e)

    @typed
    def cpf(source: Dir="", target: Path="", extension: Str='') -> Nill:
        try:
            source = Path_(source)
            target = Path_(target)
            if extension:
                if not extension.startswith('.'):
                    ext = '.' + extension
                pattern = f'*{ext}'
            else:
                pattern = '*'

            for src_path in source.rglob(pattern):
                if not src_path.is_file():
                    continue
                rel_path = src_path.relative_to(source)
                target_path = target / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, target_path)
        except Exception as e:
            raise CmdErr(e)

    @typed
    def cp(source: Exists='', target: Path='') -> Nill:
        try:
            src = Path_(source)
            dest = Path_(target)
            if src.is_file():
                if dest.exists() and dest.is_dir():
                    target = dest / src.name
                else:
                    target = dest
                    target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
                return
            if src.is_dir():
                if dest.exists():
                    if dest.is_dir():
                        target = dest / src.name
                        shutil.copytree(src, target)
                    else:
                        raise NotADirectoryError(f"Destination is not a dir: {dest}")
                else:
                    shutil.copytree(src, dest)
                return
            raise ValueError(f"Unsupported source type: {src}")
        except Exception as e:
            raise CmdErr(e)

    @typed
    def rsync(source: Exists='', target: Path='', delete: Bool=False) -> Nill:
        source_path = Path_(source)
        destination_path = Path_(destination)

        if source_path.is_file():
            if delete:
                if destination_path.exists():
                    cmd.rm(destination_path)

            shutil.copy2(source, destination)

        def sync_dirs(src, dest):
            for source, _, files in os.walk(src):
                target = source.replace(str(src), str(dest), 1)
                Path_(target).mkdir(parents=True, exist_ok=True)
                for file_ in files:
                    src_file = os.path.join(source, file_)
                    dst_file = os.path.join(target, file_)
                    if not os.path.exists(dst_file) or not filecmp.cmp(src_file, dst_file, shallow=False):
                        shutil.copy2(src_file, dst_file)

        if os.path.isdir(source):
            destination_path.mkdir(parents=True, exist_ok=True)
            sync_dirs(source_path, destination_path)

            if delete:
                for target, _, files in os.walk(destination_path):
                    source = target.replace(str(destination_path), str(source_path), 1)
                    if not os.path.exists(source):
                        shutil.rmtree(target)
                    else:
                        for file_ in files:
                            dst_file = os.path.join(target, file_)
                            src_file = os.path.join(source, file_)
                            if not os.path.exists(src_file):
                                os.remove(dst_file)
