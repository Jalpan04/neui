from neui.ui.box import Box
from neui.ui.text import Text
from neui.core.animation import animation_manager, Animation, Easing
import time

class Toast(Box):
    def __init__(self, message, duration=3.0, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.duration = duration
        self.start_time = time.time()
        self.is_dying = False
        
        # Default Style
        if 'bg' not in self.style: self.style['bg'] = '#333'
        if 'radius' not in self.style: self.style['radius'] = 5
        if 'padding' not in self.style: self.style['padding'] = 10
        if 'shadow' not in self.style: self.style['shadow'] = 5
        if 'w' not in self.style: self.style['w'] = 300
        
        # Initial opacity/position for animation
        self.style['opacity'] = 0
        self.style['y_offset'] = 20 # Slide up from bottom
        
        # Content
        self.add(Text(message, style={'color': 'white'}))

    def update(self):
        elapsed = time.time() - self.start_time
        if elapsed > self.duration and not self.is_dying:
            self.is_dying = True
            # Fade out
            self.animate({'opacity': 0, 'y_offset': 20}, duration=0.5, on_complete=self.remove)
            
    def remove(self):
        if self.parent:
            self.parent.remove_toast(self)

class ToastManager(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fixed position overlay
        self.style['w'] = '100%'
        self.style['h'] = '100%'
        self.style['layout'] = 'col'
        self.style['align'] = 'end' # Bottom right
        self.style['justify'] = 'end'
        self.style['padding'] = 20
        self.style['gap'] = 10
        
        # Pass-through clicks?
        # We need to ensure we don't block clicks on the main app unless clicking a toast.
        # Hit testing needs to handle this.
        
    def show(self, message, duration=3.0, type='info'):
        bg = '#333'
        if type == 'success': bg = '#2e7d32'
        elif type == 'error': bg = '#c62828'
        elif type == 'warning': bg = '#f9a825'
        
        toast = Toast(message, duration=duration, style={'bg': bg})
        self.add(toast)
        
        # Animate In
        toast.animate({'opacity': 1, 'y_offset': 0}, duration=0.3, easing=Easing.ease_out_quad)
        
    def remove_toast(self, toast):
        if toast in self.children:
            self.children.remove(toast)

    def render(self, canvas, renderer):
        # Update toasts
        for child in list(self.children): # Copy list as we might modify it
            if isinstance(child, Toast):
                child.update()
                
        # Layout toasts (simple stacking from bottom)
        # We need to manually position them because they are in an overlay
        # and we want them to stack up from bottom-right.
        
        # Actually, if we use 'col' layout with 'justify: end', they stack at bottom.
        # But we need to ensure the ToastManager itself doesn't block the app.
        # For now, let's just render them.
        
        # We need to run layout on ourselves to position children
        # But we are an overlay, so we might not be in the main layout tree.
        # App calls render() on us.
        
        # Let's assume App sets our bounds to window size.
        # We need to layout children.
        
        # Hack: Run layout logic here? Or rely on App calling layout?
        # App only calls layout on root.
        # So we need to layout ourselves.
        
        # Get window size from canvas? Or pass it in?
        # Renderer doesn't know window size.
        # But we can get it from self.computed_bounds if set.
        
        # Let's assume we are full screen.
        w = self.style.get('w')
        h = self.style.get('h')
        
        # We need to resolve '100%'
        # But we don't have parent context easily here if not in tree.
        # Let's assume App sets our computed_bounds when adding/resizing?
        # App doesn't currently layout overlays.
        
        # We should add layout support for overlays in App.
        
        super().render(canvas, renderer)

