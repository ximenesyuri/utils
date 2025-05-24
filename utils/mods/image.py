from utils.err import ImageErr

class image:
    def download(url, path):
        import requests
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
        else:
            response.raise_for_status()

    def png_to_webp(source, target):
        try:
            from PIL import Image
            with Image.open(source) as img:
                img.save(target, 'webp')
        except Exception as e:
            raise ImageErr(e)

    def png_to_svg(source, target):
        try:
            from pixels2svg import pixels2svg
            pixels2svg(source, target, remove_background=True)
        except Exception as e:
            raise ImageErr(e)
