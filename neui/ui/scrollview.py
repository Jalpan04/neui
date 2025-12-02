from .box import Box
import skia

class ScrollView(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_y = 0
        self.scroll_x = 0
        self.content_height = 0
        self.content_width = 0
        
        # Default style
        if 'overflow' not in self.style: self.style['overflow'] = 'hidden'

    def on_scroll(self, dx, dy):
        # dy is usually +/- 1.0 per tick
        scroll_speed = 20
        self.scroll_y -= dy * scroll_speed
        self.scroll_x -= dx * scroll_speed
        
        # Clamp
        max_scroll_y = max(0, self.content_height - self.computed_bounds['h'])
        self.scroll_y = max(0, min(self.scroll_y, max_scroll_y))
        
        # For X, similar logic if needed, but usually vertical scroll is primary
        # max_scroll_x = max(0, self.content_width - self.computed_bounds['w'])
        # self.scroll_x = max(0, min(self.scroll_x, max_scroll_x))

    def render(self, canvas, renderer):
        # 1. Draw Background/Border (using Box logic)
        renderer.draw_rect(canvas, self.computed_bounds, self.style)
        
        # 2. Clip Content
        renderer.save(canvas)
        renderer.clip_rect(canvas, self.computed_bounds)
        
        # 3. Translate for Scroll
        canvas.translate(-self.scroll_x, -self.scroll_y)
        
        # 4. Render Children
        # We need to ensure children are positioned relative to the scroll view's origin
        # The layout engine positions them absolutely on screen.
        # But since we translate the canvas, we need to be careful.
        # If children have absolute screen coordinates, translating canvas will shift them wrong 
        # IF they were calculated assuming no scroll.
        
        # Actually, layout engine calculates 'x' and 'y' relative to parent's content box + parent pos.
        # So children.y = parent.y + offset.
        # If we translate canvas by -scroll_y, the child at parent.y will be drawn at parent.y - scroll_y.
        # This is correct relative to the window origin?
        # No. If we translate the canvas, everything drawn after is shifted.
        # If we draw a rect at (100, 100) and translate by (0, -10), it draws at (100, 90).
        # This is what we want for scrolling UP.
        
        # However, we need to make sure we don't translate the background (already drawn).
        # We did save/restore around the children render.
        
        # One issue: Layout engine might not know about scroll content size?
        # If ScrollView has fixed height, children might be laid out outside bounds?
        # Yes, layout engine should just layout children as if they have space.
        # But if ScrollView has fixed height, layout engine might constrain children?
        # We need the ScrollView to act as an infinite height container for its children during layout?
        # Or we use a inner "content" container?
        
        # For now, let's assume children are laid out normally. 
        # If we want scroll, we usually put a big Box inside the ScrollView.
        # The ScrollView itself has fixed size. The inner Box has auto size (which grows).
        
        # We need to capture the content size for clamping.
        # We can calculate it from children bounds.
        
        self._calculate_content_size()
        
        for child in self.children:
            child.render(canvas, renderer)
            
        renderer.restore(canvas)
        
        # Draw Scrollbar? (Optional)
        self._draw_scrollbar(canvas, renderer)

    def _calculate_content_size(self):
        max_y = 0
        max_x = 0
        for child in self.children:
            b = child.computed_bounds
            max_y = max(max_y, b['y'] + b['h'])
            max_x = max(max_x, b['x'] + b['w'])
            
        # Relative to our own position
        self.content_height = max_y - self.computed_bounds['y']
        self.content_width = max_x - self.computed_bounds['x']

    def _draw_scrollbar(self, canvas, renderer):
        if self.content_height <= self.computed_bounds['h']: return
        
        # Simple scrollbar
        view_h = self.computed_bounds['h']
        ratio = view_h / self.content_height
        thumb_h = max(20, view_h * ratio)
        thumb_y = self.computed_bounds['y'] + (self.scroll_y / self.content_height) * view_h
        
        thumb_rect = {
            'x': self.computed_bounds['x'] + self.computed_bounds['w'] - 6,
            'y': thumb_y,
            'w': 4,
            'h': thumb_h
        }
        
        renderer.draw_rect(canvas, thumb_rect, {'bg': '#ffffff40', 'radius': 2})
