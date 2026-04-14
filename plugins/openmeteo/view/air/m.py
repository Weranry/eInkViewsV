import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from plugins.openmeteo.lib.air_fetcher import fetch_air_quality
from plugins.openmeteo.view.air.utils import format_number
from modules.common_timezone import now_in_timezone
from modules.errors.errors import ParamError

def generate_image(rotate=0, invert=False, tz=None, cmode=None, lat=None, lon=None, item='pm2_5', **kwargs):
    if not lat or not lon:
        lat = "52.52"  # fallback
        lon = "13.41"
    if not tz:
        tz = 'Asia/Shanghai'
        
    items = fetch_air_quality(lat, lon, tz)
    
    # default to the first if not found
    target_data = next((x for x in items if x and x['key'] == item), None)
    if not target_data:
        target_data = items[0]  # default to pm2_5 normally
        
    canvas, draw = create_canvas('m', 'bwr', cmode=cmode) # 200x200
    
    font16 = get_font(16, get_root_font_path('font.ttf'))
    font32 = get_font(32, get_root_font_path('font.ttf'))
    font48 = get_font(48, get_root_font_path('font.ttf'))
    font64 = get_font(64, get_root_font_path('font.ttf'))
    
    px = 12
    py = 12
    
    # 1. Update time (HH:MM) at top right
    now_str = now_in_timezone(tz).strftime('%H:%M')
    bbox_time = draw.textbbox((0,0), now_str, font=font16)
    time_w = bbox_time[2] - bbox_time[0]
    draw.text((200 - px - time_w, py), now_str, font=font16, fill=(0,0,0))
    
    # 2. Title and Unit (top left, same line)
    name = target_data['name']
    unit = target_data.get('unit', '')
    
    title_str = name
    if unit:
        title_str += f" ({unit})"
        
    draw.text((px, py), title_str, font=font16, fill=(0,0,0))
    
    # 4. Current Value (center-left big font, 48px)
    curr_str = format_number(target_data['current'])
    curr_font = font48
        
    bbox_curr = draw.textbbox((0,0), curr_str, font=curr_font)
    curr_w = bbox_curr[2] - bbox_curr[0]
    # Place roughly at middle vertically for the top half
    draw.text((px, 60), curr_str, font=curr_font, fill=(0,0,0))
    
    # 5. Min / Max Values (right side aligned, 32px)
    min_v = format_number(target_data['min'])
    max_v = format_number(target_data['max'])
    
    max_str = f"H {max_v}"
    min_str = f"L {min_v}"
    
    bbox_max = draw.textbbox((0,0), max_str, font=font32)
    bbox_min = draw.textbbox((0,0), min_str, font=font32)
    
    draw.text((200 - px - (bbox_max[2] - bbox_max[0]), 50), max_str, font=font32, fill=(255,0,0)) 
    draw.text((200 - px - (bbox_min[2] - bbox_min[0]), 90), min_str, font=font32, fill=(0,0,0))
    
    # 6. 24h Line chart (bottom full width, no margins on sides or bottom)
    chart_x_start = 0
    chart_x_end = 200
    chart_y_start = 140
    chart_y_end = 200
    
    vals = target_data['hourly']
    if vals and len(vals) > 0:
        valid_vals = [v for v in vals if v is not None]
        if valid_vals:
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
                    
    return finalize_image_common(canvas, rotate=rotate, invert=invert)