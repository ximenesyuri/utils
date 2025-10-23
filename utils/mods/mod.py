import importlib
import importlib.util
import sys
import ast
import inspect
from typed import typed, Any, Entry, Str, Bool, Dict, Union, Tuple, convert, TYPE, name, Nill
from utils.err import ModErr
from types import ModuleType

Module = convert(ModuleType, TYPE)

class mod:
    @typed
    def exists(module: Entry) -> Bool:
        """
        Checks if some given module entry exists.
        """
        try:
            importlib.import_module(module)
            return True
        except:
            return False

    @typed
    def get(module: Entry) -> Module:
        """
        Returns the module gect of a given module entry.
        """
        try:
            return importlib.import_module(module)
        except:
            raise ModErr(f"The required module '{module}' does not exists.") from None

    @typed
    def _is_local(obj: Any) -> Bool:
        try:
            return name(obj).startswith('_')
        except Exception as e:
            raise ModErr(e)

    @typed
    def _is_global(obj: Any) -> Bool:
        try:
            return not mod._is_local(obj)
        except Exception as e:
            raise ModErr(e)

    @typed
    def has_local(module: Entry, *locals: Tuple) -> Bool:
        """
        Checks if given locals exists in a given module entry.
        """
        for l in locals:
            if not mod._is_local(l):
                raise ModErr(f"The provided object '{l}' is not a local object.")
        return all(hasattr(mod.get(module), l) for l in locals)

    @typed
    def has_global(module: Entry, *globals: Tuple) -> Bool:
        """
        Checks if given globals exists in a given module entry.
        """
        for g in globals:
            if not mod._is_global(g):
                raise ModErr(f"The provided object '{g}' is not a global object.")
        return all(hasattr(mod.get(module), g) for g in globals)

    @typed
    def get_local(module: Entry, *locals: Tuple) -> Any:
        """
        Get some locals from a given module entry.
        """
        existing_locals = []
        for l in locals:
            if not mod._is_local(l):
                raise ModErr(f"The provided object '{l}' is not a local object.")
            if mod.has_local(module, l):
                existing_locals.append(getattr(mod.get(module), l))
        if existing_locals:
            if len(existing_locals) > 1:
                return existing_locals
            return existing_locals[0]
        else:
            raise ModErr(f"There are no locals '{locals}' in the given module '{module}'")

    @typed
    def get_global(module: Entry, *globals: Tuple) -> Any:
        """
        Get some globals from a given module entry.
        """
        existing_globals = []
        for g in globals:
            if not mod._is_global(g):
                raise ModErr(f"The provided object '{g}' is not a global object.")
            if mod.has_global(module, g):
                existing_globals.append(getattr(mod.get(module), g))
        if existing_globals:
            if len(existing_globals) > 1:
                return existing_globals
            return existing_globals[0]
        else:
            raise ModErr(f"There are no globals '{globals}' in given module '{module}'")

    @typed
    def locals(module: Entry) -> Dict:
        """
        Returns the dictionary of locals of a given module entry.
        """
        try:
            return {name: mod.get_local(module, name) for name in dir(mod.get(module)) if name.startswith('_')}
        except Exception as e:
            raise ModErr(e)

    @typed
    def globals(module: Entry) -> Dict:
        """
        Returns the dictionary of globals of a given module entry.
        """
        try:
            return {name: mod.get_global(module, name) for name in dir(mod.get(module)) if not name.startswith('_')}
        except Exception as e:
            raise ModErr(e)

    @typed
    def imports(module: Entry) -> Union(Dict(Str), Dict(Dict(Str))):
        """
        Returns the dictionary of imports of a given module entry.
        """
        try:
            if not mod.exists(module):
                raise ModErr(f"The given module '{module}' does not exists.")
            spec = importlib.util.find_spec(module)
            if not spec or not spec.origin or not spec.origin.endswith('.py'):
                raise ImportError(f"Cannot find source for module {module}")

            with open(spec.origin, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filename=spec.origin)

            imports = []

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.ImportFrom) and node.module != "__future__":
                    for alias in node.names:
                        if alias.asname:
                            imports.append((node.lineno, {node.module: {alias.name: alias.asname}}))
                        else:
                            imports.append((node.lineno, {node.module: alias.name}))
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.asname:
                            imports.append((node.lineno, {alias.name: {'': alias.asname}}))
                        else:
                            imports.append((node.lineno, {alias.name: ''}))
            return tuple(import_dict for _, import_dict in sorted(imports, key=lambda x: x[0]))
        except Exception as e:
            raise ModErr(e)

    @typed
    def import_all(module: Entry) -> Nill:
        caller_globals = sys._getframe(2).f_globals

        mod = importlib.import_module(module)
        spec = importlib.util.find_spec(module)
        if not spec or not spec.origin or not spec.origin.endswith('.py'):
            raise ImportError(f"Cannot find source for module {module}")
        with open(spec.origin, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=spec.origin)

        defined_names = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                defined_names.add(node.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            defined_names.add(target.id)
                elif isinstance(node, ast.AnnAssign):
                    if isinstance(node.target, ast.Name):
                        defined_names.add(node.target.id)
        for name in defined_names:
            if name in mod.__dict__:
                caller_globals[name] = mod.__dict__[name]
