def compute_layout(element, parent_w, parent_h, parent_x=0, parent_y=0):
    """
    Recursive layout engine.
    Calculates element.computed_bounds based on style and children.
    """
    style = element.style
    
    # 1. Resolve Own Dimensions
    w = _resolve_dim(style.get('w'), parent_w)
    h = _resolve_dim(style.get('h'), parent_h)
    
    # Default width behavior (block-like)
    if w is None:
        if hasattr(element, 'measure'):
            # Use intrinsic width if available
            intr_w, _ = element.measure(parent_w, parent_h)
            w = intr_w + (style.get('padding', 0) * 2)
        else:
            w = parent_w # Stretch to fill parent width by default
        
    # Padding
    padding = style.get('padding', 0)
    
    # 2. Measure Children (to determine auto height/width)
    layout_dir = style.get('layout', 'col')
    gap = style.get('gap', 0)
    
    # We need to determine content size
    # If we have fixed w/h, we use it.
    # If auto, we sum children.
    
    # Available space for children
    avail_child_w = w - (padding * 2) if w is not None else parent_w 
    avail_child_h = h - (padding * 2) if h is not None else parent_h
    
    # Pass 1: Measure all children
    child_measurements = []
    
    main_size = 0
    cross_size = 0
    
    for child in element.children:
        # Recursively measure child
        # We don't know x,y yet, so pass 0,0
        # We pass available size
        
        # If child has % size, it needs our resolved size.
        # If we are auto, and child is %, that's circular.
        # CSS says % of auto is undefined/0 usually.
        # Let's assume if we are auto, we pass 0 or handle it.
        
        cw, ch = _measure_element(child, avail_child_w, avail_child_h)
        child_measurements.append((cw, ch))
        
        if layout_dir == 'col':
            main_size += ch + gap
            cross_size = max(cross_size, cw)
        else:
            main_size += cw + gap
            cross_size = max(cross_size, ch)
            
    if element.children:
        main_size -= gap # Remove last gap
        
    # Resolve Auto Dimensions
    if h is None:
        if layout_dir == 'col':
            h = main_size + (padding * 2)
        else:
            h = cross_size + (padding * 2)
            
    # If w was None, we set it to parent_w above.
    # But if layout='row' and w=None, maybe we want content width?
    # For now, let's stick to block behavior (fill width).
    
    # Re-calculate available content box
    content_w = w - (padding * 2)
    content_h = h - (padding * 2)
    content_x = parent_x + padding
    content_y = parent_y + padding
    
    # 3. Position Children
    align = style.get('align', 'start')
    justify = style.get('justify', 'start')
    
    # Distribute Main Axis
    free_main_space = (content_h if layout_dir == 'col' else content_w) - main_size
    
    start_offset = 0
    gap_extra = 0
    
    if justify == 'center':
        start_offset = free_main_space / 2
    elif justify == 'end':
        start_offset = free_main_space
    elif justify == 'space-between' and len(element.children) > 1:
        gap_extra = free_main_space / (len(element.children) - 1)
        
    current_pos = start_offset
    
    for i, child in enumerate(element.children):
        cw, ch = child_measurements[i]
        
        cx, cy = 0, 0
        
        # Cross Axis Alignment
        free_cross_space = (content_w if layout_dir == 'col' else content_h) - (cw if layout_dir == 'col' else ch)
        cross_offset = 0
        
        if align == 'center':
            cross_offset = free_cross_space / 2
        elif align == 'end':
            cross_offset = free_cross_space
        elif align == 'stretch':
             # If stretch, we force child size?
             # Only if child didn't have fixed size?
             # For now, skip stretch logic or implement simple version
             pass

        if layout_dir == 'col':
            cx = content_x + cross_offset
            cy = content_y + current_pos
            current_pos += ch + gap + gap_extra
        else:
            cx = content_x + current_pos
            cy = content_y + cross_offset
            current_pos += cw + gap + gap_extra
            
        # Recursive Layout (Pass 2 - Finalize)
        # We call compute_layout again? 
        # Or just set bounds and recurse?
        # We need to recurse to layout grandchildren.
        # We already measured, but now we have exact X,Y.
        
        # Optimization: We could merge measure/layout if we didn't need justify.
        
        # Set bounds temporarily so child knows its size?
        # Actually, we should just call compute_layout with the decided size.
        
        # If we force size (stretch), update cw/ch
        
        child.computed_bounds = {'x': cx, 'y': cy, 'w': cw, 'h': ch}
        compute_layout(child, cw, ch, cx, cy)

    # Finalize Own Bounds
    element.computed_bounds = {'x': parent_x, 'y': parent_y, 'w': w, 'h': h}

def _resolve_dim(val, parent_val):
    if val is None: return None
    if isinstance(val, (int, float)): return val
    if isinstance(val, str) and val.endswith('%'):
        if parent_val is None: return 0 # % of auto is 0
        return parent_val * (float(val[:-1]) / 100)
    return 0

def _measure_element(element, parent_w, parent_h):
    # Helper to measure an element without setting final position
    # This is effectively a "dry run" of layout for size
    
    # If element has intrinsic size (Text), use it.
    if hasattr(element, 'measure'):
        return element.measure(parent_w, parent_h)
        
    # Otherwise, run layout logic to determine size
    # This is expensive (double recursion).
    # Ideally we cache or split logic.
    
    # For now, just duplicate logic or create a dummy run?
    # Let's just create a dummy run.
    
    # Hack: We can't easily dry run without modifying element state if we use compute_layout.
    # But compute_layout sets computed_bounds.
    # Let's just run compute_layout with 0,0 and return w,h.
    
    # Save current bounds? No need, we are in a measure pass.
    
    compute_layout(element, parent_w, parent_h, 0, 0)
    b = element.computed_bounds
    return b['w'], b['h']
