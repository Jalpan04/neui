from .element import Element

class Box(Element):
    def render(self, canvas, renderer):
        # Draw self (background, border, etc)
        renderer.draw_rect(canvas, self.computed_bounds, self.style)
        
        # Draw children
        super().render(canvas, renderer)
