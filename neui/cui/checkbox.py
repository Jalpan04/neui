from neui.ui.box import Box
from neui.core.renderer import Renderer
import skia

class Checkbox(Box):
    def __init__(self, checked=False, on_change=None, **kwargs):
        super().__init__(**kwargs)
        self.checked = checked
        self.on_change = on_change
        
        # Default Style
        if 'w' not in self.style: self.style['w'] = 20
        if 'h' not in self.style: self.style['h'] = 20
        if 'radius' not in self.style: self.style['radius'] = 4
        if 'border_color' not in self.style: self.style['border_color'] = '#666'
        if 'bg' not in self.style: self.style['bg'] = 'transparent'
        
        # Click handler
        self.on_click = self._toggle

    def _toggle(self):
        self.checked = not self.checked
        if self.on_change:
            self.on_change(self.checked)

    def render(self, canvas, renderer):
        # Draw Box (Border/Background)
        # We need to handle checked state visual
        
        # Save original style to restore? Or just modify copy?
        # Let's modify style based on state for rendering
        
        original_bg = self.style.get('bg')
        original_border = self.style.get('border_color')
        
        if self.checked:
            self.style['bg'] = '#007ACC' # Accent color
            self.style['border_color'] = '#007ACC'
        else:
            self.style['bg'] = 'transparent'
            self.style['border_color'] = '#666'
            
        # Draw base box (using renderer's draw_rect logic if we had it exposed, 
        # but Box.render calls renderer.draw_rect.
        # However, we want to draw a border.
        # Renderer.draw_rect supports border? 
        # Looking at renderer.py: draw_rect supports 'bg', 'shadow'. No explicit border support yet?
        # Let's check renderer.py.
        
        # If renderer doesn't support border, we simulate it or add it.
        # For now, let's assume we need to draw it manually or update renderer.
        # I'll check renderer.py content first.
        
        super().render(canvas, renderer)
        
        # Draw Checkmark if checked
        if self.checked:
            self._draw_checkmark(canvas)
            
        # Restore style (optional, but good for consistency if user changes it)
        # self.style['bg'] = original_bg
        
    def _draw_checkmark(self, canvas):
        # Simple checkmark path
        path = skia.Path()
        x = self.computed_bounds['x']
        y = self.computed_bounds['y']
        w = self.computed_bounds['w']
        h = self.computed_bounds['h']
        
        # Checkmark coordinates (normalized)
        # Start (0.2, 0.5) -> Mid (0.4, 0.7) -> End (0.8, 0.3)
        path.moveTo(x + w * 0.25, y + h * 0.5)
        path.lineTo(x + w * 0.45, y + h * 0.7)
        path.lineTo(x + w * 0.75, y + h * 0.3)
        
        paint = skia.Paint(
            Color=skia.ColorWHITE,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=2,
            AntiAlias=True,
            StrokeCap=skia.Paint.kRound_Cap
        )
        canvas.drawPath(path, paint)
