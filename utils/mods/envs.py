import os
import json
from utils.mods.types import Path, Any, Type
from utils.mods.path import path
from utils.err import EnvErr

class Env(str):
    def __new__(cls, value):
        if not isinstance(value, str):
            raise TypeError("Env variable name must be a string.")

        if not all(c.isupper() or c.isdigit() or c == '_' for c in value):
            raise ValueError(
                "Env variable name must contain only uppercase letters, numbers, and underscores."
            )
        return super().__new__(cls, value)


class envs:
    def __get_dot_env():
        current_dir = os.path.abspath(".")
        while True:
            envpath = path.join(current_dir, ".env")
            if path.exists(envpath):
                return envpath
            parent_dir = path.dirname(current_dir)
            if parent_dir == current_dir:
                return None
            current_dir = parent_dir

    def load(envpath: Path = __get_dot_env()) -> None:
        if not path.exists(envpath):
            raise EnvErr(f".env file not found at '{envpath}'.")

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

    def is_defined(env: Env) -> Any:
        try:
            if os.getenv(Env(env)):
                return True
            return False
        except Exception as e:
            raise EnvErr(e)

    def get(env: Env) -> Any:
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

    def set(env: Env='', value: Any=None) -> None:
        try:
            if env and value:
                os.environ[Env(env)] = value
        except Exception as e:
            raise EnvErr(e)

    def type(env: Env='') -> Type:
        value = envs.get(env)
        if value is None:
            return None
        return type(value)

    def has_value(env: str='', value: Any=None) -> bool:
        env_value = envs.get(env)
        if env_value == value:
            return True
        return False
