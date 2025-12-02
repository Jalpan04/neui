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
    
    # Calculate content box early
    content_w = w - (padding * 2)
    content_h = h - (padding * 2) if h is not None else None
    content_x = parent_x + padding
    content_y = parent_y + padding
    
    if layout_dir == 'grid':
        # Grid Layout Logic
        cols_template = style.get('grid_template_columns', '1fr')
        col_widths = _parse_grid_template(cols_template, content_w, gap)
        num_cols = len(col_widths)
        
        # We need to determine row heights. 
        # For auto rows, we need to measure children first.
        # This is a bit complex because we need to know width to measure height (for text wrapping),
        # and we know width from col_widths.
        
        row_heights = []
        current_row_idx = 0
        current_col_idx = 0
        
        # Group children by row
        grid_rows = []
        current_row_children = []
        
        for child in element.children:
            current_row_children.append(child)
            current_col_idx += 1
            if current_col_idx >= num_cols:
                grid_rows.append(current_row_children)
                current_row_children = []
                current_col_idx = 0
                current_row_idx += 1
        
        if current_row_children:
            grid_rows.append(current_row_children)
            
        # Measure rows
        for row_children in grid_rows:
            max_h = 0
            for i, child in enumerate(row_children):
                # Child width is fixed by column
                cw = col_widths[i]
                # Measure height given width
                _, ch = _measure_element(child, cw, avail_child_h) # Pass avail height?
                max_h = max(max_h, ch)
            row_heights.append(max_h)
            
        # Calculate Total Height for Auto Height Container
        total_grid_h = sum(row_heights) + (gap * (len(row_heights) - 1)) if row_heights else 0
        
        if h is None:
            h = total_grid_h + (padding * 2)
            # Re-calc content_h if h changed
            content_h = h - (padding * 2)

        # Position Children
        current_y = content_y
        
        for r, row_children in enumerate(grid_rows):
            rh = row_heights[r]
            current_x = content_x
            
            for c, child in enumerate(row_children):
                cw = col_widths[c]
                
                # Stretch height to row height by default in grid?
                # Or align? Let's stretch for consistency with 'fr' logic usually.
                # But let's respect child's intrinsic height if it's smaller?
                # CSS Grid defaults to stretch.
                
                # For now, let's just center vertically or top align?
                # Let's use top align for simplicity, or stretch if we had alignment props.
                # We'll set the child bounds to the cell bounds.
                
                child.computed_bounds = {'x': current_x, 'y': current_y, 'w': cw, 'h': rh}
                
                # Recurse
                compute_layout(child, cw, rh, current_x, current_y)
                
                current_x += cw + gap
            
            current_y += rh + gap
            
    elif layout_dir == 'col' or layout_dir == 'row':
        # Flex-like Layout (Existing Logic)
        
        # Pass 1: Measure all children
        child_measurements = []
        
        main_size = 0
        cross_size = 0
        
        for child in element.children:
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
                
        # Re-calculate available content box
        # content_w/h/x/y are already defined, but h might have changed.
        content_h = h - (padding * 2)
        # content_w, content_x, content_y remain same
        
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
            
            if layout_dir == 'col':
                cx = content_x + cross_offset
                cy = content_y + current_pos
                current_pos += ch + gap + gap_extra
            else:
                cx = content_x + current_pos
                cy = content_y + cross_offset
                current_pos += cw + gap + gap_extra
                
            # Apply relative offsets (left/top)
            off_x = child.style.get('left', 0)
            off_y = child.style.get('top', 0)
            
            final_x = cx + off_x
            final_y = cy + off_y
            
            child.computed_bounds = {'x': final_x, 'y': final_y, 'w': cw, 'h': ch}
            compute_layout(child, cw, ch, final_x, final_y)

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

def _parse_grid_template(template_str, available_space, gap):
    parts = template_str.split()
    if not parts: return [available_space]
    
    # Calculate total fixed width and gaps
    total_gap = gap * (len(parts) - 1)
    fixed_width = 0
    total_fr = 0
    
    parsed = []
    
    for p in parts:
        if p.endswith('px'):
            val = float(p[:-2])
            fixed_width += val
            parsed.append(('px', val))
        elif p.endswith('fr'):
            val = float(p[:-2])
            total_fr += val
            parsed.append(('fr', val))
        else:
            # Assume fr if just a number? or px?
            # Let's assume px if number
            try:
                val = float(p)
                fixed_width += val
                parsed.append(('px', val))
            except:
                # Fallback
                parsed.append(('px', 0))
                
    remaining_space = max(0, available_space - fixed_width - total_gap)
    fr_unit = remaining_space / total_fr if total_fr > 0 else 0
    
    final_widths = []
    for type, val in parsed:
        if type == 'px':
            final_widths.append(val)
        else:
            final_widths.append(val * fr_unit)
            
    return final_widths
