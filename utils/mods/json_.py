import re
import json as json_
from typed import typed, Json, Type, Any, List, Str, Regex, Nill, Bool, Path
from typed.examples import JsonFlat, JsonFlatEntry
from utils.mods.path  import path
from utils.err import JsonErr, PathErr

class json:
    @typed
    def read(json_file: Path='') -> Json:
        try:
            if path.is_file(json_file):
                with open(json_file, 'r') as file:
                    return json_.load(file)
            else:
                raise PathErr(f"path '{json_file}' does not exists or is not a file.")
        except Exception as e:
            raise JsonErr(f"Could not read json file '{json_file}'.")

    @typed
    def write(json_data: Json={}, output_file: Path='') -> Nill:
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

    @typed
    def print(json_data: Json={}) -> Nill:
        print(json_.dumps(json_data, indent=4))

    @typed
    def new(*kwargs: Json) -> Json:
        return kwargs

    @typed
    def flat(json_data: Json) -> JsonFlat:
        flat_dict = {}
        def _flatten(item: Any, parent_key: Str = "") -> Nill:
            if isinstance(item, dict):
                for key, value in item.items():
                    if not isinstance(key, (str, int, float)):
                        raise JsonErr(f"Invalid key type encountered: {type(key)}. Keys must be strings, integers, or floats.")
                    str_key = str(key)
                    new_key = f"{parent_key}.{str_key}" if parent_key else str_key
                    _flatten(value, new_key)
            elif isinstance(item, list):
                for index, value in enumerate(item):
                    new_key = f"{parent_key}.{index}" if parent_key else str(index)
                    _flatten(value, new_key)
            elif isinstance(item, set):
                for index, value in enumerate(sorted(item, key=str)):
                    new_key = f"{parent_key}.{index}" if parent_key else str(index)
                    _flatten(value, new_key)
            elif isinstance(item, (str, int, float, bool, type(None))):
                if parent_key:
                    flat_dict[parent_key] = item
            else:
                raise JsonErr(f"Unsupported data type encountered during flattening: {type(item)}")
        try:
            _flatten(json_data)
            return flat_dict
        except Exception as e:
            raise JsonErr(f"An unexpected error occurred during flattening: {e}") from e 

    @typed
    def unflat(flat_json_data: JsonFlat={}) -> Json:
        nested = {}
        for compound_key, value in flat_json_data.items():
            keys = compound_key.split('.')
            current = nested
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
        return nested

    @typed
    def has_entry(entry: JsonFlatEntry='', json_data: Json={}) -> Bool:
        try:
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if entry == key:
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)
    has = has_entry

    @typed
    def check_entry_type(entry: JsonFlatEntry='', value_type: Type=Nill, json_data: Json={}) -> Bool:
        try:
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if key == entry:
                    if not type(value) is value_type:
                        return False
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)
    check = check_entry_type

    @typed
    def get_entry(entry: JsonFlatEntry='', json_data: Json={}) -> Any:
        try:
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
    get = get_entry

    @typed
    def entry_has_value(entry: JsonFlatEntry='', value: Any=Nill, json_data: Json={}) -> Bool:
        if json.has_entry(entry=entry, json_data=json_data):
            value_ = json.get_entry(entry=entry, json_data=json_data)
            if value_:
                if value == value_:
                    return True
                return False
            raise JsonErr(f"Json data entry is not set: entry='{entry}', json_data='{json_data}'")
        raise JsonErr(f"Json data has not the given entry: entry='{entry}', json_data='{json_data}'")
    has_value = entry_has_value

    @typed
    def get_entries_with_given_value(json_data: Json={}, value: Any=Nill) -> List(Str):
        flat_json_data = json.flat(Json(json_data))
        return [key for key, v in flat_json_data.items() if v == value]

    @typed
    def set_entry_value(entry: JsonFlatEntry='', json_data: Json={}, new_value: Any=Nill) -> Json:
        try:
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if entry == key:
                    json_data[entry] = new_value
                    return json_data
        except Exception as e:
            raise JsonErr(e)
    set = set_entry_value

    @typed
    def replace(json_data: Json, entry: JsonFlatEntry='', old: Any=Nill, new: Any=Nill) -> Json:
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
