from importlib import import_module as __import__
from typing import TYPE_CHECKING as __lsp__

def lazy(imports):
    all_names = list(imports.keys())
    all_list_str = ",\n    ".join(f'"{name}"' for name in all_names)
    all_code = f"__all__ = [\n    {all_list_str}\n]\n"

    lazy_dict_items = []
    for name, module_path in imports.items():
        attr_name = name
        if name == "dt" and "datetime" in imports and imports["datetime"] == module_path:
            module_path_for_dt = imports["datetime"]
            attr_name_for_dt = "datetime"
            lazy_dict_items.append(f'    "{name}":       ("{module_path_for_dt}", "{attr_name_for_dt}"),')
        else:
            lazy_dict_items.append(f'    "{name}":       ("{module_path}", "{attr_name}"),')

    lazy_dict_str = "\n".join(lazy_dict_items)
    lazy_code = f"\n__lazy__ = {{\n{lazy_dict_str}\n}}\n"

    boilerplate_code = """

def __getattr__(name):
    try:
        module_name, attr_name = __lazy__[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None

    module = __import__(module_name)
    attr = getattr(module, attr_name)
    globals()[name] = attr
    return attr


def __dir__():
    return sorted(set(globals().keys()) | set(__all__))
"""
    generated_code_string = all_code + lazy_code + boilerplate_code
    exec(generated_code_string, globals())

    return __lsp__
