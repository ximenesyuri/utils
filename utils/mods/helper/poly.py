from typed import typed, Dict, Any

@typed
def _union_dict(d1: Dict(Any), d2: Dict(Any)) -> Dict(Any):
    result = {}
    for k, v in d1.items():
        result[k] = v
    for k, v in d2.items():
        if k in result:
            if result[k] != v:
                raise ValueError(f"Key {k!r} has conflicting values: {result[k]!r} and {v!r}")
        else:
            result[k] = v
    return result

@typed
def _inter_dict(*dicts):
    if not dicts:
        return {}
    result = {}
    first = dicts[0]
    for k, v in first.items():
        if all(k in d and d[k] == v for d in dicts[1:]):
            result[k] = v
    return result
