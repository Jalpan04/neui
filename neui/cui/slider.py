from ..ui.element import Element
import skia

class Slider(Element):
    def __init__(self, value=0.5, min_val=0.0, max_val=1.0, on_change=None, **kwargs):
        style = kwargs.get('style', {})
        if 'w' not in style: style['w'] = 200
        if 'h' not in style: style['h'] = 20
        if 'track_color' not in style: style['track_color'] = "#444444"
        if 'active_color' not in style: style['active_color'] = "#007ACC"
        if 'thumb_color' not in style: style['thumb_color'] = "white"
        
        kwargs['style'] = style
        super().__init__(**kwargs)
        
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.on_change = on_change
        self.dragging = False

    def on_mouse_down(self):
        self.dragging = True
        # We need to update value immediately on click too (jump to pos)
        # But we don't have x,y here easily unless passed?
        # EventManager dispatches on_mouse_down without args currently.
        # We should update EventManager to pass x,y to mouse down too?
        # Or just wait for first move?
        # Let's update EventManager to pass x,y to mouse down.
        pass

    def on_mouse_up(self):
        self.dragging = False

    def on_mouse_move(self, x, y):
        if self.dragging:
            self._update_value_from_pos(x)

    def _update_value_from_pos(self, x):
        b = self.computed_bounds
        # Clamp x to bounds
        rel_x = max(0, min(x - b['x'], b['w']))
        ratio = rel_x / b['w']
        
        new_value = self.min_val + (ratio * (self.max_val - self.min_val))
        self.value = new_value
        
        if self.on_change:
            self.on_change(self.value)

    def render(self, canvas, renderer):
        b = self.computed_bounds
        cy = b['y'] + b['h'] / 2
        
        # 1. Draw Track Background
        track_paint = skia.Paint(Color=renderer._parse_color(self.style['track_color']), AntiAlias=True)
        # 4px height track
        track_rect = skia.Rect.MakeXYWH(b['x'], cy - 2, b['w'], 4)
        canvas.drawRRect(skia.RRect.MakeRectXY(track_rect, 2, 2), track_paint)
        
        # 2. Draw Active Track
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        active_w = b['w'] * ratio
        
        active_paint = skia.Paint(Color=renderer._parse_color(self.style['active_color']), AntiAlias=True)
        active_rect = skia.Rect.MakeXYWH(b['x'], cy - 2, active_w, 4)
        canvas.drawRRect(skia.RRect.MakeRectXY(active_rect, 2, 2), active_paint)
        
        # 3. Draw Thumb
        thumb_x = b['x'] + active_w
        thumb_radius = 8
        thumb_paint = skia.Paint(Color=renderer._parse_color(self.style['thumb_color']), AntiAlias=True)
        # Add shadow to thumb?
        canvas.drawCircle(thumb_x, cy, thumb_radius, thumb_paint)
