import skia

class Renderer:
    def __init__(self):
        self.default_typeface = skia.Typeface('Arial')
        self.default_font = skia.Font(self.default_typeface, 14)

    def draw_rect(self, canvas, rect, style):
        """
        Draws a rectangle with optional background, border, and radius.
        rect: {'x': float, 'y': float, 'w': float, 'h': float}
        style: dict
        """
        x, y, w, h = int(rect['x']), int(rect['y']), int(rect['w']), int(rect['h'])
        radius = style.get('radius', 0)
        
        # Draw Shadow
        if 'shadow' in style:
            shadow_blur = style['shadow']
            shadow_paint = skia.Paint(
                Color=skia.Color(0, 0, 0, 100),
                AntiAlias=True,
                MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, shadow_blur)
            )
            shadow_rect = skia.Rect.MakeXYWH(x + 2, y + 2, w, h)
            if radius > 0:
                canvas.drawRRect(skia.RRect.MakeRectXY(shadow_rect, radius, radius), shadow_paint)
            else:
                canvas.drawRect(shadow_rect, shadow_paint)

        # Draw Background
        if 'bg' in style:
            bg_color = self._parse_color(style['bg'])
            paint = skia.Paint(Color=bg_color, AntiAlias=True)
            
            if radius > 0:
                rrect = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), radius, radius)
                canvas.drawRRect(rrect, paint)
            else:
                canvas.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint)

        # Draw Border
        if 'border_color' in style:
            border_color = self._parse_color(style['border_color'])
            border_width = style.get('border_width', 1)
            paint = skia.Paint(
                Color=border_color, 
                AntiAlias=True,
                Style=skia.Paint.kStroke_Style,
                StrokeWidth=border_width
            )
            
            if radius > 0:
                rrect = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), radius, radius)
                canvas.drawRRect(rrect, paint)
            else:
                canvas.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint)

    def draw_text(self, canvas, text, x, y, style):
        """
        Draws text.
        """
        color = self._parse_color(style.get('color', 'white'))
        paint = skia.Paint(Color=color, AntiAlias=True)
        
        # Font handling
        font_size = style.get('font_size', 14)
        font = skia.Font(self.default_typeface, font_size)
        
        # Draw text (Skia draws from baseline, so we might need adjustment if x,y is top-left)
        # For now assuming simple baseline drawing or that layout handles it.
        # But typically we want to draw at x, y+ascent.
        # Let's stick to simple drawing for now as per previous working version.
        canvas.drawString(text, x, y + font_size, font, paint)

    def measure_text(self, text, style):
        font_size = style.get('font_size', 14)
        font = skia.Font(self.default_typeface, font_size)
        width = font.measureText(text)
        metrics = font.getMetrics()
        height = -metrics.fAscent + metrics.fDescent
        return width, height

    def draw_image(self, canvas, image, rect, style):
        if not image: return
        
        # Ensure floats
        w = float(image.width())
        h = float(image.height())
        src_rect = skia.Rect.MakeWH(w, h)
        
        dx = float(rect['x'])
        dy = float(rect['y'])
        dw = float(rect['w'])
        dh = float(rect['h'])
        dst_rect = skia.Rect.MakeXYWH(dx, dy, dw, dh)
        
        # Try without paint first
        # Try without paint first
        canvas.drawImageRect(image, src_rect, dst_rect)

    def save(self, canvas):
        return canvas.save()

    def restore(self, canvas):
        canvas.restore()

    def clip_rect(self, canvas, rect):
        """
        rect: {'x': float, 'y': float, 'w': float, 'h': float}
        """
        skia_rect = skia.Rect.MakeXYWH(rect['x'], rect['y'], rect['w'], rect['h'])
        canvas.clipRect(skia_rect, skia.ClipOp.kIntersect, True)

    def _parse_color(self, color_str):
        if isinstance(color_str, str):
            if color_str.startswith('#'):
                hex_color = color_str.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = "".join(c*2 for c in hex_color)
                
                if len(hex_color) == 6:
                    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    return skia.Color(r, g, b)
                elif len(hex_color) == 8:
                    r, g, b, a = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
                    return skia.Color(r, g, b, a)
            elif color_str.lower() == 'white': return skia.ColorWHITE
            elif color_str.lower() == 'black': return skia.ColorBLACK
            elif color_str.lower() == 'red': return skia.ColorRED
            elif color_str.lower() == 'blue': return skia.ColorBLUE
            elif color_str.lower() == 'green': return skia.ColorGREEN
        
        return skia.ColorWHITE
