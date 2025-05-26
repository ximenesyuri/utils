from utils.types import Path
from utils.mods.file import file

class static:
    def build_scss(scss_file: Path, css_file: Path, minify: bool) -> None:
        import sass
        file.write(
            file=css_file,
            content=sass.compile(filename=scss_file, compress=minify)
        )
