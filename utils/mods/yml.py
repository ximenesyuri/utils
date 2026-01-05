import os
from typed import *
from utils.mods.path  import PathErr
from utils.mods.lib   import lib
from utils.mods.json_ import Json

class YMLErr(Exception): pass

class yml:
    def read(yml_file):
        lib.install('pyyaml')
        import yaml
        try:
            if os.path.isfile(yml_file):
                with open(yml_file, 'r') as file:
                    json_data = yaml.safe_load(file)
                    return json_data if json_data else {}
            else:
                raise PathErr(f"path '{yml_file}' does not exist or is not a file.")
        except Exception as e:
            raise YMLErr(f"Could not read YML file '{yml_file}'. Error: {e}")

    def write(json_data, output_file):
        lib.install('pyyaml')
        import yaml
        try:
            with open(output_file, 'w') as file:
                yaml.dump(json_data, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise YMLErr(f"Could not write YML data to file '{output_file}'. Error: {e}")

    def dump(json_data: Json) -> Str:
        lib.install('pyyaml')
        import yaml
        try:
            yaml.dump(json_data, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise YMLErr(f"Could not dump YML data. Error: {e}")


