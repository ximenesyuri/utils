from typed  import typed, Bool, Nill
from utils.mods.file import file
from utils.mods.lib  import lib
from utils.mods.path import Path
from utils.err import StaticErr

class static:
    @typed
    def build_scss(scss_file: Path='', css_file: Path='', minify: Bool=True) -> Nill:
        try:
            lib.install('libsass')
            import sass
            file.write(
                file=css_file,
                content=sass.compile(filename=scss_file, compress=minify)
            )
        except Exception as e:
            raise StaticErr(e)
