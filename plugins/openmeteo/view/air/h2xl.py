import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from plugins.openmeteo.lib.air_fetcher import fetch_air_quality
from plugins.openmeteo.view.air.utils import draw_air_cell
from modules.common_timezone import now_in_timezone

def generate_image(rotate=0, invert=False, tz=None, cmode=None, lat=None, lon=None, **kwargs):
    if not lat or not lon:
        lat = "52.52"  # fallback
        lon = "13.41"
    if not tz:
        tz = 'Asia/Shanghai'
        
    items = fetch_air_quality(lat, lon, tz)
    
    canvas, draw = create_canvas('h2xl', 'bwr', cmode=cmode) # 400x300
    
    font16 = get_font(16, get_root_font_path('font.ttf'))
    
    # Title Bar
    draw.text((16, 12), "空气污染物", font=font16, fill=(0,0,0))
    
    now_str = now_in_timezone(tz).strftime('%Y-%m-%d %H:%M')
    bbox_time = draw.textbbox((0,0), now_str, font=font16)
    time_w = bbox_time[2] - bbox_time[0]
    draw.text((400 - 16 - time_w, 12), now_str, font=font16, fill=(0,0,0))
    
    # Divider
    draw.line([(0, 40), (400, 40)], fill=(0,0,0), width=2)
    
    # Grid 2x4
    col_w = 200
    row_h = 65
    
    for i, item in enumerate(items[:8]):
        r = i // 2
        c = i % 2
        x = c * col_w
        y = 40 + r * row_h
        
        draw_air_cell(draw, x, y, col_w, row_h, item)
        
        # Grid lines
        if c == 0:
            draw.line([(x + col_w, y), (x + col_w, y + row_h)], fill=(0,0,0), width=1)
        if r < 3:
            draw.line([(x, y + row_h), (x + col_w, y + row_h)], fill=(0,0,0), width=1)
            
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
