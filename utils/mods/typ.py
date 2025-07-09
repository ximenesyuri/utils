from typed import TYPE, Nill, Any

class typ:
    def get(typ: TYPE=Nill, attr: Str="") -> Any:
        return getattr(typ, attr)

    def set(typ: TYPE=Nill, name: Str="", value: Any=None) -> Nill:
        try:
            return setattr(typ, name, value)
        except Exception as e:
            raise TypErr(e)

    def prop(typ: Type=Nill, prop: Str="", func: PlainFuncType=None) -> Nill:
        try:
            return setattr(typ, name, value)
        except Exception as e:
            raise TypErr(e)

