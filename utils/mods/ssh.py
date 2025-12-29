import os
import stat
import shlex
from typed import typed, TYPE, Str, Bool, Tuple, List, Nill, Union, Maybe
from utils.err import SSHErr
from utils.mods.path import Path, File, Exists
from utils.mods.file import file
from utils.mods.cmd  import cmd as _cmd
from utils.mods.helper.ssh import _is_ssh_key

class SSH_KEY(TYPE(Str)):
    def __call__(cls, *types, private=False):
        type_tuple = tuple(str(t) for t in types)

        if type_tuple:
            types_str = ", ".join(type_tuple)
            class_name = f"SSHKey({types_str}, private={private})"
        else:
            class_name = f"SSHKey(private={private})"

        namespace = {
            "__display__": class_name,
            "__null__": "",
            "_ssh_types": type_tuple,
            "_ssh_private": private,
        }

        return SSH_KEY(class_name, (Str,), namespace)

    def __instancecheck__(cls, instance):
        if not instance in Str:
            return False

        private = getattr(cls, "_ssh_private", None)
        types_ = getattr(cls, "_ssh_types", ())

        if private is None:
            return (
                instance in SSHKey(private=True) or
                instance in SSHKey(private=False)
            )

        if types_:
            return any(
                _is_ssh_key(key_string=instance, key_type=t, private=private)
                for t in types_
            )
        return _is_ssh_key(key_string=instance, key_type=None, private=private)

SSHKey = SSH_KEY('SSHKey', (Str,), {
        "__display__": 'SSHKey',
        "__null__": "",
        "_ssh_types": (),
        "_ssh_private": None
    })

class ssh:
    class key:
        @typed
        def prepare(key: Union(Path, SSHKey(private=True))) -> Tuple:
            try:
                if key in Path:
                    return key, False

                tmp_file = _cmd.mktemp.file()
                file.write(tmp_file, key)
                _cmd.chmod(tmp_file, stat.S_IRUSR | stat.S_IWUSR)
                return tmp_file, True
            except Exception as e:
                raise SSHErr(e)

        @typed
        def add(key: Union(Path, SSHKey(private=True))) -> Nill:
            try:
                if "SSH_AUTH_SOCK" not in os.environ:
                    stderr, stdout = _cmd.run("ssh-agent -s")
                    out = stdout or ""
                    for line in out.splitlines():
                        if "SSH_AUTH_SOCK" in line or "SSH_AGENT_PID" in line:
                            k, v = line.split(";", 3)[0].split("=", 1)
                            os.environ[k] = v

                key_path, temp_key = ssh.key.prepare(key)

                stderr, stdout = _cmd.run(f"ssh-add {key_path}")
                if stderr:
                    raise SSHErr(stderr)

                if temp_key:
                    _cmd.rm(key_path)
                return
            except Exception as e:
                raise SSHErr(e)

    @typed
    def exec(host: Str, user: Str, key: Str, cmd: Union(Str, Tuple(Str), List(Str), File), cwd: Maybe(Str)=None) -> Tuple:
        try:
            key_path, temp_key = ssh.key.prepare(key)
            try:
                if not cmd in Union(List, Tuple):
                    if cmd in File:
                        remote_cmd = file.read(cmd)
                    else:
                        remote_cmd = str(cmd)
                else:
                    remote_cmd = " ".join(shlex.quote(str(p)) for p in cmd)

                if cwd:
                    if "\n" in remote_cmd:
                        remote_cmd = (
                            f"cd {shlex.quote(str(cwd))} && (\n{remote_cmd}\n)"
                        )
                    else:
                        remote_cmd = f"cd {shlex.quote(str(cwd))} && {remote_cmd}"

                ssh_cmd = [
                    "ssh",
                    "-i", str(key_path),
                    "-o", "StrictHostKeyChecking=no",
                    f"{user}@{host}",
                    remote_cmd,
                ]

                stderr, stdout = _cmd.run(ssh_cmd)

                if stderr:
                    raise SSHErr(stderr)

                return stdout, stderr
            finally:
                if temp_key and key_path and os.path.exists(key_path):
                    _cmd.rm(key_path)
        except Exception as e:
            if isinstance(e, SSHErr):
                raise
            raise SSHErr(str(e))

    @typed
    def rsync(host: Str, user: Str, key: Str, source: Exists, target: Path, delete: Bool=False, pull: Bool=False) -> Nill:
        try:
            if not _cmd.exists("rsync"):
                raise SSHErr("rsync command not found in PATH")

            key_path, temp_key = ssh.key.prepare(key)
            try:
                rsync_cmd = ["rsync", "-az"]
                if delete:
                    rsync_cmd.append("--delete")

                ssh_part = [
                    "ssh",
                    "-i", str(key_path),
                    "-o", "StrictHostKeyChecking=no",
                ]
                rsync_cmd += ["-e", " ".join(shlex.quote(p) for p in ssh_part)]

                if pull:
                    src = f"{user}@{host}:{source}"
                    dst = str(target)
                else:
                    src = str(source)
                    dst = f"{user}@{host}:{target}"

                rsync_cmd += [src, dst]

                stderr, stdout = _cmd.run(rsync_cmd)

                if stderr:
                    raise SSHErr(stderr)

                return
            finally:
                if temp_key and key_path and os.path.exists(key_path):
                    _cmd.rm(key_path)
        except Exception as e:
            if isinstance(e, SSHErr):
                raise
            raise SSHErr(str(e))

ssh.rsync(
    host='201.54.9.220',
    user='ubuntu',
    key='/home/yx/.ssh/vortice/id_ed25519',
    source='/home/yx/aaa',
    target='/home/ubuntu/test'
)
