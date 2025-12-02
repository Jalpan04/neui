from .box import Box
import skia

class ScrollView(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_y = 0
        self.scroll_x = 0
        self.content_height = 0
        self.content_width = 0
        
        # Scrollbar interaction state
        self.is_dragging_scrollbar = False
        self.drag_start_y = 0
        self.scroll_start_y = 0
        self.scrollbar_hovered = False
        
        # Default style
        if 'overflow' not in self.style: self.style['overflow'] = 'hidden'
        if 'scrollbar_width' not in self.style: self.style['scrollbar_width'] = 10
        if 'scrollbar_color' not in self.style: self.style['scrollbar_color'] = '#ffffff40'
        if 'scrollbar_hover_color' not in self.style: self.style['scrollbar_hover_color'] = '#ffffff80'

    def on_scroll(self, dx, dy):
        # dy is usually +/- 1.0 per tick
        scroll_speed = 20
        
        # Vertical Scroll
        if self.style.get('overflow_y', 'auto') != 'hidden':
            self.scroll_y -= dy * scroll_speed
            self._clamp_scroll()
            
        # Horizontal Scroll (Locked by default unless overflow_x is 'auto' or 'scroll')
        if self.style.get('overflow_x', 'hidden') in ('auto', 'scroll'):
            self.scroll_x -= dx * scroll_speed
            # Clamp X (TODO: Implement X clamping properly if needed)
            max_scroll_x = max(0, self.content_width - self.computed_bounds['w'])
            self.scroll_x = max(0, min(self.scroll_x, max_scroll_x))

    def _clamp_scroll(self):
        max_scroll_y = max(0, self.content_height - self.computed_bounds['h'])
        self.scroll_y = max(0, min(self.scroll_y, max_scroll_y))

    def on_mouse_move(self, x, y):
        # Check hover on scrollbar
        thumb_rect = self._get_scrollbar_rect()
        if thumb_rect:
            # Simple hit test
            if (x >= thumb_rect['x'] and x <= thumb_rect['x'] + thumb_rect['w'] and
                y >= thumb_rect['y'] and y <= thumb_rect['y'] + thumb_rect['h']):
                self.scrollbar_hovered = True
            else:
                self.scrollbar_hovered = False
                
        # Handle Dragging
        if self.is_dragging_scrollbar:
            delta_y = y - self.drag_start_y
            
            # Calculate scroll delta based on track height
            view_h = self.computed_bounds['h']
            track_h = view_h
            
            if self.content_height > view_h:
                # Ratio of scrollable content to viewport
                # scroll_y / (content_h - view_h) = thumb_pos / (track_h - thumb_h)
                
                thumb_h = max(20, view_h * (view_h / self.content_height))
                available_track = track_h - thumb_h
                available_scroll = self.content_height - view_h
                
                if available_track > 0:
                    scroll_ratio = delta_y / available_track
                    self.scroll_y = self.scroll_start_y + (scroll_ratio * available_scroll)
                    self._clamp_scroll()

    def on_mouse_down(self, x, y):
        if self.scrollbar_hovered:
            self.is_dragging_scrollbar = True
            self.drag_start_y = y
            self.scroll_start_y = self.scroll_y
            return True # Consume event

    def on_mouse_up(self):
        self.is_dragging_scrollbar = False

    def render(self, canvas, renderer):
        # 1. Draw Background/Border (using Box logic)
        renderer.draw_rect(canvas, self.computed_bounds, self.style)
        
        # 2. Clip Content
        renderer.save(canvas)
        renderer.clip_rect(canvas, self.computed_bounds)
        
        # 3. Translate for Scroll
        canvas.translate(-self.scroll_x, -self.scroll_y)
        
        # 4. Render Children
        self._calculate_content_size()
        
        for child in self.children:
            child.render(canvas, renderer)
            
        renderer.restore(canvas)
        
        # Draw Scrollbar
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

    def _get_scrollbar_rect(self):
        if self.content_height <= self.computed_bounds['h']: return None
        
        view_h = self.computed_bounds['h']
        view_w = self.computed_bounds['w']
        
        # Calculate thumb height
        ratio = view_h / self.content_height
        thumb_h = max(20, view_h * ratio)
        
        # Calculate thumb position
        # scroll_y / (content_h - view_h) = thumb_y_offset / (view_h - thumb_h)
        max_scroll = self.content_height - view_h
        if max_scroll > 0:
            scroll_pct = self.scroll_y / max_scroll
            thumb_y_offset = scroll_pct * (view_h - thumb_h)
        else:
            thumb_y_offset = 0
            
        thumb_y = self.computed_bounds['y'] + thumb_y_offset
        
        sb_width = self.style.get('scrollbar_width', 10)
        
        return {
            'x': self.computed_bounds['x'] + view_w - sb_width,
            'y': thumb_y,
            'w': sb_width,
            'h': thumb_h
        }

    def _draw_scrollbar(self, canvas, renderer):
        rect = self._get_scrollbar_rect()
        if not rect: return
        
        color = self.style.get('scrollbar_hover_color') if (self.scrollbar_hovered or self.is_dragging_scrollbar) else self.style.get('scrollbar_color')
        
        renderer.draw_rect(canvas, rect, {'bg': color, 'radius': rect['w']/2})
