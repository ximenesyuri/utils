import os
from typed import typed, Path, Nill, Maybe, Url, File
from utils.mods.lib import lib
from utils.err import ImgErr

class img:
    @typed
    def download(url: Url("http", "https")='https://', path: Maybe(Path)=Nill) -> Nill:
        try:
            lib.install('requests')
            import requests
            response = requests.get(url)
            if response.status_code == 200:
                if not path:
                    path = os.getcwd()
                with open(path, 'wb') as file:
                    file.write(response.content)
            else:
                response.raise_for_status()
        except Exception as e:
            raise ImgErr(e)

    @typed
    def png_to_webp(source: File='', target: Maybe(Path)=Nill) -> Nill:
        try:
            if not target:
                from utils.mods.path import path
                parent   = path.parent(source)
                filename = path.filename(path.basename(source))
                target   = path.join(parent, f'{filename}.webp')
            from PIL import Image
            with Image.open(source) as image:
                image.save(target, 'webp')
        except Exception as e:
            raise ImgErr(e)

    def png_to_svg(source: File="", target: Maybe(Path)=Nill) -> Nill:
        try:
            if not target:
                from utils.mods.path import path
                parent   = path.parent(source)
                filename = path.filename(path.basename(source))
                target   = path.join(parent, f'{filename}.svg')
            lib.install('pixels2svg')
            from pixels2svg import pixels2svg
            pixels2svg(source, target, remove_background=True)
        except Exception as e:
            raise ImgErr(e)
