import json as json_
from utils.mods.path import path
from utils.err import JsonErr, PathErr

class json:
    def read(json_file):
        try:
            if path.is_file(json_file):
                with open(json_file, 'r') as file:
                    return json_.load(file)
            else:
                raise PathErr(f"path '{json_file}' does not exists or is not a file.")
        except Exception as e:
            raise JsonErr(f"Could not read json file '{json_file}'.")

    def write(json_data, output_file):
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

    def flat(json_data):
        if isinstance(json_data, str):
            stripped = json_data.strip()
            if not stripped:
                raise ValueError("Empty JSON string provided.")
            json_data = json_.loads(stripped)

        flat_dict = {}

        def flatten(item, parent_key=""):
            if isinstance(item, dict):
                for key, value in item.items():
                    new_key = f"{parent_key}.{key}" if parent_key else key
                    flatten(value, new_key)
            else:
                flat_dict[parent_key] = item

        flatten(json_data)
        return flat_dict

        def unflat(flat_json_data):
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

        def has_entry(json_data, entry):
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if entry == key:
                    return True
            return False

        def check_entry(json_data, entry, value_type):
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if key == entry:
                    if not type(value) is value_type:
                        return False
                    return True
            return False

        def get_entry_value(entry, json_data):
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

        def get_entries_by_value(json_data, value):
            flat_json_data = json.flat(json_data)
            return [key for key, v in flat_json_data.items() if v == value]


        def set_entry_value(entry, json_data, new_value):
            flat_json_data = json.flat(json_data)
            for key, value in flat_json_data.items():
                if entry == key:
                    json_data[entry] = new_value
                    return json_data

        def get_row(json_data, row_name):
            row_entries = []
            for entry in json_data:
                for key, value in entry.items():
                    if key == row_name:
                        row_entries.append(value)
            return row_entries

        def normalize(json_data):
            if isinstance(json_data, list):
                normalized_list = []
                for item in json_data:
                    if isinstance(item, (dict, list)):
                        cleaned_item = json.normalize(item)
                        normalized_list.append(cleaned_item)
                    elif not(item == "" or item is None):
                        normalized_list.append(item)
                return normalized_list

            if isinstance(json_data, dict):
                return json.normalize(list(json.flat(json_data)))

        def replace(json_data, entry=None, old="", new=""):
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
