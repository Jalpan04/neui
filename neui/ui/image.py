import skia
from .element import Element

class Image(Element):
    def __init__(self, src, **kwargs):
        super().__init__(**kwargs)
        self.src = src
        self.image = None
        self._load_image()

    def _load_image(self):
        try:
            self.image = skia.Image.open(self.src)
        except Exception as e:
            print(f"Error loading image {self.src}: {e}")
            self.image = None

    def measure(self, parent_w, parent_h):
        # Helper to resolve dim
        def resolve(val, parent_val):
            if val is None: return None
            if isinstance(val, (int, float)): return val
            if isinstance(val, str) and val.endswith('%'):
                if parent_val is None: return 0
                return parent_val * (float(val[:-1]) / 100)
            return 0

        # If w/h are set in style, use them
        w = resolve(self.style.get('w'), parent_w)
        h = resolve(self.style.get('h'), parent_h)
        
        if w is None and self.image:
            w = self.image.width()
        if h is None and self.image:
            h = self.image.height()
            
        return w or 0, h or 0

    def render(self, canvas, renderer):
        if self.image:
            # print(dir(canvas))
            renderer.draw_image(canvas, self.image, self.computed_bounds, self.style)
