from neui.ui.box import Box
import skia

class Radio(Box):
    def __init__(self, checked=False, on_change=None, **kwargs):
        super().__init__(**kwargs)
        self.checked = checked
        self.on_change = on_change
        
        # Default Style
        if 'w' not in self.style: self.style['w'] = 20
        if 'h' not in self.style: self.style['h'] = 20
        if 'border_color' not in self.style: self.style['border_color'] = '#666'
        if 'bg' not in self.style: self.style['bg'] = 'transparent'
        
        # Force circular
        # We can't easily force radius=50% in px if we don't know size yet, 
        # but usually radio buttons are fixed size.
        # Let's assume w/h are set and equal.
        self.style['radius'] = self.style['w'] / 2
        
        # Click handler
        self.on_click = self._toggle

    def _toggle(self):
        # Radio buttons usually only toggle ON, not OFF by clicking themselves (if in a group).
        # But for a standalone component, we might want toggle?
        # Standard behavior: clicking an unchecked radio checks it. Clicking a checked one does nothing.
        if not self.checked:
            self.checked = True
            if self.on_change:
                self.on_change(self.checked)

    def render(self, canvas, renderer):
        # Update style based on state
        if self.checked:
            self.style['border_color'] = '#007ACC'
        else:
            self.style['border_color'] = '#666'
            
        # Draw base circle (border)
        super().render(canvas, renderer)
        
        # Draw Inner Dot if checked
        if self.checked:
            self._draw_dot(canvas)
            
    def _draw_dot(self, canvas):
        x = self.computed_bounds['x']
        y = self.computed_bounds['y']
        w = self.computed_bounds['w']
        h = self.computed_bounds['h']
        
        # Dot size = 50% of container
        dot_size = w * 0.5
        offset = (w - dot_size) / 2
        
        rect = skia.Rect.MakeXYWH(x + offset, y + offset, dot_size, dot_size)
        paint = skia.Paint(Color=skia.Color(0, 122, 204), AntiAlias=True) # #007ACC
        
        canvas.drawOval(rect, paint)
