from importlib import import_module as __import__
from typing import TYPE_CHECKING as __lsp__

__all__ = [
    'lazy',
    'Message',
    'Result'
]

__lazy__ = {
    "lazy":      ("utils.mods.general", "lazy"),
    "Message":   ("utils.mods.general", "Message"),
    "Result":    ("utils.mods.general", "Result"),
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
    from utils.mods.general import lazy, Message, Result
