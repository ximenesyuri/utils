from typed import *
from utils.mods.path import path
from utils.mods.lib  import lib
from utils.err import PathErr, YamlErr

class yaml:
    def read(yaml_file):
        lib.install("pyyaml")
        import yaml
        try:
            if path.is_file(yaml_file):
                with open(yaml_file, 'r') as file:
                    return yaml.safe_load(file)
            else:
                raise PathErr(f"path '{yaml_file}' does not exist or is not a file.")
        except Exception as e:
            raise YamlErr(f"Could not read YAML file '{yaml_file}'. Error: {e}")

    def write(json_data, output_file):
        lib.install("pyyaml")
        import yaml
        try:
            with open(output_file, 'w') as file:
                yaml.dump(json_data, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise YamlErr(f"Could not write YAML data to file '{output_file}'. Error: {e}")

    def dump(json_data: Json) -> Str:
        lib.install("pyyaml")
        import yaml
        try:
            yaml_.dump(json_data, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise YamlErr(f"Could dum YAML data. Error: {e}")


