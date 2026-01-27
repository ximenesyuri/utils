from importlib import import_module as __import__
from typing import TYPE_CHECKING as __lsp__

__all__ = [
    'Exception',
    'AlreadyExists',     'NotExists',
    'AlreadSet',         'NotSet'
    'AlredyDefined',     'NotDefined',
    'AlreadyRegistered', 'NotRegistered',
    'AlreadyConnected',  'NotConnected',

    'NotMatch', 'NotFound'
]

__lazy__ = {
    "Exception":         ("utils.mods.err", "Exception"),
    "AlreadyExists":     ("utils.mods.err", "AlreadyExists"),
    "NotExists":         ("utils.mods.err", "NotExists"),
    "AlreadSet":         ("utils.mods.err", "AlreadySet"),
    "NotSet":            ("utils.mods.err", "NotSet"),
    "AlreadyDefined":    ("utils.mods.err", "AlreadyDefined"),
    "NotDefined":        ("utils.mods.err", "NotDefined"),
    "AlreadyRegistered": ("utils.mods.err", "AlreadyRegistered"),
    "NotRegistred":      ("utils.mods.err", "NotRegistered"),
    "AlreadyConnected":  ("utils.mods.err", "AlreadyConnected"),
    "NotConnected":      ("utils.mods.err", "NotConnected"),

    "NotMatch":          ("utils.mods.err", "NotMatch"),
    "NotFound":          ("utils.mods.err", "NotFound")
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

if __lazy__:
    from utils.mods.err import (
        Exception,
        AlreadyExists,     NotExists,
        AlreadySet,        NotSet,
        AlreadyDefined,    NotDefined,
        AlreadyRegistered, NotRegistered,
        AlreadyConnected,  NotConnected,
        NotMatch, NotFound
    )
