class _Markdown(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False
        try:
            from utils.mods.lib import lib
            lib.install('markdown')
            from markdown import markdown
            html = markdown(instance)
            return True
        except Exception as e:
            raise TypeError(e)

Markdown = _Markdown('Markdown', (Str,), {"__display__": "Markdown"})
