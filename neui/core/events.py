import glfw

class EventManager:
    def __init__(self, window):
        self.window = window
        self.hovered_element = None
        self.focused_element = None
        self.mouse_down_element = None
        
        # State
        self.last_mouse_state = glfw.RELEASE
        
        # Callbacks
        glfw.set_key_callback(self.window, self._on_key)
        glfw.set_char_callback(self.window, self._on_char)
        glfw.set_scroll_callback(self.window, self._on_scroll)

    def _on_key(self, window, key, scancode, action, mods):
        if self.focused_element:
            # Dispatch to focused element
            if action == glfw.PRESS:
                self._dispatch(self.focused_element, 'on_keydown', key=key, mods=mods)
            elif action == glfw.RELEASE:
                self._dispatch(self.focused_element, 'on_keyup', key=key, mods=mods)
            elif action == glfw.REPEAT:
                self._dispatch(self.focused_element, 'on_keyrepeat', key=key, mods=mods)

    def _on_char(self, window, codepoint):
        if self.focused_element:
            self._dispatch(self.focused_element, 'on_char', codepoint=codepoint)

    def _on_scroll(self, window, xoffset, yoffset):
        # Dispatch to hovered element first, then bubble up
        target = self.hovered_element or self.focused_element
        if target:
            self._dispatch(target, 'on_scroll', dx=xoffset, dy=yoffset)

    def process_events(self, root, overlays=None):
        if not root and not overlays: return

        x, y = glfw.get_cursor_pos(self.window)
        mouse_state = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT)
        
        # 1. Hit Test
        target = None
        
        # Check overlays first (reverse order - top most first)
        if overlays:
            for overlay in reversed(overlays):
                hit = self._hit_test(overlay, x, y)
                if hit:
                    target = hit
                    break
        
        # If no overlay hit, check root
        if not target and root:
            target = self._hit_test(root, x, y)
        
        # 2. Hover Events
        if target != self.hovered_element:
            # Mouse Leave
            if self.hovered_element:
                self._dispatch(self.hovered_element, 'on_mouse_leave')
            
            self.hovered_element = target
            
            # Mouse Enter
            if self.hovered_element:
                self._dispatch(self.hovered_element, 'on_mouse_enter')

        # Mouse Move
        # If we have a mouse_down_element (capture), dispatch to it
        if self.mouse_down_element:
            self._dispatch(self.mouse_down_element, 'on_mouse_move', x=x, y=y)
        elif self.hovered_element:
            self._dispatch(self.hovered_element, 'on_mouse_move', x=x, y=y)

        # 3. Click Events
        if mouse_state == glfw.PRESS and self.last_mouse_state == glfw.RELEASE:
            # Mouse Down
            self.mouse_down_element = target
            
            # Focus Management
            if target != self.focused_element:
                if self.focused_element:
                    self._dispatch(self.focused_element, 'on_blur')
                self.focused_element = target
                if self.focused_element:
                    self._dispatch(self.focused_element, 'on_focus')

            if target:
                self._dispatch(target, 'on_mouse_down', x=x, y=y)
        
        elif mouse_state == glfw.RELEASE and self.last_mouse_state == glfw.PRESS:
            # Mouse Up
            if target:
                self._dispatch(target, 'on_mouse_up')
            
            # Click (if released on same element as down)
            if target == self.mouse_down_element and target:
                self._dispatch(target, 'on_click')
            
            self.mouse_down_element = None

        self.last_mouse_state = mouse_state

    def _hit_test(self, element, x, y):
        # Check if point is within element bounds
        b = element.computed_bounds
        if not (b['x'] <= x <= b['x'] + b['w'] and b['y'] <= y <= b['y'] + b['h']):
            return None
        
        # Check children in reverse order (top-most first)
        for child in reversed(element.children):
            hit = self._hit_test(child, x, y)
            if hit:
                return hit
        
        return element

    def _dispatch(self, element, event_name, **kwargs):
        # Bubble up? For now, just call on target.
        # If we want bubbling, we loop up via parent.
        curr = element
        while curr:
            handler = getattr(curr, event_name, None)
            if handler:
                # Call handler, if it returns True, stop propagation?
                # Or just call it.
                handler(**kwargs)
                break # For now, let's stop at first handler to avoid double handling? 
                      # Actually, standard bubbling calls all. 
                      # But let's keep it simple: if handled, stop?
                      # Let's just call the specific handler on the target for now.
            curr = curr.parent
