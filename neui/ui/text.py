from .element import Element

class Text(Element):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def render(self, canvas, renderer):
        # Draw text
        b = self.computed_bounds
        renderer.draw_text(canvas, self.text, b['x'], b['y'], self.style)
        
    def measure(self, parent_w, parent_h):
        # We need a renderer instance to measure.
        # This is a bit tricky since measure is called from layout which doesn't have renderer.
        # We might need a singleton renderer or pass it down.
        # For now, let's create a temporary renderer or use a global one.
        from neui.core.renderer import Renderer
        renderer = Renderer() # This is cheap-ish?
        w, h = renderer.measure_text(self.text, self.style)
        return w, h
