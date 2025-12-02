from .element import Element

class Text(Element):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._wrapped_lines = None  # Cache wrapped lines

    def _wrap_text(self, text, max_width, renderer):
        """
        Wrap text to fit within max_width.
        Returns list of lines.
        """
        wrap_mode = self.style.get('wrap', 'word')  # 'none', 'word', or 'char'
        
        if wrap_mode == 'none' or max_width <= 0:
            return [text]
        
        lines = []
        words = text.split(' ') if wrap_mode == 'word' else list(text)
        current_line = ""
        
        for item in words:
            # For word wrapping, add space between words
            separator = ' ' if wrap_mode == 'word' and current_line else ''
            test_line = current_line + separator + item
            
            # Measure the test line
            width, _ = renderer.measure_text(test_line, self.style)
            
            if width <= max_width:
                current_line = test_line
            else:
                # Line would be too long
                if current_line:
                    lines.append(current_line)
                    current_line = item
                else:
                    # Single word/char is longer than max_width
                    # For char mode, we can force break
                    if wrap_mode == 'char':
                        lines.append(item)
                        current_line = ""
                    else:
                        # For word mode, keep the long word on its own line
                        lines.append(item)
                        current_line = ""
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [text]

    def render(self, canvas, renderer):
        # Draw text with wrapping support
        b = self.computed_bounds
        
        # Check if wrapping is enabled and we have a width constraint
        wrap_mode = self.style.get('wrap', 'none')
        max_width = b.get('w', 0)
        
        if wrap_mode != 'none' and max_width > 0:
            # Wrap text
            lines = self._wrap_text(self.text, max_width, renderer)
            
            # Get line height
            font_size = self.style.get('font_size', 14)
            line_height = self.style.get('line_height', font_size * 1.2)
            
            # Draw each line
            y_offset = b['y']
            for line in lines:
                renderer.draw_text(canvas, line, b['x'], y_offset, self.style)
                y_offset += line_height
        else:
            # Draw single line
            renderer.draw_text(canvas, self.text, b['x'], b['y'], self.style)
        
    def measure(self, parent_w, parent_h):
        # We need a renderer instance to measure.
        from neui.core.renderer import Renderer
        renderer = Renderer()
        
        # Check if wrapping is enabled
        wrap_mode = self.style.get('wrap', 'none')
        max_width = self.style.get('max_width', parent_w if parent_w else 0)
        
        if wrap_mode != 'none' and max_width > 0:
            # Measure wrapped text
            lines = self._wrap_text(self.text, max_width, renderer)
            
            # Calculate total height
            font_size = self.style.get('font_size', 14)
            line_height = self.style.get('line_height', font_size * 1.2)
            total_height = len(lines) * line_height
            
            # Width is the max_width
            return max_width, total_height
        else:
            # Measure as single line
            w, h = renderer.measure_text(self.text, self.style)
            return w, h
