import re
import json as json_
from utils.mods.types import Path, Json, Any, Type, List
from utils.mods.path  import path
from utils.err import JsonErr, PathErr

class JsonEntry:
    _VALID_ENTRY_REGEX = re.compile(r'^[a-zA-Z0-9_.]+$')
    def __init__(self, entry: str):
        if not isinstance(entry, str):
            raise TypeError("FlatJsonEntry must be initialized with a string.")

        if not self._VALID_ENTRY_REGEX.match(entry):
            raise JsonErr(
                f"Invalid characters in FlatJsonEntry string: '{entry}'. "
                "Expected format: numbers, letters, underscores, and dots."
            )
        self._value = entry

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"JsonEntry('{self._value}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsonEntry):
            return self._value == other._value
        elif isinstance(other, str):
            return self._value == other
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    @property
    def type(self) -> Type:
        return type(self)

    @property
    def value(self) -> str:
        return self._value

class JsonFlat:
    def __init__(self, json_data: Json):
        flat_dict = {}

        def flatten(item, parent_key=""):
            if isinstance(item, dict):
                for key, value in item.items():
                    new_key = f"{parent_key}.{key}" if parent_key else key
                    flatten(value, new_key)
            elif isinstance(item, list):
                for index, value in enumerate(item):
                    new_key = f"{parent_key}.{index}" if parent_key else str(index)
                    flatten(value, new_key)
            else:
                if parent_key:
                    flat_dict[parent_key] = item

        if isinstance(json_data, str):
            stripped = json_data.strip()
            if not stripped:
                raise ValueError("Empty JSON string provided.")
            try:
                json_data = json_.loads(stripped)
            except json.JSONDecodeError as e:
                raise JsonErr(f"Invalid JSON string provided: {e}") from e

        if not isinstance(json_data, (dict, list)):
            if json_data is not None:
                raise TypeError("Input data must be a dictionary, list, or JSON string representing a dictionary or list.")
            else:
                self._data = {}
                return
        flatten(json_data)
        self._data = {}
        for key, value in flat_dict.items():
            try:
                json_entry_key = JsonEntry(key)
                self._data[json_entry_key] = value
            except (TypeError, JsonErr) as e:
                raise JsonErr(f"Internal flattening error: Invalid key '{key}' generated: {e}") from e

    def unflat(self) -> Json:
        nested = {}
        for compound_key, value in self.items():
            keys = compound_key.split('.')
            current = nested
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
        return nested

class json:
    def read(json_file: Path='') -> Json:
        try:
            if path.is_file(json_file):
                with open(json_file, 'r') as file:
                    return json_.load(file)
            else:
                raise PathErr(f"path '{json_file}' does not exists or is not a file.")
        except Exception as e:
            raise JsonErr(f"Could not read json file '{json_file}'.")

    def write(json_data: Json={}, output_file: Path='') -> None:
        try:
            with open(output_file, 'w') as file:
                if isinstance(json_data, str):
                    file.write(json_data)
                elif isinstance(json_data, dict):
                    json.dump(json_data, file, indent=4)
                else:
                    file.write(str(json_data))
        except Exception as e:
            raise JsonErr(f"Could not write json data to file '{output_file}'.")

    def flat(json_data: Json={}) -> JsonFlat:
        try:
            return JsonFlat(json_data)
        except Exception as e:
            raise JsonErr(e)

    def unflat(flat_json_data: JsonFlat={}) -> Json:
        try:
            return JsonFlat(flat_json_data).unflat()
        except Exception as e:
            raise JsonErr(e)

    def has_entry(entry: JsonEntry='', json_data: Json={}) -> bool:
        try:
            entry = JsonEntry(entry)
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if entry == key:
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)

    def check_entry_type(entry: JsonEntry='', value_type: Type=None, json_data: Json={}) -> bool:
        try:
            entry = JsonEntry(entry)
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if key == entry:
                    if not type(value) is value_type:
                        return False
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)

    def get_entry(entry: JsonEntry='', json_data: Json={}) -> Any:
        try:
            entry = JsonEntry(entry)
            keys = entry.split('.')
            value = json_data
            for key in keys:
                if isinstance(value, dict):
                    if key not in value:
                        return ''
                    value = value[key]
                elif isinstance(value, list):
                    try:
                        index = int(key)
                    except ValueError:
                        return ''
                    if index < 0 or index >= len(value):
                        return ''
                    value = value[index]
                else:
                    return ''
            return value if value is not None else ''
        except Exception as e:
            raise JsonErr(e)

    def entry_has_value(entry: JsonEntry='', value: Any=None, json_data: Json={}) -> bool:
        if json.has_entry(entry=entry, json_data=json_data):
            value_ = json.get_entry(entry=entry, json_data=json_data)
            if value_:
                if value == value_:
                    return True
                return False
            raise JsonErr(f"Json data entry is not set: entry='{entry}', json_data='{json_data}'")
        raise JsonErr(f"Json data has not the given entry: entry='{entry}', json_data='{json_data}'")

    def get_entries_with_given_value(json_data: Json={}, value: Any=None) -> List[str]:
        flat_json_data = json.flat(json_data)
        return [key for key, v in flat_json_data.items() if v == value]

    def set_entry_value(entry: JsonEntry='', json_data: Json={}, new_value: Any=None) -> Json:
        try:
            entry = JsonEntry(entry)
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if entry == key:
                    json_data[entry] = new_value
                    return json_data
        except Exception as e:
            raise JsonErr(e)

    def replace(json_data: Json, entry=None, old="", new=""):
        flat_json_data = json.flat(json_data)
        if entry:
            for key, value in flat_json_data.items():
                if key == entry:
                    if type(value) is str:
                        flat_json_data[entry] = flat_json_data[entry].replace(old, new)
                        return json.unflat(flat_json_data)
                    raise TypeError(f"Entry value is not a string: {entry}")

        for key, value in flat_json_data.items():
            if type(value) is str:
                flat_json_data[key] = flat_json_data[key].replace(old, new)
        return json.unflat(flat_json_data)
