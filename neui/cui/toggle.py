from ..ui.box import Box
import skia

class Toggle(Box):
    def __init__(self, checked=False, on_change=None, **kwargs):
        style = kwargs.get('style', {})
        if 'w' not in style: style['w'] = 50
        if 'h' not in style: style['h'] = 26
        if 'bg_on' not in style: style['bg_on'] = "#007ACC"
        if 'bg_off' not in style: style['bg_off'] = "#444444"
        if 'thumb_color' not in style: style['thumb_color'] = "white"
        if 'radius' not in style: style['radius'] = 13 # Half height
        
        kwargs['style'] = style
        super().__init__(**kwargs)
        
        self.checked = checked
        self.on_change = on_change

    def on_click(self):
        self.checked = not self.checked
        if self.on_change:
            self.on_change(self.checked)

    @property
    def value(self):
        return self.checked

    @value.setter
    def value(self, val):
        self.checked = val

    def render(self, canvas, renderer):
        # 1. Draw Track (Background)
        bg_color = self.style['bg_on'] if self.checked else self.style['bg_off']
        
        # Create a temporary style for the track to use renderer.draw_rect
        track_style = self.style.copy()
        track_style['bg'] = bg_color
        
        renderer.draw_rect(canvas, self.computed_bounds, track_style)
        
        # 2. Draw Thumb
        b = self.computed_bounds
        thumb_radius = (b['h'] - 4) / 2
        thumb_padding = 2
        
        thumb_x = b['x'] + thumb_padding + thumb_radius
        if self.checked:
            thumb_x = b['x'] + b['w'] - thumb_padding - thumb_radius
            
        thumb_y = b['y'] + b['h'] / 2
        
        thumb_paint = skia.Paint(Color=renderer._parse_color(self.style['thumb_color']), AntiAlias=True)
        canvas.drawCircle(thumb_x, thumb_y, thumb_radius, thumb_paint)
