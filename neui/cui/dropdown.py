from ..ui.element import Element
from ..ui.box import Box
from ..ui.text import Text
from ..core.app import App

class Dropdown(Element):
    def __init__(self, options, value=None, on_change=None, **kwargs):
        super().__init__(**kwargs)
        self.options = options
        self.value = value if value is not None else (options[0] if options else "")
        self.on_change = on_change
        self.is_open = False
        self.overlay = None
        
        # Default styles
        if 'w' not in self.style: self.style['w'] = 200
        if 'h' not in self.style: self.style['h'] = 40
        if 'bg' not in self.style: self.style['bg'] = '#2D333B'
        if 'radius' not in self.style: self.style['radius'] = 6
        if 'padding' not in self.style: self.style['padding'] = 10
        if 'color' not in self.style: self.style['color'] = 'white'
        if 'border_color' not in self.style: self.style['border_color'] = '#444'
        if 'border_width' not in self.style: self.style['border_width'] = 1
        
        # Hover state
        self.hovered = False

    def render(self, canvas, renderer):
        # Update style based on state
        current_style = self.style.copy()
        if self.hovered:
            current_style['bg'] = '#373E47' # Slightly lighter
            
        # Render main box
        renderer.draw_rect(canvas, self.computed_bounds, current_style)
        
        # Render text
        b = self.computed_bounds
        text_style = {**self.style, 'font_size': 14}
        
        # Draw value
        renderer.draw_text(canvas, str(self.value), b['x'] + 10, b['y'] + 10, text_style)
        
        # Render Chevron
        chevron = "▲" if self.is_open else "▼"
        # Measure chevron to align right
        cw, ch = renderer.measure_text(chevron, text_style)
        renderer.draw_text(canvas, chevron, b['x'] + b['w'] - cw - 10, b['y'] + 10, text_style)

    def on_mouse_enter(self):
        self.hovered = True
        
    def on_mouse_leave(self):
        self.hovered = False

    def on_click(self):
        self.toggle()

    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    def open(self):
        if self.is_open: return
        
        app = App.get_instance()
        if not app: return
        
        self.is_open = True
        
        # Create Overlay (Full screen transparent)
        self.overlay = Box(style={
            'w': '100%', 'h': '100%', 
            'position': 'absolute', 'x': 0, 'y': 0,
        })
        
        # Close on click outside
        self.overlay.on_click = self.close
        
        # Calculate Menu Position
        b = self.computed_bounds
        menu_x = b['x']
        menu_y = b['y'] + b['h'] + 5
        menu_w = b['w']
        
        # Menu Container
        menu = Box(style={
            'w': menu_w,
            'bg': self.style['bg'],
            'radius': self.style['radius'],
            'shadow': 10,
            'layout': 'col',
            'padding': 5,
            'gap': 2,
            'left': menu_x, # Absolute positioning via left/top
            'top': menu_y,
            'border_color': self.style.get('border_color'),
            'border_width': 1
        })
        
        # Prevent clicks on menu from closing overlay
        def no_op(): pass
        menu.on_click = no_op
        
        # Add Options
        for opt in self.options:
            # Option Item
            opt_style = {
                'w': '100%', 
                'h': 30, 
                'padding': 5, 
                'radius': 4,
                'bg': self.style['bg'] # Default bg
            }
            
            # We need a clickable item. Box works.
            item = Box(style=opt_style)
            
            # Text
            t = Text(str(opt), style={'color': self.style['color'], 'font_size': 14})
            item.add(t)
            
            # Hover effect for item
            # We need to attach event handlers. 
            # Python loop variable capture fix:
            def make_handler(option_value, item_box):
                def on_select():
                    self.value = option_value
                    if self.on_change:
                        self.on_change(option_value)
                    self.close()
                
                def on_enter():
                    item_box.style['bg'] = '#1F6FEB' # Blue highlight
                
                def on_leave():
                    item_box.style['bg'] = self.style['bg']
                    
                return on_select, on_enter, on_leave

            select_handler, enter_handler, leave_handler = make_handler(opt, item)
            
            item.on_click = select_handler
            item.on_mouse_enter = enter_handler
            item.on_mouse_leave = leave_handler
            
            menu.add(item)
            
        self.overlay.add(menu)
        app.add_overlay(self.overlay)

    def close(self):
        if not self.is_open: return
        
        app = App.get_instance()
        if app and self.overlay:
            app.remove_overlay(self.overlay)
            
        self.is_open = False
        self.overlay = None
