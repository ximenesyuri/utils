import ast
import inspect
import textwrap
from functools import wraps, WRAPPER_ASSIGNMENTS, update_wrapper
from inspect import signature, Signature, Parameter, _empty, getsource, cleandoc
from typed import typed, Function, Set, Any, Str, Dict, Bool

@typed
def _extract_recursive_globals(func: Function) -> Set(Any):
    src = getsource(func)
    src = textwrap.dedent(src)
    tree = ast.parse(src)
    referenced = set()
    sig = signature(func)
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

@typed
def _copy_func(func: Function, **rename_map: Dict(Str)) -> Function:
    if not callable(func):
        raise TypeError("copy_function expects a function as input")

    seen = set()
    while hasattr(func, '__wrapped__') and func not in seen:
        seen.add(func)
        func = func.__wrapped__

    if not rename_map:
        def make_empty_deepcopy(f):
            newf = type(f)(
                f.__code__, f.__globals__, f.__name__,
                f.__defaults__, f.__closure__
            )
            newf.__dict__.update(f.__dict__)
            update_wrapper(newf, f)
            return newf
        return make_empty_deepcopy(func)

    src = getsource(func)
    src = textwrap.dedent(src)
    tree = ast.parse(src)

    class ParamRenamer(ast.NodeTransformer):
        def __init__(self, rename_map):
            self.rename_map = rename_map
        def visit_FunctionDef(self, node):
            for arg in node.args.args:
                if arg.arg in self.rename_map:
                    arg.arg = self.rename_map[arg.arg]
            for arg in node.args.kwonlyargs:
                if arg.arg in self.rename_map:
                    arg.arg = self.rename_map[arg.arg]
            if node.args.vararg and node.args.vararg.arg in self.rename_map:
                node.args.vararg.arg = self.rename_map[node.args.vararg.arg]
            if node.args.kwarg and node.args.kwarg.arg in self.rename_map:
                node.args.kwarg.arg = self.rename_map[node.args.kwarg.arg]
            self.generic_visit(node)
            return node
        def visit_Name(self, node):
            if node.id in self.rename_map:
                node.id = self.rename_map[node.id]
            return node
        def visit_Attribute(self, node):
            self.generic_visit(node)
            if isinstance(node.value, ast.Name) and node.value.id in self.rename_map:
                node.value.id = self.rename_map[node.value.id]
            return node
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in self.rename_map:
                node.func.id = self.rename_map[node.func.id]
            self.generic_visit(node)
            return node

    class StringDotRenamer(ast.NodeTransformer):
        def __init__(self, rename_map):
            self.rename_map = rename_map
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                for k, v in self.rename_map.items():
                    node.value = node.value.replace(f"{k}.", f"{v}.")
            return node
        def visit_Str(self, node):
            for k, v in self.rename_map.items():
                node.s = node.s.replace(f"{k}.", f"{v}.")
            return node

    tree = ParamRenamer(rename_map).visit(tree)
    tree = StringDotRenamer(rename_map).visit(tree)
    ast.fix_missing_locations(tree)

    code = compile(tree, filename="<_copy_func>", mode="exec")
    globs = _get_globals(func)
    locs = {}
    exec(code, globs, locs)
    func_name = func.__name__
    new_func = locs[func_name]
    update_wrapper(new_func, func)

    old_sig = signature(func)
    new_params = []
    new_annotations = {}
    for param in old_sig.parameters.values():
        if param.name in rename_map:
            new_name = rename_map[param.name]
            new_param = Parameter(
                new_name, kind=param.kind, default=param.default,
                annotation=param.annotation
            )
            new_params.append(new_param)
            if param.annotation is not _empty:
                new_annotations[new_name] = param.annotation
        else:
            new_params.append(param)
            if param.annotation is not _empty:
                new_annotations[param.name] = param.annotation
    new_func.__signature__ = Signature(parameters=new_params, return_annotation=old_sig.return_annotation)
    new_annotations['return'] = old_sig.return_annotation
    new_func.__annotations__ = new_annotations

    return new_func

@typed
def _eval_func(func: Function, **fixed_kwargs: Dict(Any)) -> Function:
    sig = signature(func)
    old_params = list(sig.parameters.items())

    missing = [k for k in fixed_kwargs if k not in sig.parameters]
    if missing:
        raise TypeError(
            f"{func.__name__} has no argument(s): {', '.join(missing)}"
        )

    new_params = []
    for name, param in old_params:
        if name in fixed_kwargs:
            new_param = Parameter(
                name,
                kind=param.kind,
                default=fixed_kwargs[name],
                annotation=param.annotation
            )
            new_params.append(new_param)
        else:
            new_params.append(param)

    new_sig = Signature(new_params)

    def wrapper(*args, **kwargs):
        ba = new_sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        result = func(**ba.arguments)
        return result

    wrapper.__signature__ = new_sig
    if hasattr(func, '__annotations__'):
        wrapper.__annotations__ = dict(func.__annotations__)

    return wrapper
