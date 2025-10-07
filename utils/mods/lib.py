import os
import importlib
import subprocess
from pathlib import Path

class lib:
    def install(lib, venv=None):
        if importlib.util.find_spec(lib) is not None:
            return

        if venv is None:
            current = Path.cwd()
            found = False
            for parent in [current] + list(current.parents):
                possible = parent / '.venv'
                if possible.exists() and (possible / 'bin' / 'python').exists():
                    venv = str(possible)
                    found = True
                    break
            if not found:
                return 'Error: No virtual environment found (.venv not located in parent directories)'

        if os.name == 'nt':
            pip_executable = os.path.join(venv, 'Scripts', 'pip.exe')
        else:
            pip_executable = os.path.join(venv, 'bin', 'pip')

        if not os.path.isfile(pip_executable):
            return f"Error: pip not found in the virtual environment at '{venv}'."

        try:
            subprocess.check_call([pip_executable, 'install', lib, '-q'])
            return f"'{lib}' has been installed in venv: {venv}"
        except subprocess.CalledProcessError as e:
            return f"Error installing '{lib}' in venv: {venv}. Detail: {str(e)}" 
