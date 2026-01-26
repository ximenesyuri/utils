from importlib import import_module as __import__
from typing import TYPE_CHECKING as __lsp__

__all__ = [
    'Exception',
    'NotExists',
    'AlreadyExists',
    'AlreadSet',
    'NotMatch',
    'NotSet'
]

__lazy__ = {
    "Exception":      ("utils.mods.err", "Exception"),
    "NotExists":      ("utils.mods.err", "NotExists"),
    "AlreadyExists":  ("utils.mods.err", "AlreadyExists"),
    "AlreadSet":      ("utils.mods.err", "AlreadySet"),
    "NotMatch":       ("utils.mods.err", "NotMatch"),
    "NotSet":         ("utils.mods.err", "NotSet")
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
    from utils.mods.err import Exception, AlreadyExists, AlreadySet, NotExists, NotMatch, NotSet
