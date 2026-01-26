from importlib import import_module as __import__
from typing import TYPE_CHECKING as __lsp__

__all__ = [
    "Cron",
    "HEX",
    "RGB",
    "HSL",
    "Env",
    "Module",
    "Json",
    "Entry",
    "Table",
    "Path",
    "File",
    "Exists",
    "Dir",
    "Mount",
    "Symlink",
    "Url",
    "Hostname",
    "Nat",
    "Num",
    "Even",
    "Odd",
    "Pos",
    "Neg",
    "IPv4",
    "IPv6",
    "Char",
    "Email",
    "Extension",
    "PathUrl",
    "Header",
    "Params",
    "Response",
    "Result",
    "Data"
]

__lazy__ = {
    "Cron":      ("utils.mods.cron",            "Cron"),

    "HEX":       ("utils.mods.color",           "HEX"),
    "RGB":       ("utils.mods.color",           "RGB"),
    "HSL":       ("utils.mods.color",           "HSL"),

    "Env":       ("utils.mods.envs",            "Env"),
    "Module":    ("utils.mods.mod",             "Module"),

    "Json":      ("utils.mods.json_",           "Json"),
    "Entry":     ("utils.mods.json_",           "Entry"),

    "Table":     ("utils.mods.table",           "Table"),

    "Path":      ("utils.mods.path",            "Path"),
    "File":      ("utils.mods.path",            "File"),
    "Exists":    ("utils.mods.path",            "Exists"),
    "Dir":       ("utils.mods.path",            "Dir"),
    "Mount":     ("utils.mods.path",            "Mount"),
    "Symlink":   ("utils.mods.path",            "Symlink"),

    "Url":       ("utils.mods.url",             "Url"),
    "Hostname":  ("utils.mods.url",             "Hostname"),

    "Nat":       ("utils.mods.number",          "Nat"),
    "Num":       ("utils.mods.number",          "Num"),
    "Even":      ("utils.mods.number",          "Even"),
    "Odd":       ("utils.mods.number",          "Odd"),
    "Pos":       ("utils.mods.number",          "Pos"),
    "Neg":       ("utils.mods.number",          "Neg"),

    "IPv4":      ("utils.mods.ip",              "IPv4"),
    "IPv6":      ("utils.mods.ip",              "IPv6"),

    "Char":      ("utils.mods.helper.types",    "Char"),
    "Email":     ("utils.mods.helper.types",    "Email"),
    "Extension": ("utils.mods.helper.types",    "Extension"),
    "PathUrl":   ("utils.mods.helper.types",    "PathUrl"),
    "Result":    ("utils.mods.helper.types",    "Result"),

    "Header":    ("utils.mods.helper.http_",    "Header"),
    "Params":    ("utils.mods.helper.http_",    "Params"),
    "Response":  ("utils.mods.http_",           "Response"),
    "Data":      ("utils.mods.http_",           "Data")
}


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


if __lsp__:
    from utils.mods.cron   import Cron
    from utils.mods.color  import HEX, RGB, HSL
    from utils.mods.envs   import Env
    from utils.mods.json_  import Json, Entry, Table
    from utils.mods.path   import Path, File, Exists, Dir, Mount, Symlink
    from utils.mods.url    import Url, Hostname
    from utils.mods.number import Nat, Num, Even, Odd, Pos, Neg
    from utils.mods.ip     import IPv4, IPv6
    from utils.mods.helper.types import Char, Email, Extension, PathUrl, Result
    from utils.mods.helper.http_ import Header, Params
    from utils.mods.http_ import Response, Data

