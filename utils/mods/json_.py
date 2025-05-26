import re
import json as json_
from utils.mods.types import Path, Json, JsonData, Any, Type, List
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

class JsonFlat(dict):
    def __init__(self, json_obj: Json):
        super().__init__()

        if not isinstance(json_obj, Json):
            raise TypeError("Input must be an instance of the Json class.")

        data_to_flatten = json_obj.data

        flat_dict = {}

        def flatten(item: Any, parent_key: str = "") -> None:
            if isinstance(item, dict):
                for key, value in item.items():
                    if not isinstance(key, (str, int, float)):
                        raise JsonErr(f"Invalid key type encountered: {type(key)}. Keys must be strings, integers, or floats.")
                    str_key = str(key)
                    new_key = f"{parent_key}.{str_key}" if parent_key else str_key
                    flatten(value, new_key)
            elif isinstance(item, list):
                for index, value in enumerate(item):
                    new_key = f"{parent_key}.{index}" if parent_key else str(index)
                    flatten(value, new_key)
            elif isinstance(item, set):
                for index, value in enumerate(item):
                    new_key = f"{parent_key}.{index}" if parent_key else str(index)
                    flatten(value, new_key)
            elif isinstance(item, (str, int, float, bool, type(None))):
                if parent_key:
                    flat_dict[parent_key] = item
            else:
                raise JsonErr(f"Unsupported data type encountered during flattening: {type(item)}")
        try:
            flatten(data_to_flatten)
            self.update(flat_dict)
        except JsonErr as e:
            raise JsonErr(f"Error during flattening: {e}") from e
        except Exception as e:
            raise JsonErr(f"An unexpected error occurred during flattening: {e}") from e

    def unflat(self) -> JsonData:
        nested = {}
        for compound_key, value in self.items():
            keys = compound_key.split('.')
            current = nested
            for i, key in enumerate(keys[:-1]):
                try:
                    nested_key: Any = int(key)
                except ValueError:
                    nested_key = key

                if nested_key not in current:
                    if i + 1 < len(keys) - 1 and keys[i+1].isdigit():
                        current[nested_key] = []
                    elif nested_key.isdigit():
                        current[nested_key] = []
                    else:
                        current[nested_key] = {}

                if isinstance(current[nested_key], (dict, list)):
                    current = current[nested_key]
                else:
                    raise JsonErr(f"Unflattening failed: Expected dict or list, but found {type(current[nested_key])} at key '{'.'.join(keys[:i+1])}'") 
            last_key_str = keys[-1]
            try:
                last_key: Any = int(last_key_str)
            except ValueError:
                last_key = last_key_str
            if isinstance(current, dict):
                current[last_key] = value
            elif isinstance(current, list):
                index = int(last_key_str)
                while len(current) <= index:
                    current.append(None)
                current[index] = value
            else:
                raise JsonErr(f"Unflattening failed: Expected dict or list to add value, but found {type(current)} for key '{compound_key}'")
        if len(nested) == 1 and list(nested.keys())[0] == '0' and isinstance(list(nested.values())[0], list):
            return list(nested.values())[0]
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

    def write(json_data: JsonData={}, output_file: Path='') -> None:
        try:
            with open(output_file, 'w') as file:
                if isinstance(json_data, str):
                    file.write(json_data)
                elif isinstance(json_data, dict):
                    json_.dump(json_data, file, indent=4)
                else:
                    file.write(str(json_data))
        except Exception as e:
            raise JsonErr(f"Could not write json data to file '{output_file}'.")

    def flat(json_data: JsonData={}) -> JsonFlat:
        try:
            return JsonFlat(Json(json_data))
        except Exception as e:
            raise JsonErr(e)

    def unflat(flat_json_data: JsonFlat={}) -> Json:
        try:
            return JsonFlat(flat_json_data).unflat()
        except Exception as e:
            raise JsonErr(e)

    def has_entry(entry: JsonEntry='', json_data: JsonData={}) -> bool:
        try:
            entry = JsonEntry(entry)
            flat_json_data = json.flat(Json(json_data))
            for key, value in flat_json_data.items():
                if entry == key:
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)

    def check_entry_type(entry: JsonEntry='', value_type: Type=None, json_data: JsonData={}) -> bool:
        try:
            entry = JsonEntry(entry)
            flat_json_data = json.flat(Json(json_data))
            for key, value in flat_json_data.items():
                if key == entry:
                    if not type(value) is value_type:
                        return False
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)

    def get_entry(entry: JsonEntry='', json_data: JsonData={}) -> Any:
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

    def entry_has_value(entry: JsonEntry='', value: Any=None, json_data: JsonData={}) -> bool:
        if json.has_entry(entry=entry, json_data=json_data):
            value_ = json.get_entry(entry=entry, json_data=json_data)
            if value_:
                if value == value_:
                    return True
                return False
            raise JsonErr(f"Json data entry is not set: entry='{entry}', json_data='{json_data}'")
        raise JsonErr(f"Json data has not the given entry: entry='{entry}', json_data='{json_data}'")

    def get_entries_with_given_value(json_data: JsonData={}, value: Any=None) -> List[str]:
        flat_json_data = json.flat(Json(json_data))
        return [key for key, v in flat_json_data.items() if v == value]

    def set_entry_value(entry: JsonEntry='', json_data: JsonData={}, new_value: Any=None) -> JsonData:
        try:
            entry = JsonEntry(entry)
            flat_json_data = json.flat(Json(json_data))
            for key, value in flat_json_data.items():
                if entry == key:
                    json_data[entry] = new_value
                    return json_data
        except Exception as e:
            raise JsonErr(e)

    def replace(json_data: JsonData, entry=None, old="", new="") -> JsonData:
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
