import os
import stat
from typed import typed, TYPE, Str, Nill, Union, Tuple
from utils.err import SSHErr
from utils.mods.path import Path, File
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
                from utils import cmd, file

                if key in Path:
                    return key, False

                tmp_file = cmd.mktemp.file()
                file.write(tmp_file, key)
                cmd.chmod(tmp_file, stat.S_IRUSR | stat.S_IWUSR)
                return tmp_file, True
            except Exception as e:
                raise SSHErr(e)

        @typed
        def add(key: Union(Path, SSHKey(private=True))) -> Nill:
            try:
                from utils import cmd

                if "SSH_AUTH_SOCK" not in os.environ:
                    stderr, stdout = cmd.run("ssh-agent -s")
                    out = stdout or ""
                    for line in out.splitlines():
                        if "SSH_AUTH_SOCK" in line or "SSH_AGENT_PID" in line:
                            k, v = line.split(";", 3)[0].split("=", 1)
                            os.environ[k] = v

                key_path, temp_key = ssh.key.prepare(key)

                stderr, stdout = cmd.run(f"ssh-add {key_path}")
                if stderr:
                    raise SSHErr(stderr)

                if temp_key:
                    cmd.rm(key_path)
                return
            except Exception as e:
                raise SSHErr(e)

    @typed
    def exec(host: Str, user: Str, key: Str, command: Str) -> Tuple:
        try:
            from utils import cmd
            key_path, temp_key = ssh.key.prepare(key)
            try:
                ssh_cmd = (
                    f"ssh -i {key_path} "
                    f"-o StrictHostKeyChecking=no "
                    f"{user}@{host} {command}"
                )
                stderr, stdout = cmd.run(ssh_cmd)

                if stderr:
                    raise SSHErr(stderr)

                return stdout, stderr
            finally:
                if temp_key and key_path and key_path in File:
                    cmd.rm(key_path)
        except Exception as e:
            if isinstance(e, SSHErr):
                raise
            raise SSHErr(str(e))
