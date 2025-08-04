import inspect
from typed import typed, Function, Set, Any, Dict, Bool

@typed
def _extract_recursive_globals(func: Function) -> Set(Any):
    src = inspect.getsource(func)
    src = inspect.cleandoc(src)
    tree = ast.parse(src)
    referenced = set()
    sig = inspect.signature(func)
    for param in sig.parameters.values():
        ann = param.annotation
        if isinstance(ann, str):
            referenced.add(ann.split('.')[-1])
        elif hasattr(ann, '__name__'):
            referenced.add(ann.__name__)
        default = param.default
        if hasattr(default, '__name__'):
            referenced.add(default.__name__)
    if sig.return_annotation is not inspect._empty:
        ra = sig.return_annotation
        if isinstance(ra, str):
            referenced.add(ra.split('.')[-1])
        elif hasattr(ra, '__name__'):
            referenced.add(ra.__name__)
    class GlobalReferred(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                referenced.add(node.id)
        def visit_Attribute(self, node):
            self.generic_visit(node)
        def visit_FunctionDef(self, node):
            pass
        def visit_ClassDef(self, node):
            pass
    GlobalReferred().visit(tree)
    for param in sig.parameters.keys():
        referenced.discard(param)
    referenced -= set(__import__('builtins').__dict__.keys())
    return referenced

@typed
def _get_globals(func: Function, extra_search_modules: Bool=True) -> Dict(Any):
    base = func.__globals__.copy()
    needed = _extract_recursive_globals(func)
    missing = [name for name in needed if name not in base]
    for name in missing:
        found = False
        if name in globals():
            base[name] = globals()[name]
            continue
        if extra_search_modules:
            for mod in sys.modules.values():
                if mod and hasattr(mod, name):
                    base[name] = getattr(mod, name)
                    found = True
                    break
        if not found:
            pass
    return base
