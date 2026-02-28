from typed import typed, Prod, Interval, Range, Regex, Float, Typed, List, Tuple, Union, Enum, Int, Str
from math import sqrt, atan2, cos, sin, degrees, radians
from utils.mods.helper.color import _clamp

RGB = Prod(Range(0, 255), 3)
HEX = Regex(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
HSL = Prod(Range(0, 360), Range(0, 100), Range(0, 100))
HSV = Prod(Range(0, 360), Range(0, 100), Range(0, 100))
XYZ = Prod(Float, 3)

RGBA = Prod(Range(0, 255), 4)
HSVA = Prod(Range(0, 360), Range(0, 100), Range(0, 100), Range(0, 100))
CMYK = Prod(Range(0, 100), 4)
LAB = Prod(
    Union(Interval(Int, 0, 100),    Interval(Float, 0.0, 100.0)),
    Union(Interval(Int, -128, 127), Interval(Float, -128.0, 127.0)),
    Union(Interval(Int, -128, 127), Interval(Float, -128.0, 127.0))
)
LCH = Prod(Range(0, 100), Range(0, 180), Range(0, 360))

Color = Union(RGB, HEX, HSL, HSV, XYZ, RGBA, HSVA, CMYK, LAB, LCH)
ColorDistance = Enum(Str, "euclidean", "weighted", "delta", "hsv")

RGB.__display__ = "RGB"
HEX.__display__ = "HEX"
HSL.__display__ = "HSL"
HSV.__display__ = "HSV"
XYZ.__display__ = "XYZ"

RGBA.__display__  = "RGBA"
HSVA.__display__  = "HSVA"
CMYK.__display__  = "CMYK"
LAB.__display__   = "LAB"
LCH.__display__ = "LCH"

Color.__display__ = "Color"

class ColorErr(Exception): pass
typed = typed(enclose=ColorErr)

### TODO ###
# Extend color.sort and color.distance to receive 
# a generic Color instead of only HEX colors
###########

class color:
    @typed
    def sort(base: HEX, colors: List(HEX), method: Typed(HEX, cod=Float)):
        return sorted(colors, key=lambda c: method(base, c))

    class convert:
        class rgb:
            @typed
            def to_hex(rgb: RGB) -> HEX:
                r, g, b = rgb
                return f"#{r:02x}{g:02x}{b:02x}"

            @typed
            def to_hsl(rgb: RGB) -> HSL:
                r, g, b = rgb
                r /= 255.0
                g /= 255.0
                b /= 255.0

                max_c = max(r, g, b)
                min_c = min(r, g, b)
                l = (max_c + min_c) / 2.0

                if max_c == min_c:
                    h = 0.0
                    s = 0.0
                else:
                    d = max_c - min_c
                    s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
                    if max_c == r:
                        h = (g - b) / d + (6.0 if g < b else 0.0)
                    elif max_c == g:
                        h = (b - r) / d + 2.0
                    else:
                        h = (r - g) / d + 4.0
                    h /= 6.0

                H = int(round(h * 360.0)) % 360
                S = int(round(s * 100.0))
                L = int(round(l * 100.0))
                S = _clamp(S, 0, 100)
                L = _clamp(L, 0, 100)
                return (H, S, L)

            @typed
            def to_hsv(rgb: RGB) -> HSV:
                r, g, b = rgb
                r /= 255.0
                g /= 255.0
                b /= 255.0

                max_c = max(r, g, b)
                min_c = min(r, g, b)
                v = max_c
                d = max_c - min_c

                if max_c == 0:
                    s = 0.0
                else:
                    s = d / max_c

                if d == 0:
                    h = 0.0
                else:
                    if max_c == r:
                        h = (g - b) / d + (6.0 if g < b else 0.0)
                    elif max_c == g:
                        h = (b - r) / d + 2.0
                    else:
                        h = (r - g) / d + 4.0
                    h /= 6.0

                H = int(round(h * 360.0)) % 360
                S = _clamp(int(round(s * 100.0)), 0, 100)
                V = _clamp(int(round(v * 100.0)), 0, 100)
                return (H, S, V)

            @typed
            def to_cmyk(rgb: RGB) -> CMYK:
                r, g, b = rgb
                if (r, g, b) == (0, 0, 0):
                    return (0, 0, 0, 100)

                r /= 255.0
                g /= 255.0
                b /= 255.0

                k = 1.0 - max(r, g, b)
                c = (1.0 - r - k) / (1.0 - k)
                m = (1.0 - g - k) / (1.0 - k)
                y = (1.0 - b - k) / (1.0 - k)

                C = _clamp(int(round(c * 100.0)), 0, 100)
                M = _clamp(int(round(m * 100.0)), 0, 100)
                Y = _clamp(int(round(y * 100.0)), 0, 100)
                K = _clamp(int(round(k * 100.0)), 0, 100)
                return (C, M, Y, K)

            @typed
            def to_xyz(rgb: RGB) -> XYZ:
                r, g, b = rgb
                r /= 255.0
                g /= 255.0
                b /= 255.0

                def inv_gamma(c):
                    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

                r = inv_gamma(r)
                g = inv_gamma(g)
                b = inv_gamma(b)

                x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
                y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
                z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

                return (x, y, z)

            @typed
            def to_lab(rgb: RGB) -> LAB:
                xyz = color.convert.rgb.to_xyz(rgb)
                return color.convert.xyz.to_lab(xyz)

        class hex:
            @typed
            def to_rgb(hex_value: HEX) -> RGB:
                s = hex_value.lstrip("#")
                if len(s) == 3:
                    s = "".join(ch * 2 for ch in s)
                if len(s) != 6:
                    raise ValueError("Invalid hexadecimal color format. Expected '#RRGGBB' or '#RGB'.")
                try:
                    r = int(s[0:2], 16)
                    g = int(s[2:4], 16)
                    b = int(s[4:6], 16)
                    return (r, g, b)
                except ValueError:
                    raise ValueError("Invalid hexadecimal color format. Contains non-hex characters.")

            @typed
            def to_hsl(hex_value: HEX) -> HSL:
                rgb = color.convert.hex.to_rgb(hex_value)
                return color.convert.rgb.to_hsl(rgb)

            @typed
            def to_hsv(hex_value: HEX) -> HSV:
                rgb = color.convert.hex.to_rgb(hex_value)
                return color.convert.rgb.to_hsv(rgb)

            @typed
            def to_cmyk(hex_value: HEX) -> CMYK:
                rgb = color.convert.hex.to_rgb(hex_value)
                return color.convert.rgb.to_cmyk(rgb)

            @typed
            def to_xyz(hex_value: HEX) -> XYZ:
                rgb = color.convert.hex.to_rgb(hex_value)
                return color.convert.rgb.to_xyz(rgb)

            @typed
            def to_lab(hex_value: HEX) -> LAB:
                rgb = color.convert.hex.to_rgb(hex_value)
                return color.convert.rgb.to_lab(rgb)

        class hsl:
            @typed
            def to_rgb(hsl: HSL) -> RGB:
                h, s, l = hsl
                h = (h % 360) / 360.0
                s /= 100.0
                l /= 100.0

                def hue_to_rgb(p, q, t):
                    if t < 0:
                        t += 1
                    if t > 1:
                        t -= 1
                    if t < 1 / 6:
                        return p + (q - p) * 6 * t
                    if t < 1 / 2:
                        return q
                    if t < 2 / 3:
                        return p + (q - p) * (2 / 3 - t) * 6
                    return p

                if s == 0:
                    r = g = b = l
                else:
                    q = l * (1 + s) if l < 0.5 else l + s - l * s
                    p = 2 * l - q
                    r = hue_to_rgb(p, q, h + 1 / 3)
                    g = hue_to_rgb(p, q, h)
                    b = hue_to_rgb(p, q, h - 1 / 3)

                R = _clamp(int(round(r * 255.0)), 0, 255)
                G = _clamp(int(round(g * 255.0)), 0, 255)
                B = _clamp(int(round(b * 255.0)), 0, 255)
                return (R, G, B)

            @typed
            def to_hex(hsl: HSL) -> HEX:
                rgb = color.convert.hsl.to_rgb(hsl)
                return color.convert.rgb.to_hex(rgb)

            @typed
            def to_hsv(hsl: HSL) -> HSV:
                rgb = color.convert.hsl.to_rgb(hsl)
                return color.convert.rgb.to_hsv(rgb)

            @typed
            def to_cmyk(hsl: HSL) -> CMYK:
                rgb = color.convert.hsl.to_rgb(hsl)
                return color.convert.rgb.to_cmyk(rgb)

            @typed
            def to_xyz(hsl: HSL) -> XYZ:
                rgb = color.convert.hsl.to_rgb(hsl)
                return color.convert.rgb.to_xyz(rgb)

            @typed
            def to_lab(hsl: HSL) -> LAB:
                rgb = color.convert.hsl.to_rgb(hsl)
                return color.convert.rgb.to_lab(rgb)

        class hsv:
            @typed
            def to_rgb(hsv: HSV) -> RGB:
                h, s, v = hsv
                h = (h % 360) / 60.0
                s /= 100.0
                v /= 100.0

                if s == 0:
                    r = g = b = v
                else:
                    i = int(h) % 6
                    f = h - i
                    p = v * (1 - s)
                    q = v * (1 - s * f)
                    t = v * (1 - s * (1 - f))

                    if i == 0:
                        r, g, b = v, t, p
                    elif i == 1:
                        r, g, b = q, v, p
                    elif i == 2:
                        r, g, b = p, v, t
                    elif i == 3:
                        r, g, b = p, q, v
                    elif i == 4:
                        r, g, b = t, p, v
                    else:
                        r, g, b = v, p, q

                R = _clamp(int(round(r * 255.0)), 0, 255)
                G = _clamp(int(round(g * 255.0)), 0, 255)
                B = _clamp(int(round(b * 255.0)), 0, 255)
                return (R, G, B)

            @typed
            def to_hex(hsv: HSV) -> HEX:
                rgb = color.convert.hsv.to_rgb(hsv)
                return color.convert.rgb.to_hex(rgb)

            @typed
            def to_hsl(hsv: HSV) -> HSL:
                rgb = color.convert.hsv.to_rgb(hsv)
                return color.convert.rgb.to_hsl(rgb)

            @typed
            def to_cmyk(hsv: HSV) -> CMYK:
                rgb = color.convert.hsv.to_rgb(hsv)
                return color.convert.rgb.to_cmyk(rgb)

            @typed
            def to_xyz(hsv: HSV) -> XYZ:
                rgb = color.convert.hsv.to_rgb(hsv)
                return color.convert.rgb.to_xyz(rgb)

            @typed
            def to_lab(hsv: HSV) -> LAB:
                rgb = color.convert.hsv.to_rgb(hsv)
                return color.convert.rgb.to_lab(rgb)

        class cmyk:
            @typed
            def to_rgb(cmyk: CMYK) -> RGB:
                c, m, y, k = cmyk
                c /= 100.0
                m /= 100.0
                y /= 100.0
                k /= 100.0

                r = 255.0 * (1.0 - c) * (1.0 - k)
                g = 255.0 * (1.0 - m) * (1.0 - k)
                b = 255.0 * (1.0 - y) * (1.0 - k)

                R = _clamp(int(round(r)), 0, 255)
                G = _clamp(int(round(g)), 0, 255)
                B = _clamp(int(round(b)), 0, 255)
                return (R, G, B)

            @typed
            def to_hex(cmyk: CMYK) -> HEX:
                rgb = color.convert.cmyk.to_rgb(cmyk)
                return color.convert.rgb.to_hex(rgb)

            @typed
            def to_hsl(cmyk: CMYK) -> HSL:
                rgb = color.convert.cmyk.to_rgb(cmyk)
                return color.convert.rgb.to_hsl(rgb)

            @typed
            def to_hsv(cmyk: CMYK) -> HSV:
                rgb = color.convert.cmyk.to_rgb(cmyk)
                return color.convert.rgb.to_hsv(rgb)

            @typed
            def to_xyz(cmyk: CMYK) -> XYZ:
                rgb = color.convert.cmyk.to_rgb(cmyk)
                return color.convert.rgb.to_xyz(rgb)

            @typed
            def to_lab(cmyk: CMYK) -> LAB:
                rgb = color.convert.cmyk.to_rgb(cmyk)
                return color.convert.rgb.to_lab(rgb)

        class xyz:
            @typed
            def to_rgb(xyz: XYZ) -> RGB:
                x, y, z = xyz

                r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
                g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
                b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

                def gamma(c):
                    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055

                r = gamma(r)
                g = gamma(g)
                b = gamma(b)

                R = _clamp(int(round(r * 255.0)), 0, 255)
                G = _clamp(int(round(g * 255.0)), 0, 255)
                B = _clamp(int(round(b * 255.0)), 0, 255)
                return (R, G, B)

            @typed
            def to_hex(xyz: XYZ) -> HEX:
                rgb = color.convert.xyz.to_rgb(xyz)
                return color.convert.rgb.to_hex(rgb)

            @typed
            def to_hsl(xyz: XYZ) -> HSL:
                rgb = color.convert.xyz.to_rgb(xyz)
                return color.convert.rgb.to_hsl(rgb)

            @typed
            def to_hsv(xyz: XYZ) -> HSV:
                rgb = color.convert.xyz.to_rgb(xyz)
                return color.convert.rgb.to_hsv(rgb)

            @typed
            def to_cmyk(xyz: XYZ) -> CMYK:
                rgb = color.convert.xyz.to_rgb(xyz)
                return color.convert.rgb.to_cmyk(rgb)

            @typed
            def to_lab(xyz: XYZ) -> LAB:
                x, y, z = xyz

                Xn, Yn, Zn = 0.95047, 1.00000, 1.08883

                x /= Xn
                y /= Yn
                z /= Zn

                def f(t):
                    return t ** (1.0 / 3.0) if t > 0.008856 else (7.787 * t + 16.0 / 116.0)

                fx = f(x)
                fy = f(y)
                fz = f(z)

                L = 116.0 * fy - 16.0
                a = 500.0 * (fx - fy)
                b = 200.0 * (fy - fz)

                L_i = _clamp(int(round(L)), 0, 100)
                a_i = _clamp(int(round(a)), -128, 127)
                b_i = _clamp(int(round(b)), -128, 127)
                return (L_i, a_i, b_i)

        class lab:
            @typed
            def to_xyz(lab: LAB) -> XYZ:
                L, a, b = lab

                Xn, Yn, Zn = 0.95047, 1.00000, 1.08883

                fy = (L + 16.0) / 116.0
                fx = fy + a / 500.0
                fz = fy - b / 200.0

                def f_inv(t):
                    t3 = t ** 3.0
                    return t3 if t3 > 0.008856 else (t - 16.0 / 116.0) / 7.787

                x = f_inv(fx) * Xn
                y = f_inv(fy) * Yn
                z = f_inv(fz) * Zn

                return (x, y, z)

            @typed
            def to_rgb(lab: LAB) -> RGB:
                xyz = color.convert.lab.to_xyz(lab)
                return color.convert.xyz.to_rgb(xyz)

            @typed
            def to_lch(lab: LAB) -> LCH:
                L, a, b = lab
                C = sqrt(a * a + b * b)
                h = degrees(atan2(b, a))
                if h < 0:
                    h += 360.0

                L_i = _clamp(int(round(L)), 0, 100)
                C_i = _clamp(int(round(C)), 0, 180)
                h_i = _clamp(int(round(h)) % 360, 0, 360)
                return (L_i, C_i, h_i)

            @typed
            def to_hex(lab: LAB) -> HEX:
                rgb = color.convert.lab.to_rgb(lab)
                return color.convert.rgb.to_hex(rgb)

            @typed
            def to_hsl(lab: LAB) -> HSL:
                rgb = color.convert.lab.to_rgb(lab)
                return color.convert.rgb.to_hsl(rgb)

            @typed
            def to_hsv(lab: LAB) -> HSV:
                rgb = color.convert.lab.to_rgb(lab)
                return color.convert.rgb.to_hsv(rgb)

            @typed
            def to_cmyk(lab: LAB) -> CMYK:
                rgb = color.convert.lab.to_rgb(lab)
                return color.convert.rgb.to_cmyk(rgb)

        class lch:
            @typed
            def to_lab(lch: LCH) -> LAB:
                L, C, h = lch
                rad = radians(h)
                a = C * cos(rad)
                b = C * sin(rad)

                L_i = _clamp(int(round(L)), 0, 100)
                a_i = _clamp(int(round(a)), -128, 127)
                b_i = _clamp(int(round(b)), -128, 127)
                return (L_i, a_i, b_i)

            @typed
            def to_rgb(lch: LCH) -> RGB:
                lab = color.convert.lch.to_lab(lch)
                return color.convert.lab.to_rgb(lab)

            @typed
            def to_hex(lch: LCH) -> HEX:
                lab = color.convert.lch.to_lab(lch)
                return color.convert.lab.to_hex(lab)

            @typed
            def to_hsl(lch: LCH) -> HSL:
                lab = color.convert.lch.to_lab(lch)
                return color.convert.lab.to_hsl(lab)

            @typed
            def to_hsv(lch: LCH) -> HSV:
                lab = color.convert.lch.to_lab(lch)
                return color.convert.lab.to_hsv(lab)

            @typed
            def to_cmyk(lch: LCH) -> CMYK:
                lab = color.convert.lch.to_lab(lch)
                return color.convert.lab.to_cmyk(lab)

            @typed
            def to_xyz(lch: LCH) -> XYZ:
                lab = color.convert.lch.to_lab(lch)
                return color.convert.lab.to_xyz(lab)

    class distance:
        @typed
        def euclidean(c1: HEX, c2: HEX) -> Float:
            rgb1 = color.convert.hex.to_rgb(c1)
            rgb2 = color.convert.hex.to_rgb(c2)
            return sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

        @typed
        def weighted(c1: HEX, c2: HEX) -> Float:
            r1, g1, b1 = color.convert.hex.to_rgb(c1)
            r2, g2, b2 = color.convert.hex.to_rgb(c2)

            return sqrt(
                0.3 * (r1 - r2) ** 2 +
                0.59 * (g1 - g2) ** 2 +
                0.11 * (b1 - b2) ** 2
            )

        @typed
        def delta(c1: HEX, c2: HEX) -> Float:
            rgb1 = color.convert.hex.to_rgb(c1)
            rgb2 = color.convert.hex.to_rgb(c2)

            lab1 = color.convert.rgb.rgb_to_lab(rgb1)
            lab2 = color.convert.rgb.rgb_to_lab(rgb2)

            L1, a1, b1 = lab1
            L2, a2, b2 = lab2
            return sqrt(
                (L1 - L2) ** 2 +
                (a1 - a2) ** 2 +
                (b1 - b2) ** 2
            )

        @typed
        def hsv(c1: HEX, c2: HEX) -> Float:
            hsv1 = color.convert.hex.to_hsv(c1)
            hsv2 = color.convert.hex.to_hsv(c2)

            h1, S1, V1 = hsv1
            h2, S2, V2 = hsv2

            s1, v1 = S1 / 100.0, V1 / 100.0
            s2, v2 = S2 / 100.0, V2 / 100.0

            dh = abs(h1 - h2)
            h_diff = min(dh, 360.0 - dh)

            return sqrt(
                (h_diff / 360.0 * 255.0) ** 2 +
                (s1 - s2) ** 2 +
                (v1 - v2) ** 2
            )

    class average:
        @typed
        def euclidean(*colors: Tuple(HEX)) -> HEX:
            if not colors:
                raise ColorErr("color.average.euclidean requires at least one color")

            rgbs = [color.convert.hex.to_rgb(c) for c in colors]
            n = len(rgbs)
            r_avg = int(round(sum(r for r, g, b in rgbs) / n))
            g_avg = int(round(sum(g for r, g, b in rgbs) / n))
            b_avg = int(round(sum(b for r, g, b in rgbs) / n))

            return color.convert.rgb.to_hex((r_avg, g_avg, b_avg))

        @typed
        def weighted(*colors: Tuple(HEX)) -> HEX:
            if not colors:
                raise ColorErr("color.average.weighted requires at least one color")

            rgbs = [color.convert.hex.to_rgb(c) for c in colors]
            n = len(rgbs)
            r_avg = int(round(sum(r for r, g, b in rgbs) / n))
            g_avg = int(round(sum(g for r, g, b in rgbs) / n))
            b_avg = int(round(sum(b for r, g, b in rgbs) / n))

            return color.convert.rgb.to_hex((r_avg, g_avg, b_avg))

        @typed
        def delta(*colors: Tuple(HEX)) -> HEX:
            if not colors:
                raise ColorErr("color.average.delta requires at least one color")

            labs = [color.convert.hex.to_lab(c) for c in colors]
            n = len(labs)

            L_avg = sum(L for L, a, b in labs) / n
            a_avg = sum(a for L, a, b in labs) / n
            b_avg = sum(b for L, a, b in labs) / n

            lab_centroid = (L_avg, a_avg, b_avg)
            return color.convert.lab.to_hex(lab_centroid)  # uses internal clamping

        @typed
        def hsv(*colors: Tuple(HEX)) -> HEX:
            if not colors:
                raise ColorErr("color.average.hsv requires at least one color")

            hsvs = [color.convert.hex.to_hsv(c) for c in colors]
            n = len(hsvs)

            sum_cos = 0.0
            sum_sin = 0.0
            S_sum = 0.0
            V_sum = 0.0

            for H, S, V in hsvs:
                rad = radians(H % 360)
                sum_cos += cos(rad)
                sum_sin += sin(rad)
                S_sum += S
                V_sum += V

            if n == 1:
                H_avg = hsvs[0][0]
            else:
                H_rad = atan2(sum_sin / n, sum_cos / n)
                if H_rad < 0:
                    H_rad += 2.0 * 3.141592653589793
                H_avg = int(round(degrees(H_rad))) % 360

            S_avg = _clamp(int(round(S_sum / n)), 0, 100)
            V_avg = _clamp(int(round(V_sum / n)), 0, 100)

            return color.convert.hsv.to_hex((H_avg, S_avg, V_avg))
