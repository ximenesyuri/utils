import importlib
from typed import typed, Any, Entry, Bool, Dict, Tuple, convert, TYPE, name
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
