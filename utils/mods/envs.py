import os
import json
from typed import *
from typed.examples import Env
from utils.mods.path import path
from utils.err import EnvErr

class envs:
    @typed
    def dotenv() -> Union(Path, Nill):
        current_dir = path.abs(path.dirname(__file__))
        while True:
            envpath = path.join(current_dir, ".env")
            if path.exists(envpath):
                return envpath
            parent_dir = path.dirname(current_dir)
            if parent_dir == current_dir:
                return None
            current_dir = parent_dir

    @typed
    def load(envpath: Union(Path, Nill)=None) -> Nill:
        if not envpath:
            envpath = envs.dotenv()
            if not envpath:
                envpath = '.env'
        if not path.exists(envpath):
            raise EnvErr(f".env file not found.")

        with open(envpath, 'r') as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                comment_index = line.find('#')
                if comment_index != -1:
                    line = line[:comment_index].strip()

                equals_index = line.find('=')
                if equals_index == -1:
                    continue

                key = line[:equals_index].strip()
                value = line[equals_index + 1:].strip()

                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'') and value.endswith("''):
                    value = value[1:-1]

                value = value.replace('\\n', '\n')
                value = value.replace('\\r', '\r')
                value = value.replace('\\t', '\t')
                value = value.replace('\\"', '"')
                value = value.replace("\\'", "'")
                value = value.replace('\\\\', '\\')

                os.environ[key] = value

    @typed
    def get_all(envpath: Union(Path, Nill)=None) -> Dict(Any):
        if not envpath:
            envpath = envs.dotenv()
            if not envpath:
                envpath = '.env'
        if not path.exists(envpath):
            raise EnvErr(f".env file not found at '{envpath}'.")
        with open(envpath, 'r') as f:
            envs_ = {}
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                equals_index = line.find('=')
                if equals_index == -1:
                    continue
                key = line[:equals_index].strip()
                value = line[equals_index + 1:].strip()
                envs_.update({key: value})
            return envs_

    @typed
    def print(envpath: Union(Path, Nill)=None) -> Nill:
        print(envs.get_all(envpath))

    @typed
    def is_defined(env: Env='') -> Any:
        try:
            if os.getenv(env):
                return True
            return False
        except Exception as e:
            raise EnvErr(e)
    exists = is_defined

    @typed
    def get(env: Env='') -> Any:
        if not envs.is_defined(env):
            raise EnvErr(f"The env '{env}' is not defined.")
        value = os.getenv(env)
        try:
            processed_value = value.replace("'", '"')
            parsed_value = json.loads(processed_value)

            if isinstance(parsed_value, (list, dict)) or (isinstance(parsed_value, (int, float, bool)) and not value.isdigit() and not (value.count('.') == 1 and value.replace('.', '').isdigit())):
                return parsed_value
            elif isinstance(parsed_value, str) and parsed_value != value:
                return value
            elif isinstance(parsed_value, (int, float, bool)) and (value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit())):
                return parsed_value
            elif isinstance(parsed_value, list) and value.startswith('[') and value.endswith(']'):
                return parsed_value
            elif isinstance(parsed_value, dict) and value.startswith('{') and value.endswith('}'):
                return parsed_value
            elif isinstance(parsed_value, list) and value.startswith('{') and value.endswith('}'):
                return set(parsed_value)

        except json.JSONDecodeError:
            pass

        if value.isdigit():
            try:
                return int(value)
            except ValueError:
                pass
        if value.count('.') == 1 and value.replace('.', '').isdigit():
            try:
                return float(value)
            except ValueError:
                pass
        return value

    @typed
    def set(env: Env='', value: Any=Nill) -> Nill:
        try:
            if env and value:
                os.environ[env] = value
        except Exception as e:
            raise EnvErr(e)

    @typed
    def type(env: Env='') -> Type:
        value = envs.get(env)
        if value is None:
            return None
        return type(value)

    @typed
    def has_value(env: Env='', value: Any=Nill) -> Bool:
        env_value = envs.get(env)
        if env_value == value:
            return True
        return False
