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
        x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
        radius = style.get('radius', 0)
        
        # Draw Shadow
        if 'shadow' in style:
            shadow_blur = style['shadow']
            # Simple shadow implementation
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

        # Draw Border (optional, can add later)

    def draw_text(self, canvas, text, x, y, style):
        """
        Draws text.
        """
        color = self._parse_color(style.get('color', 'white'))
        paint = skia.Paint(Color=color, AntiAlias=True)
        
        # Font handling
        font_size = style.get('font_size', 14)
        # Simple font cache or creation could go here
        font = skia.Font(self.default_typeface, font_size)
        
        # Adjust y to be baseline? Skia draws from baseline.
        # If x,y is top-left of text box, we need to add ascent.
        # For now, let's assume x,y is baseline or handle it in layout.
        # Let's assume x,y passed here is the top-left of the text element, 
        # so we shift down by font size roughly or measure it.
        
        # Better: measure text
        # metrics = font.getMetrics()
        # y += -metrics.fAscent # Shift down to baseline
        
        canvas.drawString(text, x, y + font_size, font, paint)

    def measure_text(self, text, style):
        font_size = style.get('font_size', 14)
        font = skia.Font(self.default_typeface, font_size)
        width = font.measureText(text)
        metrics = font.getMetrics()
        height = -metrics.fAscent + metrics.fDescent
        return width, height

    def _parse_color(self, color_str):
        if isinstance(color_str, str):
            if color_str.startswith('#'):
                hex_color = color_str.lstrip('#')
                if len(hex_color) == 3:
                    # Expand #RGB to #RRGGBB
                    hex_color = "".join(c*2 for c in hex_color)
                
                if len(hex_color) == 6:
                    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    return skia.Color(r, g, b)
                elif len(hex_color) == 8: # ARGB or RGBA? usually hex is RRGGBB
                    # Let's assume RRGGBB
                    pass
            elif color_str.lower() == 'white': return skia.ColorWHITE
            elif color_str.lower() == 'black': return skia.ColorBLACK
            elif color_str.lower() == 'red': return skia.ColorRED
            elif color_str.lower() == 'blue': return skia.ColorBLUE
            elif color_str.lower() == 'green': return skia.ColorGREEN
        
        return skia.ColorWHITE
