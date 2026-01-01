from importlib import import_module as __import__
from typing import TYPE_CHECKING as __lsp__

__all__ = [
    "cmd",
    "json",
    "table",
    "color",
    "datetime",
    "envs",
    "path",
    "file",
    "img",
    "compress",
    "yml",
    "static",
    "lib",
    "md",
    "func",
    "text",
    "mod",
    "url",
    "sys",
    "ssh",
    "log",
    "thread",
    "cron",
    "http",
    "dt",
]

__lazy__ = {
    "cmd":       ("utils.mods.cmd",       "cmd"),
    "json":      ("utils.mods.json_",     "json"),
    "table":     ("utils.mods.table",     "table"),
    "color":     ("utils.mods.color",     "color"),
    "datetime":  ("utils.mods.datetime_", "datetime"),
    "envs":      ("utils.mods.envs",      "envs"),
    "path":      ("utils.mods.path",      "path"),
    "file":      ("utils.mods.file",      "file"),
    "img":       ("utils.mods.img",       "img"),
    "compress":  ("utils.mods.compress",  "compress"),
    "yml":       ("utils.mods.yml",       "yml"),
    "static":    ("utils.mods.static",    "static"),
    "lib":       ("utils.mods.lib",       "lib"),
    "md":        ("utils.mods.md",        "md"),
    "func":      ("utils.mods.func",      "func"),
    "text":      ("utils.mods.text",      "text"),
    "mod":       ("utils.mods.mod",       "mod"),
    "url":       ("utils.mods.url",       "url"),
    "sys":       ("utils.mods.sys",       "sys"),
    "ssh":       ("utils.mods.ssh",       "ssh"),
    "log":       ("utils.mods.log",       "log"),
    "thread":    ("utils.mods.thread",    "thread"),
    "cron":      ("utils.mods.cron",      "cron"),
    "http":      ("utils.mods.http",      "http"),
    # alias: dt = datetime
    "dt":        ("utils.mods.datetime_", "datetime"),
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
    from utils.mods.cmd       import cmd       as cmd
    from utils.mods.json_     import json      as json
    from utils.mods.table     import table     as table
    from utils.mods.color     import color     as color
    from utils.mods.datetime_ import datetime  as datetime
    from utils.mods.envs      import envs      as envs
    from utils.mods.path      import path      as path
    from utils.mods.file      import file      as file
    from utils.mods.img       import img       as img
    from utils.mods.compress  import compress  as compress
    from utils.mods.yml       import yml       as yml
    from utils.mods.static    import static    as static
    from utils.mods.lib       import lib       as lib
    from utils.mods.md        import md        as md
    from utils.mods.func      import func      as func
    from utils.mods.text      import text      as text
    from utils.mods.mod       import mod       as mod
    from utils.mods.url       import url       as url
    from utils.mods.sys       import sys       as sys
    from utils.mods.ssh       import ssh       as ssh
    from utils.mods.log       import log       as log
    from utils.mods.thread    import thread    as thread
    from utils.mods.cron      import cron      as cron
    from utils.mods.http      import http      as http
    dt = datetime

