import time
import math

class AnimationManager:
    def __init__(self):
        self.animations = []
        
    def add(self, animation):
        self.animations.append(animation)
        
    def update(self):
        if not self.animations: return False
        
        now = time.time()
        active_animations = []
        needs_redraw = False
        
        for anim in self.animations:
            if not anim.started:
                anim.start_time = now
                anim.started = True
                
            elapsed = now - anim.start_time
            progress = min(1.0, elapsed / anim.duration)
            
            # Apply easing
            eased_progress = anim.easing(progress)
            
            # Update values
            anim.update(eased_progress)
            needs_redraw = True
            
            if progress < 1.0:
                active_animations.append(anim)
            else:
                # Animation finished
                if anim.on_complete:
                    anim.on_complete()
                    
        self.animations = active_animations
        return needs_redraw

class Animation:
    def __init__(self, element, properties, duration=0.3, easing=None, on_complete=None):
        self.element = element
        self.target_properties = properties
        self.duration = duration
        self.easing = easing or Easing.linear
        self.on_complete = on_complete
        
        self.start_time = 0
        self.started = False
        self.start_values = {}
        
        # Capture start values
        for prop in properties:
            # Handle nested style properties?
            # For now assume style properties
            val = element.style.get(prop)
            
            # Parse value if string (e.g. "100px", "#fff")
            # For v0.2, let's support numeric values only for simplicity
            # Color interpolation is harder.
            
            if val is None: val = 0
            if isinstance(val, (int, float)):
                self.start_values[prop] = val
            else:
                # Try to parse?
                # If we can't animate, skip
                pass

    def update(self, progress):
        for prop, target_val in self.target_properties.items():
            start_val = self.start_values.get(prop)
            if start_val is not None:
                # Interpolate
                current_val = start_val + (target_val - start_val) * progress
                self.element.style[prop] = current_val

class Easing:
    @staticmethod
    def linear(t): return t
    
    @staticmethod
    def ease_in_quad(t): return t * t
    
    @staticmethod
    def ease_out_quad(t): return t * (2 - t)
    
    @staticmethod
    def ease_in_out_quad(t):
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
        
    @staticmethod
    def ease_out_elastic(t):
        p = 0.3
        return math.pow(2, -10 * t) * math.sin((t - p / 4) * (2 * math.pi) / p) + 1

# Global instance
animation_manager = AnimationManager()
