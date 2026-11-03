import skia

from .fonts import FontManager


class Renderer:
    def __init__(self):
        self.font_manager = FontManager()
        self.default_typeface = self.font_manager.regular

        # Resource caches
        self._font_cache = {}
        self._color_cache = {}
        self._fill_paint_cache = {}
        self._stroke_paint_cache = {}
        self._shadow_paint_cache = {}

        self.default_font = self._get_font(14)

    @staticmethod
    def _store_cache(cache, key, value, max_size=256):
        """
        Store an object in a bounded cache.

        Clear the cache when it reaches its limit to avoid
        unbounded memory growth.
        """
        if len(cache) >= max_size:
            cache.clear()

        cache[key] = value
        return value

    # ---------------------------------------------------------
    # Font cache
    # ---------------------------------------------------------

    def _get_font(self, font_size):
        key = float(font_size)

        font = self._font_cache.get(key)

        if font is None:
            font = skia.Font(self.default_typeface, font_size)
            self._store_cache(self._font_cache, key, font)

        return font

    # ---------------------------------------------------------
    # Paint caches
    # ---------------------------------------------------------

    def _get_fill_paint(self, color):
        paint = self._fill_paint_cache.get(color)

        if paint is None:
            paint = skia.Paint(
                Color=color,
                AntiAlias=True,
            )

            self._store_cache(
                self._fill_paint_cache,
                color,
                paint,
            )

        return paint

    def _get_stroke_paint(self, color, width):
        key = (color, float(width))

        paint = self._stroke_paint_cache.get(key)

        if paint is None:
            paint = skia.Paint(
                Color=color,
                AntiAlias=True,
                Style=skia.Paint.kStroke_Style,
                StrokeWidth=width,
            )

            self._store_cache(
                self._stroke_paint_cache,
                key,
                paint,
            )

        return paint

    def _get_shadow_paint(self, blur):
        key = float(blur)

        paint = self._shadow_paint_cache.get(key)

        if paint is None:
            paint = skia.Paint(
                Color=skia.Color(0, 0, 0, 100),
                AntiAlias=True,
                MaskFilter=skia.MaskFilter.MakeBlur(
                    skia.kNormal_BlurStyle,
                    blur,
                ),
            )

            self._store_cache(
                self._shadow_paint_cache,
                key,
                paint,
            )

        return paint

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------

    def draw_rect(self, canvas, rect, style):
        """
        Draw a rectangle with optional background, border and radius.
        """
        x = int(rect["x"])
        y = int(rect["y"])
        w = int(rect["w"])
        h = int(rect["h"])

        radius = style.get("radius", 0)

        # Shadow
        if "shadow" in style:
            shadow_paint = self._get_shadow_paint(style["shadow"])

            shadow_rect = skia.Rect.MakeXYWH(
                x + 2,
                y + 2,
                w,
                h,
            )

            if radius > 0:
                canvas.drawRRect(
                    skia.RRect.MakeRectXY(
                        shadow_rect,
                        radius,
                        radius,
                    ),
                    shadow_paint,
                )
            else:
                canvas.drawRect(shadow_rect, shadow_paint)

        # Background
        if "bg" in style:
            bg_color = self._parse_color(style["bg"])
            paint = self._get_fill_paint(bg_color)

            rect = skia.Rect.MakeXYWH(x, y, w, h)

            if radius > 0:
                canvas.drawRRect(
                    skia.RRect.MakeRectXY(
                        rect,
                        radius,
                        radius,
                    ),
                    paint,
                )
            else:
                canvas.drawRect(rect, paint)

        # Border
        if "border_color" in style:
            border_color = self._parse_color(style["border_color"])
            border_width = style.get("border_width", 1)

            paint = self._get_stroke_paint(
                border_color,
                border_width,
            )

            rect = skia.Rect.MakeXYWH(x, y, w, h)

            if radius > 0:
                canvas.drawRRect(
                    skia.RRect.MakeRectXY(
                        rect,
                        radius,
                        radius,
                    ),
                    paint,
                )
            else:
                canvas.drawRect(rect, paint)

    def draw_text(self, canvas, text, x, y, style):
        color = self._parse_color(style.get("color", "white"))
        paint = self._get_fill_paint(color)

        font_size = style.get("font_size", 14)
        font = self._get_font(font_size)

        line_height = style.get(
            "line_height",
            font_size * 1.2,
        )

        lines = str(text).replace("\r\n", "\n").replace("\r", "\n").split("\n")

        for index, line in enumerate(lines):
            line_y = y + font_size + (index * line_height)

            canvas.drawString(
                line,
                x,
                line_y,
                font,
                paint,
            )

    def measure_text(self, text, style):
        font_size = style.get("font_size", 14)
        font = self._get_font(font_size)

        lines = str(text).replace("\r\n", "\n").replace("\r", "\n").split("\n")

        width = max(
            (font.measureText(line) for line in lines),
            default=0,
        )

        metrics = font.getMetrics()
        font_height = -metrics.fAscent + metrics.fDescent

        line_height = style.get(
            "line_height",
            font_size * 1.2,
        )

        height = font_height + (len(lines) - 1) * line_height

        return width, height

    def draw_image(self, canvas, image, rect, style):
        if not image:
            return

        src_rect = skia.Rect.MakeWH(
            float(image.width()),
            float(image.height()),
        )

        dst_rect = skia.Rect.MakeXYWH(
            float(rect["x"]),
            float(rect["y"]),
            float(rect["w"]),
            float(rect["h"]),
        )

        canvas.drawImageRect(
            image,
            src_rect,
            dst_rect,
        )

    # ---------------------------------------------------------
    # Canvas helpers
    # ---------------------------------------------------------

    def save(self, canvas):
        return canvas.save()

    def restore(self, canvas):
        canvas.restore()

    def clip_rect(self, canvas, rect):
        skia_rect = skia.Rect.MakeXYWH(
            rect["x"],
            rect["y"],
            rect["w"],
            rect["h"],
        )

        canvas.clipRect(
            skia_rect,
            skia.ClipOp.kIntersect,
            True,
        )

    # ---------------------------------------------------------
    # Color cache
    # ---------------------------------------------------------

    def _parse_color(self, color_str):
        if not isinstance(color_str, str):
            return skia.ColorWHITE

        key = color_str.casefold()

        cached = self._color_cache.get(key)

        if cached is not None:
            return cached

        color = self._resolve_color(key)

        return self._store_cache(
            self._color_cache,
            key,
            color,
        )

    @staticmethod
    def _resolve_color(color_str):
        if color_str.startswith("#"):
            hex_color = color_str.lstrip("#")

            if len(hex_color) == 3:
                hex_color = "".join(
                    character * 2
                    for character in hex_color
                )

            if len(hex_color) == 6:
                r, g, b = (
                    int(hex_color[i:i + 2], 16)
                    for i in (0, 2, 4)
                )

                return skia.Color(r, g, b)

            if len(hex_color) == 8:
                r, g, b, a = (
                    int(hex_color[i:i + 2], 16)
                    for i in (0, 2, 4, 6)
                )

                return skia.Color(r, g, b, a)

        named_colors = {
            "white": skia.ColorWHITE,
            "black": skia.ColorBLACK,
            "red": skia.ColorRED,
            "blue": skia.ColorBLUE,
            "green": skia.ColorGREEN,
        }

        return named_colors.get(
            color_str,
            skia.ColorWHITE,
        )
