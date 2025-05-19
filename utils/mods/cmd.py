import shutil
import filecmp
import tempfile
import os
import time
import subprocess
from pathlib import Path

class cmd:
    def run(cmd_string, cwd=None, envs=None, terminate=True, **kargs):
        cmd_list = cmd_string.split()
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

    def lsf(directory, ext=None):
        try:
            if ext:
                return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(ext)]
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def lsd(directory, exclude=None):
        try:
            if exclude is None:
                exclude = []
            return [
                d for d in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, d)) and d not in exclude
            ]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def rm(path):
        path_to_remove = Path(path)
        if path_to_remove.exists():
            if path_to_remove.is_dir():
                shutil.rmtree(path_to_remove)
            else:
                os.remove(path_to_remove)

    def mkd(path):
        path_to_create = Path(path)
        path_to_create.mkdir(parents=True, exist_ok=True)

    def mkf(path):
        path_to_create = Path(path)
        path_to_create.touch(exist_ok=True)

    def mktemp():
        return tempfile.mkdtemp()

    def cpf(src_dir, dest_dir, ext=None):
        src_dir = Path(src_dir)
        dest_dir = Path(dest_dir)
        if ext:
            if not ext.startswith('.'):
                ext = '.' + ext
            pattern = f'*{ext}'
        else:
            pattern = '*'

        for src_path in src_dir.rglob(pattern):
            if not src_path.is_file():
                continue
            rel_path = src_path.relative_to(src_dir)
            target_path = dest_dir / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, target_path)

    def cp(src, dest):
        src = Path(src)
        dest = Path(dest)
        if not src.exists():
            raise FileNotFoundError(f"Source not found: {src}")
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
                    raise NotADirectoryError(f"Destination is not a directory: {dest}")
            else:
                shutil.copytree(src, dest)
            return
        raise ValueError(f"Unsupported source type: {src}")

    def rsync(source, destination, delete=False):
        source_path = Path(source)
        destination_path = Path(destination)

        if not source_path.exists():
            raise FileExistsError(f"The source path {source_path} does not exist.")
            return

        if source_path.is_file():
            if delete:
                if destination_path.exists():
                    cmd.rm(destination_path)

            shutil.copy2(source, destination)

        def sync_dirs(src, dest):
            for src_dir, _, files in os.walk(src):
                dst_dir = src_dir.replace(str(src), str(dest), 1)
                Path(dst_dir).mkdir(parents=True, exist_ok=True)
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if not os.path.exists(dst_file) or not filecmp.cmp(src_file, dst_file, shallow=False):
                        shutil.copy2(src_file, dst_file)

        if os.path.isdir(source):
            destination_path.mkdir(parents=True, exist_ok=True)
            sync_files(source_path, destination_path)

            if delete:
                for dest_dir, _, files in os.walk(destination_path):
                    src_dir = dest_dir.replace(str(destination_path), str(source_path), 1)
                    if not os.path.exists(src_dir):
                        shutil.rmtree(dest_dir)
                    else:
                        for file_ in files:
                            dst_file = os.path.join(dest_dir, file_)
                            src_file = os.path.join(src_dir, file_)
                            if not os.path.exists(src_file):
                                os.remove(dst_file)
    def sleep(seconds):
        return time.sleep(seconds)
