class Element:
    def __init__(self, **kwargs):
        self.children = []
        self.parent = None
        self.style = kwargs.get('style', {})
        
        # Merge direct kwargs into style for convenience (e.g. w=100)
        for k, v in kwargs.items():
            if k not in ['style', 'children']:
                self.style[k] = v
                
        self.computed_bounds = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
        
        # Add children if passed
        if 'children' in kwargs:
            for child in kwargs['children']:
                self.add(child)

        # Auto-add to current context
        from neui import _context_stack
        if _context_stack and self.parent is None:
             _context_stack[-1].add(self)

    def add(self, child):
        child.parent = self
        self.children.append(child)
        return child # Return child for chaining

    def render(self, canvas, renderer):
        # Base render: draw children
        # Subclasses should call super().render() or handle children manually
        for child in self.children:
            child.render(canvas, renderer)
            
    def animate(self, properties, duration=0.3, easing=None, on_complete=None):
        from neui.core.animation import animation_manager, Animation
        anim = Animation(self, properties, duration, easing, on_complete)
        animation_manager.add(anim)
            
    def __enter__(self):
        # Context manager support for nesting
        # We need a global context stack or similar to know who the parent is?
        # The user example: with ui.Box(...): ui.Text(...)
        # This implies a global "current container" stack.
        # We need a helper for this.
        from neui import _context_stack
        _context_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        from neui import _context_stack
        _context_stack.pop()
        
        # Auto-add to parent if we are not the root and haven't been added
        if self.parent is None and _context_stack:
            parent = _context_stack[-1]
            parent.add(self)
