import importlib
import sys
from typing import TYPE_CHECKING as __lsp__

def lazy(imports):
    caller_globals = sys._getframe(1).f_globals
    caller_name = caller_globals.get("__name__", "<unknown>")

    all_names = list(imports.keys())
    caller_globals["__all__"] = all_names

    lazy_map = {}
    for name, module_path in imports.items():
        if name == "dt" and "datetime" in imports and imports["datetime"] == module_path:
            lazy_map[name] = (imports["datetime"], "datetime")
        else:
            lazy_map[name] = (module_path, name)

    caller_globals["__lazy__"] = lazy_map

    def __getattr__(name):
        try:
            module_name, attr_name = caller_globals["__lazy__"][name]
        except KeyError:
            raise AttributeError(
                f"module {caller_name!r} has no attribute {name!r}"
            ) from None

        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name)
        caller_globals[name] = attr
        return attr

    def __dir__():
        return sorted(set(caller_globals.keys()) | set(caller_globals["__all__"]))

    caller_globals["__getattr__"] = __getattr__
    caller_globals["__dir__"] = __dir__

    return __lsp__

class _Checker:
    def __init__(self, values, aggregator):
        self.values = values
        self.aggregator = aggregator

    def _evaluate_comparison(self, op, other):
        results = []
        errors = []

        for value in self.values:
            try:
                result = op(value, other)
                results.append(result)
            except Exception as e:
                errors.append(e)
        if len(errors) == len(self.values) and len(self.values) > 0:
            raise errors[0]
        return self.aggregator(results) if results else False

    def __eq__(self, other):
        return self._evaluate_comparison(lambda x, y: x == y, other)

    def __ne__(self, other):
        return self._evaluate_comparison(lambda x, y: x != y, other)

    def __lt__(self, other):
        return self._evaluate_comparison(lambda x, y: x < y, other)

    def __le__(self, other):
        return self._evaluate_comparison(lambda x, y: x <= y, other)

    def __gt__(self, other):
        return self._evaluate_comparison(lambda x, y: x > y, other)

    def __ge__(self, other):
        return self._evaluate_comparison(lambda x, y: x >= y, other)

    def __contains__(self, item):
        results = []
        errors = []

        for value in self.values:
            try:
                result = item in value
                results.append(result)
            except Exception as e:
                errors.append(e)

        if len(errors) == len(self.values) and len(self.values) > 0:
            raise errors[0]

        return self.aggregator(results) if results else False

    def is_(self, other):
        results = [x is other for x in self.values]
        return self.aggregator(results)

    def is_not(self, other):
        results = [x is not other for x in self.values]
        return self.aggregator(results)

class Checker:
    def __init__(self, aggregator):
        self.aggregator = aggregator

    def __call__(self, *args):
        return _Checker(args, self.aggregator)

some = Checker(any)
every = Checker(all)
