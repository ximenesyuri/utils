import os
import subprocess
import stat
from typed import typed, TYPE, Str, Path, Nill, Union, SSHKey
from utils.err import SSHErr
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
        if not isinstance(instance, Str):
            return False

        private = getattr(cls, "_ssh_private", None)
        types_ = getattr(cls, "_ssh_types", ())

        if private is None:
            return (
                isinstance(instance, SSHKey(private=True)) or
                isinstance(instance, SSHKey(private=False))
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
        def add(key: Union(Path, SSHKey(private=True))) -> Nill:
            try:
                if "SSH_AUTH_SOCK" not in os.environ:
                    out = subprocess.check_output(["ssh-agent", "-s"], text=True)
                    for line in out.splitlines():
                        if "SSH_AUTH_SOCK" in line or "SSH_AGENT_PID" in line:
                            k, v = line.split(";", 1)[0].split("=", 1)
                            os.environ[k] = v
                if key in Path:
                    subprocess.check_call(["ssh-add", key])
                    return
                from utils import cmd, file
                tmp_file = cmd.mktemp.file()
                file.write(tmp_file, key)
                os.chmod(tmp_file, stat.S_IRUSR | stat.S_IWUSR)
                subprocess.check_call(["ssh-add", tmp_file])
                cmd.rm(tmp_file)
                return
            except Exception as e:
                raise SSHErr(e)
