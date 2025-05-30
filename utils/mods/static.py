from typed  import typed, Bool, Path, Nill
from utils.mods.file import file

class static:
    @typed
    def build_scss(scss_file: Path, css_file: Path, minify: Bool) -> Nill:
        import sass
        file.write(
            file=css_file,
            content=sass.compile(filename=scss_file, compress=minify)
        )
