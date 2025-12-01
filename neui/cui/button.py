from ..ui.box import Box
import skia

class Button(Box):
    def __init__(self, text="Button", on_click=None, **kwargs):
        # Default styles
        style = kwargs.get('style', {})
        if 'bg' not in style: style['bg'] = "#007ACC"
        if 'radius' not in style: style['radius'] = 6
        if 'padding' not in style: style['padding'] = 10
        if 'align' not in style: style['align'] = 'center'
        if 'justify' not in style: style['justify'] = 'center'
        if 'cursor' not in style: style['cursor'] = 'hand'
        
        kwargs['style'] = style
        super().__init__(**kwargs)
        
        self.text = text
        # We do NOT add a Text child anymore. We render manually.
        
        self.on_click_handler = on_click
        
        # State styles
        self.normal_bg = style['bg']
        self.hover_bg = self._lighten_color(self.normal_bg, 20)
        self.pressed_bg = self._darken_color(self.normal_bg, 20)

    def on_mouse_enter(self):
        self.style['bg'] = self.hover_bg

    def on_mouse_leave(self):
        self.style['bg'] = self.normal_bg

    def on_mouse_down(self):
        self.style['bg'] = self.pressed_bg

    def on_mouse_up(self):
        self.style['bg'] = self.hover_bg

    def on_click(self):
        if self.on_click_handler:
            self.on_click_handler()

    def render(self, canvas, renderer):
        # 1. Draw Background (Box logic)
        renderer.draw_rect(canvas, self.computed_bounds, self.style)
        
        # 2. Draw Text Centered
        # We calculate position relative to our current bounds
        b = self.computed_bounds
        
        # Measure text
        text_style = {**self.style, 'color': 'white'} # Force white text for now
        w, h = renderer.measure_text(self.text, text_style)
        
        # Center X: x + (width - text_width) / 2
        text_x = b['x'] + (b['w'] - w) / 2
        
        # Center Y: y + (height - text_height) / 2
        # Note: draw_text expects top-left Y (based on our previous fixes)
        text_y = b['y'] + (b['h'] - h) / 2
        
        renderer.draw_text(canvas, self.text, text_x, text_y, text_style)

    def _lighten_color(self, hex_color, amount=20):
        return "#3399FF" 

    def _darken_color(self, hex_color, amount=20):
        return "#005599"
