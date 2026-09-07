from modules.generate_views.font_loader import get_font, get_root_font_path

def format_number(val):
    if val is None:
        return "0"
    v = float(val)
    if v >= 1000:
        return f"{int(v)}"
    elif v >= 100:
        # Keep 1 decimal place if it has one, but if it ends in .0, maybe just string formatting
        # the user asked "保留一位小数"
        res = f"{v:.1f}"
        return res.rstrip('0').rstrip('.') if '.' in res else res
    else:
        # "如果两位，则正常"
        # we can just convert to string, but trim to max 2 decimal places to be safe
        res = f"{v:.2f}"
        return res.rstrip('0').rstrip('.') if '.' in res else res

def draw_air_cell(draw, x, y, width, height, item_data):
    # Padding
    px, py = 8, 4
    
    font16 = get_font(16, get_root_font_path('font.ttf'))
    font32 = get_font(32, get_root_font_path('font.ttf'))
    
    name = item_data['name']
    unit = item_data.get('unit', '')
    
    # Format numerical values
    curr = format_number(item_data['current'])
    min_v = format_number(item_data['min'])
    max_v = format_number(item_data['max'])
    
    vals = item_data['hourly']
    
    bbox_name = draw.textbbox((0,0), name, font=font16)
    name_w = bbox_name[2] - bbox_name[0]
    
    bbox_unit = draw.textbbox((0,0), unit, font=font16)
    unit_w = bbox_unit[2] - bbox_unit[0]
    
    left_block_w = max(name_w, unit_w)
    
    # 1. Top-left: Name and Unit (stacked)
    draw.text((x + px, y + py), name, font=font16, fill=(0,0,0))
    if unit:
        draw.text((x + px, y + py + 16), unit, font=font16, fill=(0,0,0))
    
    # 2. Middle: Current (side by side with the name/unit block)
    draw.text((x + px + left_block_w + 8, y + py), curr, font=font32, fill=(0,0,0))
    
    # 3. Far-right: Max (top) and Min (bottom) stacked
    bbox_max = draw.textbbox((0,0), max_v, font=font16)
    bbox_min = draw.textbbox((0,0), min_v, font=font16)
    
    draw.text((x + width - px - (bbox_max[2] - bbox_max[0]), y + py), max_v, font=font16, fill=(255,0,0)) # Max string in RED to distinguish
    draw.text((x + width - px - (bbox_min[2] - bbox_min[0]), y + py + 16), min_v, font=font16, fill=(0,0,0))
    
    # 4. Bottom: Line Chart, occupying the full width and the bottom height
    chart_x_start = x + px
    chart_x_end = x + width - px
    chart_y_start = y + py + 34
    chart_y_end = y + height - py
    
    if vals and len(vals) > 0:
        valid_vals = [v for v in vals if v is not None]
        if not valid_vals:
            return
            
        v_min = min(valid_vals)
        v_max = max(valid_vals)
        v_rng = v_max - v_min
        if v_rng == 0:
            v_rng = 1
            
        cw = chart_x_end - chart_x_start
        ch = chart_y_end - chart_y_start
        
        pts = []
        for i, v in enumerate(vals[:24]):
            if v is None:
                continue
            cx = chart_x_start + (i / 23) * cw
            cy = chart_y_end - ((v - v_min) / v_rng) * ch
            pts.append((cx, cy))
            
        if len(pts) > 1:
            for i in range(len(pts)-1):
                draw.line([pts[i], pts[i+1]], fill=(255,0,0), width=2)
