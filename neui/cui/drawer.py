from neui.ui.box import Box
from neui.core.animation import Easing

class Drawer(Box):
    def __init__(self, width=300, on_close=None, **kwargs):
        super().__init__(**kwargs)
        self.on_close_callback = on_close
        
        # Drawer Overlay (Scrim) Styles
        self.style['w'] = '100%'
        self.style['h'] = '100%'
        self.style['bg'] = '#00000080' # Semi-transparent black
        # self.style['layout'] = 'manual' # Use default layout to ensure children are measured
        
        self.drawer_width = width
        self.is_open = False
        
        # Panel (The actual drawer content)
        self.panel = Box(style={
            'w': width,
            'h': '100%',
            'bg': '#1e1e1e',
            'shadow': 20,
            'left': -width # Start off-screen
        })
        
        # Add panel to self (Overlay)
        self.add(self.panel)
        
        # Click on Scrim closes drawer
        self.on_click = self._on_scrim_click
        
        # Prevent clicks on panel from closing drawer (consume event)
        self.panel.on_click = lambda: None 

    def _on_scrim_click(self):
        self.close()

    def open(self):
        self.is_open = True
        # Animate Panel In
        # From -width to 0
        self.panel.animate({'left': 0}, duration=0.3, easing=Easing.ease_out_quad)
        
        # Fade In Scrim
        self.style['bg'] = '#00000000'
        self.animate({'bg': '#00000080'}, duration=0.3) # Need color tweening support? 
        # AnimationManager currently only supports numeric.
        # For now, let's skip scrim fade or implement color tweening.
        # Or just set it instantly.
        self.style['bg'] = '#00000080'

    def close(self):
        self.is_open = False
        # Animate Panel Out
        self.panel.animate({'left': -self.drawer_width}, duration=0.3, easing=Easing.ease_in_quad, on_complete=self._remove_self)
        
    def _remove_self(self):
        if self.on_close_callback:
            self.on_close_callback()
            
    def add_content(self, element):
        self.panel.add(element)
