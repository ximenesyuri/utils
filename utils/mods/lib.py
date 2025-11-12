import os
import subprocess
from typed import typed, Str, Tuple, Bool, Maybe, Nill
from utils.err import LibErr

class lib:
    @typed
    def is_installed(lib: Str, version: Maybe(Str)=None) -> Bool:
        try:
            venv = os.getenv('VIRTUAL_ENV')
            site_packages_path = None
            if os.name == 'nt':
                site_packages_path = os.path.join(venv, 'Lib', 'site-packages')
            else:
                lib_dir = os.path.join(venv, 'lib')
                if os.path.isdir(lib_dir):
                    for entry in os.listdir(lib_dir):
                        if entry.startswith('python') and os.path.isdir(os.path.join(lib_dir, entry, 'site-packages')):
                            site_packages_path = os.path.join(lib_dir, entry, 'site-packages')
                            break
                if not site_packages_path:
                    site_packages_path = os.path.join(venv, 'site-packages')

            if not site_packages_path or not os.path.isdir(site_packages_path):
                print(f"Warning: site-packages directory not found at expected locations for '{venv}'.")
                return False

            normalized_lib_name = lib.lower().replace('-', '_')

            target_version_suffix = None
            if version:
                target_version_suffix = f"-{version}.dist-info".lower()

            for item in os.listdir(site_packages_path):
                item_lower = item.lower()

                is_dist_info = item_lower.endswith('.dist-info') and os.path.isdir(os.path.join(site_packages_path, item))
                is_egg_info = not is_dist_info and item_lower.endswith('.egg-info') and os.path.isdir(os.path.join(site_packages_path, item))

                if is_dist_info or is_egg_info:
                    if '-' in item_lower:
                        package_name_part = item_lower.split('-', 1)[0]
                    elif '.' in item_lower:
                        package_name_part = item_lower.split('.', 1)[0]
                    else:
                        package_name_part = item_lower

                    normalized_found_package_name = package_name_part.replace('-', '_')

                    if normalized_found_package_name == normalized_lib_name:
                        if version is None:
                            return True
                        else:
                            if is_dist_info:
                                if item_lower == (f"{normalized_lib_name}{target_version_suffix}").lower():
                                    return True
                            elif is_egg_info:
                                if version.lower() in item_lower:
                                    return True
            return False
        except Exception as e:
            raise LibErr(e)

    @typed
    def install(*libs: Tuple(Str)) -> Nill:
        try:
            for l in libs:
                if not lib.is_installed(l):
                    venv = os.getenv('VIRTUAL_ENV')
                    if os.name == 'nt':
                        pip_executable = os.path.join(venv, 'Scripts', 'pip.exe')
                    else:
                        pip_executable = os.path.join(venv, 'bin', 'pip')

                    if not os.path.isfile(pip_executable):
                        return f"Error: pip not found in the virtual environment at '{venv}'."
                    try:
                        subprocess.check_call([pip_executable, 'install', l, '-q'])
                    except subprocess.CalledProcessError as e:
                        raise LibErr(f"Error installing '{lib}' in venv: {venv}. Detail: {str(e)}")
        except Exception as e:
            raise LibErr(e)

    @typed
    def uninstall(*libs: Str) -> Nill:
        try:
            for l in libs:
                if lib.is_installed(l):
                    venv = os.getenv('VIRTUAL_ENV')
                    if os.name == 'nt':
                        pip_executable = os.path.join(venv, 'Scripts', 'pip.exe')
                    else:
                        pip_executable = os.path.join(venv, 'bin', 'pip')

                    if not os.path.isfile(pip_executable):
                        return f"Error: pip not found in the virtual environment at '{venv}'."
                    try:
                        subprocess.check_call([pip_executable, 'uninstall', l, '-y', '-q'])
                    except subprocess.CalledProcessError as e:
                        raise LibErr(f"Error uninstalling '{lib}' in venv: {venv}. Detail: {str(e)}")
        except Exception as e:
            raise LibErr(e)
