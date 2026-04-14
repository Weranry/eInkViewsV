import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from plugins.openmeteo.lib.daily_fetcher import fetch_daily_weather
from plugins.openmeteo.view.now.utils import get_weather_info
from modules.common_timezone import now_in_timezone

def generate_image(rotate=0, invert=False, tz=None, cmode=None, lat=None, lon=None, **kwargs):
    if not lat or not lon:
        lat = "52.52"  # fallback
        lon = "13.41"
    if not tz:
        tz = 'Asia/Shanghai'
        
    days = fetch_daily_weather(lat, lon, tz)
    now_str = now_in_timezone(tz).strftime('%H:%M')
    
    canvas, draw = create_canvas('hxl', 'bwr', cmode=cmode) # 384x184
    
    from modules.generate_views.font_loader import get_font, get_root_font_path
    font16 = get_font(16, get_root_font_path('font.ttf'))
    font32 = get_font(32, get_root_font_path('font.ttf'))
    font_icon_64 = get_font(64, get_root_font_path('weather-icon.ttf'))
    
    py = 12
    time_w = draw.textbbox((0,0), now_str, font=font16)[2] - draw.textbbox((0,0), now_str, font=font16)[0]
    draw.text((384 - 16 - time_w, py), now_str, font=font16, fill=(0,0,0))
    # Line
    draw.line([(8, py + 24), (384 - 8, py + 24)], fill=(0,0,0), width=2)
    
    col_w = 384 / 5
    
    for i, d in enumerate(days):
        cx = i * col_w
        
        # Day
        weekday = d['weekday'] if i > 0 else "今天"
        wd_w = draw.textbbox((0,0), weekday, font=font16)[2] - draw.textbbox((0,0), weekday, font=font16)[0]
        draw.text((cx + (col_w - wd_w)/2, py + 30), weekday, font=font16, fill=(0,0,0))
        
        # Icon
        desc, icon_char = get_weather_info(d['code'])
        icon_w = draw.textbbox((0,0), icon_char, font=font_icon_64)[2] - draw.textbbox((0,0), icon_char, font=font_icon_64)[0]
        draw.text((cx + (col_w - icon_w)/2, py + 50), icon_char, font=font_icon_64, fill=(0,0,0))
        
        # Temp (High / Low)
        hi = f"{d['t_max']}°"
        lo = f"{d['t_min']}°"
        
        hi_w = draw.textbbox((0,0), hi, font=font16)[2] - draw.textbbox((0,0), hi, font=font16)[0]
        draw.text((cx + (col_w - hi_w)/2, py + 120), hi, font=font16, fill=(255,0,0))
        
        lo_w = draw.textbbox((0,0), lo, font=font16)[2] - draw.textbbox((0,0), lo, font=font16)[0]
        draw.text((cx + (col_w - lo_w)/2, py + 140), lo, font=font16, fill=(0,0,0))
        
        if i > 0:
            draw.line([(cx, py + 30), (cx, 184 - 8)], fill=(0,0,0), width=1)
            
    return finalize_image_common(canvas, rotate=rotate, invert=invert)