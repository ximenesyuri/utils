from typed import *
from utils.mods.path import path
from utils.mods.lib  import lib
from utils.err import PathErr, YMLErr

class yml:
    def read(yml_file):
        import yaml
        try:
            if path.is_file(yml_file):
                with open(yml_file, 'r') as file:
                    return yml.safe_load(file)
            else:
                raise PathErr(f"path '{yml_file}' does not exist or is not a file.")
        except Exception as e:
            raise YMLErr(f"Could not read YML file '{yml_file}'. Error: {e}")

    def write(json_data, output_file):
        import yaml
        try:
            with open(output_file, 'w') as file:
                yaml.dump(json_data, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise YMLErr(f"Could not write YML data to file '{output_file}'. Error: {e}")

    def dump(json_data: Json) -> Str:
        import yaml
        try:
            yaml.dump(json_data, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise YMLErr(f"Could not dump YML data. Error: {e}")


