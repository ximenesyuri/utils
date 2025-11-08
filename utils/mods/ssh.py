import os
import subprocess
import stat
from typed import typed, Path, Nill, Union, SSHKey
from utils.err import SSHErr

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




