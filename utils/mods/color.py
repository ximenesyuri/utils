from typed import typed, HEX, RGB, HSL

class color:
    @typed
    def rgb_to_hex(rgb: RGB) -> HEX:
        red   = rgb[0] * 255
        green = rgb[1] * 255
        blue  = rgb[2] * 255
        return f'#{red:02x}{green:02x}{blue:02x}'

    @typed
    def hex_to_rgb(hex: HEX) -> RGB:
        hex = hex.lstrip('#')
        if len(hex) != 6:
            raise ValueError("Invalid hexadecimal color format. Expected '#RRGGBB'.")

        try:
            r = int(hex[0:2], 16)
            g = int(hex[2:4], 16)
            b = int(hex[4:6], 16)
            return (r, g, b)
        except ValueError:
            raise ValueError("Invalid hexadecimal color format. Contains non-hex characters.")

    @typed
    def rgb_to_hsl(rgb: RGB) -> HSL:
        rgb[0] /= 255.0
        rgb[1] /= 255.0
        rgb[2] /= 255.0
        max_c = max(rgb[0], rgb[1], rgb[2])
        min_c = min(rgb[0], rgb[1], rgb[2])
        l = (max_c + min_c) / 2.0

        if max_c == min_c:
            s = h = 0.0
        else:
            d = max_c - min_c
            s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
            if max_c == rgb[0]:
                h = (rgb[1] - rgb[2]) / d + (6.0 if rgb[1] < rgb[2] else 0.0)
            elif max_c == rgb[1]:
                h = (rgb[2] - rgb[0]) / d + 2.0
            elif max_c == rgb[2]:
                h = (rgb[0] - rgb[1]) / d + 4.0
            h /= 6.0
        return round(h * 360), round(s * 100), round(l * 100)

    @typed
    def hex_to_hsl(hex: HEX) -> HSL:
        def _hsl(h, s, l):
            return "{} {}% {}%".format(h, s, l)

        r, g, b = color.hex_to_rgb(hex)
        h, s, l = color.rgb_to_hsl(r, g, b)
        return _hsl(h, s, l)
