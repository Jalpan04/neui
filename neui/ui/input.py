import glfw
import skia
import time
from .element import Element

class Input(Element):
    def __init__(self, placeholder="", password=False, **kwargs):
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self.password = password
        self.text = ""
        self.cursor_pos = 0
        self.focused = False
        self.cursor_visible = True
        self.last_blink_time = 0
        
        # Default styles
        if 'padding' not in self.style: self.style['padding'] = 10
        if 'bg' not in self.style: self.style['bg'] = "#333333"
        if 'radius' not in self.style: self.style['radius'] = 5
        if 'w' not in self.style: self.style['w'] = 200 # Default width

    def on_focus(self):
        self.focused = True
        self.style['border'] = '2px solid #007ACC' # Visual feedback
        # Reset blink
        self.cursor_visible = True
        self.last_blink_time = time.time()

    def on_blur(self):
        self.focused = False
        if 'border' in self.style: del self.style['border']

    def on_char(self, codepoint):
        char = chr(codepoint)
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.cursor_pos += 1

    def on_keydown(self, key, mods):
        if key == glfw.KEY_BACKSPACE:
            if self.cursor_pos > 0:
                self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                self.cursor_pos -= 1
        elif key == glfw.KEY_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif key == glfw.KEY_RIGHT:
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1
        elif key == glfw.KEY_HOME:
            self.cursor_pos = 0
        elif key == glfw.KEY_END:
            self.cursor_pos = len(self.text)

    def measure(self, parent_w, parent_h):
        # Intrinsic size
        font_size = self.style.get('font_size', 14)
        padding = self.style.get('padding', 10)
        # Default width if not set is 200, but layout might override.
        # If layout calls measure, it wants intrinsic.
        # Input usually has a fixed default width or expands.
        # Let's say default w=200, h=font_size + padding*2
        w = self.style.get('w', 200)
        if isinstance(w, str): w = 200 # Fallback for % in measure
        h = font_size + (padding * 2)
        return w, h

    def render(self, canvas, renderer):
        # Draw background
        renderer.draw_rect(canvas, self.computed_bounds, self.style)
        
        # Draw Border if focused
        if self.focused:
            # Simple border simulation
            pass

        # Prepare Text
        display_text = "*" * len(self.text) if self.password else self.text
        if not display_text and not self.focused:
            display_text = self.placeholder
            text_color = "#888888"
        else:
            text_color = self.style.get('color', 'white')

        # Draw Text
        b = self.computed_bounds
        padding = self.style.get('padding', 10)
        
        # Vertical Centering
        font_size = self.style.get('font_size', 14)
        # Measure text height for better centering?
        # renderer.measure_text returns width, height.
        _, text_h = renderer.measure_text("Ay", self.style)
        
        text_x = b['x'] + padding
        # Center: y + (h - text_h) / 2
        # But draw_text draws at y + font_size (baseline-ish) in renderer.
        # So we need top of text.
        # renderer.draw_text(..., y + font_size)
        # So we pass top-left Y.
        text_y = b['y'] + (b['h'] - text_h) / 2
        
        renderer.draw_text(canvas, display_text, text_x, text_y, {**self.style, 'color': text_color})

        # Draw Cursor
        if self.focused:
            if time.time() - self.last_blink_time > 0.5:
                self.cursor_visible = not self.cursor_visible
                self.last_blink_time = time.time()
            
            if self.cursor_visible:
                cursor_text = display_text[:self.cursor_pos]
                w, h = renderer.measure_text(cursor_text, self.style)
                cursor_x = text_x + w
                
                paint = skia.Paint(Color=skia.ColorWHITE, AntiAlias=False)
                # Cursor Y same as text Y
                canvas.drawRect(skia.Rect.MakeXYWH(cursor_x, text_y, 2, text_h), paint)
