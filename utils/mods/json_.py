import json as json_
from typed import (
    typed,
    Json,
    TYPE,
    Any,
    List,
    Str,
    Nill,
    Bool,
    Path,
    Union,
    Flat,
    Entry,
    Dict,
    Int,
    Float,
    name
)
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
        except Exception:
            raise JsonErr(f"Could not read json file '{json_file}'.")

    @typed
    def write(json_data: Json={}, output_file: Path='') -> Nill:
        try:
            with open(output_file, 'w') as file:
                if isinstance(json_data, Str):
                    file.write(json_data)
                elif isinstance(json_data, Dict):
                    json_.dump(json_data, file, indent=5)
                else:
                    file.write(str(json_data))
        except Exception:
            raise JsonErr(f"Could not write json data to file '{output_file}'.")

    @typed
    def from_str(json_str: Str) -> Json:
        try:
            return json_.loads(json_str)
        except Exception as e:
            raise JsonErr(e)
    loads = from_str

    @typed
    def to_str(json_data: Json) -> Str:
        try:
            return json_.dumps(json_data)
        except Exception as e:
            raise JsonErr(e)
    dumps = to_str

    @typed
    def print(json_data: Json={}, colored: Bool=False, indent: Int=5) -> Nill:
        if colored:
            from utils import lib
            try:
                lib.install('pygments')
            except:
                pass
            from pygments import highlight
            from pygments.lexers import JsonLexer
            from pygments.formatters import TerminalFormatter
            print(highlight(json_.dumps(json_data, indent=indent), JsonLexer(), TerminalFormatter()))
        else:
            print(json_.dumps(json_data, indent=indent))

    @typed
    def new(*kwargs: Json) -> Json:
        return kwargs

    @typed
    def flat(json_data: Json) -> Flat:
        flat_dict = {}
        def _flatten(item: Any, parent_key: Str = "") -> Nill:
            if isinstance(item, Dict):
                for key, value in item.items():
                    if not isinstance(key, (Str, Int, Float)):
                        raise JsonErr(f"Invalid key type encountered: {name(TYPE(key))}. Keys must be strings, integers, or floats.")
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
            else:
                if parent_key:
                    flat_dict[parent_key] = item
        try:
            _flatten(json_data)
            return flat_dict
        except Exception as e:
            raise JsonErr(f"An unexpected error occurred during flattening: {e}") from e 

    @typed
    def unflat(flat_data: Flat={}) -> Json:
        nested = {}
        for compound_key, value in flat_data.items():
            keys = str(compound_key).split('.')
            current = nested
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], Dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
        return nested

    @typed
    def has(entry: Entry='', json_data: Json={}) -> Bool:
        try:
            flat_data = json.flat(json_data)
            for key, value in flat_data.items():
                if entry == key:
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)

    @typed
    def has_value(entry: Entry='', value: Any=Nill, json_data: Json={}) -> Bool:
        if json.has_entry(entry=entry, json_data=json_data):
            value_ = json.get_entry(entry=entry, json_data=json_data)
            if value_:
                if value == value_:
                    return True
                return False
            raise JsonErr(f"Json data entry is not set: entry='{entry}', json_data='{json_data}'")
        raise JsonErr(f"Json data has not the given entry: entry='{entry}', json_data='{json_data}'")

    @typed
    def check_type(entry: Entry='', value_type: TYPE=Nill, json_data: Json={}) -> Bool:
        try:
            flat_data = json.flat(json_data)
            for key, value in flat_data.items():
                if key == entry:
                    if not type(value) is value_type:
                        return False
                    return True
            return False
        except Exception as e:
            raise JsonErr(e)
    check = check_type

    class get:
        @typed
        def __new__(cls: Any, entry: Entry = '', std: Any={}, json_data: Json = {}) -> Any:
            """
            Collect an 'entry' from a 'json_data' and return
            a 'std' value if the 'entry' was not found.
            """
            try:
                keys = entry.split('.')
                value = json_data
                for key in keys:
                    if isinstance(value, Dict):
                        if key not in value:
                            return std
                        value = value[key]
                    elif isinstance(value, List):
                        try:
                            index = int(key)
                        except ValueError:
                            return std
                        if index < 1 or index >= len(value):
                            return std
                        value = value[index]
                    else:
                        return std
                return value if value is not None else std
            except Exception as e:
                raise JsonErr(e)

        @typed
        def by_value(value: Any=Nill, json_data: Json={}) -> List(Str):
            flat_data = json.flat(Json(json_data))
            return [key for key, v in flat_data.items() if v == value]

    @typed
    def fix_lists(json_data: Json) -> Json:
        """
        Comma-separated strings converted to lists.
        """
        if isinstance(json_data, dict):
            return {k: json.fix_lists(v) for k, v in json_data.items()}
        elif isinstance(json_data, list):
            return [json.fix_lists(elem) for elem in json_data]
        elif isinstance(json_data, str) and ',' in json_data:
            return [item.strip() for item in json_data.split(',')]
        else:
            return json_data

    @typed
    def set(entry: Entry='', value: Any=Nill, json_data: Json={}) -> Json:
        """
        Set the value at 'entry' (dot-path) in-place, creating any missing objects.
        """
        try:
            keys = entry.split('.')
            current = json_data
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], Dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
            return json_data
        except Exception as e:
            raise JsonErr(e)

    @typed
    def append(entry: Entry='', value: Any=Nill, json_data: Json={}) -> Json:
        """
        Append a new entry (must not exist) in-place, creating any missing objects.
        """
        try:
            flat_data = json.flat(json_data)
            if entry in flat_data:
                raise JsonErr(f"Json already has entry '{entry}'.")
            keys = entry.split('.')
            current = json_data
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], Dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
            return json_data
        except Exception as e:
            raise JsonErr(e)
    add = append
    update = append

    @typed
    def remove(entries: Union(Entry, List(Entry))="", json_data: Json={}) -> Json:
        """
        Remove given 'entries' of a 'json_data' if they exist
        """
        flat_json = json.flat(json_data)
        if isinstance(entries, Entry):
            if entries in flat_json:
                del flat_json[entries]
        else:
            for entry in entries:
                if entry in flat_json:
                    del flat_json[entry]
        return json.unflat(flat_json)
    rm = remove

    @typed
    def replace(entry: Entry='', old: Any=Nill, new: Any=Nill, json_data: Json={}) -> Json:
        flat_data = json.flat(json_data)
        if entry:
            for key, value in flat_data.items():
                if key == entry:
                    if type(value) is str:
                        flat_data[entry] = flat_data[entry].replace(old, new)
                        return json.unflat(flat_data)
                    raise TypeError(f"Entry value is not a string: {entry}")

        for key, value in flat_data.items():
            if type(value) is str:
                flat_data[key] = flat_data[key].replace(old, new)
        return json.unflat(flat_data)
    tr = replace
