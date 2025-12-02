from neui.ui.box import Box
import skia

class ProgressBar(Box):
    def __init__(self, value=0.0, **kwargs):
        super().__init__(**kwargs)
        self.value = max(0.0, min(1.0, value))
        
        # Default Style
        if 'w' not in self.style: self.style['w'] = 200
        if 'h' not in self.style: self.style['h'] = 10
        if 'bg' not in self.style: self.style['bg'] = '#333'
        if 'radius' not in self.style: self.style['radius'] = 5
        
        # Fill color
        self.fill_color = kwargs.get('fill_color', '#007ACC')

    def set_value(self, value):
        self.value = max(0.0, min(1.0, value))

    def render(self, canvas, renderer):
        # Draw Track
        super().render(canvas, renderer)
        
        # Draw Fill
        if self.value > 0:
            x = self.computed_bounds['x']
            y = self.computed_bounds['y']
            w = self.computed_bounds['w']
            h = self.computed_bounds['h']
            radius = self.style.get('radius', 0)
            
            fill_w = w * self.value
            
            fill_rect = skia.Rect.MakeXYWH(x, y, fill_w, h)
            paint = skia.Paint(
                Color=renderer._parse_color(self.fill_color), 
                AntiAlias=True
            )
            
            if radius > 0:
                # We might need to clip the fill to the rounded corners of the track?
                # Or just draw a rounded rect.
                # If fill is small, rounded rect might look weird if radius > width.
                # Let's just draw a rounded rect with same radius.
                canvas.drawRRect(skia.RRect.MakeRectXY(fill_rect, radius, radius), paint)
            else:
                canvas.drawRect(fill_rect, paint)
